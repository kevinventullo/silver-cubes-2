"""Silver (p,3)-cube core machinery. Conventions: see ../NOTES.md.

Quick recap:
* orbit (c, s): tau-orbit of corner triples; c = coset (t*x - y) of the middle
  corner, s = defect. Footprint (corner cosets) = {c - t*s, c, c + s}.
* In (coset,row) cells the triple of orbit (c,s) at row x covers
  {(c, x), (c - t*s, x - s), (c + s, x)}.
* Dihedral pinned solution: fixed[-o] = -fixed[o]; B = -A;
  triple of o in A at row x has color a_{x - phase[o]};
  triple of -o in B at row x has color b_{x + phase[o]}.
* Colors: a_j = j, b_j = p + j, fixed color of coset a = 2p + rank(a).
"""
import itertools
import json
from collections import Counter
from dataclasses import dataclass


def orbit_list(p):
    return [(c, s) for c in range(p) for s in range(1, p)]


def neg_orbit(o, p):
    c, s = o
    return ((-c) % p, (-s) % p)


def footprint(o, p, t=1):
    c, s = o
    return ((c - t * s) % p, c % p, (c + s) % p)


def tile_cells(o, x0, p, t=1):
    c, s = o
    return ((c % p, x0 % p), ((c - t * s) % p, (x0 - s) % p),
            ((c + s) % p, x0 % p))


@dataclass
class Solution:
    p: int
    t: int
    h: int
    fixed: dict  # orbit -> owning coset (nu-symmetric, both halves present)
    A: set       # orbits in cycle A
    phase: dict  # orbit in A -> row x0 of its a_0-colored triple

    def to_json(self):
        return json.dumps({
            "p": self.p, "t": self.t, "h": self.h,
            "fixed": sorted([c, s, a] for (c, s), a in self.fixed.items()),
            "A": sorted([c, s] for (c, s) in self.A),
            "phase": sorted([c, s, x] for (c, s), x in self.phase.items()),
        })

    @staticmethod
    def from_json(txt):
        d = json.loads(txt)
        return Solution(
            p=d["p"], t=d["t"], h=d["h"],
            fixed={(c, s): a for c, s, a in d["fixed"]},
            A={(c, s) for c, s in d["A"]},
            phase={(c, s): x for c, s, x in d["phase"]},
        )


def check_solution(sol):
    """Combinatorial validity of the orbit-level dihedral solution."""
    p, t, h = sol.p, sol.t % sol.p, sol.h % sol.p
    allo = set(orbit_list(p))
    B = {neg_orbit(o, p) for o in sol.A}
    fx = set(sol.fixed)
    assert not (sol.A & B), "A meets -A"
    assert not ((sol.A | B) & fx), "cycle orbits meet fixed orbits"
    assert sol.A | B | fx == allo, "roles do not cover all orbits"
    for o, a in sol.fixed.items():
        assert sol.fixed[neg_orbit(o, p)] == (-a) % p, "fixed half not nu-symmetric"
    owners = {}
    for o, a in sol.fixed.items():
        owners.setdefault(a, []).append(o)
    assert set(owners) == set(range(p)) - {h, (-h) % p}, "owner cosets wrong"
    for a, os in owners.items():
        cov = Counter()
        for o in os:
            fp = footprint(o, p, t)
            assert len(set(fp)) == 3 and a not in fp, (a, o, fp)
            cov.update(fp)
        assert all(cov[c] == (0 if c == a else 1) for c in range(p)), \
            f"fixed color {a}: footprints do not partition Z_p - {{{a}}}"
    cov = Counter()
    for o in sol.A:
        cov.update(tile_cells(o, sol.phase[o], p, t))
    for c in range(p):
        for r in range(p):
            want = 0 if (c, r) == (h, 0) else 1
            assert cov[(c, r)] == want, f"tiling defect at cell {(c, r)}"
    return True


def fixed_color_map(sol):
    fixed_cosets = sorted(set(sol.fixed.values()))
    return {a: 2 * sol.p + i for i, a in enumerate(fixed_cosets)}


def build_cube(sol):
    """Full coloring of (Z_p)^3 from an orbit-level solution."""
    p, t, h = sol.p, sol.t % sol.p, sol.h % sol.p
    hB = (-h) % p
    cc = fixed_color_map(sol)
    col = {}
    for x, y, z in itertools.product(range(p), repeat=3):
        s = (x + y + z) % p
        c = (t * x - y) % p
        if s == 0:
            if c == h:
                col[(x, y, z)] = x
            elif c == hB:
                col[(x, y, z)] = p + x
            else:
                col[(x, y, z)] = cc[c]
        else:
            o = (c, s)
            if o in sol.fixed:
                col[(x, y, z)] = cc[sol.fixed[o]]
            elif o in sol.A:
                col[(x, y, z)] = (x - sol.phase[o]) % p
            else:
                col[(x, y, z)] = p + (x + sol.phase[neg_orbit(o, p)]) % p
    return col


def verify_cube(col, p):
    """Direct rainbow check; returns the list of bad diagonal vertices."""
    q = 3 * p - 2
    want = list(range(q))
    bad = []
    for x, y, z in itertools.product(range(p), repeat=3):
        if (x + y + z) % p:
            continue
        colors = [col[(x, y, z)]]
        colors += [col[(u, y, z)] for u in range(p) if u != x]
        colors += [col[(x, u, z)] for u in range(p) if u != y]
        colors += [col[(x, y, u)] for u in range(p) if u != z]
        if sorted(colors) != want:
            bad.append((x, y, z))
    return bad


def check_equivariance(col, sol):
    """Confirm c(tau v) = rho(c(v)) and c(-v) = sigma(c(v)) at all vertices."""
    p, t = sol.p, sol.t % sol.p
    cc = fixed_color_map(sol)
    inv_cc = {v: k for k, v in cc.items()}

    def rho(k):
        if k < p:
            return (k + 1) % p
        if k < 2 * p:
            return p + (k - p + 1) % p
        return k

    def sigma(k):
        if k < p:
            return p + (-k) % p
        if k < 2 * p:
            return (-(k - p)) % p
        return cc[(-inv_cc[k]) % p]

    for x, y, z in itertools.product(range(p), repeat=3):
        k = col[(x, y, z)]
        if col[((x + 1) % p, (y + t) % p, (z - 1 - t) % p)] != rho(k):
            return False
        if col[((-x) % p, (-y) % p, (-z) % p)] != sigma(k):
            return False
    return True


def save_cube(col, sol, path):
    p = sol.p
    with open(path, "w") as f:
        f.write(f"# silver ({p},3)-cube, colors={3 * p - 2}, "
                f"dihedral model slope t={sol.t} hole h={sol.h}\n")
        f.write(f"# diagonal: x+y+z = 0 (mod {p}); lines: x y z color\n")
        for x, y, z in itertools.product(range(p), repeat=3):
            f.write(f"{x} {y} {z} {col[(x, y, z)]}\n")
