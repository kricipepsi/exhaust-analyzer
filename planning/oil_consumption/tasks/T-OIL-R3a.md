# T-OIL-R3a — GASLab→COMLab high-idle (L2) gas contract

### Goal ###

Add the high-idle (L2) gas snapshot to the GASLab→COMLab boundary so downstream
rules can use the low→high-idle delta. GASLab emits a high-idle gas block
(`hc/co/co2/o2/nox/λ`); COMLab's `GasLabPayload` mirrors it as **optional** fields
(typed JSON boundary — no cross-lab Python import). Done when `GasLabPayload`
accepts and round-trips a high-idle block and the GASLab emitter produces it, both
covered by tests. This is the precondition for R3b/R4/R5.

### Success criteria ###

- `labs/comlab/tests/unit/test_ingestion_high_idle.py::test_gaslab_payload_accepts_high_idle`
  passes — `GasLabPayload(**case_with_high_idle)` populates the new optional fields;
  a payload without them still validates (backward-compatible). Write failing first.
- `labs/gaslab/tests/...::test_emits_high_idle_block` passes — the GASLab
  output builder emits the high-idle fields for an L1+L2 run.
- Existing `comlab` + `gaslab` suites stay green (fields are optional → no break).

### Context ###

`comlab/comlab/schemas/ingestion.py:162` `GasLabPayload` carries a single snapshot
(`gas_hc`, `gas_co`, `gas_co2`, `gas_o2`, `gas_nox`, `lambda_chem`) — no high-idle.
The pipeline already distinguishes L1 idle vs L2 high-idle gas (CLAUDE.md "Pipeline
layers"), so GASLab has the L2 data internally; the gap is emitting it across the
boundary. House rule: COMLab mirrors the types it needs locally — define the
high-idle fields directly on `GasLabPayload`, do NOT import a GASLab type. Keep the
new fields **optional** (`| None = None`) so every existing single-snapshot case and
all current tests keep validating.

Proposed field names (mirror the existing `gas_*` convention):
`high_idle_hc: int | None`, `high_idle_co: float | None`,
`high_idle_co2: float | None`, `high_idle_o2: float | None`,
`high_idle_nox: int | None`, `high_idle_lambda: float | None`. Reuse the existing
`Field(ge=…, le=…)` bounds from the low-idle counterparts (cite the same line).

STRICT-ONLY: Load skills: none.

### Consumer (signal/noise) ###

- **Consumer:** the R3b shim PID resolver and the R4 (`MW-008`) + R5 (`MW-009`)
  rules — all in this pack. Fields + readers ship together → **PROPOSAL** default.
- **Code path:** `integration_shim` `_PID_SOURCES`/`_build_observation` (R3b) read
  `high_idle_*` from the mirrored `GasLabPayload`; the PCV/turbo rules' high-idle
  evidence rows consume the resolved PIDs. Until R3b lands, the fields are inert —
  this row is explicitly the first half of a field+reader proposal pair.

### Deliverables ###

1. `labs/comlab/comlab/schemas/ingestion.py` — add the 6 optional
   `high_idle_*` fields to `GasLabPayload` with bounds + wiki citations.
2. `labs/gaslab/<output builder>` — emit the high-idle block (coder pins the
   exact file from the gaslab contract; READ-NARROW the gaslab output module).
3. `labs/comlab/tests/unit/test_ingestion_high_idle.py` (CREATE).
4. `labs/gaslab/tests/...` (CREATE/EXTEND) — emitter test.

### Files to touch ###

- `labs/comlab/comlab/schemas/ingestion.py` (MODIFY)
- gaslab output builder (MODIFY — coder pins path)
- `labs/comlab/tests/unit/test_ingestion_high_idle.py` (CREATE)
- gaslab emitter test (CREATE/MODIFY)

### Out of scope ###

No shim resolver changes (R3b). No new rules (R4/R5). No cross-lab Python import —
boundary is JSON only. Do not widen the live `chemical_state` enum. Do not make the
fields required. GRAPH GUARDRAIL: no graphify / graph rebuild.

### Verification ###

```bash
cd /sessions/<vm>/mnt/4DLab
ruff check labs/comlab/comlab/schemas/ingestion.py
pyright labs/comlab/comlab/schemas/ingestion.py
python3.14 -m pytest -x -q labs/comlab/tests/unit/test_ingestion_high_idle.py
python3.14 -m pytest -q labs/comlab labs/gaslab
```

All steps must pass.

### Progress hook ###

PROGRESS.md `T-OIL-R3a`: Status=done, Files changed=4, Verification="GasLabPayload mirrors optional high-idle gas; GASLab emits L2 block; both suites green; fields backward-compatible"
