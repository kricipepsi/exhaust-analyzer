# DNALab Tri-Module Audit — dna · vin · symptom

**Date:** 2026-06-12
**Scope:** the three DNALab modules — `dna` (`dnalab/`), `vin` (`vinlab/`), `symptom` (`symptomlab/`).
**Lenses applied per module:** code-review-excellence, uncle-bob-craft, improve-codebase-architecture (from `_skills/codingskills`).
**Trigger:** all coder tasks for DNALab reported finished; this is the post-completion audit + full test run.

> Nomenclature note (owner-flagged, to resolve later): "DNALab" is used here as the
> umbrella for all three modules, while `dnalab/` is also the name of the `dna` assembly
> package specifically. This audit keeps **dna / vin / symptom** as the module names.

---

## 1. Test-suite results (full inner loop)

Inner loop = the three automated gates a coder runs: **ruff** (style/lint linter — catches
unused imports, ordering, formatting), **pyright** (static type-checker — verifies types line
up without running the code), and **pytest** (runs the unit tests).

| Module | ruff | pyright | pytest | Verdict |
|---|---|---|---|---|
| **vin** (`vinlab`) | clean | 0 errors / 0 warn | **173 passed, 15 skipped** | GREEN |
| **symptom** (`symptomlab`) | clean | 0 errors / 0 warn | **63 passed** | GREEN |
| **dna** (`dnalab`) | clean | 0 errors / 0 warn | **27 passed** | GREEN |
| **Total** | clean | 0 / 0 | **263 passed, 15 skipped, 0 failed** | GREEN |

All three suites pass on Python 3.14. The 15 vin skips are conditional fixtures (CSV/db
suites), not failures.

### Environment defect found while running (infrastructure, not code)

Running dna's suite surfaced a **file-sync problem on the Linux mount**, not in the source:

- `dnalab/pyproject.toml` arrived **truncated** (cut mid-line at `typeCh…`), which broke
  install, pytest config, and ruff/pyright config loading.
- Three dna test files (`test_assembly.py`, `test_models.py`, `test_vehicledna_roundtrip.py`)
  arrived truncated / null-padded on the mount.

The **canonical Windows copies of all four files are complete and valid** (verified field-by-field), and `assembly.py`/`models.py` matched byte-for-byte across both views — so the
audit subject is trustworthy and the dna suite was run against faithfully reconstructed
copies (27/27 pass). **Action for you:** open `labs/dnalab/pyproject.toml` in your editor
once and confirm the last line is `extraPaths = ["../vinlab", "../symptomlab"]`. If it ends
at `typeCh`, the on-disk file is genuinely corrupt and the real coder/CI will break — re-save
it. If it looks whole, this was only a transient mount hiccup and nothing on disk needs fixing.

---

## 2. Headline finding — `load_state` is an orphan (signal/noise breach)

> **Correction (2026-06-12, post-publication).** This section overstated the severity.
> COMLab is built **last** (Stage 4); its ledger states that an emitted field whose consumer
> is *forward-registered* is **compliant** until then — anti-orphan is a Stage-4-close gate,
> not a live one. `load_state` **does** have a named consumer: proposal **COMLab-B**
> (`comlab/config/proposals/entries.yaml`), the context-modifier prior with a 65% trust cap.
> The real, narrower defect is that COMLab-B is **not forward-registered** in
> `comlab/tasks/PROGRESS.md` or `CROSS_LAB_DEPENDENCIES.md` (unlike every sibling field), so
> it would be off the S4 anti-orphan checklist. Tracked as **T-DNA-11** (ledger fix, no code).
> Read the rest of this section with that reframing in mind.

This is the one finding that touches the project's single hard rule: *every field added to any
schema must have a named, existing consumer in COMLab analytics or fault-atlas routing.*

`load_state` (the `LoadState` enum on `EnvironmentalConditions`, added by **T-DNA-2**) is:

- **defined** in `symptomlab/models.py`,
- **serialized** through `symptom_dna → environmental_conditions.load_state` and round-tripped
  in dna's payload, and **covered by tests**, but
- **read by no live code path in COMLab.** `comlab/core/symptom_router.py` consumes only
  `engine_state` and `occurs_during`; its own docstring lists the SymptomDNA fields it
  deliberately ignores. A repo grep confirms **zero** non-test COMLab references to `load_state`.

A green test run does **not** clear this — a round-trip test is not a consumer. Per the
anti-orphan rule, a field read nowhere is a signal/noise breach regardless of passing tests.

```
 symptomlab.models.LoadState ──► SymptomDNA.environmental_conditions.load_state
        │                                    │
   (serialized, tested)                 (in JSON payload)
        │                                    │
        ▼                                    ▼
   COMLab symptom_router.py  ──reads──►  engine_state, occurs_during   ✓ consumed
                             ──reads──►  load_state                     ✗ NO consumer
```

**Disposition (your call — this is the architect's decision, not the coder's):**

1. **Name the consumer and ship it** (the v2-rework default): add the load-state routing rule
   to `symptom_router.py` — e.g. `load_state == transient_acceleration` promoting a load-dependent
   hypothesis — and register it as a proposal with its code path. This is forward progress.
2. **Defer to PENDING** only if no consumer can be named even as a proposal — then `load_state`
   should not be live in the shipped schema yet.

The current state (live field, no consumer, "future use") is exactly the disposition the rule
forbids. `free_text_notes` is a softer version of the same thing (no COMLab consumer), but it
is a human-readable notes field plausibly consumed by the UI/report layer rather than analytics,
so it is a lower-priority question rather than a breach.

---

## 3. Per-module findings

Severity key: **[S]** signal/noise · **[C]** correctness/clarity · **[K]** craftsmanship · **[A]** architecture · **[nit]** cosmetic.

### 3.1 dna — `dnalab/assembly.py` (46), `dnalab/models.py` (92)

Smallest and cleanest of the three. A deep module (a lot of behaviour behind a tiny interface):
one public function `build_vehicle_dna(vin, triage)` and one frozen dataclass (an immutable
record type) `VehicleDNA`.

| # | Sev | Finding | Recommendation |
|---|---|---|---|
| D1 | C/K | **`to_json()` means two different things.** `VinDNA.to_json()` and `SymptomDNA.to_json()` return a **dict**; `VehicleDNA.to_json()` returns a **str**, and the dict version is `VehicleDNA.to_json_payload()`. Same verb, different return type across the JSON boundary — a reliable source of confusion. | Pick one convention: e.g. `*_payload()` → dict, `*_json()` → str, applied to all three models. Cross-lab rename — spec it, don't hot-fix. |
| D2 | nit | `from_json_payload` raises `ValueError` on schema-version mismatch but lets `KeyError` propagate for missing top-level keys. Asymmetric error type. | Documented already; acceptable. Optionally wrap missing keys in a typed error for a uniform boundary contract. |
| D3 | A | dna **imports vinlab + symptomlab directly** (`assembly.py`, `models.py`). This is the one sanctioned cross-lab import — dna is the composition seam (the join point) — whereas COMLab mirrors types locally instead. | Correct by design; documented here so the asymmetry isn't mistaken for a rule violation. No change. |
| ✓ | — | Fail-fast ordering is correct: missing-triage-key check raises **before** either `_decode_vin` or `_resolve_symptom` runs (test-confirmed). `SCHEMA_VERSION` is centralised. Frozen dataclasses give immutability. | Keep. |

### 3.2 symptom — `symptomlab/models.py` (101), `symptomlab/validator.py` (72)

| # | Sev | Finding | Recommendation |
|---|---|---|---|
| S1 | **S** | **`load_state` orphan** — see §2. The field is owned here. | Name a consumer (proposal) or move to PENDING. |
| S2 | C/nit | **`EngineState.WONT_START = "won_not_start"`** reads like a typo. It is **not** — COMLab's `symptom_router.py` mirrors the exact string `"won_not_start"`. **Do not "fix" this value** without a coordinated COMLab change; it is the JSON-boundary contract string. | Leave the value. Optionally add a one-line comment pinning it to the COMLab mirror so the next reader doesn't "correct" it. |
| S3 | K | `SymptomValidator.__init__` reads YAML from disk (I/O in a constructor). Mildly complicates isolated testing. | Mitigated: path is injectable (`allowed_path`) and the validator is cached via `lru_cache`. Acceptable as-is. |
| S4 | nit | `resolve()` makes the env trio keyword-only; `validator.validate()` takes them positionally. Minor interface drift between the two. | Optionally make `validate()` keyword-only for the env trio to match `resolve()`. |
| ✓ | — | **Good deliberate design:** closed vocabularies are `StrEnum` (a fixed string-valued enum), open vocabularies (`tier_1`/`tier_2`) are plain `str` validated against YAML — documented, so adding a symptom needs no code change. The exactly-18-pairs invariant is hard-checked at load. | Keep. |

### 3.3 vin — `vinlab/decoder.py` (644), `vinlab/models.py` (306)

The heaviest module and the one with the real refactor opportunity.

| # | Sev | Finding | Recommendation |
|---|---|---|---|
| V1 | **A/K** | **`decode_vin_payload()` is ~290 lines in one method** doing ~10 jobs (validate → WMI → year → engine → vref.db → emissions → CoC → cylinder heuristic → air metering → confidence → assemble). Violates single-responsibility (one unit, one job) and is hard to unit-test in pieces. | Decompose (split into smaller named functions) along the seams that already exist as comment banners: `_resolve_engine_attributes`, `_resolve_coc`, `_resolve_emissions`, `_resolve_air_metering`. The overlay modules (`air_metering`, `cylinder_heuristic`, `horizon`, `stress_rpm`, `switches`) are the precedent — continue that pattern inward. Highest-value deepening opportunity in the three modules. |
| V2 | **C** | **Checksum comment vs. code mismatch.** Comment (line ~541) says "valid check digits are 0-9, X", but the guard `if vin[8] not in "123456789X"` **excludes `0`** — so any VIN whose check digit is `0` silently bypasses checksum validation. Likely intentional (European dummy markers) but the comment contradicts the code. | Confirm intent. If `0` should bypass, fix the comment to say so; if not, add `0` to the set. Either way the ambiguity is a latent correctness trap. |
| V3 | K | **Magic strings vs. enum members.** Lines ~449–457 compare enum-typed values to bare string literals (`_fuel_delivery_type != "CARBURETOR"`, `_induction_type in ("TURBOCHARGED","SUPERCHARGED")`, `== "GDI"`). Works only because `StrEnum` members equal their string value; fragile if a value is ever changed. | Compare against the enum members (`InductionType.TURBOCHARGED`, etc.) for type-safe, refactor-proof checks. |
| V4 | nit | CoC-null scan (`for fld in coc_fields … break`) stops at the first null, so `conf_flags` records only one `coc_null_*` reason even when several are null. | Fine if one flag is enough to downgrade to PARTIAL; if per-field reasons matter to COMLab, drop the `break`. |
| V5 | nit | `float()/int()` CSV parses are wrapped in `try/except … pass` — malformed cells are swallowed silently (defaults retained). | Acceptable; consider a debug-level log so bad source rows are traceable. |
| ✓ | — | **Strong traceability:** every lookup table and constant carries a source citation (NHTSA 49 CFR 565, SAE J853, ISO 3780). `downstream_trim_role` and `has_catalyst` both have live COMLab consumers (4 and 11 files) — signal/noise clean. `_resolve_engine` two-path fallback is a clean deep helper. | Keep. |

---

## 4. Cross-module verdict

The three modules are **functionally green and well-documented**, with citation discipline and
deliberate type design that exceed the minimum bar. Two things stand between "tests pass" and
"audit-clean":

1. **`load_state` orphan (§2)** — the only hard-rule (signal/noise) breach. Needs a named
   consumer or a move to PENDING. Architect decision.
2. **`decode_vin_payload` decomposition (V1)** — the only sizeable craftsmanship/architecture
   debt. Not blocking, but it is where future bugs will hide.

Everything else is clarity-level (the `to_json` naming split D1, the checksum comment V2) or
cosmetic.

---

## 5. Unplanned follow-ups (off-scope discoveries — not changed in this audit)

| ID | Item | Origin |
|---|---|---|
| U-1 | Decide `load_state` disposition: name a COMLab consumer (proposal) or move to PENDING. | §2 / S1 |
| U-2 | Verify `labs/dnalab/pyproject.toml` is intact on disk (not truncated at `typeCh`). | §1 |
| U-3 | Unify `to_json` naming across VinDNA / SymptomDNA / VehicleDNA (cross-lab rename — spec it). | D1 |
| U-4 | Spec `decode_vin_payload` decomposition into the four already-banner-marked helpers. | V1 |
| U-5 | Resolve the checksum `0` comment/code mismatch (correctness clarification). | V2 |
| U-6 | Replace magic-string enum comparisons in `decoder.py` with enum members. | V3 |
| U-7 | Resolve the "DNALab umbrella vs. `dnalab` package" naming overload (owner-flagged). | header |

*Per workspace rules these are tracked here, not folded into any diff. Each U-row that
implies a schema/code change still needs a task spec with a named consumer before it ships.*
