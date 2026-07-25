"""Joint model: tau-equivariant silver cube with MULTIPLICATIVELY SYMMETRIC
cycle classes.  Slope t = 1 throughout.

Coordinates (coset c, row r).  The tile of orbit (c,s) at phase x covers
cells (c,x), (c-s,x-s), (c+s,x).   [= the corner triple {(X,Y),(X-s,Y),(X,Y-s)}
after (X,Y) = (x, x-c); the hole then sits at the origin.]

tau-equivariant solution = holes h_A != h_B, cycle A tiles Z_p^2 - {(h_A,0)},
cycle B tiles Z_p^2 - {(h_B,0)}, A and B disjoint orbit sets, and the
remaining (p-1)(p-2)/3 orbits partition into bundles, one per owner coset
a not in {h_A,h_B}, whose footprints {c-s,c,c+s} partition Z_p - {a}.

NEW ANSATZ: the map (c,r) -> (h + alpha(c-h), alpha r) sends tiles to tiles
and fixes the hole (h,0), so each cycle's tiling admits a Z_p^* scaling
symmetry about ITS OWN hole.  (It is not a symmetry of the whole cube -- the
two holes get moved to each other -- which is why the dihedral models never
saw it.)  Impose invariance under the subgroup H of order m.
Requires m | p-1 and 3 | (p-1)/m; the maximal choice is m = (p-1)/3,
H = the cubic residues, valid for EVERY p = 1 mod 3.
"""
import itertools
from collections import defaultdict

from ortools.sat.python import cp_model


def subgroup(p, m):
    assert (p - 1) % m == 0, (p, m)
    g = next(a for a in range(2, p)
             if len({pow(a, k, p) for k in range(p - 1)}) == p - 1)
    return sorted({pow(pow(g, (p - 1) // m, p), k, p) for k in range(m)})


def tile_cells(p, c, s, x):
    return ((c % p, x % p), ((c - s) % p, (x - s) % p), ((c + s) % p, x % p))


def build(p, mA, mB, hA=0, hB=1, mfix=0):
    """mA/mB = order of the scaling subgroup imposed on cycle A/B (1 = free).
    mfix = order of the scaling subgroup imposed on each FIXED colour's bundle
    about its own owner coset (0 = free).  mfix = (p-1)/3 makes every fixed
    bundle a single K-orbit, i.e. a *coset bundle* in the sense of
    Theorem-CosetBundles.md -- then EVERY colour class of the cube is one
    K-orbit family about its own diagonal coset."""
    orbs = [(c, s) for c in range(p) for s in range(1, p)]
    fp = {o: ((o[0] - o[1]) % p, o[0], (o[0] + o[1]) % p) for o in orbs}
    mo = cp_model.CpModel()
    ph, inX, cell = {}, {}, {}

    for tag, h in (("A", hA), ("B", hB)):
        ph[tag] = {o: [mo.NewBoolVar(f"{tag}{o}_{x}") for x in range(p)]
                   for o in orbs}
        inX[tag] = {o: mo.NewBoolVar(f"in{tag}{o}") for o in orbs}
        cell[tag] = defaultdict(list)
        for o in orbs:
            mo.Add(sum(ph[tag][o]) == inX[tag][o])
            for x in range(p):
                for cl in tile_cells(p, o[0], o[1], x):
                    if cl == (h, 0):
                        mo.Add(ph[tag][o][x] == 0)
                    else:
                        cell[tag][cl].append(ph[tag][o][x])
        for c in range(p):
            for r in range(p):
                if (c, r) != (h, 0):
                    mo.AddExactlyOne(cell[tag][(c, r)])

    # multiplicative symmetry: equalities between phase variables
    for tag, h, m in (("A", hA, mA), ("B", hB, mB)):
        if m <= 1:
            continue
        for a in subgroup(p, m)[1:]:
            for (c, s) in orbs:
                for x in range(p):
                    c2, s2, x2 = (h + a * (c - h)) % p, a * s % p, a * x % p
                    mo.Add(ph[tag][(c, s)][x] == ph[tag][(c2, s2)][x2])

    owners = [a for a in range(p) if a not in (hA, hB)]
    fix = {(o, a): mo.NewBoolVar("") for o in orbs for a in owners
           if a not in fp[o]}
    for o in orbs:
        mo.AddExactlyOne([inX["A"][o], inX["B"][o]]
                         + [fix[(o, a)] for a in owners if (o, a) in fix])
    for a in owners:
        for d in range(p):
            if d != a:
                mo.AddExactlyOne([fix[(o, a)] for o in orbs
                                  if (o, a) in fix and d in fp[o]])

    if mfix > 1:
        for al in subgroup(p, mfix)[1:]:
            for a in owners:
                for (c, s) in orbs:
                    o2 = ((a + al * (c - a)) % p, al * s % p)
                    if ((c, s), a) in fix and (o2, a) in fix:
                        mo.Add(fix[((c, s), a)] == fix[(o2, a)])

    return mo, dict(p=p, hA=hA, hB=hB, orbs=orbs, ph=ph, inX=inX, fix=fix,
                    owners=owners)


def extract(val, hs):
    p, orbs = hs["p"], hs["orbs"]
    A = {o: x for o in orbs for x in range(p)
         if val(hs["ph"]["A"][o][x])}
    B = {o: x for o in orbs for x in range(p)
         if val(hs["ph"]["B"][o][x])}
    fixed = {o: a for o in orbs for a in hs["owners"]
             if (o, a) in hs["fix"] and val(hs["fix"][(o, a)])}
    return A, B, fixed


def build_cube(p, hA, hB, A, B, fixed):
    cc = {a: 2 * p + i for i, a in enumerate(sorted(set(fixed.values())))}
    col = {}
    for x, y, z in itertools.product(range(p), repeat=3):
        s, c = (x + y + z) % p, (x - y) % p
        if s == 0:
            col[(x, y, z)] = (x if c == hA else p + x if c == hB else cc[c])
        else:
            o = (c, s)
            col[(x, y, z)] = (cc[fixed[o]] if o in fixed else
                              (x - A[o]) % p if o in A else
                              p + (x - B[o]) % p)
    return col


def verify(col, p):
    want = list(range(3 * p - 2))
    for x, y, z in itertools.product(range(p), repeat=3):
        if (x + y + z) % p:
            continue
        cs = ([col[(x, y, z)]]
              + [col[(u, y, z)] for u in range(p) if u != x]
              + [col[(x, u, z)] for u in range(p) if u != y]
              + [col[(x, y, u)] for u in range(p) if u != z])
        if sorted(cs) != want:
            return False, (x, y, z)
    return True, None
