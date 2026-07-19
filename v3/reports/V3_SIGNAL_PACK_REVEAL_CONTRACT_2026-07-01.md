# V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01

**Task:** `T-V3-P4-C2-PRE`  **Mode:** DISCLOSE only (read-only pre-author)
**Writes engine/lab/registry/corpus code:** no  **Moves score / mints yardstick:** no
**Machine-readable twin:** `v3/reports/V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.json`
(regenerate with `/agent_workspace/.venv-wired/bin/python v3/build_reveal_contract.py`).

This document freezes the **reveal contract** every Phase-4 signal-pack task
(`T-V3-P4-C*A` dry-run + `T-V3-P4-C*B` commit) must inherit, and works the **C2**
(rich_mixture vs catalyst_failure) instance as the template. It builds nothing and
scores nothing; it fixes *how* a pack discloses so no later pack re-decides — or
blurs — what to surface.

---

## 0. The confusion this resolves (stated plainly)

`v3/research/research_answers/` contains discriminating **logic** — quantitative
thresholds and decision trees — **not** per-case measured sensor values. So a
"signal pack" is two separable things, and conflating them is dishonest:

1. **BUILDABLE-NOW-FROM-RESEARCH** — the producer-state emit rule, the consumer
   rule wiring, and the numeric thresholds are fully specified by the cluster
   answer. They can be authored and **unit-tested on synthetic vectors now**, with
   no owner data.
2. **SCORING-GATED-ON-OWNER-DATA** — a `top3_family` delta cannot be shown until
   the owner supplies the residual cases' real column values. Those columns are
   absent from the corpus *by construction* — that absence is exactly why the
   cases are residual. **No synthetic value may stand in.**

A pack that reports "threshold implemented" as "cases banked" crosses this line.
This contract exists to force the separation, permanently, for every cluster.

---

## 1. The reveal contract (cluster-agnostic template)

Every signal-pack task MUST surface these five sections, each defined once here:

| Section | Definition |
| --- | --- |
| **BUILDABLE_NOW** | Producer/consumer logic + thresholds derivable from the cluster research answer; provable by unit tests on synthetic vectors, with no owner data. |
| **SCORING_GATED** | The per-case owner columns still required and which residual `case_id`s each unlocks; stays abstained until the owner supplies real measured values (no synthetic stand-in). |
| **CODE_LANDED != SCORE_MOVED** | Explicit separation of "producer/consumer logic shipped" from "`top3_family` delta." Landing code proves the discriminator is wired; it does NOT move the score until gated data arrives. Never report the first as the second. |
| **REGRESSION / FT-8** | The neighbour set the consumer edit touches (rules in the same family file + shared `competition_group` + their `passes_cases`), plus the no-regressed-family audit run on the full corpus at commit time. |
| **ABSTAIN_FALLBACK** | Cases whose discriminating signal the owner cannot supply stay abstained (MARGIN=0.02 dial), never guessed from the idle snapshot. |

**How a pack pair uses the template:** the **`C*A` dry-run** fills BUILDABLE_NOW
(the logic it simulates), SCORING_GATED (the owner columns + case_ids), the
CODE_LANDED!=SCORE_MOVED disclaimer (it moves no live score — it *predicts*), the
FT-8 neighbour list it simulates for regressions, and ABSTAIN_FALLBACK (cases with
no supplied value). The **`C*B` commit** re-uses the same five headings but now
BUILDABLE_NOW is *landed* code, SCORING_GATED becomes the *measured* delta, and
FT-8 becomes the *actual* full-corpus no-regressed-family audit (mint a new
yardstick because the corpus changed; `run_suite.py` stays frozen).

---

## 2. C2 producer extraction (cited to `cluster2.md`)

The C2 producer is two states — **GASLab `CatalystConversionState`** (chemistry
conversion) and **OBDLab `CatalystMonitorState`** (Mode $06 / OSC monitors). The
emit thresholds, transcribed read-only from the research answer:

| Signal | Maneuver | Threshold | Emit verdict | Producer state | Cite (`cluster2.md`) |
| --- | --- | --- | --- | --- | --- |
| Total Fuel Trim (STFT+LTFT) | Curb idle, 60 s, 100 pts | **`<= -10%`** | `TRUE_RICH` (rich fueling active) | GASLab CatalystConversionState / rich producer | Protocol step 4 + Quantitative Signatures (Fuel Trim ±10% Normal) |
| Mode $06 O2 index ratio | Steady-state downstream O2 | **`<= 0.20`** | catalyst **PASS**; high ratio → `LOW_OSC_OR_HIGH_INDEX` | OBDLab CatalystMonitorState | Quantitative Signatures (Index Ratio ≤ 0.20 Pass) |
| OSC lag `Δt_osc` | Fuel step-change (lean +6% 4.0 s → rich −10% 3.0 s), transition at 0.45 V | **`Δt_osc < 0.5 s`** | catalyst **FAIL** (low OSC / minimal delay) | OBDLab CatalystMonitorState | Quantitative Signatures (OSC/Lag < 0.5 s Fail) + Protocol step 5 |
| Decel 5-gas sweep CO | Decel 2500 rpm → curb idle, continuous tailpipe CO | **`CO > 0.8%`** | catalyst **FAIL** (lazy/low conversion at idle) | GASLab CatalystConversionState | Quantitative Signatures (5-Gas Sweep CO > 0.8% Fail) + Protocol step 6 |
| **Pre-gate:** misfire (MID $A2/$A7) or pending heater (P0135) codes | Query DTCs before any catalyst read | present → **INVALID** | `ABSTAIN` / repair-first | pre-gate on both producers | Diagnostic Acquisition Protocol step 1 (Architectural Pre-Gate) |

**Producer emit summary (what C2A simulates, C2B commits):** rich producer emits
`TRUE_RICH` when negative trims are sustained (`<= -10%`); catalyst producer emits
`LOW_OSC_OR_HIGH_INDEX` when the Mode $06 margin/index fails (`index_ratio > 0.20`,
`Δt_osc < 0.5 s`, or decel `CO > 0.8%`) **without** rich trims. The pre-gate voids
the read when misfire/heater codes are present.

> **Producer-tuning risk flagged:** the index-ratio pass band (`<= 0.20`) and the
> catalyst-bed / coolant preconditioning windows in `cluster2.md` Protocol step 3
> are stated as vehicle-representative constants, but the research itself notes the
> index band "varies by vehicle" and warns Mode $06 may hold pre-populated defaults
> right after a Mode $04 clear. Treat `0.20` and the OSC/CO cut-points as **producer
> tuning parameters to confirm against real values in C2A**, not firm universal
> constants. The fuel-trim `<= -10%` cut is the most portable (it mirrors the live
> `rich_mixture` rules' `longft1 <= -10`).

---

## 3. C2 consumer mapping (named; no edit)

| Family file | Rules | Field each reads today | What the C2 state would supply |
| --- | --- | --- | --- |
| `rich_mixture.json` | **RM-001 / RM-003 / RM-004** | `obd_evidence` `longft1` (`<= -10/-5/-15`), `shrtft1`; `chemistry_evidence` `RICH_MIXTURE` | The `TRUE_RICH` producer state confirms/gates the negative-trim rules with a *measured* multi-point trim, instead of the single idle-chemistry inference. |
| `catalyst_failure.json` | **CF-001 / CF-002 / CF-006 / CF-007** | `chemistry_evidence` `CATALYST_OVERWHELMED` / `NORMAL_OPERATION`; `obd_evidence` `nox`/`co2`/`hc`/`obd_lambda` | The `LOW_OSC_OR_HIGH_INDEX` producer state supplies the direct catalyst-health discriminator (Mode $06 / OSC) that CF-002's "masking" and CF-006's "perception-gap" rules currently infer from tailpipe chemistry alone. |

This is the mapping the **commit** (`C2B`) will make. Nothing is edited here.

---

## 4. C2 per-case split — BUILDABLE_NOW vs SCORING_GATED (reconcile to 22)

**BUILDABLE_NOW-reachable by logic alone: 0** (expected — say so). Every C2 case
is residual precisely because its discriminating column (fuel trims + Mode $06
catalyst) is absent from the corpus; logic without values cannot move it.

**SCORING_GATED: 22 / 22**, split by residual bucket:

- **OUTRANKED_HARD = 11:** CASE-015, CSV-100, CSV-121, CSV-122, EXP-N017, EXT-232,
  EXT-233, PDF-HI-006, case_004, era1_017, era2_015.
- **PRODUCER_GAP_SIGNAL_REQUIRED = 11:** CASE-023, CASE-029, CASE-040, EXT-217,
  PDF-HI-001, RULE-CO-1, YAML-PDF_HI_001, case_002, case_015, case_017, era2_019.

Every one requires the columns `stft_idle_pct, ltft_idle_pct, stft_2500_pct,
ltft_2500_pct, mode06_catalyst_margin_pct, catalyst_index_ratio` (plus optional
`pre_post_cat_hc_delta_ppm, pre_post_cat_co_delta_pct`). **11 + 11 = 22.** ✔

**CODE_LANDED != SCORE_MOVED, stated for C2:** the producer emit rule and consumer
wiring above are BUILDABLE_NOW and unit-testable on synthetic trim/Mode-$06 vectors
— that is *code landed*. Any `top3_family` delta on these 22 (*score moved*) is
**unobservable until the owner supplies real values**. A pack report must never
present the first as the second.

---

## 5. REGRESSION / FT-8 neighbour set (derived live from the two rule files)

A C2 consumer edit touches the `rich_mixture` and `catalyst_failure` family files
— both `competition_group`s. The commit must re-audit every case those rules
currently pass for a regressed family. Union of `passes_cases` across all 4 RM +
7 CF rules = **33 cases**:

```
CASE-013, CASE-015, CASE-016, CASE-023, CASE-026, CASE-031, CSV-018, CSV-121,
CSV-122, EXP-N003, EXP-N008, EXP-N012, EXP-N013, EXT-203, EXT-207, EXT-208,
EXT-213, EXT-217, EXT-227, EXT-232, EXT-233, PDF-4G-01, PDF-4G-03, PDF-HI-001,
PDF-HI-006, REAL-005, RULE-CO-1, YAML-PDF_4G_01, YAML-PDF_HI_006, case_010,
case_024, case_030, case_034
```

**Shared-neighbour caveat (named now):** several of these are already-passing
non-C2 cases inside the same competition groups (e.g. `CSV-018`, `EXP-N003`,
`EXT-203`, `EXT-227` under RM-001; `EXT-207/208/213`, `CASE-013`, `EXP-N012` under
CF-003; `PDF-4G-01`, `case_010/034`, `REAL-005` under CF-001). A C2 gate that
tightens or re-weights RM/CF rules could regress these — so FT-8 in `C2A`/`C2B`
must run the **full corpus** and show **no regressed family**, not just re-check
the 22 targets. Note `PDF-HI-006`, `CASE-023`, `EXT-217`, `RULE-CO-1`, `PDF-HI-001`
appear in **both** the C2 target set and the neighbour set — they are targets *and*
regression-sensitive.

---

## 6. ABSTAIN_FALLBACK (C2)

If Mode $06 catalyst data and fuel trims are absent for a case, it **stays
abstained** at the current dial (MARGIN=0.02); a single downstream tailpipe
snapshot is not a catalyst-vs-rich discriminator. Cases the owner cannot measure
are never guessed.

---

## 7. Owner next-task fork (surfaced, NOT decided)

The owner now chooses how the *next* task proceeds. Both are legitimate; the
contract above holds either way.

| Option | Does | Cost / risk | Benefit |
| --- | --- | --- | --- |
| **(i) Build C2 producer/consumer code now** (scoring deferred) | Author + unit-test the C2 producer emit rule and consumer wiring on synthetic vectors; land BUILDABLE_NOW logic; leave all 22 cases abstained until data arrives. | Engine/registry churn now that moves **no score yet**; the hand-set thresholds (`0.20`, OSC/CO cuts) may drift from the eventual real-data calibration. | Commit path pre-validated; when C2 data lands only the scoring + FT-8 step remains. |
| **(ii) Hold all pack code until C2 data lands** | Write no producer/consumer code until the owner supplies the 22 cases' trim + Mode $06 values; then run `C2A` dry-run → `C2B` commit. | No forward progress on C2 until the owner-data wall clears. | Thresholds calibrated against real values, not research defaults; zero speculative code. |

**Decision: OWNER DECIDES — not chosen here.** `T-V3-P4-C2A` remains blocked on
owner C2 data regardless; this fork only decides whether *logic authoring* begins
before that data or not.

---

## Provenance / guardrails

- Read-only: no corpus column added, no producer/consumer wired, no rule/weight
  edit, no re-score, no yardstick mint, no synthesized values, no abstain-dial
  change (MARGIN=0.02). Writes only under `v3/`. `Vault/` untouched. No
  `graphify`/frozen-graph rebuild. `run_suite.py` untouched. No secrets.
- Sources: `v3/research/research_answers/cluster2.md`;
  `v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.{md,json}` §C2;
  `labs/comlab/registry/rules/rich_mixture.json`, `catalyst_failure.json` (query
  only); governs `v3/v3_tasks/T-V3-P4-C2A_c2_signal_dryrun.md` (+ forthcoming
  `C2B`) and every later cluster pair.
