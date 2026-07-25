#!/usr/bin/env python3
"""Mixed-shape nu-stable bundle analysis for the sigma-fixed color.

A bundle = partition of Z_p^* into centered 3-APs, closed under negation,
i.e. (p-1)/6 disjoint AP-pairs {A, -A}. Projectively: each pair covers 3
distinct +/- classes, so bundles = perfect matchings of the class set
P = {1..(p-1)/2} by 'AP-triples' counted with multiplicity mu(triple) =
number of AP-pairs realizing it.

Provides:
  count_bundles(p)      exact count via bitmask DP over P (feasible M<=24)
  enum_bundles(p)       explicit enumeration (use when count is moderate)
  orbit_report(p)       G = Z_p^*/{+-1} orbit and stabilizer spectrum
  interval_bundle(p)    the always-existing difference-1 bundle (p = 1 mod 3)
"""
import sys
from collections import Counter, defaultdict


def ap_pairs(p):
    """All AP-pairs {A,-A} with A,-A disjoint, 0 not in A.
    Returns dict: canonical pair key -> (frozenset A, class triple)."""
    out = {}
    for c in range(1, p):
        for s in range(1, (p - 1) // 2 + 1):
            A = ((c - s) % p, c, (c + s) % p)
            if 0 in A or len(set(A)) < 3:
                continue
            fA = frozenset(A)
            nA = frozenset((-x) % p for x in A)
            if fA & nA:
                continue
            key = min(tuple(sorted(fA)), tuple(sorted(nA)))
            cls = frozenset(min(x, p - x) for x in A)
            assert len(cls) == 3
            out[key] = (fA, cls)
    return out


def triple_table(p):
    """class-triple -> multiplicity, plus the pair lists per triple."""
    mu = defaultdict(list)
    for key, (fA, cls) in ap_pairs(p).items():
        mu[cls].append(key)
    return mu


def count_bundles(p):
    """Exact weighted count of bundles via DP on subsets of P."""
    M = (p - 1) // 2
    mu = triple_table(p)
    # triples containing each class, as (bitmask, weight)
    by_lowest = defaultdict(list)
    for cls, keys in mu.items():
        mask = 0
        for x in cls:
            mask |= 1 << (x - 1)
        by_lowest[min(cls)].append((mask, len(keys)))
    from functools import lru_cache
    full = (1 << M) - 1

    sys.setrecursionlimit(10000)
    memo = {}
    def rec(rem):
        if rem == 0:
            return 1
        if rem in memo:
            return memo[rem]
        low = (rem & -rem).bit_length()  # lowest uncovered class
        tot = 0
        for mask, w in by_lowest[low]:
            if mask & rem == mask:
                tot += w * rec(rem & ~mask)
        memo[rem] = tot
        return tot
    return rec(full)


def enum_bundles(p, cap=2000000):
    """Enumerate bundles as frozensets of pair keys."""
    mu = triple_table(p)
    by_lowest = defaultdict(list)
    for cls, keys in mu.items():
        by_lowest[min(cls)].append((cls, keys))
    M = (p - 1) // 2
    out = []
    def rec(rem, acc):
        if len(out) >= cap:
            return
        if not rem:
            out.append(frozenset(acc))
            return
        low = min(rem)
        for cls, keys in by_lowest[low]:
            if cls <= rem:
                for k in keys:
                    acc.append(k)
                    rec(rem - cls, acc)
                    acc.pop()
    rec(frozenset(range(1, M + 1)), [])
    return out


def scale_pair(key, alpha, p):
    A = frozenset(alpha * x % p for x in key)
    nA = frozenset((-x) % p for x in A)
    return min(tuple(sorted(A)), tuple(sorted(nA)))


def orbit_report(p, bundles):
    """Group bundles into G-orbits; return orbit stats."""
    reps = {b: None for b in bundles}
    G = [a for a in range(1, p) if 1 <= min(a, p - a) and a <= (p - 1) // 2]
    # G acts via alpha in 1..(p-1)/2 (alpha and -alpha act identically)
    orbits = []
    seen = set()
    bset = set(bundles)
    for b in bundles:
        if b in seen:
            continue
        orb = set()
        for alpha in range(1, (p - 1) // 2 + 1):
            img = frozenset(scale_pair(k, alpha, p) for k in b)
            assert img in bset, "G-action does not preserve bundle set!"
            orb.add(img)
        seen |= orb
        orbits.append(orb)
    return orbits


def shapes_of(bundle, p):
    sh = []
    for key in bundle:
        srt = sorted(key)
        # center = the element equal to average of other two
        for c in key:
            rest = [x for x in key if x != c]
            if (rest[0] + rest[1]) % p == 2 * c % p:
                s = (rest[1] - c) % p
                t = s * pow(c, p - 2, p) % p
                sh.append(min(t, p - t))
                break
    return tuple(sorted(sh))


def interval_bundle(p):
    assert p % 3 == 1
    keys = []
    for k in range((p - 1) // 3):
        A = (3 * k + 1, 3 * k + 2, 3 * k + 3)
        fA = frozenset(A)
        nA = frozenset((-x) % p for x in A)
        keys.append(min(tuple(sorted(fA)), tuple(sorted(nA))))
    b = frozenset(keys)
    # validate: pairs disjoint, cover Z_p^*, nu-stable by construction
    cov = set()
    for key in b:
        A = set(key)
        nA = {(-x) % p for x in A}
        assert not (A & nA) and not (cov & (A | nA))
        cov |= A | nA
    assert cov == set(range(1, p))
    return b


if __name__ == "__main__":
    import time
    for p in [int(x) for x in sys.argv[1:]] or [7, 13, 19, 31, 37, 43]:
        t0 = time.time()
        n = count_bundles(p)
        el = time.time() - t0
        iv = "interval-bundle OK" if interval_bundle(p) else "?"
        print(f"p={p}: B(p) = {n}  ({el:.1f}s; M={(p-1)//2}; {iv})", flush=True)
