# Formula wiki — Fuel trim (OBDLab / COMLab)

## F-FT-01 · Total fuel trim

**Formula**
```
 total_trim = STFT + LTFT          healthy: |total| <~ ±10%   (DTC at ±18..±25)
 sign:  + = lean (ECU adding fuel)     − = rich (ECU pulling fuel)
```
**Logic** The single scalar the engine evaluates; STFT is the fast O₂-driven correction,
LTFT the learned offset. **Connected case** fuel-trim/01; P0171/P0172 routing. **Lab**
OBDLab (emit) → COMLab fault_atlas. **Source** master_fuel_trim_guide / Vol3 (Vol3 display
stripped; standard form).

---

## F-FT-02 · Per-bank total trim + bank divergence

**Formula**
```
 TFT_B1 = STFT_B1 + LTFT_B1        TFT_B2 = STFT_B2 + LTFT_B2
 bank-specific fault  <=  |TFT_B1 − TFT_B2| >= 20%   (dual-bank engines)
```
**ASCII**
```
 B1 +50% ┤█████████      injector driver OPEN (B1)
 B2  +2% ┤█              normal           -> asymmetric => ECU/bank-local fault
```
**Logic** Symmetry vs asymmetry is the strongest internal-vs-external ECU tell. **Connected
case** ecu-diagnosis/03 injector-driver; chunks/fuel-trim/05. **Lab** OBDLab
`trim_vector_aggregator` → COMLab. **Source** OBD_ImplProp.md §2.B (readable).

---

## F-FT-03 · Trim delta (low idle → stress idle)

**Formula**
```
 ΔTFT = TFT_low − TFT_stress
   vacuum leak:        ΔTFT >= +15%  (high +trim at idle recovers at RPM)
   fuel restriction:   ΔTFT <= −15%  (normal idle, spikes +trim under load)
```
**ASCII**
```
 trim
 +40 ┤●            ● vacuum leak (improves)
     │  ╲        ╱   fuel restriction (worsens)
  +5 ┤   ●────●
     └── idle ── 2500 RPM ──>
```
**Logic** Direction of change across the speed step separates faults identical at one
point. **Connected case** delta-relations/01–05; fuel-trim/16. **Lab** COMLab delta engine
(FU-2). **Source** FuelTrimW.md (readable LaTeX).

---

## F-FT-04 · OBD-I ↔ OBD-II trim scale conversion

**Formula**
```
 Trim% = ((Value − 128) / 128) × 100%      (raw 0–255 byte, 128 = 0% baseline)
```
**Logic** Normalises legacy raw-byte trim to percent for the 1990–2010 fleet. **Connected
case** pids-protocol legacy ingest (DR-FU-1). **Lab** OBDLab ingestion. **Source**
FuelTrimW.md (image-locked in HTML, readable here).
