#!/usr/bin/env bash
# Wire repo skills into .agent/skills/ so omp's `skill://<name>` discovery resolves them.
#
# Why: omp only discovers skills from conventional dirs (.agent/skills, .claude/skills,
# skills/, …). This repo keeps skills in per-lab `_<lab>_skills/` and shared `_skills/`,
# which omp never scans. This script leaves them in their homes and creates omp-discoverable
# symlinks keyed by each skill's frontmatter `name`. Idempotent; safe to re-run.
#
# Guard: omp loads .agent/skills/* as one batch; a SINGLE unparseable YAML frontmatter
# makes that batch throw and discover ZERO skills ("Available: none"). So we validate
# frontmatter and skip the broken ones loudly, instead of letting one typo nuke them all.
#
# .agent/skills/ is git-ignored (machine-local wiring, reconstructable). Re-run after adding
# or renaming a skill. The omp launchers (run-*.sh) call this before launch.
set -euo pipefail
cd "$(dirname "$0")/.."                      # repo root (/agent_workspace)
DEST=.agent/skills
rm -rf "$DEST"; mkdir -p "$DEST"

# Collect candidate SKILL.md files once (used for both the guard and the wiring loop).
mapfile -t skills < <(find . \( -path ./.git -o -path ./ARCHIVE \) -prune -o -name SKILL.md -print \
          | grep -vE '_skills/graph/skilltest-out/|planning/skill_eval/trials|/managed-skills/|/\.agent/skills/')

# Guard: flag SKILL.md files whose YAML frontmatter fails to parse. No-op (blocks nothing)
# if python3/PyYAML is unavailable, so the guard can never itself break wiring.
declare -A bad_fm
if command -v python3 >/dev/null 2>&1; then
  while IFS= read -r bad; do [ -n "$bad" ] && bad_fm["$bad"]=1; done < <(
    python3 - "${skills[@]}" <<'PY'
import sys
try:
    import yaml
except Exception:
    sys.exit(0)  # no validator available -> don't block wiring
for p in sys.argv[1:]:
    try:
        t = open(p, encoding='utf-8', errors='replace').read()
        if t.lstrip().startswith('---'):
            parts = t.split('---', 2)        # ['', frontmatter, body]
            if len(parts) >= 3:
                yaml.safe_load(parts[1])     # raises on malformed frontmatter
    except Exception:
        print(p)
PY
  )
fi

declare -A seen
count=0; dupes=0; skipped=0
for skill in "${skills[@]}"; do
  if [ -n "${bad_fm[$skill]:-}" ]; then
    echo "  SKIP bad YAML frontmatter -> $skill" >&2
    skipped=$((skipped+1)); continue
  fi
  dir=$(dirname "$skill")
  name=$(awk -F':[[:space:]]*' '/^name:/{gsub(/["'\''[:space:]]/,"",$2); print $2; exit}' "$skill")
  [ -z "$name" ] && name=$(basename "$dir")
  if [ -n "${seen[$name]:-}" ]; then
    echo "  DUPE name '$name' -> $dir  (kept ${seen[$name]})" >&2
    dupes=$((dupes+1)); continue
  fi
  seen[$name]="$dir"
  ln -sfn "$(realpath --relative-to="$DEST" "$dir")" "$DEST/$name"
  count=$((count+1))
done

echo "wired $count skills into $DEST ($dupes dup-name(s), $skipped bad-frontmatter skipped)"
