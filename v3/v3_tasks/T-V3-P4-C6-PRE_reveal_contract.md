### Goal ###
C6-pack PRE-AUTHOR DISCLOSURE (read-only). Instance the **frozen reveal contract**
(`V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.md` template — do NOT re-derive it) for
**C6 — sensor fault under-detection**, next in the pinned sequence (C2 ✓ → C3 ✓ → **C6** → C5 →
C4 → C9 → C8 → C1 → C7). Output the C6 worked instance: producer thresholds cited from
`cluster6.md`, consumers named, the 14-case split, the FT-8 neighbour union derived live, and —
new for this pack — the **C3-interaction disclosure** (C6 boosts the same SF rules C3's live state
prunes). **No engine/lab/registry/corpus edit; no producer/consumer wired; no data synthesized.**
### Success criteria ###
Produce `v3/reports/V3_C6_REVEAL_CONTRACT_2026-07-05.md` (+ `.json`) with:
1. **C6 producer extraction (cited):** from `cluster6.md` (§Question One/Three/Four Answers +
   §Candidate Signature Table — grep the section anchors, cite line numbers), the emit gates for
   OBDLab `SensorDynamicsState`: `O2_LAZY_OR_BIASED` (Mode $06 O2 response margin vs vehicle limits;
   rich↔lean / lean↔rich response times slower than OEM limit — pin the numeric bounds the research
   gives, e.g. the healthy-vs-fault transition-time bands), `MAF_UNDERREAD` (MAF actual-vs-calculated
   airflow sustained 10–15% low at BOTH idle and 2500), and `SENSOR_HEALTH_UNPROVEN_ABSTAIN`
   (static-only values → abstain, per acq-spec §C6.6). **Grounding-strength tag on every threshold**
   (the 849 ms / <150 ms O2-response figures vs vaguer "vehicle Mode $06 limits" differ in strength).
2. **Consumer mapping (named, no edit):** `sensor_fault.json` SF-005/SF-008 (dynamics) +
   SF-001/SF-002 (bias) and `no_fault.json` NF-001/NF-002 for the healthy-vs-under-detected split
   (acq-spec §C6.4). Name the exact evidence field each would read.
3. **C3-INTERACTION DISCLOSURE (new, mandatory):** the live shim now PRUNES SF-001/SF-002 on
   `CONTROL_REFERENCE_FAULT` (C3B); C6 will BOOST SF rules on `SensorDynamicsState`. Column
   populations are disjoint today (C3 cases vs C6 cases), but state the composition/precedence rule
   the C6B commit must implement for a future row carrying both column sets — surface it now, do not
   let the coder discover it mid-commit. Cite `integration_shim.py::_control_plausibility_state` and
   the `_score_rule` C3 branch by line.
4. **Per-case split reconciling to 14:** CASE-045, CASE-048, YAML-TC46 (DATA_GAP_ACQUISITION_GAP=3);
   CASE-014, EXT-229, EXT-230, YAML-CSV25, case_046, era1_006 (OUTRANKED_HARD=6); CSV-025, EXP-N020,
   PDF-4G-05, TC-046, era2_012 (TUNABLE_HELD=5 — the 4A-held cases whose honest fix is this signal).
   BUILDABLE_NOW vs SCORING_GATED per case; oracle-fault mix disclosed (which are truly sensor_fault
   vs no_fault vs lookalikes — this drives the SYNTH separability split).
5. **FT-8 neighbour union derived LIVE** from `sensor_fault.json` + `no_fault.json` `passes_cases`
   (both competition groups; never reuse C3's list); name dual target+neighbour cases. NF rules
   touch healthy cases — a no_fault regression is the costliest kind; call that out.
6. **Confounder disclosure:** which non-sensor faults mimic lazy-O2/MAF-underread signatures per
   cluster6.md (and the C4 overlap: C4's deferred discriminator consumes THESE columns — acq-spec
   §C4); cases the C6 signal cannot separate are stay-abstained candidates for C6-SYNTH.
7. **Baseline pinned:** `V3_YARDSTICK_2026-07-05-C3B` (csv `9f530695…`, oracle `3088a7c3…`), run
   `apps/wired/v7/runs/POST_T_V3_P4_C3B/results.json`. If anything commits first, STOP and re-pin.
8. Read-only: `py_compile`+`ruff`+`pyright` clean on the extractor; score unchanged
   (`top3_family` 228/294, `Hash lock: ok`).
### Context ###
- Research (READ-NARROW): `v3/research/research_answers/cluster6.md` — §Question One Answer (line
  ~110), §Question Three/Four Answers (~141/153), §Candidate Signature Table (~167). Note: no
  `cluster6_prepped.md` exists — if the tables are corrupted like raw cluster3 was, STOP and surface
  it (md-prep is architect-level), do not hand-repair thresholds.
- Column contract: `V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md §C6` (9 columns:
  `mode06_o2_response_margin_pct, o2_rich_to_lean_ms, o2_lean_to_rich_ms,
  maf_actual_calc_delta_pct_idle, maf_actual_calc_delta_pct_2500, maf_gps_idle, maf_gps_2500,
  calc_airflow_gps_idle, calc_airflow_gps_2500`) — flag up-front which subset is plausibly
  load-bearing (the C3A lesson: the dry-run's scenario ladder may let C6B commit fewer columns).
- Worked instances to mirror: `V3_C3_REVEAL_CONTRACT_2026-07-05.{md,json}` + extractor
  `v3/build_c3_contract.py` (adapt; shared template sections identical).
Load skills: wired-signal-pack.
### Consumer (signal/noise) ###
- **Consumer:** the owner (C6-SYNTH go/no-go + stay-abstained set) and `T-V3-P4-C6-SYNTH`/`C6A`/`C6B`
  (inherit bands, consumer map, interaction rule, FT-8 union, baseline pin). No engine field/state
  added here.
### Disclosure ###
Surface, don't hide: weakly-grounded thresholds; the C3-prune/C6-boost interaction; the C4 column
dependency (landing C6 unblocks half of C4B's ask); NF-rule regression exposure; oracle-fault
lookalikes → stay-abstained candidates; any corrupted research table. Tier essential-first
(headline split → threshold/interaction tables → per-case JSON).
### Deliverables ###
1. `v3/reports/V3_C6_REVEAL_CONTRACT_2026-07-05.md` — CREATE. C6 instance of the frozen template.
2. `v3/reports/V3_C6_REVEAL_CONTRACT_2026-07-05.json` — CREATE. Machine-readable map + case split.
3. `v3/build_c6_contract.py` — CREATE (adapt `build_c3_contract.py`; do not fork shared logic silently).
### Files to touch ###
- `v3/reports/V3_C6_REVEAL_CONTRACT_2026-07-05.md` (CREATE)
- `v3/reports/V3_C6_REVEAL_CONTRACT_2026-07-05.json` (CREATE)
- `v3/build_c6_contract.py` (CREATE)
### Out of scope ###
**No producer/consumer wired. No corpus column. No rule/weight/shim edit. No re-score, no yardstick
mint. No synthesized values** (C6-SYNTH). No template re-derivation. No abstain-dial change
(MARGIN=0.02). No md-prep of cluster6.md (surface corruption instead). Writes only under `v3/`.
Never `Vault/`. GRAPH GUARDRAIL: no `graphify`/frozen-graph rebuild. `run_suite.py` untouched. No secrets.
### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/build_c6_contract.py
/agent_workspace/.venv-wired/bin/python -m ruff check v3/build_c6_contract.py
/agent_workspace/.venv-wired/bin/python -m pyright v3/build_c6_contract.py
grep -cE 'SF-00[1258]|NF-00[12]|MAF_UNDERREAD|O2_LAZY|CONTROL_REFERENCE_FAULT|interaction|abstain' v3/reports/V3_C6_REVEAL_CONTRACT_2026-07-05.md
/agent_workspace/.venv-wired/bin/python apps/wired/fl_tasks/score_v3_yardstick.py score   # unchanged: top3_family 228/294, Hash lock: ok
git status --porcelain   # only new files under v3/
```
Gate: 14/14 attributed; FT-8 union derived live with derivation shown; every threshold
grounding-tagged; C3-interaction rule stated; baseline pin present; score unchanged.
### Progress hook ###
PROGRESS.md `T-V3-P4-C6-PRE`: Status=done, Files changed=3 (new under v3/), Verification="C6 reveal
contract instanced: SensorDynamicsState gates cited+tagged, SF/NF consumers named, C3-prune/C6-boost
interaction disclosed, 14-case split reconciled, FT-8 union live, baseline pinned POST_T_V3_P4_C3B;
read-only, score unchanged".
### Depends on ###
`T-V3-P4-C3B` done ✓ (new baseline minted). Runnable now. **Unblocks `T-V3-P4-C6-SYNTH`** →
`C6A` → `C6B` (forward-registered).
