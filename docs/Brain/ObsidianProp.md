## Agent Onboarding Guide: Graph-Aware Monorepository Architecture## 📂 1. Physical Directory Architecture
This workspace structure integrates your four source analytics engines (obdlab, dtclab, comlab, gaslab) and the structural orchestrator module into a single shared file context (DLD_OBDLab... pp. 1-2, COMLab_DLD... p. 12). The AI agent mounts the Vault Root directly, establishing a common operational envelope across code segments, test matrices, and structural wikis (COMLab_DLD... pp. 1, 10).

Vault-Root/
├── .claude/                       # Global agent runtime parameters
│   └── commands/                  # Custom terminal-aware automation scripts
├── scripts/
│   └── build_validate.py          # Fast-failing multi-module validation engine
├── Application/                   # Active codebase domain
│   ├── orchestrator/              # The Coordinator Module
│   │   ├── core/                  # Pipeline execution managers
│   │   └── schemas/               # Inbound/Outbound contract payloads
│   ├── obdlab/                    # Module 1: Diagnostic telemetry ingest
│   │   ├── core/                  # ve_engine, sensor_signal_translator
│   │   └── config/                # physical_sensor_bounds.json
│   ├── dtclab/                    # Module 2: Trouble code diagnostics
│   ├── comlab/                    # Module 3: Central data fusion core
│   │   ├── core/                  # fault_atlas_router
│   │   └── config/                # global_fault_registry.json, kg/*.json
│   └── gaslab/                    # Module 4: Exhaust gas analytics
├── Knowledge-Graph/               # Documented relationships layer
│   ├── System-Map.md              # Global entry points index
│   ├── OBDLab_KG_Wiki.md          # Telemetry conversion specs
│   └── COMLab_KG_Wiki.md          # Fault routing rulebooks
└── CLAUDE.md                      # Persistent monorepo memory manifest

------------------------------
## 🏷️ 2. Metadata & Monorepo Linking Rules
Because your workspace uses terminal grep commands for file discovery, you must enforce rigid frontmatter schemas to avoid missing cross-module trace connections (obsid.pdf p. 26). Every documentation file must state its exact relationships at the absolute top of the page.
## Document Node Schema Rule

---node_type: wikimodule: comlabsubsystem: data-fusionimplements: "Application/comlab/core/fault_atlas_router.py"consumers: ["Application/orchestrator/core/pipeline_manager.py"]drift_guards: ["Application/comlab/tests/test_fault_atlas_router.py"]tags: [orchestrated-node, fault-atlas, zero-state]
---

## Downstream Structural Reference Example
When modeling properties across domain boundaries—such as the ObdLabDnaView data model being transformed by COMLab into a SanitizedPayload entry—utilize exact file tracking paths (DLD_OBDLab... p. 2, COMLab_DLD... pp. 2, 4):

# Module Node: Core Inbound Ingestion Pipeline- **Orchestrator Contract:** `Application/orchestrator/schemas/inbound.json`
- **Ingestion Target:** `Application/obdlab/core/pid_ingestion_validator.py`
- **Downstream Fusion Receiver:** `Application/comlab/core/fault_atlas_router.py`
## Implementation Rules- Data structures coming from `obdlab` must parse using `pydantic v2` bounds.- Missing telemetry properties trigger immediate fail-fast error events.

------------------------------
## 🛠️ 3. Project-Aware Command Skills
These configuration templates allow the agent to track system dependencies using local terminal scripts without encountering cross-module memory limits (obsid.pdf pp. 17, 26). Place these markdown files in ~/.claude/commands/ (obsid.pdf pp. 17, 20).
## /graph-find — Deep Cross-Module Map
This skill helps the agent find matching wiki items, implementation scripts, and dependency trees for a specific module query.
Create ~/.claude/commands/graph-find.md:

# Graph Relationship Explorer
Trace systemic node parameters across module code, unit tests, and wikis using path grep utilities.
## Execution Sequence1. Locate module documentation entries:
   ```bash
   grep -rnwl "module: {{args.[0]}}" Knowledge-Graph/
   ```
2. Extract targeted execution fields (`implements`, `consumers`) from the frontmatter headers.3. Check code tracking properties for cross-module runtime imports:
   ```bash
   grep -rn --include="*.py" "import {{args.[0]}}" Application/
   ```4. Output a summary mapping file paths, interface consumers, and current validation coverage.

## /check-impact — System Integration Guard
This command maps exact dependencies before code changes occur, preventing errors when fields or enums are modified (DLD_OBDLab... p. 1, COMLab_DLD... p. 11).
Create ~/.claude/commands/check-impact.md:

# System Integration Impact Analyzer
Evaluate regression risks across schema boundaries before creating or modifying code components.
## Execution Sequence1. Search the `Knowledge-Graph/` directory for the code path to find its documentation node.
2. Read the `consumers` array from the frontmatter to locate dependent modules.
3. Check for structural dependencies across modules (e.g., changes to `obdlab` schemas affecting `comlab`):
   ```bash
   grep -rn "ObdLabDnaView" Application/comlab/
   ```4. Provide an itemized risk evaluation covering serialization updates, CI script modifications, and wiki drift targets.

------------------------------
## 📝 4. The Monorepo Manifest Core (CLAUDE.md)
This permanent reference file acts as the agent's central onboarding document (obsid.pdf pp. 4, 14). It configures the agent's baseline understanding of project layouts and architecture limits (obsid.pdf pp. 4, 16).
Create Vault-Root/CLAUDE.md:

# Monorepo Memory Profile: 4DApp Diagnostic Analytics Engine## System Layout & Domains- **Orchestrator:** Coordinates data pipelines through stateless operations.- **OBDLab:** Telemetry ingest engine bounded by physical sensor check ranges.- **DTCLab:** Resolves and validates diagnostic trouble code sets.- **COMLab:** Central knowledge graph engine utilizing explicit rule definitions.- **GASLab:** Evaluates gas emission characteristics and engine conditions.
## Core Operational Constraints- **Zero Runtime State:** Modules must operate as pure functions.- **Memory Boundaries:** Combined configuration assets must not exceed 2.5 MB on disk.- **Performance Budget:** End-to-end processing must run under 250 ms at p95.
## Automation Development Steps1. Make code modifications inside target `Application/<module>` paths.2. Add comprehensive boundary tests to the matching component test suites.3. Run local build validations to ensure consistency across configuration arrays:
   ```bash
   python scripts/build_validate.py
   ```
4. Document updated workflows in the corresponding `Knowledge-Graph/` directories.

------------------------------
## 📋 5. Everyday Operational Checklist
To maintain workspace clarity, ensure the agent follows this sequence during feature development cycles (obsid.pdf pp. 15, 18):

  ┌────────────────────────────────────────────────────────┐
  │ 1. SESSION RE-ANCHORING                                │
  │ >> /resume                                             │
  │ Agent reads CLAUDE.md to load core system rules.       │
  └───────────────────────────┬────────────────────────────┘
                              │
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │ 2. SCHEMA TRACING                                      │
  │ >> /graph-find comlab                                  │
  │ Locates rule configuration registries and schemas.     │
  └───────────────────────────┬────────────────────────────┘
                              │
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │ 3. CHANGE SIMULATION                                   │
  │ >> /check-impact "add fuel_pressure to payload"        │
  │ Identifies consumer breaks across modules.             │
  └───────────────────────────┬────────────────────────────┘
                              │
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │ 4. LOCAL QUALITY GATE                                  │
  │ >> python scripts/build_validate.py                    │
  │ Verifies performance limits and cross-file schemas.    │
  └───────────────────────────┬────────────────────────────┘
                              │
                              ▼
  ┌────────────────────────────────────────────────────────┐
  │ 5. CONTEXT ARCHIVING                                   │
  │ >> /compress                                           │
  │ Logs change steps and saves context before exit.       │
  └────────────────────────────────────────────────────────┘


   1. Session Alignment (/resume): Restores permanent project parameter rules and active priorities from CLAUDE.md (obsid.pdf pp. 14, 18).
   2. Schema Tracing (/graph-find): Uses path grep sweeps to trace current component connections across code files and wikis (obsid.pdf p. 26).
   3. Change Simulation (/check-impact): Reviews integration points to check for compilation breaks or validation issues in sibling modules (DLD_OBDLab... p. 1, COMLab_DLD... p. 11).
   4. Local Quality Gate: Runs local validation checks to test memory usage, verify syntax formatting, and run regression test cases (COMLab_DLD... p. 11).
   5. Context Archiving (/compress): Updates project memory documents, outlines resolution steps, and cleans the session state before closure (obsid.pdf pp. 15, 18).

------------------------------





