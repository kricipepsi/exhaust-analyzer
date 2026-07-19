# Formula wiki — O₂ / lambda translation & catalyst (OBDLab / GASLab)

## F-O2-01 · Wideband pumping-current sign → λ

**Formula**
```
 Ip > 0  -> LEAN (O2 pumped out)     Ip = 0 -> λ=1.000     Ip < 0 -> RICH (O2 pumped in)
```
**ASCII — narrowband vs wideband**
```
 NB voltage:  0.1V ──┐_┌──┐_┌──  (switches across stoich only)
 WB current:  ──/────0────\──     (linear λ ≈ 0.7 .. 1.3 via Ip)
```
**Logic** Wideband quantifies λ over a range (Ip), narrowband only flags richer/leaner.
A drifted Ip reference reads λ=1.0 while the engine is lean → WIDEBAND_OFFSET.
**Connected case** o2-logic/08; N-015 wideband ref drift. **Lab** OBDLab `o2_normalizer`.
**Source** Vol2 MD2 (concept readable; mA cells stripped).

---

## F-O2-02 · Lambda-delta vector (perception gap)

**Formula**
```
 Δλ = λ_obd − λ_chem
   = 0   calibrated     > 0  engine leaner than ECU thinks (Rich-Blind)
                        < 0  engine richer than ECU thinks (Lean-Blind)
```
**Logic** Quantifies the "liar/blind" gap at the L3 matrix. **Connected case**
truth-perception/02; N-002 Δλ≈+0.21. **Lab** COMLab perception_contradiction.
**Source** Vol1 (numbers in case tables; prose symbols stripped).

---

## F-O2-03 · Catalyst OSC switching ratio (P0420)

**Formula**
```
 switch_ratio = downstream_switch_freq / upstream_switch_freq
   healthy: << 1   (rear flat, cat stores O2)     P0420/P0430 when ratio -> 1:1
 (variant) TI_cat = σ(V_down) / σ(V_up)           degraded when -> 1
```
**ASCII**
```
 up   ┌┐┌┐┌┐┌┐  (fast switching)
 down ───────   healthy (flat)      down ┌┐┌┐┌┐  failed (mirrors up)
```
**Logic** A healthy cat's cerium washcoat damps O₂ swings → flat rear sensor; when OSC
is gone the rear mirrors the front. **Connected case** EP-CAT-01; GAS-COV-001. **Lab**
GASLab/catalyst → COMLab. **Source** master_catalyst_guide.md / O2logic.md / Vol2 MD7 (readable).

---

## F-O2-04 · Catalyst field-test thresholds

**Formula / rule**
```
 backpressure:  idle <= 1.5 psi ;  2500 RPM <= 3.0 psi  (above => substrate restriction)
 IR Δtemp:      outlet − inlet >= 20 °C  => converting ;  outlet <= inlet => dead
 misfire rate:  > 1% of combustion events => catalyst meltdown boundary (>1000 °C)
```
**Logic** Physical confirmation before condemning a converter; the 1 % misfire rule is
the Type-A monitor calibration boundary. **Connected case** EP-CAT-03/04; GAS-IMIS misfire
→ cat thermal threat. **Lab** catalyst → COMLab. **Source** master_catalyst_guide.md (readable).
