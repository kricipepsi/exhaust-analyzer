# OBDLab Purge Audit — 2026-06-08

**Author:** architect (Cowork session)
**Scope of audit:** `labs/obdlab` — live `obdlab/` package, `tests/`, `config/`, schemas.
**Question put to the audit:** *Which code kept v1 OBDLab useless (stalled, near-100% NO_FAULT, quarantine-bound), and which SAI / 2010–2020 era artefacts are no longer in 4DLab scope?*
**Deliverable:** findings + recommended purge dispositions. This is a **spec/finding document**, not a diff. No code was edited. Removal is downstream of the `T-OBDV2-0` revive/quarantine gate.

---

## 0. One-line answer

Two things keep OBDLab stalled, and they are separable:

1. **A dead fault-family classifier layer** (`ranking.py` + `family_map.py`, ~346 LOC) wired to the **archived `OBDLabSimple`/`COMLabSimple` composition path**. It has **no live consumer**, it collapses every signature to one of four families (mostly `no_fault`), and it is the visible source of the ">95% NO_FAULT" behaviour. It is dead under *either* revive or quarantine.
2. **Orphan era/emissions schema fields** on the DNA view (`EuroEmissionCategory`, `ResolvedHorizon`, `ObdEmissionsView`/`egr_equipped`) — defined but read **nowhere** in OBDLab. These are the "2010–2020 artefact" you flagged, plus their 1990–2010 siblings. They are signal/noise breaches.

**SAI:** there is **no SAI code, schema, or config artefact** anywhere in `obdlab/`. SAI exists only in the `research/sources/` corpus (1990s-era material). Nothing to purge in code.

---

## 1. What is actually *live* in OBDLab (the keep set)

The real pipeline is the analytics-channel emitter, not a classifier. Entry point `SensorSignalTranslator.translate()` (`obdlab/core/sensor_signal_translator.py`) wires §3–§12 and returns an **`OBDLivePayload`** of typed channels (trims, normalized lambda, VE, `o2_failure_mode`, gates). It **never calls** `rank_candidates`, `classify_top3`, or `signature_to_family`.

Live modules and their real consumers (verified by grep, refs outside the defining file):

| Module | Role | Live? |
|---|---|---|
| `core/sensor_signal_translator.py` | orchestrator → `OBDLivePayload` | ✅ public surface (`obdlab/__init__.py`) |
| `core/pid_ingestion_validator.py` | §3 sanitize + DNA-RPM gate | ✅ |
| `core/state_bucketing.py` | §8.2 rpm bucket | ✅ |
| `core/semantic_consistency_checker.py` | §4 thermal/physics gates | ✅ |
| `core/ve_engine.py` | §10 VE | ✅ |
| `core/o2_normalizer.py` | §11 lambda normalization | ✅ |
| `core/trim_vector_aggregator.py` | §12 trim | ✅ |
| `core/analytics_preconditions.py` | §9 trim gate | ✅ |
| `schemas/payload.py`, `schemas/vocabulary.py` | output contract | ✅ |
| `schemas/dna_view.py` | input DNA view (partly live, partly orphan — see §3) | ⚠️ mixed |

This keep set is what the v2 ledger (`tasks/PROGRESS.md`) and the inherited cross-lab specs (`T-OBDV2-ECU-PERCEPT-1` / DEP-2, `T-OBDV2-BANK-ASYM-1` / DEP-3) build on. None of them touch `ranking.py`/`family_map.py`.

---

## 2. Dead "useless-v1" code — recommend PURGE

### 2.1 The dead classifier layer

| File | LOC | Evidence it is dead |
|---|---|---|
| `obdlab/ranking.py` | 266 | Docstring: *"keeps the internal runners-up needed by the later **OBDLabSimple** composition path"*; `classify_top3` builds *"a plain stdlib tuple surface for the composition adapter … **COMLabSimple `LabResult`**"*. Imported **only** by `tests/unit/test_ranking.py` and `tests/unit/test_classify_top3.py`. |
| `obdlab/family_map.py` | 80 | Docstring: *"name the family that later ranking code can pass through to **COMLabSimple's LabCandidate.fault_id**"*. Imported **only** by `ranking.py` and tests. `OBDLAB_REACHABLE_FAMILIES` = `{sensor_fault, lean_condition, rich_mixture, no_fault}`; `signature_to_family()` returns `no_fault` for everything non-discriminating — this is the literal ">95% NO_FAULT" collapse. |
| `tests/unit/test_ranking.py` | 133 | Tests of the above; die with the modules. |
| `tests/unit/test_classify_top3.py` | 152 | Tests of the above; die with the modules. |
| `tests/unit/test_family_map.py` | 78 | Tests of the above; die with the modules. |
| **Total** | **~709** | |

**Why it is safe to remove (the signal/noise + consumer check):**

- **No live consumer in OBDLab** — `translate()` does not call it.
- **No live consumer anywhere in `4DLabV2`** — grep for `classify_top3` / `rank_candidates` / `signature_to_family` / `obdlab.ranking` / `obdlab.family_map` / `OBDLabSimple` returns **only** `labs/obdlab/` tests (the only other `ranking.py` hits are DTCLab's *own, separate, live* classifier — unrelated).
- **The historical consumer is already condemned** — `DECISIONS.md` **D-V2-10**: *"All `*Simple/` are dead experiments → ARCHIVE (COMLabSimple, GASLabSimple, **OBDLabSimple**, DTCLabSimple — the top-3 line) … `T-RM-3-WIRED` is cut-on-copy."* OBDLab's `ranking`/`family_map` were the OBDLab feeder for that archived top-3 line.

> **Important framing (not hidden):** deleting this layer does **not**, by itself, make OBDLab diagnostic. It removes the dead surface that *pretended* OBDLab classifies faults. In v2 the verdicts are re-homed to **COMLab fusion** (`ecu_fault` via DEP-2, bank asymmetry via DEP-3); OBDLab's job becomes a clean **analytics-channel emitter**. The purge clears the schema so the new perception-delta / per-bank-trim channels can land without colliding with the no_fault classifier.

### 2.2 Relationship to the `T-OBDV2-0` gate

`tasks/PROGRESS.md` makes `T-OBDV2-0` (revive vs quarantine) the gate that blocks all OBDLab work. **This purge is independent of that decision** — the classifier is dead whether OBDLab is revived or quarantined — so it can be specced as a standalone cleanup task that *unblocks* a clean revive. Recommend authoring it as **`T-OBDV2-PURGE-1`** (see §5). I did **not** flip any ledger row.

---

## 3. Orphan era / emissions artefacts — the "2010–2020" finding (recommend PURGE from OBDLab)

All of the following live in `obdlab/schemas/dna_view.py` and have **zero references anywhere in `obdlab/` outside that file** (verified by per-symbol grep):

| Symbol | Location | Refs outside `dna_view.py` | The era range |
|---|---|---|---|
| `EuroEmissionCategory` (`EURO_1`…`EURO_7`, `UNKNOWN`) | `dna_view.py:13` | **0** — not even used by `ObdLabDnaView` itself | — |
| `ResolvedHorizon` (`HORIZON_LEGACY` / `ADAPTIVE` / `MODERN`) | `dna_view.py:60` | **0** | LEGACY = Euro 1–2, **1990–2000**; ADAPTIVE = Euro 3–4, **2000–2010**; MODERN = Euro 5–7, **2010–2020** ← your flag |
| field `resolved_horizon: ResolvedHorizon` | `dna_view.py:107` | **0** | era-gating field, read by nobody |
| `ObdEmissionsView` + `egr_equipped: bool` | `dna_view.py:83` / `:88` | **0** | EGR-present flag, read by nobody |
| field `emissions: ObdEmissionsView` | `dna_view.py:106` | **0** | — |

Notes:

- `EURO_7` + the `HORIZON_MODERN` comment "Euro 5-7, 2010-2020" is internally **anachronistic** (Euro 7 is not a 2010–2020 band) — a sign these were copied in speculatively, never wired.
- **These are required by the project's own signal/noise rule to come out of OBDLab**: a field with no named OBDLab consumer does not belong on OBDLab's schema.
- **The era/EGR capability is not lost — it is re-homed by existing proposals, and neither names OBDLab as the consumer:**
  - `research/proposals/extracted/EP-DNA-03_euro-era-tier-gate.md` (status *PROPOSAL, named consumer*): emits `euro_tier` + `era` from **DNALab**, consumed by **COMLab `fault_atlas`** — not OBDLab.
  - `research/proposals/extracted/EP-FA-06_egr-insufficient-flow.md`: EGR logic keyed in **`fault_atlas_router.py`** (fault-atlas/COMLab), not OBDLab.

So purging these from `obdlab/dna_view.py` is **consistent with** the forward-progress proposals: the era/EGR fields belong on the DNALab→COMLab path, not mirrored unused in OBDLab.

**Keep (these DNA-view fields have real OBDLab consumers — do NOT purge):** `air_metering_strategy` (ve_engine), `upstream_o2_type`/`O2SensorType` (o2_normalizer), `induction_type`/`InductionType` (semantic Physics_Gate_3), `confidence`/`VinConfidence` (pid_ingestion + semantic), `engine_displacement_liters`, `cylinder_count`, `rated_rpm`, `stress_idle_rpm_target`.

---

## 4. SAI (secondary air injection) — no code artefact

`grep -i` for `secondary air | \bSAI\b | air injection | smog pump | P041x` across `obdlab/`, `tests/`, `schemas/`, `config/`:

- **Code / schema / config: zero hits.** There is nothing to purge.
- **Research corpus only:** `research/sources/various/Vol6.md` (SAI pumps as a **1990s** cold-start catalyst-light-off device — i.e. `HORIZON_LEGACY` era), `Vol2.md`, `Vol4.md` (`P0411`), and `PIDresearch.md` (Mode 06 secondary-air monitor).

**Disposition:** `research/sources/` is reference material, not shipped code, so it does not breach signal/noise and needs no purge action. If you want the research corpus itself pruned to the in-scope era, that is a **separate documentation task**, not part of the code purge — flagged below as an unplanned follow-up. SAI being "out of scope" reinforces the §3 conclusion that the legacy/era machinery should not be carried in OBDLab code.

---

## 5. Recommended task (architect to author; coder to run after `T-OBDV2-0`)

**`T-OBDV2-PURGE-1` — remove dead OBDLabSimple classifier + orphan era/EGR DNA fields.**

- **Delete:** `obdlab/ranking.py`, `obdlab/family_map.py`, `tests/unit/test_ranking.py`, `tests/unit/test_classify_top3.py`, `tests/unit/test_family_map.py`.
- **Trim from `obdlab/schemas/dna_view.py`:** `EuroEmissionCategory`, `ResolvedHorizon`, `ObdEmissionsView`, fields `resolved_horizon` and `emissions`. Update `tests/unit/test_dna_view.py` field-set assertion accordingly.
- **Success criteria:** grep-gate each deleted symbol as a *target* returns no live (non-test) reference before deletion; after deletion `ruff` + `pyright` + `pytest -x -q` clean; `translate()` → `OBDLivePayload` unaffected (no live path imported the removed code).
- **Consumer (signal/noise):** N/A — this is a *removal* that restores the invariant; the net effect is that every remaining `dna_view` field has a named OBDLab consumer.
- **Sequencing:** independent of revive/quarantine; recommend running it as the cleanup that precedes a `revive` `T-OBDV2-0`.

---

## Unplanned follow-ups (not in this audit's scope)

| # | Item | Why deferred |
|---|---|---|
| U1 | Decide whether `research/sources/various/Vol6.md` SAI / pre-OBD-II era material is pruned or retained as historical reference | Documentation-scope, not a code purge; owner call |
| U2 | Wiki drift already catalogued in `wiki/drift_inventory_2026-05-25.md` (15 rows) — independent of this purge | Separate `T-DOC-N` track |
| U3 | If `T-OBDV2-0` = revive, author the analytics-channel build (DEP-2 perception-delta, DEP-3 per-bank trim) | Gated on Q1/Q2/Q4/Q6 research + the gate decision |

*One task per session: this document is the audit deliverable only. Authoring `T-OBDV2-PURGE-1` into the ledger and any code removal are separate sessions.*
