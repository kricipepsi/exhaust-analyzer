### Goal ###
Author the **`V3_SIGNAL_ACQUISITION_SPEC`** — the precise, copy-pasteable data request that turns
each research cluster's discriminating measurement into a **concrete corpus-column + producer-state +
consumer-rule contract** the owner can fill. For every cluster it states: the new column name(s) and
units, the source (GASLab / OBDLab / shop test), the exact families the signal separates, the case_ids
it unlocks, and the producer→consumer wiring a later signal pack will build. This is the first
Phase-4 deliverable and it is **research-independent** (research has landed) — it produces the data
ask; it writes **no engine code**. Until the owner supplies a cluster's data, no signal pack begins,
so this spec is the thing that lets the owner bring exactly the right measurement first.

### Progressive-disclosure role — the DISCLOSE step ###
Phase 4's whole loop is: disclose the data ask → owner supplies one cluster's data → build that one
signal pack → re-score → decide the next cluster from the result. This task is the disclosure at the
top of that loop. It commits **nothing** to the engine; it makes the owner's next move (which
cluster's data to acquire) an evidence-based choice ordered by yield. The per-cluster signal packs
(`T-V3-P4-C2` … `T-V3-P4-C7`) are the commits, each gated behind this spec **and** that cluster's
real data landing — they are forward-registered, not authored here.

### Ordering by yield (the disclosure's spine) ###
Order clusters by cases-unlocked so the owner acquires the highest-leverage signal first:
**C2 (11) → C9 (10) → C5 (5) → C8 (5) → C1 (3) → C3 (3) → C6 (3) → C7 (2).**
(C4's rank work is already done; its residual needs signal — note it, but it is not a new-column
ask here.) Each cluster section is self-contained so the owner can act on C2 alone without reading
the rest — progressive disclosure within the document.

### The signal/noise contract each cluster section must state (canon) ###
A new field ships **only** with a named **producer** (the GASLab/OBDLab state that emits it) **and** a
named **consumer** (the rule that gates on it); **never synthesize sensor values.** So per cluster:
1. **Discriminating measurement** — from `v3/research/research_answers/cluster{1-9}.md`: the single
   measurement (or smallest combination) the research ranked highest, with its feasibility tier
   (OBD live/Mode $06 / 5-gas-used-differently / added shop equipment).
2. **Corpus column contract** — proposed column name(s), **units**, allowed range/enum, and the
   acquisition maneuver (RPM/load points, warm-up state, sampling) copied from the research
   protocol. This is the literal thing the owner adds to the corpus CSV.
3. **Producer state** — the GASLab/OBDLab state the column would drive and the bound/threshold that
   emits it (the research "expected signature" / decision band). Name the lab and where the state
   lives. (Spec only — no lab edit in this task.)
4. **Consumer rule** — which existing rule (or one new rule) in `labs/comlab/registry/rules/*.json`
   gates on the new state, and which families it then separates (e.g. C2: rich vs catalyst).
5. **Cases unlocked** — the exact case_ids this signal recovers, drawn from the residual reports, so
   the owner sees the payoff per cluster and the running total.
6. **Abstain fallback** — cases in the cluster whose signal the owner *cannot* supply stay
   **abstained**, not guessed. Name them.

### Success criteria ###
Produce `v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.{md,json}`, tiered for disclosure:
- **Tier 1 — headline matrix:** one row per cluster: measurement · feasibility tier · new column(s) ·
  producer state · consumer rule · cases-unlocked · running cumulative. Ordered C2→C9→C5→C8→C1→C3→C6→C7.
- **Tier 2 — per-cluster contract:** the six items above, self-contained, one section per cluster.
- **Tier 3 (JSON) — per-case unlock table:** every case_id in the Phase-4 residual mapped to its
  cluster, expected family, the column that unlocks it, and `unlockable | abstain-if-absent`.
- **Reconciliation:** the case_ids across clusters must reconcile against the residual buckets in the
  handoff (PRODUCER_GAP·SIGNAL_REQUIRED 23, DATA_GAP 19, HARD 49, + the 12 held TUNABLE routed here);
  state coverage and name any residual case **not** unlockable by any listed signal (honest gap).
- No engine/scorer/oracle/CSV/registry/lab file is modified. `top3_family` and the yardstick unchanged.
- `py_compile` + `ruff` clean on any helper used to assemble the JSON.

### Disclosure (what this task must surface, not hide) ###
If a cluster's research answer does **not** yield a workshop-acquirable signal (feasibility tier =
lab-only/impractical), say so — that cluster's cases stay abstained and the spec must not imply a
column the owner cannot fill. If two clusters need the **same** acquisition (e.g. live STFT/LTFT
serves C3 and C5), surface the shared column so the owner's cost is counted once — cite the research
"minimum added-signal set". Report the true cumulative unlock, not a best case: if the 8 buckets sum
to fewer than the residual, name the leftover cases that no proposed signal reaches.

### Context ###
- Residual → cluster map + counts: `v3/PHASE4_HANDOFF.md` §3 (the target list) and the exact-case
  reports it cites: `V3_PRODUCER_GAP_SPLIT_2026-06-30.md` (23 SIGNAL_REQUIRED),
  `V3_DATA_GAP_SPLIT_2026-06-30.md` (19), `V3_OUTRANKED_MAP_2026-06-30.md` (49 HARD),
  `V3_TUNABLE_REWEIGHT_MAP_2026-07-01.md` (12 held → routed here).
- The research answers (the measurement per cluster): `v3/research/research_answers/cluster{1-9}.md`.
- The already-written owner data ask (reuse its structure, do not duplicate it):
  `v3/reports/RESEARCH_PROMPT_blocking_measurements.md` — the clusters + candidate signals are stated
  there; this spec turns them into corpus-column contracts with case_ids attached.
- Rule/producer wiring targets (to name consumers): `labs/comlab/registry/rules/*.json` fields
  `chemistry_evidence` / `obd_evidence` (tier/PID), `competition_group`; producer states in
  `labs/gaslab/`, `labs/obdlab/`. Query only.

### Consumer (signal/noise) ###
- **Consumer:** the owner (the human), who reads Tier 1 and picks which cluster's data to acquire
  first; and every later signal pack (`T-V3-P4-C*`), which consumes its cluster's Tier-2 contract as
  its build spec. This task adds **no** field/enum/fault to the engine — it *specifies* them for the
  packs that will.

### Deliverables ###
1. `v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md` — CREATE. Tier 1 + Tier 2.
2. `v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json` — CREATE. Tier 3 per-case unlock table.
3. (Optional) `v3/build_acquisition_spec.py` — CREATE, read-only assembler that joins residual
   case_ids to clusters and emits the JSON; must not import-mutate engine/lab state.

### Files to touch ###
- `v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md` (CREATE)
- `v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.json` (CREATE)
- (optional) `v3/build_acquisition_spec.py` (CREATE, read-only)

### Out of scope ###
**No engine/scorer/oracle/CSV/registry/lab edit. No new corpus column actually added** — this task
*specifies* the columns, it does not create them (that is each signal pack, after the owner supplies
values). **No synthesized sensor values.** No abstain changes (dial stays MARGIN=0.02). Writes only
under `v3/`. Never `Vault/`. GRAPH GUARDRAIL: no `graphify` / frozen-graph rebuild; a fresh offline
index for querying is fine. No secrets in files.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/build_acquisition_spec.py 2>/dev/null || true
/agent_workspace/.venv-wired/bin/python -m ruff check v3/ 2>/dev/null || true
/agent_workspace/.venv-wired/bin/python v3/build_acquisition_spec.py 2>/dev/null || true
# all 8 clusters present, ordered by yield; headline totals reconcile to the residual:
grep -iE 'C2|C9|C5|C8|C1|C3|C6|C7|cumulative|abstain' v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md
```
Gate: Tier-1 matrix lists all 8 clusters in yield order, each with column/units/producer/consumer/
cases-unlocked; Tier-3 JSON maps every residual case_id to a cluster + unlock verdict and reconciles
to the handoff bucket counts (with any leftover named); no file outside `v3/` modified.

### Progress hook ###
PROGRESS.md `T-V3-P4-1`: Status=done, Files changed=N (all new under v3/), Verification="Signal
acquisition spec authored: 8 clusters in yield order C2..C7, each a column+producer+consumer contract
with case_ids; per-case unlock JSON reconciles to residual buckets; shared-column costs de-duped;
unreachable clusters flagged abstain; no engine/corpus/lab touched".

### Depends on ###
Research answers present (`v3/research/research_answers/cluster{1-9}.md`) and the residual reports
(handoff §3). Independent of `T-V3-P4-0A`. Runnable now.
