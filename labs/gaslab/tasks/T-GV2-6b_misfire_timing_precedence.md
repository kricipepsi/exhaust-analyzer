# T-GV2-6b — Misfire-vs-timing precedence (prune co-surviving misfire)

### Goal ###

When T-GV2-6a's idle→2500 RPM-differential has **confirmed** a cam-timing state
(`CAM_TIMING_RETARDED_MAP` / `_MAF` / `CAM_TIMING_ADVANCED` survived
`apply_differentiators`), stop a co-surviving generic misfire candidate from
out-ranking it. This closes `questions.md` Q7 ("cam/valve timing … versus generic
misfire, which currently outranks them — OUTRANKED").

### Premise (verified — read before authoring/altering) ###

- `CAM_TIMING_*` and the misfire signatures (`IGNITION_MISFIRE`, `LEAN_MISFIRE`,
  `RICH_MISFIRE`, `EGR_DILUTION_MISFIRE`, `INCOMPLETE_COMBUSTION`) are **both
  `SPECIFIC`** in the ontology — so `ranking.py` match-type ordering does **not**
  separate them; `_raw_score` (corroborating channels + specificity-inverse) can
  let misfire win. (Confirmed: `gas_lab_ontology.yaml` — misfire entries are not
  `signature_type: catch_all`.)
- T-GV2-6a only **retains** a timing candidate that passes the RPM check; it does
  **not** touch misfire candidates. So a case where both survive is unresolved
  after 6a — that is exactly this task's scope, and **only** that case.

### Steps ###

1. In `apply_differentiators` (`GASLab/gaslab/resolution.py`), **after** the
   timing RPM-differential block (6a) has run: if a `CAM_TIMING_*` candidate is
   still in `survivors` (RPM-confirmed) **and** a misfire-family candidate is
   also present, prune the misfire candidate(s) **only when the misfire's own
   defining magnitude is absent** — i.e. `reading.hc` is below the ignition-
   misfire HC floor. A true high-HC misfire (HC ≥ floor) is a real co-fault and
   is **not** pruned.
   - HC floor: `HC_IGNITION_MISFIRE_FLOOR` — `# vocab: GAS_VOCABULARY §10.1`.
   - Precedence rationale (RPM-diff is the SPECIFIC discriminator):
     `# wiki: docs/GASLab/wikiNEW/GAS_WIKI.md §8.9` (TEST_RPM_SEPARATION_MATRIX).
   - If §8.9 / §10.1 give the HC floor as a range rather than a single value, the
     coder pins the exact literal in scope confirmation — **do not invent it**.
2. Tests in `GASLab/tests/test_rule_engine.py`.

### Success criteria ###

- `test_timing_confirmed_prunes_low_hc_misfire` — RPM-confirmed `CAM_TIMING_*`
  + a low-HC misfire candidate ⇒ misfire pruned, timing emitted.
- `test_true_high_hc_misfire_survives_with_timing` — HC ≥ floor ⇒ misfire
  retained (no false prune).
- `test_no_timing_no_change` — without an RPM-confirmed timing candidate the
  misfire ranking is unchanged (no regression to non-timing cases).
- All existing GASLab tests (173+) pass.

### Files to touch ###

- `GASLab/gaslab/resolution.py` (MODIFY)
- `GASLab/tests/test_rule_engine.py` (MODIFY)

### Signal/noise consumer ###

The misfire-family vs cam_timing `ChemicalSignature` routing → COMLab
`chemical_state` / fault-atlas precedence (GASWIKI-08). **No new field, no new
enum.** The prune reads existing fields (`reading.hc`, the 6a-retained
survivors).

### Harness compatibility ###

- **No schema-surface change** ⇒ the harness `ModuleDescriptor` field set and box
  table are untouched; this task does not invalidate any harness fixture or
  descriptor. It only changes *which* label wins on co-survival.
- This is a **ranking/precedence** change, not a box-membership property — the
  single-point box generators (T-TH-1/T-TH-2) **cannot** validate it by
  construction. It must be covered by the **regression fixture** (T-TH-7 /
  T-TH-10/11), and its discriminator is **RPM-differential**, so harness
  validation also depends on the planned **dual-RPM descriptor extension**
  (harness pack). Until that lands, gaslab's own pytest is the gate.

### Out of scope ###

- 6a's timing-retention logic (do not re-implement; this task runs after it).
- lean separation (6c), mechanical_wear (T-GV2-7), sensor (T-GV2-10), abstain
  (6d). No `ranking.py` scoring-formula change — prune at the survivor level, not
  by re-weighting `_raw_score`. No new DNA field, no enum change.
