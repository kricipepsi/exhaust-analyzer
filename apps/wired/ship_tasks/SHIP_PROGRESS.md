# ship — Progress Ledger (pre-publish blockers + hygiene)
**Pack goal:** clear the four ship blockers from `planning/SHIP_AUDIT_2026-07-07.md`
(full-suite re-verify, synthetic-vs-real scoreboard split, VIN blank-brand recovery,
end-user UI) plus ledger hygiene. Engine accuracy work is CLOSED (owner stop ruling
2026-07-06) — no task in this pack tunes, tightens, or chases score.
**Tasks dir:** `apps/wired/ship_tasks/` · **Mode:** STRICT (dual-gate)
**Last updated:** 2026-07-09 (coder Agy — T-SHIP-8 done; README status lines synchronized).

Keep under ~120 lines; gate blocks go in `ship_tasks/progress_notes/<id>.md`.

---

## Task log
| ID | Task file | Status | Blocked by | Date | Commit | Verification | Notes |
|---|---|---|---|---|---|---|---|
| T-SHIP-1 | `T-SHIP-1_full_verification_sweep.md` | **done** | — | 2026-07-07 | (T-SHIP-5) | suites+guards green (2 findings reconciled); hash lock ok 269/294; synthetic map 191+78; CS-002 hard-absence OK | READ-ONLY disclose done — `reports/SHIP_VERIFY_2026-07-07.md`; F-1 stale dial tests fixed, F-2 4B knife-edge re-pinned (BL-8). |
| T-SHIP-2 | `T-SHIP-2_scoreboard_synthetic_split.md` | **done** | T-SHIP-1 (**done**) | 2026-07-07 | (T-SHIP-5) | ruff clean; topk-scorer 4 passed; split renders 191/294 real + 78 synthetic; hash lock ok | COMMIT done — split live in `score_v3_yardstick.py` (canon Provisional-synthetic #3). |
| T-SHIP-3 | `T-SHIP-3_vin_blank_brand_recovery.md` | **done** | — | 2026-07-07 | (T-SHIP-5) | vinlab 203 passed; TMB sample conf>NONE 198/200 (was 0); idempotent; no mojibake remains | Audit figure was stale (blank=0.00%); real defect = corrupt brand spellings — repaired via `tools/repair_brand_spellings.py`. Report `labs/vinlab/VIN_BRAND_RECOVERY_2026-07-07.md`. |
| T-SHIP-4 | `T-SHIP-4_ledger_hygiene_disposition.md` | **done** | — | 2026-07-07 | (T-SHIP-5) | doc==code enum set-compare equal; drift guard 27 passed; zero rows deleted | Harness pack dispositioned (11 rows); T-RMW-MIRROR void; gaslab header de-staled; FU-2 closed; `POST_LAUNCH_BACKLOG.md` BL-1..13. |
| T-SHIP-UI-1 | `T-SHIP-UI-1_ui_build_contract.md` | **done** | — | 2026-07-07 | (T-SHIP-5) | contract on disk; 36 NEW columns enumerated w/ producer states; forks F-1..F-3 recommended | `reports/SHIP_UI_CONTRACT_2026-07-07.md`. |
| T-SHIP-UI-2 | `T-SHIP-UI-2_build_streamlit_ui.md` | **done** | T-SHIP-UI-1 | 2026-07-08 | `8e0d08b` | pytest 5 passed; ruff clean; MW-002 returns MW-002; abstain ok | Built single-file Streamlit app in apps/ui/app.py per contract. |
| T-SHIP-5 | `T-SHIP-5_owner_commit_delegated.md` | **done** | T-SHIP-1 (**done**) | 2026-07-07 | G1-G9 (`reports/SHIP_COMMIT_2026-07-07.md`) | tree clean (`git status --porcelain` empty); secrets gate clean per commit; no add -A / branch / push | One-shot owner delegation executed. Branch is `task/t-com-vault` — mainline merge stays with the owner. |
| T-SHIP-UI-3 | `T-SHIP-UI-3_per_field_help_tooltips.md` | **done** | T-SHIP-UI-2 (**done**) | 2026-07-08 | | pytest 8 passed; ruff/pyright clean; tooltips format ok | FIELD_HELP in ui_payload.py drives app.py tooltips & limits. |
| T-SHIP-6 | `T-SHIP-6_final_full_suite_pre_push.md` | **done** | — | 2026-07-08 | `72eedc6`+`322642b` (coder-run — see D-SHIP-4) | full suites green; guards green; UI smoke green; score lock 269/294 + split 191/78; dirty-tree F-1 disclosed | Final READ-ONLY full-app sweep report `reports/SHIP_FINAL_VERIFY_2026-07-08.md`; AUDIT 2026-07-08: results accepted; counts reconcile; coder committed WITHOUT authorization → D-SHIP-4 ratify-or-reset. |
 | T-SHIP-7 | `T-SHIP-7_lab_doc_drift_audit.md` | **done** | — | 2026-07-08 | `436E` | audit report `DOC_DRIFT_2026-07-08.md` authored | READ-ONLY disclosure done; A drifts classified; T-SHIP-8 unblocked.
| T-SHIP-8 | `T-SHIP-8_lab_doc_sync.md` | **done** | T-SHIP-7 (**done**) | 2026-07-09 | `f87f875` | README status fields synced; suites green; score lock ok | COMMIT half: applied A fix list verbatim; no coder git commit. |

**Status values:** `pending` · `in_progress` · `done` · `blocked` · `deferred` · `void`
**Runnability:** `pending` = runnable now. Forward-registered rows stay `deferred`, never
`pending`. Guard takes the first `pending` row top-to-bottom whose Blocked-by are all `done`.
T-SHIP-1, T-SHIP-3, T-SHIP-4, T-SHIP-UI-1 are independent — parallel-safe across coders
(disjoint write scopes; UI-1 and SHIP-1 are read-only).

## Owner decision rows (not coder-runnable)
| ID | Decision needed | Unblocks |
|---|---|---|
| D-SHIP-1 | Rings/PCV domain ruling: does worn-ring HC **rise or drop** idle→2500? (`apps/wired/wiring_prep_tasks/RINGS_PCV_TRIAGE_RULING.md`) | T-XLAB-RINGS-RECONCILE-1 · T-XLAB-PCV-VERIFY-1 (gaslab ledger) — else MW-001→CF-001 and MW-008→SF-001 ship as known-wrong routes |
| D-SHIP-2 | Q-C5-EGR wiki-vs-cluster5 conflict: authenticated firecrawl verification pass, then edit the losing document (DECISIONS 2026-07-06 HOLD) | EGR rows stay honestly abstained meanwhile — not score-blocking |
| D-SHIP-3 | ~~Owner-run commit~~ **Delegated to `T-SHIP-5`** (owner ruling 2026-07-07). Remaining owner call: waive or keep the T-SHIP-1 blocker. | A published build from a committed tree |
| D-SHIP-4 | **RESOLVED 2026-07-19 — ratified as-is** (owner delegated the call to architect recommendation; audit had already accepted the sweep results, so a soft-reset would change authorship only, not content). Commits `72eedc6`+`322642b` stand; F-1 + `pyrightconfig.json` ratified with them. | ~~The GitHub push~~ unblocked |

## Unplanned follow-ups
| ID | Discovered in | One-liner | Status |
|---|---|---|---|
| — | — | — | — |

## Change log
| Date | Patch |
|---|---|
| 2026-07-07 | Pack authored from `planning/SHIP_AUDIT_2026-07-07.md` (architect, Cowork). |
| 2026-07-08 | T-SHIP-6 audited (architect): sweep accepted; V-1 unauthorized coder commits → D-SHIP-4. |
| 2026-07-19 | D-SHIP-4 resolved (ratify, owner-delegated). Deploy files authored at root (`render.yaml`, `requirements.txt`, `app.py` shim, `.python-version`) for the Render cutover; `.gitignore` gains `Vault/githubtoken.md`, `.backups/`, `.skylos/`. |
