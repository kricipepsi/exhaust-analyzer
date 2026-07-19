# Oil-Consumption Expansion — task ledger (PROGRESS) — **REBUILT 2026-06-12**

Authored 2026-06-12 (architect). **This ledger supersedes the drifted first-pass
ledger** (old rows `T-OIL-1…5`, archived at the bottom). The rebuild was triggered
by a verify-the-premise pass that found the first pass was authored against the
wrong consumer (the COMLab KG) while the live engine decides faults from the
**registry rules via the shim**. See `OIL_CONSUMPTION_START_HERE.md` §0 for the
architecture truth, and each `tasks/T-OIL-R*.md` for the pinned spec.

Pick the first `pending` row whose Blocked-by are all `done`. **One task per coder
session.** Status legend: `pending` = scoped + authored, ready for a coder ·
`blocked` = waiting on a Blocked-by row · `done`.

---

## 0. Why this was rebuilt (the drift, in one paragraph)

The live verdict is produced by `registry/integration_shim.py::_translate_to_output`
(`fault_code = rule.rule_id`, `fault_family = rule.fault_family.value`,
`fault_name = rule.description`) because `FaultAtlasRouter.__init__` defaults
`use_v2_registry=True` and `route()` delegates to the shim
(`comlab/comlab/core/fault_atlas_router.py:249`, `:1017`). The live path **never
resolves the COMLab KG** — KG enrichment runs only in the v1 inline branch, which
is off by default. So the first-pass artefacts (the `P_NEW_09…13` KG nodes, the 3
"Engine Mechanical (…)" families, and the `oil_consumption.*` tier_2 symptom-prior
wiring) have **no live reader** — they are orphans under the signal/noise rule.
Separately, the dossier's discrimination model is **delta-based** (low-idle L1 vs
high-idle L2), but the COMLab inbound `GasLabPayload`
(`comlab/comlab/schemas/ingestion.py:162`) carries a **single** gas snapshot only —
there is no high-idle field — so PCV and turbo cannot be discriminated until the
GASLab→COMLab contract gains high-idle gas.

---

## 1. Corrected task graph

| ID | Title | Lab / area | Status | Blocked-by | Signal/noise consumer (named) |
|---|---|---|---|---|---|
| **T-OIL-R1** | Demote orphaned KG nodes (`P_NEW_09…13`), 3 "Engine Mechanical (…)" families, and `oil_consumption.*` tier_2 symptom wiring to the **proposals registry** with named *future* consumers; add an anti-orphan test asserting none are read by the live shim path | comlab config | **done** | — | Proposals registry only (`comlab/config/proposals/`). Future consumer = T-OIL-R4/R5 rules + a future KG-enrichment task; documented, not live. Code path asserted absent: `integration_shim.route_case` does not load `config/kg/`. |
| **T-OIL-R2** | Verify + lock the three single-snapshot oil verdicts already live: rings→`MW-001`, valve-seals→`MW-002`, head-gasket→`MW-003`; add registry tests; tweak rules only if a test fails | registry | **done** | — | `integration_shim.route_case_with_diagnostics` → `route()` verdict (`fault_code=MW-00x`). Live consumer already exists; this row proves + pins it. |
| **T-OIL-R3a** | GASLab→COMLab **high-idle (L2) gas contract**: GASLab emits high-idle `hc/co/co2/o2/nox/λ`; COMLab `GasLabPayload` mirrors them as optional fields (typed JSON boundary, no cross-lab import) | gaslab + comlab schema | **done** | — | T-OIL-R3b shim resolver + T-OIL-R4/R5 rules (same-pack readers). Ship fields + readers together = **proposal**. Code path: `GasLabPayload` fields read by `integration_shim` PID resolver (R3b). |
| **T-OIL-R3b** | Shim **high-idle PID resolver** (`high_idle_hc`, `high_idle_co`, `high_idle_lambda`) + rule-schema support for high-idle evidence rows | registry shim | **done** | — | T-OIL-R4/R5 rules consume the resolved high-idle PIDs. Code path: `integration_shim._PID_SOURCES` + `_build_observation` → `_check_obd_evidence`. |
| **T-OIL-R4** | **PCV** registry rule (`MW-008`): `POA_SIGNATURE` + `low_idle.HC>500` && `high_idle.HC<250` && `low_idle.λ<0.94` (rich-at-idle discriminator vs rings/turbo) | registry | **done** | — | `route()` verdict (`fault_code=MW-008`). Live consumer ships in this diff. |
| **T-OIL-R5** | **Turbo** registry rule (`MW-009`): `low_idle.HC>500` && `low_idle.CO<0.15` && `low_idle.λ∈[0.99,1.01]` && `high_idle.HC<200` (stoich-λ perception trigger); `forced_induction` as corroborating guard only | registry | **done** | — | `route()` verdict (`fault_code=MW-009`). Live consumer ships in this diff. |
| **T-OIL-R6** | Docs/wiki/dossier refresh: SEMANTIC_CONTRACT, vocabularies, `casesextra_new_cases.html` cards reconciled to the shipped registry + proposals | docs | **done** | R1, R2, R4, R5 | N/A — documentation reconcile; gate = docs match shipped registry/proposals. |
| **T-OIL-R7** | Refresh the GASLab vault tier to absorb the oil pack (proposal-only `06a`/GAS vocabulary map deltas, rebuild, `health` gate) | gaslab (vault) | **done** | R6 | Vault `.base` views + `vault_query.py health` read the injected `06a` frontmatter. (Carry-over of old `T-OIL-VAULT`.) |

**All rows done.** (R7 was the last unblocked row; R6 was its only blocker.)

T-OIL-R1 completion hook: Files changed=3. Verification="anti-orphan test green;
oil KG/families/symptom rows registered as proposals with future_consumer".
T-OIL-R2 completion hook: Files changed=2. Verification="rings/valve-seals/head-gasket route to MW-001/002/003 on live shim path; registry suite green".
T-OIL-R3a completion hook: Files changed=5. Verification="GasLabPayload mirrors optional high-idle gas; GASLab emits L2 block; both suites green; fields backward-compatible".
T-OIL-R3b completion hook: Files changed=2. Verification="shim resolves high_idle_* PIDs None-safely; high-idle-gated fixture rule fires/prunes correctly; registry suite green".
T-OIL-R4 completion hook: Files changed=4. Verification="MW-008 fires for PCV (rich λ + HC drop), does not steal rings MW-001, prunes without high-idle; registry suite green".
T-OIL-R5 completion hook: Files changed=4. Verification="MW-009 fires for turbo (stoich λ + low CO + HC drop), does not steal PCV MW-008, prunes without high-idle; registry suite green".
T-OIL-R6 completion hook: Files changed=5 (comlab SEMANTIC_CONTRACT, semantic/vocabul SEMANTIC_CONTRACT, symptomlab SYMPTOM_VOCABULARY, gaslab GAS_VOCABULARY, casesextra_new_cases.html — mirrored to docs/GASLab/lib/ copy). Verification="docs reconciled to shipped MW-001/002/003/008/009 + proposals; all five P_NEW_* cards cross-reference their live MW-00x and card gates match the shipped rule JSON; no live-KG-verdict claims remain (exact grep `KG .*decid|knowledge graph.*verdict` clean); gaslab oil-submode table column-count fixed (head-gasket row had lost its MW-003 cell)".
Focused checks passed; the broad `python -m pytest -q labs/comlab
registry/tests` run still has unrelated pre-existing registry corpus/charging
failures (missing Jaeger blueprint, CSV drift, DTCRoutingTag count).
T-OIL-R7 completion hook: Files changed=6 (Vault rebuild propagated 5 oil-pack
source files into `Vault/labs/gaslab/` — `wiki/06a_fault_atlas_oil_mechanical.md`,
`docs/GAS_VOCABULARY.md`, `code/contracts.py`, `code/process.py`,
`tests/unit/test_process.py` — plus `Vault/_meta/PROVENANCE.md` upsert; progress
note created). Verification="vault health green (exit 0; lone WARN is pre-existing
cross-ledger blocked_by refs, R7 touched 0 task files); oil 06a proposal deltas
present in rebuilt tier (PCV_STUCK_OPEN/TURBO_SEAL_OIL_LEAK/HEAD_GASKET_OIL_BREACH
×7, high_idle/MW-008/MW-009 ×5); diff oil-scoped after line-ending normalization;
06a frontmatter intact; oil signatures remain proposal-only (no live
ChemicalSignature change)".

---

## 2. Pinned dossier numerics (source: `planning/OilburnCases.md`, readability-gate passed 2026-06-12)

| Case | Low-idle (L1) | High-idle (L2) | Discriminator the rule must encode |
|---|---|---|---|
| P_NEW_09 rings (`MW-001`) | HC 120, λ stoich | HC 380 ↑ | HC **rises** with RPM; `low.HC>80 && high.HC>300` |
| P_NEW_10 valve-seals (`MW-002`) | HC 450 ↑ | HC 65 (cleanup) | elevated idle, rapid high-idle **cleanup**; `low.HC>300 && high.HC<100`, `low.λ<0.98` |
| P_NEW_11 PCV (`MW-008`, NEW) | HC 610, λ<0.94 **rich** | HC 170 | `low.λ<0.94` rich-at-idle; `low.HC>500 && high.HC<250` |
| P_NEW_12 head-gasket (`MW-003`) | HC 340, O₂ 2.0+, CO₂<11.5, NOx<30 | HC 440 | `low.O2>2.0`, `CO2<11.5 && NOx<30`, `high.HC>300` |
| P_NEW_13 turbo (`MW-009`, NEW) | HC 720, CO 0.07, λ 1.000 | HC 130 | `low.λ∈[0.99,1.01]` stoich; `low.HC>500 && low.CO<0.15`, `high.HC<200` |

All numeric literals authored into `registry/rules/` carry a wiki/dossier citation
comment (house rule). Cite `OilburnCases.md §<case>` + the GAS_VOCABULARY anchor.

---

## 3. Named cross-lab consumers (must exist or ship as proposals)

| Dep | Pairs with | What must happen |
|---|---|---|
| High-idle gas contract | R3a | GASLab emits L2 gas; COMLab `GasLabPayload` mirrors. No cross-lab import — typed JSON only. |
| PCV family | R4 | `MW-008` resolves to a registry `mechanical_wear` verdict. (The "PCV/Crankcase" *display* family is a proposal, R1.) |
| Turbo family | R5 | `MW-009` resolves to a registry `mechanical_wear` verdict. Stoich-λ + low-CO gas gate; `forced_induction` corroborating only. |

## 4. Unplanned follow-ups (off-scope discoveries — not in any diff)

| ID | Item | Origin |
|---|---|---|
| U-OIL-1 | Decide whether `oil_consumption.blue_oily_smell` (existing, under `visible_exhaust_smoke`) is retired now that `oil_consumption` is its own tier_1. | first-pass §1 |
| U-OIL-KG-1 | Future task: wire COMLab KG enrichment into the v2 `route()` path so the `P_NEW_*` nodes + display families become live consumers. This is the *named future consumer* that lets R1's proposals graduate. | rebuild §0 |
| U-OIL-FI-1 | Add a `forced_induction` (VIN-DNA) flag to the COMLab metadata mirror so R5 can use it as a hard guard rather than corroboration. | R5 scope |

---

## 5. Superseded — first-pass rows (history, do not action)

These were authored against the KG consumer and are retired by the rebuild. Their
on-disk artefacts are handled by **T-OIL-R1** (demoted to proposals), not deleted.

| Old ID | Old title | Disposition |
|---|---|---|
| T-OIL-1 (was done) | Add `oil_consumption` tier_1 + 3 tier_2 markers; validator cap 18→21 | Symptom vocabulary kept; its symptom-prior "consumer" was KG-path → demoted to proposal by R1. |
| T-OIL-2 (was done) | Pin proposal-only ChemicalSignature candidates `PCV_STUCK_OPEN`, `TURBO_SEAL_OIL_LEAK`, `HEAD_GASKET_OIL_BREACH` | Kept as proposals; unchanged. |
| T-OIL-3 (was done) | Add 5 KG nodes `P_NEW_09…13` + 3 families | KG nodes have no live reader → demoted to proposals by R1. |
| T-OIL-4 (was pending) | Oil routing rules (one task) | Split into R2/R3a/R3b/R4/R5 — the original single task was not buildable (no high-idle contract). |
| T-OIL-5 (was authoring) | Doc/wiki refresh | Re-issued as T-OIL-R6. |
| T-OIL-VAULT (was authoring) | Vault refresh | Re-issued as T-OIL-R7. |
