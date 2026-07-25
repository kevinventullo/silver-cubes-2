# Derivation Notes (rederived from scratch, 2026-07-10)

Everything below was re-derived independently of the earlier instances' code;
13Handoff.md was used only as a map of *what* to aim for. These notes are the
mathematical contract that `code/` implements.

## 1. Corner-triple reduction

p prime. Vertices (Z_p)^3, diagonal I = {x+y+z ≡ 0}, indexed by (x,y)
(so z = -x-y). Colors {0, ..., 3p-3}.

Off-diagonal w = (x,y,z) with defect s = x+y+z ≠ 0 has exactly three diagonal
neighbors, obtained by fixing two coordinates and correcting the third:
{(x,y), (x-s,y), (x,y-s)} — the **corner triple** of w. The map
w ↔ (middle corner (x,y), defect s) is a bijection onto (Z_p)^2 × (Z_p \ {0}).

A silver (p,3)-cube with this diagonal exists iff the intersection graph of
the p^2(p-1) corner triples (adjacent ⇔ sharing a diagonal point) is properly
(3p-2)-colorable; each diagonal point then takes the unique color missing from
the 3p-3 triples through it.

## 2. Equivariance, slope t

Diagonal-preserving translations = vectors (u,v,w), u+v+w = 0. Take
τ = translation by (1, t, -1-t), acting on diagonal indices as
(x,y) ↦ (x+1, y+t). Invariants and coordinates:

- **coset** of a point: c(x,y) = t·x - y (constant on τ-orbits; p cosets,
  each a τ-orbit of p points)
- **row** of a point: r(x,y) = x (τ shifts rows by +1)

The triple with middle corner on coset c and defect s has corners on cosets
{c - t·s, c, c + s} (its **footprint**), and its orbit under τ is labeled
(c, s) — there are p(p-1) orbits. In (coset,row) cells, the triple at row x
covers

    {(c, x), (c - t·s, x - s), (c + s, x)}.

For t = 1 the footprint is the centered 3-AP {c-s, c, c+s} and every tile is
the **s-dilate of one tromino** {(0,0), (-1,-1), (1,0)}, translated.

**Slope classification.** The footprint is a 3-AP iff t ∈ {1, -2, -1/2}
(the S_3-orbit of t = 1 under the anharmonic action t ↦ 1/t, t ↦ -1-t).
Directions with a zero coordinate (t ∈ {0, -1}) give degenerate (doubled)
footprints and admit no fixed colors — infeasible. Up to cube automorphisms
the slope classes are the orbits of the anharmonic group on t ∉ {0,-1}:
the harmonic class {1, -2, -1/2}, the equianharmonic class {ω, ω²}
(ω² + ω + 1 = 0, exists iff p ≡ 1 mod 3), and (p-5-|equianh.|)/6 generic
classes of size 6. For p = 13 this gives exactly 3 classes (matching the
"three slopes" of the handoff); for p = 19, four.

## 3. Forced color structure

Equivariance c(τ·v) = ρ(c(v)) forces ρ = two p-cycles (A, B) + (p-2) fixed
colors (possible iff p ≡ 1 mod 3). Consequences:

- Each **fixed** color owns one diagonal coset a (all p points), and its
  triple-class is a union of orbits whose footprints **partition Z_p \ {a}**
  — that is (p-1)/3 orbits. *This condition is also sufficient*: distinct
  orbits in the bundle occupy disjoint cosets, and triples within one orbit
  are pairwise disjoint. The fixed half is therefore **locally free**; its
  only interaction with the rest is which orbits it consumes.
- The two cycles own one diagonal coset each ("holes" h_A, h_B). Orbit
  (c,s) assigned to cycle A carries a **phase** x0: the row whose triple has
  color a_0 (the triple at row x has color a_{x-x0}). Pinning the diagonal
  point (h_A, r) to color a_r, the class of a_0 must **exactly cover the
  torus (Z_p)^2 minus the single cell (h_A, 0)** — an exact tiling by
  (p²-1)/3 dilated trominoes, one from each orbit in S_A. Orbit counts:
  (p-2)(p-1)/3 fixed + 2·(p²-1)/3 cycled = p(p-1). ✓

## 4. Dihedral model and pinning

Negation ν : v ↦ -v maps orbit (c,s) ↦ (-c,-s), cell (c,r) ↦ (-c,-r).
Demanding c(ν·v) = σ(c(v)) (dihedral group of order 2p): σ swaps the cycles
and pairs fixed cosets {a, -a}; the coset-0 fixed color is σ-fixed. With the
conventions σ(a_j) = b_{-j}, point (h, r) colored a_r, point (-h, r) colored
b_r:

- h_B = -h_A =: -h, h ≠ 0
- fixed[-o] = -fixed[o] (the fixed half is determined by one representative
  per ± pair of owners)
- S_B = -S_A, and the b_0-row of -o is -(a_0-row of o); cycle B's tiling
  condition is automatically the ν-image of cycle A's.

**WLOG h = 1.** Scaling μ_α : v ↦ αv is a cube automorphism preserving I,
normalizing ⟨τ⟩ (τ ↦ τ^α, same subgroup, same slope), commuting with ν, and
sending holes ±h ↦ ±αh. So dihedral solutions at hole h biject with those at
hole 1. (Verified computationally at p=7: the μ_2 bijection maps the h=1
census exactly onto the h=2 census, 6826 = 6826.) No enlargement of the
dihedral group by scalings is possible: a scaling in the color symmetry
group must permute the two holes, forcing α = ±1.

**The residual involution Φ.** The pinned model does retain one symmetry.
The coordinate swap ι : (x,y,z) ↦ (y,x,z) commutes with τ (for slope t = 1);
composing with ν and τ^{-1} gives an involution on pinned solutions:

    Φ : orbit (c,s) ↦ (c,-s),  owner unchanged,  A-phase x0 ↦ c - x0 - 1,

acting on cells as (c,r) ↦ (c, c-r-1). (Verified: Φ permutes the p=7 census.)
Φ has **no fixed solutions, provably, for any p**: Φ-invariance would put
(c,s) and (c,-s) — the *same* AP — into the same fixed bundle, double-
covering its cosets. This proves the empirical "four-fold extension
over-constrains and admits nothing" from the handoff, and means Φ is a
canonicalization tool (solutions come in Φ-pairs; census/mining can be
halved) rather than a search-space reducer.

## 5. The pinned model (what the solver sees)

Parameters (p, t, h), defaults t = 1, h = 1. Variables:

- fix[o, a] for one representative o per ± orbit-pair and each admissible
  owner a (a ∉ footprint(o), a ∉ {h, -h}); the partner orbit's assignment is
  the ν-image (variable shared).
- inA[o] for every orbit; inB[o] := inA[-o].
- pht[o][x] ("o ∈ A with phase x"), Σ_x pht[o][x] = inA[o].

Constraints:

1. Each ± pair: exactly one of {inA[o], inA[-o], fix[o,·]}.
2. Fixed partition: for each owner a (one per ± pair of owners) and each
   coset c ≠ a: Σ { fix[o,a] : c ∈ footprint(o) } = 1.
3. Tiling: for each cell (c,r) ≠ (h,0): Σ over s of
   pht[(c,s)][r] + pht[(c+ts,s)][r+s] + pht[(c-s,s)][r] = 1; and = 0 at (h,0).

A solution yields the full cube:
diagonal coset h row r ↦ a_r; coset -h ↦ b_r; fixed coset ↦ its color.
Off-diagonal w in orbit o at row x: fixed color, or a_{x-phase[o]} (o ∈ A),
or b_{x+phase[-o]} (o ∈ B). Colors: a_j = j, b_j = p+j, fixed = 2p+rank(coset).

## 6. Verification levels

1. `check_solution` — orbit-level: roles partition, ν-symmetry, footprint
   partitions, exact tiling.
2. `verify_cube` / standalone `code/verify.py` — direct rainbow check of all
   p² closed neighborhoods on the full p³ cube (independent of the model).
3. `check_equivariance` — c(τv) = ρ(c(v)) and c(νv) = σ(c(v)) at all vertices.

## 7. Empirical facts from the p=7 census (2026-07-10)

Exhaustive census at (p,t,h) = (7,1,1): **6826 solutions, 680 fixed halves,
all 680 completable** (completions per half: min 1, max 27, mode ~8).
Cross-validated: CP-SAT enumeration and the bespoke backtracker/Algorithm-X
enumerator produce identical line sets; the μ_2 scaling maps the h=1 census
exactly onto the h=2 census.

Negative results (all 6826 solutions tested):
- No orbit-level backbone: every orbit takes different roles across solutions.
- No algebraic phase function: x0 never lies in span{1,c,s}, {1,c,1/s},
  {1,c,s,1/s}, {1,c,s,c/s}, {1,c,s,1/s,c/s,cs}, or deg-2 polynomials in (c,s).
- No simple sign predicate for cycle-A membership (chi_2(s), chi_2(c),
  s-interval all fail on every solution).

Hardness inversion (p=13): clamping a *known-completable* fixed half makes
the instance much harder than the free problem (free model: 70 s; clamped:
>30 min for CP-SAT and >5 min for glucose without success, even though the
clamped instance provably contains the known solution). The free solver
succeeds by co-choosing the half and its tiling; random per-half probes at
p >= 13 need hour-scale budgets. Consequence: the "every half completes"
conjecture is cheap to test only at p=7 so far; at p=13 it remains open.

## 8. The shape-3 bundle theorem (2026-07-11)

The "exactly 3 pure shape-3 σ-fixed bundles" pattern at p = 7, 13, 19 is
now a theorem with a closed form — and it is *not* universal. With
e = ord_p(−2), d = (p−1)/e: the count is 3^{gcd(d,(p−1)/2)} if 3 | e, else
0. Proof via discrete-log transport to tilings of Z_{p−1} by {0,a,2a},
coset splitting, and interval-tiling rigidity; verified by brute force at
13 primes. First failures: p = 31, 43 (no such bundle exists at all).
Full statement, proof, table, corollaries: Theorem-Shape3Bundles.md.

## 9. Bundle taxonomy (2026-07-11, later)

Mixed-shape bundle counts B(p) = 3, 15, 120, 19692, 352107, 7531347 for
p = 7..43 — superexponential, no closed form (perfect-matching count of a
dense circulant 3-hypergraph). The structured content instead
(Theorem-CosetBundles.md): the **interval bundle** {3k+1,3k+2,3k+3} is a
ν-stable σ-seed for every p ≡ 1 (mod 3); the **maximally symmetric**
bundles are exactly C-orbits of a single AP-pair with cubic-transversal
tile, numbering 3τ(p) with τ(p) = p/9 + O(√p) ≥ 1 for all p ≤ 600 checked
(τ = 4 at p = 31, where they are pure shape 4 — the replacement for the
dead shape-3 seed). Enumeration/DP code: code/bundles.py.

## 10. Open directions this codebase serves

- **Population mining** (p = 7 exhaustive, p = 13 bulk): backbone facts,
  arithmetic predictors (cubic/quadratic characters of s, c, s/c), phase-
  function fits. The fixed half being locally free suggests the real signal
  is in (a) the fixed/cycle orbit split, (b) the phase function.
- **The tiling half as algebra**: cycle A is an exact cover of (Z_p)² minus a
  point by dilated trominoes; character sums (cubic Gauss/Jacobi sums exist
  exactly for p ≡ 1 mod 3) are the natural attack for a uniform phase formula.
- **New primes**: p = 19, 31, 37 via the same pinned model; slope portfolio
  {harmonic, equianharmonic, generic classes} if t = 1 fails.
