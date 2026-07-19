# GW-ENH-3 — Vocab-path repoint + stale citation cleanup (housekeeping)

**Type:** code + comment cleanup (NOT a wiki-content task) — **STRICT inner loop applies**
**Scope:** petrol 1990–2010 unchanged; this is path/citation hygiene, no logic change
**Trigger:** the vault reorg of 2026-06-10 — `GAS_VOCABULARY.md` moved from `wiki/` to
`docs/`, and the single-file `GAS_WIKI.md` was archived. Two consequences left the
codebase inconsistent (found during the wiki-enhancement pack authoring).

> This is housekeeping, not a research candidate from the triage. It exists because
> the file moves broke a path the tests depend on and left stale citation strings.

---

## Why this is needed (two concrete problems)

**Problem A — the test suite is currently broken.** `tests/unit/test_validators.py`
reads the vocabulary from the **old** path `docs/wiki/GAS_VOCABULARY.md`, but that
folder is now **empty** (the 26 KB copy was removed in the reorg). The canonical
vocabulary now lives at `docs/GAS_VOCABULARY.md`. Until the test path is repointed,
the drift-guard test (the test that checks the engine's thresholds still match the
vocabulary) raises `FileNotFoundError`.

Exact reads to fix in `tests/unit/test_validators.py`:
- **line 36** — `Path(__file__).resolve().parent.parent.parent / "docs" / "wiki" / "GAS_VOCABULARY.md"`
- **line 376** — `vocab_path = repo_root / "docs" / "wiki" / "GAS_VOCABULARY.md"`

Both must become `… / "docs" / "GAS_VOCABULARY.md"` (drop the `"wiki"` segment).

**Problem B — 85 stale citation comments.** `gaslab/resolution.py` (76 lines) and
`gaslab/rule_engine.py` (9 lines) cite the **pre-migration** path
`docs/GASLab/wikiNEW/GAS_WIKI.md §X` / `wikiNEW/06b §…`. That path no longer exists
(the canonical wiki is the chunk set in `labs/gaslab/wiki/`, and the single file is
archived). Comments only — no behaviour — but they point readers at a dead location.

---

## Part A — repoint the vocab path (REQUIRED; fixes the red suite)

1. In `tests/unit/test_validators.py`, change the two path constructions (lines 36,
   376) from `"docs" / "wiki" / "GAS_VOCABULARY.md"` to `"docs" / "GAS_VOCABULARY.md"`.
2. **Grep-confirm no other reader.** `grep -rn 'docs.*wiki.*GAS_VOCAB\|"wiki".*GAS_VOCAB' tests/ gaslab/`
   — the path grep at authoring time found only `test_validators.py`; confirm
   `tests/unit/test_rule_engine.py` (flagged for containing both "docs" and "wiki")
   only **cites** `GAS_WIKI §…` in comments and does **not** open a vocab file. Fix
   any additional real read the same way.
3. **Remove the now-empty `docs/wiki/` directory** (housekeeping) so nothing is
   tempted to read it again. Skip if git tooling makes an empty-dir removal awkward —
   it is harmless empty.
4. Run the inner loop. The **drift-guard must pass against the canonical vocab**:
   `test_wiki_drift_thresholds_match_vocab` (line 283) and
   `test_dna_gate_count_matches_wiki` (line 359, expects ontology=6 / wiki=7 non-`none`
   §3.1 gates). If either fails, the canonical `docs/GAS_VOCABULARY.md` differs from
   the retired `docs/wiki/` copy in §10 thresholds or the §3.1 gate table — **stop and
   surface the diff to the owner**, do not edit the test's expected numbers to force
   green (that would mask a real vocabulary divergence).

## Part B — stale citation-comment sweep (cosmetic; same session OK)

Bulk-replace the dead `wikiNEW` citations in `gaslab/resolution.py` (76) and
`gaslab/rule_engine.py` (9) with the canonical **chunk-id + section** form the wiki
uses for itself. No code/logic/numeric-literal changes — comments only.

Mapping (section number → owning chunk):
- `docs/GASLab/wikiNEW/GAS_WIKI.md §2.8`  → `GASWIKI-02 §2.8` (`wiki/02_combustion_foundations.md`)
- `wikiNEW/06b §FAULT_CAM_TIMING_*`        → `GASWIKI-06B §…` (`wiki/06b_fault_atlas_valvetrain_egr_combustion.md`)
- `GAS_WIKI §8.9` (already chunk-agnostic) → keep, or normalise to `GASWIKI-08 §8.9`
- any other `wikiNEW/<n>` → `GASWIKI-<n>` (the chunk that owns that section)

Guard: confirm the replacement touched **only comment text** — every numeric literal
and predicate is byte-identical before/after (diff review). The §-numbers themselves
are unchanged; only the doc/path prefix changes.

> Part B is purely cosmetic. If context runs short, ship Part A alone (it un-breaks
> the suite) and leave Part B as a follow-up row — but Part A must not ship red.

---

## Success criteria

- `tests/unit/test_validators.py` reads `docs/GAS_VOCABULARY.md`; no test references
  `docs/wiki/…` for a file read.
- Full inner loop green: `ruff` clean, `pyright` clean, `pytest -x -q` — including the
  drift-guard and DNA-gate-count tests passing **against the canonical vocab**.
- (Part B, if done) zero `wikiNEW` occurrences remain in `gaslab/*.py`; a diff shows
  only comment-text changes — no logic or numeric-literal change.
- No `chemical_state` / `GasLabPayload` / threshold value changed anywhere.

## Files to touch

- `labs/gaslab/tests/unit/test_validators.py` (MODIFY — 2 path lines)
- `labs/gaslab/docs/wiki/` (REMOVE — now-empty dir; optional)
- `labs/gaslab/gaslab/resolution.py` (MODIFY — Part B comments only)
- `labs/gaslab/gaslab/rule_engine.py` (MODIFY — Part B comments only)

## Verification (STRICT — this is code, not docs)

- **Completed 2026-06-10.**
- Reproduced the original failure with `python -m pytest tests/unit/test_validators.py -x -q`: `FileNotFoundError` for `docs/wiki/GAS_VOCABULARY.md`.
- Repointed both validator reads to `docs/GAS_VOCABULARY.md`; targeted validator check now reports `8 passed`.
- Confirmed no `docs/wiki/GAS_VOCABULARY.md` reader remains in `tests/` or `gaslab/`, and `docs/wiki/` is absent.
- Converted `wikiNEW` citations in `gaslab/resolution.py` and `gaslab/rule_engine.py` to `GASWIKI-<chunk>` comment citations; grep confirms zero `wikiNEW` occurrences remain in `gaslab/*.py`.
- Strict loop:
  - `python -m ruff check .` — pass.
  - `python -m pyright` — pass (`0 errors, 0 warnings, 0 informations`; pyright also printed its version-update notice).
  - `$env:PYTHONPATH='C:\Users\muto\claude\4DApp\4DLab\4DLabV2\harness'; python -m pytest -x -q` — `211 passed, 2 skipped in 660.44s`.
- Diff review: only `test_validators.py` path construction changed; `resolution.py` / `rule_engine.py` changes are citation comments/docstrings only. No `chemical_state`, `GasLabPayload`, predicate, or threshold values changed.

- `ruff` → `pyright` → `pytest -x -q` all green; the previously-failing
  `test_validators` collection/read now passes.
- Drift-guard + DNA-gate-count assert green against `docs/GAS_VOCABULARY.md` (proves
  the canonical vocab is structurally what the engine expects — see Part A step 4
  stop-condition).
- `git diff` review confirms Part B changed comments only (no predicate/literal moved).

## Deliverables

1. `test_validators.py` vocab path repointed to `docs/GAS_VOCABULARY.md` (lines 36, 376).
2. Empty `docs/wiki/` removed (optional).
3. (Part B) `wikiNEW` comment citations in `resolution.py` / `rule_engine.py` converted
   to `GASWIKI-<chunk> §…` form.
