import os, sys, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pysat.solvers import Cadical195
from core import Solution
from satprobe import leftover_pairs, tiling_cnf

sol = Solution.from_json(open(sys.argv[1]).read())
p, t, h = sol.p, sol.t, sol.h
pairs = leftover_pairs(p, sol.fixed)
clauses, lit_info = tiling_cnf(p, t, h, pairs)
print(f"known half of {sys.argv[1]}: {len(clauses)} clauses", flush=True)
t0 = time.time()
n = 0
with Cadical195(bootstrap_with=clauses) as s:
    while n < 200 and s.solve():
        n += 1
        if n == 1:
            print(f"FIRST completion found in {time.time()-t0:.1f}s", flush=True)
        if n % 10 == 0:
            print(f"...{n} completions, {time.time()-t0:.1f}s", flush=True)
        model = set(l for l in s.get_model() if l > 0)
        s.add_clause([-v for v in lit_info if v in model])
print(f"DONE: {'>=200' if n >= 200 else n} completions in {time.time()-t0:.1f}s", flush=True)
