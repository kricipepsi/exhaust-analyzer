
> **Context:** ADR-0011 · Module: COMLab · Section: Preamble · Parent document: COMLab HLD v2.0 / COMLab DLD v2.0
# ADR-0011: Surface the routing directive and input-echo audit in the outbound contract

**Status:** Accepted

**Context.** Two pieces of session context were "internal only" in the early
design and flagged as open sign-off questions: (a) the `LabRoutingDirective` that
suppresses lab sections (e.g. a no-start engine has no live PIDs), and (b) the
technician's typed wizard inputs. The mobile wizard wipes per-screen state on view
switch, so the UI cannot reliably reconstruct what was entered, and a greyed-out
result section is confusing without an explanation.

**Decision.** Both are **surfaced in `OrchestratorFinalUIOutput`**. The routing
directive is exposed as `execution_meta.lab_routing_directive`
(`LabRoutingDirectiveOut` — the four suppression booleans plus a typed `reasons[]`
of `LabRoutingDirectiveReason`), so the UI can grey out a section *and explain why*
(PRD §5.6). The wizard inputs are carried as `user_input_echo_audit`, **emitted by
COMLab as a verbatim pass-through** — COMLab does not generate the echo, it carries
it through; when absent, Stage D emits a sentinel (`submitted_at=now`,
`groups=[]`). Both fields have named UI consumers, satisfying ADR-0003.

**Consequences.**
- Positive: the result page is self-explanatory — suppressed sections carry a
  reason, and the technician sees exactly what they typed beside the verdict
  (catches typos without re-running).
- Positive: settles two v1.0 open questions in the contract rather than leaving
  them to the UI layer.
- Negative: the outbound payload grows; both blocks are mandatory shape (with the
  echo sentinel covering the absent case).
- Neutral: COMLab stays read-only over the echo content — it never edits the typed
  values, only forwards them.

**Alternatives considered.**
1. *Keep both internal; let the UI reconstruct.* Rejected — the mobile wizard
   cannot reliably re-emit per-screen state, and unexplained greyed sections hurt
   trust.
2. *Have COMLab synthesise the echo from the parsed payload.* Rejected — that would
   echo COMLab's interpretation, not the user's raw input; pass-through is honest.

**References.** `COMLab_HLD.md` §12 (resolved Q4/Q6); `COMLab_PRD.md` §5.5, §5.6;
`comlab/schemas/response.py` (`ExecutionMeta.lab_routing_directive`,
`OrchestratorFinalUIOutput.user_input_echo_audit`);
`comlab/schemas/ingestion.py` (`UserInputEchoAudit`).


## Graph relations (explicit)

**ADR-0011** DESCRIBES **Surface routing directive and echo audit**
**comlab/schemas/response.py** IMPLEMENTS **ADR-0011**
