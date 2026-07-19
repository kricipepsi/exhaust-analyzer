# T-DNA-13 — Audit clarity fixes: `to_json` naming (D1) · checksum comment (V2) · magic strings (V3)

**Authored:** 2026-06-12 (architect). **Source:** tri-module audit
`labs/dnalab/docs/audits/AUDIT_2026-06-12_trimodule_dna_vin_symptom.md` §3 (D1, V2, V3).
**Type:** clarity/correctness; **no JSON wire shape changes.**

Three independent low-risk fixes bundled per owner selection. A coder tight on context may
split D1 into its own session — it is the only one that touches all three labs; V2 and V3
are vinlab-local and trivial. **None changes the emitted JSON.**

---

### Part A — D1: unify `to_json` naming across the three models ###

**Problem.** `to_json()` means two different things: `VinDNA.to_json()` and
`SymptomDNA.to_json()` return a **dict**; `VehicleDNA.to_json()` returns a **str** (its dict
form is `to_json_payload()`).

**Fix (convention to apply to all three models):** `to_json_payload()` → **dict**,
`to_json()` → **str**. Rename each leaf model's current dict-returning `to_json()` →
`to_json_payload()`, and add a thin `to_json()` str wrapper (`json.dumps(self.to_json_payload())`).
Update internal callers: `VehicleDNA.to_json_payload` calls `vin_dna.to_json()` /
`symptom_dna.to_json()` (→ `.to_json_payload()`).

**Wire-safety:** the dict **keys and values are unchanged** — only Python method names move.
COMLab is unaffected (it consumes plain JSON dicts, never calls these methods). Blast radius
= the three lab packages + their tests only.

### Part B — V2: checksum comment vs. code (`decoder.py` ~line 541-545) ###

**Problem.** Comment says "valid check digits are 0-9, X" but the guard
`if vin[8] not in "123456789X"` **excludes `0`**, so a check digit of `0` silently bypasses
validation.

**Fix decision (verify against `VINlookup.md` §1 first):**
- **Default (no behaviour change):** if a pos-9 `0` is intentionally a European dummy
  marker, **fix the comment** to state that `0` is treated as a dummy/bypass — keep the code.
- **Only if** the wiki says `0` is a real check digit that must validate: add `0` to the set
  (`"0123456789X"`) — but this changes which VINs pass, so it **must** be re-run against the
  full vin suite and any failures triaged. Do not flip behaviour without the wiki backing it.

### Part C — V3: magic strings → enum members (`decoder.py` ~lines 449, 454-457) ###

**Problem.** Enum-typed values compared to bare string literals
(`_fuel_delivery_type != "CARBURETOR"`, `_induction_type in ("TURBOCHARGED","SUPERCHARGED")`,
`== "GDI"`). Works only because `StrEnum` members equal their string value — fragile.

**Fix:** compare against the enum members (`FuelDeliveryType.CARBURETOR`,
`InductionType.TURBOCHARGED`/`.SUPERCHARGED`, `FuelDeliveryType.GDI`). Behaviour-preserving.

---

### Named signal/noise consumer ###

N/A — no schema field added. D1 renames methods (wire unchanged); V2 is comment-or-guard;
V3 is behaviour-preserving. Gate = all suites green: **dnalab + vinlab + symptomlab** (and a
quick comlab run for D1 reassurance, though comlab should be untouched).

### Success criteria ###

- D1: all three models expose `to_json_payload()` (dict) + `to_json()` (str); callers/tests
  updated; emitted JSON byte-identical (assert an unchanged payload in a test).
- V2: comment and code agree; if behaviour changed, full vin suite re-run and green.
- V3: no bare-string enum comparisons remain in `decoder.py` (grep clean).
- Inner loop clean in every edited lab.

### Files to touch ###

- `labs/vinlab/vinlab/models.py`, `labs/symptomlab/symptomlab/models.py`,
  `labs/dnalab/dnalab/models.py` (MODIFY — D1)
- `labs/vinlab/vinlab/decoder.py` (MODIFY — V2 comment/guard, V3 enum members)
- `labs/*/tests/unit/` touching `to_json` (MODIFY — D1 caller/asserts)

### Out of scope ###

The decoder decomposition (T-DNA-12). The engine_state rename / schema bump (T-DNA-10). Any
change to JSON keys or values.

### Verification ###

```bash
cd $HOME/mnt/4DLab/4DLabV2
grep -nI '"\(CARBURETOR\|TURBOCHARGED\|SUPERCHARGED\|GDI\)"' labs/vinlab/vinlab/decoder.py  # V3: expect none in comparisons
for L in vinlab symptomlab dnalab comlab; do (cd labs/$L && ruff check . && pyright . && pytest tests -x -q); done
```

### On completion ###

Both gates clean in `progress_notes/T-DNA-13.md`; flip the row → `done`. STOP. If D1 was
split to its own session, record that in the note and keep the row open until all three parts land.
