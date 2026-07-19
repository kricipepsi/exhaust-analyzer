---
node_type: "prd"
lab: "comlab"
module: "comlab"
subsystem: "requirements"
implements: []
consumers:
  - "hld: labs/comlab/docs/COMLab_HLD.md"
  - "wired: apps/4DLabWired/wired/composition.py LabPipelineAggregator integration"
drift_guards: []
tags: [comlab, finished, prd]
source: "labs/comlab/docs/COMLab_PRD.md"
---
# COMLab Product Requirements Document (PRD)

**Document type:** PRD — what COMLab promises to the technician/user and how
that promise is shaped by the manual-input, petrol-only, no-hardware-pairing
operational context.

**Status:** v2.0 — **as-built**, reconciled to the shipped `comlab/` package
(2026-06-21). Supersedes the v1.0 draft (2026-05-21), archived at
`docs/ARCHIVE/COMLab_PRD_v1.0_2026-05-21.md`. Screen-6 commitments are reconciled
to the `OrchestratorFinalUIOutput` contract; UI-side screen behaviour remains a
front-end commitment.

**Scope (binding, per `wiki/04_horizon_eras.md`):** petrol **1990–2010, Euro
1–5**, manual-input, no hardware pairing. Post-2010 Euro 6+ technology —
secondary-air injection (SAI), GPF/DPF, LSPI, boost-era perks — is **out of
scope**: no SAI checkbox, no GPF/Boost quick-tags, no such fields in the payload.

**Companion to:** `COMLab_HLD.md` (architecture, binding), `COMLab_LLD.md`,
`COMLab_DLD.md`, `docs/adr/`, `COMLab_BDD.md`. This PRD inherits every
architectural decision from them and does not re-litigate them.

**Out of scope:**

- File-level class/method specifications — `COMLab_LLD.md`.
- Resource budgets, latency allocation, CI build script — `COMLab_DLD.md`.
- UI visual design / branding / typography; native-app vs PWA — front-end team.

**Authoritative inputs:**

- `COMLab_HLD.md` — architecture (binding).
- `wiki/` — domain truth (esp. `04_horizon_eras` scope; `10_differential_and_symptom_prior`).
- `docs/Vocabulary/SEMANTIC_CONTRACT.md` — boundary protocol.
- The six v1.0 rulings, now settled in code and recorded in `docs/adr/`
  (siblings cap 5; KG per-family directory; `user_input_echo_audit` kept;
  filename kept; `lab_routing_directive` surfaced in `execution_meta`).

---

## 1. Product vision & strategic value

### 1.1 What COMLab is, from the user's perspective

COMLab is the **diagnostic verdict engine** behind 4DApp's petrol-vehicle
fault-finder. A technician (or vehicle owner) enters readings from a
workshop gas analyser, an OBD-II scan tool, and a DTC reader through a
multi-screen wizard. After the final submit, COMLab returns one
plain-language diagnostic verdict, a structured list of repair steps, an
estimated power-loss percentage, and a small panel of "also worth
considering" runner-up faults.

The product is petrol-only in v1 (no diesel — `PRD_4D_App.md` §5). Every
step on the way to the verdict is auditable: the technician sees the
exact numbers they typed echoed back on the result screen alongside the
verdict, so a typo can be caught without re-running the session.

### 1.2 Strategic value

- **Workshop-grade diagnosis without OE-tool capital.** Standard gas
  analyser + basic scan tool + COMLab → an output that competes with
  factory diagnostic equipment. No proprietary OEM dongles, no Bluetooth
  pairing, no firmware-update hoops.
- **No live data stream required.** Entirely manual input. Works in
  environments without OBD-II Bluetooth coverage, on older vehicles
  whose ECUs do not stream cleanly, or for owner-operators who do not
  have a live scanner.
- **Domain-expert maintainability.** Diagnostic rules and the
  fault-to-component mapping (the Fault-Atlas KG) live in flat JSON
  config files. A qualified automotive expert can add a new fault, fix
  a remediation step, or tune a threshold without touching Python.
- **Petrol-first focus.** Diesel and cold-start hybrid logic are
  deliberately excluded from v1; COMLab can be tuned aggressively for
  the petrol-running-warm operating envelope without compromise.

### 1.3 What COMLab is *not*

- It is not a real-time live-data logger. There is no streaming, no
  graphing, no continuous monitor. One session in, one verdict out.
- It is not a parts catalogue. The Fault-Atlas KG names component
  groups and subsystems for grouping and explanation, not part numbers
  or supplier links.
- It is not a repair-cost estimator. v1 does not surface labour hours
  or parts cost bands (HLD §5.2 explicitly drops these fields).
- It is not an AI free-text symptom interpreter. Symptom selection is
  a fixed two-tier picker (`tier_1_primary_symptom`,
  `tier_2_subfield_filter`) backed by SymptomLab; free text is logged
  but not analysed in v1.

---

## 2. Users

Two primary personas. COMLab's behaviour does not branch on persona —
the same wizard, the same verdict shape — but the user research
informing the PRD did distinguish them.

| Persona | Context | What they need from the result page |
|---|---|---|
| **Workshop technician** (primary) | Diagnosing a customer car, paid by the job. Needs to commit to a repair quote in under 5 minutes. | Verdict + remediation steps with enough specificity to skip re-diagnosis ("replace valve stem seals — measure clearance" is good; "engine problem" is not). Runner-up panel reads as "I considered these too and ruled them out". |
| **Skilled owner-operator** (secondary) | Diagnosing their own car. Cares more about understanding than speed. | Verdict + plain-language `mechanical_failure_mode` ("what is happening inside the engine"). Power-loss percentage to estimate "is this drivable until next month". Echo audit to confirm the inputs were right. |

Persona-neutral guarantees:

- The same wizard for both. No "expert mode" toggle in v1.
- The same verdict shape, including the runner-up panel and the
  remediation steps.
- The same defensive guardrails on input.

---

## 3. The wizard ingestion flow

The wizard is multi-screen and submits a single combined payload to
COMLab on the final step. Screens are owned by the UI layer; COMLab's
contract is the **payload shape on submit** and the **field-gating
rules each screen must honour** (the latter authoritatively listed in
`data_flow_report.md` §8 — referenced, not duplicated here).

```
┌─────────────────────────────────────────────────────────────────────────────┐
│ Screen 1 — VEHICLE CONTEXT                                                  │
│  • VIN (17 char, uppercase auto-normalised)                                 │
│  • Two-tier symptom picker (Tier 1 → Tier 2 cascade)                        │
│  • Engine state at sample time (running / cranking / won_not_start)         │
│  • Confidence banner if VIN decodes PARTIAL or NONE (yellow / red)          │
│ ──► Triggers VINLab.decode() + SymptomLab.resolve() → DNALab.build_dna()    │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Screen 2 — GAS-ANALYSER READINGS                                            │
│  • Idle baseline group (HC, CO, CO₂, O₂, NOx)                               │
│  • Stress-idle group (same fields, at stress_idle_rpm_target from DNA)      │
│  • Sample validity gate runs INSIDE GASLab on submit (per horizontal-DNA)   │
│ Suppressed entirely when SymptomDNA.engine_state == won_not_start           │
│ ──► On submit, GASLab.analyze() produces GasLabPayload                      │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Screen 3 — OBD LIVE PIDS                                                    │
│  • Engine state (RPM, ECT, load, throttle)                                  │
│  • Air metering (MAF/MAP/IAT — fields shown per DNA architecture)           │
│  • Fuel trims (Bank 1 always; Bank 2 only if number_of_banks >= 2)          │
│  • O₂ inputs vary by upstream_o2_type (per the UpstreamO2Type enum)         │
│  • Plausibility/decimal-misplacement sentinels run INSIDE OBDLab on submit  │
│ Suppressed/limited when SymptomDNA.engine_state in {won_not_start,cranking} │
│ ──► On submit, OBDLab.process() produces OBDLivePayload                     │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Screen 4 — DTC & MIL                                                        │
│  • Confirmed / Pending / Permanent DTCs (multi-line, DTC_REGEX validated)   │
│  • MIL on / MIL flashing checkboxes                                         │
│  • DNA-gated quick-tags (Catalyst, EGR — per emissions flags from DNA;      │
│    SAI / GPF / Boost are out of scope, Euro 6+ perks)                       │
│  • Misfire cylinder picker, capped at cylinder_count                        │
│  • Freeze frame (collapsible, advanced)                                     │
│  • Mode $06 monitors (advanced expander) — suppressed when won_not_start    │
│ ──► On submit, DTCLab.compile_dtcs() produces DTCLabPayload                 │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Screen 5 — REVIEW & SUBMIT                                                  │
│  • Read-only summary of every value entered across screens 1–4              │
│  • Per-screen "edit" jump links                                             │
│  • Single SUBMIT button — assembles OrchestratorInboundRequest              │
│ ──► POST to COMLab → OrchestratorFinalUIOutput → render Screen 6            │
└──────────────────────┬──────────────────────────────────────────────────────┘
                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ Screen 6 — RESULT (the only screen COMLab's payload directly shapes)        │
│  • Verdict header + confidence score                                        │
│  • Fault-enrichment block (component group, subsystems, failure mode)       │
│  • Remediation steps (numbered list)                                        │
│  • Differential siblings panel (up to 5 runner-ups)                         │
│  • Performance analytics (power loss %, catalyst index, severity)           │
│  • User-input echo audit (every value typed, side-by-side with verdict)     │
│  • Lab routing directive panel (greyed-out sections explained)              │
│  • Execution meta footer (horizon, degradation mode, confidence rating)     │
└─────────────────────────────────────────────────────────────────────────────┘
```

**Horizontal-DNA implication for screens 2–4:** Each producer lab
validates DNA-relative plausibility on submit, *before* the data
reaches COMLab. The wizard surfaces those validation errors on the
relevant screen, not on Screen 6. Example: if OBDLab rejects `engine_rpm:
7200` because the vehicle's `rated_rpm` from DNA is 5200, the user sees
the error inline on Screen 3 — they never get to Screen 5. COMLab's
contract is that *if* a payload reaches it, every value in it has
already passed the producer's DNA-aware checks.

---

## 4. Defensive input gates — who runs which check

The COMLabDesign proposal centralised plausibility checks in COMLab.
The horizontal-DNA flip moves most of them to the producer labs, where
the DNA context is local. COMLab keeps only the gates that intrinsically
require all four labs' data to evaluate.

### 4.1 Producer-lab gates (run on submit of screens 2, 3, 4 — not COMLab)

| Gate | Producer | Trigger | What the user sees |
|---|---|---|---|
| DNA-relative RPM ceiling | OBDLab | `engine_rpm > rated_rpm` from DNA | Inline error on Screen 3: "Entered RPM exceeds this engine's redline (rated 5200). Re-check value." |
| Decimal-misplacement sentinel | OBDLab / GASLab | Value > 10× plausible bound | Inline error on the relevant screen: "Value 140 is unusually high for CO%. Did you mean 1.40?" |
| Thermal gate (ECT < 70 °C for trim analytics; ECT < 75 °C for engine-state bucket) | OBDLab | `coolant_temp_c < 70` and analytics needed | Inline warning on Screen 3: "Engine is cold (ECT 62 °C). Warm to ≥70 °C before reading fuel trims." Wizard offers "skip trim analytics" or "go back". Two thresholds coexist: 70 °C gates trim analytics (`ENGINE_COLD`), 75 °C gates the `COLD_OPEN_LOOP_INVALID` engine-state bucket. Both must be satisfied before closed-loop diagnostics run. |
| Gas sample validity | GASLab | `gas_co + gas_co2 + gas_o2` outside 14–18% | Inline error on Screen 2: "Gas sample fails validity check — likely air leak at probe. Re-seat and re-sample." |
| Single-bank Bank 2 enforcement | OBDLab | Bank 2 trim values entered when `number_of_banks == 1` from DNA | Fields hidden by DNA gating; if somehow submitted, OBDLab strips them and warns. |
| DTC format | DTCLab | DTC string fails `^[BCPU][0-3][0-9]{3}$` | Inline error on Screen 4 next to the offending row. |

### 4.2 COMLab gates (run in Stage A of the pipeline, on the assembled payload)

| Gate | Trigger | Error code | What the user sees on Screen 6 |
|---|---|---|---|
| Schema/contract drift | Pydantic ValidationError | `ERR-CONTRACT-001` (regex/range) or `ERR-CONTRACT-002` (cross-field) | "Internal payload mismatch. Please re-submit. If the error persists, your wizard version may need updating." |
| Schema version mismatch | `vehicle_dna.schema_version` older than `MIN_SUPPORTED_SCHEMA_VERSION` | `ERR-ABORT-005` | "Your client app needs updating to communicate with the diagnostic engine." |
| Sample validity (final guard) | `gas_lab_output.sample_validity != "VALID"` (and GASLab not suppressed) | `ERR-ABORT-001` | Same wording as the GASLab inline guard — surfaces the same root cause if it somehow slipped through. |
| Engine warmed (final guard) | `obd_live_data.engine_warmed == false` (and OBDLab not suppressed) | `ERR-ABORT-002` | Same wording as the OBDLab inline guard. |
| VIN unresolvable | `vehicle_dna.vin_dna.confidence == "NONE"` | `ERR-ABORT-004` | "Vehicle could not be identified from the VIN. Diagnosis cannot run without vehicle identification." |

COMLab's gates are intentionally a thin safety net behind the producer
gates. The user should almost never see a COMLab-level abort if the
wizard is working correctly — if they do, the message names the
specific upstream cause.

### 4.3 Null vs zero — the integrity rule

The product treats an unfilled field (`null`) and an explicit zero
(`0.0`) as different facts, especially for fuel trims. The wizard never
auto-fills numeric fields with `0`. When the technician leaves a field
blank, the payload carries `null`; when the technician types `0`, the
payload carries `0.0`. COMLab's degradation classifier (Stage A step 5
of HLD §4.1) reads `null`s as missing-evidence; readers of `0.0` treat
it as a real measurement. The user does not need to know this rule
exists — the wizard simply does the right thing by not pre-populating
numeric fields with zeros.

---

## 5. The result page — what's on Screen 6

The result page is a direct rendering of the `OrchestratorFinalUIOutput`
JSON (HLD §7.4). Every block on the screen corresponds to one named
field in that payload; every field in the payload has at least one
visible UI consumer.

### 5.1 Verdict header

- Plain-language `display_headline` (one sentence, ≤ 140 chars).
- `fault_code` (small, monospace, for service-record cross-reference).
- `fault_name` (snake_case, for cross-reference to KG and registry).
- `fault_family` chip (small badge: `rich_mixture`, `misfire`, etc.).
- `confidence_score` (0.00–1.00), with a copy-friendly band label:
  ≥ 0.85 "high", 0.60–0.85 "medium", < 0.60 "low".
- `severity_level` ribbon at the top:
  - `CRITICAL_IMMEDIATE_STOP` → red, with "do not drive" copy.
  - `WARNING_DEGRADED_PERFORMANCE` → amber, with "safe to drive,
    schedule repair" copy.
  - `OPTIMAL_HEALTH` → green, with "no fault detected" copy.

### 5.2 Fault enrichment block

Sourced from `fault_enrichment` in the payload (KG node values).

- `component_group` as a section heading (e.g. "Engine Cylinder Head
  Assembly").
- `impacted_subsystems` as a badge list under the heading.
- `mechanical_failure_mode` as a 1–3 sentence explanation paragraph.
- `ui_remediation_steps` as a numbered list (1..8 items). The wizard
  renders these verbatim; no editorial truncation.

### 5.3 Differential siblings panel

Sourced from `diagnostic_verdict.differential_siblings[]`. Up to **5
total slots** (HLD answer-set Q1):

- Up to **3 runtime-derived** runner-ups (the next-highest scoring
  rules from this session) — each shows `confidence_score`.
- Up to **2 editor-curated** "commonly confused with" siblings from
  the KG node's `differential_siblings` field — each shows
  `confidence_score: null` (did not fire this session) and a small
  "consider also" tag.
- Click-through on any sibling shows that fault's KG enrichment block
  (read-only modal). No re-running of the engine.

If the verdict is `OPTIMAL_HEALTH`, this panel is hidden.

### 5.4 Performance analytics

- `kinetic_power_loss_pct` as a circular gauge or bar (0–100 %).
- `catalyst_efficiency_index_pct` as a second gauge, shown only when
  `vehicle_dna.vin_dna.emissions.downstream_o2_present == true`
  (otherwise the value would be meaningless; suppress).
- `severity_level` — duplicated as the result-page top ribbon; here as
  a small badge for clarity.

### 5.5 User-input echo audit (Q4 ruling)

Per the ruling recorded in `docs/adr/`, this block is **emitted by COMLab** and surfaced on
Screen 6 because the mobile wizard wipes per-screen state on view
switch and cannot reliably re-emit the typed values from local cache.

Layout:

- Collapsible expander, collapsed by default ("Show what I typed →").
- When expanded: a two-column table of `field_label : value` grouped by
  screen origin. Includes VIN, symptom selection, every gas reading,
  every OBD PID, every DTC.
- Visual cue when an entered value materially influenced the verdict
  (e.g. the trim value the router used) — the value is bold + linked
  to the relevant rule explanation modal (a stretch enhancement;
  v1.0 ships with bolding only).
- A "Was this value wrong?" link next to each row, which jumps back to
  the originating wizard screen for correction and re-submit.

### 5.6 Lab routing directive panel (Q6 ruling)

Per the ruling recorded in `docs/adr/`, the four `LabRoutingDirective` booleans are surfaced
inside `execution_meta.lab_routing_directive`. The result page renders
them as a small "what was skipped and why" disclosure:

- `suppress_gaslab: true` → "Gas analyser inputs skipped because the
  symptom is 'vehicle won't start'."
- `suppress_obd_live_pids: true` → "Live OBD PIDs skipped because the
  engine was not running."
- `suppress_mode06_ui: true` → "Mode $06 monitor section skipped —
  monitors are not ready when the engine is not running."
- `cold_start_mode: true` → "Cold-start hypothesis was active — some
  warm-only rules were down-weighted."

Hidden if all four are false (the FULL_FUSION common case).

### 5.7 Execution meta footer

Small, low-emphasis (italic, light grey) at the bottom of Screen 6:

- `resolved_horizon` (`HORIZON_LEGACY` / `_ADAPTIVE` / `_MODERN`) and
  what it means for this car ("Euro-3-era tuning applied").
- `degradation_mode` (`FULL_FUSION` / `GAS_DOMINANT`).
- `processing_confidence_rating` (`HIGH_ASSURANCE` /
  `DEGRADED_ASSURANCE` / `LOW_CERTAINTY`).
- `vin_confidence` (`HIGH` / `PARTIAL` / `NONE`).
- `session_id` (copy button next to it for support tickets).
- `schema_version`.

### 5.8 Result-page layout when a fatal abort fires

If COMLab returns the abort-shape payload (HLD §7.5), Screen 6 changes:

- Top: red banner with the `error_code` and `ui_remediation_message`.
- Below: the user-input echo audit (collapsed by default) — so the
  technician can see what was sent.
- Below: a single "Edit and resubmit" button that returns the user to
  the wizard with all values preserved.
- No verdict, no enrichment, no analytics, no runner-ups — because
  there is no verdict to show.

---

## 6. Error & abort UX

### 6.1 Error message principles

- Every COMLab error message names the **specific failed condition** and
  **one actionable next step**. No stack traces, no `RuntimeError`
  echoes.
- Error codes are visible (small monospace) but the human-readable
  remediation is the primary affordance.
- If the user fixes the upstream cause and resubmits, the session
  continues — no full restart.

### 6.2 Error code → user-facing copy map

The full code taxonomy lives in `COMLab_LLD.md` §10. The user-facing
copy is owned by the PRD:

| Code | Headline | Action |
|---|---|---|
| `ERR-CONTRACT-001` | Internal payload mismatch. | Resubmit. If it persists, the wizard app may need an update. |
| `ERR-CONTRACT-002` | Vehicle profile inconsistency. | Resubmit. If it persists, contact support with the session ID. |
| `ERR-ABORT-001` | Gas sample failed validity check. | Re-seat probe in tailpipe; ensure no air leak. Re-sample. |
| `ERR-ABORT-002` | Engine not at operating temperature. | Warm engine to ≥70 °C, then re-enter trim values. |
| `ERR-ABORT-004` | Vehicle could not be identified. | Verify the VIN was typed correctly. Try again. |
| `ERR-ABORT-005` | Client app needs updating. | Update the 4DApp client to the latest version. |
| `ERR-VIN-400` | VIN format invalid. | VIN must be 17 alphanumeric characters (no `I`, `O`, `Q`). |

### 6.3 Degraded modes (not errors)

Degradation is a quieter signal: the diagnosis still runs, but with
acknowledged reduced confidence. Surfaces on the result page as:

- **`GAS_DOMINANT` mode** — yellow info chip in the execution meta
  footer: "Diagnosis based on gas chemistry only; fuel trim data was
  not available."
- **`vin_confidence == PARTIAL`** — yellow banner at the top of
  Screen 6: "Vehicle profile partially resolved — DNA-relative checks
  used best-guess defaults. Verify the VIN and vehicle make/model."
- **`processing_confidence_rating == LOW_CERTAINTY`** — overrides the
  confidence band label in §5.1 to "low" even if the raw score is
  numerically higher.

---

## 7. Performance & accessibility

### 7.1 Latency commitment to the user

- The wizard's "Submit" button returns a result in **under 300 ms** on
  a warm server (250 ms COMLab budget per DLD + 50 ms transport
  allowance).
- A spinner appears immediately on submit; if no response by 1.5 s,
  the spinner is replaced with "Engine taking longer than expected —
  please wait" and a session-id-with-copy-button so the user can file
  a support note. (Operational threshold; not a normal occurrence.)

### 7.2 Accessibility

- Screen 6 is fully usable with a screen reader: every section has a
  heading, every chip has aria-label, every number has a textual unit.
- Severity ribbons use both colour and icon (do not rely on colour
  alone for the critical-stop signal).
- All text passes WCAG AA contrast at the default theme.
- Keyboard navigation: every wizard field is reachable in tab order;
  every result-page expander is keyboard-toggleable.

### 7.3 Mobile-first

The wizard targets mobile browsers and the 4DApp native mobile
container as primary surfaces. Layout adapts down to 360 px wide;
Screen 6 sections stack vertically with no horizontal scroll required.

---

## 8. Operational requirements

### 8.1 Session audit trail

Every COMLab session generates an audit record consumed by the
operations dashboard:

- `session_id`
- timestamp
- `vin_confidence`, `resolved_horizon`, `degradation_mode`
- `fault_id` (or `OPTIMAL_HEALTH` sentinel)
- `confidence_score`
- which fatal gate fired, if any (`error_code`)
- which rules in `global_fault_registry.json` evaluated truthy (rule
  IDs only — the audit is anonymous beyond the session ID)

The audit record does not include the raw user inputs — only the
derived facts. (Raw inputs are echoed only on Screen 6 to the
submitter; they are not stored server-side beyond what's needed for
support workflows.)

### 8.2 No network requirement after launch

COMLab itself does no outbound network calls during a session. All
config (`global_fault_registry.json`, `fault_atlas_kg/*.json`,
`eras_sensitivity_masks.yaml`) is loaded at boot from local disk.
This is a hard requirement: workshops with intermittent connectivity
must be able to run sessions offline once the app is loaded. (The
4DApp client-server architecture is owned outside this PRD, but
COMLab's design must support an offline mode.)

### 8.3 Config update flow

New KG content / new registry rules ship through the standard PR
process (per the ruling recorded in `docs/adr/`): any qualified domain expert can open a PR
against `comlab/config/`, an automated build-validation script
(`COMLab_DLD.md` §7) lints the schemas and the cross-reference between
registry and KG, and two reviewers must approve before merge. After
merge the change rides the normal release train; no hot-patching of
production COMLab.

### 8.4 Observability surfaces

The product team gets the following dashboards, fed by §8.1 audit
records (specified in detail in `COMLab_DLD.md` §6):

- session count by `fault_family` per day
- fatal-abort rate per day, broken down by `error_code`
- `degradation_mode` distribution (catch a sudden GAS_DOMINANT spike
  → indicates a producer-lab regression)
- 95th-percentile latency
- top-10 fired registry rules

---

## 9. Out of scope for v1 (candidates for v2+)

These items were considered and explicitly deferred. Each names the
conditions under which it would graduate into a future release.

| Item | Defer reason | Graduation condition |
|---|---|---|
| Diesel powertrains | Lambda chemistry differs; AFR target differs; would require parallel rule set | Sufficient v1 telemetry to design a clean diesel pipeline (estimated v2.0) |
| Cold-start fault analysis | Closed-loop assumptions break below ECT 70 °C; requires open-loop rule track | When OBDLab models cranking/cold-running PIDs |
| Real-time / streaming live data | Wizard-based manual input is the v1 contract | Live-Bluetooth path designed for a separate "Live mode" alongside wizard, not replacing it |
| Part-cost / labour-hour estimation | No consumer in the engine; would require external supplier data feed | Product strategy decision; not a technical blocker |
| Free-text symptom AI parser | SymptomLab v1 is tier_1 + tier_2 only; free-text logged but not analysed | LLM-side pricing/latency justifies adding it |
| Multi-fault verdicts (e.g. "fault A AND fault B simultaneously") | Confidence-ranking model is single-winner | Product evidence that real-world cases are multi-fault often enough to matter |
| Persistent user accounts / session history | v1 is stateless beyond audit | Product decision (privacy/account model) |
| OEM-specific deep DTCs (U-codes, manufacturer-specific) | DTC_REGEX accepts them but routing tags don't cover them | DTCLab adds OEM routing dictionaries |

---

## 10. Success metrics (how we know it works)

These metrics gate the v1 launch.

- **Fatal abort rate < 5 %** of submitted sessions in production.
  Higher means the wizard is letting bad payloads through.
- **`vin_confidence == NONE` rate < 2 %** of submitted sessions.
  Higher means VINLab's decoder coverage has gaps.
- **`degradation_mode == FULL_FUSION` rate > 70 %** of submitted
  sessions (excluding non-starter symptom paths). Lower means
  technicians are routinely skipping fuel-trim entry — investigate
  wizard UX.
- **95th-percentile end-to-end latency < 500 ms** wizard-submit to
  Screen-6-render. The 250 ms COMLab budget + transport + render
  must add up to this.
- **Verdict-vs-mechanic-truth agreement ≥ 80 %** on a curated
  regression set of 50+ real-world cases with confirmed
  post-repair-success outcomes. (Methodology defined separately;
  this is the "is the diagnosis actually right" metric and the only
  one that ultimately matters.)

---

## 11. Open questions for product sign-off

These were not in the HLD round and need a product call, not an
architecture call.

1. **`processing_confidence_rating == LOW_CERTAINTY` — should the
   result page require an explicit "I read the low-certainty warning"
   click before showing the verdict?** Argument for: prevents a
   technician quoting a repair on the back of a low-certainty
   diagnosis. Argument against: friction; technicians who trust their
   own judgement will be annoyed. Recommend: no gate in v1; surface
   as a prominent banner only.
2. **Differential-siblings click-through opens a modal in v1.**
   Should it instead be a sidebar that stays open while the user
   scrolls through the main verdict? Modal is simpler; sidebar is
   richer. Recommend: modal in v1, revisit if usage data shows
   technicians comparing multiple siblings.
3. **User-input echo audit — should the support ticket flow
   auto-attach this block?** Privacy-neutral (the user typed it
   themselves) but it does ship raw input to support. Recommend:
   yes, opt-in toggle at ticket-creation time, off by default.
4. **Severity ribbon copy when `severity_level == OPTIMAL_HEALTH`** —
   currently "no fault detected". Alternative: "no actionable fault
   detected — minor inefficiencies may still be present." Recommend:
   the longer copy if power_loss_pct > 5, the shorter otherwise.
5. **Mode $06 monitor results on Screen 6** — KG enrichment does not
   surface these. Should the result page have a separate "Monitor
   Health" section pulled from `dtc_lab_output.mode_06_monitors`?
   Recommend: yes, but only when at least one monitor is in
   `PENDING_FAIL_MARGINAL` or `CRITICAL_FAIL` state.

---

## 12. References

- `COMLab_HLD.md` — architecture (binding).
- `COMLab_LLD.md` — file-level specification (sibling).
- `COMLab_DLD.md` — resource/operational specification (sibling).
- `COMLab_BDD.md` — behavioural scenarios for the Screen-6 contract.
- `docs/adr/` — the six v1.0 rulings now recorded as decision records.
- `wiki/` — domain truth (esp. `04_horizon_eras` scope; `10_differential_and_symptom_prior`).
- `docs/Vocabulary/SEMANTIC_CONTRACT.md` — boundary protocol (binding for all
  schema fields named in §5).
