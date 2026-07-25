# Detached compute jobs

Run under `nohup` (OS-owned; survive harness events, NOT reboot).
Status: `./status.sh`

## Active (2026-07-25, multiplicative-symmetry framework)

| job | pid | command | log |
|---|---|---|---|
| targeted test: do the 18 candidate signatures (common to p = 13, 19, 31) also work at p = 37 and 43? 120 s per solve | 19025 | `PYTHONPATH=code .venv/bin/python code/mult_targeted.py 37 43` | `results/log_mult_targeted.txt` |

Success criterion: any signature verifying at 37 and at 43. That would make
the rule of 14Handoff.md §7 hold at five primes.

### Stopped

- template sweep `code/mult_template.py 13 19 31 37 43` (pid 17326):
  **completed 13, 19, 31** — 72/216, 72/216, 245/864 verified, i.e. 18, 18
  and 27 signatures with the 18 common to all three. Killed during p = 37
  because its 20 s solve cap manufactures false negatives at p ≥ 37 (see
  14Handoff.md §7, Trap 3); the targeted test above replaces it. Log:
  `results/log_mult_template2.txt` — the 13/19/31 numbers in it are sound.

- **Do not use** `results/log_mult_template.txt` (pre-correction): that run
  solved the fixed half with the generic `fixed_part`, which times out at
  p ≥ 31 and reports spurious failures ("0 verified at p=31" is wrong — the
  template reproduces the verified p=31 cube exactly). Superseded by
  `log_mult_template2.txt`, which uses `fixed_part_blocks`.
- `mult_sweep.py 31 37 43 61 67` (block model + pure shape, 2400 s arms):
  solved **31** (13 s) and **37** (391 s); **43 and 61 gave no verdict on
  any shape arm** (4 and 5 arms respectively, 2400 s each), killed during 67.
  The raw block model runs out of steam at p = 43 — the template route is
  the way up from here. Log: `results/log_mult_sweep.txt`.

## Done (this framework)

- p = 19: verified, `results/cube_p19_mult.txt`, `cube_p19_fullmult.txt`
- p = 31: verified, `results/cube_p31_block.txt`, `cube_p31_fullmult.txt`
- p = 37: verified, `results/cube_p37_block.txt`
- ι-invariant tilings: INFEASIBLE at p = 7…67 (rigidity fact, 14Handoff.md §8)
- the p=13/19 class assignment fails at 31, 37, 43 (corrected: was a fixed_part timeout, 14Handoff.md §7)

## Stopped / superseded (previous framework — do not relaunch)

- p19A (CP-SAT dihedral, Φ-broken), p19-SAT (CaDiCaL monolith): both ran
  ~24 h+ with no verdict. Superseded: p = 19 now takes 0.5 s.
- p13 probe bursts, known-half calibration: were measuring the hardness of
  clamping a *fixed* half. The new framework clamps the *cycle* halves
  instead, which is the easy direction.
- bulkgen p13 (population 239 in `results/pop_p13_t1_h1.jsonl`): mining
  dihedral solutions for a backbone. The backbone turned out to live in a
  family the dihedral model cannot represent.
