"""Per-solution structure sheet: the arithmetic fingerprint we mine later."""
from collections import Counter


def primitive_root(p):
    for g in range(2, p):
        seen, x = set(), 1
        for _ in range(p - 1):
            x = x * g % p
            seen.add(x)
        if len(seen) == p - 1:
            return g


def index_table(p):
    """Returns (g, ind) with g a primitive root and ind[x] = discrete log."""
    g = primitive_root(p)
    ind, x = {}, 1
    for k in range(p - 1):
        ind[x] = k
        x = x * g % p
    return g, ind


def structure_sheet(sol):
    p, t, h = sol.p, sol.t % sol.p, sol.h % sol.p
    g, ind = index_table(p)
    inv = {a: pow(a, p - 2, p) for a in range(1, p)}
    lines = [f"p={p} slope t={t} hole h={h} "
             f"(cycle A on coset {h}, B on {(-h) % p}; primitive root {g})"]
    owners = {}
    for o, a in sol.fixed.items():
        owners.setdefault(a, []).append(o)
    lines.append(f"fixed colors on cosets {sorted(owners)}; "
                 "orbits as (c,s) with AP-shape s/c and its cubic class:")
    for a in sorted(owners):
        descr = []
        for (c, s) in sorted(owners[a]):
            if c == 0:
                descr.append(f"(c=0,s={s})")
            else:
                sh = s * inv[c] % p
                descr.append(f"(c={c},s={s},shape={sh},cub{ind[sh] % 3})")
        lines.append(f"  coset {a}: " + " ".join(descr))
    lines.append(f"cycle A: {len(sol.A)} orbits; phases (c,s)->x0:")
    lines.append("  " + " ".join(f"({c},{s})->{sol.phase[(c, s)]}"
                                 for (c, s) in sorted(sol.A)))
    cub_s = Counter(ind[s] % 3 for (c, s) in sol.A)
    lines.append(f"  cubic classes of s over A: {dict(sorted(cub_s.items()))}")
    cub_c = Counter("c=0" if c == 0 else str(ind[c] % 3) for (c, s) in sol.A)
    lines.append(f"  cubic classes of c over A: {dict(sorted(cub_c.items()))}")
    return "\n".join(lines)
