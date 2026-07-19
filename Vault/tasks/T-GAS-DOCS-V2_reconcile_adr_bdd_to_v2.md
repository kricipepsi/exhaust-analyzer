---
node_type: task
task_id: T-GAS-DOCS-V2
status: pending
pack: VAULT
lab: gaslab
mode: architect/author lane
blocked_by: []
consumers:
- build_lab_vault.py — vault frontmatter derivation
- consumers.base — signal/noise audit view
- drift-guards.base — coverage view
- modules.base — module map view
- graph/v2_docs — docs graph
- design→code→test spine (.base views)
tags:
- task
- vault
- gaslab
---


# T-GAS-DOCS-V2 — Reconcile the GASLab design docs to v2 (AST ground-truth)

**Status:** `pending` · **Pack:** VAULT (GASLab) · **Mode:** architect/author lane (no inner-loop/gate)
**Origin:** pipeline guide §3·1D (the OBDLab "PRD refresh" model, `T-VAULT-PRD-V2-1`) · **Blocked by:** —
**Consumer (signal/noise):** **Adds no schema field.** The six design docs become the `docs/` corpus
that T-GAS-DOCPREP chunks and T-GAS-GRAPH-LLM graphifies into `graph/v2_docs/`. That docs graph's
consumer is the **vault build's frontmatter derivation** (`build_lab_vault.py` reads the graph to set
`node_type`/`implements`/`source`) plus the **design→code→test spine** rendered by `modules.base` /
`consumers.base` / `drift-guards.base` (plan §4). A doc field that describes a pruned/renamed value
seeds a stale graph node with no live code reader — so reconcile-to-AST *is* signal/noise at the doc
tier. No new fields are invented here; stale ones are corrected or dropped.

### Role note (author lane) ###

Design-doc authoring — no `gaslab/` code edit, no inner loop, no graphify. Reading the code/AST is
expected (to pin a bound or confirm an enum), but only to make the doc match shipped reality.

### Current doc state (verified 2026-06-10) ###

| Doc | Header state | Disposition |
|---|---|---|
| `HLD_GASLab.md` | Approved · PRD Baseline v2.1 | **confirm** AST parity (module decomposition vs shipped pkg) |
| `DLD_GASLab.md` | Approved · PRD Baseline v2.1 | **confirm** every field/bound/enum vs `dna_view.py` / `contracts.py` |
| `LLD_GASLab.md` | Approved · PRD Baseline v2.1 | **confirm** rule logic vs `rule_engine.py` / `resolution.py` |
| `PRD_GASLab.md` | Approved · v2.1 | **confirm** requirements current; it is the baseline the other three cite |
| `ADR_GASLab.md` | Living index · **v1.0** | **reconcile to v2** — add/accept the records for the 32→34 timing taxonomy (`WRONG_VALVE_TIMING` retired → 3× `CAM_TIMING_*`), dual-RPM routing, the in/out contract rebuild |
| `BDD_GASLab.md` | Approved · **v1.0** | **reconcile to v2** — scenarios must exercise the 34-value surface + dual-idle/dual-RPM behaviour (these seed `VERIFIES` edges) |

### North-star anchor (must be reflected) ###

`ChemicalSignature` is the **34-value** surface = v1's 32 − `WRONG_VALVE_TIMING` +
{`CAM_TIMING_RETARDED_MAP`, `CAM_TIMING_RETARDED_MAF`, `CAM_TIMING_ADVANCED`}
(`labs/gaslab/wiki/CHANGE_v2.1_timing_taxonomy.md`). Any doc still naming `WRONG_VALVE_TIMING` as a
live value (vs. a retired/superseded note) is stale and must be corrected.
**Known live-code smell to mirror, not hide:** `rule_engine.py:295` still carries the stale
`wrong_valve_timing_rule` name/grammar key (AUD-6) though it returns `CAM_TIMING_*`; the docs describe
the **behaviour** (CAM_TIMING), and the naming cleanup is tracked separately (AUD-6) — do not let the
doc re-introduce the retired value as current.

### Success criteria ###

1. **ADR + BDD bumped to v2** and reconciled: every record/scenario matches AST ground-truth; the
   32→34 taxonomy, dual-RPM input split, and in/out contract rebuild are represented; superseded v1
   records are marked superseded (ADR records are immutable once Accepted — add new ones, don't rewrite).
2. **HLD/DLD/LLD/PRD parity confirmed:** a field/bound/enum/exception walk against the shipped package;
   any drift corrected; numeric literals keep their wiki-citation comments; pruned values dropped.
3. **All six are current v2 peers** — no doc references a value the code no longer ships.
4. Out-of-scope design-doc neighbours flagged for the DOCPREP exclusion list (see that task): the
   generic skill stubs, the `GAS_VOCABULARY.md` duplicate, and `docs/audits/`.

### Out of scope ###

- Code edits (AUD-3/4/6 etc.) — separate GASLab diagnostic tasks.
- Chunking/anchoring/relations — that is T-GAS-DOCPREP (structural, not authoring).
- The vocabulary note's vault home — handled in the `_vocabulary/` tier at build time.

### Verification (author lane) ###

```bash
cd <repo>/labs/gaslab
grep -niE 'version|status' docs/ADR_GASLab.md docs/BDD_GASLab.md   # expect v2
grep -rn 'WRONG_VALVE_TIMING' docs/                                # only as 'retired/superseded', never 'current'
# spot-check a DLD field block against the code it specifies:
grep -n 'target_lambda_v112\|co_high_idle\|CAM_TIMING' docs/DLD_GASLab.md gaslab/dna_view.py gaslab/rule_engine.py | head
```

### Progress hook ###

`Vault/tasks/progress_notes/T-GAS-DOCS-V2.md` opens with the confirmed `## Plan` (which records/scenarios
get added, parity-walk checklist). The session fills `VERIFICATION GATE` (six docs current v2, no stale
value live, citations intact) + `CODE REVIEW` (here: a doc-review — drift items found/fixed, exclusions
flagged for DOCPREP). Ledger row flips to `done` only when both blocks are clean.
