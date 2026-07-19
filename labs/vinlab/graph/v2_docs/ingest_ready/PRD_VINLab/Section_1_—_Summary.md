> **Context:** VINLab PRD v2.1 (2026-06-12) | Module: VINLab | Section: Section 1 — Summary | Parent document: PRD_VINLab.md / SEMANTIC_CONTRACT section 4.1

## Section 1 — Summary

VINLab is the **vehicle-identity channel** of the 4D petrol diagnostic pipeline. It
accepts a 17-character VIN and decodes it — fully offline, with zero network and zero
MySQL at runtime — into a typed `VinDNA` dataclass: the **physical DNA** of the
vehicle (make, displacement, cylinder count, banks, induction, fuel delivery, air
metering, emissions equipment, era, plus per-engine-code CoC emission targets). The
single public entry point is `vinlab.decode(vin) → VinDNA`.

VINLab is one of the three sibling labs of the **DNA family** (`vinlab` + `symptomlab`
→ `dnalab`). Its `VinDNA` is Part A; SymptomLab supplies Part B; DNALab composes both
into `VehicleDNA`. `VinDNA`'s shape is governed by `SEMANTIC_CONTRACT.md §4.1` — that
contract wins over all other documents.

VINLab is a **producer, not a judge.** It emits a decoded profile; it does not rank
faults or render verdicts. Its consumers live downstream in **COMLab** (which projects
`VinDNA` into per-lab DNA views) and through them in **OBDLab** and **GASLab**. The
symptom/identity channel is the cheapest independent prior, and the identity half of
that prior is what VINLab produces.

---

## Graph relations (explicit)

**Section 1 — Summary** DESCRIBES **VINLab PRD v2.1 (2026-06-12)**
**vinlab.__init__.decode** CONSUMES **vinlab.decoder.RobustVINDecoder.decode_vin_payload**
**vinlab.models.VinDNA** OWNED_BY **VINLab**
