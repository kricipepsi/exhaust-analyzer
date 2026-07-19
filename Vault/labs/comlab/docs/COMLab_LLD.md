---
node_type: "lld"
lab: "comlab"
module: "comlab"
subsystem: "low-level-design"
implements:
  - "labs/comlab/comlab/core/lab_pipeline_aggregator.py"
  - "labs/comlab/comlab/core/fault_atlas_router.py"
  - "labs/comlab/comlab/core/fault_atlas_kg.py"
  - "labs/comlab/comlab/core/ecu_hardware_checker.py"
  - "labs/comlab/comlab/core/horizon_context_injector.py"
  - "labs/comlab/comlab/core/perception_contradiction.py"
  - "labs/comlab/comlab/core/symptom_router.py"
  - "labs/comlab/comlab/analytics/delta_engine.py"
  - "labs/comlab/comlab/analytics/power_loss_analytics.py"
  - "labs/comlab/comlab/projection.py"
  - "labs/comlab/comlab/schemas/ingestion.py"
  - "labs/comlab/comlab/schemas/response.py"
  - "labs/comlab/comlab/schemas/vocabulary.py"
  - "labs/comlab/comlab/schemas/lab_dna_views.py"
  - "labs/comlab/comlab/schemas/kg.py"
consumers:
  - "dld: labs/comlab/docs/COMLab_DLD.md"
  - "comlab: labs/comlab/comlab/core/lab_pipeline_aggregator.py five-phase pipeline implementation"
  - "wired: apps/4DLabWired/wired/composition.py LabPipelineAggregator import"
drift_guards:
  - "labs/comlab/tests/unit/test_lab_pipeline_aggregator.py"
  - "labs/comlab/tests/unit/test_fault_atlas_router.py"
  - "labs/comlab/tests/unit/test_fault_atlas_kg.py"
  - "labs/comlab/tests/unit/test_ecu_hardware_checker.py"
  - "labs/comlab/tests/unit/test_horizon_context_injector.py"
  - "labs/comlab/tests/unit/test_perception_contradiction.py"
  - "labs/comlab/tests/unit/test_symptom_router.py"
  - "labs/comlab/tests/unit/test_delta_engine.py"
  - "labs/comlab/tests/unit/test_power_loss_analytics.py"
  - "labs/comlab/tests/unit/test_projection.py"
  - "labs/comlab/tests/unit/test_vocabulary.py"
  - "labs/comlab/tests/e2e/test_diagnostic_engine.py"
tags: [comlab, finished, lld]
source: "labs/comlab/docs/COMLab_LLD.md"
---
# COMLab Low-Level Design (LLD)

**Document type:** LLD — directory blueprint, per-module class/method
signatures, Pydantic schemas, JSON schemas for config artefacts, error-code
taxonomy, and test layout. Implementation-ready spec for the coder.

**Status:** v2.0 — **as-built**, reconciled to the shipped `comlab/` package
(2026-06-21). Supersedes the v1.0 draft (2026-05-21), archived at
`docs/ARCHIVE/COMLab_LLD_v1.0_2026-05-21.md`.

> **Authority note (read first).** The shipped Python in `comlab/schemas/*.py`,
> `comlab/core/*.py`, and `comlab/analytics/*.py` is the **single source of
> truth** for exact field sets, types, and signatures. The snippets in this LLD
> are *representative* — they name the load-bearing types and contracts and call
> out where the code has grown past the v1.0 draft, but they do not re-list every
> field (that would re-introduce drift). Where this doc and the code disagree,
> the code wins; open an issue to correct the doc.

**Scope (binding, per `wiki/04_horizon_eras.md`):** petrol **1990–2010, Euro
1–5**. Post-2010 Euro 6+ technology — GPF/DPF inference, LSPI, secondary-air
injection — is out of scope and absent from every schema. The v1.0
`secondary_air_equipped` field has been **removed** from `EmissionsConfiguration`
accordingly.

**Companion to:** `COMLab_HLD.md` (architecture), `COMLab_PRD.md` (user-facing
behaviour), `COMLab_DLD.md` (resource/ops), `docs/adr/` (decisions),
`COMLab_BDD.md` (behaviour). This LLD inherits every decision from them.

**Out of scope:**

- Resource budgets, latency allocation, CI/build script — `COMLab_DLD.md`.
- Actual rule rows / KG node entries — config data, not code; this LLD specifies
  their *schema*, not their *content*.
- Method bodies. Method *signatures* and *contracts* are in scope.

**Authoritative inputs:**

- `COMLab_HLD.md` §3–§8 — module responsibilities and pipeline stages.
- `COMLab_PRD.md` §4–§6 — gates, error UX, what Screen 6 must consume.
- The six v1.0 rulings, now settled in code and recorded in `docs/adr/` and
  HLD §12: KG as a per-family **directory** (13 files), `user_input_echo_audit`
  COMLab-emitted, `lab_routing_directive` in `execution_meta`,
  `horizon_context_injector.py` filename kept, differential siblings capped at 5.
- `docs/Vocabulary/SEMANTIC_CONTRACT.md` §4, §5, §8 — JSON shapes and enum
  vocabulary.
- `wiki/` — domain truth (esp. `04_horizon_eras`, `07_pipeline_stages`,
  `08_scoring_to_fusion_rework`, `11_two_point_delta`).
- The shipped `comlab/` package — this doc reconciles up to it.

---

## 1. Scope and non-goals

The LLD specifies **types, signatures, and contracts** for every COMLab
module the HLD names. It does not specify method bodies (those belong in
the code), and it does not specify config content (that belongs in
config files).

Two design constraints govern every signature in this document:

1. **Read-only over inputs.** No method in COMLab mutates a
   `VehicleDNA`, producer-lab payload, or any nested dict from them.
   Mutation is via *derived* working dicts created by COMLab.
2. **JSON-only sibling boundaries.** No import statement in `comlab/*`
   names `gaslab`, `obdlab`, `dtclab`, or `dnalab`. The only allowed
   producer-lab types are the local mirrors in
   `comlab/schemas/ingestion.py`.

---

## 2. Directory blueprint (final, post-LLD)

```
labs/comlab/
├── docs/
│   ├── COMLab_HLD.md  COMLab_PRD.md  COMLab_LLD.md  COMLab_DLD.md  COMLab_BDD.md
│   ├── adr/                                    numbered ADRs
│   ├── Vocabulary/  (OBD_/DTC_VOCABULARY.md, SEMANTIC_CONTRACT.md)
│   └── ARCHIVE/     (superseded doc snapshots, read-only history)
├── wiki/            (00_index … 14_sources_appendices — domain truth)
├── pyproject.toml   requirements.txt
├── scripts/
├── registry/                                   repo-root one-way dep (integration_shim)
├── comlab/
│   ├── __init__.py
│   ├── projection.py                          §5  — VehicleDNA dict → LabDnaView
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── vocabulary.py                      §3.1 — enums (cross-lab source of truth)
│   │   ├── ingestion.py                       §3.2 — OrchestratorInboundRequest + mirrors
│   │   ├── response.py                        §3.3 — OrchestratorFinalUIOutput
│   │   ├── kg.py                              §3.4 — KGNode / KGFile
│   │   └── lab_dna_views.py                   §5.1 — Gas/Obd/Dtc views + ProjectedViews
│   ├── core/
│   │   ├── __init__.py
│   │   ├── horizon_context_injector.py        §6.1 — reads resolved_horizon (no VIN parse)
│   │   ├── symptom_router.py                  §6.2 — SymptomDNA → LabRoutingDirective
│   │   ├── lab_pipeline_aggregator.py         §6.3 — Stage A + pipeline entry
│   │   ├── perception_contradiction.py        §6.6 — λ-truth vs λ-perception (NEW)
│   │   ├── ecu_hardware_checker.py            §6.7 — ECU digital-lie detector (NEW)
│   │   ├── fault_atlas_router.py              §6.4 — Stage B 5-phase triage
│   │   └── fault_atlas_kg.py                  §6.5 — KG loader + resolver
│   ├── analytics/
│   │   ├── __init__.py
│   │   ├── power_loss_analytics.py            §7   — Stage D
│   │   └── delta_engine.py                    §7.1 — two-operating-point Δ (NEW)
│   ├── observability/
│   │   ├── __init__.py
│   │   └── _tracer.py                         §6.8 — OTel-or-no-op tracer (NEW)
│   └── config/
│       ├── eras_sensitivity_masks.yaml        per-horizon threshold masks
│       ├── global_fault_registry.json         §8.1
│       ├── symptom_prior.yaml  tag_discriminator.yaml
│       ├── proposals/                          taxonomy_backbone.yaml + entries
│       └── kg/                                §8.2 — 13 per-family files + _kg_schema.json
│           ├── _kg_schema.json
│           ├── lean_condition.json   rich_mixture.json    misfire.json
│           ├── sensor_fault.json     ecu_fault.json       no_fault.json
│           ├── catalyst_failure.json exhaust_leak.json    ignition_fault.json
│           ├── mechanical_wear.json  cam_timing.json      non_starter.json
│           └── invalid_input.json
└── tests/
    ├── __init__.py  conftest.py
    ├── fixtures/    (mock_gas_lab, mock_obd_lab, mock_dtc_lab, descriptor)
    ├── unit/        §9.2 — per-module tests
    ├── e2e/         §9.3 — test_kg_registry_consistency, test_pipeline_round_trip,
    │                       test_error_codes, test_real_routing, test_diagnostic_engine,
    │                       test_delta_router_wiring
    ├── integration/ test_truth_perception
    ├── regression/  test_comlab_regression
    └── generative/  test_combinatorial, test_fuzz
```

**`core/horizon_context_injector.py` keeps its filename** (the v1.0 rename to
`horizon_resolver.py` was not taken). The class drops VIN parsing (§6.1); the
path is stable so test imports do not churn. There is **no `adapters/`
package** — producer-lab types are mirrored directly in `schemas/ingestion.py`.

---

## 3. `comlab/schemas/`

### 3.1 `vocabulary.py` — locked enums

Existing file. Inherits from `SEMANTIC_CONTRACT.md` §8 verbatim. The LLD
adds two enums introduced by this design pass; everything else stays.

```python
# new in this LLD round (added to existing file)

class FaultEnrichmentSeverity(StrEnum):
    """NOT to be confused with PerformanceAnalytics.severity_level.
    
    Tracks the *editor-asserted* severity hint for a KG node when the
    runtime power-loss computation cannot weigh in (e.g. OPTIMAL_HEALTH
    path). NOT used in the FaultAtlas router scoring. Consumer:
    `response.fault_enrichment.editor_severity_hint` only when
    `severity_level == OPTIMAL_HEALTH` and the KG editor wants a
    "monitor closely" cue.
    """
    INFORMATIONAL = "INFORMATIONAL"
    WATCH         = "WATCH"
    REPAIR        = "REPAIR"
    URGENT        = "URGENT"


class LabRoutingDirectiveReason(StrEnum):
    """Why a directive flag was set. Surfaced in execution_meta per Q6.
    
    Consumer: `response.execution_meta.lab_routing_directive.reasons`
    list — UI uses this to render the 'why was this section greyed out'
    copy in PRD §5.6.
    """
    NON_STARTER_NO_EXHAUST        = "NON_STARTER_NO_EXHAUST"        # engine_state == will_not_start
    NON_RUNNING_NO_LIVE_PIDS      = "NON_RUNNING_NO_LIVE_PIDS"      # engine_state in {will_not_start, cranking}
    NON_RUNNING_MONITORS_NOT_READY= "NON_RUNNING_MONITORS_NOT_READY"# engine_state == will_not_start
    COLD_START_HYPOTHESIS         = "COLD_START_HYPOTHESIS"         # occurs_during == cold_only
```

**Decision on `FaultEnrichmentSeverity`:** added now because the open
question PRD §11 Q4 ("OPTIMAL_HEALTH copy variant") may need it; the
field is **optional** and the KG editor may omit it. If product
ultimately says "no, do not add it", the field is dropped and the enum
deleted in a patch — no consumer code shipped yet.

Every other enum in `SEMANTIC_CONTRACT.md §8` (`Horizon`,
`EuroEmissionCategory`, `InductionType`, `AirMeteringStrategy`,
`PrimaryLoadCalculation`, `FuelDeliveryType`, `UpstreamO2Type`,
`RpmStateBucket` / `EngineStateBucket`, `FaultFamily`, `SampleValidity`,
`Mode06Status`, `HistoricalFaultContext`, `DegradationMode`,
`SeverityLevel`, `VinConfidence`, `ConfidenceRating`,
`FuelSystemStatus`, `Mode06MonitorState`, `NodeMAFStatus`,
`NodeMAPStatus`, `O2FailureMode`, `TrimAnalyticsGate`, `VEValidity`,
`DTCRoutingTag`) stays exactly as already defined in the existing
`vocabulary.py`.

### 3.2 `ingestion.py` — `OrchestratorInboundRequest` and friends

Existing file. Extended per `data_flow_report.md` and HLD §7.1. The
T-FX-5 elevation of `symptom_dna` to top-level is already applied.

**Type tree (top-down):**

```python
class OrchestratorInboundRequest(BaseModel):
    """The only inbound shape COMLab accepts. Built by the assembler
    (UI / test harness / demo CLI) per HLD §6.1.
    """
    vehicle_dna:    VehicleDNA
    gas_lab_output: GasLabPayload
    obd_live_data:  OBDLiveDataPayload
    dtc_lab_output: DTCLabPayload
    symptom_dna:    SymptomDNA   # T-FX-5: top-level, not nested

# ----- vehicle_dna (mirror of DNALab's output) -----

class VehicleDNA(BaseModel):
    session_id:     UUID4
    timestamp:      datetime
    schema_version: str = Field(pattern=r"^\d+\.\d+$")
    vin_dna:        VinDNA
    symptom_dna:    Optional[SymptomDNA] = None   # back-compat; new code reads top-level

class VinDNA(BaseModel):
    vin:                          str = Field(min_length=17, max_length=17,
                                              pattern=r"^[A-HJ-NPR-Z0-9]{17}$")  # wiki: VINLab VIN spec
    make:                         str
    model:                        str
    model_year:                   int = Field(ge=1980, le=2099)  # wiki: VINLab model year range
    engine_displacement_liters:   float = Field(gt=0, le=10.0)  # wiki: DNALab vehicle spec
    cylinder_count:               int = Field(ge=2, le=12)  # wiki: DNALab vehicle spec
    number_of_banks:              int = Field(ge=1, le=2)  # wiki: DNALab vehicle spec
    induction_type:               InductionType
    fuel_delivery_type:           FuelDeliveryType
    air_metering_architecture:    AirMeteringArchitecture
    air_metering_strategy:        AirMeteringStrategy
    emissions:                    EmissionsConfiguration
    euro_emission_category:       EuroEmissionCategory
    stress_idle_rpm_target:       int = Field(ge=2800, le=5000)  # wiki: DNALab vehicle spec §stress
    rated_rpm:                    Optional[int] = Field(default=None, ge=1500, le=12000)  # wiki: DNALab vehicle spec §rated
    confidence:                   VinConfidence
    resolved_horizon:             Horizon  # pre-computed by DNALab per NewArchPlan §2

    @model_validator(mode="after")
    def _air_metering_consistency(self) -> "VinDNA":
        """SEMANTIC_CONTRACT §9.3 — booleans must agree with strategy.
        Raises ValueError → ERR-CONTRACT-002 at the gate."""
        ...

class AirMeteringArchitecture(BaseModel):
    has_maf_sensor:           bool
    has_map_sensor:           bool
    primary_load_calculation: PrimaryLoadCalculation

class EmissionsConfiguration(BaseModel):
    upstream_o2_type:         UpstreamO2Type
    downstream_o2_present:    bool
    downstream_trim_role:     DownstreamTrimRole = DownstreamTrimRole.NONE  # O2_MODEL_STRATEGY §3
    egr_equipped:             bool
    has_catalyst:             bool = True   # near-universal; explicit for KG consistency
    # NOTE: secondary_air_equipped REMOVED — SAI is out of scope (Euro 6+ perk; wiki 04 scope reminder).
    # model_validator: downstream_trim_role != NONE requires downstream_o2_present (ERR-CONTRACT-003).

# ----- symptom_dna -----

class SymptomDNA(BaseModel):
    tier_1_primary_symptom: str   # enum source: VehicleDNA.md triage table
    tier_2_subfield_filter: str
    environmental_conditions: EnvironmentalConditions
    free_text_notes:        Optional[str] = None   # logged, not analysed in v1

class EnvironmentalConditions(BaseModel):
    occurs_during: Literal["always", "cold_only", "hot_only", "intermittent"]
    engine_state:  Literal["running", "cranking", "will_not_start"]

# ----- producer payloads (mirrors per data_flow_report) -----

class GasLabPayload(BaseModel):
    chemical_state:   str   # canonical ChemicalSignature label (opaque string at this boundary)
    gas_co:           float = Field(ge=0.0, le=15.0)        # wiki: GAS_VOCABULARY §3
    gas_hc:           int   = Field(ge=0,   le=20000)       # wiki: GAS_VOCABULARY §3
    gas_co2:          float = Field(ge=0.0, le=22.0)        # wiki: GAS_VOCABULARY §3
    gas_o2:           float = Field(ge=0.0, le=22.0)        # wiki: GAS_VOCABULARY §3
    gas_nox:          int   = Field(ge=0,   le=5000)        # wiki: GAS_VOCABULARY §3
    lambda_chem:      float = Field(ge=0.5, le=2.5)         # Brettschneider; wiki: GAS_WIKI §4
    sample_validity:  SampleValidity
    lambda_measured:  float | None = Field(default=None, ge=0.5, le=2.0)  # wiki: GAS_VOCABULARY §2/§6 — optional directly-measured analyser λ; consumer: perception_contradiction.select_perception_lambda (T-FX-7 no-OBD path)

class OBDLiveDataPayload(BaseModel):
    engine_warmed:                bool
    total_trim_correction_delta:  float = Field(ge=-200.0, le=200.0)  # wiki: OBD_VOCABULARY §11
    normalized_obd_lambda:        float | None = Field(default=None, ge=0.7, le=1.3)  # wiki: OBD_VOCABULARY §13 — None when OBD channel absent (T-FX-7 no-OBD fallback)
    ve_pct:                       float = Field(ge=0.0,  le=100.0)    # wiki: OBD_VOCABULARY §16
    ve_validity:                  VEValidity
    rpm_state_bucket:             EngineStateBucket
    trim_analytics_gate:          TrimAnalyticsGate
    o2_failure_mode:              O2FailureMode
    maf_status:                   NodeMAFStatus
    map_status:                   NodeMAPStatus
    freeze_frame_pids:            Optional[FreezeFramePIDs] = None

class DTCLabPayload(BaseModel):
    active_mil:                  bool
    mil_flashing:                bool                                  # wiki: DTC_VOCABULARY §9 (Class A)
    confirmed_dtcs:              list[str] = Field(default_factory=list)
    pending_dtcs:                list[str] = Field(default_factory=list)
    permanent_dtcs:              list[str] = Field(default_factory=list)
    routing_tags:                list[DTCRoutingTag] = Field(default_factory=list)
    mode_06_monitors:            dict[str, Mode06MonitorResult] = Field(default_factory=dict)
    historical_fault_context:    HistoricalFaultContext
    freeze_frame:                FreezeFrameRecord

    @field_validator("confirmed_dtcs", "pending_dtcs", "permanent_dtcs")
    @classmethod
    def _validate_dtc_list(cls, v: list[str]) -> list[str]:
        """Every DTC string must match DTC_REGEX. Wiki: DTC_VOCABULARY §2.3.
        Raises ValueError → ERR-CONTRACT-001 at the gate."""
        ...
```

The `FreezeFrameRecord` (12 mandatory + 7 optional PIDs + 6 derived symptom
flags, incl. `ff_fuel_spark_cut_at_crank` for the no-start branch) and
`Mode06MonitorResult` mirror classes are defined in full in `ingestion.py`.

> **As-built: the producer mirrors carry many more fields than shown.** The
> snippets above are the v1.0 core; the shipped `ingestion.py` has grown each
> mirror to feed the DEP-2…DEP-10 fusion consumers. Notably:
> - `GasLabPayload` adds `gas_co2`/`gas_nox` and six optional `high_idle_*`
>   channels (R3b PID resolver). `chemical_state` is the canonical
>   `ChemicalSignature` label set (an opaque string at this boundary).
> - `OBDLiveDataPayload` widened `total_trim_correction_delta` to **[-254, 254]**
>   (railed STFT+LTFT), and added `total_trim_correction_delta_b2`,
>   `lambda_perception_delta`, `per_bank_trim_delta`, `per_cylinder_misfire_counts`,
>   `ltft_cell_vector`, `control_module_voltage_v` (VPWR pre-check), `w_theo`/
>   `sensor_error_delta` (MAF linearity), `intake_air_temp_c`/`throttle_pos_pct`
>   (ECU-hardware checker), and `fuel_system_status`. Every field names its
>   consumer in a comment.
> - `DTCLabPayload.routing_tags` is the 19-value `DTCRoutingTag` set. **`SAI_HISTORY`
>   is not present** — secondary-air is out of scope (deferred Euro 6+ perk).
> - `OrchestratorInboundRequest` adds the optional `second_operating_point`
>   (`SecondOperatingPointFrame`) consumed by `delta_engine` (§7.1), plus
>   top-level `downstream_trim_role`, `has_catalyst`, and `user_input_echo_audit`.

### 3.3 `response.py` — `OrchestratorFinalUIOutput` extended

Existing file. Extended per HLD §7.4 and ADR-0011. The
extension introduces three new top-level blocks: `differential_siblings`
(nested inside `diagnostic_verdict`), `fault_enrichment`,
`user_input_echo_audit`, and the `lab_routing_directive` sub-block of
`execution_meta`.

```python
HorizonLit         = Literal["HORIZON_LEGACY", "HORIZON_ADAPTIVE", "HORIZON_MODERN"]
DegradationLit     = Literal["FULL_FUSION", "GAS_DOMINANT", "SINGLE_POINT", "FATAL_INCOMPLETE"]  # SINGLE_POINT added by the Δ engine (no second operating-point frame)
ConfidenceLit      = Literal["HIGH_ASSURANCE", "DEGRADED_ASSURANCE", "LOW_CERTAINTY"]
VinConfidenceLit   = Literal["HIGH", "PARTIAL", "NONE"]
SeverityLit        = Literal["CRITICAL_IMMEDIATE_STOP",
                             "WARNING_DEGRADED_PERFORMANCE",
                             "OPTIMAL_HEALTH"]
FaultFamilyLit     = Literal["lean_condition", "rich_mixture", "misfire",
                             "sensor_fault", "ecu_fault", "no_fault",
                             "catalyst_failure", "exhaust_leak", "ignition_fault",
                             "mechanical_wear", "cam_timing", "non_starter"]


class LabRoutingDirectiveOut(BaseModel):
    """Surfaced in execution_meta per Q6 ruling.
    Consumer: PRD §5.6 grey-out panel."""
    suppress_gaslab:          bool
    suppress_obd_live_pids:   bool
    suppress_mode06_ui:       bool
    cold_start_mode:          bool
    reasons:                  list[LabRoutingDirectiveReason] = Field(default_factory=list)


class ExecutionMeta(BaseModel):
    resolved_horizon:               HorizonLit
    degradation_mode:               DegradationLit
    processing_confidence_rating:   ConfidenceLit
    vin_confidence:                 VinConfidenceLit
    lab_routing_directive:          LabRoutingDirectiveOut   # Q6


class DifferentialSiblingOut(BaseModel):
    """Up to 5 total per diagnostic_verdict, per Q1.
    Consumer: PRD §5.3 runner-up panel."""
    fault_id:          str
    fault_name:        str
    confidence_score:  Optional[float] = Field(default=None, ge=0.0, le=1.0)  # wiki: DNALab_TO_COMLab_FLOW §4 scoring
    source:            Literal["runtime", "editor_curated"]   # for UI badge


class DiagnosticVerdict(BaseModel):
    is_fault_detected:        bool
    fault_code:               str   # fault_id
    fault_name:               str
    fault_family:             FaultFamilyLit
    display_headline:         str = Field(max_length=140)  # wiki: PRD §5.1 display constraints
    confidence_score:         float = Field(ge=0.0, le=1.0)  # wiki: DNALab_TO_COMLab_FLOW §4
    differential_siblings:    list[DifferentialSiblingOut] = Field(default_factory=list, max_length=5)  # ADR-0011 (cap 5)


class FaultEnrichment(BaseModel):
    """KG node values projected into the payload.
    Consumer: PRD §5.2."""
    component_group:           str
    impacted_subsystems:       list[str]
    mechanical_failure_mode:   str = Field(max_length=280)  # wiki: KG node spec §fault_profile
    ui_remediation_steps:      list[str] = Field(min_length=1, max_length=8)  # wiki: KG node spec §fault_profile
    editor_severity_hint:      Optional[FaultEnrichmentSeverity] = None   # see §3.1 decision


class PerformanceAnalytics(BaseModel):
    kinetic_power_loss_pct:           float = Field(ge=0.0, le=100.0)  # wiki: OBD_VOCABULARY §18 power-loss bands
    catalyst_efficiency_index_pct:    Optional[float] = Field(default=None, ge=0.0, le=100.0)  # wiki: OBD_VOCABULARY §19 catalyst index
    lambda_perception_delta:          float                                    # lld: §3.3 — signed OBD lambda − GASLab lambda_chem; consumer: UI Lambda Δ metric + sensor-bias classifier (T-FX-6)
    o2_sensor_bias_verdict:           Optional[str] = None                     # lld: §3.3 — O2_SENSOR_BIASED_LOW / O2_SENSOR_BIASED_HIGH / None; consumer: fault-atlas router Stage B + UI perception panel (T-FX-6)
    severity_level:                   SeverityLit


# user_input_echo_audit per Q4 — COMLab-emitted because mobile wizard wipes state

class UserInputEchoFieldGroup(BaseModel):
    """One screen's worth of typed values."""
    screen_id:    Literal["vehicle_context", "gas", "obd", "dtc"]
    label:        str
    fields:       dict[str, Any]   # key = wizard field name, value = raw typed value or None

class UserInputEchoAudit(BaseModel):
    """Consumer: PRD §5.5 — render echo audit on Screen 6."""
    submitted_at:        datetime
    groups:              list[UserInputEchoFieldGroup]


class OrchestratorFinalUIOutput(BaseModel):
    """The full happy-path response shape."""
    session_id:               UUID4
    schema_version:           str
    execution_meta:           ExecutionMeta
    diagnostic_verdict:       DiagnosticVerdict
    fault_enrichment:         FaultEnrichment
    performance_analytics:    PerformanceAnalytics
    user_input_echo_audit:    UserInputEchoAudit


# Error shape per HLD §7.5

class OrchestratorErrorOutput(BaseModel):
    session_id:               UUID4
    schema_version:           str
    execution_meta:           ExecutionMetaAborted   # subset; degradation_mode == FATAL_INCOMPLETE
    error:                    ErrorBody
    user_input_echo_audit:    UserInputEchoAudit     # PRD §5.8 — echo still shown on abort


class ExecutionMetaAborted(BaseModel):
    degradation_mode:         Literal["FATAL_INCOMPLETE"]
    lab_routing_directive:    Optional[LabRoutingDirectiveOut] = None

class ErrorBody(BaseModel):
    error_code:               str   # see §10 taxonomy
    ui_remediation_message:   str
```

**How the echo audit is populated.** The assembler builds
`UserInputEchoAudit` from the wizard form state and **passes it as an
optional field on `OrchestratorInboundRequest`**:

```python
class OrchestratorInboundRequest(BaseModel):
    # ...existing fields...
    user_input_echo_audit: Optional[UserInputEchoAudit] = None
```

COMLab does not generate the echo (it does not know the wizard's field
labels); it **carries it through** verbatim to the response. If the
assembler omits it (e.g. in synthetic test fixtures), COMLab emits a
sentinel value (`groups=[]`) so the response shape remains stable.

### 3.4 `kg.py` — Fault-Atlas KG types (NEW)

New file. Hosts the Pydantic types that mirror the on-disk KG schema
(§8.2).

```python
class KGNode(BaseModel):
    """One fault entry. Mirrors a single object in any kg/*.json file.
    
    Consumer: fault_atlas_kg.FaultAtlasKG.resolve()."""
    fault_name:                str
    fault_family:              FaultFamilyLit
    component_group:           str
    impacted_subsystems:       list[str] = Field(min_length=1, max_length=8)
    mechanical_failure_mode:   str = Field(max_length=280)
    ui_remediation_steps:      list[str] = Field(min_length=1, max_length=8)
    differential_siblings:     list[str] = Field(default_factory=list, max_length=5)
    editor_severity_hint:      Optional[FaultEnrichmentSeverity] = None

class KGFile(BaseModel):
    """The full shape of one kg/<family>.json file."""
    schema_version:  str = Field(pattern=r"^\d+\.\d+$")
    fault_family:    FaultFamilyLit
    nodes:           dict[str, KGNode]   # key = fault_id (e.g. "ERR-E2-MECH-082")
```

---

## 4. (reserved for future schema groups)

Intentionally empty section to keep numbering aligned with HLD.

---

## 5. `comlab/projection.py` and `comlab/schemas/lab_dna_views.py` (NEW)

The projector promised in HLD §6.

### 5.1 `comlab/schemas/lab_dna_views.py`

Three frozen Pydantic models with the field lists from
`data_flow_report.md` §1 / §2 / §3. Each carries `confidence` and
`resolved_horizon` per HLD §6.3.

```python
class GasLabDnaView(BaseModel):
    model_config = ConfigDict(frozen=True)
    engine_displacement_liters: float
    cylinder_count:             int
    number_of_banks:            int
    euro_emission_category:     EuroEmissionCategory
    fuel_delivery_type:         FuelDeliveryType
    induction_type:             InductionType
    upstream_o2_type:           UpstreamO2Type
    has_catalyst:               bool
    egr_equipped:               bool
    target_lambda_v112:         Optional[float] = None
    co_low_idle:                Optional[float] = None
    co_high_idle:               Optional[float] = None
    confidence:                 VinConfidence
    resolved_horizon:           Horizon


class ObdLabDnaView(BaseModel):
    model_config = ConfigDict(frozen=True)
    engine_displacement_liters: Optional[float]
    cylinder_count:             Optional[int]
    rated_rpm:                  Optional[int]
    stress_idle_rpm_target:     Optional[int]
    air_metering_strategy:      AirMeteringStrategy
    upstream_o2_type:           UpstreamO2Type
    induction_type:             InductionType
    egr_equipped:               bool
    resolved_horizon:           Horizon
    confidence:                 VinConfidence


class DtcLabDnaView(BaseModel):
    model_config = ConfigDict(frozen=True)
    make:                       str
    model_year:                 int
    euro_emission_category:     EuroEmissionCategory
    air_metering_strategy:      AirMeteringStrategy
    resolved_horizon:           Horizon
    has_catalyst:               bool
    egr_equipped:               bool
    confidence:                 VinConfidence
```

A fourth model, `ProjectedViews(gas, obd, dtc)` (also frozen), bundles all three;
`project_all(vehicle_dna_json) -> ProjectedViews` is what `fault_atlas_router`
holds for the lifetime of one session. `project()` reads VIN fields from the
**top-level** `vin_dna` block (e.g. `vin.get("target_lambda_v112")`), with a
`_horizon_from_euro()` fallback when `resolved_horizon` is absent from older
payloads (DEP-4 — pure projection path, no upstream contract gap).

### 5.2 `comlab/projection.py`

```python
def project(
    vehicle_dna_json: dict,
    *,
    target: Literal["gas", "obd", "dtc"],
) -> GasLabDnaView | ObdLabDnaView | DtcLabDnaView:
    """Project a full VehicleDNA JSON dict into the requested LabDnaView.
    
    Precondition: vehicle_dna_json conforms to the VehicleDNA schema
        (§3.2). Caller is responsible for the schema check.
    Postcondition: returned model is frozen; mutation raises.
    Raises: pydantic.ValidationError if a required field is missing
        from the source DNA (signals upstream DNALab regression —
        producer test should have caught it).
    """
    ...


def project_all(vehicle_dna_json: dict) -> ProjectedViews:
    """Convenience: project once into all three views.
    
    Returned tuple-shaped model is what fault_atlas_router holds for
    the lifetime of one session.
    """
    ...


class ProjectedViews(BaseModel):
    model_config = ConfigDict(frozen=True)
    gas: GasLabDnaView
    obd: ObdLabDnaView
    dtc: DtcLabDnaView
```

**No cross-lab import.** `project()` is a pure dict-to-Pydantic
operation. The sibling labs do not import this module; they mirror
their own view internally (per HLD §6.1).

---

## 6. `comlab/core/` — pipeline modules

### 6.1 `horizon_context_injector.py` — rewritten in place

**Filename kept (Q5 ruling).** Internal class signature changes
significantly — the v0.1 stub parsed VINs; the v1 implementation reads
pre-computed values from `VehicleDNA`.

```python
@dataclass(frozen=True)
class HorizonContext:
    """Final output of Stage A horizon resolution."""
    resolved_horizon:  Horizon
    cylinder_count:    int
    number_of_banks:   int
    threshold_mask:    dict[str, Any]   # from eras_sensitivity_masks.yaml


class HorizonContextInjector:
    """Reads VehicleDNA, returns HorizonContext.
    
    Does NOT parse the VIN. Does NOT compute the horizon. Both are
    pre-supplied by DNALab. The injector's job collapsed to:
      1. read vehicle_dna.vin_dna.resolved_horizon (or derive from
         euro_emission_category if a v1.0 DNALab payload omits it)
      2. read vehicle_dna.vin_dna.cylinder_count and number_of_banks
      3. load the era-sensitivity threshold mask from yaml
    """

    def __init__(self, masks_yaml_path: str | Path):
        """Loads eras_sensitivity_masks.yaml once. Cached for the
        lifetime of the COMLab process."""
        ...

    def from_vehicle_dna(self, vehicle_dna: VehicleDNA) -> HorizonContext:
        """The only public method. Pure function over a parsed DNA."""
        ...

    # Internal — derive horizon from euro_emission_category when DNALab
    # ships a payload without resolved_horizon. SEMANTIC_CONTRACT §6.4.
    @staticmethod
    def _horizon_from_euro(category: EuroEmissionCategory) -> Horizon:
        ...
```

**Removed from the v0.1 stub:** `parse_vin_dna`, `resolve_horizon(vin)`,
the `_VIN_REGEX` constant. VIN handling is no longer COMLab's concern.

### 6.2 `symptom_router.py`

Existing file. One signature change: the result type now carries
`reasons: list[LabRoutingDirectiveReason]` so the response can render
the PRD §5.6 copy.

```python
@dataclass(frozen=True)
class LabRoutingDirective:
    suppress_gaslab:           bool
    suppress_obd_live_pids:    bool
    suppress_mode06_ui:        bool
    cold_start_mode:           bool
    reasons:                   tuple[LabRoutingDirectiveReason, ...]


def route_symptom(symptom_dna: SymptomDNA | dict) -> LabRoutingDirective:
    """Reads SymptomDNA, returns the directive.
    
    Routing rules (verbatim from data_flow_report §5.3 / DNALab_TO_COMLab §4 Stage B):
      engine_state == won_not_start  → suppress_gaslab, suppress_obd_live_pids,
                                       suppress_mode06_ui + reason NON_STARTER_NO_EXHAUST
      engine_state == cranking       → suppress_obd_live_pids
                                       + reason NON_RUNNING_NO_LIVE_PIDS
      occurs_during == cold_only     → cold_start_mode
                                       + reason COLD_START_HYPOTHESIS
    """
    ...
```

Accepts both the Pydantic `SymptomDNA` and a raw dict — keeps the
function callable from places that have not yet parsed (e.g. the
fallback tree).

### 6.3 `lab_pipeline_aggregator.py` — Stage A completed

Existing skeleton; methods given full signatures here. Methods raise
`AggregatorAbort` with the §10 error codes.

```python
class AggregatorAbort(RuntimeError):
    def __init__(self, error_code: str, ui_remediation_message: str): ...


class SanitizedPayload(TypedDict):
    """Working dict that flows from Stage A into Stage B."""
    request:             OrchestratorInboundRequest
    horizon_ctx:         HorizonContext
    routing_directive:   LabRoutingDirective
    degradation_mode:    DegradationMode
    projected_views:     ProjectedViews
    # plus the original payloads accessible by attribute on `request`


class LabPipelineAggregator:

    MIN_SUPPORTED_SCHEMA_VERSION: ClassVar[str] = "1.0"

    def __init__(self, horizon_injector: HorizonContextInjector): ...

    # Stage A step 1
    def validate_payload(self, raw_input: dict) -> OrchestratorInboundRequest:
        """Pydantic gate.
        Raises pydantic.ValidationError → caller wraps as ERR-CONTRACT-001/002."""
        ...

    # Stage A step 2
    def check_schema_version(self, vehicle_dna: VehicleDNA) -> None:
        """Raises AggregatorAbort(ERR-ABORT-005) on too-old client."""
        ...

    # Stage A steps 3 + 4
    def run_fatal_gates_and_routing(
        self,
        request: OrchestratorInboundRequest,
    ) -> LabRoutingDirective:
        """Compute routing directive first (because it gates which
        fatal checks apply). Then run the three fatal gates honouring
        the suppression flags.
        
        Raises AggregatorAbort(ERR-ABORT-001 | ERR-ABORT-002 | ERR-ABORT-004).
        """
        ...

    # Stage A step 5
    def classify_degradation(
        self,
        request: OrchestratorInboundRequest,
        directive: LabRoutingDirective,
    ) -> DegradationMode:
        """FULL_FUSION | GAS_DOMINANT — per HLD §4.1 step 5."""
        ...

    # Stage A steps 6 + 7
    def sanitize_and_aggregate(self, raw_input: dict) -> SanitizedPayload:
        """End-to-end Stage A entry point. Calls all of the above in order."""
        ...
```

### 6.4 `fault_atlas_router.py` — Stage B completed

```python
class TriageVerdict(TypedDict):
    """Internal — passed from execute_triage_loop into the serializer."""
    winner:           Optional[RegistryRow]          # None means OPTIMAL_HEALTH
    winner_score:     float
    runner_ups:       list[tuple[RegistryRow, float]]  # at most 3 — HLD §4.2 step 8


class FaultAtlasRouter:

    def __init__(
        self,
        registry_path: str | Path,
        kg: FaultAtlasKG,                 # injected — §6.5
        analytics: PowerLossAnalytics,    # injected — §7
    ): ...

    # §4.2 step 1
    def _load_registry(self) -> list[RegistryRow]: ...

    # §4.2 step 6 — relational operators
    @staticmethod
    def evaluate_operator(
        operator: Literal["EQUALS", "IN_RANGE", "GREATER_THAN", "LESS_THAN",
                          "LESS_THAN_OR_EQUAL", "GREATER_THAN_OR_EQUAL",
                          "DEVIATES_FROM_TARGET"],
        runtime_value: Any,
        rule_value:    Any,
    ) -> bool: ...

    # §4.2 steps 2 + 3 + 4
    def _prune_candidates(
        self,
        rows: Iterable[RegistryRow],
        horizon: Horizon,
        vin_dna: VinDNA,
        symptom_dna: SymptomDNA,
        routing_tags_with_synthetic: list[DTCRoutingTag],
    ) -> list[RegistryRow]: ...

    # §4.2 step 5 + scoring
    def execute_triage_loop(self, sanitized: SanitizedPayload) -> TriageVerdict: ...

    # §4.2 step 7 — catalyst-damage-imminent override
    def apply_catalyst_damage_override(
        self,
        verdict: TriageVerdict,
        request: OrchestratorInboundRequest,
        analytics_result: PerformanceAnalytics,
    ) -> PerformanceAnalytics:
        """If mil_flashing && any P030x in confirmed_dtcs:
        force severity_level = CRITICAL_IMMEDIATE_STOP. Returns the
        possibly-mutated analytics block."""
        ...

    # §4.4 → §4.5 — end-to-end
    def route(self, sanitized: SanitizedPayload) -> OrchestratorFinalUIOutput:
        """Stage B + Stage C + Stage D + Stage E in order:
          1. execute_triage_loop
          2. fault_atlas_kg.resolve(winner.fault_id) → FaultEnrichment
          3. analytics.compute(...)
          4. apply_catalyst_damage_override
          5. assemble OrchestratorFinalUIOutput
        """
        ...

    def _merge_differential_siblings(
        self,
        runtime_runner_ups: list[tuple[RegistryRow, float]],   # ≤ 3 per Q1
        editor_curated:     list[str],                          # fault_ids from KG node
    ) -> list[DifferentialSiblingOut]:
        """Union, dedupe by fault_id, cap at 5. Editor-curated entries
        have confidence_score=None unless they happen to be in the
        runtime runner-up set (then runtime score wins, source becomes
        'runtime')."""
        ...
```

### 6.5 `fault_atlas_kg.py` — NEW

The KG loader and resolver promised in HLD §5.

```python
class FaultAtlasKG:
    """Read-only Fault-Atlas Knowledge Graph.
    
    Loaded once at boot from comlab/config/kg/*.json (13 per-family
    files). Cached as one flat dict[fault_id, KGNode] for O(1)
    runtime lookup.
    """

    def __init__(self, kg_directory: str | Path):
        """Load all kg/*.json files matching the schema in §8.2.
        
        Raises FileNotFoundError if no files match.
        Raises KGConsistencyError if any node fails KGNode validation
            or if two files declare the same fault_id.
        """
        ...

    @property
    def all_fault_ids(self) -> frozenset[str]: ...

    def resolve(self, fault_id: str) -> KGNode:
        """O(1) lookup. Raises KeyError on miss — caller (router)
        must guarantee the fault_id came from the registry."""
        ...

    def resolve_with_default(self, fault_id: str | None) -> FaultEnrichment:
        """Used for OPTIMAL_HEALTH path (fault_id is None) — returns
        a sentinel FaultEnrichment with the 'no fault' KG node."""
        ...


class KGConsistencyError(RuntimeError):
    """KG/Registry cross-reference failed, or duplicate fault_id, or
    schema-invalid node. Build-time / boot-time error, never runtime."""
```

The consistency check between KG and registry runs as a unit test
(§9.4) and as part of the build-validation script (`COMLab_DLD.md` §7).
It is NOT a runtime check on every request — runtime treats the KG as
trusted; the test suite is the gate.

### 6.6 `perception_contradiction.py` — λ-truth vs λ-perception (as-built)

Pure-function module (no class state) comparing OBDLab's perceived lambda against
GASLab's Brettschneider `lambda_chem`. Runs in Stage A before the router.

```python
def select_perception_lambda(*, normalized_obd_lambda: float | None,
                             lambda_measured: float | None) -> float | None:
    """OBD lambda wins when present; else GASLab's directly-measured λ
    (T-FX-7 no-OBD path); else None (detector goes inert)."""

@dataclass(frozen=True)
class PerceptionContradictionResult:
    lambda_perception_delta: float           # signed: perception − chemistry
    bias_verdict: ChemicalSignature | None   # O2_SENSOR_BIASED_LOW/HIGH or None

def detect(*, lambda_chem, normalized_obd_lambda, era_lambda_tolerance,
           downstream_trim_role, has_catalyst,
           control_module_voltage_v=None, enable_vpwr_gate=False
           ) -> PerceptionContradictionResult: ...

def detect_compensated_rich(*, lambda_chem, total_trim_correction_delta,
                            obd_lambda, era_lambda_tolerance,
                            rich_dtc_present) -> CompensatedRichResult: ...
```

Surfaces an `O2_SENSOR_BIASED_*` verdict only when λ diverges beyond the era
tolerance while gas chemistry is near-normal (Lambda-Truth filter). A
`SECONDARY_FUEL_TRIM` downstream role qualifies "healthy sensor" agreement as
weak evidence. The optional VPWR gate (`_VPWR_LOW_V=12.0` / `_VPWR_HIGH_V=15.0`)
rules out a drifting rail before attributing bias (DEP-10). Outputs populate
`PerformanceAnalytics.lambda_perception_delta` / `o2_sensor_bias_verdict`.

### 6.7 `ecu_hardware_checker.py` — ECU digital-lie detector (as-built, DEP-9)

```python
@dataclass(frozen=True)
class ECUHardwareVerdict:
    is_ecu_hardware_fault: bool
    confidence: float                # _ECU_HW_CONFIDENCE = 0.80
    reason: str

class ECUHardwareChecker:
    def check(self, *, intake_air_temp_c, throttle_pos_pct,
              total_trim_correction_delta, per_bank_trim_delta) -> ECUHardwareVerdict: ...
```

Flags the digital-lie signature — railed IAT (`-40 °C` floor), railed TPS
(`100 %`), railed trims (`±25 %`) with broken bank symmetry (`5 %`). All bounds
carry `wiki: 02_lab_input_contract.md §2a` citations. Consumed by the router's
Phase 5 when `enable_ecu_hw=True`.

### 6.8 `observability/_tracer.py` — tracer shim (as-built)

`get_tracer(name)` returns an OpenTelemetry tracer when the optional dependency
and an exporter are configured, otherwise a `_NoOpTracer` whose spans are inert.
The aggregator and router open a span per stage and set attributes (resolved
horizon, degradation mode, winner fault_id, confidence). No-op by default — zero
runtime cost when OTel is absent. See `COMLab_DLD.md` §6.

---

## 7. `comlab/analytics/power_loss_analytics.py`

```python
class PowerLossAnalytics:

    def compute(
        self,
        request: OrchestratorInboundRequest,
        cylinder_count: int,
    ) -> PerformanceAnalytics:
        """Stage D — returns the populated PerformanceAnalytics block.
        
        Calculates:
          - kinetic_power_loss_pct from gas chemistry deltas + cylinder
            dilution per OBD_VOCABULARY §18 (citations in inline comments)
          - catalyst_efficiency_index_pct from upstream/downstream O₂
            ratios — only when vin_dna.emissions.downstream_o2_present
            == True; else returns None for that field
          - severity_level mapping power_loss_pct + chemistry state into
            CRITICAL/WARNING/OPTIMAL bands per the registry
        
        lambda_perception_delta and o2_sensor_bias_verdict are populated
        earlier by the perception-contradiction detector (Stage A,
        ``lab_pipeline_aggregator.py``) — Stage D passes them through
        unchanged. See ``comlab/core/perception_contradiction.py`` (T-FX-6).
        
        Pure function; no I/O.
        """
        ...
```

Numeric literals inside the bodies (band boundaries for severity, the
catalyst ratio constants, the dilution coefficient) carry wiki
citations as inline comments per the project numeric-literal rule.

### 7.1 `comlab/analytics/delta_engine.py` — two-operating-point Δ (as-built, NEW)

Stateless cross-state delta calculator. The emitter labs stay single-point; the
cross-state Δ math lives here (`wiki: delta-relations/07`).

```python
class DeltaSignature(BaseModel):
    """Typed Δ result: ΔTrim / Δgas / ΔO2 sub-results + degradation flag."""
    ...

class DeltaEngine:
    def compute_delta_signature(
        self, request: OrchestratorInboundRequest) -> DeltaSignature:
        """When request.second_operating_point is None → _single_point_sentinel()
        (degradation SINGLE_POINT). Else difference the elevated frame against the
        primary low-idle channels and assemble the signature."""

    def apply_rank_score(self, sig: DeltaSignature, candidates) -> ...:
        """Phase-5 rank term: a Δ-matched fault family is promoted above the
        base-weighted static signatures (the fallback)."""
```

Mandatory gates before any ΔTrim profile is applied: an **architecture gate**
(`_architecture_gate` — MAP-only nulls ΔTrim for a real leak; forced induction
inverts ΔTrim sign) and a **validity gate** (`_validity_gate` — per-frame
sample_validity, dilution, RPM-settled). Each band check ABSTAINs on an
`rpm_state_bucket` mismatch rather than differencing across regimes. Wired into
`fault_atlas_router.execute_triage_loop` Phase 5 via `enable_delta=True`.

---

## 8. Config schemas

### 8.1 `global_fault_registry.json`

JSON Schema (Draft-07) for the registry file. Validated at boot.

```jsonc
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "COMLab Global Fault Registry",
  "type": "object",
  "required": ["schema_version", "registry"],
  "properties": {
    "schema_version": { "type": "string", "pattern": "^\\d+\\.\\d+$" },
    "registry": {
      "type": "array",
      "items": { "$ref": "#/definitions/RegistryRow" }
    }
  },
  "definitions": {
    "RegistryRow": {
      "type": "object",
      "required": [
        "fault_id", "target_horizons", "preconditions",
        "cross_domain_matrix", "confidence_scoring"
      ],
      "properties": {
        "fault_id":            { "type": "string", "pattern": "^ERR-[A-Z0-9-]+$" },
        "target_horizons":     {
          "type": "array",
          "items": { "enum": ["HORIZON_LEGACY", "HORIZON_ADAPTIVE", "HORIZON_MODERN"] }
        },
        "preconditions":       {
          "type": "object",
          "description": "Hardware/architecture predicates that must hold.",
          "properties": {
            "induction_type":             { "type": "string" },
            "egr_equipped":               { "type": "boolean" },
            "fuel_delivery_type":         { "type": "string" }
          }
        },
        "cross_domain_matrix": { "$ref": "#/definitions/CrossDomainMatrix" },
        "fallback_strategy":   { "enum": ["REQUIRE_MATCH", "PROCEED_ON_MATCH_OR_EMPTY", "PROCEED"] },
        "confidence_scoring":  {
          "type": "object",
          "required": ["base_weight"],
          "properties": {
            "base_weight":         { "type": "number", "minimum": 0.0, "maximum": 1.0 },
            "bonus_on_dtc_match":  { "type": "number", "minimum": 0.0, "maximum": 0.5 }
          }
        }
      }
    },
    "CrossDomainMatrix": {
      "type": "object",
      "properties": {
        "gas_lab_state": { "type": "string" },
        "obd_live_pids": {
          "type": "object",
          "additionalProperties": { "$ref": "#/definitions/OperatorClause" }
        },
        "dtc_clause": {
          "type": "object",
          "properties": {
            "any_of_routing_tags":  { "type": "array", "items": { "type": "string" } },
            "any_of_confirmed_dtcs":{ "type": "array", "items": { "type": "string" } }
          }
        }
      }
    },
    "OperatorClause": {
      "type": "object",
      "required": ["operator", "value"],
      "properties": {
        "operator": {
          "enum": ["EQUALS", "IN_RANGE", "GREATER_THAN", "LESS_THAN",
                   "LESS_THAN_OR_EQUAL", "GREATER_THAN_OR_EQUAL",
                   "DEVIATES_FROM_TARGET"]
        },
        "value": {}
      }
    }
  }
}
```

The registry rows **do not carry** `fault_name`, `component_group`,
`mechanical_failure_mode`, `ui_remediation_steps` — those belong in the
KG (§5.5 of HLD: strict separation). No `ui_diagnostic_string` either
(it became `mechanical_failure_mode` in the KG node).

### 8.2 `kg/_kg_schema.json` and per-family files (Q2 ruling)

**Directory layout:**

```
comlab/config/kg/
├── _kg_schema.json          ← single JSON Schema, applied to every other file in the dir
├── lean_condition.json
├── rich_mixture.json
├── misfire.json
├── sensor_fault.json
├── ecu_fault.json
├── no_fault.json            ← contains the sentinel "OPTIMAL_HEALTH" node
├── catalyst_failure.json
├── exhaust_leak.json
├── ignition_fault.json
├── mechanical_wear.json
├── cam_timing.json
└── non_starter.json
```

Twelve files match the twelve values of `FaultFamily`. The loader globs the
directory at boot, validates each file against `_kg_schema.json`,
loads each into the flat `dict[fault_id, KGNode]`, and aborts boot on
schema failure or duplicate fault_id across files.

**`_kg_schema.json` (the schema mirror of `KGFile` in §3.4):**

```jsonc
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "COMLab Fault-Atlas KG File",
  "type": "object",
  "required": ["schema_version", "fault_family", "nodes"],
  "properties": {
    "schema_version": { "type": "string", "pattern": "^\\d+\\.\\d+$" },
    "fault_family":   {
      "enum": ["rich_mixture", "lean_condition", "misfire",
               "sensor_fault", "ecu_fault", "no_fault",
               "catalyst_failure", "exhaust_leak", "ignition_fault",
               "mechanical_wear", "cam_timing", "non_starter"]
    },
    "nodes": {
      "type": "object",
      "patternProperties": {
        "^.+$": { "$ref": "#/definitions/KGNode" },
        "^OPTIMAL_HEALTH$": { "$ref": "#/definitions/KGNode" }
      },
      "additionalProperties": false
    }
  },
  "definitions": {
    "KGNode": {
      "type": "object",
      "required": [
        "fault_name", "fault_family", "component_group",
        "impacted_subsystems", "mechanical_failure_mode",
        "ui_remediation_steps"
      ],
      "properties": {
        "fault_name":               { "type": "string" },
        "fault_family":             {
          "enum": ["rich_mixture", "lean_condition", "misfire",
                   "sensor_fault", "ecu_fault", "no_fault",
                   "catalyst_failure", "exhaust_leak", "ignition_fault",
                   "mechanical_wear", "cam_timing", "non_starter"]
        },
        "component_group":          { "type": "string", "minLength": 1 },
        "impacted_subsystems":      {
          "type": "array",
          "minItems": 1, "maxItems": 8,
          "items": { "type": "string", "minLength": 1 }
        },
        "mechanical_failure_mode":  { "type": "string", "maxLength": 280 },
        "ui_remediation_steps":     {
          "type": "array",
          "minItems": 1, "maxItems": 8,
          "items": { "type": "string", "minLength": 1 }
        },
        "differential_siblings":    {
          "type": "array",
          "maxItems": 5,
          "items": { "type": "string", "pattern": "^ERR-[A-Z0-9-]+$" }
        },
        "editor_severity_hint":     {
          "enum": ["INFORMATIONAL", "WATCH", "REPAIR", "URGENT"]
        }
      },
      "additionalProperties": false
    }
  }
}
```

**Cross-file rules** (enforced by the loader and §9.4 test, not by
JSON Schema):

1. Every `fault_id` in the registry must have exactly one
   corresponding key in some KG file's `nodes` map.
2. Every key in any KG file's `nodes` map must appear in the registry
   (with one exception: `OPTIMAL_HEALTH`, the sentinel, which lives in
   `no_fault.json` and is not a registry row).
3. The `fault_family` field on a node must match the file's
   `fault_family` value (no rich_mixture nodes in misfire.json).
4. Every `differential_siblings` entry must resolve to a fault_id
   that exists in the union of all KG files.
5. No duplicate fault_id across files.

### 8.3 `eras_sensitivity_masks.yaml` (existing)

No LLD-level change. The schema is the existing dict-of-dicts keyed
by `Horizon` enum value. Documented in OrchestratorLabBP archive.

---

## 9. `tests/` — layout and required tests

### 9.1 `tests/fixtures/`

```
tests/fixtures/
├── vehicle_dna/
│   ├── vehicle_dna_ford_mustang_2017.json    (HORIZON_MODERN, EURO_6, GDI, WB AFR)
│   ├── vehicle_dna_volkswagen_1998.json      (HORIZON_LEGACY, EURO_2, port-inj, NB)
│   └── ...                                   one per representative archetype
├── inbound/
│   ├── inbound_full_fusion.json
│   ├── inbound_gas_dominant_legacy.json
│   ├── inbound_non_starter_no_gas.json
│   ├── inbound_cold_engine_aborts.json       (ERR-ABORT-002)
│   ├── inbound_invalid_gas_sample.json       (ERR-ABORT-001)
│   ├── inbound_vin_none_aborts.json          (ERR-ABORT-004)
│   ├── inbound_bad_dtc_string.json           (ERR-CONTRACT-001)
│   └── inbound_air_metering_drift.json       (ERR-CONTRACT-002)
└── cases/
    └── (paired inbound + expected verdict for the e2e regression set)
```

### 9.2 `tests/unit/`

Per-module test files; one per `comlab/*` module that contains real
logic:

```
tests/unit/
├── test_vocabulary.py                test enum stability (any reorder → break)
├── test_ingestion_schema.py          pydantic gate coverage; bad inputs raise
├── test_response_schema.py           output payload shape conformance
├── test_kg_types.py                  KGNode/KGFile validation
├── test_lab_dna_views.py             three frozen views; frozen-ness enforced
├── test_projection.py                full DNA in, exact field set out per view
├── test_horizon_context_injector.py  no VIN parsing; reads DNA fields
├── test_symptom_router.py            7+ routing tables verified
├── test_lab_pipeline_aggregator.py   each gate, each error code
├── test_fault_atlas_router.py        operator coverage, pruning, scoring,
│                                     POA injection, catalyst-damage override,
│                                     differential merging cap at 5
├── test_fault_atlas_kg.py            loader, resolve, OPTIMAL_HEALTH sentinel
└── test_power_loss_analytics.py      math against cited reference values
```

### 9.3 `tests/e2e/`

End-to-end pipeline tests using the fixtures in §9.1.

### 9.4 `tests/e2e/test_kg_registry_consistency.py` (critical)

The most important test in the suite. Validates the KG/Registry
contract at every commit.

```python
def test_every_registry_fault_id_has_a_kg_node(registry, kg):
    missing = set(registry.fault_ids) - kg.all_fault_ids
    assert not missing, f"Registry rows without KG nodes: {missing}"

def test_every_kg_node_has_a_registry_row(registry, kg):
    extra = kg.all_fault_ids - registry.fault_ids - {"OPTIMAL_HEALTH"}
    assert not extra, f"KG nodes without registry rows: {extra}"

def test_kg_node_family_matches_file_family(kg_loader):
    for path, kg_file in kg_loader.per_file().items():
        for fault_id, node in kg_file.nodes.items():
            assert node.fault_family == kg_file.fault_family, (
                f"{path}: {fault_id} declared {node.fault_family!r} "
                f"but lives in {kg_file.fault_family!r} file"
            )

def test_differential_siblings_resolve(kg):
    for fid, node in kg.iter_all():
        for sibling_fid in node.differential_siblings:
            assert sibling_fid in kg.all_fault_ids, (
                f"{fid} references unknown differential_sibling {sibling_fid}"
            )

def test_no_duplicate_fault_ids_across_files(kg_loader):
    # Already enforced by FaultAtlasKG.__init__; this test asserts the
    # boot-time error fires correctly given a planted duplicate.
    ...
```

Build-validation in `COMLab_DLD.md` §7 runs this test as a CI gate.

### 9.5 `tests/e2e/test_pipeline_round_trip.py`

For each fixture in `tests/fixtures/cases/`, runs the full pipeline
and asserts the response matches the fixture's expected verdict
file. Parameterised; failures point at the case ID so the fix is
locatable.

### 9.6 `tests/e2e/test_error_codes.py`

Walks every error code in §10 and asserts the corresponding fixture
triggers it cleanly with the right `ui_remediation_message` template.

---

## 10. Error-code taxonomy

Inherited verbatim from `DNALab_TO_COMLab_FLOW.md §6`; no new codes
introduced by this LLD round.

| Code | Stage | Trigger | Raised by |
|---|---|---|---|
| `ERR-CONTRACT-001` | A.1 | Pydantic validation (regex/range/missing) | `validate_payload` |
| `ERR-CONTRACT-002` | A.1 | Cross-field consistency (`air_metering_strategy` ↔ booleans) | `VinDNA._air_metering_consistency` |
| `ERR-CONTRACT-003` | A.1 | `downstream_trim_role != NONE` but `downstream_o2_present == False` | `EmissionsConfiguration._downstream_trim_role_implies_sensor` |
| `ERR-ABORT-001` | A.3 | `gas_lab_output.sample_validity not in {"VALID", "BORDERLINE"}` (GASLab not suppressed) | `run_fatal_gates_and_routing` |
| `ERR-ABORT-002` | A.3 | `obd_live_data.engine_warmed != True` (OBDLab not suppressed) | `run_fatal_gates_and_routing` |
| `ERR-ABORT-004` | A.3 | `vehicle_dna.vin_dna.confidence == "NONE"` | `run_fatal_gates_and_routing` |
| `ERR-ABORT-005` | A.2 | `vehicle_dna.schema_version < MIN_SUPPORTED_SCHEMA_VERSION` | `check_schema_version` |
| `ERR-VIN-400` | A.1 | VIN format invalid (raised inside VinDNA pydantic gate) | `validate_payload` |

User-facing copy is owned by PRD §6.2.

---

## 11. Inner-loop expectations

This LLD imposes the following CI gates on every change to `comlab/*`:

1. `ruff check comlab/ tests/` — clean.
2. `pyright comlab/ tests/` — clean (strict mode preferred; minimum
   `basic` mode required).
3. `pytest -x -q tests/` — every test passes; first-failure stops the
   run. The KG/registry consistency test (§9.4) must be in the
   default run.
4. Build-validation script (`COMLab_DLD.md §7`) — clean.

Every wiki-cited numeric literal added in this round (registry
thresholds, KG `mechanical_failure_mode` content rules, analytics
constants) carries a comment with the citation. Lint rule deferred to
the DLD.

---

## 12. References

- `COMLab_HLD.md` — architecture (binding).
- `COMLab_PRD.md` — user-facing behaviour (sibling).
- `COMLab_DLD.md` — resource/operational specification (sibling).
- `docs/adr/` — numbered decision records; the six v1.0 rulings now live here
  (siblings cap at 5; KG per-family directory; `user_input_echo_audit` kept;
  filename kept; `lab_routing_directive` in `execution_meta`).
- `docs/Vocabulary/SEMANTIC_CONTRACT.md` — cross-lab JSON boundary protocol
  (binding for §3 schemas).
- `docs/Vocabulary/OBD_VOCABULARY.md`, `docs/Vocabulary/DTC_VOCABULARY.md` —
  enum/identifier authority.
- `wiki/` — domain truth (esp. `04_horizon_eras` scope; `07_pipeline_stages`;
  `08_scoring_to_fusion_rework`; `11_two_point_delta`).
- `CROSS_LAB_DEPENDENCIES.md` — DEP-1…DEP-10 emitter→fusion registry.
- The shipped `comlab/` package — this LLD reconciles up to it (authority note, top).
