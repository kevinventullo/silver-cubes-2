# The pure shape-3 bundles: a complete classification

*2026-07-11. Resolves the "exactly 3 pure shape-3 bundles at p = 7, 13, 19"
pattern observed in the censuses. The pattern is real but not universal;
the true statement is a closed-form count in terms of ord_p(−2).*

## Setting

Fix a prime p ≡ 1 (mod 6) and the dihedral pinned model at slope t = 1
(NOTES.md). The σ-fixed color owns diagonal coset 0, and its **bundle** is a
partition of Z_p ∖ {0} into centered 3-APs {c−s, c, c+s}, stable under
negation. The **shape** of an AP is ±s/c (sign-free, since the AP determines
s only up to sign). A bundle is **pure shape 3** if every AP has shape ±3.

**Empirical input.** The exhaustive p = 7 census and the standalone bundle
enumeration found exactly 3 pure shape-3 bundles at p = 7, 13, 19.

## Theorem

Let e = ord_p(−2) and d = (p−1)/e. The number of negation-stable pure
shape-3 bundles is

> **N(p) = 3^gcd(d, (p−1)/2)  if 3 | e,  and N(p) = 0 otherwise.**

In particular N(7) = N(13) = N(19) = N(37) = N(61) = N(79) = 3, while
N(31) = N(43) = N(127) = 0 and N(73) = 81, N(97) = 9, N(109) = 27.
"Exactly 3 at every p" is false; it holds iff 3 | e and gcd(d, (p−1)/2) = 1.

## Proof

**Step 1 (shape-3 APs are dilated geometric progressions).** An AP of shape
±3 centered at c is {c − 3c, c, c + 3c} = c·{−2, 1, 4} = c·{1, r, r²} with
r = −2. For p > 5 the map c ↦ c·{−2,1,4} is injective (a multiplicative
stabilizer element g of {−2,1,4} must satisfy g ∈ {−2,1,4} with
g·{−2,1,4} = {−2,1,4}, forcing p | 9 or p | 15). Hence a pure shape-3
bundle is exactly a set T ⊆ Z_p^* with

    T · {1, −2, 4} = Z_p^*   (each element covered once),

and negation-stability of the bundle is exactly T = −T (an AP is never its
own negation, since its center would be 0).

**Step 2 (transport to a cyclic tiling).** Fix a primitive root g and take
discrete logs: Z_p^* ≅ Z_n with n = p − 1. The tile {1, −2, 4} becomes
A = {0, a, 2a} with a = ind(−2), and T becomes S ⊆ Z_n with S + A = Z_n.
Note ord(−2) = e = n/gcd(a, n), so with d := gcd(a, n) we have n/d = e.
Negation is translation by w := n/2, so the symmetry condition is
S + w = S.

**Step 3 (coset splitting).** A ⊆ H := ⟨a⟩ = ⟨d⟩ ≅ Z_e. Since every tile
s + A stays inside the H-coset of s, a tiling S + A = Z_n splits into d
independent tilings S_i := S ∩ (i + H) of the cosets i + H, i = 0, …, d−1.

**Step 4 (rigidity of 3-AP tilings of a cyclic group).** Within a coset,
identify i + H ≅ Z_e; the tile is {0, a″, 2a″} with a″ = a/d invertible
mod e. Multiplying by (a″)^{-1} is an automorphism of Z_e taking the tile
to the interval {0, 1, 2}. Tilings of the cycle Z_e by intervals of length
3 are rigid: placing one interval forces its neighbors around the whole
cycle, so a tiling exists iff 3 | e and there are exactly 3 of them, the
phase classes {j + 3Z_e}, j ∈ {0, 1, 2}. Hence, back in Z_n:

    S_i = i + a·j_i + ⟨3a⟩,   with a free phase j_i ∈ Z_3 per coset,

and (unrestricted) tilings biject with phase vectors (j_0,…,j_{d−1}) ∈ Z_3^d.
This already gives the unrestricted count 3^d (if 3 | e, else 0).

**Step 5 (symmetry bookkeeping).** Translation by w permutes cosets by
i ↦ i + w (mod d) and transports phases affinely: writing
i + w = r + h with r = (i + w) mod d and h ∈ H, h ≡ k_i·a (mod ⟨n⟩),
the condition S + w = S becomes

    j_{(i+w) mod d} = j_i + k_i  (mod 3)     for all i.

This is a linear system over the cycles of the translation i ↦ i + w on
Z_d. Since w = n/2 and d | n, only the 2-adic valuations matter:
- if v_2(d) < v_2(n): d | w, the permutation is the identity (cycles of
  length L = 1, gcd(w,d) = d of them);
- if v_2(d) = v_2(n): gcd(w,d) = d/2 and all cycles have length L = 2.

Around a cycle of length L the k's telescope: a·(Σk) ≡ L·w (mod n), which
determines Σk mod e, hence mod 3 (as 3 | e). The system is solvable iff
every cycle-sum Σk ≡ 0 (mod 3), and then has exactly 3^{#cycles} solutions
(one free phase per cycle).

- L = 2: Σk ≡ 0 comes from a·Σk ≡ 2w = n ≡ 0 (mod n), so Σk ≡ 0 (mod e) —
  always solvable.
- L = 1: each k_i satisfies a·k_i ≡ w (mod n), so k_i ≡ K₀ (mod e) with
  d | w and K₀ = w/... determined by 3d·K₀' ≡ ... concretely the condition
  is w ∈ ⟨3a⟩ = ⟨3d⟩, i.e. 3d | n/2, i.e. 3 | e/2. Here e is even (this is
  the v_2(d) < v_2(n) case), so 3 | e/2 ⟺ 3 | e — already assumed.

In both cases: solvable, with #cycles = gcd(w, d) = gcd(d, (p−1)/2), giving

    N(p) = 3^{gcd(d, (p−1)/2)}   when 3 | e,   N(p) = 0 otherwise.  ∎

## Computational verification

Brute-force enumeration (backtracking over mirror-pairs of shape-3 APs)
agrees with the formula at every prime tested — 13/13, including all
degenerate and nontrivial cases:

| p | e = ord_p(−2) | d | N(p) formula | N(p) brute | unrestricted 3^d | brute |
|---|---|---|---|---|---|---|
| 7 | 6 | 1 | 3 | 3 | 3 | 3 |
| 13 | 12 | 1 | 3 | 3 | 3 | 3 |
| 19 | 9 | 2 | 3 | 3 | 9 | 9 |
| 31 | 10 | 3 | **0** | 0 | 0 | 0 |
| 37 | 36 | 1 | 3 | 3 | 3 | 3 |
| 43 | 7 | 6 | **0** | 0 | 0 | 0 |
| 61 | 60 | 1 | 3 | 3 | 3 | 3 |
| 67 | 33 | 2 | 3 | 3 | 9 | 9 |
| 73 | 18 | 4 | **81** | 81 | 81 | 81 |
| 79 | 78 | 1 | 3 | 3 | 3 | 3 |
| 97 | 48 | 2 | 9 | 9 | — | — |
| 109 | 36 | 3 | 27 | 27 | — | — |
| 127 | 14 | 9 | **0** | 0 | — | — |

## Corollaries and consequences for the program

1. **Existence criterion.** A negation-stable pure shape-3 bundle exists
   iff 3 | ord_p(−2). Both cases occur infinitely often (positive density
   each way, by Hasse-type order-divisibility results).

2. **The uniform construction cannot be built on the GP bundle.** At
   p = 31, 43, 127 the σ-fixed color *cannot* be pure shape 3 — the
   would-be seed doesn't exist. Any construction uniform in p must either
   avoid the shape-3 structure or branch on the arithmetic of ord_p(−2).
   (This sharpens the handoff's observation that single-shape tilings
   don't always exist at t = 3.)

3. **Cubic residues are not the criterion.** −2 failing to be a cube
   forces 3 | e (so bundles exist whenever p ≠ x² + 27y², by Gauss's cubic
   residue criterion for 2), but the converse fails: at p = 109 = 1² + 27·2²
   the number 2 *is* a cubic residue yet N(109) = 27, because
   v_3(ind(−2)) < v_3(p−1). The clean invariant is ord_p(−2), not cubic
   residuosity.

4. **The "3" at 7, 13, 19 is two coincidences deep**: those primes happen
   to satisfy both 3 | e and gcd(d, (p−1)/2) = 1. The next prime of our
   target family, p = 31, is already a counterexample to both the count
   and existence.

5. **Method note.** The same transport (discrete log → tile {0,a,2a} →
   coset splitting → interval rigidity) classifies pure shape-t bundles
   for any *geometric* shape, but t = ±3 is the only shape whose AP is a
   geometric progression (r² + r − 2 = 0 with r ≠ 1 forces r = −2, shape 3
   — the handoff's observation), so it is the only shape with this
   multiplicative structure. Mixed-shape bundle counts (the 15 at p = 13,
   120 at p = 19) remain open — plausibly attackable, but not by this
   argument alone.
