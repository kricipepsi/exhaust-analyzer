---
node_type: "dld"
lab: "comlab"
module: "comlab"
subsystem: "detailed-design"
implements:
  - "labs/comlab/comlab/core/lab_pipeline_aggregator.py"
  - "labs/comlab/comlab/core/fault_atlas_router.py"
  - "labs/comlab/comlab/core/fault_atlas_kg.py"
  - "labs/comlab/comlab/observability/_tracer.py"
  - "labs/comlab/comlab/analytics/power_loss_analytics.py"
  - "labs/comlab/comlab/schemas/ingestion.py"
  - "labs/comlab/comlab/schemas/response.py"
consumers:
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py deployment / latency-budget / observability surfaces"
  - "wired: apps/4DLabWired/wired/composition.py LabPipelineAggregator import"
drift_guards:
  - "labs/comlab/tests/unit/test_lab_pipeline_aggregator.py"
  - "labs/comlab/tests/unit/test_fatal_gate_wiring.py"
  - "labs/comlab/tests/e2e/test_pipeline_round_trip.py"
  - "labs/comlab/tests/e2e/test_error_codes.py"
tags: [comlab, finished, dld]
source: "labs/comlab/docs/COMLab_DLD.md"
---
# COMLab Detailed/Deployment Design (DLD)

**Document type:** DLD — runtime resource budgets, latency targets, boot
sequence, logging and observability strategy, build-validation CI script,
integration test harness shape, cross-version compatibility, deployment
model, failure-mode recovery.

**Status:** v2.0 — **as-built**, reconciled to the shipped `comlab/` package
(2026-06-21). Supersedes the v1.0 draft (2026-05-21), archived at
`docs/ARCHIVE/COMLab_DLD_v1.0_2026-05-21.md`. Resource budgets and latency
targets remain *commitments* (the operational envelope each release must hit),
not measured facts; module/config/observability details are reconciled to code.

**Scope (binding, per `wiki/04_horizon_eras.md`):** petrol **1990–2010, Euro
1–5**; post-2010 Euro 6+ tech (GPF/LSPI/SAI) out of scope.

**Companion to:** `COMLab_HLD.md` (binding architecture), `COMLab_LLD.md`
(binding file/class spec), `COMLab_PRD.md` (binding user-facing
commitments), `docs/adr/` (decisions). The DLD does not relitigate any decision
in those documents; it specifies the *operational envelope* every COMLab release
must hit and the CI machinery that proves it.

**Out of scope:**

- Class signatures and method contracts — `COMLab_LLD.md`.
- Wizard UX copy — `COMLab_PRD.md`.
- Architectural reconciliation with sibling labs — `COMLab_HLD.md` §11.
- Choice of cloud vendor / container orchestrator. The DLD specifies a
  resource envelope; how the surrounding 4DApp infrastructure provisions
  it is owned outside this lab.

**Authoritative inputs:**

- `COMLab_HLD.md` §4 (the four pipeline stages — they drive the latency
  allocation in §3).
- `COMLab_LLD.md` §6, §8, §9 (modules + config schemas + tests — they
  drive the boot sequence in §4 and the build-validation in §7).
- `COMLab_PRD.md` §7 (latency commitment to the user) and §8 (operational
  requirements) — bind §3 and §6.
- `docs/adr/` — the mandatory automated build-validation + two-reviewer ruling
  directly feeds §7; the other decisions flow through the HLD/LLD/PRD references
  above.

---

## 1. Scope and runtime targets

This DLD specifies what an in-production COMLab process must deliver,
how it boots, what it spends, what it logs, and how a build is gated
before it reaches production.

Three runtime targets bind every release:

1. **Per-session end-to-end latency ≤ 250 ms** at p95 on the reference
   hardware profile (§2.4). The PRD's user-facing 300 ms commitment
   (PRD §7.1) reserves 50 ms for transport and serialisation outside
   COMLab.
2. **Combined config footprint ≤ 2.5 MB** on disk (`global_fault_registry.json`
   + `comlab/config/kg/*.json` + `eras_sensitivity_masks.yaml`).
3. **Cold-boot time ≤ 1.5 s** from process start to ready-to-serve.

A release that fails any of the three is a release blocker, not a
warning.

---

## 2. Resource manifest

### 2.1 In-memory footprint at steady state

| Asset | Loaded into | Approximate budget | Notes |
|---|---|---|---|
| `global_fault_registry.json` | `FaultAtlasRouter._registry` (`list[RegistryRow]`) | ≤ 800 KB | ~120 rule rows × ~6 KB each in the parsed Pydantic form |
| `config/kg/*.json` (13 per-family files) | `FaultAtlasKG._nodes` (`dict[str, KGNode]`) | ≤ 2 MB | one file per fault family + `_kg_schema.json` |
| `eras_sensitivity_masks.yaml` | `HorizonContextInjector._masks` (`dict[Horizon, dict]`) | ≤ 50 KB | 3 horizon entries |
| Pydantic schema classes + cached validators | module-level singletons | ≤ 4 MB | One-time JIT cost, amortised over all sessions |
| Per-session working dict | stack-allocated `SanitizedPayload` | ≤ 80 KB peak | Freed when response returns |
| **Total RSS at idle** | | **≤ 80 MB** | Including Python interpreter + dependencies |
| **RSS under 50 concurrent sessions** | | **≤ 160 MB** | 80 KB × 50 = 4 MB of session state on top of idle |

Concurrent-session ceiling of 50 is the v1 reference; horizontal scale
beyond that is the infra team's choice — COMLab is stateless within a
session, so adding workers is linear.

### 2.2 On-disk config envelope (the 2.5 MB hard limit)

The build-validation script (§7) `du -b`-sums the contents of
`comlab/config/` (recursively) at every PR. Exceeding 2.5 MB is a CI
failure. Today's expected breakdown:

```
comlab/config/global_fault_registry.json      ~ 0.75 MB
comlab/config/kg/                              ~ 2.40 MB total
  ├── _kg_schema.json                          ~ 6 KB
  ├── rich_mixture.json                        ~ 0.30 MB
  ├── lean_condition.json                      ~ 0.25 MB
  ├── misfire.json                             ~ 0.25 MB
  ├── sensor_fault.json                        ~ 0.20 MB
  ├── ecu_fault.json                           ~ 0.15 MB
  ├── no_fault.json                            ~ 0.05 MB
  ├── catalyst_failure.json                    ~ 0.20 MB
  ├── exhaust_leak.json                        ~ 0.20 MB
  ├── ignition_fault.json                      ~ 0.20 MB
  ├── mechanical_wear.json                     ~ 0.20 MB
  ├── cam_timing.json                          ~ 0.20 MB
  └── non_starter.json                         ~ 0.20 MB
comlab/config/eras_sensitivity_masks.yaml      ~ 0.03 MB
─────────────────────────────────────────────────────────
                                         total ~ 2.78 MB  (0.22 MB headroom)
```

The 12 FaultFamily values (live code `vocabulary.py`) are: `lean_condition`,
`rich_mixture`, `misfire`, `sensor_fault`, `ecu_fault`, `no_fault`,
`catalyst_failure`, `exhaust_leak`, `ignition_fault`, `mechanical_wear`,
`cam_timing`, `non_starter`.

Headroom of 220 KB allows ~25 additional KG nodes before a contract
bump to 3.0 MB is needed.

### 2.3 No persistent state

COMLab keeps no per-session state on disk and writes no database
records during processing. The audit-record stream (PRD §8.1) is
emitted as a structured log line per session; whichever log sink the
surrounding 4DApp infrastructure picks up that line is responsible for
durable storage. COMLab itself is a pure function: same input, same
output, every time.

### 2.4 Reference hardware profile

The 250 ms p95 target is measured on:

- 2 vCPU @ 2.4 GHz (x86-64) or 1 vCPU Apple Silicon equivalent.
- 256 MB RSS ceiling.
- Local-disk config (no network mount).
- Python 3.10 with `pydantic v2` and `orjson`.

Production may exceed these specs; the target does not get tighter on
better hardware (the user does not perceive sub-100 ms latency on a
manual-input wizard).

---

## 3. Latency budget — per-stage allocation

The 250 ms p95 end-to-end budget is allocated across the HLD stages as
follows. Each stage owns its slice; an LLD-level optimisation that
trades stage budgets is allowed if and only if the sum stays ≤ 250 ms.

| Stage | HLD ref | Budget | Notes |
|---|---|---|---|
| JSON parse + Pydantic gate (Stage A.1) | §4.1 step 1 | 40 ms | Dominant cost is Pydantic v2 model construction |
| Schema version + fatal gates (A.2 + A.3) | §4.1 steps 2–4 | 5 ms | Cheap arithmetic and lookups |
| Routing directive + degradation classify (A.4 + A.5) | §4.1 steps 4–5 | 5 ms | `route_symptom()` is a constant-time table lookup |
| DNA projection (A.6) | §4.1 step 6 + §6 | 10 ms | Three frozen-Pydantic model builds |
| Sanitized assembly (A.7) | §4.1 step 7 | 5 ms | Pure dict merge |
| Fault-atlas walk (Stage B) | §4.2 | 60 ms | Up to 120 rule rows × ≤ 5 operator clauses each |
| KG resolve (Stage C) | §4.3 | 5 ms | O(1) dict lookup for winner + ≤ 5 sibling lookups |
| Power-loss analytics (Stage D) | §4.4 | 15 ms | Pure math; no I/O |
| Serializer (Stage E) | §4.5 | 25 ms | Pydantic model dump + orjson serialise |
| **Slack** | | **80 ms** | Cushion for GC pauses, jitter, future stages |
| **Total** | | **250 ms** | |

The 80 ms slack is deliberate; without it a single GC pause at p99
would blow the budget. The slack is **not** budget for new
functionality — adding work requires reallocating from the slack with
a DLD revision.

Latency is measured by `perf_counter()` deltas around each stage
boundary, emitted as the `stage_latency_ms.*` fields in the
structured log line (§5.3). The build-validation script (§7) runs a
synthetic benchmark on the e2e fixture corpus and fails the build if
p95 of any stage exceeds 110 % of its budget.

---

## 4. Boot sequence

COMLab boots once per process. Boot is split into four phases; each
phase is fail-fast — a missing file at phase 2 aborts the process
before phase 3 starts.

```
Phase 0 — process start
   Python interpreter + deps loaded
   COMLab package imported

Phase 1 — schema priming
   Pydantic model classes resolved (forward refs, cross-refs)
   StrEnum modules resolved
   Cost: one-time, ~200 ms

Phase 2 — config load
   2a. eras_sensitivity_masks.yaml → HorizonContextInjector._masks
       (validate YAML shape; abort on bad)
   2b. global_fault_registry.json
       (validate against §8.1 schema; abort on bad)
   2c. comlab/config/kg/_kg_schema.json
       (load the schema document used to validate the per-family files)
   2d. comlab/config/kg/*.json (glob, exclude underscored)
       FOR EACH file:
         - parse JSON
         - validate against _kg_schema.json
         - merge into FaultAtlasKG._nodes
         - on duplicate fault_id → boot abort with file path
   Cost: ≤ 800 ms

Phase 3 — cross-reference validation (in-process variant of §7 test)
   3a. registry fault_ids ⊆ kg fault_ids   (every rule has a KG node)
   3b. kg fault_ids ⊆ registry fault_ids ∪ {OPTIMAL_HEALTH}
   3c. every node.differential_siblings ⊆ kg fault_ids
   On any failure → KGConsistencyError; process exits with code 78
       (configuration error, per sysexits.h convention)
   Cost: ≤ 50 ms

Phase 4 — ready
   FaultAtlasRouter(registry, kg, analytics) constructed
   /healthz handler is now wired (or the in-process call entry point
   is now exposed)
   Total boot time: ≤ 1.5 s
```

Boot logging emits one INFO line per phase boundary with elapsed-ms
and asset counts. If phase 2 or 3 fails, the FATAL line names the
offending file/path/key precisely — the operator should not need to
diff configs to find the problem.

---

## 5. Logging strategy

### 5.1 Library and format

COMLab logs through the standard `logging` module to a named logger
(`comlab`). Every log record is structured (JSON line on stdout) so
the surrounding 4DApp infra can ingest into a log search system
without parser rules.

A logging adapter wraps every record with three constant fields and
two per-session fields:

```jsonc
{
  // constants
  "service":          "comlab",
  "version":          "1.0.0",
  "schema_version":   "1.0",

  // per-session (None when outside a session, e.g. boot logs)
  "session_id":       "DNA_TX_8849201",
  "request_id":       "req_a9f1...",   // optional, set by the caller

  // the actual log
  "level":            "INFO",
  "ts":               "2026-05-21T16:42:11.123Z",
  "logger":           "comlab.core.fault_atlas_router",
  "message":          "registry walk complete",
  "kv":               { /* structured fields per §5.2 */ }
}
```

### 5.2 Per-stage event vocabulary

Each pipeline stage emits one terminal INFO record on success, plus
WARN records for non-fatal anomalies and ERROR records for aborts.
The `event` field is a small fixed vocabulary so dashboards can be
built deterministically.

| Stage | INFO event | WARN events | ERROR events |
|---|---|---|---|
| Stage A.1 (pydantic) | `stage_a_pydantic.ok` | — | `stage_a_pydantic.err_contract` (with `error_code`) |
| Stage A.2 (version) | `stage_a_version.ok` | `stage_a_version.minor_drift` | `stage_a_version.err_abort_005` |
| Stage A.3 (gates) | `stage_a_gates.ok` | — | `stage_a_gates.err_abort_001` / `_002` / `_004` |
| Stage A.4 (routing) | `stage_a_routing.ok` | — | — |
| Stage A.5 (degradation) | `stage_a_degradation.ok` | `stage_a_degradation.partial_dna` (when GAS_DOMINANT triggered by `suppress_gaslab` — engine_state == will_not_start) | — |
| Stage A.6 (projection) | `stage_a_projection.ok` | — | `stage_a_projection.err_internal` |
| Stage B (walk) | `stage_b_walk.ok` (with `rules_evaluated`, `rules_truthy`, `winner_fault_id`) | `stage_b_walk.no_winner` (no rule fired) | — |
| Stage C (KG) | `stage_c_kg.ok` | — | `stage_c_kg.err_lookup_miss` (registry/KG drift at runtime — should never happen) |
| Stage D (analytics) | `stage_d_analytics.ok` | `stage_d_analytics.catalyst_unavailable` | — |
| Stage E (serialize) | `stage_e_serialize.ok` | — | `stage_e_serialize.err_response_invalid` |
| End-to-end | `pipeline.ok` (with total_latency_ms, severity_level) | — | `pipeline.aborted` (with originating error_code) |

The `event` taxonomy is closed; adding a new event is a DLD change.

### 5.3 Per-stage latency fields

Every `pipeline.ok` and `pipeline.aborted` line carries:

```jsonc
{
  "stage_latency_ms": {
    "a_pydantic":   18.4,
    "a_version":     0.6,
    "a_gates":       1.2,
    "a_routing":     0.8,
    "a_degradation": 0.4,
    "a_projection":  6.1,
    "a_assemble":    1.3,
    "b_walk":       42.7,
    "c_kg":          2.1,
    "d_analytics":  11.5,
    "e_serialize":  17.2,
    "total":       102.3
  }
}
```

This is the raw data behind §3's stage-latency CI gate and the PRD
§8.4 95-th-percentile dashboard.

### 5.4 Audit record

Per PRD §8.1, one structured INFO line per session at `pipeline.ok` or
`pipeline.aborted`. Beyond `event` + `kv`, the line carries:

```jsonc
{
  "event": "pipeline.ok",
  "kv": {
    "vin_confidence":          "HIGH",
    "resolved_horizon":        "HORIZON_MODERN",
    "degradation_mode":        "FULL_FUSION",
    "fault_id":                "ERR-E2-MECH-082",
    "fault_family":            "rich_mixture",
    "confidence_score":        0.92,
    "severity_level":          "WARNING_DEGRADED_PERFORMANCE",
    "rules_evaluated":         57,
    "rules_truthy":            2,
    "differential_siblings_n": 4,
    "echo_audit_groups":       4,
    "lab_routing_directive": {
      "suppress_gaslab":          false,
      "suppress_obd_live_pids":   false,
      "suppress_mode06_ui":       false,
      "cold_start_mode":          false
    }
  }
}
```

Raw user inputs are **not** in the audit record (PRD §8.1 — by design;
they exist only in the response payload returned to the submitter).

### 5.5 Log levels

Default level `INFO`. The `pipeline.ok` and `pipeline.aborted` records
alone are sufficient for the operations dashboard at this level. To
debug a specific session, switch to `DEBUG` — `comlab` will emit one
record per sub-step (e.g. each registry row evaluated). `DEBUG` is
**not** safe in production: rule-row logging at ~120 rows per session
× concurrent throughput floods log ingestion.

---

## 6. Observability surfaces

The product/ops team consumes the PRD §8.4 dashboards. The DLD
specifies the queries that produce them, in terms of the §5 audit
fields.

| Dashboard | Source | Aggregation |
|---|---|---|
| Sessions / day | `event:"pipeline.ok"` count | per-day bar |
| Fault family share | `event:"pipeline.ok"` group by `kv.fault_family` | stacked area, per-day |
| Fatal abort rate | `event:"pipeline.aborted"` count / total count | per-day line + 7-day MA |
| Aborts by code | `event:"pipeline.aborted"` group by `kv.error_code` | pie/bar |
| Degradation mode share | `event:"pipeline.ok"` group by `kv.degradation_mode` | stacked area |
| p95 stage latency | `event:"pipeline.ok"` `kv.stage_latency_ms.total` p95 | per-day line, with per-stage breakdown drill-down |
| Top-10 fired rules | `kv.rules_truthy` rule IDs (LLD adds a `top_rule_id` field) | bar chart, weekly |
| Catalyst-imminent overrides | `kv.severity_level == "CRITICAL_IMMEDIATE_STOP"` count | per-day, with `fault_family == "misfire"` breakdown |

The first three are the v1 launch-gate dashboards. The rest are
nice-to-have for v1, required by v1.1.

### 6.1 Tracing (as-built)

Distributed tracing is wired in `comlab/observability/_tracer.py`. `get_tracer(name)`
returns a real OpenTelemetry tracer when the optional dependency **and** an
exporter/provider are configured, and a `_NoOpTracer` otherwise. The aggregator
and router open one span per pipeline stage and set attributes (resolved horizon,
degradation mode, winner `fault_id`, confidence). The shim is **no-op by default**
— zero added runtime cost when OTel is absent, so the latency envelope in §3 holds
whether or not a collector is attached. Span names mirror the §5.2 event vocabulary
so traces and structured logs correlate.

---

## 7. Build validation script (the CI gate)

Per the build-validation ruling (recorded in `docs/adr/`), every PR against
`comlab/` runs an
automated build-validation script before any reviewer is required to
look. The script lives at `scripts/build_validate.py` and runs as the
sole job of the `comlab-validate` CI workflow.

### 7.1 What the script enforces (in order — fail-fast)

1. **Repo layout.** All paths in `COMLab_LLD.md §2` exist; no
   unexpected extra files in `comlab/config/kg/`.
2. **JSON schema validity.** Every `comlab/config/*.json` parses; the
   registry validates against Pydantic model `RegistryFile` (in-memory) and
   every `comlab/config/kg/*.json` (except `_kg_schema.json` itself)
   validates against `kg/_kg_schema.json`.
3. **Cross-file consistency.** Boot-time §4 phase 3 checks, run
   standalone:
   - registry fault_ids ⊆ kg fault_ids
   - kg fault_ids ⊆ registry fault_ids ∪ {`OPTIMAL_HEALTH`}
   - per-node `fault_family` matches the file's `fault_family`
   - every `differential_siblings` entry resolves
   - no duplicate fault_id across kg files
4. **Enum coverage.** Every `target_horizons` value, every
   `fault_family`, every operator name in the registry is in the
   locked enum vocabulary (`comlab/schemas/vocabulary.py`).
5. **Wiki citation lint.** Every numeric literal in
   `comlab/config/global_fault_registry.json`'s `OperatorClause.value`
   appears in a sibling `comlab/config/global_fault_registry.json`
   `_citations` map keyed by `fault_id` (the editor maintains the
   citation; the script verifies its presence, not its accuracy).
6. **Config size envelope.** `du -b comlab/config/` ≤ 2.5 MB.
7. **Unit + e2e tests.** `pytest -x -q` over `tests/` — must pass.
   Includes §9.4 consistency tests at full strength.
8. **Latency benchmark.** Run the e2e fixtures end-to-end on the
   reference hardware profile (CI runner mapped to the §2.4 spec);
   p95 of `stage_latency_ms.total` ≤ 275 ms (250 ms target + 10 %
   tolerance). Per-stage p95 ≤ 110 % of the §3 allocation.
9. **Ruff + Pyright.** `ruff check` and `pyright` clean on both
   `comlab/` and `tests/`.
10. **Boot smoke test.** Spawn a subprocess that imports `comlab` and
    exits 0; assert clean exit and stderr-free.

Each check is its own log section. The script returns a non-zero exit
code on the first failure with a one-line "fix this" hint.

### 7.2 What the script does NOT do (deliberately)

- It does **not** check the *accuracy* of a wiki citation — only that
  one exists. Accuracy is a reviewer's job (per Q3 two-reviewer rule).
- It does **not** check semantic plausibility of remediation text
  (e.g. "is this a real procedure?") — reviewer's job.
- It does **not** run an external network call.

### 7.3 Two-reviewer rule integration

The PR cannot merge until:

- the CI workflow (`comlab-validate`) is green, AND
- two reviewers approve, AND
- at least one of the two has `CODEOWNERS` on the file path being
  changed (registry vs. each KG family file gets a different
  CODEOWNERS line).

Both gates are enforced by repo branch-protection settings (the DLD
specifies *what* must be enforced; the repo admin owns *how*).

---

## 8. Integration test harness

### 8.1 Fixture sourcing

Fixtures in `tests/fixtures/cases/` are the regression set referenced
by PRD §10 ("Verdict-vs-mechanic-truth agreement ≥ 80 %"). Each case
ships as a pair of files:

```
tests/fixtures/cases/
├── case_001_hpfp_leak/
│   ├── inbound.json              the full OrchestratorInboundRequest payload
│   ├── expected_response.json    the OrchestratorFinalUIOutput we expect
│   └── README.md                 mechanic-confirmed ground truth, post-repair outcome
├── case_002_egr_dilution/
│   ├── inbound.json
│   ├── expected_response.json
│   └── README.md
... (≥ 50 cases for the launch gate)
```

A case's `expected_response.json` may use the special marker
`"<ANY>"` for fields the test does not assert on (e.g. `session_id`
timestamps). The e2e test runner replaces those with deep-equal
wildcards.

### 8.2 Fixture refresh policy

The fixture set grows over the lab's life; existing fixtures are not
edited after merge except by a DLD-revision-grade PR. A change to
KG content that flips an existing fixture's expected verdict is a
red flag — the PR description must include:

- which case(s) flipped,
- a short rationale,
- a re-confirmation of the ground-truth (mechanic note in the case
  README).

This protects against an editor "fixing" the model to match data
instead of fixing data to match the model.

### 8.3 Synthetic stress cases

Beyond real-world cases, `tests/fixtures/cases/` carries synthetic
edge cases — one per error code in §10 of the LLD, one per
degradation mode, one per non-starter symptom path. These guarantee
every documented behaviour has at least one regression anchor.

---

## 9. Cross-version compatibility

### 9.1 `schema_version` matrix

COMLab declares a constant `MIN_SUPPORTED_SCHEMA_VERSION` (currently
"1.0", per `LLD §6.3`). The compatibility matrix is:

| Producer ships | COMLab v1.x accepts | Why |
|---|---|---|
| `vehicle_dna.schema_version == "1.0"` | yes | current |
| `vehicle_dna.schema_version == "1.2"` | yes | minor bumps are backward-compatible additions only |
| `vehicle_dna.schema_version == "0.9"` | no — `ERR-ABORT-005` | pre-stable |
| `vehicle_dna.schema_version == "2.0"` | no — `ERR-ABORT-005` | major bump invalidates v1 reader |

Outbound `OrchestratorFinalUIOutput.schema_version` echoes the
inbound `vehicle_dna.schema_version`. The UI may use this to render
a "your data uses an older schema" hint if it cares; COMLab does not.

### 9.2 KG file `schema_version`

Each `kg/*.json` carries its own `schema_version`. The build-validation
script (§7 step 2) requires every file to declare the same value, and
that value to match the `schema_version` field declared by each KG file's
`_kg_schema.json` (no separate `KG_SCHEMA_VERSION` constant exists in
`comlab/core/fault_atlas_kg.py` — the schema file is the single source of truth). A mismatched file fails the build —
prevents accidentally mixing v1 and v2 KG nodes in one boot.

### 9.3 Backward-compatibility release rule

A new COMLab release may introduce new **optional** output fields
without bumping `schema_version`. Adding a new required field, removing
any field, or restricting an existing field's value range is a major
bump and requires a paired producer release (per
`SEMANTIC_CONTRACT.md §10`).

---

## 10. Deployment model

### 10.1 v1 — in-process library

COMLab v1 ships as a Python package consumed in-process by whichever
4DApp surface assembles the inbound request. The wizard backend
imports `comlab.run_orchestrator(...)` (LLD-defined entry point) and
gets a `dict` back. There is no network hop inside COMLab.

This model is chosen because:

- Boot cost (≤ 1.5 s) amortises across the host process's lifetime.
- 0 ms transport-inside-COMLab — the entire 250 ms budget is real
  work.
- The 80 MB RSS fits comfortably alongside the typical Django/FastAPI
  4DApp backend.

### 10.2 v2 candidate — microservice

When 4DApp scales out and the surrounding backend needs to use COMLab
from multiple language runtimes, COMLab can be promoted to an
HTTP/gRPC microservice without internal restructuring:

- Phase 1 add: a thin FastAPI wrapper at `comlab/api/server.py` (NOT
  in v1) exposing one `POST /diagnose` endpoint.
- Phase 2 add: an OpenAPI spec generated from the existing Pydantic
  schemas — no new types to define.
- Phase 3: containerise; surrounding 4DApp talks HTTP/JSON.

The `comlab/` package boundaries already support this — no business
logic lives in a hypothetical FastAPI layer. v2 is a packaging
exercise.

### 10.3 What we do not deploy

- No background workers, no cron jobs, no scheduled tasks.
- No outbound HTTP from `comlab/*`.
- No filesystem writes from `comlab/*` after boot (audit log goes
  through the stdlib `logging` handler the surrounding app owns).
- No mutation of files under `comlab/config/` at runtime.

---

## 11. Failure modes and recovery

### 11.1 Failure-to-recovery matrix

| Failure | Detection | Recovery | Operator action |
|---|---|---|---|
| Config file missing at boot | Phase 2 of boot (§4) | Process exits non-zero (78) before serving | Restore file from VCS; restart |
| KG/registry drift at boot | Phase 3 of boot (§4) | Process exits non-zero (78) | Fix the offending PR (CI should have caught it — investigate why §7 step 3 passed) |
| Pydantic validation error mid-session | Stage A.1 | Per-session abort `ERR-CONTRACT-001`; pipeline.aborted log; next session unaffected | None — producer-lab regression. Page producer-lab owner if rate spikes. |
| Producer payload field missing that v1 contract requires | Stage A.1 | Per-session abort with field path | Same as above. |
| Registry walk evaluates 0 truthy rules | Stage B step 5 | `OPTIMAL_HEALTH` verdict returned; `stage_b_walk.no_winner` WARN | None — legitimate outcome. Investigate if rate spikes above the historical baseline. |
| KG lookup miss at runtime (`ERR-stage_c_kg.err_lookup_miss`) | Stage C | Should never happen; protected by §7 step 3. If it does → per-session abort, page COMLab owner | Inspect the offending fault_id; verify CI caught the drift |
| Analytics divide-by-zero / NaN | Stage D | Internal stage error caught; pipeline.aborted with internal error | Page COMLab owner; reproduce with the session_id from the log |
| Response serialise failure | Stage E | Same as analytics — caught, internal error | Page COMLab owner |
| Process OOM | host signal | Process killed; restarted by supervisor | Investigate RSS growth — may indicate a regression in §2.1 ceiling |
| Boot time exceeds 1.5 s | startup observability | Process serves, but ops dashboard shows yellow | Investigate config-file growth or new schema validator slowness |

### 11.2 Graceful degradation paths (not failures)

These are by-design and never page anyone:

- `suppress_gaslab` (engine_state == won_not_start) → `degradation_mode == GAS_DOMINANT`,
  pipeline proceeds, PRD §6.3 yellow banner shown.
- `SymptomDNA.engine_state == won_not_start` → producer labs suppressed
  via routing directive, pipeline proceeds with DTC-only evidence.
- `obd_live_data.engine_warmed == false` AND OBDLab suppressed → no
  abort.

### 11.3 No automatic retry inside COMLab

COMLab does not retry a failed session. The user resubmits, and the
new session is a new session (new `session_id`). Retry policy is the
caller's choice. (For schema/contract errors this is correct — retrying
the same payload changes nothing.)

---

## 12. Versioning, release, and rollback

### 12.1 Release cadence

- **Patch (1.0.0 → 1.0.1):** KG content fix, registry threshold tune,
  doc typo. Ships as needed; expected weekly.
- **Minor (1.0 → 1.1):** new optional output field, new KG/registry
  capability behind a flag. Ships ≤ monthly.
- **Major (1.x → 2.0):** breaking schema change. Coordinated with
  producer labs; requires `SEMANTIC_CONTRACT.md §10` RFC.

### 12.2 Rollback model

Every release is a tagged git commit and a versioned Python package.
Rollback is "deploy the previous tag" — no schema migration, no
database, no state-clean-up. The audit log carries the COMLab
`version` field per §5.1 so a post-incident review can correlate
errors with releases.

### 12.3 Canary

For a non-trivial minor or major release, the deploy plan should
route ≤ 10 % of sessions to the new version for ≥ 24 hours before
full cutover. The §6 dashboards (fatal abort rate, fault family
share, p95 latency) compared between canary and primary fleets are
the gate. Specific traffic-shaping mechanism is the infra team's
choice; COMLab is stateless so the split is safe.

---

## 13. Open questions for ops sign-off

Tight, yes/no, to lock in before first production deploy.

1. **Log sink format.** §5 assumes structured JSON on stdout. Confirm
   the surrounding 4DApp infra ingests stdout-JSON, or specify a
   different handler shape.
2. **Reference-hardware mapping in CI.** §7 step 8 requires the CI
   runner to be sized per §2.4. Confirm GitHub-hosted runners satisfy,
   or specify the self-hosted runner spec.
3. **Audit-log retention.** §5.4 emits one line per session. Specify
   retention (recommended ≥ 90 days for the PRD §10 success-metric
   calculations).
4. **Alerting thresholds for §6 dashboards.** Recommend: page when
   abort rate > 10 % over 1 hour, or when p95 latency > 400 ms over
   1 hour. Confirm or override.
5. **Canary traffic-shaping.** §12.3 recommends ≥ 24 h at 10 %. The
   v1 launch volume may not support a meaningful 24-hour canary at
   10 % — propose 5 % for 72 h instead? Defer to ops.
6. **Build-validation script as standalone CLI.** §7 specifies a
   script at `scripts/build_validate.py`. Should the same script be
   callable locally by a domain expert before opening a PR (`make
   validate-kg`)? Recommend: yes; cheap to expose.

---

## 14. References

- `COMLab_HLD.md` — binding architecture; §4 pipeline stages drove §3 latency split.
- `COMLab_LLD.md` — binding file/class spec; §6 modules and §9 test layout drove
  §4 boot sequence and §7 build script.
- `COMLab_PRD.md` — binding user-facing commitments; §7.1 latency and §8
  operational requirements drove §3 and §6.
- `docs/adr/` — decision records (incl. the mandatory build-validation ruling
  behind §7).
- `docs/Vocabulary/SEMANTIC_CONTRACT.md` §10 — change-protocol semver rules
  inherited in §12.
- `wiki/04_horizon_eras.md` — binding scope (petrol 1990–2010, Euro 1–5).
- The shipped `comlab/` package (esp. `observability/_tracer.py`, `config/kg/`).
