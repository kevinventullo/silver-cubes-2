"""Test ONLY the 18 candidate signatures (fitted at p = 13, 19) at a prime.

A canonical signature is (cls(v), phi, gam, del, eps, miss, one) with
cls(v) = 1; the labelling action is j -> lambda*j.  So at a prime, for each
transversal index v with cls(v) = k in {1,2}, the actual parameters are
k * (the canonical entries).

Far cheaper than the full block model: 18 signatures x 2 swaps x (#v),
each needing three small decoupled solves.
"""
import sys
import time

from mult_block import arith, transversal_indices
from mult_construct import phases, fixed_part_blocks
from mult_model import build_cube, verify
from mult_template import make


def signatures():
    S = []
    for phi in range(3):
        others = [j for j in range(3) if j != phi]
        for gam in others:
            for de, eps in [(others[0], others[1]), (others[1], others[0])]:
                for one in range(3):
                    ok = (one == (phi + de) % 3) if gam == de \
                        else (one != (phi + de) % 3)
                    if ok:
                        S.append((phi, gam, de, eps, (one + de - phi) % 3, one))
    return S


def run(p, tl=30.0):
    cls, Kj, _ = arith(p)
    K = {j: set(Kj[j]) for j in range(3)}
    n = (p * p - 1) // 3
    allo = {(c, s) for c in range(p) for s in range(1, p)}
    sig = signatures()
    print(f"=== p={p}: {len(sig)} signatures x 2 swaps x "
          f"{len([v for v in transversal_indices(p) if cls[v]])} indices",
          flush=True)
    t0 = time.time()
    for v in sorted(transversal_indices(p)):
        k = cls[v]
        for (phi0, gam0, de0, eps0, miss0, one0) in sig:
            phi, gam, de, eps, miss, one = [(k * z) % 3 for z in
                                            (phi0, gam0, de0, eps0, miss0, one0)]
            for swap in (0, 1):
                A, B = make(p, v, phi, swap, gam, de, eps, miss, one, cls, K)
                if len(A) != n or len(B) != n or (A & B):
                    continue
                pa = phases(p, 0, A, cls, tl)
                if pa is None:
                    continue
                pb = phases(p, 1, B, cls, tl)
                if pb is None:
                    continue
                fx = fixed_part_blocks(p, allo - A - B, 0, 1, cls, tl)
                if fx is None:
                    continue
                ok, _ = verify(build_cube(p, 0, 1, pa, pb, fx), p)
                print(f"  p={p} v={v} cls(v)={k} swap={swap} "
                      f"sig={(phi0,gam0,de0,eps0,miss0,one0)} -> "
                      f"{'*** VERIFIED ***' if ok else 'bad'}", flush=True)
                if ok:
                    return (v, swap, phi, gam, de, eps, miss, one, pa, pb, fx)
    print(f"  p={p}: no signature works ({time.time()-t0:.0f}s)", flush=True)
    return None


if __name__ == "__main__":
    sys.path.insert(0, "/Users/kevinventullo/SilverCube19AndBeyond/code")
    for p in [int(a) for a in sys.argv[1:]]:
        run(p)
