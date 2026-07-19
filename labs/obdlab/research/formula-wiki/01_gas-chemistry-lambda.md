# Formula wiki — Gas chemistry & lambda (GASLab)

> Each entry: **Formula** · **ASCII** (where it helps) · **Logic** · **Connected case** · **Lab** · **Source**.
> Formulas here are extracted from READABLE sources. Brettschneider/vsum display forms
> were stripped in the Vol1/Vol7 exports but survive in `wikiResearch.md`/prose — sourced
> accordingly, not reconstructed. Truly-missing forms are in `PENDING_STRIPPED_FORMULAS.md`.

---

## F-GAS-01 · Brettschneider lambda (chemical λ from 5-gas)

**Formula**
```
        [CO2] + CO/2 + [O2] + NOx + (Hcv/4 − Ocv/2)·([CO2] + [CO])
 λ =  ───────────────────────────────────────────────────────────────
        (1 + Hcv/4 − Ocv/2) · ([CO2] + [CO] + K·[HC])
```
Hcv = atomic H/C ratio of fuel (~1.85 petrol); Ocv = O/C ratio; K = HC conversion factor.

**ASCII — mixture number line**
```
 rich  <-----------------|----------------->  lean
 λ:   0.74      0.90    1.00     1.10      2.12
       CO high          stoich           O2 high
```

**Logic** Mass-conservation truth: unlike an O₂ sensor (ion concentration only),
Brettschneider counts all C- and O-bearing species, so it sees a rich engine even when
the O₂ sensor is "fooled" (e.g. misfire passing raw O₂). This is the ground-truth half
of truth-vs-perception (PRD §5).

**Connected case** truth-perception/03 N-002: ECU λ_obd≈1.05 (P0171 lean) but Brettschneider
λ_chem≈0.84 → exposes the silicone-poisoned-sensor "liar."

**Lab** GASLab (producer of `lambda_chem`). **Source** wikiResearch.md (full LaTeX);
referenced by Vol1/Vol7 (display stripped there).

---

## F-GAS-02 · Stoichiometric reference

**Formula**
```
 AFR_stoich(petrol) = 14.7 : 1  (by mass)   <->   λ = AFR_actual / 14.7 = 1.000
 λ < 1.0  rich (excess fuel)     λ > 1.0  lean (excess air)
```
**Logic** The fixed target all closed-loop fuel control aims at; the denominator that
turns an AFR into λ. **Connected case** every closed-loop case. **Lab** GASLab / OBDLab.
**Source** Vol2/Vol3/master_fuel_trim_guide (readable).

---

## F-GAS-03 · 5-gas sample validity (vsum + dilution)

**Formula**
```
 vsum = HC + CO + CO2 + O2 + NOx        (key constituents, % vol basis)
 VALID:        14.0% <= vsum <= 18.0%
 dilution fail: CO + CO2 <= 6.0%
```
**ASCII**
```
 vsum:  |----dilution----|====VALID====|----ambient/leak----|
        0              14.0          18.0                 ~20.9 (O2 air)
```
**Logic** Guards every Δgas/λ from a leaking probe or cracked tailpipe drawing ambient
air (false-lean). At curb idle, pulse reversion dilutes; at 2500 RPM positive exhaust
pressure purifies the sample. **Connected case** delta-relations/08; any low-idle false-lean.
**Lab** GASLab (ingestion gate). **Source** Vol7 (thresholds in prose; vsum display
equation stripped → PENDING list).

---

## F-GAS-04 · Chemical efficiency score (carbon oxidation)

**Formula**
```
 Chemical_Efficiency = CO2 / (CO2 + CO)     healthy -> near 1.0 (>~0.95)
```
**Logic** Fraction of carbon fully oxidised to CO₂; a low value means fundamental
combustion failure (pumping loss, misfire, bad timing) regardless of trims. **Connected
case** truth-perception/04; GAS-IMIS / GAS-FC misfire rows (Vol7). **Lab** GASLab → COMLab.
**Source** Vol1 (prose; standard ratio — flagged readable-prose-derived).

---

## F-GAS-05 · Oxygen-usage factor (misfire vs rich discriminator)

**Formula**
```
 Oxygen_Usage ~ O2 / CO   (qualitative, Vol1)
   high O2 + high HC/CO  -> MISFIRE (both reactants unburned)
   high CO + ~0 O2       -> pure RICH over-fuelling
```
**Logic** Resolves the "rich AND lean at once" paradox: both reactants present =
combustion never happened = misfire, not a mixture error. **Connected case** o2-logic/07
misfire-lean caveat; GAS-LMIS-001 (Vol7). **Lab** GASLab → COMLab fault_atlas.
**Source** Vol1 (prose).
