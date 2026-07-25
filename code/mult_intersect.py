"""Intersect the template-sweep hits across primes.

A hit is (v, phi, gam, del, eps, miss, one).  The only labelling freedom is
the choice of primitive root, which acts on ALL cubic-class indices by
j -> lambda*j (lambda in {1,2}; K_0 = cubes is canonical).  So the invariant
signature of a hit is the orbit of

    (cls(v), phi, gam, del, eps, miss, one)   in (Z_3)^7

under simultaneous multiplication by lambda.  Canonical representative: the
lexicographically smaller of the two.
"""
import re
import sys
from collections import defaultdict

PAT = re.compile(
    r"p=(\d+) HIT v=(\d+) cls\(v\)=(\d) phi=(\d) swap=(\d) gam=(\d) "
    r"del=(\d) eps=(\d) miss=(\d) one=(\d)")


def canon(t):
    a = tuple(t)
    b = tuple((2 * x) % 3 for x in t)
    return min(a, b)


def main(path):
    hits = defaultdict(set)
    done = []
    for line in open(path):
        m = PAT.search(line)
        if m:
            p = int(m.group(1))
            clsv, phi, swap, gam, de, eps, miss, one = map(int, m.groups()[2:])
            hits[p].add(canon((clsv, phi, gam, de, eps, miss, one)))
        if line.startswith("  p=") and "passed size" in line:
            done.append(int(line.split("=")[1].split(":")[0]))
    print(f"primes completed: {done}")
    for p in sorted(hits):
        print(f"  p={p}: {len(hits[p])} distinct signatures")
    common = None
    for p in done:
        common = hits[p] if common is None else common & hits[p]
    if common is None:
        return
    print(f"\nsignatures working at ALL of {done}: {len(common)}")
    hdr = "(cls(v), phi, gam, del, eps, miss, one)"
    print(f"  {hdr}")
    for s in sorted(common):
        print(f"  {s}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "log_template.txt")
