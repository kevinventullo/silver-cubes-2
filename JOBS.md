# Detached compute jobs

Run under `nohup` (OS-owned; survive harness events, NOT reboot).
Status: `./status.sh`

## Active

| job | pid | command | log |
|---|---|---|---|
| targeted test at p = 43: do any of the 18 candidate signatures work? 120 s per solve | 20484 | `PYTHONPATH=code .venv/bin/python code/mult_targeted.py 43` | `results/log_mult_targeted.txt` |

Success: a line `p=43 ... *** VERIFIED ***`. That would put the §7 rule of
`14Handoff.md` at five primes (13, 19, 31, 37, 43) and would make 43 the
first order reached by *predicting* the configuration rather than searching
for it — the raw block model gave no verdict at 43 on any of four
2400 s arms. Failure mode: the run ends with `p=43: no signature works`,
which would confine the rule to p ≤ 37.

Expect 20–60 min if a hit exists early; up to a few hours to exhaust all
288 combinations (18 signatures × 2 swaps × 8 transversal indices).

An earlier run of this job (pid 19025) completed p = 37 — **hit**, see
below — then exited during p = 43 without printing either a hit or its
end-of-run line. Cause unknown; no traceback. Restarted 2026-07-25.

## Results so far (2026-07-25, multiplicative-symmetry framework)

New cubes, each verified three independent ways (`code/verify.py`,
`kv_manual_verification.py`, pipeline check):

- **p = 19** — `results/cube_p19_mult.txt`, `cube_p19_fullmult.txt`
- **p = 31** — `results/cube_p31_fullmult.txt`, `cube_p31_block.txt`
- **p = 37** — `results/cube_p37_block.txt`

Template sweep `code/mult_template.py` (log `results/log_mult_template2.txt`),
verified tuples of those passing sizes/disjointness:

| p | verified / size-valid | distinct signatures |
|---|---|---|
| 13 | 72 / 216 | 18 |
| 19 | 72 / 216 | 18 |
| 31 | 245 / 864 | 27 (⊃ the 18) |
| 37 | targeted hit at sig (0,1,2,1,2,0), v = 2, swap = 1 | — |

The 18 signatures common to 13, 19, 31 are cut out exactly by
`miss ≡ one + δ − φ`, with `one ≡ φ+δ` if `γ=δ` and `one ≢ φ+δ` if `γ=ε`
(cls(v) ≡ 1 normalised). See `14Handoff.md` §7.

## Stopped / superseded — do not relaunch

- `mult_template.py 13 19 31 37 43` (pid 17326): completed 13, 19, 31; killed
  during 37 because its 20 s solve cap manufactures false negatives at
  p ≥ 37 (14Handoff.md §7, Trap 3). Default is now 120 s. The 13/19/31
  numbers in `log_mult_template2.txt` are sound.
- `results/log_mult_template.txt` (pre-correction): used the generic
  `fixed_part`, which times out at p ≥ 31 and reports spurious failures.
  Its "0 verified at p=31" is **wrong**. Superseded by `log_mult_template2.txt`.
- `mult_sweep.py 31 37 43 61 67`: solved 31 (13 s) and 37 (391 s); **no
  verdict at 43 or 61** on any shape arm (4 and 5 arms × 2400 s). The raw
  block model runs out at p = 43. Log: `results/log_mult_sweep.txt`.
- Everything from the previous dihedral framework (p19A, p19-SAT, probe
  bursts, bulkgen): superseded — p = 19 now takes 0.5 s.
