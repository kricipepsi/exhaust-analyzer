> **Context:** DNALab LLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 2. · Parent document: LLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## 2. Session-ID Format (`models.py::VehicleDNA.new`)

```python
session_id = session_id or f"DNA_TX_{uuid.uuid4().hex[:10].upper()}"
```

`DNA_TX_` prefix + the first 10 hex characters of a UUID4, upper-cased. A caller-supplied
`session_id` is used verbatim. Tested by `test_assembly.py` (`startswith("DNA_TX_")`).

---

## Graph relations (explicit)

**session_id** OWNED_BY **VehicleDNA.new()** (models.py)
**session_id** DESCRIBES **DNA_TX_ prefix + uuid4().hex[:10].upper()**
**session_id** CONSUMED_BY **COMLab session correlation** (live)
**session_id** VERIFIES **startswith("DNA_TX_")** (test_assembly.py)
