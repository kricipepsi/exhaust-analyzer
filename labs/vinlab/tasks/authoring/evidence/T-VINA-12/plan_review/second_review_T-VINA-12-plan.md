I've completed a static review of the plan against R1–R4, the success criteria, and the embedded `rekey.py`/`join_check.py`/decoder snippets (no file access is available, so all counts below are re-derived from the embedded artifacts).

**Findings**

**R2 mechanism — biased vote (HIGH)**
- Plan: "vote over files 1+2 petrol VINs whose post-R1 brand folds to `fold(B_new)`"; "Most votes wins."
- The vote population merges W's own VINs with *other* WMIs of the new brand, so on any shared key the pre-existing brand's VINs outvote the very W VINs the re-key exists to fix. Concrete input from the plan's own log: key `(TOYOTA, BH31V)` — 12 W VINs (JTM/JTE) vote `1AZ`, 57 non-W Toyota VINs vote `1AZ-FE`; the rule keeps `1AZ-FE`, so the 12 W VINs now resolve `1AZ-FE` and mismatch their actual `1AZ`. Same pattern in `KIA_DA242` (`M3` 1 vs `B3` 63) and `JEEP_BU000` (6:36). This is the R2 "two-brands-share" vote implemented as a single-brand fold vote.
- Fix: count only W's own VINs on each key (the population the old rows were built from), or explicitly weight W so the re-keyed population decides the key's code; re-derive the W totals afterward.

**Tie rule (MEDIUM)**
- Plan: "Tie: the existing `B_new` row wins"; code `max(range(len(order)), key=lambda i: (vt[norm(...)], -i))` gives index 0 (existing) every tie.
- Concrete: `CHRYSLER_EMN6C` ends 1:1 and keeps `VN599960`; the 1C3 VIN's actual old code is dropped. The tie-break systematically resolves ambiguity against the WMIs the task is fixing.
- Fix: break ties to the old (W) code, or by the old row's `majority_share`, instead of unconditionally favoring the existing row.

**Key the rule misses / 1C4 loss under total-only floors (MEDIUM-HIGH, = A2)**
- Plan: "Their `LANCIA` rows have keys no files 1+2 `1C4` VIN has, so K does not hold them"; W match 1004 vs floor 1001.
- Re-derived per-W match deltas: JTE +2, 1C3 +2, VF8 +1, 1C4 −2 → net +3 (1001→1004). So the total floor hides a 2-match regression on `1C4` (`1C4GYN5B1YU528746`, `1C4GCB4L9YU518831`, registry `CHRYSLER` Voyagers). A per-WMI reading of the Goal ("loses no engine-code match, for these WMIs") fails on `1C4`; the plan passes only under R2's total-only floors.
- Fix: R2's totals are binding, so this is acceptable *only if Cowork explicitly signs off on the 1C4 per-WMI loss*; the only file-3-free recovery is the rejected "copy every old row" pollution. Record that acceptance.

**Wrongly deletes via folded key (MEDIUM, latent)**
- Code: `if x["vds_full"] and (_fold_brand(x["brand"]), x["vds_full"]) in delete: continue` deletes *every* row under the folded key, while the plan §2 says "delete the `B_new` row" (singular).
- Concrete: if a base key that is already duplicated under its fold (the plan's own asserts admit base duplicates) is one of the 17 old-win keys, both rows are dropped, making `deleted_rows` exceed 17 and `12,987` wrong — while the duplicate-subset assert still passes.
- Fix: delete only the exact row `row_a` returned (identity/primary key), or assert exactly one row per folded delete key.

**Wrongly copies stale `majority_share` (LOW)**
- Code: `add.append(dict(olds[0][1], brand=bn))` keeps the old row's share on the 59 copy keys.
- Concrete: a LANCIA row copied to JEEP keeps a share computed over LANCIA VINs, so `_resolve_engine` flags (or fails to flag) `vds_engine_ambiguous` wrongly on the new key. This never changes match totals (flag only).
- Fix: recompute share over the new-brand VINs for copied keys, or blank it.

**Held-out file 3 — no leak (LOW, verified)**
- Plan: "File 3 is read only by `join_check.py` (the prediction) and by `plan/diag.py` (a diagnosis after the rule was fixed, not a choice)."
- Verified: `rekey.py` opens only `Nio_vozila_{1,2}.csv`; K, the vote and the tie rule are fully determined by files 1+2 plus the base map. The `join_check.py` run on file 3 is the R2-mandated held-out prediction (and its "below floor = stop" is exactly what R2 requires). `plan/diag.py` is post-hoc diagnosis, not a choice.
- Fix: none required; keep the note's explicit statement that diag ran after the rule was frozen.

**Control set C — claim is correct (LOW, verified)**
- Plan: "C decodes to these brands, and the folds of the new and the old brands are disjoint, so C cannot change."
- Verified: R1 touches only the 10 P1 rows plus LSJ; `rekey.py` adds/deletes/changes-share only on new-brand keys; old-brand rows are never edited or deleted; the folds (SUBARU/TOYOTA, LEXUS/TOYOTA, HYUNDAI/KIA, RAM/JEEP, LANCIA/JEEP, LANCIA/CHRYSLER, INFINITI/NISSAN, MATRA/RENAULT) are pairwise disjoint; and `join_check.py` freezes C from `wmi_base.csv`. C is byte-identical to base (4388/5071).

**R3 tool and tests (MEDIUM + LOW)**
- Untested chain (MEDIUM): `build(...) -> int: passes it through` and the `--registry-csv` wiring are not exercised by any of the 7 tests. A mutant that makes `build()` drop `registry_make` passes all 7 tests (none call `build`); only `_pick_vpic_make`/`_load_vpic_wmis`/`_registry_majority` are covered. Fix: add one in-memory test that calls `build(...)` with a `registry_make` and asserts the emitted wmi.csv brand.
- No-vPIC divergence (MEDIUM-LOW): P6 shows `KNE`, `VF8`, `LSJ` have no vPIC make (and `1C4`/`3C4` are unlisted), so `_load_vpic_wmis` never reaches `_pick_vpic_make` for them; re-running the fixed tool still cannot produce `KNE→KIA`. R3 is scoped to "several vPIC makes", so this is compliant, but the plan should state which WMIs R3 actually corrects.
- Empty-makes edge (LOW): `_pick_vpic_make([], "KIA")` raises `IndexError` at `makes[-1]`; unreachable via `_load_vpic_wmis` today, but the `Sequence[str]` contract doesn't exclude empty. Fix: `if not makes: return ""` (plus a test).
- Weak `_registry_majority` test (LOW): the temp CSV is ASCII-only, so the cp1250 decode path it will use on real Nio files is never exercised; a wrong-encoding mutant passes.

**R4 coverage (MEDIUM-LOW)**
- Plan: "M1-M4: revert the `JTM`, `JTE`, `KNE`, `VF8` brand cell"; §5: "`grep` ... hits only `test_wmi_brands.py`."
- Concrete: reverting any of the other six renames (`5TD`, `ZAC`, `1C4`, `3C4`, `1C3`, `3N1`) fails no unit test, and the total-based `join_check` slack (+3 match) can absorb a single-row revert (e.g., `1C3→LANCIA` drops W match to 1002 ≥ 1001). Those six rows are guarded only indirectly.
- Fix: this matches R4's literal scope (4 probe rows), but the plan should record that the other six renames have no dedicated test/mutant.

**Assumptions and wording (LOW)**
- A1: transparent guard workaround; fine.
- A2: "loses 2 matches ... and gains 7 elsewhere" mixes units — the +7 is engine (+2 JTE, +4 1C3, +1 VF8), while match gains are +5. Wording only.
- A3: reasonable; keep-last on an unmatched majority matches R3's "keeps the current choice."
- Encoding inconsistency (LOW): `rekey.py` reads Nio files 1+2 with `encoding="latin-1"` while the registry is pinned cp1250 and `join_check.py` uses cp1250; a cp1250-only byte in `P15` normalizes differently. The `"\ufffd" in c` quarantine check is dead under latin-1. Fix: read with cp1250.
- Pos-8 justification incomplete (LOW-MEDIUM): "No P1 or old brand has a `pos_8_only` row, so only Path A matters" does not rule out W VINs resolving via Path B through rows that carry both `vds_full` and `pos_8`; the plan should verify (files 1+2) that no W VIN resolves via the pos-8 index.

**Verdict**
The plan is structurally sound: R1 is exact, the rule is file-3-free, C genuinely cannot change, and the predicted totals clear every R2 floor (W eng +1, W match +3, C exact). The blocking issues are the biased vote/tie rule, the latent over-deletion, the untested `build()` parameter chain, and the unguarded 1C4 per-WMI loss and six untested renames — all correctable without a redesign.

APPROVE WITH CORRECTIONS