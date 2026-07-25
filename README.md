# silver-cubes-2

Silver (n,3)-cubes for prime orders — continuation of
[silver-cubes](https://github.com/kevinventullo/silver-cubes).

A **silver (n,3)-cube** is a colouring of the n×n×n Hamming graph with 3n−2
colours, plus a diagonal (a maximum independent set of size n²), such that the
closed neighbourhood of every diagonal vertex is rainbow. Existence is
conjectured for all n (Ghebleh–Goddyn–Mahmoodian–Verdian-Rizi, *Silver Cubes*,
Graphs and Combinatorics 24 (2008) 429–442); a multiplicativity theorem
reduces the conjecture to prime orders.

## New in this repo

Silver cubes at **p = 19, 31 and 37** — orders open in the literature.

| file | order |
|---|---|
| `results/cube_p19_mult.txt`, `cube_p19_fullmult.txt` | 19 |
| `results/cube_p31_block.txt`, `cube_p31_fullmult.txt` | 31 |
| `results/cube_p37_block.txt` | 37 |

Format: comment lines beginning `#`, then `x y z colour` over all of
(Z_p)³. Each cube is verified three independent ways — `code/verify.py`
(standalone, imports nothing else), `kv_manual_verification.py` (handwritten,
different diagonal parametrisation), and the construction pipeline's own
check.

    python code/verify.py results/cube_p37_block.txt
    # p=37 colors=109 diagonal_vertices=1369 (expect 1369) rainbow_failures=0
    # VERDICT: SILVER CUBE VERIFIED

## How

For p ≡ 1 (mod 3) the problem reduces, under an order-p translation symmetry,
to a colouring whose "cycle" classes are exact covers of a punctured torus by
dilated trominoes. The substitution (X,Y) = (r, r−c+h) turns those tiles into
corner triples with the hole at the origin, revealing that **each colour
class's subproblem is invariant under scaling about its own hole** — a
symmetry that is *not* a symmetry of the cube, and so is invisible to any
search organised around cube automorphisms. Imposing invariance under the
cubic residues collapses p = 19 from days with no solver verdict to 0.5 s.

Full account, including the open problem (a uniform construction for all
p ≡ 1 mod 3): **[`14Handoff.md`](14Handoff.md)** — start there.

## Layout

- `14Handoff.md` — current state of the program; read first
- `NOTES.md` — the base reduction and the dihedral framework
- `Theorem-Shape3Bundles.md`, `Theorem-CosetBundles.md` — two proved results
  about the "fixed colour" half
- `13Handoff.md`, `CombinedFindings.md`, `Intro.txt` — earlier state (through
  p = 11 and 13)
- `code/mult_*.py` — the multiplicative-symmetry machinery
- `code/` (rest) — the earlier dihedral machinery, censuses, verifiers
- `results/` — cubes, solutions, logs

Requires Python 3 with `ortools` (CP-SAT).
