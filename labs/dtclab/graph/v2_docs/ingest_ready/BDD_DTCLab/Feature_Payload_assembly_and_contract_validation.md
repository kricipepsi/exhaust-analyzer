
> **Context:** DTCLab BDD v1.0 (2026-06-11) · Module: DTCLab · Section: Feature: Payload assembly and contract validation · Parent document: BDD_DTCLab.md
## Feature: Payload assembly and contract validation
*Backing tests: `tests/unit/test_payload.py`.*

```gherkin
Scenario: A valid payload round-trips through JSON
  Given a fully populated DTCLabPayload
  When it is serialised and re-parsed
  Then the re-parsed payload equals the original

Scenario: A malformed DTC in the payload is rejected with a contract code
  Given a payload whose confirmed_dtcs contains "p0171"
  When the payload is validated
  Then validation fails with ERR-CONTRACT-001

Scenario: An invalid routing tag is rejected with a contract code
  Given a payload whose routing_tags contains "NOT_A_TAG"
  When the payload is validated
  Then validation fails with ERR-CONTRACT-002
```

---


## Graph relations (explicit)

**Feature: Payload assembly and contract validation** DESCRIBES **DTCLab BDD v1.0**
**test_payload.py** VERIFIES **Feature: Payload assembly and contract validation**
