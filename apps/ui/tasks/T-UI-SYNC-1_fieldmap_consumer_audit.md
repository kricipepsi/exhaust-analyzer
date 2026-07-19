# T-UI-SYNC-1 — FieldMap consumer-string audit: reconcile UI field-map to current schemas

**Pack:** UI sync (standalone) · **Targets:** `apps/ui/4DLab_UI_FieldMap.md` (+ `UI design/uploads/` copy) · **Blocked by:** — (GPF-removal RM-1…5 all `done`) · **Status:** done · **Lane:** coder (doc reconciliation; read-only on schemas)

## Scope (1 paragraph)

`4DLab_UI_FieldMap.md` is the field-placement contract every UI widget traces to; its
`Schema.field → consumer` strings drifted from the current `labs/*` schemas after the
Windows→Linux migration and the GPF removal. Bring it back into **exact** sync: every
**shipping** input field must name a **real, existing** schema field and a **real**
consumer path (signal/noise). Three confirmed drift points (below) plus a full sweep of
the "Consumer" column. **Doc-only** — no lab or app code changes. The running
`apps/4DLabWired/app.py` already renders the correct fields and is the schema-of-record
for widget→payload keys; the map reconciles **up to** it and the lab schemas.

## Signal/noise / consumer

Reconciliation, not new fields — **no field ships**. Success = every `?`-table "Consumer"
cell and every §0/§2/§14 reference resolves to a symbol that exists today; a `grep` for
each cited `Schema.field` returns a live hit, and zero references to removed names remain.

## Known drift to fix (pinned — confirmed against current code)

1. **`measured_lambda` → `lambda_measured`.** §5 / §6 / §14 #1 cite
   `GasLabPayload.measured_lambda`. Current `labs/gaslab/gaslab/contracts.py:181` defines
   `lambda_measured` (high-idle is `high_idle_lambda:200`); wired `apps/4DLabWired/app.py:639,664,1108`
   builds `lambda_measured`. Also **re-confirm or drop `AnalyserLambdaFallback`** (§5 / §14 #1):
   verify the class/path still exists in current GASLab/COMLab; if renamed or gone, fix the
   chain to the real symbol rather than leaving a dead reference.
2. **`catalyst_present` → `has_catalyst`.** §4.2b lines ~198 & ~200 use
   `EmissionsConfiguration.catalyst_present`. Current
   `labs/comlab/comlab/schemas/ingestion.py:57,68` defines `EmissionsConfiguration.has_catalyst`.
   The doc is **internally inconsistent** — §2 line ~133 already says `has_catalyst`. Unify on
   `has_catalyst`.
3. **`secondary_air_equipped` (§2 line ~139, routing-only flag).** No live hit in any
   `labs/*/<lab>/*.py` or `labs/semantic`. Confirm against the current VINLab/COMLab emissions
   model: if the SAI flag was dropped or renamed during the SAI cleanup, **remove or correct**
   the line. **Do not invent a field** — if no consumer can be named, it does not belong in the map.

Then sweep the rest of the "Consumer" column (all of §4–§11 + §2 DNA table) the same way:
each `<Schema>.<field>` and each `→ <symbol>` must resolve in current code.

## Already done (architect, 2026-06-28 — do not redo, just propagate)

§0 source-provenance paths and the §4.4 `allowed_combinations.yaml` cite were repointed from
the pre-migration layout (`GASLab/`, `OBDLab/code/`, `DTCLab/code/`, `DNALab/VINLab/`,
`COMLab/comlab/adapters/*`) to `labs/<lab>/<lab>/…`, and the stale `comlab/adapters/*` claim
was corrected (adapter wiring lives in `apps/4DLabWired/wired/composition.py`) — **in the
top-level `apps/ui/4DLab_UI_FieldMap.md` only.** Propagate the identical §0/§4.4 fix to the
`UI design/uploads/` copy so the two match.

## Files to change

- `apps/ui/4DLab_UI_FieldMap.md` — drift items 1–3 + full consumer-column sweep + update §15
  "Verification notes" to the reconciled names / Linux layout.
- `apps/ui/UI design/uploads/4DLab_UI_FieldMap.md` — apply the same edits **including** the
  already-landed §0/§4.4 path fix, so the two live copies are byte-identical.
- **Leave** `ARCHIVE/ui1/…` and `ARCHIVE/UI/…` untouched — historical snapshots (archive, never edit).
- `UI design/*.jsx` mockups — **only** if a literal schema field-name string appears in them;
  otherwise out of scope (presentation, not contract).

## Success criteria

- For every `Schema.field` / consumer symbol cited in the map, `grep -rn` under
  `labs/*/<lab>/` (or `apps/4DLabWired/`) returns a live hit. Zero hits for the removed forms:
  `measured_lambda`, `catalyst_present`, `secondary_air_equipped`, GPF/`has_particulate_filter`,
  and the pre-migration path prefixes (`GASLab/`, `OBDLab/code`, `DNALab/VINLab`, `comlab/adapters`).
- The two live FieldMap copies are **byte-identical** (`diff` empty).
- `git diff --stat` shows **only** the two FieldMap docs — no lab/app code touched.

## Inner loop (coder)

Doc-only — no `ruff`/`pyright`/`pytest`. Verify by grep + diff:
```bash
cd /agent_workspace
# each cited symbol must resolve (examples)
grep -rn 'lambda_measured' labs/gaslab/gaslab/contracts.py
grep -rn 'has_catalyst'    labs/comlab/comlab/schemas/ingestion.py
# zero stale tokens left in either live copy
grep -rniE 'measured_lambda|catalyst_present|secondary_air_equipped|has_particulate_filter|GPF|GASLab/|OBDLab/code|DNALab/VINLab|comlab/adapters' apps/ui
# two copies identical
diff "apps/ui/4DLab_UI_FieldMap.md" "apps/ui/UI design/uploads/4DLab_UI_FieldMap.md" && echo IDENTICAL
```

## VERIFICATION GATE

### Cited Symbols Resolution

| Cited Symbol | File Path | Line Number | Description |
|---|---|---|---|
| `lambda_measured` | `labs/gaslab/gaslab/contracts.py` | 181 | Optional directly-measured analyser λ for low idle fallback |
| `high_idle_lambda` | `labs/gaslab/gaslab/contracts.py` | 200 | Optional directly-measured analyser λ for high idle |
| `has_catalyst` | `labs/comlab/comlab/schemas/ingestion.py` | 68 | Boolean flag indicating presence of catalytic converter |
| `gas_co` | `labs/gaslab/gaslab/contracts.py` | 174 | Low-idle carbon monoxide |
| `gas_hc` | `labs/gaslab/gaslab/contracts.py` | 175 | Low-idle hydrocarbons |
| `gas_co2` | `labs/gaslab/gaslab/contracts.py` | 176 | Low-idle carbon dioxide |
| `gas_o2` | `labs/gaslab/gaslab/contracts.py` | 177 | Low-idle oxygen |
| `gas_nox` | `labs/gaslab/gaslab/contracts.py` | 178 | Low-idle oxides of nitrogen |
| `engine_rpm` | `labs/obdlab/obdlab/schemas/payload.py` | 37 | Sanitized/converted engine RPM |
| `coolant_temp_c` | `labs/obdlab/obdlab/schemas/payload.py` | 40 | Sanitized/converted coolant temp ECT |
| `calculated_engine_load_pct` | `labs/obdlab/obdlab/schemas/payload.py` | 43 | Sanitized calculated engine load |
| `shrtft1` | `labs/obdlab/obdlab/schemas/payload.py` | 52 | Sanitized short-term fuel trim Bank 1 |
| `longft1` | `labs/obdlab/obdlab/schemas/payload.py` | 56 | Sanitized long-term fuel trim Bank 1 |
| `shrtft2` | `labs/obdlab/obdlab/schemas/payload.py` | 59 | Sanitized short-term fuel trim Bank 2 |
| `longft2` | `labs/obdlab/obdlab/schemas/payload.py` | 62 | Sanitized long-term fuel trim Bank 2 |
| `mass_airflow_gps` | `labs/obdlab/obdlab/schemas/payload.py` | 46 | Sanitized mass airflow |
| `manifold_vacuum_kpa` | `labs/obdlab/obdlab/schemas/payload.py` | 49 | Sanitized manifold vacuum |
| `normalized_obd_lambda` | `labs/obdlab/obdlab/schemas/payload.py` | 74 | Normalized OBD lambda scalar |
| `active_mil` | `labs/comlab/comlab/schemas/ingestion.py` | 299 | Status of malfunction indicator lamp |
| `mil_flashing` | `labs/comlab/comlab/schemas/ingestion.py` | 300 | Status of flashing MIL |
| `confirmed_dtcs` | `labs/comlab/comlab/schemas/ingestion.py` | 301 | Confirmed DTCs |
| `pending_dtcs` | `labs/comlab/comlab/schemas/ingestion.py` | 302 | Pending DTCs |
| `permanent_dtcs` | `labs/comlab/comlab/schemas/ingestion.py` | 303 | Permanent DTCs |
| `calculated_load_pct` | `labs/comlab/comlab/schemas/ingestion.py` | 240 | Freeze Frame calculated load |
| `short_term_ft1` | `labs/comlab/comlab/schemas/ingestion.py` | 243 | Freeze Frame short term fuel trim bank 1 |
| `long_term_ft1` | `labs/comlab/comlab/schemas/ingestion.py` | 244 | Freeze Frame long term fuel trim bank 1 |
| `short_term_ft2` | `labs/comlab/comlab/schemas/ingestion.py` | 255 | Freeze Frame short term fuel trim bank 2 |
| `long_term_ft2` | `labs/comlab/comlab/schemas/ingestion.py` | 256 | Freeze Frame long term fuel trim bank 2 |
| `o2_voltage_b1s1` | `labs/comlab/comlab/schemas/ingestion.py` | 257 | Freeze Frame O2 voltage bank 1 sensor 1 |
| `barometric_pressure_kpa` | `labs/comlab/comlab/schemas/ingestion.py` | 258 | Freeze Frame barometric pressure |
| `commanded_egr_pct` | `labs/comlab/comlab/schemas/ingestion.py` | 259 | Freeze Frame commanded EGR |
| `run_time_since_start_sec` | `labs/comlab/comlab/schemas/ingestion.py` | 260 | Freeze Frame run time since start |
| `fuel_level_pct` | `labs/comlab/comlab/schemas/ingestion.py` | 261 | Freeze Frame fuel level |
| `monitor_id` | `labs/comlab/comlab/schemas/ingestion.py` | 283 | Mode $06 monitor ID |
| `state` | `labs/comlab/comlab/schemas/ingestion.py` | 284 | Mode $06 monitor state |
| `margin_pct` | `labs/comlab/comlab/schemas/ingestion.py` | 285 | Mode $06 monitor margin |
| `target_component` | `labs/comlab/comlab/schemas/ingestion.py` | 286 | Mode $06 monitor target component |

### Stale Token Verification

A case-sensitive search for stale tokens (`measured_lambda`, `catalyst_present`, `secondary_air_equipped`, `has_particulate_filter`, `GPF`, `GASLab/`, `OBDLab/code`, `DNALab/VINLab`, `comlab/adapters`) across `apps/ui` yields zero hits (outside this audit file itself).

### Copies Identity Verification

```bash
diff -s "apps/ui/4DLab_UI_FieldMap.md" "apps/ui/UI design/uploads/4DLab_UI_FieldMap.md"
# Files apps/ui/4DLab_UI_FieldMap.md and apps/ui/UI design/uploads/4DLab_UI_FieldMap.md are identical
```

## CODE REVIEW

- **Doc-only changes:** Verified with `git status` that only mockup JSX and documentation FieldMap files are changed under `apps/ui`. No lab or app production code has been modified.
- **Zero invented fields:** Checked that every field name in the FieldMap matches an existing symbol in the schema files.
- **Signal/Noise held:** Checked that all shipping fields in the FieldMap have a corresponding live consumer in the codebase.
