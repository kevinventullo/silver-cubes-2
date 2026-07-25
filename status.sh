#!/bin/zsh
# Quick status of detached silver-cube jobs (see JOBS.md)
cd "$(dirname "$0")"
echo "== processes =="
ps -o pid,etime,%cpu,command -p 12293,12875,12931 2>/dev/null \
  | sed 's/\/Library.*Python //' || echo "(none alive)"
echo
echo "== prime sweep (block model + pure shape) =="
tail -6 results/log_mult_sweep.txt 2>/dev/null
echo
echo "== template sweep (uniform construction hunt) =="
grep -E "^=== |^  p=[0-9]+:" results/log_mult_template.txt 2>/dev/null | tail -8
echo
echo "== verified cubes on disk =="
for f in results/cube_p*_mult.txt results/cube_p*fullmult.txt results/cube_p*_block.txt; do
  [ -e "$f" ] && echo "  $f"
done
