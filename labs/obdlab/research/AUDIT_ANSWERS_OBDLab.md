# OBDLab audit questions — researched answers

**Author:** architect (4DLab) · **Date:** 2026-06-08
**Source of record:** `labs/obdlab/research/chunks/` (the new wiki — 57 chunks, all readability-gate clean).
**Question source:** `docs/reference/audit_2026-06-03/4DLAB_CAPABILITY_AUDIT_AND_RESEARCH_QUESTIONS.md` → OBDLab § (Q1–Q10).
**Purpose:** close the research gate that blocks `T-OBDV2-ECU-PERCEPT-1` (Q1+Q4) and `T-OBDV2-BANK-ASYM-1` (Q2+Q6), and pin the remaining OBDLab answers so `T-OBDV2-2…10` can be authored. Numbers are quoted research data from the chunks (cited inline); they are not code.

---

## Q1 — Can `ecu_fault` be separated from a genuine mixture fault using only OBD-II data, and with which PIDs?

**Answer: Not from OBD-II data *alone* in the defining sense.** "`ecu_fault` = the ECU is wrong about the mixture" is a **truth-vs-perception** verdict — it only resolves where the ECU's λ (perception) is compared against the gas analyser's Brettschneider λ (ground truth). OBD-II supplies the *perception* half; the separation happens at the **gas↔OBD fusion layer** (COMLab), which is exactly why the architecture splits it (GASLab emits reality, OBDLab emits perception, COMLab fuses). So the honest answer to "OBD-II alone": **no** — but OBD-II carries strong **mode-discriminating** fingerprints once a contradiction is flagged.

**The OBD-side discriminator (PID combination), from the comparative signature tables:**

1. **Bank symmetry** — internal/shared-plane ECU faults hit **both banks symmetrically** (B1≈B2); external sensor/harness faults are **bank-specific**. Needs `shrtft1/longft1` vs `shrtft2/longft2` → `total_trim_correction_delta` vs `_b2`. ⚠ `total_trim_correction_delta_b2` is **emitted but read nowhere** in COMLab today — the consumer must be added.
2. **Pinned trims + implausible context** — e.g. collapsed 5 V rail = `+25 %` STFT/LTFT *both* banks + artificially-low MAP + global lean tailpipe + high NOx; ground-trace blown = `LOAD 100 %` + `ECT −40 °C` locked + `TPS 100 %` at idle. Needs `calculated_engine_load_pct`, `coolant_temp_c`, `manifold_vacuum_kpa`, **and TPS/IAT** (not currently payload fields — field gap).
3. **Deceptive λ** — single-cylinder coil/injector faults read `λ_chem ≈ 1.01` (normal-looking) while `HC ≈ 2200 ppm`. This *requires GASLab HC*, reinforcing that OBD alone is insufficient.

**Quantified (Table 1/2, `ecu-diagnosis/07`):** Mode 5 VREF collapse → STFT/LTFT +25 % both banks, MAP artificially low, λ_chem 1.35→1.55; Mode 4 ground-trace → trims 0/0, LOAD 80–100 %, ECT −40 °C; Mode 2A injector-open (B1) → STFT/LTFT +25 % B1 only, B2 ~0–3 %.

**Sources:** `ecu-diagnosis/07_comparative-signature-tables.md` (Tables 1–3 + analytical conclusions), `ecu-diagnosis/01_method-load-pct-and-idle-bands.md`, `o2-logic/05_bias-vs-real-truth-perception.md`, `truth-perception/02_lambda-delta-vector-and-scoring.md`.

**Unblocks `T-OBDV2-ECU-PERCEPT-1`:** ✅ confirms the design — OBDLab emits `lambda_perception_delta` (the trigger) **plus** per-bank trim symmetry (the discriminator). Two architect pins fall out: (a) the consumer must **read `total_trim_correction_delta_b2`** (today an orphan); (b) **TPS/IAT** are a real field gap — add only if the ECU checker names them as consumers (ECU-FU-3), else drop.

---

## Q2 — Realistic STFT/LTFT magnitudes and signs per fault family at warm idle (1990–2010 petrol)?

**Answer: pinned from the 20-case real-world matrix.** Healthy warm closed-loop idle = STFT −5…+5 % (bouncing), LTFT −10…+10 %, total within ±10 %; bank-to-bank match within ±5 %. Severity ladder: ±10 % healthy / ±10–20 % investigational / >±20 % confirmed. DTC set-points: LTFT ≈ **+25 %** → P0171/P0174 (lean), ≈ **−25 %** → P0172/P0175 (rich); many OEMs trip at total ≈ **±18 %**.

**Per-family signs/magnitudes (idle → 2500 RPM), the discriminator being the idle→RPM shift:**

| Family | idle STFT/LTFT | @2500 RPM | Tell |
|---|---|---|---|
| Vacuum leak (post-MAF) | +15 / +25 | →0 / +5 | drops toward 0 at RPM |
| Fuel-delivery restriction | +2 / +5 | +25 / +25 | worsens at RPM |
| MAF/MAP sensor bias | −22…−12 (or +) | flat across RPM | RPM-independent |
| Leaking injector / rich | −20…−25 | −15…−20 | negative, flat |
| Single-bank (injector/coil/compression) | +14…+18 **one bank** | persists | single-bank only |
| Open-loop / failsafe (ECT stuck, EGR, limp) | 0 / 0 | 0 / 0 | trim *silence* + symptom |

**Sources:** `fuel-trim/03_normal-ranges-and-dtc-thresholds.md`, `fuel-trim/09_fault-family-case-matrix.md` (20 cases), `fuel-trim/04_trim-pattern-decision-tree.md`, `fuel-trim/05_bank-to-bank-comparison.md`.

**Unblocks `T-OBDV2-BANK-ASYM-1`** (and the T-OBDV2-1a logset realism): ✅ provides the real per-family trims to replace the 16 guessed corpus cases, and the ±5 % bank-match bound that defines "asymmetry".

---

## Q3 — Do real STFT/LTFT PIDs reach ±100/±127, or is that a sentinel? What does a shorted/open O₂ report?

**Answer: ±127 % is a sentinel, not a reading.** ±127 % is the absolute signed-8-bit register limit; ±99 % on a scan tool means "ECU commanding maximum correction." Both are **range-limit/sentinel values** — treat a pegged value as "very large deviation, magnitude meaningless," never as a measured trim. Real closed-loop trims with a healthy sensor sit in the bands in Q2. (This confirms the T-OBDV2-0 note: the corpus's ±127 rows were sentinels, not data.)

**Shorted/open O₂ on a scan tool:** `STUCK_RICH` = pinned **> 0.85 V** (silicone poisoning / short-to-voltage); `STUCK_LEAN` = pinned **< 0.20 V** (exhaust leak pre-sensor / short-to-ground); `DEAD` = flat ~0.45 V bias, no switching (open heater / broken wire → ECU drops to open loop, sets P0134-family).

**Sources:** `fuel-trim/06_trim-rails-and-sentinels.md`, `fuel-trim/03_normal-ranges-and-dtc-thresholds.md`, `o2-logic/03_failure-modes-taxonomy.md`.

**Unblocks:** T-OBDV2-1a — fixtures use realistic trims everywhere except the explicit saturation **rejection** case; shorted/open-O₂ cases use the pin thresholds above.

---

## Q4 — Which model years/protocols actually report a usable λ / commanded-λ PID (so `lambda_perception_delta` is computable on the real fleet)?

**Answer: only where a wideband/linear λ or a commanded-equivalence-ratio PID exists — i.e. Era 2+ (≈2000–2010, Euro 3→4 mainstream).** A **narrowband** sensor is a *switch, not a meter*: OBDLab can only map it to a coarse stepped λ (~0.97 rich / ~1.03 lean about the 0.45 V threshold) — that is **not** a usable continuous λ for a meaningful perception-delta. A **wideband/UEGO linear** sensor reports a true λ (`normalized_obd_lambda = 1/Φ`, pump current `Ip ∝ λ−1`), which *is* usable. Era 1 (1990–2000) is narrowband-only; wideband A/F sensors are an Era 2 (2000–2010) feature.

**Sources:** `o2-logic/04_normalized-lambda-translation.md`, `o2-logic/08_wideband-pumping-current-logic.md`, `taxonomy/01_euro-emission-standards-eras.md`.

**Unblocks `T-OBDV2-ECU-PERCEPT-1`:** ⚠ **kill-switch guard pins itself** — `lambda_perception_delta` should be emitted as computable **only when `upstream_o2_type == WIDEBAND_LINEAR`** (or a commanded-λ PID is present). On narrowband-only vehicles the delta is coarse/non-discriminating and the channel must declare itself non-computable rather than emit a misleading value. This is the architect bound the task's kill-switch was waiting for.

---

## Q5 — On single-air-sensor engines (MAP-only or MAF-only), is any valid VE cross-check possible?

**Answer: No independent VE cross-check is possible with a single air sensor — it is circular.** VE validation needs **two independent air measurements**; with only one, the missing quantity is back-calculated *from* the present one, so VE cannot independently confirm anything (the audit's "VE pinned/circular"). The chunks give the concrete failure: on a **speed-density (MAP-only)** engine a vacuum leak produces **ΔTrim ≈ 0** (the "Speed-Density paradox" — MAP reads the true higher pressure, ECU adds matching fuel), so VE/trim is blind to it; the leak instead shows as reduced IAC counts and elevated idle MAP (~45 kPa vs healthy ~30). The substitute on single-sensor engines is the **MAF/MAP/TPS rationality cross-check** (P0068) + inferred-BARO, not VE.

**Sources:** `delta-relations/06_architecture-modifiers.md` (Speed-Density paradox), `pids-protocol/02_maf-map-tps-rationality-p0068.md`.

**Unblocks T-OBDV2-2…10:** any VE-based sensor-diagnosis spec must **gate on `air_metering_strategy`** — VE evidence is valid only for `DUAL_MAF_MAP_CROSSCHECK`; for MAP-only/MAF-only, route to rationality/IAC/MAP-at-idle, not VE.

---

## Q6 — How much of the 1990–2010 fleet supports fuel trims and Mode $06, and how trustworthy pre-2001?

**Answer: STFT/LTFT are core J1979 PIDs present on all OBD-II vehicles (US 1996+, EU Euro 3 ~2000+); bank-2 trims (`$08`/`$09`) exist only on 2-bank engines; Mode $06 is only standardized/portable on CAN (≈2008+).** Pre-OBD-II (pre-1996 US / pre-Euro-3 EU) there are no standardized PIDs at all. Pre-2001 OBD-II trims exist but are less trustworthy (pre-CAN maturity); Mode $06 pre-CAN is non-standardized / per-OEM (MID/TID hex varies).

**Sources:** `taxonomy/01_euro-emission-standards-eras.md` (era→sensor gating), `pids-protocol/01_mode06-freezeframe-nostart-method.md` (Mode 06 MID/TID), `fuel-trim/05_bank-to-bank-comparison.md` (per-bank PIDs).

**Unblocks `T-OBDV2-BANK-ASYM-1`:** ✅ **does not kill-switch, but bounds applicability** — per-bank trim is structurally available on **2-bank (V6/V8) OBD-II engines 1996+**; the channel is correctly gated by the existing applicability rule (emit only when two banks exist), with reduced confidence pre-2001. Inline engines have one bank and emit nothing here (as designed). For **Q8/Mode-06-dependent** specs, restrict to CAN-era (≈2008+) or accept per-OEM gaps.

---

## Q7 — What downstream-O₂ behaviour indicates a secondary-trim loop masking upstream drift, and is it scan-tool detectable?

**Answer: it is carried by the `downstream_trim_role` classification, not a raw post-cat waveform.** When the rear sensor is `SECONDARY_FUEL_TRIM` (drives a real rear trim loop), post-cat trim analytics run and P2096/P2099 are eligible — and an *in-tolerance* upstream λ agreement is only **weak** evidence of a healthy upstream sensor, because the rear loop may be masking drift (the detector down-weights agreement). When the rear sensor is `CATALYST_MONITOR_ONLY`, COMLab **suppresses** post-cat trim verdicts entirely. The role comes from DNALab/VINLab's emissions profile (mirrored on the OBD boundary), so the "signal channel" the audit flagged as missing is the **role field**, not a new PID.

**Sources:** `o2-logic/06_downstream-trim-suppression.md`, `o2-logic/02_upstream-vs-downstream-roles.md`, `o2-logic/05_bias-vs-real-truth-perception.md` (the down-weight caveat). Note `o2-logic/06` also corrects a doc bug: `SUPPRESS_POST_CAT_TRIM` is **not** a `TrimAnalyticsGate` value (O2-FU-2).

**Unblocks T-OBDV2-2…10:** the `downstream_trim_role`-driven suppression/down-weight is the consumer; no new signal channel is needed — closes the audit's "flag but no channel" gap by routing it through the existing role field.

---

## Q8 — Which Mode $06 monitor IDs discriminate catalyst/misfire/EVAP/O₂ faults, without per-OEM tables?

**Answer: the standard MID/TID test-value-vs-limit set discriminates well, but is only portable on CAN (2008+).** Concrete IDs from the wiki: Misfire Monitor **MID $A1 / TID $53** ("Incomplete"/all-zero = monitor aborted → security lock-out vs mechanical no-start); Fuel System Monitor **MID $81 / TID $01/$02** (value vs ±20/±25 % limit → lean/rich); **EGR Monitor TID $41** (e.g. 65,227 vs max 896 = stuck); MAF "fails to reach peak (< 40 × Disp. g/s at WOT)". The **"Incomplete/aborted" monitor state is itself diagnostic** — a pure DTC list cannot split a security lock-out from a mechanical no-start.

**Sources:** `pids-protocol/01_mode06-freezeframe-nostart-method.md`, `o2-logic/07_o2-dtc-families.md`.

**Unblocks T-OBDV2-2…10:** a Mode-06/no-start branch is viable as a **PROPOSAL** with DTCLab producer + COMLab fault_atlas reader, **CAN-era gated** (pre-CAN MID/TID are per-OEM — exclude or flag). New Mode-06 fields earn their place only via that named consumer.

---

## Q9 — What O₂ metrics separate a lazy/aged sensor from a biased one from a dead one?

**Answer: switching frequency / cross-counts, response time, and pin behaviour — already encoded as `O2FailureMode`.** Lazy/aged = `SLUGGISH`: cross-counts **< 8 / 10 s @ 2500 RPM**, switching freq **< 0.5 Hz**, rise/fall **> 100 ms** (may pass a static voltage check yet be slow). Biased = `STUCK_LEAN` (< 0.20 V) / `STUCK_RICH` (> 0.85 V) / `WRONG_CENTERLINE` (switches off-centre, e.g. 0.3–0.6 V). Dead = `DEAD`: no switching, flat ~0.45 V. Healthy = `NO_FAULT`: cross-counts ≥ 8 / 10 s @ 2500 RPM, warm + closed loop.

**Sources:** `o2-logic/03_failure-modes-taxonomy.md`, `o2-logic/01_sensor-types-and-physics.md`, `o2-logic/04_normalized-lambda-translation.md` (cross-count test).

**Unblocks T-OBDV2-2…10:** the discriminators are already the live `O2FailureMode` triggers — `sensor_fault` separability is realised by emitting the right failure mode, not by new fields. (A wideband constant-offset fault is the one gap → the two-stage `WIDEBAND_OFFSET` proposal, O2-FU-1.)

---

## Q10 — Will the product capture live PIDs (revive vs prune)?

**Already RESOLVED — `revive` (emitter role), `T-OBDV2-0`, owner-ratified 2026-06-08.** OBDLab emits typed perception channels; COMLab judges. The quarantine was a PID-less-corpus artefact, not a code defect. No further research needed; this answer is recorded for completeness.

---

## What this unblocks (architect summary)

| Gated task | Gating Qs | Verdict | Pins this research hands the architect |
|---|---|---|---|
| **T-OBDV2-ECU-PERCEPT-1** | Q1, Q4 | **Proceed** | (1) emit `lambda_perception_delta` only when `upstream_o2_type == WIDEBAND_LINEAR` / commanded-λ present (Q4 kill-switch guard); (2) the discriminator is bank-symmetry → consumer must read `total_trim_correction_delta_b2` (today an orphan); (3) TPS/IAT field gap — add only if the ECU checker consumes them. |
| **T-OBDV2-BANK-ASYM-1** | Q2, Q6 | **Proceed (no kill-switch)** | Per-bank trim is available on 2-bank OBD-II engines 1996+; asymmetry bound = banks differ by **> ±5 %** (the bank-match limit); reduced confidence pre-2001; applicability gate = two banks exist (as designed). |
| **T-OBDV2-2…10** | Q5, Q7, Q8, Q9 | **Authorable** | VE evidence valid only on dual-sensor engines (Q5); downstream masking handled by `downstream_trim_role` (Q7); Mode-06 branch is CAN-era-gated proposal (Q8); O₂ lazy/biased/dead already in `O2FailureMode` (Q9). |

Two doc-truth corrections surfaced (not in scope to fix here, logged): `SUPPRESS_POST_CAT_TRIM` is not a `TrimAnalyticsGate` value (O2-FU-2); the O₂-delta stress band is inconsistent (2500 vs 3500–4500 RPM, O2-FU-3).

## Sources

All answers cite chunk files under `4DLabV2/labs/obdlab/research/chunks/` (read in full this session): `ecu-diagnosis/{01,07}`, `fuel-trim/{03,04,05,06,09}`, `o2-logic/{01,03,04,05,06,07,08}`, `delta-relations/06`, `pids-protocol/{01,02}`, `taxonomy/01`, `truth-perception/02`. Question text from `docs/reference/audit_2026-06-03/4DLAB_CAPABILITY_AUDIT_AND_RESEARCH_QUESTIONS.md` OBDLab §.
