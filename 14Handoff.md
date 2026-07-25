# Silver Cubes — Handoff (current)

**START HERE.** This supersedes `13Handoff.md`, which described the state of
the program before 2026-07-25 and whose strategic advice is now largely
obsolete. Read this first; `13Handoff.md` is retained because its problem
statement and its account of *what did not work* remain accurate and useful.

---

## 0. The problem

A **silver (n,3)-cube** is a colouring of the n×n×n Hamming graph (vertices
[n]³, edges join words differing in one coordinate) with 3n−2 colours,
together with a *diagonal* — a maximum independent set of size n² — such that
the closed neighbourhood of every diagonal vertex (itself plus its 3(n−1)
neighbours, 3n−2 vertices in all) is rainbow.

Existence is conjectured for all n (Ghebleh–Goddyn–Mahmoodian–Verdian-Rizi
2008). A multiplicativity theorem reduces the conjecture to **prime** orders.
Classical: 2, 3, 5, 7. Earlier work in this program added 11 and 13. We
always use the **linear diagonal** {x+y+z ≡ 0 (mod n)}.

There is a genuine dichotomy: the whole framework below needs a translation
symmetry of order p, which exists **iff p ≡ 1 (mod 3)**. Primes p ≡ 2 (mod 3)
(11, 17, 23, …) are provably outside it and remain an independent track.

## 1. Status

| p | status |
|---|---|
| 2, 3, 5, 7 | classical |
| 11 | earlier work (non-equivariant; p ≡ 2 mod 3) |
| 13 | earlier work |
| **19** | **new (2026-07-25), verified** |
| **31** | **new (2026-07-25), verified** |
| **37** | **new (2026-07-25), verified** |
| **43** | **new (2026-07-25), verified — constructed, not searched** |
| 61, 67 | open; raw search does not reach them, see §6 |

Every cube is verified three independent ways: the in-pipeline check, the
standalone `code/verify.py`, and `kv_manual_verification.py` (handwritten by
KV, different diagonal parametrisation). Files: `results/cube_p19_mult.txt`,
`cube_p19_fullmult.txt`, `cube_p31_block.txt`, `cube_p31_fullmult.txt`,
`cube_p37_block.txt`.

p = 19 went from *days of CP-SAT and CaDiCaL with no verdict* to **0.5 s**.

## 2. Background reductions (unchanged; details in NOTES.md)

1. **Corner triples.** Index the diagonal by (x,y). Each off-diagonal vertex
   with defect s = x+y+z ≠ 0 is adjacent to exactly three diagonal vertices
   {(x,y), (x−s,y), (x,y−s)}. A silver cube exists **iff** the intersection
   graph of these triples is properly (3p−2)-colourable; diagonal colours are
   then forced.
2. **Equivariance.** Impose a translation τ of order p. The colour action is
   forced to be *two p-cycles + (p−2) fixed colours* — possible iff
   p ≡ 1 (mod 3). Orbits are pairs (c, s): coset and defect.
3. **The two halves.** Each **fixed** colour owns a coset a and its orbits'
   footprints {c−s, c, c+s} partition Z_p ∖ {a}. Each **cycle** colour is an
   exact cover of the torus (Z_p)² (coordinates: coset c, row r) minus one
   cell (h,0), by tiles T(c,s,x) = {(c,x), (c−s,x−s), (c+s,x)}, at most one
   per orbit.

13Handoff called the cycle half "opaque — no discernible closed form." That
was a coordinate artifact.

## 3. The symmetry (the new idea)

Substitute

    (X, Y) = (r, r − c + h).

The tile becomes the **corner triple** {(X,Y), (X−s,Y), (X,Y−s)} and the hole
moves to the **origin**. Then

    μ_α : (X,Y) ↦ (αX, αY),  s ↦ αs      (α ∈ Z_p^*)

sends tiles to tiles, fixes the hole, and permutes orbit labels
(X−Y, s) ↦ (α(X−Y), αs), preserving the one-tile-per-orbit constraint. Back
in (c,r) coordinates:

> **Each cycle colour's tiling problem is invariant under scaling about its
> own hole,  (c, r) ↦ (h + α(c−h), αr).**

**Why nobody saw it.** μ_α is an automorphism of the *cube* only if it fixes
{h_A, h_B}; since h ↦ αh, that forces α = ±1, i.e. exactly the negation ν of
the old dihedral model (NOTES.md §4 proves this). The proof is correct — and
it is precisely what hides the symmetry. This is a symmetry of each colour's
*own subproblem*, **with a different centre per colour**; it is an ansatz on
the pieces, never an equivariance of the whole. Any search organised around
symmetries *of the cube* is structurally unable to find it.

## 4. Which subgroup

For H ≤ Z_p^* of order m acting freely on the (p²−1)/3 tiles: m | (p²−1)/3,
which with m | p−1 is equivalent to

    m | p−1   and   3 | (p−1)/m.

The maximal choice is **m = (p−1)/3, H = K the cubic residues** — available at
every p ≡ 1 (mod 3), i.e. exactly our family. (The full group never works:
(p+1)/3 ∉ Z.) Under K, the cell space has 3(p+1) orbits, naturally
**P¹(F_p) × Z/3**; identifying Z_p² ≅ F_{p²}, cell classes are the cyclic
group F_{p²}^*/K of order 3(p+1). A tiling needs only **p+1** tile orbits.

## 5. The block model

The fixed colours fit the same frame. A fixed bundle has (p−1)/3 = m orbits;
a K-orbit has m elements. Taking the bundle to *be* a K-orbit gives exactly
the **coset bundles** of `Theorem-CosetBundles.md`: with

    Blk(a, w, j) = { (a + w s, s) : s ∈ K_j }

the footprints partition Z_p ∖ {a} **iff w−1, w, w+1 lie in three distinct
cubic cosets** — w is a *transversal index*, w = 1/t for a transversal shape
t. These exist at every p in the family (Theorem C; τ(p) ≈ p/9).

> **A silver cube of this type = 3p blocks partitioning the p(p−1) orbits:
> p+1 centred at each cycle hole (WLOG cosets 0 and 1), one at each of the
> other p−2 cosets; singletons transversal; the two cycle families admitting
> phases that exactly cover the 3(p+1) cell classes.**

Counting is exact: (p+1)+(p+1)+(p−2) = 3p blocks × m orbits = p(p−1).

Equivalently, per cubic class j the used pairs (a,w) form a set P_j of p
points in Z_p² **no two of which have (Δa)/(Δw) ∈ K_j** — a spread condition.
Rows a = const and columns w = const are automatically legal, which is why
solutions look like unions of horizontal and vertical lines.

## 6. What it buys, and where it stops

Time to a verified cube (CP-SAT, 6 workers, MacBook Air M3):

| p | old framework | block model | + pure shape |
|---|---|---|---|
| 13 | 70 s | 0.11 s | 0.1 s |
| 19 | **days, no verdict** | **0.49 s** | 0.6 s |
| 31 | out of reach | 400 s | **13 s** |
| 37 | out of reach | — | **391 s** (v = 8) |
| 43 | — | no verdict (4 arms × 2400 s) | no verdict |
| 61 | — | no verdict (5 arms × 2400 s) | no verdict |

"Pure shape" = all fixed colours are coset bundles of the *same* shape ±t.
Note this **revives** the single-shape hypothesis that 13Handoff declared
dead: it is false inside the dihedral ansatz and true inside this one. At
p = 7, 13, 19 the unique transversal shape is ±3; at p = 31, where shape 3
provably does not exist (`Theorem-Shape3Bundles.md`, N(31) = 0), the
construction simply uses shape 4.

**The raw block model runs out at p = 43.** Going higher needs the explicit
construction of §7, not more compute.

## 7. The construction template (the live problem)

Every block solution examined (p = 13, 19, 31, 37) has the same three-piece
shape. With u = −v, v a transversal index, {h,h'} = {0,1}:

    cycle FULL  = { (h + w s, s)      : s ∈ K_φ, w ∈ Z_p }          p blocks
                ∪ { (h + u s, s)      : s ∈ K_γ }                   1 block

    cycle OTHER = { (h' + (u−d) s, s) : s ∈ K_δ, d ∉ K_miss }       2m+1 blocks
                ∪ { (h' + (u−d) s, s) : s ∈ K_ε, d ∈ K_one ∪ {0} }  m+1 blocks

Sizes are automatic: p+1 = (2m+1)+(m+1), |A| = |B| = (p²−1)/3. In words:
**one cycle is every orbit whose defect lies in a single cubic coset, plus one
extra block; the other is a pair of coset-defined slices of the remaining two
classes.**

Given A and B as orbit sets, the rest **decouples into three small
independent problems**: phases for A, phases for B, and the fixed
decomposition. This is the reverse of the hardness inversion in NOTES.md §7 —
clamping the *fixed* half makes things harder, clamping the *cycle* halves
makes them easy.

**The open question is the class assignment (φ, γ, δ, ε, miss, one).** Status:

- The only labelling freedom is the primitive root, acting on all class
  indices by j ↦ λj (λ ∈ {1,2}; K_0 = cubes is canonical).
- Verified tuples per prime (of the tuples passing sizes/disjointness):
  **p = 13: 72/216, p = 19: 72/216, p = 31: 245/864**. Modulo λ these are
  **18, 18 and 27** distinct signatures, and the 18 are **common to all
  three** — p = 31's 27 are a strict superset.
- The 18 are characterised exactly by

      miss ≡ one + δ − φ  (mod 3)
      one ≡ φ + δ  if γ = δ;   one ≢ φ + δ  if γ = ε

  all with cls(v) ≡ 1 after normalisation. (Checked: the rule generates
  precisely the observed set, 18 = 18.)
- The extra 9 signatures at p = 31 have **cls(v) = 0**, a case that cannot
  occur at 13 or 19 (there every transversal index has cls(v) = 2). The
  p = 31 cube in `results/` is one of them: (φ,γ,δ,ε,miss,one) = (0,1,1,2,2,1),
  v = 4, swap = 1. So cls(v) is not constant across the family, and the
  18-signature rule describes the cls(v) ≠ 0 stratum only.
- **p = 37: the rule survives.** Targeted test hit at signature
  (φ,γ,δ,ε,miss,one) = (0,1,2,1,2,0), v = 2, swap = 1 — one of the 18. So the
  rule holds at **13, 19, 31, 37**, including the two primes that killed the
  earlier fit. Found in ~8 min by testing the candidate list, versus 391 s of
  raw block-model search at 37 and *no verdict at all* at 43.
- **p = 43: the rule survives, and delivers a new prime.** Hit at canonical
  signature (0,1,1,2,2,1), v = 7, cls(v) = 2, swap = 0 — actual parameters
  (φ,γ,δ,ε,miss,one) = (0,2,2,1,1,2). Cube in
  `results/cube_p43_template.txt`, verified by `code/verify.py` and by
  `kv_manual_verification.py`.

  **This is the first order obtained by construction rather than search**:
  the block model gets no verdict at 43 in 4 × 2400 s, whereas predicting the
  configuration from the rule and solving the three decoupled subproblems
  takes minutes.

  So the rule holds at **13, 19, 31, 37, 43**.

- **p = 61: no verdict, and the reason relocates the bottleneck.** A run of
  `mult_targeted.py 61 67` reached no hit in 2h50m, and a direct probe showed
  why: **not one phase solve at p = 61 completes in 600 s**, against 6–9 s at
  p = 31 and 43 (worst observed at 43: 88 s). So the p = 61 result is *not*
  evidence against the rule — it is the phase subproblem becoming the binding
  constraint. Note this cannot currently distinguish "the rule fails at 61"
  from "the solver is too slow"; do not record either.

  This is **lemma 3 of §8 asserting itself**. Up to p = 43 the hard part was
  choosing the configuration and the phases came free; from p = 61 the
  configuration is predicted instantly and the phases are the whole problem.
  A theorem needs the phases *constructively*, not from a solver — and the
  practical next step and the theoretical one have now converged on the same
  question.

  Concrete handle (derived, unused): in the reduced picture a tile-class
  ((x,y),σ) with x−y = w covers cell classes
  ([x:y], σ+cls(x)), ([x−1:y], σ+cls(x−1)), ([x:y−1], σ+cls(x)) —
  so **each tile covers two cell classes at level σ+cls(x) and one at level
  σ+cls(x−1)**. Hence for every level ℓ, 2n_ℓ + m_ℓ = p+1 where n_ℓ counts
  tiles with σ+cls(x) = ℓ and m_ℓ those with σ+cls(x−1) = ℓ. That is a real
  constraint on any phase assignment and the natural starting point for either
  a closed-form phase function or a cheap infeasibility filter.

**Trap 3: solver time limits corrupt the intersection.** Satisfiable phase
instances usually solve in 6–9 s, but the tail is long — one at p = 43 took
**88 s and returned SAT**, one at p = 37 gave no verdict in 300 s. A sweep
capped at 20 s therefore manufactures *false negatives* at p ≥ 37, and since
false negatives only ever shrink an intersection, the likely outcome is a
spuriously empty one and a wrong conclusion that no uniform rule exists. The
defaults are now 120 s. Costs also blow up fast: p = 19 took 45 s for 216
candidates, p = 31 took 3685 s for 864 (~19× per candidate for one prime
step). Sweep broadly only where it is cheap; at 37 and above, test a
candidate list with an adequate budget instead.

**Two traps, both already sprung once.**

1. Solve the fixed half with `fixed_part_blocks`, **not** `fixed_part`. The
   generic version ignores the block structure, cannot decide at p ≥ 31
   within 300 s, and its timeout looks exactly like a mathematical negative.
   It produced a spurious "the template fails at p = 31" — it does not.
2. Agreement at p = 13 and 19 alone is weak evidence. An earlier fitted
   assignment matched both perfectly and died at 31. Two primes is the
   evidence strength that has now misled this program twice (cf. single-shape:
   clean at 7, dead at 13). Test at 31 and 37 before believing anything.

## 8. What a theorem needs

Given the template, existence for all p ≡ 1 (mod 3) reduces to:

1. **A transversal index exists** — essentially Theorem C of
   `Theorem-CosetBundles.md` (Jacobi sums; verified for all p ≤ 600).
2. **The fixed decomposition exists** — the leftover orbits split into coset
   bundles. A matching statement about cubic cosets; should follow from the
   formulas for A and B.
3. **The phases exist** — the genuinely open piece. The p+1 tile classes at
   each hole must exactly cover P¹ × Z/3. In F_{p²} terms: choose p+1
   elements v_i and shifts σ_i in the order-3 subgroup of Q = F_{p²}^*/K so
   that {σ_i q(v_i), σ_i q(v_i−1), σ_i q(v_i−θ)} is exactly Q. The projective
   part says each direction is hit 3 times; the Z/3 part is then a colouring
   condition. Cubic Gauss/Jacobi sums exist precisely for p ≡ 1 (mod 3),
   which is suggestive.

Two rigidity facts, free: the transposition ι : (X,Y) ↦ (Y,X) is a symmetry
of the tiling problem but **ι-invariant tilings are infeasible at every prime
7…67**; and the clean "all three projections bijective" sub-family exists at
7, 13, 19 but is not what generic solutions look like.

## 9. Code

All in `code/`, run with `.venv/bin/python`, `PYTHONPATH=code`:

| file | role |
|---|---|
| `mult_block.py` | **the block model** of §5 — the object a proof should be about |
| `mult_model.py` | full τ-equivariant model, symmetry as equalities between phase variables; general but slower |
| `mult_construct.py` | build A, B from an explicit class assignment; three decoupled solves (`phases`, `fixed_part_blocks`) |
| `mult_template.py` | sweep all discrete parameters of the §7 template |
| `mult_targeted.py` | test a specific candidate signature list at a prime |
| `mult_intersect.py` | intersect template hit sets across primes |
| `mult_sweep.py` | prime-by-prime block-model search over transversal shapes; writes and verifies cubes |
| `mult_analyze.py` | describe a saved solution's orbit sets in cubic-coset terms (no solver) |
| `verify.py` | standalone verifier, imports nothing from the rest |

Reproduce p = 19 from scratch (≈1 s):

    PYTHONPATH=code .venv/bin/python code/mult_sweep.py 19
    .venv/bin/python code/verify.py results/cube_p19_block.txt

Older machinery (`core.py`, `model.py`, `solve.py`, `census.py`, `bundles.py`,
…) implements the dihedral framework of NOTES.md. Still correct, still useful
for censuses and the bundle theorems; superseded for search.

## 10. Other documents

- `NOTES.md` — the rederived base framework (corner triples, slopes, orbit
  coordinates, dihedral model). Still the reference for §2.
- `Theorem-Shape3Bundles.md` — pure shape-3 bundles classified: N(p) =
  3^gcd(d,(p−1)/2) if 3 | ord_p(−2), else 0. Why shape 3 dies at 31 and 43.
- `Theorem-CosetBundles.md` — coset bundles = maximally symmetric bundles,
  3τ(p) of them; transversal shapes always exist. This is what §5 uses.
- `13Handoff.md` — the previous handoff. Obsolete strategy, accurate history.
- `CombinedFindings.md`, `Intro.txt` — the earlier (pre-2026-07) investigation
  including p = 11 and p = 13.
- `JOBS.md` — running/stopped compute jobs.
