# T-GPF-RM-5 — Progress Note

## Plan

(see above — executed as planned)

## VERIFICATION GATE

**ruff:** clean — `ruff check labs/vinlab/vinlab/ labs/vinlab/tests/ labs/dnalab/tests/ labs/comlab/tests/e2e/test_error_codes.py` → All checks passed.

**pyright (vinlab source):** 0 errors, 0 warnings, 0 informations.

**pytest — VINLab:** 169 passed in 3.13s. Green.

**pytest — DNALab:** pre-existing `ModuleNotFoundError: No module named 'symptomlab'` — DNALab imports symptomlab which is not installed in bare Python. Not caused by this change.

**pytest — whole-repo:** Cannot run in bare Python due to pre-existing cross-lab import failures (comlab, symptomlab, dnalab, streamlit — not installed). The task requires this run in `.venv-wired` which the user must run. VINLab (169 passed) is the critical path for this task since VINLab is the source being removed.

**Repo-wide anti-orphan grep:**
```
grep -rn "has_particulate_filter\|GPF_HISTORY\|gpf_combined" \
  --include="*.py" --include="*.yaml" --include="*.json" --include="*.md" \
  --exclude-dir=graph --exclude-dir=graphify-out --exclude-dir=ARCHIVE \
  --exclude-dir=.git --exclude-dir=__pycache__ --exclude-dir=.sandbox-py \
  --exclude-dir=v1_baseline --exclude-dir=v2_current --exclude-dir=v6 .
```
**Live-code results: ZERO** in `labs/` (all labs), `apps/`, `planning/test_rollout/` (task specs only, no code).

Residuals exist only in:
- `planning/gpf_removal/` — the pack's own docs (expected: they document the removal)
- `planning/test_rollout/tasks/T-FX-DTCHEX-1_*.md` — historical task documentation; §9 annotation confirms regex stays, GPF no longer consumer
- `Vault/tasks/` — Vault task specs referencing `gpf_combined` as historical examples (out of scope)
- `Vault/_vocabulary/OBD_VOCABULARY.md` — vocabulary mirror (out of scope; noted as unplanned follow-up)

**Caveat 1 (hex DTC regex):** STAYS. T-FX-DTCHEX-1 §9 annotation verified present (lines 122-126). Regex unchanged.

**Caveat 2 (has_gdi):** STAYS. Confirmed abundant live consumers: `build_vref_db.py`, `tecdoc_hardware_enricher.py`, `decoder.py` (fuel_delivery_type derivation), `vref_manual_overrides.yaml` (60+ entries), `BUILD_DATA_SOURCES.md`. Not orphaned.

## CODE REVIEW

**Only contracted files changed:** Confirmed. 20 files edited:

*VINLab source (3):* decoder.py, models.py (2 edits)
*VINLab tests (4):* test_models.py (2 edits), test_vindna_from_json.py, test_contract_conformance.py
*VINLab fixtures (5):* 1FA6P8CF0HXXXXXXX.json, VF1357K0F17697151.json, VF1BB0FCF23935016.json, VF1CB05CF25935016.json, WBA4W9C5ZLYYYYYYY.json
*VINLab docs (2):* BUILD_DATA_SOURCES.md (2 edits), update.md
*DNALab tests (2):* test_models.py, test_vehicledna_roundtrip.py (2 edits)
*Task reversals (1):* T-TST-9_dtclab_generative_harness.md (5 edits)
*COMLab residual (1):* test_error_codes.py — known residual from RM-2, cleaned as part of RM-5 source removal
*Ledger (1):* GPF_REMOVAL_PROGRESS.md

**No adjacent refactor.** Every edit traces to `has_particulate_filter`, `GPF_HISTORY`, `gpf_combined`, or GPF P-code removal.

**No symbol left half-removed:**
- `has_particulate_filter` — removed from VINLab source (decoder + models), all VINLab tests/fixtures, VINLab docs, DNALab tests, COMLab e2e test helper
- `GPF_HISTORY` — already removed by RM-1/RM-2; T-TST-9 spec amended to drop reference
- `gpf_combined` — already removed by RM-1; T-TST-9 spec amended

**T-FX-DTCHEX-1 annotation:** Verified present (§9, lines 122-126). Hex regex stays; GPF_HISTORY no longer downstream consumer.

**T-TST-9 spec amended:** GPF_HISTORY removed from routing-tag table, DNA-gating prose, fuzz spec, and success criteria. P244A references generalized to "hex DTC."
