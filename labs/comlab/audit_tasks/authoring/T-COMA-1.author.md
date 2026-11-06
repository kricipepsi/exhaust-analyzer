# T-COMA-1 — authoring sidecar (Windows Cowork, 2026-11-06)

Design input: `T-COMA-1.design.md` (same folder). Scripts and dumps: `C:/4DApp/recheck/T-COMA-1/`.

### Verified context ###
1. **F-C1-7 holds** on the spec base: 15 non-starter probes take their verdict from the idle gas (P1); the audit probe
   fails (P7). Observed.
2. **NS-001..003 are unreachable today** (P2): GASLab returns `SAMPLE_INVALID` for every cranking sample, so the
   shim's `chemistry_state` is None and the three chemistry-gated rules are pruned (`ns_prune.py`). Only NS-004 can
   score, for `case_006` (P0230). Observed. This made the design note's reason for B ("cranking chemistry is real
   evidence") void for the current pipeline; B still wins (rulings below).
3. **Option A alone does not fix the defect**: `recheck/T-AUD-4e1/rehearse.py` (gas excluded, no family gate) moves the
   non-starters to `misfire` MF-005 and `sensor_fault` SF-00x. Every variant needs the family gate. Observed.
4. **Gate without an abstain is worse**: `rehearse_b.py` (family gate only) gives `OPTIMAL_HEALTH` "no fault" for 4 of
   5 corpus non-starters. Hence R2. Observed.
5. **Rehearsal of R1-R4** (`apply_fix.py`, restored): P3, P4, P5 and P7 hold; comlab 531 → 530 + 1 failed (the
   `case_014_gas_dominant` golden, R5); wired 65 → 79 with the new file; registry and ui unchanged. Observed.
6. Corpus labels for the 5 `will_not_start` cases: 4 are `non_starter`; REAL-002 is `lean_condition`, a running-engine
   label on a non-starter (a label question for T-COMA-3). Base family hits 0/4; fix 4/4. Observed.

### Rulings and the tradeoff that lost ###
- **B (family gate), not A (wiki literal).** Both need the gate (fact 3). B keeps the gas, OBD and DTC data as
  evidence for `non_starter` rules, so a later GASLab fix (T-COMA-3) makes NS-001..003 reachable without a COMLab
  change. Lost: the wiki line "excludes its data from the matrix", amended in this row (R7).
- **No-rule outcome: an abstained `non_starter` verdict (`NS-NO-RULE`, reason `no_rule`)**, not "no fault" (false for
  an engine that does not start) and not the `floor` reason (the UI would say "candidates are below floor" with no
  candidate). Lost: no schema change (one Literal value added; the UI branch is its only reader).
- **Split.** Gas optional for a non-starter (the T-AUD-4e residual) moves to T-COMA-2: it touches the inbound schema,
  the composition abort and the aggregator's gas reads, and depends on this gate. GASLab's cranking validity and the
  NS-004 DTC list go to T-COMA-3. Lost: one row closing F-C1-7 and the residual together.
- Plan REQUIRED, difficulty 4 (`--effort high`): a new verdict path on the production router. Code row, so a second
  review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | SIMULATED | `apply_fix.py` + the test file: `14 passed`; comlab `1 failed, 530 passed, 4 skipped, 2 errors` before R5 (the failure is `case_014_gas_dominant`, which R5 rewrites: SF-001 → NS-NO-RULE, family non_starter); base `13 failed, 1 passed` |
| step 2 | SIMULATED | registry `5 failed, 502 passed, 4 deselected` (= base); wired 65 + 14 = 79; ui `38 passed` (= base) |
| step 3 | SIMULATED | `probe.py`: 15 probe lines with `NS-NO-RULE', True, True, 'no_rule', 0.0`; corpus diff exactly the 5 `will_not_start` ids; `git status --porcelain` empty after restore |
| step 4 | SIMULATED | base `1 failed, 10 deselected`; fix `1 passed, 10 deselected` |
| step 5 | SIMULATED | ruff `All checks passed!` on the three source files and the test file |
| step 6 | DEFERRED | the observable: the spec commit then the implementer's commits on `fix/T-COMA-1`; status lists only the note and the RESULT |

### Exclusivity ###
No other implementer runs. T-COMA-2 (gas optional) follows and builds on this branch.

### Progress hook ###
T-COMA-1: a non-starter is decided by the non_starter family only; no matching rule gives the NS-NO-RULE abstain.

### Cold read ###
own pass 2026-11-06: P1-P7 measured on the spec base · literals found once (`def _translate_to_output(`,
`    abstain_reason: Optional[Literal["floor", "margin"]] = None`, `Suppression skips that lab's fatal gates and excludes
its data from the matrix`, the probe name, the reason caption line) · counts: wired 65 + 14 = 79; comlab 531 − 1 + 1 =
531 · `def route_case_with_diagnostics` occurs twice (class method and module function; the spec names
`RegistryV2Router.route_case_with_diagnostics`) · 1c: "only" in Goal, R1 and Context names one set (the
`non_starter` family; defined by `FaultFamily.NON_STARTER`) · traceability: criteria 1-5 → steps 1-6 · 1 finding
patched (criterion 1 said "R6 mutant"; the mutants are P5's). cold read 2026-11-06: skipped, plan-gated.

### Correction history ###
- 2026-11-06 plan correction 01 (`corrections/T-COMA-1_plan_correction_20261106.md`): plan approved with K1-K4 (R8): no py_compile; isolation by identity; R2 output recorded; the UI info line for no_rule. Second review (codex) 6 findings: 1, 2 upheld, 4 in part, 3, 5, 6 not upheld.
