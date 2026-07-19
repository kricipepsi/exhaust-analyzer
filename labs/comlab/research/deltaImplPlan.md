 User approved Claude's plan
  ⎿  Plan saved to: ~\.claude\plans\unified-giggling-sprout.md · /plan to edit
     T-COMV2-DELTA-1 — Cross-lab delta module (delta_signature as a proposal-bounded primary rank input)

     Context

     The v2 diagnostic engine is ranking-bound at ~51%, and the audit's hardest culprits are single-snapshot
     problems: families that collide because they're read at one operating point (worn rings vs worn valve seals
     both read "elevated HC" at idle; TIMING_RETARDED → 7 families). They separate on the sign of the change
     across an RPM step. OBDLab's delta-relations/* research quantified those steps (ΔTrim profiles, a 2-speed
     Δgas matrix, ΔO₂ feeders) but its named consumer — "the COMLab delta-calculation script (FU-2)" — was never
     built, so every chunk sits at consumer: PENDING.

     This task builds that consumer as a COMLab-owned, stateless delta engine. When a case carries an optional
     second operating-point frame, the engine computes per-channel deltas and feeds a typed delta_signature
     into the ranker as a primary discriminator (the static single-point signature becomes the fallback). When
     no second frame is present, behaviour is byte-for-byte the current single-point path. The whole feature is
     proposal-bounded (COMLab-DELTA) and default-off behind a constructor flag, so it ships signal/noise-
     compliant (field + consumer in one change) without disturbing the live corpus. Live activation (two-point
     corpus + emitter emission) is a separate Gate-1 follow-up, explicitly out of scope here.

     Decisions locked in scope-confirm

     - Band policy → per-signal bands. ΔTrim validates against STRESS_IDLE (3500–4500, chunk 01); Δgas/ΔO₂
     against REGULATORY_HIGH_IDLE (~2500, chunk 07). The frame carries its own rpm_state_bucket; each
     per-signal check ABSTAINS on band mismatch rather than comparing against a baseline measured at a
     different RPM. Band boundaries stay enum-anchored (EngineStateBucket), each numeric # wiki:-cited.
     - Consumer path → v1 Phase 5 only, default-off. Production currently early-returns through the v2 registry
     shim (route() line 1017, default USE_V2_REGISTRY=1) before execute_triage_loop runs. The task's named
     consumer is execute_triage_loop Phase 5 — the v1 path, reachable with use_v2_registry=False. We wire
     there, default-off, and prove reachability with two greps (read site + the branch that calls it). The
     v2-shim re-rank activation is registered as a named follow-up T-COMV2-DELTA-2, not smuggled in here.
     - DEP registry → real file. v2-restructure/CROSS_LAB_DEPENDENCIES.md (task's pointer) does not exist; the
     live source-of-record is labs/comlab/docs/CROSS_LAB_DEPENDENCIES.md. Append DEP-14 in the DEP-2…DEP-13
     shape.
     - Fixtures → derive from delta-relations/01–08. The prompt-D ground-truth master table is an unanswered
     research prompt. Build synthetic two-point fixtures from the concrete chunk numbers, each # wiki:-cited;
     no chunk coverage → no fixture. Mark the file provisional; re-point at prompt-D when it lands.

     Key verified facts (shape the design)

     - AirMeteringStrategy (vocabulary.py:108) and InductionType (vocabulary.py:151) already exist — no
     mirror needed. But they ride on VinDNA, which is not reachable from the router's request
     (OrchestratorInboundRequest has no VinDNA). → architecture-gate inputs must be carried on the new
     second-frame model itself.
     - DegradationLit (response.py:26) is Literal["FULL_FUSION","GAS_DOMINANT","FATAL_INCOMPLETE"] and gates
     ExecutionMeta.degradation_mode. Adding SINGLE_POINT to the DegradationMode enum also requires
     widening this Literal, or ExecutionMeta validation rejects it.
     - entries.yaml is documentation/registry only (loaded in tests, does not gate behaviour). The behavioural
     default-off gate is a constructor boolean, mirroring the existing use_v2_registry pattern.
     - PowerLossAnalytics (analytics/power_loss_analytics.py:28) is the style to mirror: static-only, pure math,
     no state, pydantic I/O, constants as class attrs with # lld:/# wiki: citations.

     ---
     Implementation steps (smallest-diff order; each green before the next)

     1. comlab/schemas/vocabulary.py — SINGLE_POINT degradation mode

     Add a sibling to DegradationMode (after line 568):
     SINGLE_POINT = "SINGLE_POINT"  # wiki: delta-relations/01 — no second frame; static signature is the fallback
     AirMeteringStrategy/InductionType already present — no change.

     2. comlab/schemas/response.py — widen DegradationLit (must land with step 1)

     Add "SINGLE_POINT" to the Literal at line 26 so ExecutionMeta accepts the new mode.

     3. comlab/schemas/ingestion.py — optional second-frame input

     - Add SecondOperatingPointFrame(BaseModel) after OBDLiveDataPayload (line 367). All measurement channels
     optional (engine computes only deltas whose channels are present on both frames). Fields:
     rpm_state_bucket: EngineStateBucket, engine_rpm: int, trim channel
     (total_trim_correction_delta/shrtft1/longft1), gas channel
     (gas_hc/gas_co/gas_co2/gas_o2/gas_nox/lambda_chem), validity inputs
     (sample_validity: SampleValidity | None, rpm_stable: bool = True), ΔO₂ components
     (o2_switch_freq_hz/o2_voltage_bias_v/o2_downstream_response, named-only), and architecture-gate
     inputs carried here (air_metering_strategy: AirMeteringStrategy | None,
     induction_type: InductionType | None). Reuse the existing field-constraint bounds from GasLabPayload/
     OBDLiveDataPayload; each # wiki:-cite its chunk.
     - Add the optional request field on OrchestratorInboundRequest (after line 412):
     second_operating_point: Optional[SecondOperatingPointFrame] = None
     # T-COMV2-DELTA-1 — additive; absent → byte-identical single-point path.
     # consumer: comlab/analytics/delta_engine.py:DeltaEngine.compute_delta_signature -> fault_atlas_router Phase 5
     - Regression check after this step: run the full existing tests/ suite — default None + last-field
     position proves existing JSON fixtures validate unchanged.

     4. comlab/analytics/delta_engine.py — NEW module (mirror PowerLossAnalytics style)

     Stateless, static-only, pure math. Defines the typed DeltaSignature output model (+ sub-models
     DeltaTrimResult, DeltaGasResult, DeltaO2Result, DeltaValidityVerdict, ArchitectureGateVerdict) and
     the engine. Numeric constants as # wiki:-cited class attrs (ΔTrim leak ≤ −10 / supply ≥ +10 / backpressure
     ≤ −10; low-idle bands +15..+25 / 0..+5 / 0..+8; turbo invert ≈ −20; ΔHC rings ≥ +100, valve ≤ −50; ΔNOx EGR
     ≥ +800; vsum 14–18, dilution CO+CO₂ ≤ 6; primary-delta confidence ≈ 0.92).

     DeltaSignature carries the byte-identity contract: present: bool (False == no frame == single-point) and
     confidence: float (0.0 when absent/untrusted/nulled). Phase 5 fires only on present and confidence > 0.
     target_fault_family maps only to existing FaultFamilyLit members.

     Entry point — architecture gate FIRST, then validity, then per-signal band checks:
     compute_delta_signature(request) -> DeltaSignature
       frame None            → _single_point_sentinel()      # present=False, conf=0.0, SINGLE_POINT
       _architecture_gate    # chunk 06: MAP_ONLY_SPEED_DENSITY → trim_nulled; TURBO/SC → trim_inverted;
                             #            both None → permissive + confidence cap (never apply NA profile blind)
       _validity_gate        # chunk 08: per-frame vsum 14–18, dilution CO+CO₂>6, rpm_stable, sample_validity ok
                             #            untrusted → present=True, conf=0.0 (Phase-5 fallback)
       _delta_trim           # band must == STRESS_IDLE else ABSTAIN; apply invert/null; match profile by Δ+low band;
                             #            starvation↔MAF ambiguous → ABSTAIN
       _delta_gas            # band must == REGULATORY_HIGH_IDLE else ABSTAIN; rings/valve/flat-cam/EGR/rich profiles
       _delta_o2             # subtraction-only passthrough; never sets a profile (not yet quantified)
       _assemble             # ΔTrim profile precedence, Δgas corroborates; map to existing FaultFamilyLit;
                             #            conf = primary only when concrete profile resolved AND trusted AND not nulled

     5. comlab/core/fault_atlas_router.py — flag + compute + Phase 5 read (default-off)

     - Constructor (lines 244–264): add enable_delta: bool = False, store self._enable_delta, mirroring
     use_v2_registry.
     - In route() v1 branch, after request = sanitized["request"] (line 1155) and before execute_triage_loop
     (1158): if self._enable_delta and key absent, lazy-import DeltaEngine and set
     sanitized["delta_signature"] = DeltaEngine.compute_delta_signature(request).
     - In execute_triage_loop Phase 5, after the routing-tag discriminator (line 760) and before
     scored.sort (762), inside the phase.score span: read sanitized.get("delta_signature"); when
     present and confidence > 0 and target_fault_family, for each scored row whose KG fault_family matches,
     set score = max(score, delta_sig.confidence) (max, not + — "primary" means it dominates, promoting
     the delta-matched family above base-weighted rows; the unchanged sort then ranks it first). Emit a
     delta_signature_applied span event. Signature of execute_triage_loop is unchanged.
     - Byte-identity: three independent falsy short-circuits keep the single-point path bit-identical — key
     absent (flag off), present=False (no frame), confidence==0.0 (untrusted/nulled). Any one leaves scored
     untouched and runs the existing sort.

     6. comlab/core/lab_pipeline_aggregator.py — thread the flag (default-off)

     Add enable_delta: bool = False to __init__ (after line 95; optionally resolve from COMLAB_ENABLE_DELTA
     env mirroring USE_V2_REGISTRY, default off) and pass enable_delta=enable_delta into the
     FaultAtlasRouter(...) build (lines 112–117). No change to _map_degradation (line 173) — keeps
     ExecutionMeta byte-identical on single-point cases; surfacing SINGLE_POINT into the output is a
     live-activation follow-up.

     7. comlab/config/proposals/entries.yaml — COMLab-DELTA (docs/registry only)

     Append in the existing entry shape: id: "COMLab-DELTA", family: "cross-lab-delta-proposal",
     consumer: "comlab/comlab/core/fault_atlas_router.py:FaultAtlasRouter.execute_triage_loop",
     status: "proposed", owning_ledger: "COMLab T-COMV2-DELTA-1", source: (delta-relations/01–08 +
     research/PROPOSAL_DeltaLab_cross_lab_delta_module.md), description: (names the default-off constructor
     gate + the second_operating_point field + the v2 follow-up T-COMV2-DELTA-2), and a
     field.path: OrchestratorInboundRequest.second_operating_point.

     8. Tests

     - tests/unit/test_delta_engine.py (NEW) — fixtures derived from chunk numbers, each # wiki:-cited:
       - ΔTrim (STRESS_IDLE): vacuum_leak (low +20/elev +2 → vacuum_leak, ch02), fuel_starvation (low +3/elev +20
     → lean_condition, ch03), maf_underreport (low +6/elev +24, ch04), exhaust_backpressure (low 0/elev −14
     → exhaust_leak, ch05).
       - Δgas (REGULATORY_HIGH_IDLE): worn_piston_rings (HC 15→180 → mechanical_wear, ch07), worn_valve_seals
     (HC 120→15, ch07), flat_cam (HC 30→220 + O₂ 0.4→2.5, ch07), egr_stuck_closed (NOx 1500→2800, ch07).
       - Abstain: trim band-mismatch, starvation↔MAF ambiguous, gas no-signature.
       - Architecture (ch06, mandatory): speed_density nulls leak (MAP_ONLY → trim_nulled, conf 0);
     forced_induction inverts sign (TURBOCHARGED, elev STFT ≈ −20 → trim_inverted, not misread as NA leak).
       - Validity (ch08): vsum dilution reject (CO+CO₂ ≤ 6), vsum out-of-band reject (<14), rpm-unstable reject.
       - Sentinel: no second frame → present=False, SINGLE_POINT, conf 0.
     - tests/e2e/ (ADD) —
       - test_delta_single_point_regression: a no-second-frame request through FaultAtlasRouter(use_v2_registry= False)
     with enable_delta=True and enable_delta=False → identical OrchestratorFinalUIOutput
     (proves the flag is inert without a frame).
       - test_delta_two_point_activation: an input where the delta-target family is a static runner-up; trusted
     second frame + enable_delta=True promotes it to winner (assert winner flips + delta_signature_applied
     fired); enable_delta=False leaves the original winner.
     - Existing single-point tests/ suite is the regression lock — must stay green untouched.

     9. labs/comlab/docs/CROSS_LAB_DEPENDENCIES.md — append DEP-14

     Append in the DEP-2…DEP-13 column shape:
     | **DEP-14** | `delta_signature` cross-lab delta (per-signal bands: ΔTrim @STRESS_IDLE 3500–4500 ·
     Δgas/ΔO₂ @REG_HIGH_IDLE ~2500; ABSTAIN on band mismatch) | OBD ΔTrim baselines (fuel-trim chunk 01) +
     GAS Δgas-matrix/ΔO₂ baselines (chunk 07) — S1/S2 | COMLab delta module — **S4** · `T-COMV2-DELTA-1` →
     `execute_triage_loop` Phase 5 (default-off `enable_delta=False`; v2-shim activation follow-up
     `T-COMV2-DELTA-2`) | band bounds wiki-cited (chunks 01/07), not research-gated | emit baselines **done**;
     consumer **S4** live on v1 Phase 5 (`use_v2_registry=False`); v2-shim activation **deferred →
     `T-COMV2-DELTA-2`** |

     10. Ledger + progress note

     - labs/comlab/tasks/PROGRESS.md: flip the T-COMV2-DELTA-1 row → in_progress, then done at close.
     - Fill VERIFICATION GATE + CODE REVIEW in labs/comlab/tasks/progress_notes/T-COMV2-DELTA-1.md.

     ---
     Verification

     Inner loop (from labs/comlab):
     ruff check . && pyright comlab/ && pytest -x -q

     Consumer-read gate — two greps (read site + the branch that reaches it), proving live, not dead, code:
     grep -nI "delta_signature" comlab/core/fault_atlas_router.py     # read inside execute_triage_loop Phase 5
     grep -nI "use_v2_registry" comlab/core/fault_atlas_router.py     # the v1 branch that calls Phase 5

     Regression lock (single-point byte-identical):
     pytest tests/e2e -q -k "single_point or regression"
     pytest tests/unit/test_fault_atlas_router.py tests/unit/test_symptom_prior.py tests/unit/test_router_spans.py -q

     New delta suite:
     pytest tests/unit/test_delta_engine.py -q

     Done = both gate blocks filled in progress_notes/T-COMV2-DELTA-1.md; delta_signature two-grep-confirmed on
     the v1 live path; single-point regression byte-identical; ledger row → done; then STOP.

     Out of scope (Gate-1 / follow-ups)

     - Rebuilding the corpus to two-point or changing the single-point default.
     - Emitter changes (GASLab/OBDLab/DTCLab stay stateless/single-point; no cross-lab imports).
     - v2 registry-shim re-rank activation → named follow-up T-COMV2-DELTA-2.
     - graphify / KG rebuild; static-ranker weight re-tuning (OPEN_LEVERS F2).
     - Surfacing SINGLE_POINT into ExecutionMeta (live-activation follow-up).

     Note for the architect (not coder scope)

     The task spec names v2-restructure/CROSS_LAB_DEPENDENCIES.md; the live file is
     labs/comlab/docs/CROSS_LAB_DEPENDENCIES.md. Recommend correcting the stale pointer in the task file and in
     PROGRESS.md line 4 so the next coder doesn't hit the dead path.

  Thought for 6s (ctrl+o to expand)

● Plan approved. Per the boot drill, here's my one-paragraph scope-confirm:

  ▎ Field: delta_signature (a typed cross-lab two-point delta) computed by a new stateless COMLab analytics module from
  ▎ an optional second_operating_point frame on the request. Guard: default-off constructor flag enable_delta=False
  ▎ (mirrors use_v2_registry); absent frame / flag-off / untrusted ⇒ byte-identical single-point path. Signal/noise
  ▎ consumer: fault_atlas_router.execute_triage_loop Phase 5 — delta_signature becomes a primary rank term via score =
  ▎ max(score, confidence) on the KG-family match, the static float-score staying the fallback; proposal-bounded as
  ▎ COMLab-DELTA (consumer ships in this change). Per-signal bands: ΔTrim @ STRESS_IDLE, Δgas/ΔO₂ @
  ▎ REGULATORY_HIGH_IDLE, ABSTAIN on band mismatch. Files: schemas/{vocabulary,response,ingestion}.py, new
  ▎ analytics/delta_engine.py, core/{fault_atlas_router,lab_pipeline_aggregator}.py, config/proposals/entries.yaml,
  ▎ tests/unit/test_delta_engine.py + tests/e2e/, docs/CROSS_LAB_DEPENDENCIES.md (DEP-14), tasks/PROGRESS.md + progress
  ▎ note.