#!/bin/sh
# Keep `mult_targeted.py 43` alive until it produces a terminal verdict.
#
# Motivation: an earlier run of this job completed p=37 and then exited during
# p=43 without printing either a hit or its end-of-run line, and without a
# traceback. A silent death is indistinguishable from "still running" if you
# only read the log, so this restarts the job (up to MAX times) and stamps
# every start/exit into the log.
#
# Terminal states, either of which stops the watchdog:
#   "p=43 ... *** VERIFIED ***"   -> a signature works at 43
#   "p=43: no signature works"    -> exhausted all 288 combinations
cd "$(dirname "$0")"
LOG=results/log_mult_targeted.txt
MAX=6
i=0
while [ "$i" -lt "$MAX" ]; do
    if grep -qE "p=43 .*VERIFIED|p=43: no signature works" "$LOG" 2>/dev/null; then
        echo "=== [watchdog] terminal verdict present; done $(date) ===" >> "$LOG"
        exit 0
    fi
    if ! pgrep -f "mult_targeted.py 43" > /dev/null 2>&1; then
        i=$((i + 1))
        echo "=== [watchdog] start #$i $(date) ===" >> "$LOG"
        PYTHONPATH=code .venv/bin/python code/mult_targeted.py 43 >> "$LOG" 2>&1
        echo "=== [watchdog] run #$i exited status $? $(date) ===" >> "$LOG"
    fi
    sleep 60
done
echo "=== [watchdog] gave up after $MAX restarts $(date) ===" >> "$LOG"
