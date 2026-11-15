# REVIEW T-AUD-22d — ACCEPT, score 96 (Windows Cowork, 2026-11-15)

Run: Hydrogen lane (gemini-4-hydrogen-high), 7 min agy wall time (19:19-19:26 CET); fence check PASS; promoted
76c6c21 on fix/T-AUD-22d. Docs row: no second-model review (CLAUDE.md step 6).

## Facts re-derived by Cowork (in the worktree, before promote)
- Step 1: `CLAIMS OK group=comlab scope=labs/comlab/comlab/config/global_fault_registry.json candidates 303 covered claims 1025`; classes ANALYSER_SPEC=28 DIAGNOSTIC_THRESHOLD=370 INTERNAL_PARAMETER=448 NON_DOMAIN=140 PHYSICAL_CONSTANT=7 TYPICAL_RANGE=32; suspect 46 same_as_wiki 27 (whole register).
- Step 2: `knobs 208 internal 208`. Step 3: rules scope `CLAIMS OK ... candidates 357 covered claims 1025`; `*.py` scope OK; gaslab group OK.
- Step 4: `0` removed lines; rows CK0693-CK1026 appended (334).
- Spot checks against the source: CK0693/CK0694 (manifold_vacuum_kpa 30/50, :20-21), CK0714 (o2_b1s2_v 0.4, :184),
  CK0757 (ect_c > 90.0, :603), CK0770 (map_kpa < 30.0, :700), CK0695/CK0880/CK0990 knobs: values and conditions
  match the lines.

## Findings
- 12 new suspect claims (listed in the note and RESULT) are registry thresholds that differ from the vocabulary, the
  wiki register or the registry rules (post-cat O2 0.4-0.5 V on a dead catalyst; ect_c > 90 vs MW-003 > 95; MAP < 30
  kPa on low compression; HC 1000-3000 vs wiki 400-1200; CO2 3-6 vs the 5-8 % cranking band; stuck-rich 0.7 vs
  0.85 V; O2 switching 0.5/0.25 Hz vs 2-5 Hz). They go to the verification rows, as R6 requires; no edit here.
- Score: -4 for the RESULT omitting the branch/log paste (the lane prompt told it to skip it; recorded, not charged
  to the implementer beyond the format).

Verdict: ACCEPT.
