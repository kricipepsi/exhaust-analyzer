> **Context:** DNALab LLD_DNALab v2.1 (2026-06-12) · Module: DNALab · Section: 6. · Parent document: LLD_DNALab.md · Boundary contract: SEMANTIC_CONTRACT.md §4.3

## 6. Enum-Coercion Path (delegated)

DNALab performs no enum coercion of its own. `VinDNA.from_json` /`SymptomDNA.from_json`
coerce their respective enums; `VehicleDNA.from_json_payload` only routes the nested
dicts to them. This keeps the umbrella free of vocabulary knowledge.

---

## Graph relations (explicit)

**VehicleDNA.from_json_payload()** DELEGATES_TO **VinDNA.from_json()** (enum coercion)
**VehicleDNA.from_json_payload()** DELEGATES_TO **SymptomDNA.from_json()** (enum coercion)
**DNALab** DESCRIBES **zero enum coercion of its own** (delegates all vocabulary knowledge)
