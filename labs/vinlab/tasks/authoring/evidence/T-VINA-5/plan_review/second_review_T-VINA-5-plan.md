1. **HIGH — The merge knowingly selects wrong engines for real VINs.**  
   “Right brand wins” assigns `MB617912` diesel to `WDB12602212002803`, whose stated observed engine is `110987`. The plan identifies three other real counterexamples. Preserving resolution counts does not establish correct resolution, and copying a blank `majority_share` provides no ambiguity warning.

   **Fix:** adjudicate conflicting keys using independent engine evidence and record explicit winners. Check each exception across every WMI that reaches that key. If two VIN populations require different engines under the same brand/VDS key, establish whether a data-only solution can meet the goal; hand back that limitation before implementation.

2. **HIGH — The evidence cannot establish that “right wins” is generally superior.**  
   The plan admits that right-brand rows may derive from the same OPSI specimens used as the reference answers. Thus 89 matches versus 63 is potentially a comparison against training data. The size of the bias is unmeasured, so even the claim that the “real margin is smaller” assumes a positive margin that has not been established. Of 60 differing-key cases, the plan explains 29 right-only and four wrong-only matches, leaving 27 unclassified.

   **Fix:** trace provenance, separate independent references from overlapping specimens, and report the complete outcome table, including neither-match and unknown cases. Treat the current scores as descriptive agreement, not independent validation.

3. **HIGH — Tests and mutants protect coverage while allowing incorrect merge decisions.**  
   A mutant that selects the wrong engine at every conflicting key can still pass all make and engine-count tests. M6 tests missing rows, not collision precedence. The four acknowledged incorrect resolutions are therefore unprotected.

   **Fix:** add independently justified engine assertions for conflicting keys and mutants that reverse their winners. Also test the Mercedes folded-key collision path and ambiguity behavior for whichever winning rows are selected.

4. **MEDIUM — The corpus guard does not establish that it tests P3’s population.**  
   Repeating a regex over repository documents does not demonstrate identical file selection, deduplication, filtering, or VIN membership to `real_vins()`. Absolute floors can pass after a previously resolved VIN disappears if another specimen replaces it.

   **Fix:** establish exact corpus parity before editing, record membership and denominators, and retain per-VIN before/after resolution evidence. Use the permitted census Verification step for the authoritative population if maintaining a local equivalent is unreliable.

5. **MEDIUM — The source-note deliverable breaks R3.**  
   R3 requires a `# source:`-style note **in the ledger row** when fixing data directly. The plan instead puts a proposed note in RESULT and leaves the actual ledger update undone. The ledger is also outside the authorized write paths.

   **Fix:** resolve this specification conflict now: obtain an explicit ruling authorizing the ledger edit or assigning it to Cowork and accepting RESULT as the implementer’s handoff. Do not silently substitute one location for another.

6. **MEDIUM — The 5NM decision remains unsupported and unsettled.**  
   The plan proposes changing a sixth WMI using external assertions it expressly cannot check. Zero real 5NM specimens supplies no validation, and making the expected test value depend on approval merely tests the selected policy.

   **Fix:** settle the branch of the plan before approval. Either provide checkable evidence meeting R1 or retain 5NM unchanged and fix the predicted test counts accordingly. JSK/JSL and JN1’s country can remain follow-ups under the stated scope.

7. **MEDIUM — The mutation and commit sequence is internally inconsistent.**  
   Mutants supposedly run “after the fix commit,” but commits appear afterward. Restoring tracked files before committing would undo the implementation. The required empty status also conflicts with the already-written test and required progress note.

   **Fix:** specify one executable sequence: commit implementation paths before transient mutation, restore each mutant to those commits, and verify status against explicitly allowed note/result files. Complete that sequencing correction now.

RETHINK

Cowork (2026-11-04): the plan-review verdict RETHINK maps to loop_step.py CODEX_VERDICTS as (R2 redesigned to the Nio files-1+2 vote, correction 01):
REDESIGN
