# FINDINGS — audit ledger (architect-owned)

One row per finding. Auditors never edit this file; the architect adds a row when a report arrives and
updates `recheck` after re-running the finding on the live tree (`AUDIT_START_HERE.md` §Re-check).
`recheck`: `UPHELD` | `NOT REPRODUCED` | `UNVERIFIED` | `open`. `owner`: the task row that fixes it, or
`operator`, or `no change` with the reason.

| id | sev | kind | anchor | defect | recheck | owner |
|---|---|---|---|---|---|---|
| R0-1 | HIGH | security | `_skills/firecrawl-web-scraping-search/API.md:1` | A live Firecrawl API key (`fc-60c8…`) is committed to the **public** repo; `AGENTS.md` §Firecrawl auth tells launchers to read it from there | UPHELD (2026-10-17, `git grep -nE "fc-[A-Za-z0-9]{20,}" main`) | operator: rotate the key; architect: file untracked + gitignored in the audit commit |
| R0-2 | MEDIUM | contract | `labs/comlab/tests/unit/test_tunable_reweight.py:23-25`, `test_abstain_margin_002.py:20` | COMLab tests import `apps/wired` (`v7`, `wired`, `fl_tasks`); the comlab suite fails collection (2 errors) unless wired is installed. Breaks AGENTS.md rule 5 (lab isolation) | UPHELD (`python audit/tools/isolation.py` → 4) | open — task row to move the two tests under `apps/wired/tests/` or mirror the types |
| R0-3 | MEDIUM | doc-drift | `AGENTS.md` rule 5 — "No cross-lab Python imports" | Absolute rule, but `labs/dnalab/docs/ADR_DNALab.md:15` ADR-0002 sanctions `dnalab → vinlab + symptomlab`, and the code uses it (13 imports) | UPHELD | open — add the ADR-0002 exception to rule 5 |
| R0-4 | MEDIUM | robustness | `requirements.txt` | `apps/wired/tests/test_tracing.py` needs `opentelemetry`, which no manifest installs: 2 failures in a clean environment | UPHELD (clean venv 2026-10-17: `2 failed, 9 passed`) | open — add the dependency or mark the tests as needing the tracing extra |
| R0-5 | MEDIUM | doc-drift | `CLAUDE.md` §Environment — "Linux Mint host … Workspace root is `/agent_workspace` (the former `C:\Workspace`)" | The operator works on Windows `C:\Workspace` (2026-10-17); the same section points coders at `.venv-wired` and `4DLab_CLAUDE.md` for a Linux host | UNVERIFIED — which host is current is an operator fact | operator answer, then a doc row |
| R0-6 | LOW | security | `labs/comlab/research/**/*.html`, `*.download` | 14 `AIzaSy…` keys inside saved Gemini web pages: Google's own public web-client keys, not project secrets. Noise for every future secret scan | UPHELD as noise | no change; exclude `labs/*/research/` from scans |

## Watch list (not defects): complexity hot spots, R0 erosion census
`execute_triage_loop` CC 174 (`labs/comlab/comlab/core/fault_atlas_router.py:922`), `apply_differentiators` CC 133
(`labs/gaslab/gaslab/resolution.py:258`), `build_diagnose_payload` CC 115 (`apps/ui/ui_payload.py:822`),
`row_to_raw_inputs` CC 70, `route` CC 70, `_run_obdlab` CC 64. They steer the session order in `PROMPTS.md`.
