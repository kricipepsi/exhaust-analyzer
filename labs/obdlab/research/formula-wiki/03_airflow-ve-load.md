# Formula wiki — Airflow, volumetric efficiency & load (OBDLab)

## F-AIR-01 · Volumetric efficiency (VE)

**Formula**
```
            maf · R_GAS · IAT_K
 VE(%) = ───────────────────────────────────────────── · 100
          map_kpa · (rpm/60) · (displacement/2) · MM_AIR
```
R_GAS = specific gas constant for air; IAT_K = intake air temp (K); MM_AIR = molar mass
of air.

**Logic** The engine as an air pump: actual inducted mass ÷ theoretical mass. NA idle
healthy ≈ 75–90 %. Internal-ECU faults distort it: VE<50 % at idle w/ MAP>45 kPa =
collapsed 5 V rail / blown ground; VE>90 % at idle = capacitor-leak ripple.
**Connected case** ecu-diagnosis/06 (FAULT_VE_IDLE_COLLAPSE); N-009 MAF under-report.
**Lab** OBDLab `ve_engine.py`. **Source** OBD_ImplProp.md §2.A / wikiResearch.md (readable LaTeX).

---

## F-AIR-02 · Theoretical airflow (speed-density)

**Formula**
```
            η_V · V_disp · P_manifold · RPM
 W_theo = ──────────────────────────────────
                 120 · R · T_intake
```
**Logic** Model airflow from speed-density to sanity-check the reported MAF/MAP without
a snap-throttle test. **Connected case** EP-OBD-11; dirty-MAF non-linearity. **Lab**
OBDLab → COMLab. **Source** AddObdFields.md (readable LaTeX).

---

## F-AIR-03 · Sensor calibration-error delta

**Formula**
```
 ΔSensor_error = |Sensor_2500 − W_theo_2500| − |Sensor_750 − W_theo_750|
   ≈ 0           sensor scales linearly with demand
   far from 0    calibration drift (dirty MAF hot-wire)
```
**Logic** A MAF accurate at 750 RPM but wrong at 2500 RPM only shows up as a *delta* of
the model-vs-sensor error across the two states. **Connected case** delta-relations;
GAS/MAF under-report. **Lab** COMLab delta engine. **Source** AddObdFields.md / DataFlow.md.

---

## F-AIR-04 · Calculated engine load (J1979, PID 0x04)

**Formula**
```
                 Current Airflow        BARO @ sea level
 Calc_Load(%) = ───────────────────  ·  ────────────────── · 100
                 Peak Airflow @ SL       BARO_ambient
```
**ASCII — load vs throttle**
```
 load% 100 ┤            ●  (must hit ~100% at WOT, any altitude)
        70 ┤        ╱
        20 ┤●──── idle
           └ throttle ──────────> WOT
```
**Logic** Altitude-corrected (BARO term) so WOT ≈100 % regardless of elevation; stall at
70–80 % under full throttle = airflow restriction or MAF under-report. **Connected case**
EP-OBD-IN-01; N-012 restricted muffler. **Lab** OBDLab field → COMLab fault_atlas.
**Source** AddObdFields.md (readable). *Absolute Load (0x43) = VE-proportional, not BARO-corrected.*

---

## F-AIR-05 · MAF idle / peak rules of thumb

**Formula**
```
 idle MAF (g/s)  ≈ engine displacement (L)        (3.0 L  -> ~3.0 g/s at idle)
 WOT peak MAF    must reach rated max; misfire/restriction proxy:  MAF < 40 × Disp(L)
```
**Logic** Quick rationality bounds for the MAF without a flow bench. **Connected case**
pids-protocol/02 rationality; Vol4 MAF "fails to reach peak." **Lab** OBDLab rationality
gate. **Source** Vol2 MD4 / Vol4 (readable; `$<40×Disp$` LaTeX survives in Vol4).
