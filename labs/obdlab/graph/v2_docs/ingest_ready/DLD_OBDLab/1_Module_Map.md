> **Context:** OBDLab DLD v2.0 (2026-06-10) · Module: OBDLab · Section 1 Module Map · Parent document: DLD_OBDLab.md

## 1. Module Map

```
obdlab/
├── __init__.py                       ← public surface: SensorSignalTranslator, OBDLivePayload, LinearityAccumulator
├── core/
│   ├── sensor_signal_translator.py   ← public entry point (orchestrator) + LinearityAccumulator
│   ├── pid_ingestion_validator.py
│   ├── state_bucketing.py
│   ├── semantic_consistency_checker.py
│   ├── ve_engine.py
│   ├── o2_normalizer.py
│   ├── trim_vector_aggregator.py
│   ├── maf_linearity.py              ← w_theo / sensor_error_delta helpers (T-OBDV2-10)
│   ├── analytics_preconditions.py
│   └── exceptions.py
├── schemas/
│   ├── dna_view.py
│   ├── payload.py
│   └── vocabulary.py
└── config/
    ├── physical_sensor_bounds.json
    └── obd_translation_rules.yaml
```

`core/__init__.py` and `schemas/__init__.py` each export an explicit `__all__`
(added in T-KG-OBD-2-PREP for code-map legibility). There is **no** `config/`
Python package — config is data only.

## Graph relations (explicit)

**obdlab/__init__.py** DESCRIBES **public surface** (SensorSignalTranslator, OBDLivePayload, LinearityAccumulator)
**core/** DESCRIBES **10 modules** (orchestrator + validators + engines + normalizers + aggregators)
**schemas/** DESCRIBES **3 schema modules** (dna_view, payload, vocabulary)
**config/** DESCRIBES **2 data files** (physical_sensor_bounds.json, obd_translation_rules.yaml)
**DLD_OBDLab v2.0** SUPERSEDES **DLD_OBDLab v1.0** (2026-05-22)
