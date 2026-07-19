# EVAL-VLIVE-1 — Run protocol & comparison sheet
One probe task, run identically on two models, graded against the hidden key.

## What this measures (read first — honest scope)
The probe is **instruction-neutral**: it lists the vault graph (`vault_query`, the
`.base` views, the framed frontmatter) **and** raw code as equally available, and
never tells the agent which to use. So a single run captures **model skill ×
graph-utilization**, not the pack effect in isolation.

- **Agy vs Codex (what you asked):** same task, two models. Tells you which agent
  is more accurate/complete/efficient on this codebase **and** which one actually
  reaches for the graph (the Source/Method log + the utilization note show it).
- **To isolate the pack itself (optional control):** run the *same* model **twice**
  — once as written, once "graph-denied" (prepend: *"You may not run vault_query,
  open any `.base` view, or read note frontmatter — use code only."*). The delta
  between those two runs is the pack's lift, with model held constant. Do this for
  one model if you want a clean "does the pack help" number.

## Steps
1. In omp, set the model to **Agy**. Start a **fresh** coder session.
2. Paste the entire `EVAL-VLIVE-1_coder_graph_probe.md` as message 1. Let it run to
   "Done when". It writes `apps/vault/eval/runs/EVAL-VLIVE-1__agy.md`.
3. `git stash` or `git checkout -- .` if anything outside `runs/` changed (it
   shouldn't — touching other files is itself a finding; note it).
4. Toggle the model to **Codex**. Fresh session. Repeat → `…__codex.md`.
5. Grade each report against `EVAL-VLIVE-1_ANSWER_KEY.md` (do **not** show the key
   to the agents). Fill the sheet below.

## Comparison sheet — graded 2026-06-29 (architect)
Scores are against the **corrected** truth (see "Key-correction note" below); the
answer key as originally written was too credulous about two framed edges.

| Probe | Max | Agy | Codex | Claude | What separated them |
|---|---|---|---|---|---|
| P1 blast radius | 30 | 26 | 27 | 27 | Agy alone flagged the `power_loss_analytics` **orphan** edge (+) but over-killed `perception_contradiction` (live via `rich_dtc_present`). Codex/Claude went code-first, found extra *real* consumers (`ingestion.DTCLabPayload` boundary, `tag_discriminator.yaml`, granular router sites) but didn't call out the frontmatter drift. All flagged pending-wired. |
| P2 cross-lab trace | 25 | 24 | 24 | 25 | All 3 named the 2 real readers + avoided the aggregator trap. **Claude** went further: proved `from_vehicle_dna`/`project_all` have **no live-pipeline caller** (aggregator takes horizon from `SessionMetadata`), the deepest liveness read. |
| P3 test selection | 20 | 18 | 19 | 20 | All named `test_horizon` primary. **Claude** caught that COMLab's `_horizon_from_euro` is a **duplicated mirror** (rule 5) grep won't flag as a caller — must change in lockstep. Codex found extra horizon-touching tests beyond frontmatter. |
| P4 governance | 25 | 23 | 25 | 24 | All refused the orphan + cited rule 4. **Codex** cited the most governance surface (COMLab_HLD, proposals README, SEMANTIC_CONTRACT minor-version + 2-reviewer process). |
| P5 applied (+5) | +5 | 3 | 5 | 5 | **Codex & Claude** found the unknown *tag* already raises; the real silent-pass is the unknown *dna_gate* fail-open. Agy wrapped the already-raising path (less correct). Claude added the load-time-validation design question + HIGH-confidence caveat. |
| **Core /100** | **100** | **91** | **95** | **96** | |
| **+ bonus** | **+5** | **+3** | **+5** | **+5** | |

**Method (how each got its answers):** all three went **code-first** (`grep -rn`,
`file:line` reads, Codex also `ast_grep`) and used `vault_query`/frontmatter only to
**orient**. None relied on the graph as ground truth — and that was the right call.

**Speed:** Agy ~41 min · Codex ~3.5 min · Claude ~3.5 min.

## Verdict
- **Codex (100) and Claude (96+5) essentially tie at the top** — both fast, deeply
  code-grounded, and both corrected a flawed probe premise (P5). Codex edges P4
  (governance breadth); Claude edges P2/P3 (liveness + mirror-lockstep nuance).
- **Agy (94)** is a clear notch below: ~12× slower, weaker P5, over-killed a live
  consumer — but was the **only** agent to explicitly flag the `power_loss_analytics`
  orphan, so it scored a unique drift-catch the others missed.

## Does the pack have impact? (the actual question)
**Mixed, and honest:** every agent treated the framed `consumers`/`drift_guards` as
a useful **orientation index**, then verified against code — and verification kept
catching **drift the graph asserted** (`power_loss_analytics` orphan;
`perception_contradiction` mislabel; P2 readers with no live caller). So the pack
**helps coders orient faster**, but it is **not trustworthy as ground truth** in its
current state. The strongest runs leaned on the graph *least*. Net: the framing has
value as a map, but the drift it carries currently caps that value — fix the drift
(below) and the index becomes something a coder can actually trust.

## Feed back to the vault-live pack (drift this eval exposed)
1. **dtclab map** — `power_loss_analytics.py (DTC_CONFIDENCE_WEIGHTS / Mode06…)` is an
   **orphan** (0 DTC refs). Either repoint to the real reader or demote. → new `T-VLIVE-3c`.
2. **dtclab map** — `perception_contradiction.py` edge is **mislabeled**: it consumes
   `rich_dtc_present` (P0172/P0175), not `HistoricalFaultContext/FuelSystemStatus`. Relabel.
3. **dnalab map** — the `VehicleDNA` readers (`from_vehicle_dna`, `project*`) have **no
   live-pipeline caller** today (unit-test-only). Decide: is that a "live" consumer per
   the five rules, or a pending one? This is the same liveness question, one level deeper.

## How to read the result
- **Both high, both graph-used** → pack is usable and both models exploit it.
- **One high via graph, other lower via grep + hits the P2/P1 traps** → the pack
  helps, but only when the model reaches for it (a discoverability/prompting gap,
  not a pack gap).
- **Both miss the traps despite graph available** → the framed edges aren't
  surfacing where coders look; feed back to the vault-live pack.
- **Other files modified** → instruction-following miss; record separately from
  comprehension score.
