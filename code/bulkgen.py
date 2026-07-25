#!/usr/bin/env python3
"""Accumulate a population of solutions for one (p,t,h) by running the free
CP-SAT model across random seeds. Each solution is verified, canonicalized
under the residual involution Phi, deduped, and appended as JSON lines."""
import argparse
import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ortools.sat.python import cp_model

from core import (Solution, check_solution, build_cube, verify_cube,
                  orbit_list)
from model import build_model, extract_solution


def phi_image(sol):
    p = sol.p
    fixed = {(c, (-s) % p): a for (c, s), a in sol.fixed.items()}
    A = {(c, (-s) % p) for (c, s) in sol.A}
    phase = {(c, (-s) % p): (c - x - 1) % p
             for (c, s), x in sol.phase.items()}
    return Solution(p=p, t=sol.t, h=sol.h, fixed=fixed, A=A, phase=phase)


def canon_key(sol):
    a = sol.to_json()
    b = phi_image(sol).to_json()
    return min(a, b)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("p", type=int)
    ap.add_argument("--slope", type=int, default=1)
    ap.add_argument("--hole", type=int, default=1)
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--timeout-per", type=float, default=1800.0)
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--seed0", type=int, default=100)
    args = ap.parse_args()
    p, t, h = args.p, args.slope % args.p, args.hole % args.p

    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "results")
    out = os.path.join(outdir, f"pop_p{p}_t{t}_h{h}.jsonl")
    seen = set()
    if os.path.exists(out):
        for line in open(out):
            seen.add(canon_key(Solution.from_json(line)))
        print(f"resuming: {len(seen)} solutions already in {out}", flush=True)

    m, handles = build_model(p, t, h)
    for i in range(args.n):
        seed = args.seed0 + i
        solver = cp_model.CpSolver()
        solver.parameters.num_search_workers = args.workers
        solver.parameters.max_time_in_seconds = args.timeout_per
        solver.parameters.random_seed = seed
        solver.parameters.randomize_search = True
        t0 = time.time()
        status = solver.Solve(m)
        name = solver.StatusName(status)
        el = time.time() - t0
        if name not in ("OPTIMAL", "FEASIBLE"):
            print(f"[seed {seed}] {name} in {el:.0f}s", flush=True)
            continue
        sol = extract_solution(solver.Value, handles)
        check_solution(sol)
        assert not verify_cube(build_cube(sol), p)
        key = canon_key(sol)
        fresh = key not in seen
        if fresh:
            seen.add(key)
            with open(out, "a") as f:
                f.write(sol.to_json() + "\n")
        print(f"[seed {seed}] solution in {el:.0f}s "
              f"({'new' if fresh else 'dup'}; population {len(seen)})",
              flush=True)


if __name__ == "__main__":
    main()
