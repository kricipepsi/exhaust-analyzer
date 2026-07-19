
> **Context:** COMLab BDD v1.0 · Module: COMLab · Section: Feature: Contract validation at the ingestion gate · Parent document: COMLab LLD v2.0 / COMLab HLD v2.0
## Feature: Contract validation at the ingestion gate
*Tests: `unit/test_lab_pipeline_aggregator.py`, `unit/test_vocabulary_sae_iso_conformance.py`*

```gherkin
Scenario: A well-formed payload is accepted
  Given an inbound request that conforms to OrchestratorInboundRequest
  When the payload is validated
  Then validation passes and the pipeline proceeds to Stage A

Scenario: A malformed DTC string is rejected
  Given a request whose confirmed_dtcs contains "X1234"
  When the payload is validated
  Then validation fails with ERR-CONTRACT-001

Scenario: An air-metering strategy inconsistent with its sensors is rejected
  Given a request with air_metering_strategy DUAL_MAF_MAP_CROSSCHECK
    But has_map_sensor is false
  When the payload is validated
  Then validation fails with ERR-CONTRACT-002

Scenario: A downstream trim role without a downstream sensor is rejected
  Given a request whose downstream_trim_role is SECONDARY_FUEL_TRIM
    But downstream_o2_present is false
  When the payload is validated
  Then validation fails with ERR-CONTRACT-003
```

---


## Graph relations (explicit)

**Feature: Contract validation at the ingestion gate** DESCRIBES **COMLab BDD v1.0**
