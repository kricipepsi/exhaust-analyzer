# audit — Progress Ledger (app-scoped fix rows from `audit/FIX_PLAN.md`)

**Tasks dir:** `apps/wired/audit_tasks/` · **Mode:** STRICT · **ID prefix:** `T-AUD-` (ceiling 99)
**Scope:** the app-scoped rows of the 2026-10-17 audit (T-AUD-1a, T-AUD-1b, later T-AUD-10). Lab-scoped rows
(T-AUD-2, 3, 5, 8, 9) get packs in their lab's own `tasks/`. Source of every row: `audit/FIX_PLAN.md`.
**Branch rule:** one `fix/<ID>` branch per row, cut from `audit-r2`; never `main` (`main` redeploys Render).
**Last updated:** 2026-11-02 (Windows Cowork: rewritten to the loop column contract; T-AUD-1a re-authored).

Gate blocks go in `progress_notes/<ID>.md`. Cells stay under 120 characters and never contain `|`.

## Task log

| ID | Task file | Status | Blocked by | Date | Score | Note |
|---|---|---|---|---|---|---|
| T-AUD-1a | `repo/apps/wired/audit_tasks/T-AUD-1a_app_usable(4).md` | done | — | 2026-11-02 | 4/5 | **ACCEPT 2026-11-02, score 94, t=50/1 — `repo/apps/wired/audit_tasks/reviews/REVIEW_T-AUD-1a.md`.** P0 app usable; plan REQUIRED; 2 commits (Cowork 006/008) |
| T-AUD-1b | `repo/apps/wired/audit_tasks/T-AUD-1b_deploy_manifests(3).md` | done | T-AUD-1c | 2026-11-03 | 3/5 | **ACCEPT 2026-11-03, score 92, t=12/1 — `repo/apps/wired/audit_tasks/reviews/REVIEW_T-AUD-1b.md`.** deploy manifests F-P5-1/2/4: fourdapp-* dist names, dnalab deps, constraints.txt |
| T-AUD-1d | (not authored: fold into T-AUD-4b) | deferred | T-AUD-4b | 2026-11-03 | — | B1 f2: C4 probe test_f3b asserts nothing on the verdict; add an override-reaches-OBDLab assertion with F-C4-3 (018 ruling 3) |
| T-AUD-4a | `repo/apps/wired/audit_tasks/T-AUD-4a_o2_downstream_pid(2).md` | pending | — | 2026-11-05 | 2/5 | F-C4-4 = F-C1-17: registry o2_downstream reads the measured downstream_o2_v, not the upstream B1S1 FF voltage |
| T-AUD-4b | (not authored) | deferred | T-AUD-4a | 2026-11-05 | — | F-C4-3, F-C4-7, T-AUD-1d: O2 override reaches the labs; SUPERCHARGED/NONE vocabulary in the OBDLab projection (composition.py) |
| T-AUD-4c | (not authored) | deferred | T-AUD-4b | 2026-11-05 | — | F-C3-3 then F-C3-1, F-C4-2: drive-cycle default, cold-engine made-up lambda, trims-blocked gate consumed by COMLab |
| T-AUD-4d | (not authored) | deferred | T-AUD-4c | 2026-11-05 | — | F-C3-2, F-D2-10, F-D2-11: DTCLab gets its DNA view; COMLab projector output accepted by DTCLab |
| T-AUD-4e | (not authored) | deferred | T-AUD-4d | 2026-11-05 | — | F-D2-2, F-D2-9, F-C4-5/6/8/10, F-C5-3..5/9..11: inbound contract, won_not_start, dropped fields census; gas_lab_output residual |
| T-AUD-1c | `repo/apps/wired/audit_tasks/T-AUD-1c_ff_and_gas_prompts(2).md` | done | T-AUD-1a | 2026-11-03 | 2/5 | **ACCEPT 2026-11-03, score 97, t=6/1 — `repo/apps/wired/audit_tasks/reviews/REVIEW_T-AUD-1c.md`.** 018 S1+N1 (was T-AUD-1a-c): FF required whenever a DTC dict is sent; gas message names GASLab |
| T-AUD-7a | `repo/apps/wired/audit_tasks/T-AUD-7a_git_rule_main_production(1).md` | done | T-AUD-1b | 2026-11-03 | 1/5 | **ACCEPT 2026-11-03, score 100, t=2/1 — `repo/apps/wired/audit_tasks/reviews/REVIEW_T-AUD-7a.md`.** F-D3-1: git rule says work on main; main is production (4DLab_CLAUDE.md §Git, v3/CLAUDE.md) |
| T-AUD-7b | `repo/apps/wired/audit_tasks/T-AUD-7b_git_rule_stale_docs(1).md` | done | T-AUD-7a | 2026-11-04 | 1/5 | **ACCEPT 2026-11-04, score 98, t=1/1 — `repo/apps/wired/audit_tasks/reviews/REVIEW_T-AUD-7b.md`.** F-R3-5: 5 docs still say the only git action is the owner's commit / never branch; point at §Git |
| T-AUD-7c | `repo/apps/wired/audit_tasks/T-AUD-7c_stale_pending_ledger_rows(1).md` | done | T-AUD-7b | 2026-11-04 | 1/5 | **ACCEPT 2026-11-04, score 97, t=3/1 — `repo/apps/wired/audit_tasks/reviews/REVIEW_T-AUD-7c.md`.** F-D3-2, F-D3-3: COMLab, registry and vault-live ledgers offer finished tasks as pending |
| T-AUD-7d | `repo/apps/wired/audit_tasks/T-AUD-7d_assignment_precedence_and_pct_ledger(1).md` | done | T-AUD-7c | 2026-11-05 | 1/5 | **ACCEPT 2026-11-04, score 96, t=3/1 — `repo/apps/wired/audit_tasks/reviews/REVIEW_T-AUD-7d.md`.** F-D3-4/6/9: ledger wins over assignment; ROADMAP consumer rule; PCT-2..10 deferred |
| T-AUD-7e | `repo/apps/wired/audit_tasks/T-AUD-7e_infra_pointer_and_firecrawl_auth(1).md` | done | T-AUD-7d | 2026-11-05 | 1/5 | **ACCEPT 2026-11-04, score 97, t=2/1 — `repo/apps/wired/audit_tasks/reviews/REVIEW_T-AUD-7e.md`.** F-D3-7/8: boot docs point at 4DLab_CLAUDE.md, no sandbox ritual; python3.14; firecrawl key not in repo |
| T-AUD-7f | `repo/apps/wired/audit_tasks/T-AUD-7f_graph_build_lane_rule(1).md` | done | T-AUD-7e | 2026-11-05 | 1/5 | **ACCEPT 2026-11-04, score 96, t=1/1 — `repo/apps/wired/audit_tasks/reviews/REVIEW_T-AUD-7f.md`.** F-D3-5: one graph-build lane rule (architect; T-GR-10/11 Nemo extract); harness git line |
| T-AUD-7g | `repo/apps/wired/audit_tasks/T-AUD-7g_router_status_and_canonical_wiki(1).md` | done | T-AUD-7f | 2026-11-05 | 1/5 | **ACCEPT 2026-11-04, score 97, t=2/1 — `repo/apps/wired/audit_tasks/reviews/REVIEW_T-AUD-7g.md`.** F-D3-13/17: router and ROADMAP report ledger states; six-identity roster; canonical wiki labs/<lab>/wiki |
| T-AUD-7h | `repo/apps/wired/audit_tasks/T-AUD-7h_import_edge_and_vault_bootstrap(1).md` | done | T-AUD-7g | 2026-11-05 | 1/5 | **ACCEPT 2026-11-05, score 97, t=2/1 — `repo/apps/wired/audit_tasks/reviews/REVIEW_T-AUD-7h.md`.** R0-3, F-D3-18: rule 5 names the ADR-0002 import edge; Vault packs leave the bootstrap table |
| T-AUD-7i | `repo/apps/wired/audit_tasks/T-AUD-7i_roadmap_and_dnalab_paths(1).md` | done | T-AUD-7h | 2026-11-05 | 1/5 | **ACCEPT 2026-11-05, score 97, t=2/1 — `repo/apps/wired/audit_tasks/reviews/REVIEW_T-AUD-7i.md`.** F-D3-19 boot docs: ROADMAP and dnalab START_HERE name paths that resolve |

**Status values:** `pending` · `in_progress` · `done` · `blocked` · `deferred` · `superseded`
**Score** (column 6, checked by `ops/gen_dispatch.py`): the routing score `N/5`, the same `N` as the file name's `(N)`.
**Runnability:** `pending` = runnable now (the spec exists and every Blocked-by is `done`); otherwise `deferred`.
