> **Context:** OBDLab PRD v2.0 (2026-06-10) · Module: OBDLab · Section 1 Summary · Parent document: PRD_OBDLab.md

## Section 1 — Summary

OBDLab is the **electronic-perception channel** of the 4D petrol diagnostic pipeline (the L5 live-PID layer). It accepts a raw dict of OBD-II PIDs plus a typed vehicle DNA view (`ObdLabDnaView`, 7 fields), runs a 7-step pipeline (PID ingestion → RPM bucketing → semantic consistency → VE computation → O2 normalisation → trim aggregation → analytics gating), and emits a 31-field `OBDLivePayload` that represents the **ECU's perception** of engine state. COMLab compares this perception against GASLab's chemistry ground truth.

The v2 rework (T-OBDV2-0 through T-OBDV2-11, 2026-06-08–10) revived OBDLab as a **pure emitter** after determining the >95% NO_FAULT result that prompted the quarantine review was a PID-less-corpus artefact, not a code defect. OBDLab emits its own channels — trims, normalised lambda, VE, perception deltas, sensor provenance — and does **not** produce fault-family verdicts. That cross-referencing and final root-cause verdict is COMLab's job (see `HLD_OBDLab.md` §1, §7).

Truth-vs-Perception framing unchanged: the ECU is **perception**; GASLab Brettschneider lambda is **ground truth**.

## Graph relations (explicit)

**PRD_OBDLab v2.0** SUPERSEDES **PRD_OBDLab v1.0** (2026-05-22)
**OBDLab** DESCRIBES **electronic-perception channel** (L5 live-PID layer, 7-step pipeline, 31-field payload)
**COMLab** CONSUMES **OBDLivePayload** (ECU perception vs GASLab chemistry ground truth)
**T-OBDV2-0..11** DESCRIBES **v2 revive-as-emitter rework** (PID-less-corpus artefact resolution)
