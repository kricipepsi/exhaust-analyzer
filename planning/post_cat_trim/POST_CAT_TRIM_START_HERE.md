# Post-Cat Fuel-Trim (B1S2) — Implementation Roadmap

**Authored:** 2026-06-21 (architect, Cowork). **Decision:** Option C — real re-implementation.
**Goal:** add post-cat (downstream Sensor-2) fuel-trim modelling so oil-consumption faults are
discriminated by the **secondary fuel-trim loop** the Bosch MED17.4 ECU actually uses, exactly as
mocked in `planning/sim/oil_burn_5fr_sim.py` (5/5 cases green).
**Truth sources:** `labs/vinlab/tasks/5fr.md`, `labs/vinlab/tasks/O2NBvsWB.md`, `planning/OilburnCases.md`,
`planning/OIL_CASE_SIGNATURES_5FR.md`.
**Hard depends on:** `T-VIN-FIX-3` (decoder must import/decode first).

## Architecture rule reminders (apply to every task)
- **Wiki is truth; code reconciles up to wiki.** Stage 0 (wiki) lands before any code.
- **Emitter labs emit channels, not verdicts.** OBDLab emits the B1S2 trim + a derived bias channel;
  the verdict is COMLab/registry fusion.
- **Every new field names its consumer in the same change** (signal/noise governance).
- **No cross-lab Python imports.** COMLab mirrors OBDLab/VINLab types over JSON.
- **Numeric literals carry a wiki citation.** Reports `.md` only; archive, never delete.

## Stage order & dependencies
```
PCT-1 ─┐
PCT-2 ─┼─(wiki truth)─> PCT-4 ─(DNA/identity)─> PCT-5 ─> PCT-6 ─> PCT-7 ─> PCT-8 ─> PCT-9 ─> PCT-10
PCT-3 ─┘                                         (OBDLab emit)   (COMLab/registry)  (wire) (verify)
```

## Ledger
| ID | Title | Lab | Depends | Status |
|---|---|---|---|---|
| PCT-1 | O2_MODEL_STRATEGY wiki: 3 configs + secondary loop + B1S2 semantics | wiki | — | pending |
| PCT-2 | OBDLab wiki: B1S2 PIDs + post_cat_trim_bias channel + gates | wiki | PCT-1 | pending |
| PCT-3 | VINLab/registry wiki: dual sensor-type + trim-role + per-mode evidence | wiki | PCT-1 | pending |
| PCT-4 | Identity: upstream+downstream o2 type + trim role; seed 5FR | vinlab/dnalab | PCT-3 | pending |
| PCT-5 | OBDLab schema+ingestion: shrtft_b1s2 / longft_b1s2 + DFCO state | obdlab | PCT-2,4 | pending |
| PCT-6 | OBDLab core: B1S2 aggregation + derived post_cat_trim_bias enum | obdlab | PCT-5 | pending |
| PCT-7 | COMLab: mirror B1S2 fields + perception_contradiction uses values | comlab | PCT-6 | pending |
| PCT-8 | Registry: post-cat evidence on MW-001/002/008/009 (supersedes U-WV2-1/2) | registry | PCT-7 | pending |
| PCT-9 | wiredV2 composition: forward fields + bias; 5 case fixtures | wiredV2 | PCT-8 | pending |
| PCT-10 | E2E tests + corpus + sim-parity (5/5 match the simulation) | all | PCT-9 | pending |

---

## PCT-1 — Wiki: O2_MODEL_STRATEGY (canonical truth)
**Do:** document the three sensor configs (NB+NB / **WB+NB** / WB+WB), the dual-loop control (primary
upstream + **secondary downstream fuel-trim**), the B1S2 STFT/LTFT semantics, and the per-oil-mode
post-cat signatures (FIXED_NEGATIVE rings · TRANSIENT_NEGATIVE valve seals · DIVERGENT PCV ·
DFCO_NEGATIVE turbo). **Files:** `labs/comlab/wiki/O2_MODEL_STRATEGY.md` (or canonical home). **Gate:**
review; this is the source every later task cites.

## PCT-2 — Wiki: OBDLab post-cat PIDs + bias channel
**Do:** define PIDs `shrtft_b1s2`, `longft_b1s2` (units %, range, null rules), the **DFCO** sample state,
validity gates (engine_warmed; B1S2 invalid until catalyst light-off), and the **derived channel**
`post_cat_trim_bias` (enum: NEUTRAL/FIXED_NEGATIVE/TRANSIENT_NEGATIVE/DIVERGENT/DFCO_NEGATIVE).
**Files:** `labs/obdlab/.../wiki/`. **Consumer named:** registry MW evidence (PCT-8). **Gate:** review.

## PCT-3 — Wiki: identity + registry evidence semantics
**Do:** specify `upstream_o2_type`, `downstream_o2_type`, `downstream_trim_role` on the vehicle-identity
contract, and how registry rules read post-cat evidence per failure mode. **Files:** `labs/vinlab/wiki/`,
`labs/comlab/registry` wiki. **Gate:** review.

## PCT-4 — Identity: dual sensor type + trim role (data)
**Do:** add `upstream_o2_type` + `downstream_o2_type` + `downstream_trim_role` to `vref.db`/VinDNA and
the DNA views; **seed 5FR = WIDEBAND / NARROWBAND / SECONDARY_FUEL_TRIM** (corrects today's wrong
single `o2_type='NB'`). **Files:** `labs/vinlab/vinlab/data/vref.db`, `models.py`, `decoder.py`,
`labs/dnalab/...`. **Consumer:** OBDLab DNA view + COMLab perception. **Gate:** `5FR` decodes with WB
upstream + NB downstream + SECONDARY_FUEL_TRIM; vin tests green.

## PCT-5 — OBDLab schema + ingestion (emit raw B1S2)
**Do:** add `shrtft_b1s2` / `longft_b1s2` to the OBD payload + ingestion validator (range −127..127,
null when no downstream trim role), ingest the DFCO sample flag. **Files:**
`labs/obdlab/obdlab/schemas/payload.py`, `core/pid_ingestion_validator.py`,
`core/sensor_signal_translator.py`. **Consumer:** PCT-6 aggregator. **Gate:** obdlab tests + ruff/pyright/pytest.

## PCT-6 — OBDLab core: bias derivation (emit channel, not verdict)
**Do:** aggregate B1S2 trims and derive `post_cat_trim_bias` per PCT-2 (incl. DIVERGENT = upstream sign
vs downstream sign; DFCO_NEGATIVE = B1S2 rich during fuel-cut). Gate on warmed/light-off. **Files:**
`labs/obdlab/obdlab/core/trim_vector_aggregator.py` (+ new helper), `semantic_consistency_checker.py`.
**Consumer:** COMLab (PCT-7) + registry (PCT-8). **Gate:** unit tests for each bias value.

## PCT-7 — COMLab: mirror + perception
**Do:** mirror `shrtft_b1s2`/`longft_b1s2`/`post_cat_trim_bias` into `OBDLiveDataPayload`; extend
`perception_contradiction` to consume **actual B1S2 values** (today it only reads the
`SECONDARY_FUEL_TRIM` role flag). **Files:** `labs/comlab/comlab/schemas/ingestion.py`,
`core/perception_contradiction.py`. **Consumer:** registry. **Gate:** comlab tests.

## PCT-8 — Registry: post-cat evidence on the MW rules
**Do:** add post-cat evidence rows so: MW-001 ← FIXED_NEGATIVE, MW-002 ← TRANSIENT_NEGATIVE,
MW-008 ← DIVERGENT, MW-009 ← DFCO_NEGATIVE; retune competition so rings + PCV route cleanly. This
**supersedes follow-ups U-WV2-1 / U-WV2-2**. **Files:** `labs/comlab/registry/rules/mechanical_wear.json`
(+ rule tests). Numeric thresholds carry wiki cites (PCT-1/2). **Gate:** rule tests green.

## PCT-9 — wiredV2 composition: wire it through
**Do:** forward upstream/downstream o2 types + B1S2 fields + bias through `composition.py` mapping with
`# consumer:` comments; author/refresh 5 case fixtures (`cases/oil_*.json`) with B1S2 values from
`OIL_CASE_SIGNATURES_5FR.md`. **Files:** `apps/wiredV2/wiredv2/composition.py`, `wiredv2/cases/`.
**Gate:** `run_case.py` prints MW-001..009 for the 5 cases.

## PCT-10 — End-to-end + sim parity
**Do:** integration tests that all 5 oil cases route on the **real** pipeline to the same verdicts the
simulation produces (5/5); add to corpus; full regression. **Files:** `apps/wiredV2/tests/`,
`labs/comlab/registry/corpus_curated.csv`. **Gate:** `pytest` green across touched labs; parity table
matches `planning/sim/OIL_BURN_5FR_SIM_RESULTS.md`.

---

## Out of scope (whole effort)
Wideband-downstream (WB+WB premium) OSC mass-balance model — note as a future lane, not built here.
No graphify. No verdicts in emitter labs. The standalone simulation stays as the reference oracle.
