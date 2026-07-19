# T-SEM-4 — growth-safe conformance + extensibility gate

**Status:** `pending` · **Pack:** SEMANTIC · **Mode:** STRICT
**Origin:** `SEMANTIC_STANDARDIZATION_PROPOSAL.md` §4.1, §11 · **Blocked by:** `T-SEM-1`, `T-SEM-3`
**Consumer (signal/noise):** the test itself is the consumer — it reads the T-SEM-1 citations + the T-SEM-2/3 registry and makes both the standards-conformance **and** the signal/noise rule mechanical. This is the artefact that lets the standard stay **open** without silent drift.

### Goal ###

Author the drift-guard test that **closes** the pack by making the standard self-policing and
**growth-safe**: future faults can be added freely *provided* they carry a citation and a named consumer, and
the test fails loudly if they don't. It asserts three things, all by **dynamic iteration (no hardcoded
counts)** so additions never require editing the test: (1) every L1 PID identifier matches the J1979 CSV;
(2) every L2 cited P-code resolves in `SAE.md`; (3) every `comlab/config/proposals/` entry has a non-empty
`consumer` (file+symbol) and a dual ISO/SAE citation. Done when the test is green on the current vocabulary
**and** demonstrably red on a planted bad entry (missing consumer / missing citation / bogus P-code).

### Success criteria ###

- New `comlab/tests/unit/test_vocabulary_sae_iso_conformance.py` (mirrors the existing `test_vocabulary.py` drift-guard pattern).
- **L1 check:** for each PID row parsed from `vocabul/OBD_VOCABULARY.md §2`, assert name/id/unit/range agree with `labs/semantic/obd2-pid-table-service-01.csv` (J1979). Iterates the table — adding a PID row needs no test edit.
- **L2 check:** for each `DTCRoutingTag` member, parse the cited P-code(s) from its comment and assert each resolves to a real definition line in `labs/semantic/SAE.md`. Iterates the enum — adding a tag needs no test edit.
- **Registry / signal-noise check (the extensibility guard):** for each entry in `comlab/config/proposals/`, assert (a) `consumer` is present and names a file path that exists + a symbol, and (b) `iso_sae_citation` is present (or `family: cross-cutting` with a consumer code path). **Dynamic** over the entries dir — a new well-formed entry passes automatically.
- **Negative proof:** the task includes (and the note records) a temporary planted-bad-entry run showing the gate goes red for: missing `consumer`, missing citation, and a P-code not in `SAE.md`. The planted entry is removed before commit.
- **No hardcoded family/value/entry counts anywhere in the test.** Grep proof in verification.
- Inner loop green; the new test green on the real tree.

### Context ###

The existing `comlab/tests/unit/test_vocabulary.py` already enforces enum↔wiki traceability — this task adds
the **standards + signal/noise** counterpart. The "no hardcoded counts" requirement is the heart of the
owner's "semantic must be open to further additions": a gate that asserts `len(FaultFamily) == 12` would
block every future fault; a gate that asserts *"every member is well-formed"* welcomes them while still
catching a citation-less or consumer-less addition (a signal/noise breach). This is also the anti-orphan check
(CLAUDE.md) made automatic for the proposals registry.

Parsing notes: `SAE.md` P-codes appear as line-leading tokens (e.g. `P0171 System Too Lean Bank 1`); a
P-code "resolves" if a line matching `^<code>\b` exists. The J1979 CSV header is
`PID (dec),PID (hex),Name (short),Name,...,Min,Max,Unit,...`. Match `OBD_VOCABULARY §2` rows to the CSV by
hex PID id.

### Deliverables ###

1. `comlab/tests/unit/test_vocabulary_sae_iso_conformance.py` — the three dynamic checks above.

### Files to touch ###

- `comlab/tests/unit/test_vocabulary_sae_iso_conformance.py` (NEW)
- (reads, does not modify: `vocabulary.py`, `OBD_VOCABULARY.md`, `obd2-pid-table-service-01.csv`, `SAE.md`, `comlab/config/proposals/`)

### Out of scope ###

Do **not** modify vocabulary values, the registry entries, or `FaultFamily`. Do **not** add a J1979 decoder
or a DTC parser beyond the minimal line/row matching the asserts need. Do **not** hardcode any count. Off-scope
finds → `PROGRESS.md` follow-ups.

### Verification ###

```bash
cd <repo>/labs/comlab
ruff check comlab/ tests/
pyright comlab/ tests/
# No hardcoded counts (must return nothing)
grep -nE '==\s*[0-9]+\s*#?.*(family|families|values|entries)|len\([A-Za-z_]+\)\s*==\s*[0-9]+' \
  tests/unit/test_vocabulary_sae_iso_conformance.py \
  && { echo "FAIL: hardcoded count in conformance test"; exit 1; } || echo "OK no hardcoded counts"
# Green on the real tree
pytest -x -q tests/unit/test_vocabulary_sae_iso_conformance.py
# Negative proof (documented in the note): plant a bad entry, expect RED, then remove
#   - entry missing `consumer`      -> test fails
#   - entry missing citation        -> test fails
#   - DTCRoutingTag bogus P-code     -> test fails
pytest -x -q
```

All steps pass; negative-proof runs recorded in the progress note; planted entry removed before commit.

### Progress hook ###

`tasks/progress_notes/T-SEM-4.md` opens with `## Plan`, then `VERIFICATION GATE` (incl. the 3 negative-proof
runs) + `CODE REVIEW`. PROGRESS.md `T-SEM-4`: Status=done, Files changed=1, Verification="growth-safe
conformance gate green; no hardcoded counts (grep clean); negative proof red on missing-consumer /
missing-citation / bogus-P-code". **When T-SEM-4 is done the SEMANTIC pack is closed.**
