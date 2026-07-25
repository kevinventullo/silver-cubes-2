#!/usr/bin/env python3
"""Independent silver-cube verifier. Deliberately self-contained: imports
nothing from the rest of the codebase, so it cannot share a bug with it.

Usage: verify.py cube.txt
File: '#' comment lines, then lines "x y z color" covering (Z_p)^3 exactly
once (p inferred from the line count). Checks that for every diagonal vertex
v (x+y+z = 0 mod p) the closed neighborhood N[v] -- v plus the 3(p-1)
vertices differing from it in exactly one coordinate -- carries every color
0..3p-3 exactly once.
"""
import sys
from itertools import product


def main(path):
    col = {}
    for line in open(path):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        x, y, z, c = map(int, line.split())
        col[(x, y, z)] = c
    p = round(len(col) ** (1 / 3))
    assert len(col) == p ** 3, f"expected a full cube, got {len(col)} entries"
    assert set(col) == set(product(range(p), repeat=3)), "vertex set wrong"
    q = 3 * p - 2
    assert all(0 <= c < q for c in col.values()), "color out of range"
    want = list(range(q))
    ndiag = 0
    bad = []
    for x, y, z in product(range(p), repeat=3):
        if (x + y + z) % p:
            continue
        ndiag += 1
        colors = [col[(x, y, z)]]
        colors += [col[(u, y, z)] for u in range(p) if u != x]
        colors += [col[(x, u, z)] for u in range(p) if u != y]
        colors += [col[(x, y, u)] for u in range(p) if u != z]
        if sorted(colors) != want:
            bad.append((x, y, z))
    print(f"p={p} colors={q} diagonal_vertices={ndiag} (expect {p * p}) "
          f"rainbow_failures={len(bad)}")
    if bad:
        print("first failures:", bad[:5])
    if ndiag != p * p or bad:
        print("VERDICT: NOT SILVER")
        sys.exit(1)
    print("VERDICT: SILVER CUBE VERIFIED")


if __name__ == "__main__":
    main(sys.argv[1])
