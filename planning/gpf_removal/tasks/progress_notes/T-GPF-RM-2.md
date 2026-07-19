# T-GPF-RM-2 — Progress Note

## Plan

T-GPF-RM-2 removes COMLab's consumption of the `GPF_HISTORY` routing tag and its P-codes. DTCLab no longer emits the tag (RM-1 done), so COMLab's mirrored enum, discriminator mapping, and registry P-code matches are now dead code. **Both pack caveats are in play:** (1) the hex `DTC_REGEX` stays — RM-2 only strips GPF routing/fixtures, never narrows the regex; (2) `catalyst_flow_restriction` (ERR-CF-003) stays — strip only P244A/P2459 and GPF wording, keep P0420 and all three target_horizons.

## VERIFICATION GATE

- **ruff:** `ruff check labs/comlab` — All checks passed.
- **pyright:** `pyright labs/comlab` — 24 errors, all pre-existing (fault_atlas_router.py optional member access, descriptor.py missing harness import, test fixtures missing parameters, None→FaultAtlasKG type mismatches). Zero new errors from this task's edits.
- **pytest:** `pytest -x -q labs/comlab/tests` — 336 passed, 6 skipped (pre-existing generative/fuzz/lab_pipeline blocks), 1 deselected (pre-existing O2FailureMode wiki drift guard unrelated to GPF). Green.
- **JSON validation:** `global_fault_registry.json` and `catalyst_failure.json` both parse.
- **Zero-residual grep:**
  - `labs/comlab/comlab/` — 0 hits for `GPF_HISTORY|P244A|P2459`
  - `labs/comlab/docs/wiki/` — 0 hits for `GPF_HISTORY|P244A|P2459`
  - `labs/comlab/tests/` — 0 hits for `GPF_HISTORY|GPF|P244A|P2459`
- **catalyst_flow_restriction preserved:** ERR-CF-003 still present with fault_id, fault_name, all three target_horizons (LEGACY, ADAPTIVE, MODERN), p_code_match `["P0420"]` only, no GPF wording in ui_diagnostic_string or remediation string.

### Scope note

`has_particulate_filter` remains in `tests/e2e/test_error_codes.py:199` (`_valid_vin_dna_dict()`) because COMLab's VinDNA model still requires it — the field is defined in DNALab/VINLab and removed at the source in RM-5, with COMLab's field readers removed in RM-3. Removing it from the test fixture now would break Pydantic validation (field required). The P244A→P044A change in the hex-tail regex test is clean and preserves the regex contract.

## CODE REVIEW

**Contracted files changed (11 files):**

- `comlab/schemas/vocabulary.py` — removed `GPF_HISTORY` enum member (L462)
- `comlab/config/tag_discriminator.yaml` — removed `GPF_HISTORY:` family block (L109-112)
- `comlab/config/global_fault_registry.json` — stripped P244A/P2459 from ERR-CF-003 p_code_match; removed GPF wording from ui_diagnostic_string; rewrote remediation string (TWC catalyst case only)
- `comlab/config/kg/catalyst_failure.json` — stripped GPF from component_group, mechanical_failure_mode, and ui_remediation_steps (removed 1 step, reworded 2 steps; 6→5 steps)
- `docs/wiki/DTC_VOCABULARY.md` — removed GPF_HISTORY enum row, gating table row, prose cross-reference, fan-out sentence, field from DtcEmissionsView, example from confidence table, P244A/P2459 DTC table rows; updated 18→17 count
- `docs/wiki/OBD_VOCABULARY.md` — removed entire §13.5 GPF section (P244A/P2459 codes + gating note)
- `docs/COMLab_LLD.md` — removed `has_particulate_filter` from EmissionsConfiguration model, VinDNA projection model, and JSON schema properties
- `tests/e2e/test_error_codes.py` — changed `P244A`→`P044A` in hex-tail acceptance test (regex still tested, GPF code gone)
- `tests/unit/test_tag_discriminator.py` — updated `test_unmapped_tag_neutral` docstring (removed stale GPF_HISTORY reference, accurately describes the O2_HISTORY test)
- `tests/unit/test_vocabulary.py` — updated DTCRoutingTag drift-guard expected count 18→17
- `planning/test_rollout/tasks/T-FX-DTCHEX-1_comlab_dtc_regex_hex_widening.md` — added §9 annotation: GPF_HISTORY no longer downstream consumer; hex regex stays justified by ISO 15031-6 general requirement

**No adjacent refactor.** Every edit traces to GPF removal.

**Two caveats honoured:**
1. Hex `DTC_REGEX` (`^[BCPU][0-3][0-9A-F]{3}$`) untouched — not in any file this task touched. The regex test was updated to use P044A (non-GPF hex code) to preserve the contract.
2. `catalyst_flow_restriction` (ERR-CF-003) preserved — P0420 kept, all three target_horizons kept, P244A/P2459 and GPF wording removed.

**No symbol left half-removed.** Zero-residual grep confirmed across code, config, wiki, and tests.

## Commit block

```powershell
cd C:\Users\muto\claude\4DApp\4DLab\4DLabV2
git add `
  planning\gpf_removal\tasks\progress_notes\T-GPF-RM-2.md `
  labs\comlab\comlab\schemas\vocabulary.py `
  labs\comlab\comlab\config\tag_discriminator.yaml `
  labs\comlab\comlab\config\global_fault_registry.json `
  labs\comlab\comlab\config\kg\catalyst_failure.json `
  labs\comlab\docs\wiki\DTC_VOCABULARY.md `
  labs\comlab\docs\wiki\OBD_VOCABULARY.md `
  labs\comlab\docs\COMLab_LLD.md `
  labs\comlab\tests\e2e\test_error_codes.py `
  labs\comlab\tests\unit\test_tag_discriminator.py `
  labs\comlab\tests\unit\test_vocabulary.py `
  planning\test_rollout\tasks\T-FX-DTCHEX-1_comlab_dtc_regex_hex_widening.md
git commit -m "T-GPF-RM-2: drop GPF_HISTORY tag, discriminator, registry P-codes from COMLab"
```
