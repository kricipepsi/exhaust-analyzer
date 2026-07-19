> **Context:** VINLab PRD v2.1 (2026-06-12) | Module: VINLab | Section: Section 2 — Contacts | Parent document: PRD_VINLab.md / SEMANTIC_CONTRACT section 4.1

## Section 2 — Contacts

### Name: VINLab Owner
- **Role**: Module Owner
- **Responsibility**: VIN structural validation, WMI/year/engine resolution, overlay rules, CoC overlay, confidence grading

### Name: COMLab Team
- **Role**: Integration Consumer
- **Responsibility**: Mirrors `VinDNA` locally; projects it into `ObdLabDnaView` / `DtcLabDnaView` / `lab_dna_views`; reads `rated_rpm`, `air_metering_strategy`, `stress_idle_rpm_target`, `confidence`, CoC targets

### Name: OBDLab Owner
- **Role**: Indirect Consumer
- **Responsibility**: Reads the projected DNA view: `rated_rpm` (RPM ceiling), `air_metering_strategy` (VE routing), `upstream_o2_type`, `induction_type`, `confidence`

### Name: GASLab Owner
- **Role**: Indirect Consumer
- **Responsibility**: Reads CoC emission targets (lambda/CO/HC thresholds) via the projector

### Name: 4DApp Engineering Lead
- **Role**: Architecture
- **Responsibility**: Signal/noise rule; cross-lab JSON contract; offline-runtime constraint; SQL-isolation (H8)

---

## Graph relations (explicit)

**Section 2 — Contacts** DESCRIBES **VINLab PRD v2.1 (2026-06-12)**
**comlab.projection.project** CONSUMES **vinlab.models.VinDNA.rated_rpm**
**comlab.schemas.lab_dna_views.ObdLabDnaView** CONSUMES **vinlab.models.VinDNA.rated_rpm**
