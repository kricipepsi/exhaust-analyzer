# labs/obdlab — OBDLab v2 (Stage 2)

**Role:** OBD **perception** channel — STFT/LTFT trim, `lambda_perception_delta`, downstream-O₂
masking, Mode $06 discriminators. Truth-vs-perception: the ECU is *perception*, gas chemistry is truth.
**Build stage:** 2. **First a scope decision:** revive vs quarantine (>95% NO_FAULT on this corpus).
Prune any field with no signal channel under signal/noise.
**Code origin (Q-A / D1):** fork of v1 `OBDLab/`; v1 archived once this v2 lab is built and green.
**Boundary:** no cross-lab Python imports — consumers mirror the types locally.

**Re-homed here:** bank-asymmetry (from GASLab T-GV2-14, voided) — per-bank **STFT/LTFT bank1 vs
bank2** is the natural channel; consumer = COMLab fusion. See `../../DECISIONS.md`.

_Status: built + green (Stage 2 closed 2026-06-15). Tested and verified._
