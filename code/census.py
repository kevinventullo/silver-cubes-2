#!/usr/bin/env python3
"""Enumerate pinned-dihedral solutions (small p); save compactly; mine basics.

Line format: <roles> <phases>
  roles:  one char per orbit in orbit_list order: 'A', 'B', or base36 owner coset
  phases: one base36 char per cycle-A orbit, in orbit_list order
"""
import argparse
import json
import os
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ortools.sat.python import cp_model

from core import Solution, orbit_list, neg_orbit, check_solution
from model import build_model

B36 = "0123456789abcdefghijklmnopqrstuvwxyz"


def encode(cb, handles):
    p = handles["p"]
    obs, fixed_cosets = handles["obs"], handles["fixed_cosets"]
    inA, pht, get_fix = handles["inA"], handles["pht"], handles["get_fix"]
    roles, phases = [], []
    for o in obs:
        if cb.Value(inA[o]):
            roles.append("A")
            x = next(r for r in range(p) if cb.Value(pht[o][r]))
            phases.append(B36[x])
        elif cb.Value(inA[neg_orbit(o, p)]):
            roles.append("B")
        else:
            a = next(a for a in fixed_cosets
                     if (v := get_fix(o, a)) is not None and cb.Value(v))
            roles.append(B36[a])
    return "".join(roles) + " " + "".join(phases)


def decode(line, p, t, h):
    roles, phases = line.split()
    fixed, A, phase = {}, set(), {}
    it = iter(phases)
    for o, r in zip(orbit_list(p), roles):
        if r == "A":
            A.add(o)
            phase[o] = B36.index(next(it))
        elif r != "B":
            fixed[o] = B36.index(r)
    return Solution(p=p, t=t, h=h, fixed=fixed, A=A, phase=phase)


class Collector(cp_model.CpSolverSolutionCallback):
    def __init__(self, handles, fh, cap, check_every):
        super().__init__()
        self.handles, self.fh, self.cap = handles, fh, cap
        self.check_every = check_every
        self.n = 0
        self.t0 = time.time()

    def on_solution_callback(self):
        line = encode(self, self.handles)
        self.fh.write(line + "\n")
        self.n += 1
        if self.check_every and self.n % self.check_every == 0:
            h = self.handles
            check_solution(decode(line, h["p"], h["t"], h["h"]))
        if self.n % 100000 == 0:
            print(f"...{self.n} solutions, {time.time() - self.t0:.0f}s",
                  flush=True)
        if self.cap and self.n >= self.cap:
            self.StopSearch()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("p", type=int)
    ap.add_argument("--slope", type=int, default=1)
    ap.add_argument("--hole", type=int, default=1)
    ap.add_argument("--cap", type=int, default=1000000)
    ap.add_argument("--check-every", type=int, default=50000)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    p, t, h = args.p, args.slope % args.p, args.hole % args.p
    assert p <= 36, "compact base36 encoding assumes p <= 36"

    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "results")
    os.makedirs(outdir, exist_ok=True)
    out = args.out or os.path.join(outdir, f"enum_p{p}_t{t}_h{h}.txt")

    m, handles = build_model(p, t, h)
    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    solver.parameters.num_search_workers = 1
    t0 = time.time()
    with open(out, "w") as fh:
        coll = Collector(handles, fh, args.cap, args.check_every)
        status = solver.Solve(m, coll)
    el = time.time() - t0
    capped = args.cap and coll.n >= args.cap
    print(f"status={solver.StatusName(status)} solutions={coll.n} "
          f"{'(CAPPED)' if capped else '(exhaustive)'} time={el:.0f}s")
    print(f"saved {out}")

    # basic mining: per-orbit role marginals, backbone, fixed-half census
    obs = orbit_list(p)
    marg = [Counter() for _ in obs]
    fixed_halves = Counter()
    n = 0
    for line in open(out):
        roles, _ = line.split()
        n += 1
        for i, r in enumerate(roles):
            marg[i][r] += 1
        fixed_halves["".join(c if c not in "AB" else "." for c in roles)] += 1
    backbone = [(obs[i], next(iter(cnt))) for i, cnt in enumerate(marg)
                if len(cnt) == 1]
    print(f"\nsolutions read: {n}")
    print(f"backbone (orbits with the same role in every solution): "
          f"{len(backbone)} of {len(obs)}")
    for o, r in backbone:
        role = ("cycle " + r) if r in "AB" else f"fixed@{B36.index(r)}"
        print(f"  orbit {o}: always {role}")
    counts = sorted(fixed_halves.values(), reverse=True)
    print(f"distinct fixed-half configurations: {len(fixed_halves)}")
    if counts:
        print(f"cycle completions per fixed half: max={counts[0]} "
              f"min={counts[-1]} "
              f"top5={counts[:5]}")
    stats = {
        "p": p, "t": t, "h": h, "count": n, "capped": bool(capped),
        "n_fixed_halves": len(fixed_halves),
        "backbone": [[list(o), r] for o, r in backbone],
    }
    with open(out.replace(".txt", "_stats.json"), "w") as f:
        json.dump(stats, f, indent=1)
    print(f"saved {out.replace('.txt', '_stats.json')}")


if __name__ == "__main__":
    main()
