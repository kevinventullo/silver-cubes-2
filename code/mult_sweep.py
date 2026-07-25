"""Overnight sweep: block model, pure-shape arms, increasing primes.

For each prime p = 1 mod 3 and each transversal shape index v (mod +-),
solve the block model restricted to fixed blocks with w in {v,-v}.
On success: rebuild the cube, verify it, write results/.
"""
import itertools
import json
import os
import sys
import time

from ortools.sat.python import cp_model

from mult_block import build, to_solution, transversal_indices
from mult_model import build_cube, verify

OUT = "/Users/kevinventullo/SilverCube19AndBeyond/results"


def emit(p, hs, A, B, fixed, v):
    col = build_cube(p, hs["hA"], hs["hB"], A, B, fixed)
    ok, bad = verify(col, p)
    if not ok:
        print(f"  !! verification FAILED at {bad}", flush=True)
        return False
    json.dump({"p": p, "hA": hs["hA"], "hB": hs["hB"], "shape_index_v": v,
               "A": [[c, s, x] for (c, s), x in A.items()],
               "B": [[c, s, x] for (c, s), x in B.items()],
               "fixed": [[c, s, a] for (c, s), a in fixed.items()]},
              open(f"{OUT}/sol_p{p}_block.json", "w"))
    with open(f"{OUT}/cube_p{p}_block.txt", "w") as f:
        f.write(f"# silver ({p},3)-cube, colors={3*p-2}\n")
        f.write(f"# every colour class is one K-orbit (K = cubic residues) about\n")
        f.write(f"# its own diagonal coset; cycle holes {hs['hA']},{hs['hB']}; "
                f"fixed shape index v={v}\n")
        f.write(f"# diagonal x+y+z=0 mod {p}; lines: x y z color\n")
        for x, y, z in itertools.product(range(p), repeat=3):
            f.write(f"{x} {y} {z} {col[(x, y, z)]}\n")
    print(f"  ** SILVER ({p},3)-CUBE VERIFIED -> results/cube_p{p}_block.txt",
          flush=True)
    return True


def attempt(p, budget, workers, seed=0):
    reps = sorted({min(w, p - w) for w in transversal_indices(p)})
    for v in reps:
        mo, hs = build(p)
        for (a, w, j), var in hs["blk"].items():
            if a not in (0, 1) and w not in (v, p - v):
                mo.Add(var == 0)
        sv = cp_model.CpSolver()
        sv.parameters.max_time_in_seconds = budget
        sv.parameters.num_workers = workers
        sv.parameters.random_seed = seed
        t0 = time.time()
        st = sv.StatusName(sv.Solve(mo))
        print(f"  p={p} v={v}: {st} ({time.time()-t0:.0f}s)", flush=True)
        if st in ("OPTIMAL", "FEASIBLE"):
            A, B, fixed = to_solution(sv.Value, hs)
            if emit(p, hs, A, B, fixed, v):
                return True
    return False


if __name__ == "__main__":
    budget = float(os.environ.get("BUDGET", 1800))
    workers = int(os.environ.get("WORKERS", 6))
    for p in [int(a) for a in sys.argv[1:]]:
        if os.path.exists(f"{OUT}/cube_p{p}_block.txt"):
            print(f"p={p} already done", flush=True)
            continue
        print(f"=== p={p} (tau={len(transversal_indices(p))//2} shapes)",
              flush=True)
        t0 = time.time()
        ok = attempt(p, budget, workers)
        print(f"=== p={p}: {'SOLVED' if ok else 'no verdict'} "
              f"in {time.time()-t0:.0f}s", flush=True)
