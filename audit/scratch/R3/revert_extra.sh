#!/usr/bin/env bash
# (d) extras: (1) whole vinlab suite at the tip with vref.db restored to its pre-T-VINA-13b bytes;
# (2) T-VINA-1 behaviour revert: decoder.py at 1a32e3c^ plus the two constants the test imports.
set -uo pipefail
W=${TMPDIR:-/tmp}/r3_revx; rm -rf "$W"; mkdir -p "$W"
git worktree add -f "$W/db" HEAD >/dev/null 2>&1
git -C "$W/db" checkout -q 5bf69e5^ -- labs/vinlab/vinlab/data/vref.db
echo "### tip, vref.db at 5bf69e5^ (72 rows): whole vinlab suite"
(cd "$W/db/labs/vinlab" && PYTHONPATH="$W/db/labs/vinlab" python -m pytest -q --no-header -p no:cacheprovider 2>&1 | tail -1)
git worktree remove --force "$W/db"
git worktree add -f "$W/y" 4191fba >/dev/null 2>&1
git -C "$W/y" checkout -q 1a32e3c^ -- labs/vinlab/vinlab/decoder.py
printf '\n_YEAR_MIN, _YEAR_MAX = 1990, 2010  # R3 probe: constants only\n' >> "$W/y/labs/vinlab/vinlab/decoder.py"
echo "### T-VINA-1 behaviour revert (constants kept)"
(cd "$W/y/labs/vinlab" && PYTHONPATH="$W/y/labs/vinlab" python -m pytest -q -rA --no-header -p no:cacheprovider tests/unit/test_year_scope.py 2>&1 | grep -E '^(PASSED|FAILED|ERROR) |passed|failed' | sed -E 's/ - .*//')
git worktree remove --force "$W/y"
