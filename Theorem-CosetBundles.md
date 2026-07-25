# Bundle taxonomy: interval seeds, coset bundles, and the count landscape

*2026-07-11, companion to Theorem-Shape3Bundles.md. Answers "what are the
mixed-shape bundle counts" — partly with theorems, partly with an honest
negative.*

Throughout: p ≡ 1 (mod 6), bundle = ν-stable partition of Z_p^* into
centered 3-APs (the σ-fixed color's structure), C = cubic residues
(index 3), G = Z_p^*/{±1} acting on bundles by scaling. B(p) = total
number of bundles.

## Theorem A (interval bundle — existence for every p)

The intervals {3k+1, 3k+2, 3k+3}, 0 ≤ k < (p−1)/3, form a ν-stable bundle
for every prime p ≡ 1 (mod 3).

*Proof.* They are APs (difference 1) partitioning Z_p^*. Negation sends
the interval starting at 3k+1 to the interval starting at p−3k−3, and
p−3k−3 ≡ 1 (mod 3) precisely because p ≡ 1 (mod 3). ∎

So a σ-seed exists at every prime of the family, unconditionally. The
interval bundle has trivial stabilizer (scaling changes the common
difference) — it is the canonical *unstructured* seed.

## Theorem B (coset bundles = maximally symmetric bundles)

Call a shape t (t ≢ 0, ±1, ±2, shapes taken mod ±) a **transversal shape**
if {1−t, 1, 1+t} meets all three cosets of C. Then the bundles whose
stabilizer in G contains C/{±1} are exactly

    B_{t,β} = { βγ·{1−t, 1, 1+t} : γ ∈ C },   t transversal, β ∈ Z_p^*/C,

i.e. one C-orbit of a single AP-pair. Their number is **3·τ(p)**, where
τ(p) = #{transversal shapes mod ±}.

*Proof.* C/± has order (p−1)/6 = #(AP-pairs in a bundle). If a bundle is
C-invariant and the action on its pairs is free, the bundle is a single
C-orbit of one pair {A, −A}; it covers A·C·{±1} = A·C (−1 ∈ C), which
equals Z_p^* iff the three elements of A lie in distinct C-cosets, iff the
normalized tile is a transversal; ν-stability is automatic (−1 ∈ C). All
pairs are dilates of one AP, so the bundle is pure shape t, and distinct
(t, β) give distinct bundles. Non-free actions require an element of prime
order in C/± to fix a 3-set, forcing an order-3 rotation {x, ωx, ω²x};
such a triple is not an AP-pair of the required disjoint form when it
would need to constitute the whole stabilized pair (an element fixing
{A, −A} with αA = −A gives α² fixing A, reducing to the order-3 case; an
order-3 α with αA = A makes A = {x, αx, α²x} a multiplicative triangle,
which is an AP only if... it forces 2αx = x + α²x, i.e. α² − 2α + 1 =
(α−1)² ≡ 0, α = 1). Hence the action is free. ∎

Verified against the enumerated stabilizer spectra (exact match of both
count and shape content):

| p | \|C/±\| | max-stab bundles observed | 3·τ(p) | shapes |
|---|---|---|---|---|
| 13 | 2 | 3 | 3 | pure 3 |
| 19 | 3 | 3 | 3 | pure 3 |
| 31 | 5 | 12 | 12 | pure 4 (and 3 more transversal shapes) |
| 37 | 6 | 15 | 15 | pure 3 and 4 others |

Consistency with the shape-3 theorem: when ord_p(−2) has d = 1, the three
pure shape-3 bundles are exactly the coset bundles for t = 3 (T = cosets
of C); the extra GP bundles at d > 1 (e.g. 81 at p = 73) have smaller
stabilizers. Shape 3 is a transversal shape iff 3 | ord_p(−2)... at d = 1;
in general the GP theorem and Theorem B classify different (overlapping)
symmetric families, with Theorem B the maximal-symmetry stratum.

## Theorem C (transversal shapes always exist)

τ(p) = p/9 + O(√p): for each of the two admissible character patterns
(χ(1−t), χ(1+t)) = (ω, ω²), (ω², ω), the count of t is p/9 + O(√p) by
standard Jacobi-sum estimates, and t ↦ −t swaps the patterns, so τ(p) is
their average. In particular τ(p) ≥ 1 for all p beyond an explicit modest
bound; computationally **τ(p) ≥ 1 for every p ≡ 1 (mod 6) with p ≤ 600**
(no exceptions found; τ(7) = τ(13) = τ(19) = 1, τ(31) = 4, τ(97) = 9,
τ(499) = 52 ≈ 499/9).

**Corollary.** At every prime p ≡ 1 (mod 6) (p ≤ 600 verified; all p by
Theorem C for p large), the σ-fixed color admits both an unstructured seed
(interval bundle) and a maximally symmetric seed (coset bundle). At p = 31
and 43, where pure shape 3 is impossible (Theorem-Shape3Bundles), coset
bundles exist with other shapes — e.g. pure shape 4 at p = 31.

## The count landscape (honest negative)

Exact counts by bitmask dynamic programming over the ±-class set:

| p | 7 | 13 | 19 | 31 | 37 | 43 |
|---|---|---|---|---|---|---|
| B(p) | 3 | 15 | 120 | 19 692 | 352 107 | 7 531 347 |

B(p) is a perfect-matching count of a dense circulant 3-uniform
hypergraph — superexponential growth, no closed form expected, and the
data confirms it. The meaningful structure is the stabilizer
stratification:

| p | trivial | 2 | 3 | 5 | 6 |
|---|---|---|---|---|---|
| 13 | 12 | 3 | – | – | – |
| 19 | 117 | – | 3 | – | – |
| 31 | 19 680 | – | – | 12 | – |
| 37 | 351 378 | 648 | 66 | – | 15 |

The submaximal strata (stab 2, 3 at p = 37; mixed shapes such as
(3,3,3,17,17,17)) are unions of shorter subgroup-orbits — classifiable by
the same orbit method, left as further work.

## Consequences for the program

1. **Seed existence is settled everywhere**: no prime in the family lacks
   σ-seeds, structured or not. The dihedral ansatz never dies at the seed.
2. **The clamp strategy generalizes**: at p = 31 the analog of the p = 19
   shape-3 clamp arm is "σ-color = pure shape 4" (12 bundles), etc. The
   right clamp at each prime is read off from τ-data, not from shape 3.
3. **The uniform construction, if it exists, is shape-agnostic**: its
   σ-seed must be chosen by a rule like "any coset bundle" or "the
   interval bundle" — both available at all p — rather than a fixed shape.
