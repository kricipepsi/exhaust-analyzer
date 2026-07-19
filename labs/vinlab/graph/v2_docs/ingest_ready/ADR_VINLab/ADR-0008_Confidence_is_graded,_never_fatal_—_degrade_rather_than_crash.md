> **Context:** VINLab ADR v2.0 (2026-06-12) | Module: VINLab | Section: ADR-0008: Confidence is graded, never fatal — degrade rather than crash | Parent document: ADR_VINLab.md

## ADR-0008: Confidence is graded, never fatal — degrade rather than crash

**Status:** Accepted (T-FX / contract §4.1)

### Context

Reference data is incomplete for parts of the 1990–2020 fleet. A decode that failed
whenever a row was missing would be unusable; but downstream labs must know how much to
trust the profile.

### Decision

Missing/partial data collects **confidence flags** rather than raising. The grade is
`NONE` (engine not in CSV), `PARTIAL` (any downgrade flag), or `HIGH` (clean). Only
genuine scope/structure violations (H1 non-petrol, H2 year, bad charset/checksum, WMI
miss) raise `VINDecodeError`.

### Consequences

- **Positive:** partial profiles still flow downstream, graded honestly.
- **Positive:** OBDLab's three-branch DNA-RPM gate keys off `confidence` directly.
- **Negative:** `PARTIAL` is coarse — a single missing CoC field and a missing engine
  code both read `PARTIAL`; the specific flags are not on `VinDNA`.

### Alternatives Considered

1. **Raise on any missing data.** Rejected: unusable on a real fleet.
2. **Silent best-effort with no grade.** Rejected: downstream cannot calibrate trust.

---

## Graph relations (explicit)

**ADR-0008: Confidence is graded, never fatal — degrade rather than crash** DESCRIBES **VINLab ADR v2.0 (2026-06-12)**
**vinlab.decoder.RobustVINDecoder.decode_vin_payload** IMPLEMENTS **ADR-0008**
**labs/vinlab/tests/unit/test_csv_suite.py** VERIFIES **vinlab.decoder.RobustVINDecoder.decode_vin_payload**
