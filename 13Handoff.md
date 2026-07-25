# Silver Cube Project — Conceptual Handoff

A self-contained conceptual brief: the problem, what we understand, and
the live ideas for generalizing. Deliberately free of implementation
details — it is about the mathematics and the strategy.

## The problem

A **silver (n,3)-cube** is a coloring of the n×n×n Hamming graph (vertices
[n]^3, edges join words differing in one coordinate) with 3n−2 colors,
together with a *diagonal* — a maximum independent set of size n^2 — such
that the closed neighborhood of every diagonal vertex (itself plus its
3(n−1) neighbors, 3n−2 vertices in all) is rainbow: every color exactly
once.

Existence is conjectured for all n. A **multiplicativity theorem** (given)
says silver cubes of orders m and n yield one of order mn, so the
conjecture reduces to **prime** orders. The classical cases 2,3,5,7 were
known. Earlier iterations with Claude added verified constructions at 11 and 13 and is pushing
toward a general statement. We always use the **linear diagonal**
{x+y+z ≡ 0 (mod n)}.

**Current goal.** Establish existence for as many primes as possible,
ideally via a *uniform construction* for the tractable family. The
appetite is for clever structure that collapses the search, not for
open-ended brute force. So the central question is: **what narrow,
generalizable structure do solutions share?**

## The reductions that make it tractable

**1. From rainbow condition to graph coloring.** Index the diagonal by
points (x,y). Each off-diagonal vertex with "defect" s = x+y+z ≠ 0 is
adjacent to exactly three diagonal vertices — a *corner triple*
{(x,y), (x−s,y), (x,y−s)} — and this correspondence is a bijection onto
all n^2(n−1) such triples. Two triples conflict iff they share a point.
The upshot:

> A silver (n,3)-cube exists **iff** the intersection graph of the corner
> triples is properly (3n−2)-colorable.

The diagonal coloring is then *forced*: each point lies in exactly 3n−3
triples, which use 3n−3 distinct colors, and the diagonal vertex takes the
unique missing color. The awkward "rainbow + choose a diagonal" problem
becomes one clean coloring problem.

**2. A parity obstruction.** Counting shows every color class meets the
diagonal in a number of points ≡ 1 (mod 3). This rules out the naive
"color by layer and direction" schemes.

**3. Equivariance and a dichotomy by p mod 3.** Impose invariance under a
cyclic translation of order p. This forces the color action to be *two
p-cycles plus (p−2) fixed colors*; each fixed color owns a full
translation-line of the diagonal, each cycled color a single point. This
symmetry is **possible exactly when p ≡ 1 (mod 3)** and **provably
impossible when p ≡ 2 (mod 3)**. So:

- **p ≡ 1 (mod 3)** (7, 13, 19, 31, 37, …): the "good" family, where all
  the structural program lives.
- **p ≡ 2 (mod 3)** (11, 17, 23, …): equivariance is unavailable; these
  require a genuinely different, non-equivariant idea. (An 11-cube is
  known to exist by other means, confirming they are not hopeless — just
  outside the current framework.)

**4. Coordinates on the symmetry-reduced problem.** Modulo translation,
an orbit is a pair (δ, s): a "coset" δ and a scale s. Its footprint on the
diagonal is the 3-term arithmetic progression {δ−s, δ, δ+s}. A fixed color
is then a bundle of orbits whose APs *partition* the cosets minus one; a
cycled color class is a larger bundle of orbits with "phases" that tile a
2D torus minus a point. This recasts the whole object as two interacting
tiling problems.

**5. A second symmetry: negation.** Adjoining the central involution
(x,y,z) ↦ (−x,−y,−z) gives a **dihedral group of order 2p**. It swaps the
two color-cycles and pairs fixed colors on opposite cosets {d, −d},
roughly halving the degrees of freedom. This is the most effective
symmetry level: pushing further (a four-fold extension) over-constrains
and admits nothing.

**6. Symmetry-breaking is the real lever.** Even within the dihedral
ansatz, relabeling colors leaves an enormous redundancy (permute the fixed
colors, rotate each cycle, translate, negate). Pinning a canonical
representative — fixing which coset hosts each "hole" and which fixed color
owns which coset — removes that redundancy and is, empirically, *the*
ingredient that turned an intractable search into a solvable one. The
lesson generalizes: **the payoff comes from symmetry reduction plus
canonicalization, not from guessing the answer's fine structure.**

## What we understand about the structure of solutions

The reduction splits a solution into two very different halves.

**The fixed-color half — partially algebraic.** Each fixed color
partitions the nonzero cosets (minus the one it sits on) into 3-term APs.
Assign each AP a multiplicative "shape" t = (its common difference)/(its
center). A clean hope: all APs share one shape, i.e. the fixed system is
"scale one base triangle multiplicatively, then translate." There is a
pretty fact behind this — the only shape whose triangle is a *geometric
progression* {1, r, r²} is t = 3 (forced by r² + r − 2 = 0 with r ≠ 1,
giving r = −2). And such a single-shape tiling does exist for many primes
(every p ≡ 1 mod 3 we checked admits *some* tiling shape, though not
always t = 3).

**But this clean picture is essentially a small-prime accident.** At p = 7
every fixed color is pure shape 3; at p = 13 the actual solutions use
*mixed* shapes, even within a single color. Forcing single-shape structure
at 13 appears to over-constrain to the point of infeasibility. So the
"multiplicative tiling" is a real and beautiful phenomenon at the bottom,
but **it is not, as stated, the universal pattern** — and imposing it
hurts rather than helps at the sizes we care about.

**The cycle half — opaque.** The two cycled color classes show no
discernible closed form: the orbit-to-class assignment and the phases look
generic. This is the genuine obstacle to a uniform construction. A theorem
needs *both* halves describable; right now only the fixed half has any
algebra, and even that is fragile.

**Net assessment.** The thing that transfers from prime to prime is the
*method* (dihedral symmetry + canonical pinning + a constraint solver),
not a formula. We can reliably *generate* cubes this way; we cannot yet
*write one down* a priori for a new prime.

## The p = 13 case in detail

**How it was found — the search narrative.** The progression of effort is
itself informative about what does and does not work.

- *Direct coloring failed.* For n = 13 the corner-triple graph has 2028
  vertices, about 103,000 edges, clique number exactly 36, and target
  3n−2 = 37 colors — so it is a "tight" instance (chromatic number one
  above the clique number). Greedy coloring (DSATUR) needs 46 colors.
  Local search (tabu, iterated local search, evolutionary recombination)
  on the full graph plateaued at roughly 18–26 conflicting edges and never
  reached zero. Off-the-shelf SAT and constraint solvers on the raw,
  unsymmetrized problem returned no verdict in reasonable time. The 37-
  coloring is genuinely hard to hit by unstructured methods.

- *Equivariance shrank the problem but wasn't enough alone.* Imposing
  order-13 translation symmetry collapsed 2028 triple-variables to 156
  orbit-variables. This ansatz was validated on the small cases (fast SAT
  at n = 5, 7; UNSAT at n = 11, exactly matching the proof that p ≡ 2 mod 3
  cannot be equivariant). Yet the equivariant instance *still* would not
  resolve, because it carried a vast residual symmetry: any solution could
  be relabeled in on the order of 10^10 equivalent ways (permuting the 11
  fixed colors, independently rotating each 13-cycle of colors, plus
  translating and negating).

- *Canonical pinning was the breakthrough.* Fixing a canonical
  representative removed that redundancy. Concretely: declare cycle-A's
  distinguished point to sit at coset 0 with the diagonal point (0,0)
  taking color 0; cycle-B's distinguished point at coset δ_B; and the i-th
  remaining coset owned by the i-th fixed color. Up to the cube's own
  automorphisms there are only three inequivalent translation directions
  ("slopes") and a handful of choices for δ_B, so the pinned problem splits
  into a small number of sub-instances that are *jointly exhaustive* for
  equivariant cubes — if all are infeasible, none exists; otherwise one
  yields a cube. Handed this pinned model, a constraint solver returned an
  optimal (satisfying) assignment on the first sub-instance tried, in a few
  hours on a handful of cores. The same model *without* pinning had run far
  longer with no answer. The decisive ingredient was symmetry reduction
  *followed by canonicalization*, not any guess about the solution's
  internal arithmetic.

- *Later, more cubes came cheaply.* Adding the negation symmetry (the
  order-26 dihedral model) and varying the pinned representative produced
  additional distinct 13-cubes quickly, and the solver can enumerate them
  in bulk — which is what makes population-mining (below) feasible.

**What the resulting cubes look like.**

- *Exact translation symmetry.* The headline cube is invariant under
  τ : (x,y,z) ↦ (x+1, y+1, z−2) of order 13, with the color action
  ρ = (0 1 … 12)(13 14 … 25) fixing colors 26…36; that is,
  c(τ·v) = ρ(c(v)) at all 2197 vertices (checked directly).

- *The forced color profile.* The 37 colors split exactly as the theory
  predicts: 11 "fixed" colors, each appearing on a full translation-line
  of the diagonal (13 diagonal points apiece), and 26 "cycled" colors,
  each on a single diagonal point. The count checks: 11·13 + 26·1 = 169 =
  13². Equivalently the two 13-cycles of ρ account for 26 single-point
  colors and the 11 fixed points of ρ for the 11 line-colors.

- *Fixed-color fine structure.* Each fixed color owns a coset a and
  partitions the other twelve cosets into four centered 3-term APs
  {δ−s, δ, δ+s}. The "shapes" of these APs (common difference over center,
  read multiplicatively) are **mixed** — e.g. one color's four APs have
  shapes {2,2,3,5}, another's {5,5,6,6}. This is the key negative datum:
  unlike n = 7, where every AP is shape 3, the n = 13 cube has no single-
  shape (hence no purely "scale-one-triangle") fixed system, which is why
  imposing single-shape structure over-constrains it.

- *Dihedral cubes.* Among these solutions are ones also invariant under
  negation v ↦ −v: there cycle B is exactly the negation image of cycle A,
  and the fixed colors pair off on opposite cosets {d, −d} (which sum to 13
  here). These dihedral solutions are the cleanest and the natural objects
  to compare across primes.

- *Tightness and multiplicity.* The coloring is tight (37 = clique number
  + 1), and the cube is far from unique — many genuinely distinct 13-cubes
  exist (across slopes, pinnings, and within each, large enumerable
  families). That abundance is encouraging for finding a *shared* backbone.

## Approaches to generalization (the live ideas)

The strategic bet is that a *uniform construction* — and hence a general
theorem for p ≡ 1 (mod 3) — exists, and that it will reveal itself as a
**narrow constraint shared by all solutions** rather than as an obvious
formula. Concretely:

1. **Hunt for a backbone.** Generate large *populations* of solutions at
   p = 7 and p = 13 and ask: which facts hold in *every* solution? (Is a
   given orbit always fixed? always in a particular cycle? Is its color
   determined?) The set of always-true facts is a "backbone." A backbone
   fact that can be *described arithmetically* (a predicate on s, on δ, on
   their sum/difference, on quadratic or cubic character) and that holds at
   *both* primes is a candidate **universal law**. Imposing it would shrink
   the search for the next prime enormously — possibly to instantaneous —
   and would be the seed of a proof.

2. **Let the constraint emerge, then verify it lifts.** Any pattern
   conjectured from 7 and 13 should be (a) checked for satisfiability at
   both, then (b) imposed and tested at 19. A pattern that survives 7, 13,
   and 19 is strong evidence of universality and a concrete target to
   prove for all p ≡ 1 (mod 3). A pattern that dies at 19 is discarded
   cheaply. The earlier "single shape" hypothesis is the cautionary
   template: clean at 7, dead by 13.

3. **Mine with statistics / learning, not just eyeballing.** With
   thousands of solutions per prime, treat orbit→role as a labeled dataset
   and look for a *simple* high-accuracy predictor from arithmetic
   features. A simple model that predicts well *is* the pattern; a model
   that needs to be complex is evidence the structure is genuinely generic
   (and that we should lean on raw symmetry-reduced compute instead).

4. **Attack the cycle half directly.** Since the cycle classes are
   themselves tiling problems on a torus minus a point — structurally an
   echo of the original problem — it is worth asking whether they admit a
   recursive or multiplicative description analogous to (and perhaps
   inheriting from) the fixed half. Cracking the cycles is the difference
   between "we can compute cubes" and "we have a theorem."

5. **Compute as fallback, scoped tightly.** If no transferable law
   appears, existence at a specific new prime is still reachable by running
   the unconstrained symmetry-reduced model (varying the symmetry direction
   and the pinned representative as a small portfolio). This buys
   individual primes but not the family, and the cost grows fast with p, so
   it is the backstop, not the plan.

6. **The other residue class.** Primes p ≡ 2 (mod 3) sit entirely outside
   the equivariant framework. Progress there needs a separate idea —
   either a weaker/different symmetry, or leveraging how known cubes in
   that class were built. This is logically independent of the p ≡ 1 (mod
   3) program and should be treated as its own track.

## One-line summary

Silver cubes reduce to a structured graph-coloring problem; a dihedral
symmetry plus canonical pinning makes individual primes (≡ 1 mod 3)
solvable and gave us 13; the open frontier is finding the *narrow,
arithmetic, cross-prime invariant* — most plausibly via backbone-mining of
large solution populations — that would turn "we can compute one" into "we
can construct them all."
