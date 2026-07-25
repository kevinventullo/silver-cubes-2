#!/usr/bin/env python3
"""Bespoke exhaustive census of the pinned dihedral model (small p).

Stage 1: backtracking enumeration of nu-symmetric fixed halves
         (owner 0 takes mirror-closed AP-pairs; owner pair {a,-a} takes
         mirrored partitions; orbits are consumed globally).
Stage 2: per fixed half, Algorithm-X exact-cover enumeration of cycle-A
         tilings: one orbit + phase per leftover +/- pair, tiles covering
         the torus minus the hole cell (h,0) exactly once.

Output lines identical to census.py: "<roles> <phases>" (base36), so the
CP-SAT census can cross-validate this enumerator and vice versa.
"""
import argparse
import json
import os
import sys
import time
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core import (orbit_list, neg_orbit, footprint, tile_cells,
                  Solution, check_solution)

B36 = "0123456789abcdefghijklmnopqrstuvwxyz"


# ---------------- Algorithm X (dict-of-sets dancing links) ----------------

def algox_solve(X, Y, solution):
    if not X:
        yield solution
    else:
        c = min(X, key=lambda k: len(X[k]))
        for r in list(X[c]):
            solution.append(r)
            cols = algox_select(X, Y, r)
            yield from algox_solve(X, Y, solution)
            algox_deselect(X, Y, r, cols)
            solution.pop()


def algox_select(X, Y, r):
    cols = []
    for j in Y[r]:
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].remove(i)
        cols.append(X.pop(j))
    return cols


def algox_deselect(X, Y, r, cols):
    for j in reversed(Y[r]):
        X[j] = cols.pop()
        for i in X[j]:
            for k in Y[i]:
                if k != j:
                    X[k].add(i)


# ---------------- Stage 1: nu-symmetric fixed halves ----------------

def fixed_halves(p, t, h, rng=None):
    """Yields dicts orbit -> owner coset (both halves, nu-symmetric).
    Pass rng to randomize DFS branch order (for sampling via next())."""
    owners = [a for a in range(p) if a not in (h, (p - h) % p)]
    assert 0 in owners
    pair_reps = sorted({min(a, p - a) for a in owners if a != 0})
    fps = {o: frozenset(footprint(o, p, t)) for o in orbit_list(p)}
    by_coset = {}
    for o, fp in fps.items():
        assert len(fp) == 3, "degenerate footprint (bad slope?)"
        for c in fp:
            by_coset.setdefault(c, []).append(o)

    assign = {}
    used = set()

    def cover0(remaining):
        """Owner 0: mirror-closed set; pick AP-pairs {o, -o}."""
        if not remaining:
            yield from cover_pair(0, None)
            return
        m = min(remaining)
        cands = by_coset[m] if rng is None else rng.sample(
            by_coset[m], len(by_coset[m]))
        for o in cands:
            if o in used:
                continue
            fp = fps[o]
            if 0 in fp:
                continue
            no = neg_orbit(o, p)
            nfp = fps[no]
            if fp & nfp:
                continue
            if not (fp <= remaining and nfp <= remaining):
                continue
            assign[o] = assign[no] = 0
            used.update((o, no))
            yield from cover0(remaining - fp - nfp)
            used.difference_update((o, no))
            del assign[o], assign[no]

    def cover_pair(idx, remaining):
        """Owner pair_reps[idx]; mirror goes to owner p - a."""
        if remaining is None:
            if idx == len(pair_reps):
                yield dict(assign)
                return
            a = pair_reps[idx]
            yield from cover_pair(idx, frozenset(set(range(p)) - {a}))
            return
        a = pair_reps[idx]
        if not remaining:
            yield from cover_pair(idx + 1, None)
            return
        m = min(remaining)
        cands = by_coset[m] if rng is None else rng.sample(
            by_coset[m], len(by_coset[m]))
        for o in cands:
            if o in used:
                continue
            fp = fps[o]
            if a in fp or not fp <= remaining:
                continue
            no = neg_orbit(o, p)
            assign[o] = a
            assign[no] = p - a
            used.update((o, no))
            yield from cover_pair(idx, remaining - fp)
            used.difference_update((o, no))
            del assign[o], assign[no]

    yield from cover0(frozenset(range(1, p)))


# ---------------- Stage 2: cycle tilings per fixed half ----------------

def cycle_exact_cover(p, t, h, leftover_pairs):
    """Yields lists of (pair_index, orbit, phase) rows forming a tiling."""
    hole = (h % p, 0)
    X = {("cell", c, r): set()
         for c in range(p) for r in range(p) if (c, r) != hole}
    for i in range(len(leftover_pairs)):
        X[("pair", i)] = set()
    Y = {}
    for i, pair in enumerate(leftover_pairs):
        for o in pair:
            for x in range(p):
                cells = tile_cells(o, x, p, t)
                if hole in cells:
                    continue
                Y[(i, o, x)] = [("pair", i)] + [("cell", c, r)
                                                for (c, r) in cells]
    for rid, cols in Y.items():
        for cc in cols:
            X[cc].add(rid)
    yield from algox_solve(X, Y, [])


# ---------------- Driver ----------------

def encode_line(p, assign, A, phase):
    roles, phases = [], []
    for o in orbit_list(p):
        if o in A:
            roles.append("A")
            phases.append(B36[phase[o]])
        elif o in assign:
            roles.append(B36[assign[o]])
        else:
            roles.append("B")
    return "".join(roles) + " " + "".join(phases)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("p", type=int)
    ap.add_argument("--slope", type=int, default=1)
    ap.add_argument("--hole", type=int, default=1)
    ap.add_argument("--cap", type=int, default=2000000,
                    help="max lines written (counting always continues)")
    ap.add_argument("--check-every", type=int, default=100000)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    p, t, h = args.p, args.slope % args.p, args.hole % args.p
    assert p <= 36

    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                          "..", "results")
    os.makedirs(outdir, exist_ok=True)
    out = args.out or os.path.join(outdir, f"fastcensus_p{p}_t{t}_h{h}.txt")

    obs = orbit_list(p)
    oidx = {o: i for i, o in enumerate(obs)}
    marg = [Counter() for _ in obs]
    fh_counts = []
    n = 0
    n_halves = 0
    t0 = time.time()

    with open(out, "w") as fh:
        for assign in fixed_halves(p, t, h):
            n_halves += 1
            leftover = [o for o in obs if o not in assign]
            pairs, seen = [], set()
            for o in leftover:
                if o in seen:
                    continue
                no = neg_orbit(o, p)
                seen.update((o, no))
                pairs.append((o, no))
            local = 0
            for rows in cycle_exact_cover(p, t, h, pairs):
                A = {o for (_, o, _) in rows}
                phase = {o: x for (_, o, x) in rows}
                n += 1
                local += 1
                line = encode_line(p, assign, A, phase)
                if n <= args.cap:
                    fh.write(line + "\n")
                for o in obs:
                    marg[oidx[o]][
                        "A" if o in A else
                        (B36[assign[o]] if o in assign else "B")] += 1
                if args.check_every and n % args.check_every == 0:
                    check_solution(Solution(p=p, t=t, h=h,
                                            fixed=dict(assign),
                                            A=A, phase=phase))
                    print(f"...{n} solutions ({n_halves} halves), "
                          f"{time.time() - t0:.0f}s", flush=True)
            fh_counts.append(local)

    el = time.time() - t0
    print(f"EXHAUSTIVE: {n} solutions from {n_halves} fixed halves "
          f"in {el:.1f}s")
    print(f"saved {out} ({min(n, args.cap)} lines)")
    backbone = [(obs[i], next(iter(cnt))) for i, cnt in enumerate(marg)
                if len(cnt) == 1]
    print(f"backbone (same role in every solution): "
          f"{len(backbone)} of {len(obs)} orbits")
    for o, r in backbone:
        role = ("cycle " + r) if r in "AB" else f"fixed@{B36.index(r)}"
        print(f"  orbit {o}: always {role}")
    nz = sorted((c for c in fh_counts if c), reverse=True)
    print(f"fixed halves: {n_halves} total, {len(nz)} completable")
    if nz:
        print(f"cycle completions per completable half: max={nz[0]} "
              f"min={nz[-1]} top5={nz[:5]}")
    stats = {
        "p": p, "t": t, "h": h, "count": n, "exhaustive": True,
        "n_fixed_halves": n_halves, "n_completable_halves": len(nz),
        "completions_per_half": nz,
        "backbone": [[list(o), r] for o, r in backbone],
        "seconds": el,
    }
    with open(out.replace(".txt", "_stats.json"), "w") as f:
        json.dump(stats, f, indent=1)
    print(f"saved {out.replace('.txt', '_stats.json')}")


if __name__ == "__main__":
    main()
