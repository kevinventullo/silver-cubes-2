"""Describe a saved solution's orbit sets in cubic-coset terms (no solver)."""
import json
import sys

from mult_block import arith


def describe(p, S, K):
    S = set(S)
    for j in range(3):
        for extra, tag in ((set(), ""), ({0}, " u {0}")):
            if S == K[j] | extra:
                return f"K_{j}{tag}"
    for j in range(3):
        if S == set(range(p)) - K[j]:
            return f"Z_p \\ K_{j}"
    if S == set(range(p)):
        return "Z_p (all)"
    if S == {0}:
        return "{0}"
    if not S:
        return "empty"
    inside = [f"K_{j}" for j in range(3) if K[j] <= S]
    return f"?size {len(S)} (contains {inside}, 0in={0 in S})"


def run(path):
    d = json.load(open(path))
    p = d["p"]
    cls, Kj, _ = arith(p)
    K = {j: set(Kj[j]) for j in range(3)}
    hA, hB = d.get("hA", 0), d.get("hB", 1)
    v = d.get("shape_index_v")
    A = {(c, s) for c, s, _ in d["A"]}
    B = {(c, s) for c, s, _ in d["B"]}
    fixed = {(c, s): a for c, s, a in d["fixed"]}
    print(f"{path}: p={p} v={v} cls(v)={cls[v] if v else '-'} m={(p-1)//3}")
    for nm, S, h in (("A", A, hA), ("B", B, hB)):
        print(f"  cycle {nm} (hole {h}):")
        for j in range(3):
            Ws = None
            ok = True
            for s in range(1, p):
                if cls[s] != j:
                    continue
                W = {((c - h) * pow(s, p - 2, p)) % p for (c, t) in S if t == s}
                if Ws is None:
                    Ws = W
                elif W != Ws:
                    ok = False
            print(f"    K_{j}: |W|={len(Ws)}  K-inv={ok}  ", end="")
            if v and 0 < len(Ws) < p:
                for vv, lab in ((v, "v"), ((-v) % p, "-v")):
                    print(f"[{lab}-W = {describe(p, {(vv - w) % p for w in Ws}, K)}] ",
                          end="")
            else:
                print(describe(p, Ws, K), end="")
            print()
    ws = {}
    for (c, s), a in fixed.items():
        ws.setdefault(a, set()).add((((c - a) * pow(s, p - 2, p)) % p, cls[s]))
    idx = sorted({w for v2 in ws.values() for w, _ in v2})
    print(f"  FIXED: {len(ws)} owners; indices used {idx}; "
          f"pure shape = {len(idx) <= 2}")
    for j in range(3):
        grp = sorted(a for a, s in ws.items() if all(jj == j for _, jj in s))
        if grp:
            wv = {w for a in grp for w, _ in ws[a]}
            print(f"    class K_{j}: index {sorted(wv)}, |centres|={len(grp)},"
                  f" centres = {describe(p, grp, K)}")


if __name__ == "__main__":
    for a in sys.argv[1:]:
        run(a)
        print(flush=True)
