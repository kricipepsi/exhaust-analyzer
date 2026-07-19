> **Context:** DNALab LLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 3. · Parent document: LLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## 3. Timestamp Format (`models.py::VehicleDNA.new`)

```python
ts = (timestamp or datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")
```

ISO-8601 UTC, second precision, literal `Z` suffix. Tested against
`^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$`.

---

## Graph relations (explicit)

**timestamp** OWNED_BY **VehicleDNA.new()** (models.py)
**timestamp** DESCRIBES **ISO-8601 UTC %Y-%m-%dT%H:%M:%SZ**
**timestamp** CONSUMED_BY **COMLab temporal correlation** (live)
**timestamp** VERIFIES **ISO-8601 UTC timestamp format regex** (test_assembly.py)
