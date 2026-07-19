# AUDIT — DNALab / VINLab / SymptomLab

**Date:** 2026-06-11
**Author:** architect session
**Scope (two questions):**
1. Do DNALab or VINLab need updates now that **GASLab, OBDLab, and DTCLab** were reworked?
2. Of the 10 questions in `labs/dnalab/DNA10.md`, which can be answered from the `4DLabV2/DBS` database?
**Depth:** answerability map — no heavy data crunching. Findings only; no task files authored, no code changed.

---

## Part 1 — Does the GAS/OBD/DTC rework force DNA/VIN updates?

### How the data actually flows

DNALab emits one `VehicleDNA` JSON (Part A `vin_dna` + Part B `symptom_dna`). COMLab's
projector (`comlab/projection.py`) slices that into three per-lab **views** (a view = a
read-only subset of fields one lab is allowed to see). Each reworked lab then re-parses
its view with its **own local mirror** (a private copy of the type, so no cross-lab import).

```
            VehicleDNA (DNALab/VINLab)        <-- vocabulary is CANONICAL here
                    |
            comlab/projection.py  ── reads vin.get("...")
                    |
        ┌───────────┼───────────┐
     GasView     ObdView     DtcView          <-- COMLab's mirror: also canonical
        |           |           |
   gaslab        obdlab      dtclab  mirrors  <-- REWORK DRIFTED these
```

### Headline finding: VinDNA's vocabulary is **not** broken by the rework

I checked VinDNA's enums against COMLab's canonical vocabulary (`comlab/schemas/vocabulary.py`).
They match exactly — `UpstreamO2Type`, `AirMeteringStrategy`, `InductionType`, `Horizon` are
identical on both sides. So **DNALab/VINLab need no vocabulary change.** The mismatches the
rework introduced live in the *reworked labs' own mirrors*, which drifted away from the
contract — that is a COMLab/semantic reconciliation job, not a DNA/VIN job.

Drift in the reworked-lab mirrors (flagged for COMLab/semantic, **out of DNA/VIN scope**):

| Lab mirror | Field | Mirror's values | Canonical (VinDNA + COMLab) |
|---|---|---|---|
| `obdlab/.../dna_view.py` | `upstream_o2_type` | `NARROWBAND_0_TO_1V`, `WIDEBAND_LINEAR` | `NARROWBAND`, `WIDEBAND_AFR`, `WIDEBAND_LAMBDA` |
| `obdlab/.../dna_view.py` | `induction_type` | NA, TURBO only | NA, TURBO, **SUPERCHARGED** |
| `dtclab/.../dna_view.py` | `air_metering_strategy` | `MAF`, `MAP_SPEED_DENSITY`, `HYBRID` | `DUAL_MAF_MAP_CROSSCHECK`, `MAP_ONLY_SPEED_DENSITY`, `MAF_ONLY` |
| `dtclab/.../dna_view.py` | `resolved_horizon` | `HORIZON_CLASSIC` (Euro 3–4) | `HORIZON_ADAPTIVE` (Euro 3–4) |

### What DNA/VIN **does** genuinely lack (the real action items)

These are cases where COMLab's projector *reads* a field but VinDNA does not supply it at
the path read. Each has a **named, existing consumer**, so each is a legitimate v2 candidate
(not "future use"):

| # | Gap | Consumer + code path | Why it's real |
|---|---|---|---|
| **A** | `rated_rpm` never emitted by VinDNA | `projection.py:89` → `ObdLabDnaView.rated_rpm` → OBDLab DNA-relative RPM ceiling (`OBDLab_KG_Wiki §3.1`) | `grep` confirms no `rated_rpm` is produced anywhere in `vinlab/`. It always projects as `None`. **The source data exists** — `DBS/docs/vehicles_petrol_specimens.csv` column `P14_rated_rpm`. |
| **B** | `has_catalyst` / `egr_equipped` read at **top level**, VinDNA nests them under `emissions{}` | `projection.py:77-78, 92, 106-107` → Gas/Obd/Dtc views → EGR_STUCK faults (GAS), CATALYST/EGR_HISTORY routing (DTC) | Path mismatch ⇒ flags arrive `None`. Fixable on either side; needs one canonical decision. |
| **C** | CoC targets `target_lambda_v112`, `co_low_idle`, `co_high_idle` read from `emissions{}`, VinDNA emits them **top-level** | `projection.py:79-81` → `GasLabDnaView` → per-vehicle CoC threshold tables / Brettschneider eval | Same path mismatch ⇒ GASLab's per-vehicle CoC targets silently lost. This is exactly the channel DNA10 Q3 is about. |
| **D** | `model` required by DTCLab's mirror but emitted by no one | `dtclab/.../dna_view.py DtcLabDnaView.model: str` | COMLab's own `DtcLabDnaView` omits `model` and VinDNA never sets it → latent inconsistency (ties to DNA10 Q8). |
| **E** | GASLab proposed `fuel_type`, `altitude_band` (context-only) | `gaslab wiki 01_role_boundaries §1.4 [v2: q9]` → `comlab/schemas/lab_dna_views` | Marked **proposal** in the GAS wiki; per the v2-rework rule these ship as a proposal with their consumer, via `comlab/config/proposals/`. |

**Bottom line for Part 1:** No DNA/VIN *vocabulary* rework is required — VinDNA stays
contract-canonical. The honest DNA/VIN-side work the rework surfaced is small and concrete:
**A** (add `rated_rpm`, data already in DBS) and **B/C** (resolve the projector-vs-VinDNA
path disagreement on emissions flags + CoC targets). **D/E** are watch-items / proposals.

---

## Part 2 — Can the DBS database answer the 10 DNA10 questions?

`DBS` is a **vehicle-identity and type-approval corpus**, not a clinical one. It holds:

- `docs/vehicles_petrol_M1_1990_2020.csv` — 552,018 rows: VIN ↔ make ↔ commercial name ↔ `engine_code` ↔ first registration.
- `docs/vehicles_petrol_specimens.csv` — 7,079 rows: full per-VIN CoC (CO low/high idle, λ V112, `rated_rpm`, noise, euro class).
- `docs/engine_baseline.csv` — 11,801 engine-code baselines; **92.7% HIGH** confidence; sources **NIO (national registry) + DVSA**; λ field filled 42.4%.
- `docs/dvsa_limits.csv` — 5,747 UK MOT idle/λ test limits per make+engine code.
- `docs/tecdoc_engine_attrs.csv` — 2,205 engine codes with induction/injection/cylinder/catalyst/O₂/air-metering/VVT attributes; full TecDoc `1Q2019/`.
- `OPSI_…/Nio_vozila_{1,2,3}.csv` — ~1.8M Slovenian registration records (COC mark, masses, VIN). Registration only — no fault/symptom/repair fields.

Critically, **nothing in DBS records an operator symptom, a confirmed fault, or a repair
outcome.** That single fact decides most of the table.

| Q | Topic | DBS answerable? | Where / why |
|---|---|---|---|
| 1 | Symptom→fault confusion matrix | **No** | No symptom or confirmed-fault records anywhere in DBS. Needs a labeled repair-order corpus. |
| 2 | VIN-decode resolution 1990–2010 | **Yes** | `vehicles_petrol_M1_1990_2020.csv` (552k VIN↔engine_code) + `petrol_vin/` decoder lets you measure real make/year/engine-code resolution rates empirically. |
| 3 | Per-engine-code CoC idle datasets | **Yes** | `engine_baseline.csv` (11,801 codes, 92.7% HIGH, NIO+DVSA sourced) + `vehicles_petrol_specimens.csv` + `dvsa_limits.csv`. **Refutes the "synthetic medians" worry — a genuine national-registry CoC source exists.** Fill rate is quantifiable per field (λ ≈ 42%). |
| 4 | Which identity attributes interact with diagnosis | **Partial** | DBS answers *attribute availability/coverage* (tecdoc + baseline). Whether an attribute *changes the answer* is answered against lab fault logic, not DBS (mapped in Part 1's view tables). |
| 5 | Structured-symptom vocabulary techs use | **No** | No symptom-language corpus in DBS. Only artifact is symptomlab's 18-pair catalog. |
| 6 | Environmental context → fault prior | **No** | No symptom-context↔fault evidence in DBS. |
| 7 | Aftermarket-mod prevalence (de-cat, WB-O₂) | **No** | Registration/type-approval data reflects factory config, not retrofits. |
| 8 | Does finer identity (`model`/variant) matter | **Partial (mostly yes)** | Tractable from DBS: group `vehicles_petrol_specimens.csv` by `engine_code` and test within-code CoC variance. Low variance ⇒ `model` adds nothing ⇒ confirms `model` can stay empty (ties to Gap D). |
| 9 | Real-world false symptom-report rate | **No** | Needs paired reported-symptom vs confirmed-fault data; absent. |
| 10 | Does labeled symptom→confirmed-fault data exist | **No (not locally)** | DBS has none; `DBS/webresearch/` holds parts/spec API scouting (RDW, autodata, TAME) — not repair-outcome datasets. |

### The clean split

DBS strongly powers the **identity / Part-A** questions (Q2, Q3, and most of Q4 & Q8) — the
VINLab side. It contains **nothing** for the **operator-symptom / Part-B** questions (Q1, Q5,
Q6, Q9, Q10) or aftermarket reality (Q7). Those are precisely the *prior-strength* questions
DNA10 itself flags as the weakest channel — and they cannot be moved at all from DBS. They
need a repair-order / symptom-labeled corpus that does not exist in this database.

**Tally:** Answerable 2 (Q2, Q3) · Partial 2 (Q4, Q8) · Not answerable from DBS 6 (Q1, Q5, Q6, Q7, Q9, Q10).

---

## Unplanned follow-ups (candidate tasks — not authored, not registered)

| Candidate | One-line | Named consumer |
|---|---|---|
| T-DNA-RATEDRPM | Emit `rated_rpm` from VINLab, sourced from `vehicles_petrol_specimens.csv P14` | `ObdLabDnaView.rated_rpm` (RPM ceiling, OBDLab_KG_Wiki §3.1) |
| T-DNA-PATHFIX | Reconcile projector-vs-VinDNA path for emissions flags + CoC targets (decide canonical side) | GasLab CoC tables / DTC CATALYST+EGR routing |
| T-SEM-MIRROR-DRIFT | Realign OBD/DTC lab mirrors to canonical vocabulary (o2, air-metering, horizon, induction) | COMLab projection ↔ lab boundary |
| T-DNA-Q3-COC-STUDY | Quantify CoC fill % per engine_code from `engine_baseline.csv` to set the prior honestly | DNALab CoC target population |
| T-DNA-Q8-VARIANCE | Within-`engine_code` CoC variance study to confirm `model` can stay empty | VinDNA `model` scope decision |

Each row above has a nameable existing consumer, so each is a real proposal rather than
"future use" — but none is authored here. One task per session; these are findings for the
owner to schedule.
