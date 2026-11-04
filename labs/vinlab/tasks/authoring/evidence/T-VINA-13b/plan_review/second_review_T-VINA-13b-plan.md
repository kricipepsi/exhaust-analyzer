## T-VINA-13b Plan Review

**Finding 1 — Ruling not implemented: the builder's nullable schema change is incomplete (MEDIUM)**
- Quote: “The builder's migration guard (`build_vref_db.py:993-998`, `ALTER … NOT NULL DEFAULT 0`) is outside `CREATE_ENGINE_REF` and stays (it fires only on a db without the columns): a follow-up, not this row's.”
- R3 says the plan “makes `tools/build_vref_db.py`'s `CREATE_ENGINE_REF` match it.” The plan edits only `CREATE_ENGINE_REF` (lines 103-104) and leaves the migration guard in the same file adding `has_maf`/`has_map` as `INTEGER NOT NULL DEFAULT 0`. Any later builder run on a legacy db re-introduces the exact invented-`0` default R3 is removing.
- Fix: change the migration guard to add the two columns as plain `INTEGER` so a migrated db matches `CREATE_ENGINE_REF`; if deferred, make it a named required follow-up with a test, not “a follow-up, not this row's.”

**Finding 2 — Merged value changes a decode with no TecDoc fact: air metering (HIGH)**
- Quote: “air metering (`has_map_sensor`, load calc, strategy) MAF_ONLY → HYBRID_MAF_MAP | 32 | the decoder's own heuristic (`decoder.py:490-501`, `has_map` NULL) on TecDoc-stated turbo/supercharged induction or GDI” and “The air-metering line is the judgement call for R4: the value is not a TecDoc field.”
- R4: “Any real-VIN change in … air metering that does not come from a stated TecDoc value is a stop.” TecDoc has no MAF/MAP field, so `has_map_sensor=True` on 32 real VINs is derived, not stated. The plan asks Cowork to waive the stop rather than implementing a rule.
- Concrete: any of those 32 VINs whose no-row decode was MAF_ONLY (has_map False) flips to HYBRID_MAF_MAP once a turbo/supercharged or GDI row is applied via `decoder.py:490-501`.
- Fix: skip codes whose TecDoc induction is TURBOCHARGED/SUPERCHARGED or fuel is GDI when the no-row decode yields has_map False, or obtain an explicit amended R4 ruling before the build. The plan cannot self-approve the waiver.

**Finding 3 — Window rule flaw: union over disjoint brand spans (MEDIUM)**
- Quote: “The window is the union over the brands (rejected: skip the 87 codes whose years differ, 89 real VINs).” with `my_start` = min and `my_end` = max end + 1.
- `min`/`max+1` assumes the per-brand year spans overlap or are contiguous. For the 87 year-differing codes, disjoint spans (brand A 1995–1998, brand B 2005–2009) give `[1995, 2010]`, wrongly accepting model years 1999–2004. The plan's false-pass note names only “rare imports,” not this gap. Because lookup is code-only, one row cannot hold two disjoint windows.
- Concrete: a code produced 1995–1998 and 2005–2009; a model-year-2002 VIN on it becomes `row_applied` though TecDoc lists no engine for that era.
- Fix: compute per-brand windows and skip any code whose spans have a gap > 1 model year, or justify the contiguous hull; measure how many of the 87 codes are disjoint. Also note open→2019 caps model years at 2020, so a 2021+ VIN on an open-ended engine is a latent false fail.

**Finding 4 — Schema rebuild risk: column reorder vs positional readers (MEDIUM)**
- Quote: “Afterwards the shipped table equals the builder's, including the column order: `rated_rpm` moves from last to after `valvetrain_type`. Every reader uses column names (`sqlite3.Row` dicts in `tecdoc_query.py:66,81`; named selects in the tests and probes).”
- The “every reader” claim is evidenced only for `tecdoc_query` and tests/probes. `tools/build_vref_db.py` itself (`INSERT_ROW`, `_enrich_from_csv`) and any `SELECT * FROM engine_ref` plus positional `row[n]` access are not enumerated; moving `rated_rpm` silently breaks such readers. The plan rejected preserving shipped column order, which would have zero risk.
- Fix: keep the shipped column order (edit only the two `NOT NULL` lines), or add a repo-wide grep for `SELECT * FROM engine_ref`/`PRAGMA table_info`/positional indexing plus a positional-read smoke test before reordering.

**Finding 5 — Guard incomplete: G1/G2 miss a banks hazard class (MEDIUM)**
- Quote: “G1: skip a code when any map row of it has `engine_configuration` starting `BOXER`.” and G2(iii): “TecDoc `is_v_engine` is `0`, `h1.config` starts with V, W or BOXER, the map configuration is blank, and `h0` is not a two-bank hint.”
- `decoder.py:364` runs `banks = 2 if db_dict.get("is_v_engine") else 1` for every inserted row. For the 15 extract rows with blank `is_v_engine`, the merge writes `0` and overwrites a V/W map's 2 banks to 1 with no TecDoc fact. G1 guards only BOXER and G2(iii) only the cylinder-fallback path with a blank map config, so blank-`is_v_engine` + V/W map is unguarded.
- Concrete: a code among the 15 blank-`is_v_engine` rows whose `vds_engine_map.csv` row is `V6`/`V8`; a real VIN on it goes banks 2→1 while TecDoc never stated “not V” (the attribution table would mislabel it “stated”).
- Fix: extend G1 to skip when the row's `is_v_engine` is blank/0 and any map config is V/W/BOXER; and drop G2(iii)'s “map configuration is blank” qualifier, since `decoder.py:474-477` also fires for straight-configured map rows.

**Finding 6 — Mutant that cannot fail: M9 vs test 9 (LOW)**
- Quote: “M9 `era_bucket` written as `ERA_MODERN` → 9.” Test 9: “equals `build_vref_db._derive_era(my_start, my_end)`.” Plus: “67 inserted rows end before 1990, and `_derive_era` gives them `ERA_MODERN` (its fall-through, `build_vref_db.py:61-65`).”
- Test 9 only checks the tool value equals `_derive_era`. If the fixture window's `_derive_era` is ERA_MODERN (the fall-through), M9 is behaviorally identical and test 9 still passes, so criterion 1 (“each R5 mutant fails a named test”) is unmet.
- Fix: pin test 9's fixture to a window where `_derive_era` returns a known non-MODERN bucket and assert that exact bucket, so M9 must fail; otherwise replace M9 with a divergent mutant.

APPROVE WITH CORRECTIONS