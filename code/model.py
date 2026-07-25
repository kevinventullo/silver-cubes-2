"""CP-SAT pinned dihedral model. Conventions: core.py / ../NOTES.md."""
from ortools.sat.python import cp_model

from core import orbit_list, neg_orbit, footprint, Solution


def orbit_pairs(p):
    rep_of, reps = {}, []
    for o in orbit_list(p):
        if o in rep_of:
            continue
        rep_of[o] = o
        rep_of[neg_orbit(o, p)] = o
        reps.append(o)
    return rep_of, reps


def build_model(p, t=1, h=1, phibreak=False):
    t %= p
    h %= p
    assert t not in (0, p - 1), "slope t must avoid {0, -1} mod p"
    assert h != 0, "hole must be a nonzero coset"
    m = cp_model.CpModel()
    obs = orbit_list(p)
    hB = (-h) % p
    fixed_cosets = [a for a in range(p) if a not in (h, hB)]
    rep_of, reps = orbit_pairs(p)

    # fix[(o, a)] for representative orbits only; the nu-partner's assignment
    # (neg o -> -a) shares the same variable.
    fixvar = {}
    for o in reps:
        fp = footprint(o, p, t)
        for a in fixed_cosets:
            if a not in fp:
                fixvar[(o, a)] = m.NewBoolVar(f"f_{o[0]}_{o[1]}_{a}")

    def get_fix(o, a):
        v = fixvar.get((o, a))
        if v is None:
            v = fixvar.get((neg_orbit(o, p), (-a) % p))
        return v

    inA = {o: m.NewBoolVar(f"A_{o[0]}_{o[1]}") for o in obs}
    pht = {o: [m.NewBoolVar(f"x_{o[0]}_{o[1]}_{r}") for r in range(p)]
           for o in obs}

    for o in obs:
        m.Add(sum(pht[o]) == inA[o])

    # each +/- orbit pair takes exactly one role
    for o in reps:
        cands = [inA[o], inA[neg_orbit(o, p)]]
        cands += [v for a in fixed_cosets if (v := get_fix(o, a)) is not None]
        m.Add(sum(cands) == 1)

    # fixed color owning coset a: footprints partition Z_p - {a}
    # (constraints for owner -a are the same after variable identification)
    done = set()
    for a in fixed_cosets:
        if (-a) % p in done:
            continue
        done.add(a)
        for c in range(p):
            if c == a:
                continue
            terms = []
            for o in obs:
                if c in footprint(o, p, t):
                    v = get_fix(o, a)
                    if v is not None:
                        terms.append(v)
            m.Add(sum(terms) == 1)

    # cycle-A tiling: cover (Z_p)^2 minus {(h, 0)} exactly once.
    # cell (c, r) is covered by orbit (c,s) phase r   [middle corner],
    # orbit (c+ts, s) phase r+s [left corner], orbit (c-s, s) phase r [right].
    for c in range(p):
        for r in range(p):
            terms = []
            for s in range(1, p):
                terms.append(pht[(c, s)][r])
                terms.append(pht[((c + t * s) % p, s)][(r + s) % p])
                terms.append(pht[((c - s) % p, s)][r])
            m.Add(sum(terms) == (0 if (c, r) == (h, 0) else 1))

    # Optional Phi symmetry breaking (valid only for slope t=1, where the
    # coordinate swap iota commutes with tau). Phi acts freely on pinned
    # solutions (see NOTES.md), mapping the tile that covers the Phi-fixed
    # cell e0 = (0, (p-1)/2) to its partner with s negated; forcing the
    # covering tile to have s in {1..(p-1)/2} keeps exactly one solution
    # per Phi-pair.
    if phibreak:
        assert t == 1, "Phi symmetry breaking derived for slope t=1 only"
        c0, r0 = 0, (p - 1) // 2
        for s in range((p + 1) // 2, p):
            m.Add(pht[(c0, s)][r0] == 0)                          # middle
            m.Add(pht[((c0 + t * s) % p, s)][(r0 + s) % p] == 0)  # left
            m.Add(pht[((c0 - s) % p, s)][r0] == 0)                # right

    handles = dict(p=p, t=t, h=h, obs=obs, reps=reps,
                   fixed_cosets=fixed_cosets, fixvar=fixvar,
                   get_fix=get_fix, inA=inA, pht=pht)
    return m, handles


def extract_solution(value, handles):
    """value: BoolVar -> 0/1 (solver.Value or callback.Value)."""
    p, t, h = handles["p"], handles["t"], handles["h"]
    obs, fixed_cosets = handles["obs"], handles["fixed_cosets"]
    get_fix, inA, pht = handles["get_fix"], handles["inA"], handles["pht"]
    fixed, A, phase = {}, set(), {}
    for o in obs:
        if value(inA[o]):
            A.add(o)
            xs = [r for r in range(p) if value(pht[o][r])]
            assert len(xs) == 1, (o, xs)
            phase[o] = xs[0]
        elif not value(inA[neg_orbit(o, p)]):
            owners = [a for a in fixed_cosets
                      if (v := get_fix(o, a)) is not None and value(v)]
            assert len(owners) == 1, (o, owners)
            fixed[o] = owners[0]
    return Solution(p=p, t=t, h=h, fixed=fixed, A=A, phase=phase)
