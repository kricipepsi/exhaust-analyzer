# T-AUD-4l — authoring sidecar (Windows Cowork, 2026-11-05)

### Verified context ###
1. **F-D2-2 holds** at the 4k tip: the D2 probe fails (`metadata` Field required); `VehicleDNA` exists unused. Observed.
2. **Rehearsal** (`apply_fix.py`, restored): the probe passes; comlab 526 → 530; registry, wired, ui unchanged; mutants
   4/1/1 failed. Observed.

### Rulings and the tradeoff that lost ###
- Accept `vehicle_dna` beside the legacy `metadata` through a before-validator; the composition keeps sending
  `metadata`. Lost: switching the composition to `vehicle_dna` (a wider change across every reader of `metadata`).
- Both shapes in one request are refused. Lost: "metadata wins" (silent precedence hides a mismatched producer).
- Plan NONE, difficulty 3. The handoff had planned REQUIRED / 4 for 4l with the `gas_lab_output` residual inside; the
  residual moved to 4e, and what is left is one field and one validator with every mapping ruled and rehearsed.
  Lost: the plan gate CLAUDE.md asks for new constructions (an additive adapter here, measured first). Code row, so a
  second review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | new 4 passed; comlab `530 passed, 4 skipped, 2 errors` (base 526) |
| step 2 | RAN | registry `5 failed, 502 passed, 4 deselected`; wired 65; ui 38 (base and fix) |
| step 3 | RAN | `git status --porcelain` empty after the suites |
| step 4 | RAN | D2 probe: base `1 failed`, fix `1 passed` |
| step 5 | RAN | ruff `All checks passed!` on the rehearsed fix |

### Exclusivity ###
No other implementer runs. T-AUD-11 follows.

### Progress hook ###
T-AUD-4l: COMLab accepts vehicle_dna at the top level (the binding inbound contract); metadata is derived from it.

### Cold read ###
own pass 2026-11-05: P1-P4 measured · literals found once (`    metadata: SessionMetadata`, `class VehicleDNA`,
`class OrchestratorInboundRequest`, the probe name) · counts: comlab 526 + 4 = 530 · traceability: criteria 1-4 →
steps 1-5 · no finding. cold read: skipped (the second review covers the code).

### Correction history ###
(none)
