# V3 Abstain Checkpoint Report — 2026-07-01
This report discloses the impact of the family-aware margin definition (T-V3-3C) and sweeps thresholds to support the next-decision map.

## Tier 1 — Headline
* **Coverage**: `0.10 -> 0.37` (109/294 covered, 185 abstained)
* **Top-3 family accuracy**: `176/294 (59.86%)` **unchanged** (abstain does not change underlying engine predictions)
* **Recovered wins**: `63` unnecessary single-verdict abstentions recovered (T-V3-3B's 115 single-verdict hidden wins reduced to 52)
* **Honesty dial tension**: 185 cases are still abstained, of which **88 are top-3 correct** (hidden wins) and **97 are top-3 wrong** (correct silence). Margin-abstain conflicts directly with the top-3 verdict shape by silencing cases the engine actually got correct in its shown differential.
* **Floor inertness**: The confidence floor of 0.80 fired on **0** cases. All abstention is driven entirely by the margin check.
* **Verdict**: **improved, not settled**

---

## Tier 2 — Decision Map (The Menu)

| Option | What it buys | Gate / Risk |
|---|---|---|
| **Retune margin down** (T-V3-3D-ABSTAIN-CAL) | Sweep shows a **cliff**: relaxing MARGIN 0.05 -> 0.02 roughly doubles coverage (from 37% to 78%). Recovers 61 hidden wins while leaking only 59 top-3 wrong answers. | Owner picks operating point from the sweep; changes the honesty dial's aggressiveness (not the accuracy itself). |
| **Redefine abstain for a top-3 product** | Margin-abstain **fights the top-3 reframe**: it silences cases where the correct family is already in the shown differential. Option: abstain on floor only / on genuine cross-family low-confidence only; let the differential communicate ties. | Owner **definition** decision — what "decline to answer" means when the UI already shows 3 ranked causes. |
| **Fix floor inertness** | **Floor never fires (0/297 < 0.80).** The engine is ≥0.80 confident even when wrong, so absolute-confidence abstain is inert; only margin works. | Larger change, likely score-calibration/research-adjacent; do not fold into a threshold tweak. |
| **Genuine exact ties -> T-V3-4** | ~67 cases tie exactly across families even after family-aware margin — the true ranker ambiguity. | Research-gated (cluster answers) + FT-8 risk. |
| **Same-family residual / dedupe** | Residual same-family sibling artifacts (cf. SCORER_WINDOW `EXP-N010`, `era3_008`). | Owner decision; small; merges with T-V3-D6-SCORERWIN. |

---

## Tier 3 — Margin Sweep

| Margin threshold | Coverage | Covered cases | Total abstained | Hidden wins (top3-correct) | Correct silence (top3-wrong) |
| --- | --- | --- | --- | --- | --- |
| **0.05** (Current) | 37.07% | 109/294 | 185 | 88 | 97 |
| **0.03** | 75.85% | 223/294 | 71 | 27 | 44 |
| **0.02** | 77.89% | 229/294 | 65 | 27 | 38 |
| **0.01** | 77.89% | 229/294 | 65 | 27 | 38 |
| **0.00** (Exact ties only) | 85.37% | 251/294 | 43 | 23 | 20 |
| **Floor-only** (No margin) | 100.00% | 294/294 | 0 | 0 | 0 |

---

## Case-by-Case Movement (Scoreboard Diff)
| Case            | Family           | Movement  | Mode change                    | Single B->A  | Top3 B->A    |
| --------------- | ---------------- | --------- | ------------------------------ | ------------ | ------------ |
| era1_001        | lean_condition   | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| era1_002        | mechanical_wear  | unchanged | ORACLE_SUSPECT->ORACLE_SUSPECT | False->False | False->False |
| era1_003        | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| era1_004        | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| era1_005        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| era1_006        | sensor_fault     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| era1_007        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| era1_008        | catalyst_failure | unchanged | PASS->PASS                     | True->True   | True->True   |
| era1_009        | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| era1_011        | cam_timing       | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| era1_012        | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| era1_013        | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| era1_014        | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| era1_015        | mechanical_wear  | unchanged | ORACLE_SUSPECT->ORACLE_SUSPECT | False->False | False->False |
| era1_016        | exhaust_leak     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| era1_017        | sensor_fault     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| era1_018        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| era1_019        | lean_condition   | unchanged | PASS->PASS                     | False->False | True->True   |
| era1_020        | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| era2_001        | catalyst_failure | unchanged | PASS->PASS                     | True->True   | True->True   |
| era2_002        | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| era2_003        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| era2_004        | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| era2_005        | sensor_fault     | unchanged | PASS->PASS                     | False->False | True->True   |
| era2_006        | lean_condition   | unchanged | PASS->PASS                     | False->False | True->True   |
| era2_008        | cam_timing       | unchanged | PASS->PASS                     | False->False | True->True   |
| era2_009        | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| era2_010        | sensor_fault     | unchanged | PASS->PASS                     | True->True   | True->True   |
| era2_011        | lean_condition   | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| era2_012        | sensor_fault     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| era2_013        | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| era2_014        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| era2_015        | lean_condition   | unchanged | PASS->PASS                     | False->False | True->True   |
| era2_016        | misfire          | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| era2_017        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| era2_019        | rich_mixture     | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| era2_020        | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| era3_001        | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| era3_002        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| era3_003        | ignition_fault   | unchanged | PASS->PASS                     | True->True   | True->True   |
| era3_004        | sensor_fault     | unchanged | PASS->PASS                     | True->True   | True->True   |
| era3_005        | rich_mixture     | unchanged | PASS->PASS                     | False->False | True->True   |
| era3_006        | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| era3_007        | lean_condition   | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| era3_008        | lean_condition   | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| era3_009        | lean_condition   | unchanged | PASS->PASS                     | False->False | True->True   |
| era3_011        | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| era3_013        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| era3_014        | no_fault         | unchanged | DATA_GAP->DATA_GAP             | False->False | False->False |
| era3_015        | lean_condition   | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| era3_016        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| era3_017        | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| era3_018        | cam_timing       | unchanged | PASS->PASS                     | True->True   | True->True   |
| era3_019        | exhaust_leak     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| era3_020        | ecu_fault        | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-009        | no_fault         | unchanged | PASS->PASS                     | False->False | True->True   |
| CASE-010        | sensor_fault     | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-011        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-012        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-013        | catalyst_failure | unchanged | PASS->PASS                     | False->False | True->True   |
| CASE-014        | sensor_fault     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| CASE-015        | catalyst_failure | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| CASE-016        | catalyst_failure | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-017        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-018        | cam_timing       | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-019        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-020        | lean_condition   | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| CASE-021        | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-022        | sensor_fault     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| CASE-023        | rich_mixture     | unchanged | PASS->PASS                     | False->False | True->True   |
| CASE-024        | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-025        | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-026        | catalyst_failure | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-027        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-028        | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-029        | rich_mixture     | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| CASE-030        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-031        | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-032        | lean_condition   | unchanged | PASS->PASS                     | False->False | True->True   |
| CASE-033        | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-034        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-035        | ignition_fault   | unchanged | PASS->PASS                     | False->False | True->True   |
| CASE-036        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-037        | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-038        | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| CASE-039        | ecu_fault        | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| CASE-040        | rich_mixture     | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| CASE-045        | sensor_fault     | unchanged | DATA_GAP->DATA_GAP             | False->False | False->False |
| CASE-048        | sensor_fault     | unchanged | DATA_GAP->DATA_GAP             | False->False | False->False |
| CSV-001         | no_fault         | unchanged | PASS->PASS                     | False->False | True->True   |
| CSV-005         | no_fault         | unchanged | PASS->PASS                     | False->False | True->True   |
| CSV-016         | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-018         | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-022         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-025         | sensor_fault     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| CSV-041         | ecu_fault        | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| CSV-043         | ecu_fault        | unchanged | PASS->PASS                     | False->False | True->True   |
| CSV-045         | ecu_fault        | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| CSV-052         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-066         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-068         | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-072         | ecu_fault        | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-095         | exhaust_leak     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| CSV-100         | lean_condition   | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| CSV-101         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-102         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-103         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-104         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-105         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-106         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-107         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-108         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-109         | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-110         | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-111         | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-112         | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-113         | lean_condition   | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| CSV-114         | lean_condition   | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| CSV-115         | cam_timing       | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-116         | cam_timing       | unchanged | PASS->PASS                     | True->True   | True->True   |
| CSV-117         | mechanical_wear  | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| CSV-118         | mechanical_wear  | unchanged | ORACLE_SUSPECT->ORACLE_SUSPECT | False->False | False->False |
| CSV-119         | mechanical_wear  | unchanged | ORACLE_SUSPECT->ORACLE_SUSPECT | False->False | False->False |
| CSV-120         | mechanical_wear  | unchanged | PASS->PASS                     | False->False | True->True   |
| CSV-121         | catalyst_failure | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| CSV-122         | catalyst_failure | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| CSV-123         | ecu_fault        | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| CSV-124         | ecu_fault        | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| CSV-125         | ecu_fault        | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| CSV-126         | ecu_fault        | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| CSV-127         | no_fault         | unchanged | DATA_GAP->DATA_GAP             | False->False | False->False |
| CSV-128         | no_fault         | unchanged | DATA_GAP->DATA_GAP             | False->False | False->False |
| CSV-129         | exhaust_leak     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| CSV-130         | exhaust_leak     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| ECU-001         | ecu_fault        | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| ECU-002         | ecu_fault        | unchanged | PASS->PASS                     | False->False | True->True   |
| ECU-003         | ecu_fault        | unchanged | PASS->PASS                     | False->False | True->True   |
| ECU-007         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| ECU-008         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| ECU-009         | ecu_fault        | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| EXP-N001        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXP-N002        | ecu_fault        | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| EXP-N003        | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXP-N004        | ecu_fault        | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| EXP-N005        | ecu_fault        | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| EXP-N006        | sensor_fault     | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXP-N007        | cam_timing       | unchanged | PASS->PASS                     | False->False | True->True   |
| EXP-N008        | catalyst_failure | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXP-N009        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXP-N010        | rich_mixture     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| EXP-N011        | lean_condition   | unchanged | DATA_GAP->DATA_GAP             | False->False | False->False |
| EXP-N012        | catalyst_failure | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXP-N013        | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXP-N014        | misfire          | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| EXP-N015        | sensor_fault     | unchanged | PASS->PASS                     | False->False | True->True   |
| EXP-N016        | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXP-N017        | lean_condition   | unchanged | PASS->PASS                     | False->False | True->True   |
| EXP-N018        | ecu_fault        | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| EXP-N019        | ecu_fault        | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| EXP-N020        | sensor_fault     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| EXP-N021        | misfire          | unchanged | PASS->PASS                     | False->False | True->True   |
| EXP-N022        | lean_condition   | unchanged | DATA_GAP->DATA_GAP             | False->False | False->False |
| EXP-N023        | cam_timing       | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| EXP-N025        | catalyst_failure | unchanged | PASS->PASS                     | False->False | True->True   |
| EXP-N026        | ignition_fault   | unchanged | PASS->PASS                     | False->False | True->True   |
| EXP-N027        | rich_mixture     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| EXP-N028        | sensor_fault     | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXP-N029        | lean_condition   | unchanged | DATA_GAP->DATA_GAP             | False->False | False->False |
| EXP-N030        | mechanical_wear  | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| EXT-201         | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXT-202         | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXT-203         | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXT-204         | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXT-205         | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXT-206         | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXT-207         | catalyst_failure | unchanged | PASS->PASS                     | False->False | True->True   |
| EXT-208         | catalyst_failure | unchanged | PASS->PASS                     | False->False | True->True   |
| EXT-209         | cam_timing       | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXT-210         | cam_timing       | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXT-211         | lean_condition   | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| EXT-212         | lean_condition   | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| EXT-213         | catalyst_failure | unchanged | PASS->PASS                     | False->False | True->True   |
| EXT-214         | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXT-215         | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXT-216         | no_fault         | unchanged | DATA_GAP->DATA_GAP             | False->False | False->False |
| EXT-217         | rich_mixture     | unchanged | PASS->PASS                     | False->False | True->True   |
| EXT-218         | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXT-219         | sensor_fault     | unchanged | PASS->PASS                     | False->False | True->True   |
| EXT-220         | no_fault         | unchanged | PASS->PASS                     | False->False | True->True   |
| EXT-221         | ecu_fault        | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| EXT-222         | mechanical_wear  | unchanged | ORACLE_SUSPECT->ORACLE_SUSPECT | False->False | False->False |
| EXT-223         | mechanical_wear  | unchanged | ORACLE_SUSPECT->ORACLE_SUSPECT | False->False | False->False |
| EXT-224         | mechanical_wear  | unchanged | ORACLE_SUSPECT->ORACLE_SUSPECT | False->False | False->False |
| EXT-225         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXT-226         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXT-227         | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXT-228         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXT-229         | sensor_fault     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| EXT-230         | sensor_fault     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| EXT-231         | no_fault         | unchanged | PASS->PASS                     | False->False | True->True   |
| EXT-232         | catalyst_failure | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| EXT-233         | catalyst_failure | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| EXT-234         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXT-235         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXT-236         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXT-237         | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| EXT-238         | exhaust_leak     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| EXT-239         | exhaust_leak     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| EXT-240         | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| MECH-001        | mechanical_wear  | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| MECH-002        | mechanical_wear  | unchanged | ORACLE_SUSPECT->ORACLE_SUSPECT | False->False | False->False |
| MECH-003        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| MECH-004        | cam_timing       | unchanged | PASS->PASS                     | True->True   | True->True   |
| MECH-005        | misfire          | unchanged | PASS->PASS                     | False->False | True->True   |
| MECH-006        | mechanical_wear  | unchanged | ORACLE_SUSPECT->ORACLE_SUSPECT | False->False | False->False |
| PDF-4G-01       | catalyst_failure | unchanged | PASS->PASS                     | False->False | True->True   |
| PDF-4G-02       | misfire          | unchanged | PASS->PASS                     | False->False | True->True   |
| PDF-4G-03       | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| PDF-4G-04       | ignition_fault   | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| PDF-4G-05       | misfire          | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| PDF-HI-001      | rich_mixture     | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| PDF-HI-002      | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| PDF-HI-005      | no_fault         | unchanged | DATA_GAP->DATA_GAP             | False->False | False->False |
| PDF-HI-006      | catalyst_failure | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| PDF-HI-007      | exhaust_leak     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| PDF-HI-008      | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| PDF-HI-010      | no_fault         | unchanged | DATA_GAP->DATA_GAP             | False->False | False->False |
| REAL-001        | non_starter      | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| REAL-002        | lean_condition   | unchanged | DATA_GAP->DATA_GAP             | False->False | False->False |
| REAL-003        | non_starter      | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| REAL-004        | lean_condition   | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| REAL-005        | catalyst_failure | unchanged | PASS->PASS                     | True->True   | True->True   |
| RULE-CO-1       | rich_mixture     | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| TC-011          | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| TC-021          | ecu_fault        | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| TC-046          | sensor_fault     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| TC-048          | exhaust_leak     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| YAML-CSV1       | no_fault         | unchanged | PASS->PASS                     | False->False | True->True   |
| YAML-CSV18      | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| YAML-CSV22      | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| YAML-CSV25      | sensor_fault     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| YAML-CSV41      | ecu_fault        | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| YAML-CSV43      | ecu_fault        | unchanged | PASS->PASS                     | False->False | True->True   |
| YAML-CSV45      | ecu_fault        | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| YAML-CSV5       | no_fault         | unchanged | PASS->PASS                     | False->False | True->True   |
| YAML-CSV52      | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| YAML-CSV66      | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| YAML-CSV68      | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| YAML-CSV72      | ecu_fault        | unchanged | PASS->PASS                     | True->True   | True->True   |
| YAML-CSV95      | exhaust_leak     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| YAML-PDF_4G_01  | catalyst_failure | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| YAML-PDF_4G_02  | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| YAML-PDF_4G_03  | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| YAML-PDF_4G_04  | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| YAML-PDF_4G_05  | misfire          | unchanged | PASS->PASS                     | False->False | True->True   |
| YAML-PDF_HI_001 | rich_mixture     | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| YAML-PDF_HI_002 | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| YAML-PDF_HI_005 | no_fault         | unchanged | DATA_GAP->DATA_GAP             | False->False | False->False |
| YAML-PDF_HI_006 | catalyst_failure | unchanged | PASS->PASS                     | False->False | True->True   |
| YAML-PDF_HI_010 | no_fault         | unchanged | DATA_GAP->DATA_GAP             | False->False | False->False |
| YAML-RULE_CO_1  | misfire          | unchanged | PASS->PASS                     | False->False | True->True   |
| YAML-RULE_NOx_1 | ecu_fault        | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| YAML-TC1        | no_fault         | unchanged | DATA_GAP->DATA_GAP             | False->False | False->False |
| YAML-TC12       | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| YAML-TC22       | ecu_fault        | unchanged | PASS->PASS                     | False->False | True->True   |
| YAML-TC36       | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| YAML-TC37       | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| YAML-TC46       | sensor_fault     | unchanged | DATA_GAP->DATA_GAP             | False->False | False->False |
| YAML-TC47       | ecu_fault        | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| case_001        | ecu_fault        | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| case_002        | rich_mixture     | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| case_003        | lean_condition   | unchanged | DATA_GAP->DATA_GAP             | False->False | False->False |
| case_004        | sensor_fault     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| case_005        | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| case_006        | non_starter      | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| case_007        | non_starter      | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| case_008        | lean_condition   | unchanged | PASS->PASS                     | False->False | True->True   |
| case_009        | sensor_fault     | unchanged | PASS->PASS                     | True->True   | True->True   |
| case_010        | catalyst_failure | unchanged | PASS->PASS                     | True->True   | True->True   |
| case_013        | ecu_fault        | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| case_014        | no_fault         | unchanged | DATA_GAP->DATA_GAP             | False->False | False->False |
| case_015        | rich_mixture     | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| case_016        | lean_condition   | unchanged | DATA_GAP->DATA_GAP             | False->False | False->False |
| case_017        | rich_mixture     | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| case_018        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| case_019        | lean_condition   | unchanged | PASS->PASS                     | True->True   | True->True   |
| case_022        | misfire          | unchanged | PASS->PASS                     | True->True   | True->True   |
| case_023        | rich_mixture     | unchanged | PASS->PASS                     | True->True   | True->True   |
| case_027        | ecu_fault        | unchanged | PASS->PASS                     | True->True   | True->True   |
| case_028        | no_fault         | unchanged | PASS->PASS                     | False->False | True->True   |
| case_034        | catalyst_failure | unchanged | PASS->PASS                     | True->True   | True->True   |
| case_040        | non_starter      | unchanged | PRODUCER_GAP->PRODUCER_GAP     | False->False | False->False |
| case_044        | mechanical_wear  | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
| case_046        | sensor_fault     | unchanged | OUTRANKED->OUTRANKED           | False->False | False->False |
