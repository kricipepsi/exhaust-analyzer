# T-SEM-5 — Reconcile OBD_VOCABULARY (§12.4, §5.2) to shipped code + re-sync all copies

**Status:** `pending (next)` · **Pack:** SEMANTIC · **Mode:** STRICT
**Origin:** `labs/obdlab/docs/HANDOFF_obdlab_docs_2026-06-10.md` TODO-1 + TODO-2 · **Blocked by:** —
**Consumer (signal/noise):** **N/A — adds no field, enum value, or fault.** This task makes the wiki
*document* enum members that are **already shipped and already consumed in live code**. Both reconciled
values carry a named, existing consumer (so signal/noise is already satisfied upstream):
- `O2FailureMode.WIDEBAND_OFFSET_CANDIDATE` → returned at `obdlab/obdlab/core/o2_normalizer.py:191`;
  consumer **COMLab `T-COMV2-O2OFFSET-1`** (re-animated and verified live by `T-OBDV2-FIX-2`, status `done`).
- `FuelSystemStatus` (CL/OL/OL_DRIVE/OL_FAULT) → consumed in COMLab `fault_atlas_router`,
  `power_loss_analytics`, `symptom_prior`, `tag_discriminator` (via `ingestion.fuel_system_status`) and DTCLab
  `freeze_frame_extractor`. Defined in `obdlab/obdlab/schemas/vocabulary.py:82` and mirrored in
  `comlab/comlab/schemas/vocabulary.py:413`.

Because no new content is introduced, **no proposals-registry routing is required** — this is doc catching up
to code, not a new-fault proposal. The downstream consumer of the corrected text is the **T-SEM-4 conformance
gate**, which parses the vocab/citations.

### Goal ###

The canonical `OBD_VOCABULARY.md` (and its two byte-identical sibling copies) is **stale** against the shipped
`obdlab` enums: §12.4 still lists the **pre-ARCH-2** seven-value `O2FailureMode`, and §5.2 omits
`FuelSystemStatus` entirely. Bring the wiki into exact agreement with `obdlab/obdlab/schemas/vocabulary.py`,
and re-establish the single-source invariant (all live copies byte-identical again). Also propagate last
session's `SEMANTIC_CONTRACT §4.4` fix (which landed only in the semantic copy) to the live COMLab wiki copy.

### Success criteria ###

1. **§12.4 `O2FailureMode`** in `OBD_VOCABULARY.md` lists **exactly the 4 shipped members**, matching
   `obdlab/obdlab/schemas/vocabulary.py:113-121` member-for-member and value-for-value:
   `NO_FAULT`, `STUCK_LEAN`, `STUCK_RICH`, `WIDEBAND_OFFSET_CANDIDATE`.
   The four pruned members (`SLUGGISH`, `DEAD`, `WRONG_CENTERLINE`, `HEATER_FAULT`) are **removed** (pruned by
   `T-OBDV2-ARCH-2`, status `done`). `WIDEBAND_OFFSET_CANDIDATE` carries its code wiki-citation
   (`o2-logic/03 §BIASED_OFFSET / o2-logic/08`).
2. **§5.2 OBDLab analytics enums** gains **`FuelSystemStatus`** with the 4 shipped members
   (`CL`, `OL`, `OL_DRIVE`, `OL_FAULT`), matching `obdlab/obdlab/schemas/vocabulary.py:82-91`, annotated
   "(mirrored in COMLab + sourced from DTC_VOCABULARY §8)".
3. **All three live `OBD_VOCABULARY.md` copies are byte-identical again** after the edit
   (`md5sum` equal across the three paths in *Files to touch*). Single source of truth restored.
4. **`SEMANTIC_CONTRACT.md §4.4`** `o2_failure_mode` comment in the **`comlab/docs/wiki`** copy is corrected
   from "7 values incl. NO_FAULT" to match the semantic copy's "4 values: NO_FAULT, STUCK_LEAN, STUCK_RICH,
   WIDEBAND_OFFSET_CANDIDATE …".
5. Each edited `OBD_VOCABULARY.md` header changelog (§ top, lines ~5-6) gains a `v1.2 (2026-06-10) —
   reconciled §12.4 O2FailureMode (7→4) and §5.2 FuelSystemStatus to shipped obdlab code` line.
6. **No `.py` file is touched.** `git diff` shows `.md` changes only — the code is already correct; this is the
   doc catching up. (Owner decision: keep all copies synced, do **not** collapse to pointers — COMLab is
   reworked later.)

### Context ###

`HANDOFF_obdlab_docs_2026-06-10.md` (TODO-1/TODO-2) and AST ground-truth from the 2026-06-10 doc session:
`obdlab` vocabulary = 8 StrEnums, `O2FailureMode` = 4 members. The wiki §12.4 predates `T-OBDV2-ARCH-2`
(orphan-member prune) and `T-OBDV2-4`/`T-OBDV2-FIX-2` (wideband offset). §5.2 predates `T-OBDV2-6`
(`FuelSystemStatus` migration). All three referenced obdlab tasks are `done`, so the code is the settled
truth and the wiki is the lagging artefact. The `comlab/docs/wiki` and `obdlab/docs` copies were verified
**byte-identical** (md5 `f0db8478…`) to the canonical `semantic/vocabul` copy at task-authoring time.

Pinned target text (copy verbatim from code, including comments):

```python
# §12.4 — OBD_VOCABULARY.md must match obdlab/obdlab/schemas/vocabulary.py:113-121
class O2FailureMode(StrEnum):
    NO_FAULT            = "NO_FAULT"            # wiki: §6.7 — healthy baseline, no fault detected
    STUCK_LEAN          = "STUCK_LEAN"          # wiki: §6.7 — pinned < 0.2 V (narrowband)
    STUCK_RICH          = "STUCK_RICH"          # wiki: §6.7 — pinned > 0.85 V (narrowband)
    WIDEBAND_OFFSET_CANDIDATE = "WIDEBAND_OFFSET_CANDIDATE"  # wiki: o2-logic/03 §BIASED_OFFSET / o2-logic/08

# §5.2 — add, matching obdlab/obdlab/schemas/vocabulary.py:82-91
class FuelSystemStatus(StrEnum):   # mirrored in COMLab; sourced from DTC_VOCABULARY §8
    CL = "CL"              # §8 — closed loop; O₂ feedback active
    OL = "OL"              # §8 — open loop; base map (cold start)
    OL_DRIVE = "OL_DRIVE"  # §8 — open loop driving (WOT, decel)
    OL_FAULT = "OL_FAULT"  # §8 — open loop due to O₂ sensor fault
```

### Deliverables ###

1. `labs/semantic/vocabul/OBD_VOCABULARY.md` — §12.4 (7→4), §5.2 (+FuelSystemStatus), changelog v1.2. **[canonical]**
2. `labs/obdlab/docs/OBD_VOCABULARY.md` — identical edit (keep synced per owner decision).
3. `labs/comlab/docs/wiki/OBD_VOCABULARY.md` — identical edit (keep synced; COMLab reworked later).
4. `labs/comlab/docs/wiki/SEMANTIC_CONTRACT.md` — §4.4 `o2_failure_mode` comment 7→4 (propagate semantic-copy fix).

### Files to touch ###

- `labs/semantic/vocabul/OBD_VOCABULARY.md`
- `labs/obdlab/docs/OBD_VOCABULARY.md`
- `labs/comlab/docs/wiki/OBD_VOCABULARY.md`
- `labs/comlab/docs/wiki/SEMANTIC_CONTRACT.md` (§4.4 line only)

### Out of scope ###

- **No `.py` edits.** The code is the source of truth and is already correct.
- **`TestSuite/COM/SEMANTIC_CONTRACT.md`** — a frozen test-harness fixture (May-22), not a live wiki. Editing
  it risks the harness. **Owner decision needed** before any sync — recorded as Unplanned follow-up #4, not
  done here.
- **`FaultFamily`, `ChemicalSignature`, L3 verdict, any registry/proposal entry** — untouched.
- `OBDlab.md` archival (TODO-3), doc-prep skill + ingestion (TODO-4) — separate tasks.
- **FU-OBD-DOC-3** (`obdlab/schemas/vocabulary.py` docstring "7 StrEnums"→8) — coder-lane follow-up, not this
  doc-only task.
- Surgical rule: every changed line is the §12.4 roster, the §5.2 addition, the changelog line, or the §4.4
  comment. Any other drift noticed goes to `PROGRESS.md` "Unplanned follow-ups", not this diff.

### Verification ###

```bash
cd <repo>/labs
# 1) .md-only diff — no code touched
git diff --name-only -- 'semantic/**' 'obdlab/**' 'comlab/**' | grep -vE '\.md$' \
  && { echo "FAIL: a non-.md file changed"; exit 1; } || echo "OK md-only"
# 2) §12.4 roster == shipped 4 members, dead modes gone (each copy)
for f in semantic/vocabul/OBD_VOCABULARY.md obdlab/docs/OBD_VOCABULARY.md comlab/docs/wiki/OBD_VOCABULARY.md; do
  grep -qE 'WIDEBAND_OFFSET_CANDIDATE' "$f" || { echo "FAIL missing wideband: $f"; exit 1; }
  grep -qE 'SLUGGISH|HEATER_FAULT|WRONG_CENTERLINE|^\s*DEAD ' "$f" && { echo "FAIL dead mode left: $f"; exit 1; }
  grep -qE 'class FuelSystemStatus' "$f" || { echo "FAIL missing FuelSystemStatus: $f"; exit 1; }
done; echo "OK rosters"
# 3) single-source invariant — all 3 OBD_VOCABULARY copies identical again
md5sum semantic/vocabul/OBD_VOCABULARY.md obdlab/docs/OBD_VOCABULARY.md comlab/docs/wiki/OBD_VOCABULARY.md \
  | awk '{print $1}' | sort -u | wc -l | grep -qx 1 && echo "OK identical" || { echo "FAIL copies diverge"; exit 1; }
# 4) contract §4.4 synced
grep -q '4 values' comlab/docs/wiki/SEMANTIC_CONTRACT.md && echo "OK contract synced" || { echo "FAIL §4.4 stale"; exit 1; }
# 5) consumer of the corrected text: T-SEM-4 conformance gate stays green (growth-safe, no hardcoded counts)
cd ../comlab && pytest -q -k conformance   # or the T-SEM-4 gate test path; must be green
```

All five checks pass; the T-SEM-4 conformance gate is green.

### Progress hook ###

`tasks/progress_notes/T-SEM-5.md` opens with the confirmed `## Plan` (below), then the coder fills
`VERIFICATION GATE` + `CODE REVIEW`. PROGRESS.md `T-SEM-5`: Status flips to `done` only when both blocks are
clean. Files changed = 4. Verification = "§12.4 7→4 + §5.2 FuelSystemStatus reconciled to shipped obdlab code;
all 3 OBD_VOCABULARY copies md5-identical again; comlab SEMANTIC_CONTRACT §4.4 synced; .md-only diff;
T-SEM-4 gate green".
