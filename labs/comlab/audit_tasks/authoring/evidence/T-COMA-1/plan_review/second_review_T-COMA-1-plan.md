The core design follows R1–R7, and C1–C8 introduce no clear semantic contradiction. The plan needs corrections to its write behavior and validation gates before implementation.

1. **BLOCKER — `py_compile` writes outside the authorised paths.**  
   The plan lists “`$PY -m py_compile`” under an inner loop that “Writes nothing.” Explicit compilation creates `.pyc` files under `__pycache__`; `PYTHONDONTWRITEBYTECODE` does not suppress explicit `py_compile` output. Those paths are absent from “`### Files to touch ###`.” Replace this with in-memory compilation, or omit it and use the permitted checks. This is a concrete scope violation, not merely inaccurate documentation.

2. **CONCERN — The isolation gate can falsely pass a new violation.**  
   The plan accepts “`$PY audit/tools/isolation.py` (`violations: 4` or fewer).” A new violation could replace a resolved baseline violation while the count remains four. Compare violation identities against the baseline and reject additions; a count ceiling alone does not establish that the “COMLab import firewall” required by R1 remains intact.

3. **CONCERN — The final verification procedure is not reviewable from this submission.**  
   The plan promises “`### Verification ###` steps 1-6 as written,” but the embedded task contains no such section. Likewise, it refers to “the JSON compare in Verification step 3” without supplying that command. The success criteria provide expected results, but not the referenced procedure. Include the actual commands and comparison predicates in the plan. In particular, P4 requires all six recorded fields of the 309 running cases to remain unchanged and the five non-starter cases to match their specified outcomes—not merely the expected number of changed cases.

4. **CONCERN — R2’s complete output contract needs an explicit check.**  
   R2 mandates, among other fields, “`severity_level` `WARNING_DEGRADED_PERFORMANCE`,” “`processing_confidence_rating` `DEGRADED_ASSURANCE`,” and aliases that “follow the verdict.” The plan’s C2 explicitly covers enrichment, while its decisive checks emphasise family, code, abstention and confidence. The embedded material does not establish that those checks cover the remaining R2 fields. Add a direct assertion or recorded output comparison for the complete no-rule output, including aliases, headline and remediation. This need not change the prescribed R6 file.

5. **CONCERN — R4 has no behavioral verification.**  
   The plan explicitly says, “No test exercises the R4 caption,” relying on “the ui suite (`38 passed`) and the diff review.” That suite can pass with the caption absent or the wrong branch selected. R4 requires the exact text “Reason: no non-start rule matches the inputs,” while “floor and margin keep their text.” Exercise those three branches through the UI workflow and record the displayed captions.

6. **NIT — “Cranking” is an ambiguous boundary label.**  
   The boundary list says “`suppress_gaslab False` (running, cranking): gate False.” But P3 requires NS-NO-RULE for “all 15 probes,” which include “both cranking samples” under `will_not_start`. Clarify that gate selection follows the routing directive, independently of gas-sample type. A cranking sample in a `will_not_start` session remains gated.

The remaining choices are sound: C1 preserves R1’s literal telemetry values; C2 preserves the specified enrichment; C3 exposes the public constant; C4 checks exactly the code R3 names; C5 respects R4’s caption scope; C6 follows R6; C7 restores mutants before final validation; and C8 preserves R7’s wording.

The absent directive, plain-dictionary directive, matching NS-004 rule, empty candidate set and excluded v1 path are handled consistently with the rulings. In particular, the dictionary behavior follows R1’s mandated `getattr`, and the code-first `no_rule` branch correctly bypasses floor and margin checks.

VERDICT: PROCEED WITH CORRECTIONS

<!-- Cowork 2026-11-06: codex verdict "PROCEED WITH CORRECTIONS" (prompt wording); filed in the approved-verb vocabulary. Rulings: corrections/T-COMA-1_plan_correction_20261106.md -->
APPROVE WITH CORRECTIONS
