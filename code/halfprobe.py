#!/usr/bin/env python3
"""Test the 'every fixed half completes' conjecture at a given prime.

Samples random nu-symmetric fixed halves (randomized DFS), clamps each into
the CP-SAT dihedral model, and asks for a cycle completion. At p=7 the
exhaustive census shows all 680 halves complete; this probes whether that
survives at larger p.
"""
import argparse
import json
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ortools.sat.python import cp_model

from core import (neg_orbit, check_solution, build_cube, verify_cube)
from model import build_model, extract_solution
from fastcensus import fixed_halves


def probe_half(p, t, h, assign, workers, timeout):
    m, handles = build_model(p, t, h)
    get_fix, inA = handles["get_fix"], handles["inA"]
    done = set()
    for o, a in assign.items():
        if o in done:
            continue
        done.update((o, neg_orbit(o, p)))
        m.Add(get_fix(o, a) == 1)
    for o in handles["reps"]:
        if o not in assign:
            m.Add(inA[o] + inA[neg_orbit(o, p)] == 1)
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = workers
    solver.parameters.max_time_in_seconds = timeout
    status = solver.Solve(m)
    name = solver.StatusName(status)
    sol = None
    if name in ("OPTIMAL", "FEASIBLE"):
        sol = extract_solution(solver.Value, handles)
    return name, sol


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("p", type=int)
    ap.add_argument("--slope", type=int, default=1)
    ap.add_argument("--hole", type=int, default=1)
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--timeout-per", type=float, default=300.0)
    ap.add_argument("--seed", type=int, default=1)
    args = ap.parse_args()
    p, t, h = args.p, args.slope % args.p, args.hole % args.p
    rng = random.Random(args.seed)

    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "results")
    os.makedirs(outdir, exist_ok=True)
    report = os.path.join(outdir, f"halfprobe_p{p}_t{t}_h{h}.jsonl")

    counts = {"SAT": 0, "INFEASIBLE": 0, "UNKNOWN": 0}
    t0 = time.time()
    with open(report, "w") as f:
        for i in range(args.n):
            assign = next(iter(fixed_halves(p, t, h, rng=rng)))
            ts = time.time()
            name, sol = probe_half(p, t, h, assign, args.workers,
                                   args.timeout_per)
            el = time.time() - ts
            if sol is not None:
                check_solution(sol)
                bad = verify_cube(build_cube(sol), p)
                assert not bad
                counts["SAT"] += 1
            else:
                counts[name if name == "INFEASIBLE" else "UNKNOWN"] += 1
            rec = {"i": i, "status": name, "seconds": round(el, 2),
                   "half": sorted([c, s, a]
                                  for (c, s), a in assign.items())}
            f.write(json.dumps(rec) + "\n")
            f.flush()
            print(f"[{i + 1}/{args.n}] {name} in {el:.1f}s "
                  f"(tally {counts})", flush=True)
    print(f"\nTOTAL {counts} in {time.time() - t0:.0f}s")
    print(f"saved {report}")


if __name__ == "__main__":
    main()
