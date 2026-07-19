> **Context:** OBDLab DLD v2.0 (2026-06-10) · Module: OBDLab · Section 7 core/state_bucketing.py · Parent document: DLD_OBDLab.md

## 7. `core/state_bucketing.py`

`compute_bucket(sanitized_pids, dna_view) → RpmStateBucket`. Rules loaded once
from `obd_translation_rules.yaml`. Priority rules (lower number = higher
priority) evaluated first, then document order, then fallback `STABILIZED_IDLE`.
Operators: `LESS_THAN`, `BETWEEN`, `APPROXIMATELY` (`tolerance_pct`, default 10).
`stress_idle_rpm_target` is resolved from `dna_view` for the `APPROXIMATELY`
`STRESS_IDLE` rule. Called **before** the semantic checker (F-O7).

## Graph relations (explicit)

**compute_bucket** CONSUMES **obd_translation_rules.yaml** (rules loaded once)
**compute_bucket** CONSUMES **ObdLabDnaView.stress_idle_rpm_target** (APPROXIMATELY STRESS_IDLE rule)
**compute_bucket** ENUMERATES **RpmStateBucket** (COLD_OPEN_LOOP_INVALID, STABILIZED_IDLE, REGULATORY_HIGH_IDLE, STRESS_IDLE)
**compute_bucket** ROUTES_TO **before SemanticConsistencyChecker** (F-O7 fix)
**test_state*.py** VERIFIES **compute_bucket** (unit tests)
