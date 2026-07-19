# T-SEM-1 — ISO-primary dual-anchor citations (L1 wire identifiers + L2 routing)

**Status:** `pending (next)` · **Pack:** SEMANTIC · **Mode:** STRICT
**Origin:** `SEMANTIC_STANDARDIZATION_PROPOSAL.md` §2, §10, §11 · **Blocked by:** —
**Consumer (signal/noise):** **N/A — this task edits citation comments + wiki prose only; it adds no field, enum value, or fault.** Its output is consumed by the T-SEM-4 conformance gate, which reads the citations.

### Goal ###

Make 4DLab's existing standards alignment **explicit, dual-anchored, and ISO-primary**. Today the SAE/ISO
anchoring is real but uneven (some enums cite SAE clauses, some cite only a P-code range, the wikis list ISO
as a cross-reference). For a petrol / Euro-1–7 / EU-market engine, ISO is the apt lead standard, and because
SAE J2012↔ISO 15031-6 and J1979↔ISO 15031-5 are **technically equivalent** (proposal §10), making citations
dual-anchor is a pure comment/prose edit with **zero wire-value churn**. Done when every L1 PID identifier and
every L2 routing-tag/DTC enum carries a uniform `ISO 15031-x (≡ SAE Jyyyy)` citation.

### Success criteria ###

- Every PID row in `vocabul/OBD_VOCABULARY.md §2` shows both its **ISO 15031-5** and **SAE J1979** anchor (id/unit/range unchanged).
- Every `DTCRoutingTag` value in `comlab/comlab/schemas/vocabulary.py` keeps its P-code range comment and gains the **ISO 15031-6 (≡ SAE J2012)** anchor; `DTC_REGEX`, `DTCSeverityClass`, `DTCState` docstrings cite ISO-primary too.
- `vocabul/OBD_VOCABULARY.md §1` and `DTC_VOCABULARY.md §1` "Standards anchored" tables are reordered **ISO-primary** with SAE listed as the equivalent (not removed).
- **No enum member, no string value, no field is added, renamed, or removed.** `git diff` shows only comments, docstrings, and `.md` prose.
- Inner loop green (the edits are non-semantic, so `pytest` must be unchanged-green).

### Context ###

Proposal §10 (web-sourced): ISO 15031-6:2015 **references SAE J2012-DA** (Digital Annex) as the canonical DTC
list — they are not alternatives. J1979 ↔ ISO 15031-5 share the bit-encoded PID structure. The in-repo
`labs/semantic/SAE.md` is `J2012 DEC2007` (≡ ISO 15031-6:2005 era); cite it as the working copy and note (do
not act on) that the live list is J2012-DA / ISO 15031-6:2015 — the 1990–2010 P-code set is stable across
these, so no refresh is needed for this task.

The values are the wire format (`SEMANTIC_CONTRACT §8` — "renames of values are breaking changes"). This task
must therefore touch **comments and prose only**. The citation style to apply uniformly:
`# ISO 15031-6 §<clause> / SAE J2012 — <P-code range>` for DTC entries; the §2 table gains an `ISO 15031-5`
column beside the existing `SAE J1979 PID` column.

### Deliverables ###

1. `comlab/comlab/schemas/vocabulary.py` — dual-anchor citation comments on `DTCRoutingTag`, `DTC_REGEX`, `DTCSeverityClass`, `DTCState` (comments/docstrings only).
2. `vocabul/OBD_VOCABULARY.md` — §1 ISO-primary reorder; §2 add ISO 15031-5 anchor column.
3. `vocabul/DTC_VOCABULARY.md` — §1 ISO-primary reorder; §2 cite ISO 15031-6 alongside J2012.

### Files to touch ###

- `comlab/comlab/schemas/vocabulary.py` (comments/docstrings only — NO value/member change)
- `labs/semantic/vocabul/OBD_VOCABULARY.md`
- `labs/semantic/vocabul/DTC_VOCABULARY.md`

### Out of scope ###

Do **not** touch any enum **value/member**, `FaultFamily`, `ChemicalSignature`, the `response.py`/`kg.py`
Literals, or any test. Do **not** refresh `SAE.md` to a newer revision (separate, optional). Do **not** create
the proposals registry — that is T-SEM-2. Surgical rule: every changed line is a citation/prose edit; any
other drift you notice goes to `PROGRESS.md` "Unplanned follow-ups", not this diff.

### Verification ###

```bash
cd <repo>/labs/comlab            # lab root
ruff check comlab/
pyright comlab/
# Guard: NO value/member churn — diff must be comments/docstrings only.
git diff -- comlab/comlab/schemas/vocabulary.py | grep -E '^\+' | grep -vE '^\+\s*#|^\+\s*"""|^\+\+\+' \
  && { echo "FAIL: a non-comment line changed in vocabulary.py"; exit 1; } || echo "OK comments-only"
pytest -x -q                              # must be unchanged-green (no semantic change)
```

All steps pass; `pytest` count unchanged from baseline.

### Progress hook ###

`tasks/progress_notes/T-SEM-1.md` opens with the confirmed `## Plan`, then gains `VERIFICATION GATE` +
`CODE REVIEW`. PROGRESS.md `T-SEM-1`: Status=done, Files changed=3, Verification="dual-anchor ISO-primary
citations applied; zero value churn (comments-only diff verified); suite unchanged-green".
