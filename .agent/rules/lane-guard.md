# Lane-guard — architect (Cowork) vs coder (omp) lane separation  [resolves D3]

POLICY (human-readable). ENFORCEMENT lives in `.omp/rules/*.md` as omp **TTSR** rules.
omp 16.1.19 discovers project rules from `<project>/.omp/rules/`; inspect with `omp ttsr list`,
test with `omp ttsr test`.

Lanes:
- **Architect = Cowork.** Authors specs (`labs/<lab>/tasks/<id>.md`), ROADMAP/DECISIONS, and
  `.agent/assignments.md`. Reviews gates. Does NOT implement. `graphify` is the architect's call.
- **Coders = Codex, Agy (omp).** Implement ONE assigned task; write `progress_notes/<id>.md` gates and
  flip the `PROGRESS.md` row. Do NOT author specs/roadmap/assignments, act as architect, rebuild graphs,
  or edit the other coder's `.agent/coders/<other>/`.

Enforced TTSR rules (.omp/rules/):
- `lane-guard-no-graphify`    → blocks a coder rebuilding graphs.
- `lane-guard-no-assignments` → blocks a coder writing `.agent/assignments.md`.

Deferred to per-coder profiles (created with /home/m/.omp-codex | .omp-agy during migration):
- Codex↔Agy mutual-exclusion mirror rules belong in each coder's OWN profile rules dir, because a single
  shared project rule cannot tell which coder is running. Until then the hard boundary lives in each
  coder's identity file `.agent/coders/<name>/AGENTS.md`.
