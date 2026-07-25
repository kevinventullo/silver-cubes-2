#!/usr/bin/env python3
"""Per-half completability probe via pure SAT (cadical).

Given a nu-symmetric fixed half, the cycle question is an exact-1 cover:
pick one (orbit, phase) per leftover +/- pair so the tiles cover the torus
minus the hole exactly once. This encodes directly to CNF, where dedicated
SAT solvers are far stronger than CP-SAT enumeration search.

Modes:
  probe:  sample N random halves, report SAT/UNSAT/timeout per half.
          An UNSAT half is a counterexample to 'every half completes'.
  known:  test the fixed half of an existing solution JSON (sanity: SAT).
"""
import argparse
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pysat.card import CardEnc, EncType
from pysat.formula import IDPool
from pysat.solvers import Glucose42

from core import (orbit_list, neg_orbit, tile_cells, Solution,
                  check_solution, build_cube, verify_cube)
from fastcensus import fixed_halves


def leftover_pairs(p, assign):
    pairs, seen = [], set()
    for o in orbit_list(p):
        if o in assign or o in seen:
            continue
        no = neg_orbit(o, p)
        seen.update((o, no))
        pairs.append((o, no))
    return pairs


def tiling_cnf(p, t, h, pairs):
    pool = IDPool()
    hole = (h % p, 0)
    cover = {}   # cell -> [lit]
    bypair = []  # per pair: [lit]
    lit_info = {}
    for i, pr in enumerate(pairs):
        lits = []
        for o in pr:
            for x in range(p):
                cells = tile_cells(o, x, p, t)
                if hole in cells:
                    continue
                v = pool.id(("y", i, o, x))
                lit_info[v] = (i, o, x)
                lits.append(v)
                for cell in cells:
                    cover.setdefault(cell, []).append(v)
        bypair.append(lits)
    clauses = []
    for lits in bypair:
        clauses.extend(CardEnc.equals(
            lits, 1, vpool=pool, encoding=EncType.pairwise).clauses)
    for c in range(p):
        for r in range(p):
            if (c, r) == hole:
                continue
            lits = cover.get((c, r), [])
            clauses.extend(CardEnc.equals(
                lits, 1, vpool=pool, encoding=EncType.pairwise).clauses)
    return clauses, lit_info


def solve_half(p, t, h, assign, timeout=None, solver="glucose"):
    """Returns (status, solution_or_None, seconds).

    solver='glucose' supports wall-clock interrupts; 'cadical' is stronger
    but pysat gives it no interrupt API — use it under an external process
    timeout (see probe_burst.py)."""
    pairs = leftover_pairs(p, assign)
    clauses, lit_info = tiling_cnf(p, t, h, pairs)
    t0 = time.time()
    if solver == "cadical":
        from pysat.solvers import Cadical195 as Engine
        assert timeout is None, "cadical path has no in-process timeout"
    else:
        Engine = Glucose42
    with Engine(bootstrap_with=clauses) as s:
        if timeout:
            import threading
            timer = threading.Timer(timeout, s.interrupt)
            timer.start()
            ok = s.solve_limited(expect_interrupt=True)
            timer.cancel()
        else:
            ok = s.solve()
        el = time.time() - t0
        if ok is None:
            return "TIMEOUT", None, el
        if not ok:
            return "UNSAT", None, el
        model = set(l for l in s.get_model() if l > 0)
        A, phase = set(), {}
        for v, (i, o, x) in lit_info.items():
            if v in model:
                A.add(o)
                phase[o] = x
        sol = Solution(p=p, t=t, h=h, fixed=dict(assign), A=A, phase=phase)
        return "SAT", sol, el


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["probe", "known"])
    ap.add_argument("p", type=int, nargs="?")
    ap.add_argument("--solfile")
    ap.add_argument("--slope", type=int, default=1)
    ap.add_argument("--hole", type=int, default=1)
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--timeout-per", type=float, default=600.0)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()

    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "results")

    if args.mode == "known":
        sol = Solution.from_json(open(args.solfile).read())
        status, s2, el = solve_half(sol.p, sol.t, sol.h, sol.fixed,
                                    args.timeout_per)
        print(f"known half: {status} in {el:.1f}s")
        if s2:
            check_solution(s2)
            assert not verify_cube(build_cube(s2), sol.p)
            print("re-derived completion verified (orbit level + full cube)")
        return

    p, t, h = args.p, args.slope % args.p, args.hole % args.p
    rng = random.Random(args.seed)
    report = os.path.join(outdir, f"satprobe_p{p}_t{t}_h{h}.jsonl")
    tally = {"SAT": 0, "UNSAT": 0, "TIMEOUT": 0}
    with open(report, "w") as f:
        for i in range(args.n):
            assign = next(iter(fixed_halves(p, t, h, rng=rng)))
            status, sol, el = solve_half(p, t, h, assign, args.timeout_per)
            if sol is not None:
                check_solution(sol)
                bad = verify_cube(build_cube(sol), p)
                assert not bad
            tally[status] += 1
            rec = {"i": i, "status": status, "seconds": round(el, 2),
                   "half": sorted([c, s, a]
                                  for (c, s), a in assign.items())}
            f.write(json.dumps(rec) + "\n")
            f.flush()
            print(f"[{i + 1}/{args.n}] {status} in {el:.1f}s (tally {tally})",
                  flush=True)
            if status == "UNSAT":
                print("  ^^ COUNTEREXAMPLE half saved in report", flush=True)
    print(f"\nTOTAL {tally}")
    print(f"saved {report}")


if __name__ == "__main__":
    main()
