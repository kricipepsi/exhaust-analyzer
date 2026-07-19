> **Context:** OBDLab LLD v2.0 (2026-06-10) · Module: OBDLab · Section 9 Semantic Consistency Thresholds · Parent document: LLD_OBDLab.md

## 9. Semantic Consistency Thresholds (`core/semantic_consistency_checker.py`)

```python
_TRIM_MIN            = -127.0  # Physics_Gate_4 (widened, T-W-6)
_TRIM_MAX            =  127.0  # Physics_Gate_4 (widened, T-W-6)
_CUTOFF_ECT_COLD     =  75     # thermal gate cutoff (°C), §4.1
_CUTOFF_ECT_CLOSED   =  80     # Physics_Gate_2 closed-loop-expected (°C), §4
_CUTOFF_VSS          =  10     # Physics_Gate_1 VSS (km/h)
_CUTOFF_RPM_STALLED  =  400    # Physics_Gate_1 stalled-RPM (RPM)
```

Gate set is **1, 2, 4** (no Gate 3). `gates_passed` collects the three; the
orchestrator's `semantic_gates_passed = (len(gates_passed) == 3)`. A violated
gate **raises** (`SemanticConsistencyError`) and propagates out of `translate`,
so `TrimAnalyticsGate.SEMANTIC_ERROR` is a defensive path rather than a normal
return value.

## Graph relations (explicit)

**SemanticConsistencyChecker** ENUMERATES **_TRIM_MIN=-127.0, _TRIM_MAX=127.0** (Physics_Gate_4, widened T-W-6)
**SemanticConsistencyChecker** ENUMERATES **_CUTOFF_ECT_COLD=75, _CUTOFF_ECT_CLOSED=80** (thermal + closed-loop gates, # wiki: §4/§4.1)
**SemanticConsistencyChecker** ENUMERATES **_CUTOFF_VSS=10, _CUTOFF_RPM_STALLED=400** (Physics_Gate_1, # wiki: §4)
**SemanticConsistencyChecker** GATED_BY **gates_passed == 3** (Physics Gates 1, 2, 4 only; no Gate 3)
**TrimAnalyticsGate.SEMANTIC_ERROR** DESCRIBES **defensive path** (gate violation raises before reaching it)
**test_semantic_consistency_checker.py** VERIFIES **SemanticConsistencyChecker thresholds** (unit tests)
