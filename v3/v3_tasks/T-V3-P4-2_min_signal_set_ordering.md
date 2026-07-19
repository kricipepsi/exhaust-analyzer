### Goal ###
Turn the per-cluster acquisition spec into a single **acquisition decision map**: which real
measurement the owner should collect **first** to unlock the most residual cases for the least
shop cost. Invert the spec's per-case `unlock_columns` into a **column → clusters/cases served**
index, group columns into the concrete shop actions that capture them, and rank those actions by
**cases-unlocked-per-feasibility-tier-cost** (the research "minimum added-signal set"). Output the
recommended acquisition order + the corrected cluster yield ranking. **Read-only over the P4-1
outputs — no engine/lab/registry/corpus edit, no new column added.** This is the disclosure that
decides *which* signal pack the owner enables first.

### Progressive-disclosure role — the DISCLOSE step ###
Phase-4 signal packs are the expensive commits and each is **owner-data-gated**: the owner must go
collect a real measurement before a pack can run. Committing to the wrong cluster first wastes a
data-collection trip. `T-V3-P4-1` disclosed the per-cluster contracts but left two decisions open:
(1) its `ordered_clusters` is the stale handoff order — once HARD cases fold in, **C3 (21) nearly
ties C2 (22)** and jumps six places; (2) fuel-trim / MAF columns are **shared across 5-6 clusters**,
so a single cheap OBD acquisition (Tier-a) partially serves many packs — the spec priced these
per-cluster, never once. This task surfaces the cheapest-highest-yield acquisition so the owner
picks the first pack from evidence. It commits **nothing**; the per-cluster packs (`T-V3-P4-C*`)
gate behind it.

### Why this split (the trap it avoids) ###
Authoring the C2 pack now would pre-commit the owner to acquiring pre/post-cat gas (a Tier-b/c
action serving C2 only) when enabling **live STFT/LTFT at idle+2500** (Tier-a, one OBD action)
partially serves C2, C3, C5, C6, C9 at once. Ordering by single-cluster yield (the stale list) is
not the same as ordering by acquisition cost. The right first move is knowable **read-only** from
`unlock_columns`, before any data is collected or any pack is built.

### Success criteria ###
Produce `v3/reports/V3_MIN_SIGNAL_SET_2026-07-01.{md,json}` from
`v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json` (`case_unlocks`, `cluster_counts`):
1. **Column → served index:** for every corpus column named in any contract, list the clusters that
   name it and the count of residual cases in those clusters. Mark each column's feasibility tier
   (a OBD live/Mode $06 · b 5-gas-used-differently · c added shop equipment · d lab-only) from the
   spec's per-cluster tier notes.
2. **Shop-action grouping:** group columns into the concrete acquisition each shop action yields
   (e.g. *"enable live fuel trims"* → `stft_idle_pct, ltft_idle_pct, stft_2500_pct, ltft_2500_pct`;
   *"Mode $06 read"* → catalyst/O2/misfire monitor columns; *"cranking bundle"* → C8 columns). One
   action can serve multiple clusters — count its reach once.
3. **Minimum added-signal set (the headline):** greedily rank shop actions by
   cases-unlocked-per-cost and emit the shortest ordered acquisition list that covers the most
   residual cases, with a **cumulative cases-covered** column. Cite the research "Minimum
   added-signal set" section where it already names a shared set.
4. **Corrected cluster yield order:** re-rank clusters by `cluster_counts`
   (C2 22 · C3 21 · C6 14 · C9 11 · C4 11 · C5 10 · C8 6 · C1 5 · C7 3) and state plainly that this
   supersedes the spec's stale `ordered_clusters` for owner sequencing.
5. **Recommended first pack:** name it, with the one acquisition that unblocks it and how many cases
   it (and its shared columns) reach. This is the disclosure that scopes the first `T-V3-P4-C*`.
- **Reconciliation:** every residual case in `case_unlocks` (103) is attributed to at least one shop
  action; `CASE-039` (re-bucketed to C3 by `T-V3-P4-0A`) is folded in and called out as the +1 the
  spec's 103 did not include (→ 104). Any case reachable only by a Tier-c/d action is flagged as
  expensive-to-unlock.
- No file outside `v3/` modified; `top3_family` and the yardstick untouched. `py_compile`+`ruff`
  clean on any helper.

### Disclosure (what this task must surface, not hide) ###
State clearly that a shared column **lowers acquisition cost but does not independently unlock a
case** — each case unlocks only when its cluster's *decisive* producer signal is present, so
"fuel-trims first" is a cost-efficient *start*, not a full fix for any cluster. If the cheapest
action (Tier-a OBD) still leaves a cluster needing a Tier-c shop test to actually fire its producer,
say so — do not present a cheap partial as a full unlock. Report the true cumulative coverage per
action, and name cases no acquirable action reaches (they stay abstained).

### Context ###
- Input: `v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json` — `case_unlocks[*].unlock_columns`,
  `.cluster`, `.bucket`; `cluster_counts`; `contracts` (per-cluster tier notes + producer/consumer).
  And the `.md` Tier-1 matrix for the feasibility-tier wording.
- The research "minimum added-signal set": `v3/reports/RESEARCH_PROMPT_blocking_measurements.md`
  (output item 3) and `v3/research/research_answers/cluster{1-9}.md` per-cluster feasibility tiers.
- `CASE-039` reroute evidence: `v3/reports/V3_P4_CLASSIFIER_FIXABLE_RECHECK_2026-07-01.md`
  (RE-BUCKET_TO_SIGNAL → C3).

### Consumer (signal/noise) ###
- **Consumer:** the owner's real-world acquisition decision (what to measure first) and the first
  per-cluster signal pack (`T-V3-P4-C*`), which gates behind this ordering. No field/enum/fault is
  added to the engine — this task *sequences* the acquisitions the packs will consume.

### Deliverables ###
1. `v3/reports/V3_MIN_SIGNAL_SET_2026-07-01.md` — CREATE. Column index + shop-action ranking +
   corrected yield order + recommended first pack.
2. `v3/reports/V3_MIN_SIGNAL_SET_2026-07-01.json` — CREATE. Machine-readable action→cases + cumulative.
3. (Optional) `v3/build_min_signal_set.py` — CREATE, read-only inverter over the spec JSON.

### Files to touch ###
- `v3/reports/V3_MIN_SIGNAL_SET_2026-07-01.md` (CREATE)
- `v3/reports/V3_MIN_SIGNAL_SET_2026-07-01.json` (CREATE)
- (optional) `v3/build_min_signal_set.py` (CREATE, read-only)

### Out of scope ###
**No engine/scorer/oracle/CSV/registry/lab edit. No corpus column created. No synthesized values.**
No abstain changes (dial stays MARGIN=0.02). No signal pack authored here (that is `T-V3-P4-C*`,
gated behind this). Writes only under `v3/`. Never `Vault/`. GRAPH GUARDRAIL: no `graphify` /
frozen-graph rebuild. No secrets in files.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/build_min_signal_set.py 2>/dev/null || true
/agent_workspace/.venv-wired/bin/python -m ruff check v3/ 2>/dev/null || true
/agent_workspace/.venv-wired/bin/python v3/build_min_signal_set.py 2>/dev/null || true
# ranked actions + cumulative present; all 103 (+CASE-039) attributed; corrected order stated:
grep -iE 'cumulative|fuel.?trim|Mode ?06|C3|minimum|first pack|CASE-039' v3/reports/V3_MIN_SIGNAL_SET_2026-07-01.md
```
Gate: every `case_unlocks` case (103) attributed to >=1 shop action + `CASE-039` folded (104);
actions ranked by cases-per-cost with a cumulative-coverage column; corrected cluster order stated
as superseding the spec's `ordered_clusters`; shared-column caveat present; no file outside `v3/`.

### Progress hook ###
PROGRESS.md `T-V3-P4-2`: Status=done, Files changed=N (all new under v3/), Verification="Min
added-signal set: shop actions ranked cases-per-cost with cumulative coverage; fuel-trims/Mode06
flagged as multi-cluster cheap start; corrected yield order C2/C3/C6/... supersedes stale list;
104 cases (incl CASE-039) attributed; shared!=unlock caveat surfaced; no engine/corpus touched".

### Depends on ###
`T-V3-P4-1` done (spec JSON present) and `T-V3-P4-0A` done (`CASE-039` reroute). Runnable now.
