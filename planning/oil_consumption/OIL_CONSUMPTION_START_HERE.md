# Oil-Consumption Expansion — pack START_HERE — **REBUILT 2026-06-12**

**Authored 2026-06-12 (architect).** This START_HERE was rebuilt after a
verify-the-premise pass found the first version was authored against the wrong
consumer. Read **§0 first** — it is the constraint that governs every row.

**Source research (readability-gate passed 2026-06-12 — 0 image placeholders,
full read, gas thresholds present as text):**

- `planning/oilconsumption.md` — 5 mechanical causes, operator symptoms.
- `planning/OilburnCases.md` — engineering dossier: L1/L2 gas signatures,
  delta logic, real-world precedents for `P_NEW_09 … P_NEW_13`.

> **One rule still governs every row (signal/noise):** every field/enum/fault
> added must have a **named, existing-or-proposed consumer** and the code path
> that reads it. "Future use" is not a consumer.

---

## 0. Architecture truth — where verdicts actually come from (READ THIS)

The first pass assumed COMLab routes oil faults through the knowledge graph (KG).
**It does not, on the live path.** The facts, pinned:

- `FaultAtlasRouter.__init__` defaults `use_v2_registry=True`
  (`comlab/comlab/core/fault_atlas_router.py:249`).
- `route()` therefore delegates to `registry.integration_shim` (`:1017-1022`).
- The shim builds the verdict **purely from the winning registry rule**
  (`registry/integration_shim.py::_translate_to_output`):
  `fault_code = rule.rule_id`, `fault_family = rule.fault_family.value`,
  `fault_name = rule.description`. **It never calls the COMLab KG.**
- KG resolution (`fault_atlas_kg.resolve`) runs **only** in the v1 inline branch
  (`route()` `:1168+`), which is **off by default**.

Consequences that shape this pack:

1. **To make an oil case produce a distinct live verdict, the discrimination must
   live in a `registry/rules/*.json` rule** with a distinct `rule_id`. The KG node,
   the "Engine Mechanical (…)" display family, and `differential_siblings` are
   **not read on the live path**.
2. **The dossier model is delta-based** (low-idle L1 vs high-idle L2), but the
   COMLab inbound `GasLabPayload` (`comlab/comlab/schemas/ingestion.py:162`) carries
   a **single** gas snapshot (`gas_hc`, `gas_co`, `gas_co2`, `gas_o2`, `gas_nox`,
   `lambda_chem`). **There is no high-idle field.** PCV and turbo cannot be
   separated until that contract gains high-idle gas (task **T-OIL-R3a**).

The orphaned first-pass artefacts (`P_NEW_09…13` KG nodes, 3 display families,
`oil_consumption.*` tier_2 symptom-prior wiring) are demoted to the **proposals
registry** with a named *future* consumer by **T-OIL-R1** — kept, not deleted.

---

## 1. The five dossier cases, mapped onto the *live* (registry) architecture

| Case | Mechanical mode | GASLab `chemical_state` | Live registry rule | Status |
|---|---|---|---|---|
| **P_NEW_09** | Worn piston rings | `WORN_PISTON_RINGS` | `MW-001` *(exists)* | live; verified by **T-OIL-R2** |
| **P_NEW_10** | Degraded valve-stem seals | `WORN_VALVE_SEALS` | `MW-002` *(exists)* | live; verified by **T-OIL-R2** |
| **P_NEW_12** | Head-gasket oil/coolant breach | `COOLANT_LEAK_INTERNAL` | `MW-003` *(exists)* | live; verified by **T-OIL-R2** |
| **P_NEW_11** | Faulty PCV (stuck open) | `POA_SIGNATURE` (live map) | `MW-008` *(NEW)* | **T-OIL-R4** (needs high-idle: R3a→R3b) |
| **P_NEW_13** | Worn turbo turbine seals | `POA_SIGNATURE` (live map) | `MW-009` *(NEW)* | **T-OIL-R5** (needs high-idle: R3a→R3b) |

The three single-snapshot cases already produce distinct live verdicts via existing
`mechanical_wear` rules. The genuinely new + hard work is PCV and turbo, both of
which gate on the **low→high-idle delta** and so depend on the high-idle contract.

### The turbo case is special (flag for R5)

P_NEW_13 burns **clean in-cylinder**: λ stays stoichiometric (0.99–1.01) because the
oil cracks **post-cylinder in the hot exhaust**, yet tailpipe HC is extreme
(720 ppm at low idle, dropping to 130 at high idle as exhaust flow dilutes it). A
λ/CO band match will **miss** it. The rule keys on `low.HC>500 && low.CO<0.15 &&
low.λ∈[0.99,1.01] && high.HC<200`. `forced_induction` (VIN DNA) is corroborating,
not required — the gas signature alone is the trigger.

### The PCV-vs-rings overlap (flag for R4)

A stuck-open PCV replicates ring-failure HC at a single point; it diverges on the
**low→high-idle delta** and on the **rich λ at idle** (`low.λ<0.94`). Routing must
use the delta, not the L1 snapshot alone, or PCV and rings collide. This is the
dossier's "inspect PCV before authorizing teardown" rule, in code.

---

## 2. How to run this pack

One task per coder session. The ledger is `PROGRESS.md`; the per-task specs are in
`tasks/T-OIL-R*.md`, each authored to `_skills/coding-bootstrap/templates/task_file.md`.
Pick the first `pending` row in `PROGRESS.md` whose Blocked-by are all `done`
(currently any of **T-OIL-R1, T-OIL-R2, T-OIL-R3a**), open its task file, and follow
the house inner loop. Do **not** start a second task in the same session.

## 3. Relationship to the first pass and to T-DNA-9

The drifted first-pass rows (`T-OIL-1…5`, `T-OIL-VAULT`) are archived in
`PROGRESS.md §5`. The deferred `T-DNA-9` (`labs/dnalab/tasks/PROGRESS.md`) is still
superseded by the `oil_consumption` symptom add — now demoted to a proposal until
the KG-enrichment future consumer (U-OIL-KG-1) is built.
