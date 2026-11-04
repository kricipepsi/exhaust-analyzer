#!/usr/bin/env bash
# (d) For each row: worktree at the row's accepted commit, restore the row's SOURCE files to the pre-row commit
# (a file absent there is deleted), run the row's NEW test files, print per-test outcomes.
# Usage (repo root, venv active): bash audit/scratch/R3/revert_check.sh > out.txt
set -uo pipefail
W=${TMPDIR:-/tmp}/r3_revert; rm -rf "$W"; mkdir -p "$W"
PKGS="labs/comlab labs/dnalab labs/dtclab labs/gaslab labs/obdlab labs/symptomlab labs/vinlab apps/wired apps/ui"
row() { # name state base rundir "tests" "sources"
  local name=$1 state=$2 base=$3 rundir=$4 tests=$5 srcs=$6 d="$W/$1"
  git worktree add -f "$d" "$state" >/dev/null 2>&1
  for s in $srcs; do
    if git cat-file -e "$base:$s" 2>/dev/null; then git -C "$d" checkout -q "$base" -- "$s"; else rm -f "$d/$s"; fi
  done
  local PP=""; for p in $PKGS; do PP="$PP:$d/$p"; done
  echo "### $name state=$state base=$base reverted: $srcs"
  (cd "$d/$rundir" && PYTHONPATH="${PP#:}" python -m pytest -q -rA --no-header -p no:cacheprovider $tests 2>&1 \
     | grep -E '^(PASSED|FAILED|ERROR) |^[0-9]+ (passed|failed)|error' | sed -E 's/ - .*//' | sort | uniq)
  git worktree remove --force "$d" >/dev/null 2>&1
}
row T-AUD-1c e37bf50 f4f8fc1 apps/ui tests/test_t_aud_1c.py "apps/ui/ui_payload.py apps/wired/wired/composition.py"
row T-AUD-1b 186aa0a 186aa0a^ apps/wired tests/test_t_aud_1b_manifests.py "apps/wired/pyproject.toml constraints.txt labs/comlab/pyproject.toml labs/dnalab/pyproject.toml labs/dtclab/pyproject.toml labs/gaslab/pyproject.toml labs/obdlab/pyproject.toml labs/symptomlab/pyproject.toml labs/vinlab/pyproject.toml requirements.txt"
row T-VINA-1 4191fba 1a32e3c^ labs/vinlab tests/unit/test_year_scope.py "labs/vinlab/vinlab/decoder.py"
row T-VINA-8 597173f 4d6ee41^ labs/symptomlab "tests/test_t_vina_8.py tests/unit/test_symptomdna_from_json.py" "labs/symptomlab/symptomlab/models.py labs/symptomlab/symptomlab/validator.py"
row T-VINA-2 cbd1812 069e188^ labs/vinlab tests/unit/test_type_code_year.py "labs/vinlab/vinlab/decoder.py"
row T-VINA-3 898f9b1 869db2a^ labs/vinlab tests/unit/test_vref_year_window.py "labs/vinlab/vinlab/decoder.py"
row T-VINA-5 bbc1b6e cb31bd8^ labs/vinlab tests/unit/test_wmi_brands.py "labs/vinlab/vinlab/data/wmi.csv labs/vinlab/vinlab/data/vds_engine_map.csv"
row T-VINA-5-wmi-only bbc1b6e cb31bd8^ labs/vinlab tests/unit/test_wmi_brands.py "labs/vinlab/vinlab/data/wmi.csv"
row T-VINA-5-map-only bbc1b6e cb31bd8^ labs/vinlab tests/unit/test_wmi_brands.py "labs/vinlab/vinlab/data/vds_engine_map.csv"
row T-VINA-13a aa7cdbf f836bcf^ labs/vinlab tests/unit/test_extract_tecdoc_1q2019.py "labs/vinlab/tools/extract_tecdoc_1q2019.py labs/vinlab/tools/data/tecdoc_1q2019_engine_extract.csv"
row T-VINA-13a-csv-only aa7cdbf f836bcf^ labs/vinlab tests/unit/test_extract_tecdoc_1q2019.py "labs/vinlab/tools/data/tecdoc_1q2019_engine_extract.csv"
row T-VINA-13b 2dfbbba 5bf69e5^ labs/vinlab tests/unit/test_vref_tecdoc_merge.py "labs/vinlab/tools/merge_tecdoc_extract.py labs/vinlab/tools/build_vref_db.py labs/vinlab/vinlab/data/vref.db"
row T-VINA-13b-db-only 2dfbbba 5bf69e5^ labs/vinlab tests/unit/test_vref_tecdoc_merge.py "labs/vinlab/vinlab/data/vref.db"
