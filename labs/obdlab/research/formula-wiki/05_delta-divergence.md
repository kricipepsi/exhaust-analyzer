# Formula wiki — Delta & divergence engine (COMLab)

## F-DLT-01 · Single-speed divergence ("digital lie")

**Formula**
```
 δ = λ_obd − λ_chem        (how far ECU perception departs from gas truth, at one speed)
```
**Logic** δ≈0 = ECU honest (physical fault); δ wide = internal-ECU "liar." **Connected
case** wikiResearch cross-delta; ADC-mux. **Lab** COMLab perception_contradiction.
**Source** wikiResearch.md / DataFlow.md (readable).

---

## F-DLT-02 · Cross-delta (how the lie shifts with RPM)

**Formula**
```
 Δδ = δ_stress − δ_low = (λ_obd,s − λ_chem,s) − (λ_obd,l − λ_chem,l)
```
**ASCII — fault fingerprints**
```
 Δδ ≈ 0 wide both speeds   -> ADC mux (loop permanently broken)
 Δδ ≈ +0.10 (rises at RPM) -> capacitor leak (HF ripple worse at RPM)
 Δδ ≥ +0.16 in one cell    -> EPROM bit-flip (localised to a speed/load cell)
```
**Logic** The *shape* of the divergence across speed fingerprints the ECU failure mode.
**Connected case** ecu-diagnosis/02,06,07; EP-ECU-07 bit-flip. **Lab** COMLab delta engine.
**Source** wikiResearch.md (readable LaTeX).

---

## F-DLT-03 · State deltas (trim / lambda / airflow)

**Formula**
```
 Δtrim          = trim_high − trim_low
 Δλ_chem        = λ_chem,high − λ_chem,low
 Δairflow_eff   = ve_high − ve_low        (gated on maf_status == VALID)
```
**Logic** The vector the fault-atlas decision table routes on (vacuum leak vs fuel
restriction vs MAF vs lazy-O₂). **Connected case** DataFlow §3 decision table; EP-COM-01.
**Lab** COMLab `delta_engine.py`. **Source** DataFlow.md (readable code/LaTeX).

---

## F-DLT-04 · Two-speed gas deltas (per gas)

**Formula**
```
 Δgas = gas_2500 − gas_idle   for HC, CO, CO2, O2, NOx, λ
   vacuum/unmetered faults -> ATTENUATE at 2500 (dilution + vacuum drop)
   speed-dependent wear     -> INTENSIFY  at 2500 (rings, EVAP purge, flat cam, no-EGR NOx)
```
**Logic** The chemical complement to ΔTrim; sign per gas separates improve-vs-worsen
faults. **Connected case** delta-relations/07 (25 GAS-* matrix). **Lab** GASLab frame →
COMLab delta engine. **Source** Vol7 (numeric matrix readable; band = 2500 RPM ⚠ reconcile).
