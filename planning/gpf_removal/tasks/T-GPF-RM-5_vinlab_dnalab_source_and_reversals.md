# T-GPF-RM-5 — VINLab + DNALab: remove has_particulate_filter at source; reverse GPF tasks

**Pack:** GPF Removal · **Labs:** VINLab, DNALab · **Blocked by:** T-GPF-RM-1, T-GPF-RM-3, T-GPF-RM-4 · **Status:** pending

## Scope (1 paragraph)

Remove `has_particulate_filter` at its **source** — VINLab decodes it from
`has_gdi` + `euro_norm`, DNALab carries it on `VehicleDNA`. This runs **last**:
every reader (DTCLab in RM-1, COMLab in RM-3, wired/semantic in RM-4) must be
gone first, or removing the field here breaks them mid-pipeline. Because this is
a VINLab change, it closes only when the **whole repo is green** (VINLab strict
whole-repo gate), not just VINLab's own tests. This task also finalises the two
GPF-reinforcing tasks: it confirms the `T-FX-DTCHEX-1` regex note (added in RM-2)
and amends the `T-TST-9` generative-harness spec so it no longer asserts GPF
cases.

## Signal/noise / consumer

Removal at source. After this task, repo-wide
`grep -rn "has_particulate_filter\|GPF_HISTORY\|gpf_combined" --include=*.py --include=*.yaml --include=*.json --include=*.md`
returns **zero** outside regenerated `graph/` and `graphify-out/` artefacts and
`ARCHIVE/`. GDI itself (`has_gdi`) **stays** — it is in scope (era B); only the
`has_particulate_filter` derivation that consumed it is removed.

## Files to change

VINLab:
- `vinlab/decoder.py:379-382` — delete the `has_particulate_filter=( has_gdi AND
  euro_norm … )` derivation **and** the `<WIKI> OBD_VOCABULARY.md §13.5` citation
  comment above it (that wiki section was removed in RM-4). Leave the `has_gdi`
  read intact for other consumers.
- `vinlab/models.py:157,269` — delete the `has_particulate_filter` field default
  and its round-trip assignment.
- `labs/vinlab/tests/test_models.py`, `test_vindna_from_json.py`,
  `test_contract_conformance.py` — drop GPF/field cases.
- Fixtures `labs/vinlab/tests/fixtures/vindna_pre_refactor/*.json` — remove the
  `has_particulate_filter` key from each (or re-derive the fixtures if generated).
- `labs/vinlab/docs/BUILD_DATA_SOURCES.md`, `labs/vinlab/update.md` — strip GPF
  references.

DNALab:
- `labs/dnalab/tests/test_vehicledna_roundtrip.py`, `tests/test_models.py` — these
  currently carry `has_particulate_filter`; remove those cases. **Grep first:** the
  symbol shows up in DNALab *tests* but not in a DNALab source model — confirm
  whether DNALab defines its own `VehicleDNA.emissions` field (remove it if so) or
  only round-trips the VINLab-shaped payload (then it is a test-data fix only). Do
  not assume a source field that isn't there.

Task reversals / ledger hygiene:
- `planning/test_rollout/tasks/T-FX-DTCHEX-1_*.md` — verify the RM-2 note is
  present (regex stays; GPF no longer its consumer). No code change to the regex.
- `planning/test_rollout/tasks/T-TST-9_dtclab_generative_harness.md:88,168` —
  amend the spec: drop `GPF_HISTORY=P244A/P2459` from the expected routing set and
  the hex-edge example, so the harness, when built, does not assert a removed tag.
  Update the `TEST_ROLLOUT_PROGRESS.md` notes column for T-TST-9 accordingly.

## Success criteria

- Repo-wide grep (excludes above) for the three GPF symbols returns zero.
- `has_gdi` still decoded and still has at least one live consumer (confirm by
  grep) — if RM-* left it orphaned, raise as an Unplanned follow-up, do not
  silently delete in this task.
- **Whole repo green:** `pytest -q` across all labs + wired + e2e, plus
  `ruff`/`pyright` clean. VINLab strict gate: this row flips to done only on a
  clean whole-repo run, per `T-FX-17` baseline rule.

## Inner loop (coder)

Per-lab first (`ruff`/`pyright`/`pytest -x -q` on vinlab, then dnalab), then the
**whole-repo** run as the closing gate.

## VERIFICATION GATE
_(coder fills — must include the whole-repo green run)_

## CODE REVIEW
_(coder fills)_
