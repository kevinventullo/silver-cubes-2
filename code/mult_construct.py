"""EXPLICIT CONSTRUCTION.

Read off the block solutions at p = 7, 13, 19.  Notation: K_0,K_1,K_2 the
cubic cosets of Z_p^* (K_0 = cubes, -1 in K_0 always), m = (p-1)/3, and v a
TRANSVERSAL INDEX (v-1, v, v+1 in three distinct cosets; these exist for
every p = 1 mod 3 by Theorem-CosetBundles.md).  Put jv = cubic class of v,
and let {alpha, beta} = the two classes other than jv.  Then, with the two
cycle holes at cosets 0 and 1, the orbit sets are

  A = { (c,s) : s in K_alpha }                      (all p orbits of one
      u { (-v s, s) : s in K_jv }                    defect class + 1 block)

  B = { (1 + (-v-d) s, s) : s in K_beta, d not in K_alpha }
      u { (1 + (-v-d) s, s) : s in K_jv,  d in K_jv u {0} }

and everything left over is the fixed colours (each a coset bundle of
shape 1/v).  Sizes: |A| = |B| = m(p+1) = (p^2-1)/3, leftover m(p-2).

Given A and B as orbit sets the problem DECOUPLES into three small
independent pieces: phases for A, phases for B, fixed decomposition.
"""
import sys

from ortools.sat.python import cp_model

from mult_block import arith, transversal_indices
from mult_model import build_cube, verify


def make_AB(p, v, alpha, cls, K):
    jv = cls[v]
    beta = ({0, 1, 2} - {jv, alpha}).pop()
    A = {(c, s) for s in range(1, p) if cls[s] == alpha for c in range(p)}
    A |= {((-v * s) % p, s) for s in range(1, p) if cls[s] == jv}
    B = set()
    for s in range(1, p):
        if cls[s] == beta:
            ds = [d for d in range(p) if d not in K[alpha]]
        elif cls[s] == jv:
            ds = [0] + sorted(K[jv])
        else:
            continue
        for d in ds:
            B.add(((1 + (-v - d) * s) % p, s))
    return A, B, beta, jv


def phases(p, hole, orbset, cls, tl=60.0):
    """K-invariant phases: one normalised phase x per BLOCK; the orbit
    (hole + w s, s) of that block then sits at row s*x."""
    blocks = {}
    for (c, s) in orbset:
        w = ((c - hole) * pow(s, p - 2, p)) % p
        blocks.setdefault((w, cls[s]), []).append((c, s))
    mo = cp_model.CpModel()
    cover, ph = {}, {}
    for b, os_ in blocks.items():
        ph[b] = [mo.NewBoolVar("") for _ in range(p)]
        mo.AddExactlyOne(ph[b])
        for x in range(p):
            for (c, s) in os_:
                r = (s * x) % p
                for cl in ((c, r), ((c - s) % p, (r - s) % p),
                           ((c + s) % p, r)):
                    cover.setdefault(cl, []).append(ph[b][x])
    for c in range(p):
        for r in range(p):
            t = cover.get((c, r), [])
            if (c, r) == (hole, 0):
                for lit in t:
                    mo.Add(lit == 0)
            else:
                mo.AddExactlyOne(t)
    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = tl
    sv.parameters.num_workers = 4
    if sv.Solve(mo) not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None
    out = {}
    for b, os_ in blocks.items():
        x = next(x for x in range(p) if sv.Value(ph[b][x]))
        for (c, s) in os_:
            out[(c, s)] = (s * x) % p
    return out


def fixed_part(p, rest, hA, hB, tl=60.0):
    fp = {o: ((o[0] - o[1]) % p, o[0], (o[0] + o[1]) % p) for o in rest}
    owners = [a for a in range(p) if a not in (hA, hB)]
    mo = cp_model.CpModel()
    x = {(o, a): mo.NewBoolVar("") for o in rest for a in owners
         if a not in fp[o]}
    for o in rest:
        mo.AddExactlyOne([x[(o, a)] for a in owners if (o, a) in x])
    for a in owners:
        for d in range(p):
            if d != a:
                mo.AddExactlyOne([x[(o, a)] for o in rest
                                  if (o, a) in x and d in fp[o]])
    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = tl
    sv.parameters.num_workers = 4
    if sv.Solve(mo) not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None
    return {o: a for o in rest for a in owners
            if (o, a) in x and sv.Value(x[(o, a)])}


def attempt(p, v, alpha, cls, K, verbose=True):
    n = (p * p - 1) // 3
    A, B, beta, jv = make_AB(p, v, alpha, cls, K)
    tag = f"p={p} v={v} (cls(v)={jv}) alpha={alpha} beta={beta}"
    if len(A) != n or len(B) != n or (A & B):
        if verbose:
            print(f"  {tag}: sizes/disjointness fail "
                  f"(|A|={len(A)} |B|={len(B)} |A&B|={len(A & B)})")
        return None
    allo = {(c, s) for c in range(p) for s in range(1, p)}
    pa = phases(p, 0, A, cls)
    if pa is None:
        print(f"  {tag}: NO A-phases"); return None
    pb = phases(p, 1, B, cls)
    if pb is None:
        print(f"  {tag}: NO B-phases"); return None
    fx = fixed_part(p, allo - A - B, 0, 1)
    if fx is None:
        print(f"  {tag}: NO fixed decomposition"); return None
    ok, bad = verify(build_cube(p, 0, 1, pa, pb, fx), p)
    print(f"  {tag}: {'*** VERIFIED SILVER CUBE ***' if ok else f'BAD {bad}'}",
          flush=True)
    return (pa, pb, fx) if ok else None


if __name__ == "__main__":
    for p in [int(a) for a in sys.argv[1:]] or [7, 13, 19]:
        cls, Kj, _ = arith(p)
        K = {j: set(Kj[j]) for j in range(3)}
        reps = sorted(transversal_indices(p))
        print(f"=== p={p}  transversal indices {reps}", flush=True)
        for v in reps:
            for alpha in range(3):
                if alpha == cls[v]:
                    continue
                attempt(p, v, alpha, cls, K)


def fixed_part_blocks(p, rest, hA, hB, cls, tl=60.0):
    """Fixed decomposition RESPECTING the block structure: each owner's bundle
    must be a single K-orbit Blk(a,w,j) = {(a+ws,s) : s in K_j} with w a
    transversal index.  Tiny exact cover (p-2 owners x 3*tau(p) candidates)
    -- and the right notion, since the whole ansatz is that every colour is
    one K-orbit.  The generic fixed_part() above ignores this and is both
    slower and (at p >= 31) unable to decide in reasonable time."""
    from mult_block import transversal_indices
    tvs = transversal_indices(p)
    owners = [a for a in range(p) if a not in (hA, hB)]
    rest = set(rest)
    cand = {}
    for a in owners:
        for w in tvs:
            for j in range(3):
                blk = {((a + w * s) % p, s) for s in range(1, p)
                       if cls[s] == j}
                if blk <= rest:
                    cand[(a, w, j)] = blk
    mo = cp_model.CpModel()
    x = {k: mo.NewBoolVar("") for k in cand}
    for a in owners:
        ks = [k for k in cand if k[0] == a]
        if not ks:
            return None
        mo.AddExactlyOne([x[k] for k in ks])
    byorb = {}
    for k, blk in cand.items():
        for o in blk:
            byorb.setdefault(o, []).append(x[k])
    for o in rest:
        if o not in byorb:
            return None
        mo.AddExactlyOne(byorb[o])
    sv = cp_model.CpSolver()
    sv.parameters.max_time_in_seconds = tl
    sv.parameters.num_workers = 4
    if sv.Solve(mo) not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return None
    return {o: k[0] for k, blk in cand.items() if sv.Value(x[k])
            for o in blk}
