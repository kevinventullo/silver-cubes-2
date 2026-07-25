"""THE CONSTRUCTION TEMPLATE, swept over all its discrete parameters.

Every block solution examined (p = 13, 19, 31, 37) has the same three-piece
shape.  With u = -v (v a transversal index), K_j the cubic cosets:

  cycle FULL  = { (h + w s, s) : s in K_phi, w in Z_p }        (p blocks)
              u { (h + u s, s) : s in K_gam }                  (1 block)
  cycle OTHER = { (h' + (u-d) s, s) : s in K_del, d not in K_miss }  (2m+1)
              u { (h' + (u-d) s, s) : s in K_eps, d in K_one u {0} } (m+1)

with {h, h'} = {0, 1} and phi, gam, del, eps in Z_3, del != eps != phi != gam.
Only the class assignment differed between primes -- so sweep it and look for
the invariant rule.
"""
import itertools
import sys
import time

from ortools.sat.python import cp_model

from mult_block import arith, transversal_indices
from mult_construct import phases, fixed_part_blocks
from mult_model import build_cube, verify


def make(p, v, phi, swap, gam, dele, eps, miss, one, cls, K):
    u = (-v) % p
    hF, hO = (1, 0) if swap else (0, 1)
    F = {((hF + w * s) % p, s) for s in range(1, p) if cls[s] == phi
         for w in range(p)}
    F |= {((hF + u * s) % p, s) for s in range(1, p) if cls[s] == gam}
    O = set()
    for s in range(1, p):
        if cls[s] == dele:
            ds = [d for d in range(p) if d not in K[miss]]
        elif cls[s] == eps:
            ds = [0] + sorted(K[one])
        else:
            continue
        for d in ds:
            O.add(((hO + (u - d) * s) % p, s))
    A, B = (O, F) if swap else (F, O)
    return A, B


def sweep(p, tl=120.0, verbose=False):
    cls, Kj, _ = arith(p)
    K = {j: set(Kj[j]) for j in range(3)}
    n = (p * p - 1) // 3
    allo = {(c, s) for c in range(p) for s in range(1, p)}
    hits, nsize = [], 0
    vs = sorted(transversal_indices(p))
    for v in vs:
        for phi in range(3):
            others = [j for j in range(3) if j != phi]
            for gam in others:
                for dele, eps in [(others[0], others[1]),
                                  (others[1], others[0])]:
                    for miss in range(3):
                        for one in range(3):
                            for swap in (0, 1):
                                A, B = make(p, v, phi, swap, gam, dele, eps,
                                            miss, one, cls, K)
                                if len(A) != n or len(B) != n or (A & B):
                                    continue
                                nsize += 1
                                par = (v, phi, swap, gam, dele, eps, miss, one)
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
                                if ok:
                                    hits.append(par)
                                    print(f"  p={p} HIT v={v} cls(v)={cls[v]} "
                                          f"phi={phi} swap={swap} gam={gam} "
                                          f"del={dele} eps={eps} "
                                          f"miss={miss} one={one}", flush=True)
    print(f"  p={p}: {nsize} passed size/disjointness, {len(hits)} verified",
          flush=True)
    return hits


if __name__ == "__main__":
    for p in [int(a) for a in sys.argv[1:]] or [13, 19, 31, 37]:
        t0 = time.time()
        print(f"=== p={p}", flush=True)
        sweep(p)
        print(f"    ({time.time()-t0:.0f}s)", flush=True)
