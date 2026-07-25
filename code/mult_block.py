"""THE REDUCED MODEL.  A silver (p,3)-cube, p = 1 mod 3, all of whose colour
classes are single K-orbits about their own diagonal coset (K = cubic
residues of Z_p^*, |K| = m = (p-1)/3), is exactly the following object.

BLOCKS.  For a in Z_p (centre), w in Z_p (index), j in Z_3 (cubic class) put
    Blk(a,w,j) = { orbit (a + w s, s) : s in K_j } ,   |Blk| = m,
where K_j is the j-th cubic coset.  The p(p-1) tau-orbits are partitioned by
the 3p^2 blocks in p different ways (one per centre).

A cube = a choice of 3p blocks partitioning all orbits, with
  * p+1 blocks centred at h_A = 0 and p+1 at h_B = 1 (the two cycle colours),
  * exactly one block at each of the other p-2 centres (the fixed colours),
  * [fixed colour a] its index w must be a TRANSVERSAL INDEX: w-1, w, w+1 in
    three distinct cubic cosets   (<=> Theorem-CosetBundles.md coset bundle),
  * [cycle colour] the p+1 blocks at that centre must carry phases making an
    exact cover: normalised, block (h,w,j) contributes one tile-class
    ((x, x-w), j), and the 3(p+1) cell-classes  (P^1 point, cubic level)
    must each be hit once.

Everything is now (p+1)-sized rather than p^3-sized.
"""
from collections import defaultdict

from ortools.sat.python import cp_model


def arith(p):
    g = next(a for a in range(2, p)
             if len({pow(a, k, p) for k in range(p - 1)}) == p - 1)
    cls = {pow(g, k, p): k % 3 for k in range(p - 1)}
    Kj = defaultdict(list)
    for v, j in cls.items():
        Kj[j].append(v)

    def cellclass(w):
        W1, W2 = w
        if W1:
            return ((1, W2 * pow(W1, p - 2, p) % p), cls[W1])
        return ((0, 1), cls[W2])

    return cls, Kj, cellclass


def transversal_indices(p):
    cls, _, _ = arith(p)
    return [w for w in range(p) if w not in (0, 1, p - 1)
            and len({cls[(w - 1) % p], cls[w], cls[(w + 1) % p]}) == 3]


def build(p, hA=0, hB=1):
    cls, Kj, cellclass = arith(p)
    tvs = set(transversal_indices(p))
    mo = cp_model.CpModel()

    blk = {}
    for a in range(p):
        for w in range(p):
            for j in range(3):
                if a in (hA, hB) or w in tvs:
                    blk[(a, w, j)] = mo.NewBoolVar(f"b{a}_{w}_{j}")

    # cycle colours: phases -> exact cover of the 3(p+1) cell-classes
    tile = {}
    for h in (hA, hB):
        cover = defaultdict(list)
        for w in range(p):
            for j in range(3):
                vs = []
                for x in range(p):
                    y = (x - w) % p
                    cs = [(x, y), ((x - 1) % p, y), (x, (y - 1) % p)]
                    if (0, 0) in cs:
                        continue
                    kk = [(cellclass(c)[0], (cellclass(c)[1] + j) % 3)
                          for c in cs]
                    if len(set(kk)) != 3:
                        continue
                    v = mo.NewBoolVar("")
                    tile[(h, w, j, x)] = v
                    vs.append(v)
                    for k in kk:
                        cover[k].append(v)
                mo.Add(sum(vs) == blk[(h, w, j)])
        for k, vs in cover.items():
            mo.AddExactlyOne(vs)
        assert len(cover) == 3 * (p + 1), (len(cover), 3 * (p + 1))

    # fixed colours: exactly one block per remaining centre
    for a in range(p):
        if a not in (hA, hB):
            mo.AddExactlyOne([blk[(a, w, j)] for w in tvs for j in range(3)])

    # every tau-orbit covered exactly once
    for c in range(p):
        for s in range(1, p):
            j = cls[s]
            terms = [blk[((c - w * s) % p, w, j)] for w in range(p)
                     if ((c - w * s) % p, w, j) in blk]
            mo.AddExactlyOne(terms)

    return mo, dict(p=p, hA=hA, hB=hB, blk=blk, tile=tile, cls=cls)


def to_solution(val, hs):
    """-> (A, B, fixed) in orbit coordinates, ready for joint.build_cube."""
    p, hA, hB, cls = hs["p"], hs["hA"], hs["hB"], hs["cls"]
    A, B, fixed = {}, {}, {}
    for (a, w, j), v in hs["blk"].items():
        if not val(v):
            continue
        Kjs = [s for s in range(1, p) if cls[s] == j]
        if a in (hA, hB):
            xs = [x for x in range(p) if (a, w, j, x) in hs["tile"]
                  and val(hs["tile"][(a, w, j, x)])]
            assert len(xs) == 1
            xn, yn = xs[0], (xs[0] - w) % p
            for s in Kjs:
                c = (a + w * s) % p
                # phase: X = s*xn in the (X,Y) frame centred at the hole,
                # and the row r equals X.
                (A if a == hA else B)[(c, s)] = (s * xn) % p
        else:
            for s in Kjs:
                fixed[((a + w * s) % p, s)] = a
    return A, B, fixed
