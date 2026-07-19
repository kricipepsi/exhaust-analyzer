### Goal ###
Pre-author DISCLOSURE. Before any signal-pack code, settle read-only what a signal pack can build
**from research alone** vs what stays **scoring-gated on owner per-case data**, and freeze the
**reveal contract** every C-pack (`T-V3-P4-C*A`/`C*B`) must follow. Grounded in **C2** (the first,
highest-yield pack) as the worked instance, using `v3/research/research_answers/cluster2.md`. Output
a template + the C2 instance. **No engine/lab/registry/corpus edit; no producer/consumer wired; no
data synthesized.**

### The confusion this resolves (state it plainly, do not paper over it) ###
`research_answers/` contains discriminating **logic** — quantitative thresholds and decision trees —
**not** per-case measured sensor values. So a "signal pack" is really two separable things:
1. **BUILDABLE-NOW-FROM-RESEARCH:** the producer-state emit rule + consumer rule wiring + thresholds
   are fully specified by the cluster answer and can be authored and **unit-tested on synthetic
   vectors now**, with no owner data.
2. **SCORING-GATED-ON-OWNER-DATA:** a `top3_family` delta cannot be shown until the owner supplies
   the residual cases' real column values (absent from the corpus by construction — that is why the
   cases are residual). No synthetic value may stand in.
A pack that blurs these two (reports "threshold implemented" as "cases banked") is dishonest. This
contract exists to force the separation.

### Progressive-disclosure role — the PRE-AUTHOR disclosure (owner-invited) ###
The owner asked for a task that establishes **how** the signal-pack tasks should reveal. This is it:
it does not build the pack; it discloses the pack's own reveal structure, so `T-V3-P4-C2A` (dry-run)
and `C2B` (commit) — and every later cluster's pair — inherit one honest template instead of each
re-deciding what to surface. Reveal-structure first; pack code later.

### Success criteria ###
Produce `v3/reports/V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.md` (+ `.json`) with:
1. **C2 producer extraction (cited):** from `cluster2.md`, the exact emit thresholds with line/section
   cites — Total Fuel Trim `STFT+LTFT <= -10%` → rich; Mode $06 index ratio `<= 0.20` → catalyst
   pass / high → fail; `Δt_osc < 0.5 s` → fail; decel-sweep `CO > 0.8%` → fail; and the pre-gate
   (misfire/heater codes invalidate the read). Map each to the producer state it drives
   (`CatalystConversionState` / `CatalystMonitorState`) and the emit condition.
2. **C2 consumer mapping (named):** which rules gate on the state — `rich_mixture.json`
   (RM-001/RM-003/RM-004) vs `catalyst_failure.json` (CF-001/CF-002/CF-006/CF-007) — and the exact
   `chemistry_evidence`/`obd_evidence` field each would read. No edit; just the mapping the commit
   will make.
3. **The reveal contract (the template, cluster-agnostic):** the mandatory sections every signal-pack
   task must surface, each with a one-line definition:
   - `BUILDABLE_NOW` — producer/consumer logic + thresholds derivable from the cluster answer;
     provable by unit tests on synthetic vectors, no owner data.
   - `SCORING_GATED` — the per-case owner columns still required, and which residual case_ids each
     unlocks; stays abstained until supplied.
   - `CODE_LANDED != SCORE_MOVED` — an explicit statement separating "logic shipped" from
     "top3_family delta", so neither is mistaken for the other.
   - `REGRESSION/FT-8` — the neighbour set the consumer edit touches (`passes_cases`,
     `competition_group`) and the no-regressed-family check.
   - `ABSTAIN_FALLBACK` — cases whose signal the owner cannot supply stay abstained, never guessed.
4. **C2 per-case split:** of the 22 C2 cases, which are reachable by BUILDABLE_NOW logic alone
   (none, expected — say so) vs SCORING_GATED on which columns; reconcile to 22.
5. **Owner decision surfaced:** state the fork the owner now chooses between for the *next* task —
   (i) build C2 producer/consumer code now (unit-tested, scoring deferred), or (ii) hold all pack
   code until C2 data lands — with the cost/risk of each. Do not pick for them.
- Read-only: `py_compile`+`ruff` clean on any helper; `top3_family`, yardstick, corpus untouched.

### Disclosure (what this task must surface, not hide) ###
If the research threshold is qualitative or uncited where a number is needed (e.g. index ratio band
varies by vehicle), flag it as a producer-tuning risk, not a firm constant. If any C2 consumer edit
would touch a rule shared with a non-C2 neighbour, name the neighbour now. Never imply the pack can
move the score without owner data.

### Context ###
- Research: `v3/research/research_answers/cluster2.md` (§Quantitative Signatures / Feasibility Tiers /
  Protocol). Other clusters exist for later packs; this task templates on C2 only.
- C2 contract already drafted: `v3/reports/V3_SIGNAL_ACQUISITION_SPEC_2026-07-01.md §C2` +
  `V3_MIN_SIGNAL_SET_2026-07-01.md` (C2 = first pack, 22 cases, columns A1_TRIMS + A2_MODE06).
- Consumer rules + neighbour sets (query only): `labs/comlab/registry/rules/rich_mixture.json`,
  `catalyst_failure.json` (`chemistry_evidence`/`obd_evidence`, `competition_group`, `passes_cases`).
- The pack pair this contract governs: `T-V3-P4-C2A_c2_signal_dryrun.md` (+ forthcoming C2B).

### Consumer (signal/noise) ###
- **Consumer:** the owner (chooses the next-task fork) and every signal-pack task (inherits the
  reveal contract). No engine field/state added here — this task *specifies how packs disclose*.

### Deliverables ###
1. `v3/reports/V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.md` — CREATE. Template + C2 worked instance.
2. `v3/reports/V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.json` — CREATE. Machine-readable contract +
   C2 producer/consumer/case map.
3. (Optional) `v3/build_reveal_contract.py` — CREATE, read-only extractor over cluster2.md + the C2
   contract JSON.

### Files to touch ###
- `v3/reports/V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.md` (CREATE)
- `v3/reports/V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.json` (CREATE)
- (optional) `v3/build_reveal_contract.py` (CREATE, read-only)

### Out of scope ###
**No producer/consumer wired into any lab/registry. No corpus column added. No rule/weight edit. No
re-score, no yardstick mint. No synthesized values.** No abstain-dial change (MARGIN=0.02). Writes
only under `v3/`. Never `Vault/`. GRAPH GUARDRAIL: no `graphify`/frozen-graph rebuild. `run_suite.py`
untouched. No secrets in files.

### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/build_reveal_contract.py 2>/dev/null || true
/agent_workspace/.venv-wired/bin/python -m ruff check v3/ 2>/dev/null || true
/agent_workspace/.venv-wired/bin/python v3/build_reveal_contract.py 2>/dev/null || true
grep -iE 'BUILDABLE_NOW|SCORING_GATED|CODE_LANDED|FT-8|ABSTAIN|-10%|0.20|22' v3/reports/V3_SIGNAL_PACK_REVEAL_CONTRACT_2026-07-01.md
```
Gate: the 5 reveal-contract sections present with definitions; C2 producer thresholds cited to
`cluster2.md`; C2 consumer rules named; the 22 C2 cases split BUILDABLE_NOW vs SCORING_GATED and
reconciled; the owner next-task fork stated without being decided; no file outside `v3/` modified.

### Progress hook ###
PROGRESS.md `T-V3-P4-C2-PRE`: Status=done, Files changed=N (all new under v3/), Verification="Reveal
contract frozen (BUILDABLE_NOW / SCORING_GATED / CODE_LANDED!=SCORE_MOVED / FT-8 / ABSTAIN); C2
producer thresholds cited to cluster2.md, consumers named (RM/CF); 22 C2 cases all SCORING_GATED
(0 code-reachable); owner fork surfaced (build-logic-now vs hold-for-data); nothing wired/scored".

### Depends on ###
`T-V3-P4-1`, `T-V3-P4-2` done; `v3/research/research_answers/cluster2.md` present. Runnable now.
