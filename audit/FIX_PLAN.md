# FIX_PLAN — round 1 → fix rows (architect, 2026-10-17)

Every row below groups UPHELD findings from `FINDINGS.md` (column `owner`). A row becomes a task spec at
`labs/<lab>/tasks/<id>.md` (or `apps/<app>/…`) with its START_HERE paste-doc and a precise `Load skills:` line,
per the project conventions, before any coder touches code.

**Rulings that apply to every row**
1. **Domain truth is the lab wiki** (AGENTS.md rule 2): where code and wiki disagree, the code moves, unless the
   finding shows the wiki itself is wrong (e.g. F-D1-14, where the code is right). A wiki change is its own
   decision, recorded in the lab's `DECISIONS`/ADR, never a silent edit. Lost alternative: "code is the de-facto
   spec"; rejected because the wiki is the project's declared source of truth and the code diverged without records.
2. **`main` is production** (`AUDIT_START_HERE.md` §Deployment coupling): every row lands on a branch, passes its
   lab suites plus its own finding probes (`audit/scratch/<target>/`, which must turn green), then merges.
3. **A finding's probe is its acceptance test.** A row is done when the probes it owns pass and no other probe
   or suite regresses.

| row | priority | scope | findings (owner column) | why this order |
|---|---|---|---|---|
| **T-AUD-1** | P0 | public app usable: `registry` importable in the Render build; UI no longer crashes on blank/unticked inputs and missing triage; fields the engine needs are marked required or defaulted honestly | F-C1-5 (= F-C4-1), F-C4-9, F-C5-1, F-C5-2, F-C5-13, R1-L1 | the live app at 5-gasanalyzermot.com fails for a normal first use today (seen live 2026-10-17) |
| **T-AUD-2** | P1 | COMLab REG-V2 verdict correctness: healthy car ≠ fault, no sink rules, no-fault reported as no-fault, MIL/P030x override, era/precondition gating, O₂ bias label, KG enrichment on the production path | F-C1-1…4, 6…8, 10, 18…21; F-D2-1, 3, 4; F-D1-12 | wrong diagnoses reach users once T-AUD-1 lets runs complete |
| **T-AUD-9** | P1 | VINLab: year-cycle decode, WMI→brand table, engine row year window, petrol guard, era fallback, wideband rule, check-digit rule, scope cap 2010/Euro 5 | F-C6-1…14, F-D1-13 | era and sensor type feed every downstream lab (root of F-C5-3, F-C5-9) |
| **T-AUD-4** | P1 | cross-lab inputs: trim gate honoured (with F-C3-3 fixed first), O₂ override reaches labs, downstream O₂ mapped right, DNA to DTCLab, values range-checked, dropped UI fields wired or removed, inbound shape per SEMANTIC_CONTRACT | F-C1-17 (= F-C4-4), F-C4-2, 3, 5…8, 10; F-C3-1…3; F-C5-3…5, 9…11; F-D2-2, 9…11 | these decide what the engine actually sees |
| **T-AUD-3** | P2 | COMLab output: VIN confidence pass-through, confidence rating from verdict not era, degradation modes, invalid-sample and abort shapes, horizon validation | F-C1-9, 11…16; F-C5-6; F-D2-6, 7, 14 | user-facing labels that contradict the score |
| **T-AUD-5** | P2 | GASLab ontology and rules back to the wiki: triangle floor, collision rule, timing/valve-seal/cam boxes, override confidence gate, λ formula | F-C2-1…15; F-D2-22…24 | chemistry verdicts; several HIGH, but gated behind T-AUD-1/2 for user impact |
| **T-AUD-8** | P2 | OBDLab/DTCLab emitters and their wiki values: VE trigger, O₂ normaliser, IAT bound, trims, cold-engine O₂ placeholder, DTC ranking/family map | F-C3-4…19; F-D1-1…9, 14…17 | channel quality |
| **T-AUD-6** | P3 | tests and build: lab-isolated tests, opentelemetry dependency, BDD/test traceability gaps, missing release gates, broken symlinks, venv recipe (`apps/wiredV2`), launchers' hard-coded `/agent_workspace` | R0-2, R0-4, F-C1-22, F-D2-5, 16, 18, 25, 26, F-D3-10…12 | makes the next audit round cheaper and the suites honest |
| **T-AUD-10** | P3 | UI presentation: show horizon/routing panel/echo, distinct-family runner-ups, no direct VINLab import in the UI | F-C5-7, 8, 12 | presentation only |
| **T-AUD-7** | P3 | governance and design docs: git rule vs `main` = production (F-D3-1, do first: one line), ledger rows that are pending-but-done, rule contradictions, stale figures, superseded statements, missing citation files | R0-3, R0-5, F-D3-1…9, 13…20, F-D2-8, 12, 13, 15, 17, 19…21, 27, F-D1-10, 11, 18, 19 | F-D3-1 is a one-line edit that prevents a direct-to-production push; the rest is documentation debt |

Round 2 (`AUDIT_START_HERE.md`): after each row merges, re-run its target's probes and re-attack the target.
