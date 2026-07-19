# TRIAL — single-case run: oil-burn (oil_consumption) differential

**Authored:** 2026-06-21 (architect, Cowork). **Purpose:** one end-to-end trial of the whole 4DLab chain on the oil-burn case, to observe the full diagnostic data flow + the 5-culprit differential. Not a coder task — a trial-run recipe.

## The case
- **Symptom (SymptomLab):** `oil_consumption` + one sub-symptom: `blue_smoke_on_cold_start_clears` *(→ valve-stem seals)* · `blue_smoke_under_acceleration` *(→ rings/turbo)* · `oil_loss_no_visible_smoke` *(→ PCV / head-gasket breach)*.
- **5 culprits (KG differential, `comlab/tests/unit/test_oil_consumption_kg.py`):**
  1. `oil_consumption_worn_piston_rings`
  2. `oil_consumption_worn_valve_stem_seals`
  3. `oil_consumption_pcv_stuck_open`
  4. `oil_consumption_head_gasket_oil_breach`
  5. `oil_consumption_turbo_turbine_seal_leak`

## Data flow
```
User ticks oil burn ─► SymptomLab: oil_consumption + sub-symptom + DNA(engine, induction, mileage, oil hist)
GASLab : gas sample ─► chemistry (oil burn ≈ elevated HC; weak separator)
OBDLab : trims / PIDs (weak for oil)
DTCLab : usually no DTC
        └────────────► OrchestratorInboundRequest
COMLab : aggregator.process ─► symptom_router ─► fault_atlas ─► 5-way oil_consumption differential
        ─► ranked top-N  (separation driven by sub-symptom + DNA, NOT gas/OBD)
```

## What must be done (order)
1. **Verify reachability FIRST.** Read `registry/tests/test_oil_no_kg_on_live_path.py` — the 5-node oil KG is held **off** the live registry path. Confirm whether `composition.diagnose()` surfaces the 5 culprits today (via SymptomLab differential) or whether that differential needs wiring. If unreachable → that is the trial's first finding; wire it before expecting a 5-way output.
2. **Build one `raw_inputs` dict** (the input bundle): gas readings (elevated HC, near-stoich/slightly-rich λ), OBD trims (mild), `dtcs=[]`, `symptom=oil_consumption` + chosen sub-symptom, VIN/DNA (e.g. high-mileage, induction type to enable/exclude turbo culprit). Mirror the column shape in `registry/corpus_curated.csv` / `harness/case_mapper.py`.
3. **Run** in the Windows `.venv-wired` (PowerShell, NOT Git Bash/sandbox — `.sandbox-py` is Linux):
   ```powershell
   cd C:\Workspace\apps\wired
   $py = "..\..\labs\comlab\.venv-comlab\Scripts\python.exe"   # or .venv-wired per WIRED_PROGRESS
   & $py -c "from wired.composition import diagnose; import json; print(json.dumps(diagnose(RAW_INPUTS), default=str, indent=2))"
   ```
   (or add the case to `harness/run_cases.py` and run just that row.)
4. **Inspect:** final verdict + the 5-way differential ranking + the Jaeger trace (`_jaeger/`) for per-stage evidence.

## Caveats for this trial (current reality)
- New COMLab consumers (BANK/ECU/VE/FUELSYS/DELTA/O2OFFSET/NOSTART) are **default-off** → not exercised.
- `apps/wired` is stale at `ChemicalSignature==30` (labs at 34) → refresh before trusting boundary fidelity.
- oil_consumption separation is symptom/DNA-driven; gas+OBD give weak signal → expect a ranked differential, not one high-confidence verdict.
