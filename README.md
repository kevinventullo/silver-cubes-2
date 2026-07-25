# silver-cubes-2

N.b. Everything in this repo was written by Claude Code, with the exception
of `kv_manual_verification.py` (handwritten by KV as an independent check on
the cubes).

Silver (n,3)-cubes for prime orders — continuation of
[silver-cubes](https://github.com/kevinventullo/silver-cubes).

A **silver (n,3)-cube** is a colouring of the n×n×n Hamming graph with 3n−2
colours, plus a diagonal (a maximum independent set of size n²), such that the
closed neighbourhood of every diagonal vertex is rainbow. Existence is
conjectured for all n (Ghebleh–Goddyn–Mahmoodian–Verdian-Rizi, *Silver Cubes*,
Graphs and Combinatorics 24 (2008) 429–442); a multiplicativity theorem
reduces the conjecture to prime orders.

## Status by order

Composite orders follow from prime orders by the multiplicativity theorem, so
only primes are listed.

| n | status | found by | discovery date | file |
|---|---|---|---|---|
| 2, 3, 5 | known | Ghebleh, Goddyn, Mahmoodian, Verdian-Rizi | 2008 (published) | — |
| 7 | known | Ventullo, Khodkar | 2009 (published) | `results/cube_p7_t1_h1.txt` † |
| **11** | **solved** (was open) | Claude Opus 4.8 | 2026-05-27 | [silver-cubes](https://github.com/kevinventullo/silver-cubes) |
| **13** | **solved** (was open) | Claude Fable 5 | 2026-06-12 | [silver-cubes](https://github.com/kevinventullo/silver-cubes) ‡ |
| 17 | **open** | — | — | — |
| **19** | **solved** (was open) | Claude Opus 5 | 2026-07-24 | `results/cube_p19_mult.txt`, `cube_p19_fullmult.txt` |
| 23, 29 | **open** | — | — | — |
| **31** | **solved** (was open) | Claude Opus 5 | 2026-07-24 | `results/cube_p31_fullmult.txt`, `cube_p31_block.txt` |
| **37** | **solved** (was open) | Claude Opus 5 | 2026-07-25 | `results/cube_p37_block.txt` |
| 41, 43, 47, … | **open** | — | — | — |

The 19, 31 and 37 cubes were all found in a single session on the night of
2026-07-24/25; 37 landed just after midnight.

† and ‡: these are *not* the original artifacts. The n = 7 and n = 13 cubes
in `results/` were regenerated in July 2026 by the framework in `NOTES.md`
(both verify); the original n = 13 cube found by Fable 5 on 2026-06-12, and
the n = 11 cube, live in the [silver-cubes](https://github.com/kevinventullo/silver-cubes)
repo. Discovery credit in the table refers to the original find.

The two open classes are open for different reasons. Primes **n ≡ 2 (mod 3)**
(17, 23, 29, 41, 47, …) are *provably outside* the framework used here — the
order-n translation symmetry it rests on does not exist for them, and n = 11
was found by a different, non-equivariant route. Primes **n ≡ 1 (mod 3)**
(43, 61, 67, …) are inside the framework, but the search stalls at 43; those
need the uniform construction described in [`14Handoff.md`](14Handoff.md)
rather than more compute.

Cube file format: comment lines beginning `#`, then `x y z colour` over all
of (Z_n)³. Each new cube is verified three independent ways —
`code/verify.py` (standalone, imports nothing else),
`kv_manual_verification.py` (handwritten, different diagonal
parametrisation), and the construction pipeline's own check.

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
