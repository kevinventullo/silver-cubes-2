#!/usr/bin/env python3
"""Full pinned dihedral model as pure CNF, solved with CaDiCaL.

Same constraint system as model.py (CP-SAT), re-encoded for a dedicated
SAT solver: channel pht<->inA, one role per +/- orbit pair, footprint
partitions per owner, exact tiling for cycle A, optional Phi breaking.
Run detached; no in-process timeout (kill the process to stop).
"""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Cadical195

from core import (orbit_list, neg_orbit, footprint, Solution,
                  check_solution, build_cube, verify_cube, save_cube)


def build_cnf(p, t=1, h=1, phibreak=False):
    t %= p
    h %= p
    obs = orbit_list(p)
    hB = (-h) % p
    fixed_cosets = [a for a in range(p) if a not in (h, hB)]
    pool = IDPool()
    reps, rep_seen = [], set()
    for o in obs:
        if o in rep_seen:
            continue
        rep_seen.update((o, neg_orbit(o, p)))
        reps.append(o)

    repset = set(reps)

    def get_fix(o, a):
        if a in (h, hB) or a in footprint(o, p, t):
            return None
        if o in repset:
            return pool.id(("f", o, a))
        return pool.id(("f", neg_orbit(o, p), (-a) % p))

    inA = {o: pool.id(("A", o)) for o in obs}
    pht = {o: [pool.id(("x", o, r)) for r in range(p)] for o in obs}

    cls = []
    # channel: exactly one phase iff inA
    for o in obs:
        for r in range(p):
            cls.append([-pht[o][r], inA[o]])
        cls.append([-inA[o]] + pht[o])
        cls.extend(CardEnc.atmost(pht[o], 1, vpool=pool,
                                  encoding=EncType.ladder).clauses)
    # one role per +/- pair
    for o in reps:
        lits = [inA[o], inA[neg_orbit(o, p)]]
        lits += [v for a in fixed_cosets if (v := get_fix(o, a)) is not None]
        cls.extend(CardEnc.equals(lits, 1, vpool=pool,
                                  encoding=EncType.ladder).clauses)
    # footprint partition per owner (negation-representative owners)
    done = set()
    for a in fixed_cosets:
        if (-a) % p in done:
            continue
        done.add(a)
        for c in range(p):
            if c == a:
                continue
            lits = [v for o in obs if c in footprint(o, p, t)
                    and (v := get_fix(o, a)) is not None]
            cls.extend(CardEnc.equals(lits, 1, vpool=pool,
                                      encoding=EncType.ladder).clauses)
    # tiling of (Z_p)^2 minus (h, 0)
    for c in range(p):
        for r in range(p):
            lits = []
            for s in range(1, p):
                lits.append(pht[(c, s)][r])
                lits.append(pht[((c + t * s) % p, s)][(r + s) % p])
                lits.append(pht[((c - s) % p, s)][r])
            if (c, r) == (h, 0):
                cls.extend([-v] for v in lits)
            else:
                cls.extend(CardEnc.equals(lits, 1, vpool=pool,
                                          encoding=EncType.ladder).clauses)
    if phibreak:
        assert t == 1
        r0 = (p - 1) // 2
        for s in range((p + 1) // 2, p):
            cls.append([-pht[(0, s)][r0]])
            cls.append([-pht[(s % p, s)][(r0 + s) % p]])
            cls.append([-pht[((-s) % p, s)][r0]])

    handles = dict(p=p, t=t, h=h, obs=obs, repset=repset,
                   fixed_cosets=fixed_cosets, get_fix=get_fix,
                   inA=inA, pht=pht)
    return cls, handles


def decode(model_set, handles):
    p, t, h = handles["p"], handles["t"], handles["h"]
    fixed, A, phase = {}, set(), {}
    for o in handles["obs"]:
        if handles["inA"][o] in model_set:
            A.add(o)
            phase[o] = next(r for r in range(p)
                            if handles["pht"][o][r] in model_set)
        elif handles["inA"][neg_orbit(o, p)] not in model_set:
            owner = [a for a in handles["fixed_cosets"]
                     if (v := handles["get_fix"](o, a)) is not None
                     and v in model_set]
            assert len(owner) == 1, (o, owner)
            fixed[o] = owner[0]
    return Solution(p=p, t=t, h=h, fixed=fixed, A=A, phase=phase)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("p", type=int)
    ap.add_argument("--slope", type=int, default=1)
    ap.add_argument("--hole", type=int, default=1)
    ap.add_argument("--phibreak", action="store_true")
    args = ap.parse_args()
    p, t, h = args.p, args.slope % args.p, args.hole % args.p
    t0 = time.time()
    cls, handles = build_cnf(p, t, h, args.phibreak)
    print(f"CNF built: {len(cls)} clauses in {time.time()-t0:.1f}s"
          + (" (phibreak on)" if args.phibreak else ""), flush=True)
    with Cadical195(bootstrap_with=cls) as s:
        ok = s.solve()
        el = time.time() - t0
        print(f"result={'SAT' if ok else 'UNSAT'} time={el:.1f}s", flush=True)
        if not ok:
            sys.exit(2)
        model_set = set(l for l in s.get_model() if l > 0)
    sol = decode(model_set, handles)
    check_solution(sol)
    cube = build_cube(sol)
    assert not verify_cube(cube, p)
    print("verified: orbit level + full rainbow", flush=True)
    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "results")
    tag = f"p{p}_t{t}_h{h}_sat"
    with open(os.path.join(outdir, f"sol_{tag}.json"), "w") as f:
        f.write(sol.to_json() + "\n")
    save_cube(cube, sol, os.path.join(outdir, f"cube_{tag}.txt"))
    print(f"saved results/sol_{tag}.json and results/cube_{tag}.txt",
          flush=True)


if __name__ == "__main__":
    main()
