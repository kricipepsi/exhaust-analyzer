---
node_type: task
task_id: T-DTC-COMMENT-FIX
status: pending
pack: VAULT
lab: dtclab
mode: coder lane
blocked_by: []
consumers:
- graph/v2_code — AST code graph (module docstrings/labels, via T-DTC-GRAPH-AST)
- T-DTC-CODEPREP — AST-legibility audit (would otherwise flag the stale count)
tags:
- task
- vault
- dtclab
---

# T-DTC-COMMENT-FIX — Fix the two stale enum-count docstrings (18 vs 17/19)

**Status:** `pending` · **Pack:** VAULT (DTCLab) · **Mode:** coder lane (inner loop after the edit)
**Origin:** surfaced by the 2026-06-11 docs reconciliation (`T-DTC-DOCS-V2`) · **Blocked by:** —
**Consumer (signal/noise):** **Adds no schema field, changes no behaviour.** The fix corrects two
module docstrings whose stated enum count disagrees with the shipped `DTCRoutingTag` (18 members). The
consumer is **graph legibility**: the code graph built in `T-DTC-GRAPH-AST` reads module docstrings and
labels; a docstring asserting a wrong count is a legibility defect that `T-DTC-CODEPREP` would otherwise
flag. Fixing it here keeps the CODEPREP audit clean. No logic, no contract, no test expectation changes.

### The defect (verified 2026-06-11) ###

`DTCRoutingTag` ships **18** members (`vocabulary.py`), but two docstrings give the wrong count:

```
labs/dtclab/dtclab/schemas/vocabulary.py
    class DTCRoutingTag docstring: "Source: DTC_VOCABULARY.md §4 (17-value canonical form)."
        → 17 is stale. Actual = 18 (COOLANT_SYSTEM_MALFUNCTION + CYLINDER_FLUID_MISFIRE added).

labs/dtclab/dtclab/family_map.py
    module docstring: "Maps each DTCRoutingTag (19-value surface, DTC_VOCABULARY.md §4) to a canonical…"
        → 19 is stale. Actual = 18.
```

Ground truth (already reconciled in docs): `DTC_VOCABULARY.md §4` and all six design docs now state
**18**. The wiki `00_INDEX` / chunk prose and `DTC_VOCABULARY.md §4.2` also say "All 18 DTCRoutingTag
values…". Only these two code docstrings lag.

### Goal ###

Bring both docstrings to the correct **18-value** wording, matching `DTC_VOCABULARY.md §4` and the
shipped enum. Comment/docstring text only — no code, no enum member, no behaviour.

### Exact edits ###

1. `schemas/vocabulary.py` — `DTCRoutingTag` docstring: `§4 (17-value canonical form)` →
   `§4 (18-value canonical form)`.
2. `family_map.py` — module docstring: `(19-value surface, DTC_VOCABULARY.md §4)` →
   `(18-value surface, DTC_VOCABULARY.md §4)`.

Spot-check the rest of each file for any other `17-value`/`19-value` reference to the routing enum and
correct it the same way (report any found in the progress note).

### Success criteria ###

1. Both docstrings read `18-value` and agree with `DTC_VOCABULARY.md §4`.
2. Inner loop green with **no behaviour change**: `ruff check .` clean, `pyright` clean,
   `pytest -x -q` green (no test asserts the docstring text, so counts are unchanged).
3. `grep -rn '17-value\|19-value' dtclab/` returns nothing for the routing enum.
4. The enum itself is **untouched** (still 18 members); `git diff` shows only comment lines changed.

### Out of scope ###

- The GPF out-of-era reconciliation (`wiki/11_proposals_register.md §11.4`) — a behavioural decision,
  not a comment fix (START_HERE §5).
- Any enum member add/remove, any logic, any test edit — this is a docstring-only change.

### Files to touch ###

- `labs/dtclab/dtclab/schemas/vocabulary.py` (one docstring line).
- `labs/dtclab/dtclab/family_map.py` (one docstring line).

### Verification ###

```bash
cd <repo>/labs/dtclab
grep -rn '17-value\|19-value' dtclab/ && echo "FAIL stale count remains" || echo "OK no stale count"
ruff check . && pyright && pytest -x -q
git diff --stat dtclab/schemas/vocabulary.py dtclab/family_map.py   # comment lines only
```

### Progress hook ###

`Vault/tasks/progress_notes/T-DTC-COMMENT-FIX.md` opens with the confirmed `## Plan` (the two exact
edits); the run session fills `VERIFICATION GATE` (both docstrings = 18, grep clean, inner loop green,
enum untouched) + `CODE REVIEW` (diff is comment-only, no behaviour change). Ledger row → `done` only
when both blocks are clean.
