---
node_type: task
task_id: T-VAULT-PRD-V2-1
status: done
pack: VAULT · **Mode:** ARCHITECT-AUTHORING lane
lab: obdlab
mode: architect-authoring lane
blocked_by: []
consumers:
- graph/v2_docs — docs graph
- design→code→test spine (.base views)
tags:
- task
- vault
- obdlab
---


# T-VAULT-PRD-V2-1 — Refresh PRD_OBDLab.md (v1.0 → v2)

**Status:** `done` · **Pack:** VAULT · **Mode:** ARCHITECT-AUTHORING lane (design-doc authoring — no lab inner-loop/gate)
**Origin:** owner request 2026-06-10 ("refresh PRD first") + HANDOFF TODO-5 · **Blocked by:** —
**Consumer (signal/noise):** **Adds no schema field.** The PRD is a *design document*, not a code schema; the
refresh reconciles its prose to the **shipped v2 code** so the doc carries no field/bound/enum that lacks a live
consumer. Its downstream consumer is the **doc-prep → graphify pipeline** (T-VAULT-DOCPREP-1 → T-VAULT-DOCGRAPH-1):
the refreshed PRD becomes one chunk-set in `graph/v2_docs/`, whose ultimate consumers are the vault build's
frontmatter derivation + the design→code→test spine in the three `.base` views (plan §4). A stale-v1 field that
no v2 code path reads is exactly the signal/noise breach this refresh removes — it does not get carried into the
graph.

### Role note (architect-authoring lane) ###

This is design-doc authoring, the same lane that produced `HLD/DLD/LLD/ADR/BDD_OBDLab.md` v2 (HANDOFF 2026-06-10).
It is **not** lab diagnostic code and runs **no** inner-loop / 6-phase gate. The "gate" here is an accurate,
internally consistent v2 PRD whose every field/bound/enum matches the shipped `obdlab/` source. No `obdlab/` code,
test, or `graph.json` is touched.

### Goal ###

Bring `labs/obdlab/docs/PRD_OBDLab.md` from **v1.0 (2026-05-22, "petrol-only, v1")** up to **v2**, grounded in the
live source exactly as the sibling v2 docs are, so it can enter the doc-prep ingest set as a clean v2 peer rather
than seeding v1 drift into the docs-tier graph.

### Reconciliation facts (AST ground-truth, from HANDOFF "Verified this session") ###

The refreshed PRD must agree with these — they are the shipped reality the v2 HLD/DLD/LLD already reflect:

- `OBDLivePayload` = **31 fields** (v1 PRD predates the reworked schema).
- `ObdLabDnaView` = **7 fields**.
- `vocabulary.py` = **8 StrEnums**; `O2FailureMode` = **4 values** (`NO_FAULT/STUCK_LEAN/STUCK_RICH/WIDEBAND_OFFSET_CANDIDATE`)
  — v1 SLUGGISH/DEAD/WRONG_CENTERLINE/HEATER_FAULT were pruned (ARCH-2); `WIDEBAND_OFFSET_CANDIDATE` added (T-OBDV2-4 / EP-OBD-17).
- `FuelSystemStatus` (`CL/OL/OL_DRIVE/OL_FAULT`) added (T-OBDV2-6, mirrored from DTC_VOCABULARY §8).
- bounds = **12**; trim bounds are the reworked values (v1 PRD's ±100 trim is stale — use shipped bounds with their wiki citations).
- **no live Physics Gate 3**; exceptions live under `ObdLabError`.
- Truth-vs-Perception framing unchanged: `OBDLivePayload` is the ECU **perception**; COMLab compares it to GASLab chemistry ground truth.

### Success criteria ###

1. `docs/PRD_OBDLab.md` header reads **Version: 2.0**, dated this session, scope updated to the v2 rework (drop the
   bare "v1" wording while keeping "petrol-only").
2. Every field/bound/enum/exception named in the PRD matches the AST ground-truth above; **no pruned v1 value**
   (SLUGGISH/DEAD/WRONG_CENTERLINE/HEATER_FAULT, ±100 trim, 8-PID schema) survives.
3. Numeric literals carry their **wiki-citation comments** (CLAUDE.md HARD RULE for `gaslab/`/`obdlab/` literals
   surfaced in docs).
4. Internal consistency: PRD cross-references resolve to the v2 `HLD/DLD/LLD_OBDLab.md` section numbers (spot-check,
   not exhaustive).
5. Passes the **document readability gate** (no `![][` image placeholders, full-read, formulas as text/LaTeX).
6. **No `obdlab/` code/test edit; no `graph.json` re-extraction.**

### Files to touch ###

- `labs/obdlab/docs/PRD_OBDLab.md`

### Out of scope ###

- Running doc-prep or graphify (that is T-VAULT-DOCPREP-1 / T-VAULT-DOCGRAPH-1).
- The other v2 docs (HLD/DLD/LLD/ADR/BDD) — already v2, do not touch.
- `drift_inventory_2026-05-25.md` refresh (HANDOFF TODO-5 low-priority remainder; flag to follow-ups if needed).
- Any vocabulary edit — the canonical vocab reconciliation is HANDOFF TODO-2 in the semantic pack, not here.

### Verification (authoring lane — content correctness, not tests) ###

```bash
cd <repo>/labs/obdlab/docs
# 1) version bumped
grep -m1 -i 'version' PRD_OBDLab.md            # expect 2.0
# 2) no pruned v1 enum value survives
grep -nE 'SLUGGISH|DEAD|WRONG_CENTERLINE|HEATER_FAULT' PRD_OBDLab.md && echo "FAIL stale enum" || echo "OK enums v2"
# 3) no stale ±100 trim bound
grep -nE '(\+|-|±)100\b' PRD_OBDLab.md && echo "REVIEW: confirm not a stale trim bound" || echo "OK no ±100"
# 4) readability gate
grep -n '!\[\]\[' PRD_OBDLab.md && echo "FAIL image placeholder" || echo "OK no placeholders"
```

### Progress hook ###

`Vault/tasks/progress_notes/T-VAULT-PRD-V2-1.md` opens with the confirmed `## Plan`; the authoring session fills
`VERIFICATION GATE` (content checks above) + `CODE REVIEW` (what changed vs v1). The plan §8 row flips to `done`
only when both blocks are clean and the four checks pass. Verification = "PRD refreshed to v2, all fields/enums/
bounds reconciled to AST ground-truth (31 payload fields, O2FailureMode=4, FuelSystemStatus added, 12 bounds),
citations intact, no stale v1 value; no code/graph touched".
