
> **Context:** ADR-0010 · Module: COMLab · Section: Preamble · Parent document: COMLab HLD v2.0 / COMLab DLD v2.0
# ADR-0010: Deterministic 5-phase triage with a confidence floor and a catalyst-damage override

**Status:** Accepted

**Context.** Multiple registry rules can match one session, and the same input
must always yield the same verdict (frozen models, reproducible diagnoses, CI
grids). The engine also has a safety obligation: a catalyst-damaging misfire must
escalate regardless of how the score ranks.

**Decision.** `fault_atlas_router.execute_triage_loop` walks a fixed **5-phase**
pipeline: **(1) Horizon** prune (drop rows not targeting the resolved era) →
**(2) Chemistry/tag/perception** match → **(3) OBD operator checks** (typed
relational operators) → **(4) DTC verification** under each rule's
`DTCFallbackStrategy` → **(5) Confidence scoring** (base weight + corroboration
bonuses, plus the gated DEP fusion evidence). A rule must clear
`MIN_CONFIDENCE_THRESHOLD = 0.70` to win; open-loop trim evidence is capped
(`_OPEN_LOOP_TRIM_CONFIDENCE_CAP = 0.60`). Ranking is deterministic. Independently,
`apply_catalyst_damage_override` forces `severity_level = CRITICAL_IMMEDIATE_STOP`
when `mil_flashing` is set with a `P030x` misfire code — a safety escalation that
overrides the confidence ranking.

**Consequences.**
- Positive: a single, reproducible verdict; specific evidence beats weak; the
  confidence floor prevents low-evidence guesses from shipping as the answer.
- Positive: the catalyst override gives a deterministic safety backstop decoupled
  from scoring.
- Negative: phase order and threshold constants are part of the contract — changing
  them changes verdicts, so each numeric literal carries a wiki citation.
- Neutral: when nothing clears the floor the session resolves to `no_fault` /
  `OPTIMAL_HEALTH` rather than emitting a low-confidence winner.

**Alternatives considered.**
1. *Emit all matches and let the UI choose.* Rejected — pushes disambiguation to
   the UI and breaks the "one verdict" contract (ADR-0001).
2. *A single learned/weighted score with no phase order.* Rejected — a tuning
   surface that is hard to make deterministic and auditable.

**References.** `wiki/07_pipeline_stages.md`, `wiki/08_scoring_to_fusion_rework.md`,
`wiki/09_calibration_confidence.md`; `comlab/core/fault_atlas_router.py`
(`execute_triage_loop`, `MIN_CONFIDENCE_THRESHOLD`, `apply_catalyst_damage_override`).


## Graph relations (explicit)

**ADR-0010** DESCRIBES **Deterministic five-phase triage**
**comlab/core/fault_atlas_router.py** IMPLEMENTS **ADR-0010**
