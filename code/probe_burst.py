#!/usr/bin/env python3
"""Parallel per-half completability probes with CaDiCaL under external
process timeouts. Each worker samples one random nu-symmetric fixed half
and solves its tiling CNF unbounded; the parent kills stragglers.

An UNSAT result is a counterexample to 'every fixed half completes'.
"""
import argparse
import json
import multiprocessing as mp
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import check_solution, build_cube, verify_cube
from fastcensus import fixed_halves
from satprobe import solve_half


def worker(seed, p, t, h, outpath, count_cap=200):
    """Decide completability AND count completions (blocking clauses) up to
    count_cap. Writes progressive JSON so a timeout kill preserves the
    count lower bound found so far."""
    from pysat.solvers import Cadical195
    from satprobe import leftover_pairs, tiling_cnf
    from core import Solution

    rng = random.Random(seed)
    assign = next(iter(fixed_halves(p, t, h, rng=rng)))
    rec = {"seed": seed, "status": "RUNNING", "count_so_far": 0,
           "done": False, "seconds": 0.0,
           "half": sorted([c, s, a] for (c, s), a in assign.items())}
    def flush():
        with open(outpath + ".tmp", "w") as f:
            json.dump(rec, f)
        os.replace(outpath + ".tmp", outpath)
    flush()
    t0 = time.time()
    pairs = leftover_pairs(p, assign)
    clauses, lit_info = tiling_cnf(p, t, h, pairs)
    n = 0
    with Cadical195(bootstrap_with=clauses) as s:
        while n < count_cap and s.solve():
            model = set(l for l in s.get_model() if l > 0)
            chosen = [v for v in lit_info if v in model]
            if n == 0:
                A, phase = set(), {}
                for v in chosen:
                    _, o, x = lit_info[v]
                    A.add(o)
                    phase[o] = x
                sol = Solution(p=p, t=t, h=h, fixed=dict(assign),
                               A=A, phase=phase)
                check_solution(sol)
                assert not verify_cube(build_cube(sol), p)
                rec["first_solution_verified"] = True
            n += 1
            rec.update(status="SAT", count_so_far=n,
                       seconds=round(time.time() - t0, 1))
            if n % 5 == 0 or n == 1:
                flush()
            s.add_clause([-v for v in chosen])
    rec.update(seconds=round(time.time() - t0, 1), done=True,
               status="UNSAT" if n == 0 else "SAT",
               count=(n if n < count_cap else f">={count_cap}"))
    flush()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("p", type=int)
    ap.add_argument("--slope", type=int, default=1)
    ap.add_argument("--hole", type=int, default=1)
    ap.add_argument("--n", type=int, default=12)
    ap.add_argument("--par", type=int, default=4)
    ap.add_argument("--timeout-per", type=float, default=3600.0)
    ap.add_argument("--seed0", type=int, default=1000)
    ap.add_argument("--count-cap", type=int, default=200)
    args = ap.parse_args()
    p, t, h = args.p, args.slope % args.p, args.hole % args.p

    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "results", f"burst_p{p}_t{t}_h{h}")
    os.makedirs(outdir, exist_ok=True)

    seeds = list(range(args.seed0, args.seed0 + args.n))
    pending = list(seeds)
    running = {}  # proc -> (seed, start, outpath)
    tally = {"SAT": 0, "UNSAT": 0, "TIMEOUT": 0}
    t0 = time.time()
    while pending or running:
        while pending and len(running) < args.par:
            seed = pending.pop(0)
            outpath = os.path.join(outdir, f"half_{seed}.json")
            pr = mp.Process(target=worker,
                            args=(seed, p, t, h, outpath, args.count_cap))
            pr.start()
            running[pr] = (seed, time.time(), outpath)
        time.sleep(5)
        for pr in list(running):
            seed, start, outpath = running[pr]
            timed_out = time.time() - start > args.timeout_per
            if pr.is_alive() and not timed_out:
                continue
            if pr.is_alive():
                pr.terminate()
            pr.join()
            del running[pr]
            rec = json.load(open(outpath)) if os.path.exists(outpath) else {}
            status = rec.get("status", "RUNNING")
            cnt = rec.get("count", rec.get("count_so_far", 0))
            if status == "SAT":
                tally["SAT"] += 1
                extra = "" if rec.get("done") else " (count is a lower bound; timed out)"
                print(f"[seed {seed}] SAT, completions {cnt}{extra}, "
                      f"{rec.get('seconds', '?')}s (tally {tally})", flush=True)
            elif status == "UNSAT":
                tally["UNSAT"] += 1
                print(f"[seed {seed}] UNSAT — COUNTEREXAMPLE: {outpath} "
                      f"(tally {tally})", flush=True)
            else:
                tally["TIMEOUT"] += 1
                print(f"[seed {seed}] TIMEOUT with no verdict "
                      f"(tally {tally})", flush=True)
    print(f"\nTOTAL {tally} in {(time.time() - t0) / 60:.0f} min")


if __name__ == "__main__":
    main()
