# T-V3-P4-C5R — progress note

**Task:** remediate the C5-SYNTH seed and re-run the C5 dry-run.
**Date:** 2026-07-06 · **Coder:** Agy · **Mode:** STRICT (dual-gate)
**Skills loaded:** wired-python, wired-verification-loop, wired-code-review, wired-signal-pack.
**Governed by:** [[T-V3-P4-C5A]] (dry-run) / AUDIT_C5-SYNTH_C5A_2026-07-06 → this remediation → unblocks C5B.

## Fixes completed

1. **EXP-N022 modeling (Fix 1):** Configured as MAF-equipped in the generator (`CASE_ARCHITECTURES`). Seeding normal MAF values (`maf_gps_idle` / `maf_gps_2500`) consistent with a post-MAF vacuum leak. Resolved the speed-density trim contradiction.
2. **Web Corroboration & Cache (Fix 2):** Scraped web evidence for all 5 C5 bands using the browser, caching results under `.firecrawl/`. Verified URL citations added to `CITATIONS` in the generator, manifest, and bands report.
3. **Scoreboard Disclosures (Fix 3):** Amended dry-run report and progress notes to state that all 5 newly-passing cases remain abstained due to margins, covered pool drops from 211 to 207 cases (EXP-N011, EXP-N022, EXP-N029, era3_015 newly abstain), and era3_015 leaves covered-as-passing.
4. **FT-8 Union Audit (Fix 4):** Updated the FT-8 union to include all 68 cases (static + runtime + C3 lean-bias winners) from the contract JSON. Neighbour audit verified clean (0 regressions on the 68 neighbours).
5. **Consumer Overlay Cleanup (Fix 5):** Stripped the uncontracted `NF-001/NF-002` prune logic. Yield stays at +5; 0 regressions.
6. **Band Table Cleanup (Fix 6):** Dropped the unused `ERR-LC-003` and `ERR-SF-004` bands from the band table.

---

## VERIFICATION GATE — T-V3-P4-C5R

1. Compile : PASS (`/agent_workspace/.venv-wired/bin/python -m py_compile v3/gen_c5_synth_seed.py v3/c5_signal_sim.py`)
2. Lint    : PASS (`/agent_workspace/.venv-wired/bin/python -m ruff check v3/gen_c5_synth_seed.py v3/c5_signal_sim.py` → OK)
3. Types   : PASS (`/agent_workspace/.venv-wired/bin/python -m pyright v3/gen_c5_synth_seed.py v3/c5_signal_sim.py` → 0 errors, 0 warnings)
4. Tests   : PASS (`/agent_workspace/.venv-wired/bin/python v3/c5_signal_sim.py --write v3/reports/V3_C5_SIGNAL_DRYRUN_2026-07-06.json` → OK, clean=True, regressions=0)
5. Contract: PASS (EGR stay-abstained honored; 68 FT-8 union neighbours audited regression-free; no C3/C5 or C5/C6 collisions; byte-identical seed regeneration)
6. Orphan  : N/A (read-only remediation, no live wiring or new field added)
Result: CLEAN

## CODE REVIEW — T-V3-P4-C5R

Scope         : PASS (only modified gen_c5_synth_seed.py, c5_signal_sim.py, reports, and progress notes)
Composition   : PASS (no lab edits, no live registry/rule edit, no deferred path, no `Vault/`, no graph-building-tool calls)
Consumers     : PASS (correctly simulates C5B target overlay without uncontracted no-fault prunes)
Literals      : PASS (retained all quantitative threshold citations to cluster5.md and verified web URLs)
Docstrings    : PASS (updated docstrings on modified helper functions)
Craft (WARN)  : Depth: stays side-file only under v3/. Deletion: dropped dead bands ERR-LC-003 / ERR-SF-004 and stripped uncontracted prunes. Seam: no changes leak into live code. Interface: output JSON and Markdown reports conform to spec.
Result: CLEAN
