import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ortools.sat.python import cp_model
from core import check_solution, build_cube, verify_cube
from model import build_model, extract_solution

p = int(sys.argv[1]); workers = int(sys.argv[2])
m, handles = build_model(p, 1, 1)
bad = []
for (o, a), v in handles["fixvar"].items():
    if a != 0:
        continue
    c, s = o
    if c == 0 or (s * pow(c, p - 2, p)) % p not in (3, p - 3):
        bad.append(v)
m.Add(sum(bad) == 0)
print(f"p={p}: forbidding {len(bad)} non-shape-3 owner-0 assignments", flush=True)
solver = cp_model.CpSolver()
solver.parameters.num_search_workers = workers
t0 = time.time()
status = solver.Solve(m)
name = solver.StatusName(status)
print(f"status={name} time={time.time()-t0:.1f}s", flush=True)
if name in ("OPTIMAL", "FEASIBLE"):
    sol = extract_solution(solver.Value, handles)
    check_solution(sol)
    assert not verify_cube(build_cube(sol), p)
    shapes = sorted((s * pow(c, p - 2, p)) % p
                    for (c, s), a in sol.fixed.items() if a == 0)
    print(f"verified; sigma-color shapes: {shapes}", flush=True)
