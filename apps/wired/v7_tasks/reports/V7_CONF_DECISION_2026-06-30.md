# V7_CONF_DECISION_2026-06-30 — `confidence_score` semantics + saturation (F-V7-CONF-SAT)

**Task:** T-V7-8 (READ-ONLY investigation, decision memo only) · **Author:** GLM · **Date:** 2026-06-30
**Question:** What is `confidence_score` the calibrated probability *of*, and against that
definition is the ≥0.95 saturation (273/294 `confidence` FAIL) an **engine** defect (A) or an
**oracle** mis-calibration (B)?
**Recommendation: Option B — re-pin the v7 oracle confidence bands to the live scorer's
per-family score distribution (named-fault rows only). Zero engine change.** See §5.

---

## 1. Where `winner_score` / `confidence_score` is computed, and its definition + range

The v7 suite runs the **v2 registry path by default** — `LabPipelineAggregator.__init__`
resolves `use_v2_registry` from `USE_V2_REGISTRY` env (default `"1"` → True)
(`labs/comlab/comlab/core/lab_pipeline_aggregator.py:120-121,129-133`), and
`FaultAtlasRouter.route()` returns early through the v2 branch
(`fault_atlas_router.py:1898-2081`) before the legacy assembly at `:2093-2245`. So the
pinned fact's "`confidence_score=winner_score` passthrough at ~L2204" describes the
**legacy/v1** assembly; the v7 run actually emits the score via the v2 shim. **Both paths
pass the raw rank score through unchanged**, so the A/B conclusion is identical for either;
this section cites both.

### 1a. v2 path (the one the v7 suite exercises) — `registry/integration_shim.py`

`RegistryV2Router._score_rule` (`integration_shim.py:519-574`) — the per-rule score:

```
score = rule.base_weight
      + 0.10 per satisfied non-GATING DEFINITIVE evidence (chemistry/obd/dtc)
      + 0.05 per satisfied non-GATING SUGGESTIVE evidence
clamped at min(rule.confidence_ceiling, 1.0)   # 1.0 if confidence_ceiling is None
```

- Constants: `_TIER_BONUS_DEFINITIVE`, `_TIER_BONUS_SUGGESTIVE`,
  `_CONFIDENCE_HARD_CAP = 1.0` (`integration_shim.py:140`, spec §Context step 2).
- GATING evidence is a precondition only — no score bonus (`:531-532,548`).
- Competition resolution: within each `competition_group` the highest clamped score wins;
  ties → `base_weight` desc → `rule_id` asc (`:700-733`). Cross-group top-fault = highest
  clamped score (`:674-697`).
- **Passthrough:** `_translate_to_output` sets
  `verdict["confidence_score"] = clamped_score` and alias `"confidence" = clamped_score`
  (`:785-803`). No calibration, no normalisation — the competition-winning clamped score
  *is* the emitted `confidence_score`.

**Range:** `[0.0, 1.0]` (schema-enforced, `schemas/response.py:101`). It is a **bounded
additive evidence-accumulation rank score** — `base_weight` (registry-tuned prior per rule)
plus fixed tier bonuses for each corroborating evidence row, clamped at a per-rule ceiling.
It is **not** a calibrated posterior probability, **not** a margin, **not** an unbounded
rank score. It ranks competing rules within a competition; the winner's clamped score is
reported verbatim.

### 1b. legacy/v1 path — `fault_atlas_router.py:execute_triage_loop` (Phase 5 score, `:1038-1070`)

```
score = row.confidence_scoring.base_weight
      + row.confidence_scoring.bonus_on_dtc_match   (if a confirmed DTC matches)
      clamped at _SCORE_CEILING = 1.0
      then INCOMPLETE_OXIDATION cap (0.90 / 0.75)
then additive/bounded evidence promotions (max(score, fixed_confidence)):
      bank-asymmetry 0.80, ECU-fuse 0.80, O2-offset 0.80, no-start 0.80, sensor 0.80,
      demotion cap 0.60, symptom-prior additive boost (capped at 1.0)
```
`winner_score = scored[0]` after sort; threshold-miss suppresses to no_fault if
`< MIN_CONFIDENCE_THRESHOLD (0.70)` (`:1686-1696`). Assembled as
`DiagnosticVerdict.confidence_score = winner_score` (`:2200-2205`). Same character: a
bounded additive evidence-accumulation rank score, raw-passthrough.

### Why it saturates (the 172×1.00 / 79×0.95 / 18×0.93 / 22×0.90 distribution)

v2 registry `base_weight` distribution across 73 rules: `0.80×20, 0.75×13, 0.85×10,
0.70×9, 0.65×5, 0.60×4, 0.82×3, 0.95×2, …`; `confidence_ceiling`: `None×28, 0.85×15,
0.80×11, 0.75×6, 0.90×3, 0.95×3, …`. A rule at `base_weight 0.80` with two corroborating
DEFINITIVE rows (`+0.20`) clamps to its ceiling (`1.0` if `None`, else `0.95/0.93/0.90`).
**Saturation is structural by design** — a high-prior rule with full evidence corroboration
is *intended* to reach its ceiling; the ceiling expresses "evidence fully corroborated",
not "100 % certain". (`SCHEMA_V2_SPEC.md` §3.1: "`base_weight` — starting confidence weight";
§3.2: "`confidence_ceiling` — max confidence when rule is solo in its competition group".)

---

## 2. Spec/wiki/LLD statement of `confidence_score` meaning + downstream thresholds

### Wiki — `labs/comlab/wiki/09_calibration_confidence.md` (authoritative, v2.0)

This is the **only** doc that defines intended semantics, and it is explicit that the
calibrated regime is **not yet built**:

> "Today `ConfidenceRating` reflects **evidence-chain completeness, not calibrated
> correctness** (AUDIT Q5). A 'HIGH_ASSURANCE' verdict does not mean the diagnosis is
> probably right — only that the inputs were present. The rework makes confidence a **real
> likelihood**."
>
> "Add a **post-hoc calibration layer** after the fusion stage that maps the fused score →
> a calibrated posterior, then to tiers re-defined as posterior / likelihood-ratio bands."
>
> "**Hard dependency:** calibration is **meaningless on noisy/synthetic labels**. It must
> be fit on the **Gate-Data measured-real eval subset** (`COMWIKI-12`). Until that subset
> exists, the tiers are **expert-set priors, flagged as such** in the output."

Target tier bands (post-calibration; literals are **expert priors until Gate-Data sets
them**):

| Tier | Meaning (post-calibration) | Provisional band |
|---|---|---|
| `HIGH_ASSURANCE` | calibrated posterior strongly favours the lead | posterior ≳ 0.80 |
| `DEGRADED_ASSURANCE` | lead favoured but within a plausible differential | 0.50–0.80 |
| `LOW_CERTAINTY` | no candidate dominates; differential is the product | < 0.50 |

So the wiki's *target* semantics for `confidence_score` = a **calibrated posterior
probability** (likelihood the lead fault is correct). It explicitly labels the current
numbers as **provisional expert priors** pending a Gate-Data calibration subset that does
not yet exist. The engine constants echo this — every confidence literal in
`fault_atlas_router.py` is tagged `# wiki: 09_calibration_confidence.md §CONCEPT_CONF_TIER`
("provisional high-assurance band").

### LLD — `labs/comlab/docs/COMLab_LLD.md`

The LLD defines the **shape** but not a calibrated-probability semantics:
- `DiagnosticVerdict.confidence_score: float = Field(ge=0.0, le=1.0)  # wiki:
  DNALab_TO_COMLab_FLOW §4` (`COMLab_LLD.md:446`) — schema constraint only; cited to a *flow*
  doc, not a calibration spec.
- `ConfidenceLit = Literal["HIGH_ASSURANCE", "DEGRADED_ASSURANCE", "LOW_CERTAINTY"]`
  (`:402,426`) — the tier-label enum; numeric band mapping is in code, not the LLD.
- `MIN_CONFIDENCE_THRESHOLD = 0.70  # lld: §6.4` (`fault_atlas_router.py:77`) — the
  threshold-miss gate.

The LLD does **not** state `confidence_score` is a calibrated posterior.

### Downstream thresholds / consumers that actually read the numeric value

| Consumer | Where | Behaviour | Path |
|---|---|---|---|
| **Threshold-miss gate** | `fault_atlas_router.py:1686` | `winner_score < 0.70` → suppress verdict to `no_fault` | legacy/v1 only |
| **Tier-label step** | `fault_atlas_router.py:2234-2238`; `integration_shim.py:798` | `>= 0.70` → `HIGH_ASSURANCE`, else `DEGRADED_ASSURANCE`; abort → `LOW_CERTAINTY` | both |
| **Demotion cap** | `fault_atlas_router.py:1485,1534,1548` | `min(score, _EVIDENCE_DEMOTION_CAP=0.60)` to route a rule away | legacy/v1 only |
| `DifferentialSiblingOut.confidence_score` | `schemas/response.py:87` | UI badge only; `None` for editor-curated, runtime score for runner-ups | both |

**Key finding:** no consumer reads `confidence_score` as a continuous calibrated
probability. The only hard numeric gate is a single **0.70 step** into a 2-tier label
(3-tier with `LOW_CERTAINTY` reserved for aborts). There is no threshold keyed to the
wiki's *target* bands (≳0.80 / 0.50–0.80 / <0.50); the engine's cut is 0.70, which already
diverges from the wiki's target HIGH_ASSURANCE band of ≳0.80.

---

## 3. Oracle-band provenance (where T-V7-3 sourced the bands)

The v7 oracle `expected_confidence_min/max` band distribution (294 accuracy rows):

| Band | Count | Band | Count | Band | Count |
|---|---|---|---|---|---|
| `[0.65, 0.85]` | 53 | `[0.73, 0.93]` | 27 | `[0.80, 0.99]` | 16 |
| `[0.70, 0.90]` | 33 | `[0.75, 0.95]` | 18 | `[0.67, 0.87]` | 14 |
| `[0.85, 0.99]` | 13 | `[0.55, 0.75]` | 13 | `[0.6, 0.8]` | 10 |
| `[0.0, 0.35]` | 17 | … | | | |

Provenance:
- T-V7-3 progress note (`progress_notes/T-V7-3.md`) states only "values derived from the
  lab wikis and current fault atlas, corroborated by the original library conclusions."
- The `ORACLE_TRIAGE_2026-06-30.md` note documents **family/code conflicts only** — it
  records **no confidence-band provenance** and no script that emitted the bands.
- No T-V7-3 artifact pins a band to the live scorer's score distribution; the bands cluster
  around the wiki's **target** HIGH_ASSURANCE posterior band (≳0.80) with a ~±0.10 window.

**Assessment:** the oracle bands were pinned to the wiki's *target* **posterior** bands
(mid-range, centred ~0.80) as if the engine already emitted calibrated posteriors. The wiki
explicitly says it does not (calibration layer unbuilt, numbers are "expert-set priors,
flagged as such"). So **band B's defensibility is weak**: the bands assume a calibration
semantics the engine does not yet provide, against a scorer whose saturation is the
designed behaviour of a bounded rank score. The bands are not wrong as *target* posterior
bands; they are wrong as *oracle expectations against the live scorer*.

---

## 4. Decision — A (engine recalibrate) vs B (oracle reband)

| | **A — engine over-states** | **B — oracle bands wrong** |
|---|---|---|
| Premise | `winner_score` is a raw rank score; passing it through as `confidence_score` is wrong — recalibrate/normalise to a posterior. | The live scorer's high confidence is the intended *current* semantics; the oracle bands were pinned to a stale/target calibration. |
| Engine change | Yes — add the post-hoc calibration layer the wiki describes (Platt/temperature), or a normaliser. | **None.** |
| Blast radius | **Every verdict's `confidence_score` changes** + the 0.70 threshold-miss gate + the 0.70 tier-label step + any future consumer keyed on the value. | Zero — oracle-only edit, scorer untouched. |
| Data dependency | Wiki: calibration is **"meaningless on noisy/synthetic labels"**, must be fit on the **Gate-Data measured-real eval subset** (`COMWIKI-12`) which **does not yet exist**. | None — re-pin to the live scorer's *observed* per-family distribution (run `20260630_163900`). |
| Wiki alignment | The wiki's *end-state* is A (calibrated posterior) — but gated on a subset that doesn't exist. Demanding A now is demanding unbuilt, data-gated work. | The wiki's *interim* prescription: current numbers are **"expert-set priors, flagged as such"** until Gate-Data. Rebanding the oracle to the live scorer is exactly the interim regime. |
| Accuracy % fix | Indirect (depends on a calibrated mapping the data can't yet support). | **Direct** — re-pinning bands to the scorer's per-family distribution moves the 273/294 FAIL toward PASS without pretending the score is a probability. |

### Why B, not A

1. **The engine is behaving as the wiki says it currently behaves.** The wiki states today's
   `confidence_score` is evidence-completeness, not calibrated correctness, and that the
   calibration layer is an *unbuilt rework* (B.Q1) explicitly gated on a Gate-Data subset
   that does not exist. Flagging the engine as "over-stating" (A) would demand the unbuilt
   calibration layer **now**, with no data to fit it on — the wiki calls that
   "meaningless."
2. **The saturation is structural, not a bug.** A bounded additive rank score with
   per-rule ceilings is *designed* to saturate when a high-`base_weight` rule's evidence is
   fully corroborated. The ceiling expresses "evidence complete", not "100 % certain."
   Recalibrating it to a posterior (A) changes the meaning of every rule's `base_weight`
   and `confidence_ceiling` — a registry-wide semantics shift, not a fix.
3. **The blast radius of A is large and consumer-bearing; B is consumer-zero.** A touches
   the 0.70 threshold-miss gate + the tier-label step on every verdict; B edits only the
   oracle CSV. The wired-code-review "named consumer" rule favours the change with no
   consumer impact.
4. **B is the wiki's own interim prescription.** "Expert-set priors, flagged as such"
   describes re-pinning the oracle to the live scorer's provisional-prior distribution
   exactly. A is the *later* fix, gated on Gate-Data — out of scope for a read-only v7 task.

### Framing — B now, A later (do not conflate)

B treats the **symptom** (oracle expectations mismatched to the live scorer's semantics),
which is the correct *v7-suite* fix. B does **not** close the wiki's calibration gap —
that remains the real architectural fix (A), to be authored separately once the Gate-Data
measured-real eval subset exists (`COMWIKI-12`). The memo therefore recommends **B for the
F-V7-CONF-SAT fix task** and **forward-registers A as a deferred follow-up** (see §6), not
as the v7 fix.

---

## 5. Recommendation (single option, with affected files + symbols + consumer impact)

**Option B — re-pin the v7 oracle confidence bands to the live scorer's per-family score
distribution, named-fault rows only.** Zero engine change.

**Affected files + symbols (the eventual fix task — NOT this read-only memo):**
- `apps/wired/v7/data/cases_petrol_v7.csv` — re-derive `expected_confidence_min` /
  `expected_confidence_max` per row from the observed `confidence_score` distribution in
  run `20260630_163900`, **grouped by `expected_fault_family`** (the scorer's score
  distribution is per-family because `base_weight`/`confidence_ceiling` are per-rule and
  cluster by family).
- Keep a per-family band window (e.g. observed-family-min ± ε) rather than a single global
  band — the scorer saturates at family-specific ceilings.
- **Keep `ERR-ABORT-*` abort rows and `OPTIMAL_HEALTH` / `no_fault` rows on their existing
  bands** (`[0.0, 0.35]`, etc.) — the same discipline as the T-V7-7 code-namespace memo:
  a blanket reband must not corrupt abort/no-fault rows whose confidence is `0.0` by
  design (`lab_pipeline_aggregator.py:286`).
- Re-derivation script + provenance note: record the band source explicitly (the gap
  T-V7-3 left open — §3).

**Consumer / threshold impact:** **None.** The scorer, the 0.70 threshold-miss gate, the
0.70 tier-label step, and `DifferentialSiblingOut.confidence_score` are all untouched.
Rebanding the oracle changes only what the v7 scorer counts as a `confidence`-dim PASS/FAIL.

**Engine symbols that define the live distribution (cite, do not edit):**
- v2: `registry/integration_shim.py::_score_rule` (`:519-574`),
  `_translate_to_output` (`:785-803`), `_CONFIDENCE_HARD_CAP` (`:140`).
- v1/legacy (for completeness): `fault_atlas_router.py:execute_triage_loop` Phase-5 score
  (`:1038-1110`), `_SCORE_CEILING`/`_EVIDENCE_PROMOTION_CONFIDENCE`/`_EVIDENCE_DEMOTION_CAP`
  (`:80-82`), `MIN_CONFIDENCE_THRESHOLD` (`:77`).

---

## 6. Follow-up (forward-registered, NOT executed here)

| ID | Item | Why deferred |
|---|---|---|
| `F-V7-CONF-CALIB` (new) | Engine-side post-hoc calibration layer (wiki `COMWIKI-09` B.Q1): Platt/temperature map of the fused score → calibrated posterior; re-define tiers as posterior bands. | This is **Option A** — the wiki's real fix. Gated on the **Gate-Data measured-real eval subset** (`COMWIKI-12`) which does not yet exist; calibration on synthetic labels is "meaningless" per the wiki. Large blast radius (every verdict + 0.70 gate + tier label). Author only after Gate-Data lands. |

`F-V7-CONF-SAT` itself is resolved *as a v7-suite accuracy blocker* by the Option B reband
(the eventual fix task, gated on owner sign-off of this memo). The underlying calibration
gap is split out as `F-V7-CONF-CALIB` so the v7 suite is not blocked on an unbuilt,
data-gated architectural layer.

---

## 7. Verification of this memo (READ-ONLY)

- No source file under `labs/`, `apps/wired/wired/`, `apps/wired/v7/`, or `registry/` was
  modified. (Memo only — a new report file under `apps/wired/v7_tasks/reports/`.)
- No `graphify`; no `Vault/` edit; no suite re-run; no oracle CSV edit.
- All citations are to files read in this session (file:line) or to the wiki/LLD sections
  named inline.
