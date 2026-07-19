# T-V7-3 — Fill the v7 oracle from domain truth (wiki/atlas + library conclusions)

**Authored by:** architect (Cowork), 2026-06-30 · **Status:** `deferred` (→ `pending` when T-V7-2 is `done`) · **Blocked by:** T-V7-2
**Mode:** STRICT — fills the oracle columns + a triage note under `apps/wired/v7/`; **no source edits**. · **Scope owner:** wired-v7.
**Load skills:** wired-python, wired-verification-loop, wired-code-review.

## Objective
Fill the empty `expected_*` columns of `cases_petrol_v7.csv` with expectations pinned
from **domain truth** — the lab wikis + current fault atlas, corroborated by the
library's documented conclusion — so the suite measures the engine against
documented expectation, not itself. Multiple expectation dimensions are pinned so the
suite can catch every error class. Wiki-unpinnable cases are tagged
**characterization** (no-crash only, out of the accuracy %).

## Signal/noise
Adds no domain field or fault. The **named consumer** is the scorer T-V7-4 and the
architect (the wiki↔library disagreement list is a finding). The oracle lives in the
same CSV (filled columns) + a sidecar triage note.

## Pinned facts (verified at authoring)
- Truth (priority order): `labs/<lab>/wiki/` (rule 2) + current closed taxonomy
  `labs/comlab/comlab/schemas/vocabulary.py` + `core/fault_atlas_kg.py`; the library
  Conclusion is **corroboration**, not the primary source. **Never** `ARCHIVE/`,
  **never** `diagnose()` output.
- Assertable verdict fields: confirm the exact set from
  `comlab.schemas.response.OrchestratorFinalUIOutput.diagnostic_verdict` — pin only
  the dimensions the wiki actually supports per case.
- CSV + viability tags + `source_ref` come from T-V7-2.

## Scope
**IN:**
- For each non-negative row, fill the `expected_*` it can support, each with a
  `wiki_ref` (`labs/<lab>/wiki/<file>#<anchor>`):
  - `expected_fault_family` (must be in the current vocabulary) — required for an
    `accuracy` case;
  - `expected_fault_code` only if the wiki pins a specific code (else family-level);
  - `expected_state`, `expected_confidence_min/max`, `expected_perception_gap`,
    `expected_demotion_note_contains` — each only where the wiki/atlas pins it.
- Tag each row `accuracy` (wiki pins ≥ the family) or `characterization` (wiki silent
  → no-crash only); state the split counts.
- Negative/edge rows: pin the expected HANDLED/abort outcome, not a fault.
- Write `apps/wired/v7/ORACLE_TRIAGE_<date>.md`: where wiki and the library Conclusion
  **disagree**, where the wiki is ambiguous, and where you suspect (not assert) the
  engine diverges from the wiki — each a named follow-up, **not** fixed here. A
  library-vs-wiki conflict resolves in favour of the **wiki** (truth), and the
  conflict is logged.
- Validate: every `accuracy` row's `expected_fault_family` ∈ current vocabulary; every
  filled row has a `wiki_ref`; every CSV row is covered.

**OUT:** running `diagnose()` to populate expectations (tautology — forbidden);
trusting the library Conclusion over the wiki; reading `ARCHIVE/`/legacy oracle;
inventing a family not in `vocabulary.py`; editing `wired/`/labs/COMLab/wikis;
`graphify`; `Vault/`.

## Steps
1. Per row, open the `source`/wiki section (query the lab graph first); pin the
   expectations the wiki supports — nothing stronger.
2. Where the library Conclusion conflicts with the wiki, take the wiki, log the
   conflict in the triage note.
3. Tag `accuracy`/`characterization`; fill negatives' expected outcome.
4. Validate vocabulary membership + full row coverage + `wiki_ref` presence.
5. Fill `v7_tasks/progress_notes/T-V7-3.md` gates; STOP.

## Success criteria
- Every CSV row has its oracle resolved; every `accuracy` row carries a `wiki_ref` and
  an `expected_fault_family` in the current vocabulary; **no** expectation derived from
  `diagnose()` output or taken from the library over the wiki.
- The `accuracy`/`characterization` split is stated with counts; characterization rows
  are excluded from the future accuracy %.
- Triage note names every wiki↔library conflict / ambiguity / suspected divergence as
  a follow-up (none fixed here).
- `git status` shows only changes to `cases_petrol_v7.csv` (oracle columns) + new files
  under `apps/wired/v7/` + `apps/wired/v7_tasks/`; no source/wiki edits.

## VERIFICATION GATE — T-V7-3
Complete in `v7_tasks/progress_notes/T-V7-3.md`: vocabulary-membership check; row
coverage; accuracy/characterization split counts; triage note path.

## CODE REVIEW — T-V7-3
Complete in `v7_tasks/progress_notes/T-V7-3.md`: every expectation traces to a
`wiki_ref` (no engine-derived, no library-over-wiki, no `ARCHIVE/`); no invented
families; no source/wiki edits; `graphify` not run.

## Commit (owner, explicit paths)
```bash
cd /agent_workspace
git add \
  apps/wired/v7/data/cases_petrol_v7.csv \
  apps/wired/v7/ORACLE_TRIAGE_<date>.md \
  apps/wired/v7_tasks/progress_notes/T-V7-3.md \
  apps/wired/v7_tasks/V7_PROGRESS.md
git commit -m "T-V7-3: fill v7 oracle from wiki/atlas domain truth"
```
