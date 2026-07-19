# Nemo — manual notes (human-readable; NOT omp durable memory)
Repeated build/test gotchas, local quirks, and patterns worth re-reading. One fact per line.
Do not store secrets. Native durable memory is omp **mnemopi** (`retain`/`recall`); this file is the
part a human wants to skim and version in git.
## Environment — Linux host (recorded 2026-06-30)
- HARNESS: omp, profile `nemo`, model `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` (OpenRouter;
  1M context, reasoning efforts minimal/low/medium/high). Launched by `run-nemo.sh`. Auth via `$OPENROUTER_API_KEY`.
- TRANSPORT: `run-nemo.sh` exports `PI_OPENROUTER_RESPONSES=0` so omp uses /chat/completions, not the
  OpenAI Responses API. Verified 2026-06-30: the /responses path errored (upstream Nvidia
  ResourceExhausted); /chat/completions returned a clean `NEMO_OK`.
- FREE TIER: the `:free` endpoint is capacity-limited and can return `ResourceExhausted` under load.
  If sessions start failing intermittently, switch `NEMO_MODEL` to the paid `nvidia/nemotron-3-ultra-550b-a55b`
  (no `:free`) — same id without the suffix.
- SETUP WIZARD: `run-nemo.sh` exports `OMP_SKIP_SETUP=1`; a fresh profile otherwise shows the onboarding
  picker (login-providers only) and ignores `--model`. If the wizard ever wedges, `rm -rf ~/.omp/profiles/nemo`
  then relaunch.
- SKILLS: `skill://<name>` resolves from `.agent/skills/` (git-ignored), wired by `scripts/wire_skills.sh`
  (run automatically by run-nemo.sh on launch). If `skill://X` errors `Unknown skill … Available: none`,
  run `bash scripts/wire_skills.sh` from `/agent_workspace`, then retry.
- PYTHON: ONE shared venv `/agent_workspace/.venv-wired` (Python 3.14, uv-built). Use
  `source /agent_workspace/.venv-wired/bin/activate`, or call `/agent_workspace/.venv-wired/bin/python`.
- SPEED/QUALITY: `:free` is throttled (slow). Launcher pins `--thinking=${NEMO_THINKING:-medium}`
  (medium = viable default for gated implementation) + `--hide-thinking`. Dial per task:
  `NEMO_THINKING=low` (trivial), `=high` (gnarly). Real throughput jump = leave `:free` (paid
  Ultra) or switch `NEMO_MODEL` to faster `nvidia/nemotron-3-super-120b-a12b`. Gates (ruff/pyright/
  pytest) are the quality guarantee regardless of effort.
- CURRENT_WORKING_FOLDER: /agent_workspace/ECO (recorded 2026-07-03)
