# Jaeger Demo Runbook — 5FR Oil-Burn Simulation

Show the five oil-consumption cases on the Citroën **5FR** flowing through the diagnostic
pipeline as **traces in Jaeger**, with the post-cat fuel-trim (B1S2) step that splits the
hardest cases. The simulation is standalone — it does **not** need the decoder fix or the
real labs, so it runs today.

---

## 1. Prerequisites (one-time)

- **Jaeger v2 running** (you already have it): `jaeger.exe` → UI at http://localhost:16686, OTLP gRPC on 4317.
- **OTel libraries** in the wired venv (the runner installs them if missing):
  ```powershell
  C:\Workspace\.venv-wired\Scripts\python.exe -m pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc
  ```

## 2. Run it (one command)

```powershell
cd C:\Workspace
.\planning\sim\run_sim_traced.ps1
```

This sets the OTLP env, runs the simulation, prints the 5/5 routing table + demand ranking,
writes `oil_burn_5fr_results.json`, flushes spans to Jaeger, and opens the UI.

*(Data only, no Jaeger:* `C:\Workspace\.venv-wired\Scripts\python.exe planning\sim\oil_burn_5fr_sim.py`*)*

## 3. What you'll see in Jaeger

- **Service:** `wiredv2-oil-case` → **Find Traces** → **5 traces**, one per case (`oil_case_*`).
- Each trace is a 4-span tree:
  ```
  oil_case_<id>            (case.vin, case.expected/predicted_fault_code, case.match_status, case.demand_score)
    ├─ gas_state           (gas.hc_low/high, gas.lambda_low/high, gas.chemical_state)
    ├─ post_cat_trim       (obd.stft_b1s2, obd.ltft_b1s2, obd.dfco_b1s2, obd.post_cat_signature)
    └─ verdict             (fault.code, fault.family, fault.name, fault.confidence)
  ```
- Click a trace → expand the spans → read the attributes. The story is in `post_cat_trim`:
  it's what turns an ambiguous gas reading into a specific fault.

## 4. The case to feature (most demanding)

Demand ranking from the run (highest = hardest, best showcase):

| Demand | Case | Trace to open | Why it's the showcase |
|---|---|---|---|
| 4.0 | **Turbo turbine-seal (MW-009)** | `oil_case_turbo_turbine-seal_leak` | combustion looks perfect (λ≈1.00, clean upstream) yet it's burning oil — only `post_cat_trim` (DFCO_NEGATIVE) reveals it |
| 4.0 | **PCV stuck open (MW-008)** | `oil_case_pcv_stuck_open` | the **divergent split**: upstream trim +, downstream B1S2 − — visually dramatic |
| 3.5 | Worn rings (MW-001) | `oil_case_worn_piston_rings` | FIXED_NEGATIVE B1S2 + old cross-lab conflict |
| 2.0 | Valve seals (MW-002) | `oil_case_worn_valve_stem_seals` | TRANSIENT_NEGATIVE B1S2 |
| 1.0 | Head gasket (MW-003) | `oil_case_blown_head_gasket` | gas + ECT alone |

**Suggested demo:** open the **turbo** trace, show `gas_state` (stoich, healthy-looking), then
`post_cat_trim` (DFCO_NEGATIVE) → `verdict` MW-009. The punchline: gas chemistry alone would
miss it; the downstream fuel-trim is the tell.

## 5. Troubleshooting

- **No traces in UI:** confirm Jaeger is up (UI loads), the runner printed `Jaeger: ONLINE` and
  `[trace] spans flushed to Jaeger.`, and you searched the `wiredv2-oil-case` service (not the default).
- **`opentelemetry SDK not installed`:** run the pip line in §1.
- **Wrong endpoint:** the sim defaults to `localhost:4317`; override with
  `$env:OTEL_EXPORTER_OTLP_ENDPOINT="http://<host>:4317"` before running.

> This visualizes the **simulation**. The real `run_case.py` emits the same span shape but needs
> **T-VIN-FIX-3** (decoder) before it decodes the VIN end-to-end.
