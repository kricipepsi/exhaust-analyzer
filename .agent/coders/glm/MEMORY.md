# GLM — manual notes (human-readable; NOT omp durable memory)
Repeated build/test gotchas, local quirks, and patterns worth re-reading. One fact per line.
Do not store secrets. Native durable memory is omp **mnemopi** (`retain`/`recall`); this file is the
part a human wants to skim and version in git.
## Environment — Linux host (recorded 2026-06-30)
- HARNESS: omp, profile `glm`, model `openrouter/z-ai/glm-5.2` (OpenRouter; 1M context, reasoning
  efforts minimal/low/medium/high/xhigh). Launched by `run-glm.sh`. Auth via `$OPENROUTER_API_KEY`.
- SKILLS: `skill://<name>` resolves from `.agent/skills/` (git-ignored), wired by
  `scripts/wire_skills.sh` (run automatically by run-glm.sh on launch). If a `skill://X` ever errors
  `Unknown skill … Available: none`, run `bash scripts/wire_skills.sh` from `/agent_workspace`, then retry.
- PYTHON: ONE shared venv `/agent_workspace/.venv-wired` (Python 3.14, uv-built). Use
  `source /agent_workspace/.venv-wired/bin/activate`, or call `/agent_workspace/.venv-wired/bin/python`.
