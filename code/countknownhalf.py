#!/usr/bin/env python3
"""Count (up to a cap) the cycle completions of a given fixed half at p=13+,
by clamping the half into the CP-SAT model and enumerating."""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ortools.sat.python import cp_model

from core import Solution, neg_orbit
from model import build_model


class Counter_(cp_model.CpSolverSolutionCallback):
    def __init__(self, cap):
        super().__init__()
        self.n = 0
        self.cap = cap
        self.t0 = time.time()

    def on_solution_callback(self):
        self.n += 1
        if self.n % 50 == 0:
            print(f"...{self.n} completions, {time.time() - self.t0:.0f}s",
                  flush=True)
        if self.cap and self.n >= self.cap:
            self.StopSearch()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("solfile")
    ap.add_argument("--cap", type=int, default=200)
    ap.add_argument("--timeout", type=float, default=0.0)
    args = ap.parse_args()
    sol = Solution.from_json(open(args.solfile).read())
    p, t, h = sol.p, sol.t, sol.h
    m, handles = build_model(p, t, h)
    get_fix, inA = handles["get_fix"], handles["inA"]
    done = set()
    for o, a in sol.fixed.items():
        if o in done:
            continue
        done.update((o, neg_orbit(o, p)))
        m.Add(get_fix(o, a) == 1)
    for o in handles["reps"]:
        if o not in sol.fixed:
            m.Add(inA[o] + inA[neg_orbit(o, p)] == 1)
    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.num_search_workers = 1
    if args.timeout:
        solver.parameters.max_time_in_seconds = args.timeout
    cb = Counter_(args.cap)
    status = solver.Solve(m, cb)
    name = solver.StatusName(status)
    capped = args.cap and cb.n >= args.cap
    print(f"p={p} known half: {cb.n} completions "
          f"{'(CAPPED)' if capped else '(' + name + ')'} "
          f"in {solver.WallTime():.0f}s")


if __name__ == "__main__":
    main()
