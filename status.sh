#!/bin/zsh
# Quick status of detached silver-cube jobs (see JOBS.md).
# NOTE: results/log_mult_template.txt is the PRE-CORRECTION sweep and its
# numbers are wrong (see JOBS.md). Always read log_mult_template2.txt.
cd "$(dirname "$0")"
echo "== running jobs =="
ps -e -o pid,etime,%cpu,command | grep -E "mult_|code/(solve|satmono|probe)" \
  | grep -v grep | sed 's/\/Library.*Python //' || true
[ -z "$(ps -e -o command= | grep mult_ | grep -v grep)" ] && echo "  (none)"
echo
echo "== targeted test: 18 candidate signatures at p=37,43 =="
cat results/log_mult_targeted.txt 2>/dev/null
echo
echo "== template sweep (corrected; 13/19/31 are sound) =="
grep -E "^=== |passed size" results/log_mult_template2.txt 2>/dev/null
echo
echo "== verified cubes on disk =="
for f in results/cube_p*_mult.txt results/cube_p*fullmult.txt results/cube_p*_block.txt; do
  [ -e "$f" ] && echo "  $f"
done
echo
echo "== re-verify everything (slow-ish) =="
echo "  for f in results/cube_p{19_mult,19_fullmult,31_block,31_fullmult,37_block}.txt; do"
echo "    .venv/bin/python code/verify.py \$f; done"
