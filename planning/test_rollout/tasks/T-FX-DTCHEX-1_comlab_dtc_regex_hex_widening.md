# T-FX-DTCHEX-1 — COMLab `DTC_REGEX` hex widening (decimal → hex)

**Pack:** test-rollout (blocker) · **Author:** architect · **Status:** authored · impl pending
**Supersedes the mislabelled `T-FX-13`** reference for the DTCLab↔COMLab DTC-format
gap (the real `T-FX-13` is VINLab's *done* `T-FX-13_maf_map_tecdoc_lookup`; see
ledger FU-TST7-3 for the ID-collision hazard). Also supersedes the never-authored
`T-DTC-REGEX-1` placeholder — the fix is **COMLab-side, not DTCLab-side**.

> **Lab placement note.** The fix lives entirely in `labs/comlab/`. It is tracked
> here because this pack surfaced it (FU-TST7-3) and its rollout rows consume it.
> A coder may equally run it from the COMLab pack — the deliverables are the same.

---

## 1. Goal

Bring COMLab's copy of the DTC validation pattern into line with the canonical
hex form already pinned in its **own wiki** and already shipped in DTCLab, so a
valid hexadecimal DTC (e.g. `P244A`) is no longer false-rejected at COMLab's
ingestion boundary.

A *regex* here is the text pattern (plain-language: the shape-check) that decides
whether a DTC string like `P0171` is well-formed. COMLab's code drifted to a
**decimal-only** shape-check; its wiki and DTCLab both use the correct **hex**
one. This task closes that code-vs-wiki drift. **No new schema field** is added —
this refines an existing consumer's contract (wiki §11.2 "authoritative pin"
class).

## 2. The gap (disk-verified 2026-06-11)

| Site | Pattern | Verdict |
|---|---|---|
| `labs/comlab/comlab/schemas/vocabulary.py:34` | `r"^[BCPU][0-3][0-9]{3}$"` | **decimal-only — wrong** |
| `labs/comlab/docs/wiki/DTC_VOCABULARY.md` §2.3 | `r"^[BCPU][0-3][0-9A-F]{3}$"` | hex — **canonical (truth)** |
| `labs/dtclab/dtclab/schemas/vocabulary.py:108` | `r"^[BCPU][0-3][0-9A-F]{3}$"` | hex — already correct |

The last three characters of a DTC are hex per ISO 15031-6 (≡ SAE J2012) §5.2,
so codes whose final digits carry `A–F` are legal. COMLab's decimal-only class
`[0-9]{3}` rejects them:

```
P244A : decimal=False  hex=True      # GPF — COMLab's OWN routing enum names it
P030C : decimal=False  hex=True      # misfire cyl ≥ 12
P2459 : decimal=True   hex=True      # passes either (all-digit tail)
P0171 : decimal=True   hex=True      # passes either
BAD_CODE / X9999 / P0xxx : invalid under BOTH (negative tests stay red)
```

## 3. Named signal/noise consumer + code path

- **Code path that mis-rejects:** `LabPipelineAggregator.validate_payload` →
  the `_validate_dtc_list` *field validator* (the Pydantic gate that checks each
  DTC string) at `labs/comlab/comlab/schemas/ingestion.py:290-298`, which raises
  `ERR-CONTRACT-001` on `confirmed_dtcs` / `pending_dtcs` / `permanent_dtcs`.
- **Downstream consumer the reject starves:** the `GPF_HISTORY` routing tag at
  `labs/comlab/comlab/schemas/vocabulary.py:462`
  (`# … P244A, P2459 (DNA-gated by has_particulate_filter)`). COMLab is specced
  to route `P244A`, but its own gate throws the payload out first. The DTCLab
  wiki §15 routing table likewise routes `P244A`/`P2459` → `GPF_HISTORY`.

So the consumer is **existing and named**; this is a correctness fix to a live
code path, not a new field. Signal/noise is satisfied with no proposal needed.

## 4. Success criteria

1. `comlab.schemas.vocabulary.DTC_REGEX == r"^[BCPU][0-3][0-9A-F]{3}$"` (matches
   the wiki §2.3 literal and DTCLab byte-for-byte).
2. A `DTCLabPayload`/aggregator payload carrying `confirmed_dtcs == ["P244A"]`
   **passes** `validate_payload` (no `ERR-CONTRACT-001`).
3. The existing negative cases (`BAD_CODE`, `X9999`, `P0xxx`) **still** raise
   `ERR-CONTRACT-001` — widening must not loosen rejection of genuinely malformed
   codes.
4. The drift-guard *unit test* (the test that locks the constant to the wiki)
   asserts the hex literal, and the wiki-parity assertion passes.
5. Inner loop green on the Windows `.venv-wired`: `ruff` clean, `pyright` clean,
   `pytest -x -q` green for `labs/comlab/`.

## 5. Files to touch (exact)

| File | Change |
|---|---|
| `labs/comlab/comlab/schemas/vocabulary.py:34` | `[0-9]{3}` → `[0-9A-F]{3}`; keep the ISO 15031-6 / §2.3 citation comment. |
| `labs/comlab/tests/unit/test_vocabulary.py:112` | Update the asserted literal to the hex form; this is the drift guard, so it must move with the constant. |
| `labs/comlab/tests/fixtures/mock_dtc_lab.py:4` | Update the docstring regex (`[0-9]{3}` → `[0-9A-F]{3}`) so the mock's stated contract matches. |
| `labs/comlab/tests/e2e/test_error_codes.py` | **Add one positive case** in the `TestErrorCodes` group: `confirmed_dtcs == ["P244A"]` passes `validate_payload` (proves criterion 2). Leave the three existing negative cases untouched. |

No wiki edit — the wiki is already correct; this task makes the code catch up to it.

## 6. Out of scope (→ Unplanned follow-ups, not this diff)

- The DTCLab-side regex (already hex-correct — do **not** touch).
- The v6 master corpus currently contains **zero** hex-tail DTCs, so this fix
  changes no existing `dtclab_cases.csv` / `obdlab_cases.csv` row outcome today;
  it removes a **latent** false-reject. Do not add hex DTCs to the corpus here.
- Any COMLab v2 rework (`T-COMV2-*`) — this is a standalone pre-rework contract
  fix and must not wait on, or pull in, that program.

## 7. Sequencing correction (read before re-pointing T-TST-9)

The ledger previously listed this gap as T-TST-9's blocker. Disk check shows that
is **imprecise**:

- **T-TST-9 (isolated dtclab generative harness) does NOT depend on this fix.**
  DTCLab's own regex is already hex-correct, and the corpus has no hex DTCs, so
  the isolated harness runs through `dtclab.process()` untouched by COMLab.
- This fix gates the **connected** path only — `T-TST-8W` and `T-TST-10`
  (DTCLab→COMLab fusion), where a `P244A` payload would otherwise be rejected at
  COMLab ingestion.

Net: closing T-FX-DTCHEX-1 unblocks the connected rollout rows and removes a
latent boundary bug; it should **not** continue to be cited as a hard blocker on
the isolated T-TST-9.

## 8. Verification (coder fills both gate blocks in `progress_notes/T-FX-DTCHEX-1.md`)

- **VERIFICATION GATE:** criteria 1–5 above; show the `pytest -x -q` summary for
  `labs/comlab/` and the P244A positive-case result.
- **CODE REVIEW:** confirm only the four files in §5 changed; confirm no new
  schema field; confirm the three negative tests still red; confirm the citation
  comment survived.

## 9. GPF Removal annotation (2026-06-11, T-GPF-RM-2)

`GPF_HISTORY` (the §3 downstream consumer cited at task-authoring time) is **no
longer** the regex's downstream consumer — GPF has been removed by the GPF
Removal pack (T-GPF-RM-2). The hex `DTC_REGEX` stays and remains justified by
the general ISO 15031-6 hex-code requirement (wiki §2.3) and by other valid
hex-tailed codes (e.g. `P030C` — misfire cylinder ≥ 12).
