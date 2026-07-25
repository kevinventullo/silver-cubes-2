#!/usr/bin/env python3
"""Solve the pinned dihedral model for one (p, slope, hole); verify and save."""
import argparse
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ortools.sat.python import cp_model

from core import (check_solution, build_cube, verify_cube,
                  check_equivariance, save_cube)
from model import build_model, extract_solution
from extract import structure_sheet


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("p", type=int)
    ap.add_argument("--slope", type=int, default=1)
    ap.add_argument("--hole", type=int, default=1)
    ap.add_argument("--workers", type=int, default=8)
    ap.add_argument("--timeout", type=float, default=0.0)
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--progress", action="store_true")
    ap.add_argument("--phibreak", action="store_true",
                    help="halve the search space via the Phi involution "
                         "(slope t=1 only; see NOTES.md)")
    ap.add_argument("--outdir", default=None)
    args = ap.parse_args()

    p, t, h = args.p, args.slope % args.p, args.hole % args.p
    if p % 3 != 1:
        print(f"note: p={p} is {p % 3} mod 3; the equivariant model is "
              "provably infeasible unless p = 1 mod 3 (expect INFEASIBLE)",
              flush=True)
    outdir = args.outdir or os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "results")
    os.makedirs(outdir, exist_ok=True)

    t0 = time.time()
    m, handles = build_model(p, t, h, phibreak=args.phibreak)
    print(f"model built in {time.time() - t0:.1f}s"
          + (" (phibreak on)" if args.phibreak else ""), flush=True)

    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = args.workers
    solver.parameters.random_seed = args.seed
    if args.timeout:
        solver.parameters.max_time_in_seconds = args.timeout
    if args.progress:
        solver.parameters.log_search_progress = True
    status = solver.Solve(m)
    el = time.time() - t0
    name = solver.StatusName(status)
    print(f"status={name} time={el:.1f}s", flush=True)
    if name not in ("OPTIMAL", "FEASIBLE"):
        sys.exit(2 if name == "INFEASIBLE" else 3)

    sol = extract_solution(solver.Value, handles)
    check_solution(sol)
    print("orbit-level checks: OK", flush=True)
    cube = build_cube(sol)
    bad = verify_cube(cube, p)
    print(f"full rainbow verification: {p * p} diagonal vertices, "
          f"{len(bad)} failures", flush=True)
    assert not bad
    assert check_equivariance(cube, sol)
    print("dihedral equivariance at all vertices: OK", flush=True)

    tag = f"p{p}_t{t}_h{h}"
    spath = os.path.join(outdir, f"sol_{tag}.json")
    cpath = os.path.join(outdir, f"cube_{tag}.txt")
    with open(spath, "w") as f:
        f.write(sol.to_json() + "\n")
    save_cube(cube, sol, cpath)
    print(f"saved {spath}", flush=True)
    print(f"saved {cpath}", flush=True)
    print(structure_sheet(sol), flush=True)


if __name__ == "__main__":
    main()
