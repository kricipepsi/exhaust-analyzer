> **Context:** VINLab ADR v2.0 (2026-06-12) | Module: VINLab | Section: ADR-0006: Data-driven checksum bypass for non-NHTSA markets | Parent document: ADR_VINLab.md

## ADR-0006: Data-driven checksum bypass for non-NHTSA markets

**Status:** Accepted (VINlookup.md §1; exercised by T-FX-5)

### Context

The NHTSA modulo-11 check digit (49 CFR Part 565) is mandatory only for the
US/CA/MX market (ISO 3780). European, Japanese, Korean, and Indian VINs legitimately
omit or dummy the position-9 character, and a batch of Mexican Mazda VINs in the
Slovenian DMV data have corrupt check digits. A strict checksum would reject valid,
in-scope vehicles.

### Decision

`validate_vin_checksum` applies three bypass paths before computing the checksum:
(1) non-NHTSA WMI by `wmi.csv` country, (2) the OPSI corrupt-prefix set
`{3MZ, 3MD, 3MV}`, (3) a non-standard position-9 character (`vin[8] ∉ "123456789X"`).
The bypass is **data-driven** (driven by `wmi.csv`), not hard-coded per VIN.

### Consequences

- **Positive:** valid European/Asian VINs decode; the checksum still guards North
  American VINs.
- **Negative:** a genuinely corrupt non-NHTSA VIN passes structural validation and is
  caught later (or graded down) rather than at the checksum.

### Alternatives Considered

1. **Always enforce the checksum.** Rejected: rejects valid in-scope vehicles.
2. **Always skip the checksum.** Rejected: discards a real integrity signal for North
   American VINs.

---

## Graph relations (explicit)

**ADR-0006: Data-driven checksum bypass for non-NHTSA markets** DESCRIBES **VINLab ADR v2.0 (2026-06-12)**
**vinlab.decoder.RobustVINDecoder.validate_vin_checksum** IMPLEMENTS **ADR-0006**
**labs/vinlab/tests/unit/test_decoder.py** VERIFIES **vinlab.decoder.RobustVINDecoder.validate_vin_checksum**
