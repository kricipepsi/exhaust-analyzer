
> **Context:** DTCLab PRD v2.0 (2026-06-11) · Module: DTCLab · Section: Section 8 — Release · Parent document: PRD_DTCLab.md
## Section 8 — Release

### v2 Scope

All P0 features above, including the Phase-2 scorer and the two cross-field coolant/fluid tags.

### Proposals (labelled — not shipped; consumer nameable)

### ID: **EP-DTC-NOSTART-1**
- **Proposal**: Surface Mode $06 monitor-aborted / Incomplete state (MID $A1 / TID $53) and freeze-frame fuel/spark-cut state for no-start diagnosis. CAN-era gated.
- **Named consumer + code path**: COMLab `T-COMV2-NOSTART-1` reads the new monitor state; extends `mode06_evaluator.py` + Mode-06 schemas. Registered by `T-OBDV2-5`; tracked as `T-DTCV2-NOSTART-1`.
- **Disposition**: **PROPOSAL** (ships with its consumer as a future task; not in current code)

Wiki `11_proposals_register.md` carries the broader DTCLab proposal slate (P-DTC-1 misfire
Type A/B severity, P-DTC-2 monitor-readiness trust gate, P-DTC-3 FMEM trust flag). Those remain
wiki-side proposals and do not ship here.

### Explicitly Deferred (v2 backlog)

- `dtc_severity_map.yaml` and severity-based DTC ranking.
- Manufacturer-specific Mode $06 MID overlays.
- `DTC_CONFIDENCE_WEIGHTS` wiki drift-guard test.



### Success Criteria

1. KR1–KR5 all pass in CI.
2. `test_dtclab_pipeline.py` passes its integration scenarios including catalyst/EGR DNA gate suppression.
3. `test_vocabulary.py` drift guard confirms the enum counts vs `DTC_VOCABULARY.md` (18-tag
   `DTCRoutingTag`).
4. `test_classify_top3.py` / `test_rank_candidates.py` confirm scorer ordering, clamp, and DNA factor.


## Graph relations (explicit)

**Section 8 — Release** DESCRIBES **DTCLab PRD v2.0**
**EP-DTC-NOSTART-1** PROPOSAL **T-COMV2-NOSTART-1** -- no-start diagnosis
**test_dtclab_pipeline.py** VERIFIES **v2 Scope**
**test_vocabulary.py** VERIFIES **v2 Scope**
**test_classify_top3.py** VERIFIES **v2 Scope**
