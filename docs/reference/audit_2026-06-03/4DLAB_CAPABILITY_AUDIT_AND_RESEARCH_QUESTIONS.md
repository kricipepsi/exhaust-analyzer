# 4DLab — Full Capability Audit & External-Research Question Pack

**Date:** 2026-06-03
**Author:** engineering audit (read-only; no code changed)
**Purpose:** Diagnose the ~50% engine-capability ceiling and hand the user a
focused list of **10 questions per lab that the codebase cannot answer** — the
genuine knowledge gaps to take into external research.

**Why now:** the last FX campaign (`T-FX-WIRE-1`, 2026-06-02) confirmed the
engine is stuck at **51.2%** despite a full coverage + discriminator push. The
remaining gap is not a coding gap — it is a **knowledge and data** gap. This
document maps the culprits, then converts each into research questions.

**Provenance (what was read for this audit):**
`diag/DIAG_SUMMARY.md`, `arch-decision/ARCH_DECISION_PATH_FORWARD.md`,
`CROSS_APP_DIAGNOSTIC_COMPARISON.md`, `registry/CHEMISTRY_COVERAGE.md`,
`registry/CORPUS_AUDIT.md`, `patch/TRIM_RESEARCH_2026-05-31.md`,
`fx_tasks/O2_MODEL_STRATEGY.md`, `FX_PROGRESS.md` + the `fx_tasks/` ledger,
and the four per-lab audit reports (`GASLAB_AUDIT_2026-05-19.md`,
`OBDLab_Audit_Report.md`, `DTCLab_Audit_Report.md`, `DNALab_Audit_Report.md`),
plus `COMLab/PATH_FORWARD.md` and `registry/rules/`.

---

## Part 1 — The ceiling, diagnosed

### 1.1 Where capability actually leaks

Accuracy has moved 32.4% → 51.6% → 51.2% across the patch and DNA/REG campaigns,
then stalled. The failures decompose into three buckets that every architecture
in the cross-app study reproduced:

| Bucket | Meaning | Size (latest in-scope triage) | Nature of the problem |
|---|---|---|---|
| **PRUNED / never-surfaced** | correct family never enters the candidate set | ~44 (was 54; mostly closed by REG-2) | **coverage** — a knowledge problem (no rule maps the evidence to the family) |
| **OUTRANKED** | correct rule is present but loses the score | ~82–90 | **discrimination** — a scoring + evidence problem |
| **data-gap (STOP)** | the discriminating signal is absent from the data | ~27 (ecu_fault) | **measurement** — no code change can recover it |

### 1.2 The four systemic culprits (ranked)

**Culprit 1 — The ranking problem is now the whole game, and it is data-starved.**
REG-2 added 24 coverage rules and rescued 37/44 PRUNED cases; accuracy did **not**
move. Reason: once the correct rule survives pruning it is simply **outranked**.
The intended tie-breakers — DTC routing tags and the symptom prior — are *present
but starved*: **64 of 90 outranked cases carry no DTC at all** (`T-FX-REG-3`), and
the symptom prior fires on only ~47/281 cases.

**This is structural, not a corpus accident: not every powertrain or fault
triggers a DTC.** Many genuine faults never mature a code (single-trip monitors
not met, fault below the OBD threshold, mechanical wear / vacuum / exhaust-leak
conditions the ECU has no monitor for), and large swathes of the 1990–2010 fleet
are pre-OBD-II or thin-OBD where codes are sparse or absent entirely. So building
the **primary** rank discriminator on DTC routing tags is betting on a signal
that is missing for a structural majority of cases — the engine needs a primary
discriminator that does **not** assume a DTC exists. The team's own conclusion
(`T-FX-WIRE-2` premeasure): porting all stranded rules yields **+4 cases (52.7%)**;
"rank-weight is the real lever" — but the evidence that would drive rank weight
isn't in the data.

**Culprit 2 — The perception-vs-truth signal, the original architectural thesis,
is not measurable from the available data.** 27 `ecu_fault` cases are marked
`data-gap (STOP)`: distinguishing "the ECU is wrong about mixture" from "the
mixture is genuinely wrong" requires `lambda_perception_delta` and trim
divergence, and OBDLab emits only `o2_failure_mode = NO_FAULT` across all of them.
OBDLab is effectively **dead on this corpus** (>95% NO_FAULT, VE pinned). The
whole truth-vs-perception override was also shown to be net-negative when forced
(App 4 `resolve_conflicts` = −5), so the architecture pivoted to "prior, not
override" — which is correct, but leaves these cases unrecoverable without new data.

**Culprit 3 — The corpus is synthetic, partly hand-filled, and may not carry
enough signal to reach 85%.** `TRIM_RESEARCH` documents fabricated/!uncertain
trim values, ±127 sentinels of unclear meaning, blank `ect` masking, and a
dead-literal bug (`DUAL_BANK` vs `dual`) that dropped *every* bank-2 trim. The
`TIMING_RETARDED` chemistry state — the single most common GASLab emission (~64
cases, ~25%) — historically had **zero** matching rules and maps to **7
different families**. If the corpus labels and signals are not themselves
trustworthy and discriminating, the accuracy number is measuring the corpus, not
the engine.

**Culprit 4 — Many fault families are chemically/electronically indistinguishable
with the evidence collected.** mechanical_wear, exhaust_leak, ignition_fault,
non_starter, and several ecu_fault cases share chemistry/DTC signatures with
louder families (misfire, lean) and lose every tie. This is a *family-taxonomy +
evidence-sufficiency* question, not a tuning question — and tuning weights to fix
it provably regresses neighbours (`FT-8`, the "scoring tightening is a smell"
finding).

### 1.3 The one-sentence diagnosis

> Coverage is largely solved; the engine is now **ranking-bound**, and the
> tie-breakers it needs (DTC presence, OBD trim/perception signal, reliable
> per-vehicle baselines, trustworthy symptom labels) are **missing from the
> data, not from the code** — so the next gains are a research/data problem.

---

## Part 2 — fx_tasks ledger analysis (requested)

The `fx_tasks/` ledger is ~60 tasks. They fall into five waves; the pattern of
*what moved the number and what didn't* is itself a finding.

**Wave A — Schema/contract gap-closure (T-FX-1..8, T-FX-9..11).** Typed the
COMLab payloads, removed the GASLab→DTCLab cross-dependency, added
`WIDEBAND_NB_SIM`, the perception-contradiction detector, the no-OBD λ fallback,
EGR/incomplete-oxidation signatures, the downstream-trim role and de-cat flag.
*Effect:* made the boundaries clean and honest. **Did not move accuracy** — these
were plumbing, not new discriminating evidence.

**Wave B — Documentation drift audits/syncs (T-DOC-1..17).** A very large
fraction of the ledger is wiki/doc reconciliation. Valuable hygiene, **zero
accuracy effect.** Worth noting because it shows a lot of effort went into
keeping specs consistent rather than into new signal.

**Wave C — Git/monorepo flatten (T-GIT-1..8).** Infrastructure. No accuracy
effect. One relevant artefact: a cross-lab import guard now enforces isolation at
commit.

**Wave D — DNA absorption (T-FX-DNA-1..6).** C2 (per-vehicle CoC targets into
GASLab), C3 (surface resolved horizon), C1 (bounded symptom prior). *Effect:*
49.8% → **51.2% (+1.4pp)**. Crucially, `T-FX-DNA-6` found the **CoC band only
gates the NORMAL state** — a *structural ceiling* on how much per-vehicle
calibration can help. The symptom prior fires on only ~47 cases at weight 0.10
with **0 false-positive delta** — helpful but tiny, because corpus symptom density
was 17.8% (enriched to 31.7% in `T-FX-DNA-5`).

**Wave E — Denoise + registry expansion + honest baseline (PURGE, REG, WIRE).**
The most recent and most telling wave:
- `T-FX-PURGE-1/2/4/5`: removed MODERN (>2010) noise families/rules. Re-measure:
  **51.2%, 0 delta** — the denoise did not regress in-scope but also didn't lift
  it.
- `T-FX-REG-2`: +24 coverage rules, 37/44 PRUNED rescued → **still 51.2%.**
- `T-FX-REG-3`: routing-tag rank discriminator → **0 false-positive delta;
  OUTRANKED bucket "data-limited (64/90 no DTCs)."**
- `T-FX-REG-4`: re-measure → **0 delta, bottleneck shifted PRUNED→OUTRANKED.**
- `T-FX-REG-5`: crossed 100 rules → **still 51.2%** ("rules stranded in
  COMLab-internal").
- `T-FX-WIRE-1`: honest full composite run → **51.2% (0.0pp)**; diagnosis: REG-2/5
  rules are **stranded on the COMLab-internal registry, not the harness REG-V2
  path**; discriminators are on-path but starved.
- `T-FX-WIRE-2` (pending): porting the stranded rules measures **+4 cases →
  52.7%**, and the gain is again **OUTRANKED-bound**. Conclusion in the ledger:
  *"rank-weight is the real lever."*

**Ledger takeaways:**
1. **Every accuracy gain to date came from new evidence channels (DNA), never
   from rules, docs, or plumbing.** The +1.4pp from DNA absorption is the only
   real movement; everything since is ≤ +4 cases.
2. **There is an architecture split** — rules live in two places (REG-V2 shim vs
   COMLab-internal `global_fault_registry`), which is why "100 rules" didn't show
   up in the harness. Consolidation (`T-FX-WIRE-2`) is the honest next step but
   caps at ~52.7%.
3. **The ledger has independently arrived at the same wall this audit describes:**
   the OUTRANKED bucket is data-limited. The open follow-ups
   (`T-FX-REG-Pid`, `T-FX-REG-Eps`, several `T-FX-DOC-L*`) are premise-unverified
   or cosmetic — none is a credible path to a step-change.
4. **Unresolved real contract gaps still sit in the deferred table:** `T-FX-12`
   (COMLab O2 enum missing `WIDEBAND_NB_SIM`), `T-FX-13` (COMLab DTC regex
   decimal-only vs DTCLab hex — would reject GPF payloads at the gate). These are
   correctness, not capability, but worth clearing.

---

## Part 3 — Research questions per lab

Rules for this list: every question is one the **code/docs do not answer** and
that an automotive-diagnostics expert, standards document, or real-world dataset
**could**. Each carries the bucket it attacks. These are the inputs to push past
51%.

### GASLab — exhaust-gas chemistry (the "ground truth" layer)

State: clean, well-tested library; the issue is **domain coverage**. The most
common chemistry state maps to 7 families; several families emit no distinct
chemistry; the validity gate rejects real-fault samples.

1. **What 5-gas idle signature actually separates `TIMING_RETARDED` into its
   seven candidate families** (lean, catalyst, sensor, cam_timing, misfire,
   ecu, mechanical_wear)? This single state is ~25% of the corpus and is the
   largest discrimination gap. *(OUTRANKED/PRUNED)*
2. **How reliable is Brettschneider λ from a standard 5-gas analyzer as
   "ground truth" at idle, per fault type** — does it degrade predictably for
   misfire (raised O₂), air leaks, or catalyst masking, and what is the
   uncertainty band? *(validates the whole truth-vs-perception thesis)*
3. **What is the genuine gas signature of a pre-cat exhaust air leak** (low CO,
   elevated O₂, low HC) and **can it be told apart from a sample-handling
   error** before the triangle validity gate `CO+CO₂+O₂ ∈ [14,18]` rejects it?
   7/9 exhaust_leak cases die here. *(PRUNED)*
4. **What measurable idle-gas differences distinguish worn piston rings vs worn
   valve seals vs worn engine vs internal coolant leak — and from misfire?**
   mechanical_wear (0/11) emits no distinct chemistry today. *(PRUNED/OUTRANKED)*
5. **Do per-engine CoC idle targets (CO, HC, target λ, idle RPM) for the
   1990–2010 petrol fleet actually exist and discriminate**, or are factory idle
   specs too coarse/uniform to sharpen lean/rich classification? (`T-FX-DNA-6`
   found CoC only gates the NORMAL band — is that a data limit or a design one?)
6. **Empirically, how often and by how much does tailpipe chemistry diverge from
   ECU-reported λ across real faults?** If the divergence is usually small, the
   perception-contradiction detector has little to work with. *(data-gap)*
7. **What idle (and idle-vs-2500rpm) gas signature uniquely identifies cam/valve
   timing faults** (VVT, wrong/retarded timing) versus generic misfire, which
   currently outranks them? *(OUTRANKED)*
8. **How much do fuel formulation (E5/E10, winter blend) and altitude shift idle
   gas readings**, and what are the standard corrections, so these don't cause
   lean/rich misclassification? *(corpus realism)*
9. **Is gas chemistry informative at all for ignition_fault, non_starter, and
   ecu_fault**, or are these fundamentally non-chemical families that GASLab
   should explicitly abstain on? *(PRUNED / taxonomy)*
10. **Can a single warm-idle snapshot diagnose catalyst_failure**, or does
    reliable catalyst diagnosis require a light-off / load transient that the
    single-point corpus doesn't capture? catalyst_failure is 11/22. *(measurement)*

### OBDLab — live PIDs, fuel trims, O₂, volumetric efficiency

State: structurally sound but **dead on this corpus** (>95% NO_FAULT). The
signal that would rescue ecu_fault and sensor_fault isn't present, and trim
values are partly fabricated.

1. **Can `ecu_fault` (ECU wrong about mixture) be separated from a genuine
   mixture fault using only technician-pullable OBD-II data**, and exactly which
   PID combination does it? 27 cases are currently unrecoverable. *(data-gap)*
2. **What are realistic STFT/LTFT magnitudes and signs per fault family at warm
   idle on 1990–2010 petrol engines?** 16 corpus cases need researched trims and
   the team is currently guessing. *(corpus realism → OUTRANKED)*
3. **Do real STFT/LTFT PIDs ever reach ±100/±127, or is that a sentinel
   convention?** What does a shorted/open O₂ sensor actually report on a scan
   tool? (`case_025/026` ambiguity.) *(corpus realism)*
4. **Which model years/OBD protocols actually report a usable λ / commanded-λ
   PID** so `lambda_perception_delta` is computable in the real fleet, rather
   than only in synthetic rows? *(data-gap)*
5. **For single-air-sensor engines (MAP-only or MAF-only), is any valid VE
   cross-check possible at all**, or is VE-based sensor diagnosis impossible
   without a second independent air measurement? (Audit found VE pinned/circular
   in these modes.) *(measurement)*
6. **How much of the 1990–2010 fleet supports fuel trims and Mode $06**, and how
   trustworthy are those values pre-2001? If coverage is thin, OBD discriminators
   are structurally weak for older cars. *(data-gap)*
7. **What downstream-O₂ behavior actually indicates a secondary-trim loop is
   masking upstream drift**, and is it detectable from a scan tool? The
   `downstream_trim_role` model has a flag but **no signal channel**. *(data-gap)*
8. **Which Mode $06 monitor IDs / on-board test results discriminate catalyst /
   misfire / EVAP / O₂ faults on this fleet**, and are they standard enough to
   encode without per-OEM tables? *(coverage)*
9. **What scan-tool-exposed O₂ metrics (switch rate, amplitude, response time)
   separate a lazy/aged sensor from a biased one from a dead one?** sensor_fault
   is 10/24. *(OUTRANKED)*
10. **Will the actual product ever capture live PIDs in its workflow** — i.e.,
    is OBDLab worth reviving, or should it stay quarantined and its schema fields
    be pruned under the signal/noise rule? *(scope decision)*

### DTCLab — DTC sanitization → routing tags (the main rank discriminator)

State: clean code; the discriminator it produces is **starved** — most outranked
cases have no DTC, and the generic-code→family mapping strength is unmeasured.

1. **Across the 1990–2010 petrol fleet, what fraction of real fault cases present
   a stored DTC at diagnosis time?** 64/90 outranked cases have none — if no-DTC
   is the norm, DTC discriminators are structurally weak. *(OUTRANKED, core)*
2. **What is the empirical P-code→family mapping strength?** Does P0171 reliably
   mean lean_condition, or fire across vacuum leak / MAF / fuel-pressure /
   exhaust-leak with similar frequency? Need real co-occurrence statistics.
   *(OUTRANKED)*
3. **Which manufacturer-specific (P1xxx) codes carry discriminating power the
   generic set lacks**, and can they be used without per-OEM databases? *(coverage)*
4. **Which freeze-frame parameters most improve family discrimination** (load,
   RPM, ECT, fuel-trim-at-freeze) and how consistent are they across OEMs?
   *(OUTRANKED)*
5. **How should DTC state (pending $07 / confirmed $03 / permanent $0A) weight
   the family prior differently** — what's the professional convention? *(ranking)*
6. **How should multi-DTC patterns be read as a combined signature** (e.g.
   P0300+P030x, or P0171+P0174) rather than independent tags? *(OUTRANKED)*
7. **Are GPF / Euro-6d hex-tailed codes (P244A) even in scope for 1990–2010**, or
   are they dead weight inherited from a wider-scope era? (Ties to the `T-FX-13`
   regex contract gap.) *(scope)*
8. **Can cylinder-specific misfire codes (P0301–P0308) plus their pattern/count
   discriminate mechanical vs ignition vs lean vs fuel misfire** from the DTC set
   alone? *(OUTRANKED)*
9. **How do one-trip vs two-trip monitor maturation and clearing behaviors bias
   which codes are present**, and could that skew the corpus toward/away from
   families? *(corpus realism)*
10. **What domain heuristic do professional techs use to pick the "primary" code**
    among several stored simultaneously? There may be a standard severity/priority
    ordering the rank step could adopt. *(ranking)*

### COMLab — the prune→rank scoring spine + fault-atlas routing

State: this is where OUTRANKED happens. Weight tuning hits a ~45% reshuffling
ceiling; rules are split across two registries; the open question is whether a
hand-weighted ranker can win at all.

1. **Can a hand-tuned, additive weight-based prune→rank exceed ~55% on this
   problem**, or does the outranked bucket require a learned/statistical ranker?
   What do comparable rule-based vs ML diagnostic engines score on similar tasks?
   *(architecture)*
2. **What is the Bayes-optimal accuracy ceiling given the corpus's actual signal
   content** — i.e., how many cases are genuinely under-determined by the
   collected evidence, no matter the model? *(sets the real target)*
3. **Is there a principled scoring formulation that uses contradiction as a
   discriminator without destructive override**, given forced overrides measured
   net-negative (App 4 −5)? *(architecture)*
4. **Would calibrated likelihood / Bayesian fusion of the independent channels
   (gas, DTC, symptom, OBD) beat additive weights** without re-creating the App-1
   fusion failure (which destroyed single-lab evidence)? *(architecture)*
5. **What confidence calibration makes "DEFINITIVE" vs "suggestive" tiers reflect
   real diagnostic likelihood ratios** rather than arbitrary weights? (The
   "scoring tightening is a smell" memo says nudging weights just reshuffles.)
   *(ranking)*
6. **For families sharing a signature (misfire vs mechanical_wear; lean vs vacuum
   vs exhaust leak), what is the minimal additional evidence that breaks the
   tie**, and is it ever actually available? *(OUTRANKED, core)*
7. **Should the engine output a top-2/top-3 differential instead of forcing one
   verdict**, and how would that change the accuracy target and the user value?
   *(product + metric definition)*
8. **What magnitude should an operator-symptom prior carry** so it rescues the
   never-surfaced bucket without override harm? What do clinical/automotive
   decision-support systems use for self-reported priors? *(ranking)*
9. **What is the precision/recall tradeoff of loosening the prune gate** (it
   sometimes drops the correct rule; candidates_out as low as 6) on this corpus?
   *(PRUNED vs false-positives)*
10. **Is the fault-family taxonomy well-posed — are the 13–16 families mutually
    exclusive and collectively exhaustive**, or do overlapping/ill-defined
    boundaries inherently cap accuracy? *(taxonomy, foundational)*

### DNALab / VINLab — vehicle identity + operator symptom (the independent prior)

State: the richest *untapped* channel, but the prior is weak in practice — low
symptom density, PARTIAL VIN confidence, ~62–65% CoC fill, empty `model`.

1. **How predictive is a user-reported primary symptom of the true fault
   family?** Need the empirical confusion matrix between reported symptom and
   confirmed fault to set the prior's strength honestly. *(never-surfaced, core)*
2. **What is realistic VIN-decode resolution for 1990–2010 vehicles** — can VIN
   reliably yield engine code, induction, fuel delivery, O₂ config, EGR/cat
   equipment, or is decode too partial? (Traces show `confidence=PARTIAL`
   uniformly.) *(data quality)*
3. **Do accessible per-engine-code CoC / type-approval idle datasets exist for
   this fleet, and how complete?** Currently ~62–65% filled from CSV medians — is
   there a real source? *(data availability)*
4. **Which vehicle-identity attributes actually interact with the diagnosis**
   (change the correct answer given the same gas/OBD signature) versus being
   collected but diagnostically inert? *(signal/noise)*
5. **What structured-symptom vocabulary do professional techs actually use**, and
   is the current 18-pair tier_1/tier_2 catalog complete and correctly mapped to
   families? *(coverage)*
6. **How should environmental context (cold/hot, occurs-during, engine-state)
   modify the family prior** — is there documented symptom-context→fault
   evidence? *(ranking)*
7. **How prevalent are non-VIN-decodable aftermarket mods (de-cat, aftermarket WB
   O₂) in the target fleet, and how much do they corrupt diagnosis if unknown?**
   *(data quality)*
8. **Does finer identity (`model`, engine variant) actually matter for
   diagnosis**, or is engine_code + displacement + induction sufficient? `model`
   is always empty today — confirm it can stay that way. *(scope)*
9. **What is the real-world rate of false/misleading operator symptom reports**
   that should bound how far the symptom prior is trusted? *(prior bounding)*
10. **Does labeled symptom→confirmed-fault data exist (e.g. repair-order
    datasets) to validate or train the prior**, rather than synthetically
    enriching the corpus? *(data availability)*

---

## Part 4 — Where to point research first (highest leverage)

If the goal is the biggest accuracy step for the least research, attack the
**OUTRANKED + data-gap** buckets, in this order:

1. **DTC presence reality (DTCLab Q1) + P-code→family mapping strength
   (DTCLab Q2).** The single biggest discriminator is starved; if no-DTC is the
   norm, the architecture needs a different primary discriminator.
2. **`TIMING_RETARDED` family-separation chemistry (GASLab Q1).** One state, 25%
   of the corpus, 7 families — the largest concentrated discrimination gap.
3. **Whether ecu_fault is separable from real mixture faults at all (OBDLab Q1 +
   GASLab Q6).** This decides if the 27 `data-gap` cases are recoverable or should
   be conceded.
4. **The Bayes-optimal ceiling on the current corpus (COMLab Q2) and whether the
   taxonomy is well-posed (COMLab Q10).** These tell you whether 85% is even
   reachable with this data — before more engineering is spent chasing it.
5. **Operator-symptom predictiveness (DNALab Q1).** The cheapest independent
   channel; quantifying its real strength tells you how hard to lean on it.

A candid framing for the research: the evidence strongly suggests the **corpus
and the available signal channels — not the engine logic — are the binding
constraint.** Several questions above (corpus realism, Bayes ceiling, taxonomy
well-posedness, DTC presence rate) are really asking *"is 85% achievable with
this data?"* That question is worth resolving early, because if the answer is no,
the productive path is **better/real diagnostic data**, not more rules.
