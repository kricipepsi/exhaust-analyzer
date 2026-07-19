# EVAL-VLIVE-1 run — Claude (Claude Code, Opus 4.8)

- **Agent id:** `claude` (peer of agy/codex; separate run file so no collision).
- **Start:** 2026-06-29 11:25:29 CEST · **End:** 2026-06-29 11:28:58 CEST (~3.5 min, one focused pass).
- **Method note:** I leaned mostly on `grep -rn` over `labs/` plus targeted `file:line` reads,
  and used the in-file `consumer:` / docstring annotations to confirm liveness. I ran the
  `vault_query.py consumers` view once to orient on which docs carry framed `consumers`
  frontmatter; for symbol→caller tracing raw grep was faster and gave exact `file:line`.

---

## P1 — Blast radius: changing `DTCRoutingTag` emission

DTCLab emits `routing_tags: list[DTCRoutingTag]` on its payload
(`labs/dtclab/dtclab/core/routing_tag_mapper.py:51` `map()` → mirrored at the COMLab boundary
as `DTCLabPayload.routing_tags`, `labs/comlab/comlab/schemas/ingestion.py:304`).

### (a) Downstream consumers of the routing tags (COMLab — lab isolation means consumers mirror the type locally)

1. **`fault_atlas_router.py` — registry tag-gate prune (Phase 1+2).**
   `labs/comlab/comlab/core/fault_atlas_router.py:830` `_prune_rules(...)` (called ~:983): a
   registry row carrying a `routing_tag` only survives if that tag is in `routing_tags`
   (`:857–:873`). Tags absent → tag-gated rows pruned. **LIVE.**
2. **`fault_atlas_router.py` — POA/EGR history injection.** `:953–:964` `execute_triage_loop`:
   COMLab *appends* `DTCRoutingTag.POA_HISTORY` (when GASLab `chemical_state == POA_SIGNATURE`)
   and `DTCRoutingTag.EGR_HISTORY` (EGR dilution) into the working `routing_tags` list. This is a
   consumer **and** an in-COMLab producer (POA is no longer emitted by DTCLab — see the module
   docstring at `routing_tag_mapper.py:4`). **LIVE.**
3. **`fault_atlas_router.py` — multi-tag corroboration set.** `:1056–:1061` uses
   `VVT_HISTORY / THERMAL_HISTORY / MISFIRE_HISTORY` membership (`set(routing_tags) & supporting_tags`)
   as a supporting-evidence gate. **LIVE.**
4. **`fault_atlas_router.py` — tag→family discriminator lift (v1 path).** `:1114–:1117` iterates
   `routing_tags` and applies the `tag_discriminator.yaml` family prior
   (`config/tag_discriminator.yaml`, default path `:135`). **LIVE.**
5. **`fault_atlas_router.py` — tag→family discriminator lift (v2/registry path, T-FX-REG-3).**
   `:2021–:2049` reads `_req.dtc_lab_output.routing_tags`, applies a bounded additive score lift to
   the mapped `fault_family`, then re-sorts and rewrites `confidence_score`. **LIVE** (gated by
   `USE_V2_REGISTRY`, default `"1"` per `lab_pipeline_aggregator.py:120`).
6. **`tag_discriminator.yaml`** — config consumed by #4/#5 (maps each `DTCRoutingTag` → `FaultFamily`
   prior). Not code, but editing the enum can orphan/garble a mapping key here. **LIVE config.**

(`lab_pipeline_aggregator.py:613` also `model_dump()`s the whole `dtc_lab_output` into the response
envelope for transparency — a passthrough, not a semantic consumer of the *tag values*.)

**Source/Method:** `grep -rn "DTCRoutingTag\|routing_tag" labs/comlab/comlab` then read
`fault_atlas_router.py` at the cited lines; `routing_tag_mapper.py:1-10,51` for the producer side.

### (b) DTCLab tests guarding this area

- `labs/dtclab/tests/unit/test_routing_tag_mapper.py` — the dedicated guard (P0171→LEAN, P0300→MISFIRE,
  P0420/P0430 catalyst gate, EGR gate, enum-order determinism, HIGH/PARTIAL/NONE DNA-gate branches).
- `labs/dtclab/tests/unit/test_vocabulary.py` — enum membership/values (`DTCRoutingTag`).
- `labs/dtclab/tests/unit/test_payload.py` — payload carries `routing_tags`.
- `labs/dtclab/tests/unit/test_classify_top3.py`, `test_family_map.py`, `test_rank_candidates.py` —
  reference routing tags in ranking/family logic.
- `labs/dtclab/tests/integration/test_dtclab_pipeline.py` — end-to-end emit.
- `labs/dtclab/tests/generative/test_combinatorial.py` and `tests/test_cases.py` (+ regression
  fixtures `case_01..05`) — broad regression.

**Source/Method:** `grep -rln "routing_tag\|DTCRoutingTag\|RoutingTagMapper" labs/dtclab/tests/`.

### Consumers NOT yet live — FLAG

- **None of the six COMLab consumers above are dormant — all are on the live router path.**
- The only thing to flag is the inverse: the two enum members added late by T-DOC-15 —
  **`COOLANT_SYSTEM_MALFUNCTION`** and **`CYLINDER_FLUID_MISFIRE`**
  (`vocabulary.py:466-467`) are cross-field tags with no `dna_gate` and no entry I could find in
  `tag_discriminator.yaml`; they exist in the enum but aren't wired to a discriminator family, so a
  change to their emission would currently have **no live downstream effect**. Worth confirming
  against `tag_discriminator.yaml` before relying on them.

---

## P2 — Cross-lab trace: where COMLab actually READS `VehicleDNA`

DNALab assembles a `VehicleDNA` envelope; COMLab mirrors it as
`comlab.schemas.ingestion.VehicleDNA` (`labs/comlab/comlab/schemas/ingestion.py:138`).

**Real readers of `VehicleDNA` / its `vin_dna` in COMLab:**

1. **`comlab/core/horizon_context_injector.py:70` — `HorizonContextInjector.from_vehicle_dna(self, vehicle_dna)`.**
   Reads `vehicle_dna.vin_dna.resolved_horizon` (`:77`), `.cylinder_count` (`:78`),
   `.number_of_banks` (`:79`) → returns `HorizonContext`. This is the one method that consumes a
   `VehicleDNA` *object*.
2. **`comlab/projection.py:43` — `project(vehicle_dna_json, *, target)`** and
   **`:116` `project_all(vehicle_dna_json)`.** Read the `vin_dna` dict (`:53`) and fan it out into
   the three frozen `LabDnaView`s (gas/obd/dtc). These read a `VehicleDNA` **JSON dict**
   (`VehicleDnaJson`), not the pydantic model, but they are genuine readers of the envelope's fields.

**Liveness caveat (flagging, because P2 says "actually reads"):** grep for callers shows
`from_vehicle_dna` and `project_all` have **no non-test caller** anywhere in `labs/` or `apps/`
(`grep -rn "from_vehicle_dna\|project_all" --include=*.py labs/ apps/ | grep -v /tests/` → only
defs + the docstring pointer in `lab_dna_views.py:7`). On the **live** aggregator path,
`LabPipelineAggregator` constructs a `HorizonContextInjector` (`lab_pipeline_aggregator.py:125`) but
only ever calls `self._injector._load_masks()` (`:220`) — it takes horizon/cylinder data from
`request.metadata` (`SessionMetadata.resolved_horizon`, `:607-608`), **not** from a `VehicleDNA`
object. So today the readers are real code with real tests but are exercised by their unit tests
(`tests/unit/test_horizon_context_injector.py`, projection tests) rather than the running pipeline.

**Wrong answers I explicitly rejected:** `lab_pipeline_aggregator.py` *looks* like it reads
`VehicleDNA` (it holds the injector) but it does not call `from_vehicle_dna`; and
`schemas/lab_dna_views.py` only *documents* the consumer — neither is a reader.

**Source/Method:** `grep -rn "vehicle_dna\|VehicleDNA\|vin_dna\|from_vehicle_dna\|project_all" labs/comlab --include=*.py`;
read `horizon_context_injector.py:70-79`, `projection.py:43-125`, `lab_pipeline_aggregator.py:125,220,605-610`.

---

## P3 — Test selection after editing `labs/vinlab/vinlab/overlay/horizon.py`

This file defines `euro_to_horizon()` (`:10`) and `_year_to_horizon()` (`:28`).

### (a) Tests you must run

- **`labs/vinlab/tests/unit/test_horizon.py`** — the direct guard: imports
  `_year_to_horizon, euro_to_horizon` (`:8`), asserts contract §6.4 mapping
  (`test_euro_to_horizon_matches_contract`), the unknown-category `ValueError`
  (`test_euro_to_horizon_rejects_unknown_category`, `:28`), and the year bands
  (`test_year_to_horizon_matches_vinlookup_bands`, `:44`).
- **`labs/vinlab/tests/unit/test_decoder.py`** — `euro_to_horizon` is called inside
  `decoder.py:646` to set `VinDNA.resolved_horizon` (`decoder.py:669`), so the decoder's
  horizon/stress-RPM assertions exercise this path. Also re-run `test_stress_rpm.py`
  (consumes `horizon`) and the rest of `vinlab/tests/unit/` is cheap — run the package.

### (b) Downstream consumers in OTHER labs to sanity-check

The output is `VinDNA.resolved_horizon` (`vinlab/models.py:211`). It crosses lab boundaries via the
JSON envelope (no cross-lab import of `euro_to_horizon` itself — confirmed):

- **DNALab** — `dnalab/assembly.py:9` calls `vinlab.decode()` and `dnalab/models.py:16` imports
  `vinlab.models.VinDNA`, carrying `resolved_horizon` into the assembled `VehicleDNA`. Sanity-check
  `dnalab/tests/unit/test_assembly.py` and `test_assembly_integration.py`.
- **COMLab** — consumes `resolved_horizon` two ways: (1) `projection.py:55-57` reads it from the
  `vin_dna` JSON (with `_horizon_from_euro` fallback at `:23`), and (2) the live pipeline reads
  `SessionMetadata.resolved_horizon` (`ingestion.py:158`) used by `fault_atlas_router` era masks.
  Sanity-check `comlab/tests/unit/test_horizon_context_injector.py` and the projection tests.

Note the mapping logic is duplicated, not imported: COMLab's `_horizon_from_euro`
(`projection.py:23`) mirrors `euro_to_horizon` over the JSON boundary (rule 5). **If you change the
euro→horizon bands in vinlab, COMLab's `_horizon_from_euro` fallback must be updated in lockstep** —
grep won't catch it as a caller because it's an intentional mirror.

**Source/Method:** `grep -rln "euro_to_horizon\|vinlab.overlay\|from vinlab" labs/ apps/ --include=*.py`;
`grep -rn "euro_to_horizon" ... | grep -v /tests/` (callers); `decoder.py:646,669`,
`vinlab/models.py:211`, `projection.py:23-57`, `ingestion.py:158`.

---

## P4 — Governance: adding `cold_start_enrichment_pct` "for future use"

**Not shippable as-is.** AGENTS.md **rule 4** (Signal/noise — quoted): *"A field/fault ships only
with a **named** consumer + code path in COMLab analytics or fault-atlas routing (`"future use"` is
not a consumer)."* "For future use" is exactly the disallowed justification.

What must accompany it to ship:

1. A **named consumer** — a concrete `file:function` in COMLab analytics (`PowerLossAnalytics`) or
   `fault_atlas_router.py` that actually reads the field — added **in the same change**, since v2
   progresses forward (rule 4: a new field + its new consumer "ship together as a **proposal**").
2. Registration in the **proposals registry** `labs/comlab/comlab/config/proposals/`
   (`entries.yaml` / `proposals.yaml`) — *never* silently in the live KG — plus its **task spec**.
3. Per the carry-over invariants: a **`# wiki:` citation** for any numeric literal/threshold and the
   field's source, and a scope-confirm naming field · guard · consumer · files before code.

If no consumer can be named at all, it is **deferred/PENDING** — not added. ("Not in v1" is *not* a
reason to defer; absence of any nameable consumer is.)

**Source/Method:** `AGENTS.md:24-30` (rule 4); existence of `labs/comlab/comlab/config/proposals/{entries,proposals}.yaml`
confirmed by grep; `CLAUDE.md`/AGENTS carry-over invariants.

---

## P5 — Applied sketch (NOT modified): reject unknown tag with a typed error

Current behaviour is **fail-open**: an unknown DNA gate logs a warning and returns `True`
(`routing_tag_mapper.py:131-133`, `_check_high_confidence_gate`). To reject an *unknown tag/gate*
with a typed error instead:

- **File + function to change:** `labs/dtclab/dtclab/core/routing_tag_mapper.py` —
  `RoutingTagMapper._check_high_confidence_gate` (and define a typed error, e.g.
  `class UnknownDnaGateError(ValueError)` near the top of the module). The `DTCRoutingTag(entry["tag"])`
  cast in `_load_map` (`:84`) already raises `ValueError` for an unknown *tag string*; the gap is the
  unknown *gate name*, which currently fails open.
- **Single test file:** `labs/dtclab/tests/unit/test_routing_tag_mapper.py`.

**Diff sketch (report only):**

```python
# routing_tag_mapper.py — module top
class UnknownDnaGateError(ValueError):
    """Raised when a routing rule names a DNA gate the mapper does not implement."""

# in _check_high_confidence_gate, replace the fail-open tail:
-        # Unknown gate — defensive: emit (fail open).
-        logger.warning("unknown_dna_gate: gate=%s", gate_name)
-        return True
+        # Unknown gate — fail closed with a typed error (was fail-open).
+        raise UnknownDnaGateError(
+            f"unknown DNA gate {gate_name!r} (wiki: DTC_VOCABULARY.md §4.1)"
+        )
```

```python
# test_routing_tag_mapper.py — new assertion
def test_unknown_dna_gate_raises():
    import pytest
    from dtclab.core.routing_tag_mapper import UnknownDnaGateError
    mapper = RoutingTagMapper(MAP_PATH, dna_view=_dna_view())  # HIGH confidence
    # inject a rule with a bogus gate, or point MAP_PATH at a fixture whose entry
    # has dna_gate: "nonexistent_gate"; then:
    with pytest.raises(UnknownDnaGateError):
        mapper.map(["P0XXX"])  # DTC matching the bogus-gated rule
```

**Caveat to weigh before applying:** the gate is only consulted on `VinConfidence.HIGH`
(`_gate_allows:118-120`); PARTIAL/NONE/None short-circuit before `_check_high_confidence_gate`, so
the typed error would only fire on HIGH-confidence sessions. The cleaner place to fail-fast on an
unknown gate is **construction time** in `_load_map` (validate `entry["dna_gate"]` against a known
set when the YAML is loaded), so a bad map is rejected regardless of confidence. I'd raise that as
the design question before coding.

**Source/Method:** `routing_tag_mapper.py:93-133` (gate branches + fail-open tail), `:80-86`
(`_load_map`), `tests/unit/test_routing_tag_mapper.py` structure; `dtclab/schemas/dna_view.py:97-98`
(`emissions`, `confidence`).
