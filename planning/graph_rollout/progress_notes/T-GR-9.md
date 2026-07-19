# T-GR-9 — progress note (staleness refresh post-C5B)
**Lane:** ARCHITECT. **Date:** 2026-07-06 · **Executor:** Architect (Cowork) · **Owner go:** given
in-session 2026-07-06 ("ok go then").

## Changed-labs scan (--since=2026-06-26, code paths) — findings FIRST, per task rule
| corpus | changed? | evidence | action |
|---|---|---|---|
| comlab/comlab + tests | YES (22 + 14 py) | C2B/C3B/C5B + GTA-RECONCILE commits | rebuild (named list) |
| comlab/registry (code+tests) | YES | shim ×3 (C2B/C3B/C5B), tools, schema_v2 | rebuild (scan clause) — **this is where the probe states live** |
| obdlab/tests | YES (1 py) | 2cea8d2 (06-28 23:22) edited test_dna_view.py AFTER the 06-26 23:58 v2_tests build | rebuild v2_tests only |
| vinlab | no (post-build) | c5034a3 (06-26 22:26) predates 23:58 build; `git diff c5034a3..HEAD` empty | skip |
| dtclab / dnalab / gaslab / symptomlab | no code changes | scan | skip |

## DEVIATION 1 — probe target (task criterion 2)
`LeanRootCauseState` / `SensorDynamicsState` live in `labs/comlab/registry/integration_shim.py`,
which was **never part of the comlab `v2_current` corpus** (06-06 compose: comlab/ + tests/ + docs/
+ wiki/ + README). The criterion-2 probe as written can never pass against `v2_current`. The task's
Goal ("agent queries stop missing recent symbols") is met in the graph that indexes the shim:
`labs/comlab/registry/graph/v2_code/`. Registry tiers rebuilt under the scan clause; probes PASS
there (below). Corpus separation (registry has its own graph tree, T-RVAULT design) kept intact.

## DEVIATION 2 — build tool: graphifyy 0.8.36 (throwaway venv), NOT 0.9.7
**New finding: graphifyy 0.9.7 extracts ZERO nodes from JSON files** (upstream #1666; reproduced
standalone: 2 kg JSONs → 0 nodes; persists across re-run). A 0.9.7 rebuild would have silently
deleted the JSON node layer: comlab v2_code −1140 config nodes (71% of graph), registry v2_code
−64 rules nodes, fixtures/pid_logset losses in tests tiers. T-GR-2's smoke corpus was pure .py, so
this never surfaced. Resolution: built with the **T-GR-2 rollback pin `graphifyy==0.8.36`** in a
throwaway venv (`/tmp/t9/venv`); **`.venv-wired` remains 0.9.7 untouched** (query CLI; T-GR-2
proved 0.9.7 reads old-format graphs). Skill metadata updated with the caveat.
**Consequence for the pack: do NOT rebuild any JSON-bearing corpus with 0.9.7 until upstream fixes
#1666.** Check release notes before the next graphifyy upgrade task.

## Rebuilds — pre/post (all `graphify update`, scoped /tmp staging, offline, no key)
| tier | pre n/l | post n/l | dangling | delta explained |
|---|---|---|---|---|
| comlab v2_code | 1606/3074 | 1611/3107 | 0 | +5n: C-pack code in config/schemas/core |
| comlab v2_tests | 1643/2321 | 1713/2419 | 0 | +70n: C-pack tests |
| comlab v2_current | 3090/4139 | 3972/7911 | 0 | fresh compose (see below): docs corpus grew 363→487n; wiki 570→160n (T-COM-WIKIPREP condensed to 15 files); kg config 1035→1080n; edge growth = 0.8.36 richer structural inference on current corpus |
| registry v2_code | 206/363 | 220/419 | 0 | +14n: shim states + tools; 16 rules JSONs present |
| registry v2_tests | 824/1258 | 824/1258 | 0 | counts equal; hash differs (line refs/communities); py unchanged since 06-28 build |
| obdlab v2_tests | 878/1196 | 878/1196 | 0 | test_dna_view.py edit was 18ins/14del — node-count neutral, content refreshed |

**v2_current compose:** first attempt = documented incremental `graphify update` over staged old
graph+cache → REJECTED: 165 stale `C:\`-path nodes + old/new node-ID-scheme duplicates carried over.
Old graph's GRAPH_REPORT shows token cost 0/0 → its 906 INFERRED edges were offline inferences, not
LLM work → nothing to preserve → rebuilt FRESH over the composed corpus (comlab/ + tests/ + docs/ +
wiki/ + README.md). Result: unique IDs, no `C:` junk.

## Post-probes (0.9.7 CLI, the sanctioned reader)
- `explain LeanRootCauseState --graph labs/comlab/registry/graph/v2_code/graph.json` →
  `integration_shim.py L178` PASS
- `explain SensorDynamicsState` (same graph) → `integration_shim.py L170` PASS
- (v2_current probe: N/A per Deviation 1 — shim not in corpus, pre-run probe also absent)

## Collateral
- sha256 of ALL 41 lab graph.json pre vs post: **exactly the 6 named tiers differ, nothing else**
  (pre/post lists archived in note-adjacent shell transcript; pre file /tmp/t9/pre_sha.txt).
- Task grep-gate flagged pre-existing working-tree items (registry ingest_ready `M` mtime 06-29;
  untracked v2_docs outputs of T-GR-3..7 awaiting owner commit) — NOT touched by this task.
- No root `graphify-out/`; scratch confined to /tmp/t9 (removed post-task); `Vault/` untouched.

## VERIFICATION GATE — T-GR-9
1. Pre/post counts + deltas : PASS (table above, all explained; no --force needed anywhere)
2. Post-probe states        : PASS (registry v2_code, file+line; Deviation 1 documented)
3. Audit + ledger updated   : PASS (GRAPH_AUDIT_2026-06-28.md rows; ledger T-GR-9 → done)
4. Unlisted graphs identical: PASS (sha256 41-file sweep; only 6 named tiers differ)
Result: **CLEAN** (with 2 documented deviations)

## CODE REVIEW — T-GR-9
Scope: PASS (6 named/scan-authorized tiers + pack bookkeeping + skill-metadata caveat; no source,
no Vault, no other graphs). Composition: PASS (registry rebuild authorized by the task's changed-scan
clause; 0.8.36 via throwaway venv leaves T-GR-2's 0.9.7 install intact). Result: **CLEAN**
