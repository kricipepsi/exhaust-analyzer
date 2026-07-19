> **Context:** OBDLab PRD v2.0 (2026-06-10) · Module: OBDLab · Section 3 Background · Parent document: PRD_OBDLab.md

## Section 3 — Background

**Context.** OBD-II (ISO 15031 / SAE J1979) standardises real-time engine sensor access for all post-1996 petrol vehicles. Fuel trims (`STFT`, `LTFT`), manifold pressure, mass airflow, coolant temperature, intake air temperature, throttle position, and control module voltage together describe how the ECU is managing the engine. These are the ECU's perception signals — they can be correct or wrong, but they are always present.

**Why now.** The OBD standard is stable. The combination of `pydantic` v2 field validators and the `physical_sensor_bounds.json` drift guard means sensor boundaries can be enforced at ingestion and kept in sync with the wiki automatically. The v2 revive-as-emitter rework added 10 fields to the payload (21→31), widened trim bounds to the OBD rail (±127) to preserve sensor-fault signalling, replaced the legacy O2 failure taxonomy with a 4-value consumer-backed classification, and removed Physics Gate 3 (superseded by `FAULT_VE_SENSOR_SKEW` in the VE validity classifier).

**What recently became possible.** The 3-branch VE routing (dual MAF+MAP crosscheck, MAP-only speed-density, MAF-only) plus the DNA-first configuration model allows OBDLab to handle any petrol engine metering strategy without embedded lookup tables. MAF linearity monitoring (`w_theo`, `sensor_error_delta`) adds a two-point non-linearity check across idle and stress RPM bands. The guarded-emitters pattern (HLD §3) allows fields like `lambda_perception_delta` and `sensor_error_delta` to ship now with forward-registered COMLab consumers (HLD §7) without blocking on the Stage 4 COMLab rework.

## Graph relations (explicit)

**OBDLab PRD v2.0** DESCRIBES **v2 revive-as-emitter rework** (10 new fields 21→31, trim widening ±127, O2FailureMode taxonomy 4-value, Physics Gate 3 removed, MAF linearity)
**physical_sensor_bounds.json** GATED_BY **pydantic v2 drift guard** (auto-sync with wiki)
**VEEngine** ENUMERATES **3-branch VE routing** (DUAL_MAF_MAP_CROSSCHECK, MAP_ONLY_SPEED_DENSITY, MAF_ONLY)
**guarded emitters** DESCRIBES **lambda_perception_delta, w_theo, sensor_error_delta** (emit S2, consume S4)
