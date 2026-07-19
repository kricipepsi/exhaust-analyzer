> **Context:** OBDLab LLD v2.0 (2026-06-10) · Module: OBDLab · Section 14 freeze_frame_pids Forwarding Contract · Parent document: LLD_OBDLab.md

## 14. `freeze_frame_pids` Forwarding Contract

`OBDLivePayload.freeze_frame_pids` (default `{}`) is populated by **COMLab**
before the OBDLab call, from DTCLab freeze-frame data — OBDLab ferries it
through unchanged. OBDLab never reads DTCLab directly (no cross-lab import).

## Graph relations (explicit)

**freeze_frame_pids** DESCRIBES **passthrough channel** (populated by COMLab from DTCLab data)
**COMLab** CONSUMES **freeze_frame_pids** (writes before OBDLab call)
**OBDLab** CONSUMES **freeze_frame_pids** (ferries through unchanged, default {})
**OBDLab** GATED_BY **no cross-lab import from DTCLab** (isolation rule)
