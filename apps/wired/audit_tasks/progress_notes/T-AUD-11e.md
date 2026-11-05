# Progress note — T-AUD-11e (GASLab drift report)

## Readiness challenge
- (a) Starting state matches the task. `git branch --show-current` printed `fix/T-AUD-11e`. `git log --oneline -1` printed `49ab697 spec(T-AUD-11e): GASLab EGM drift report`, a descendant of `ecf3c75`. `git status --porcelain` printed nothing. Base = `49ab697`.
- (b) The gate fails for the intended reason. Step 1 on the missing report raises `FileNotFoundError: audit\drift\2026-11-05_DRIFT_REPORT_gaslab.md` (exit 1). The Preconditions command printed `checked` with no `MISSING` or `EXISTS` line.
- (c) Decisive expected values, derived from the code before the report existed: `grep -c "signature_type: catch_all" gas_lab_ontology.yaml` -> 4 (the docs say 3). `GasLabPayload` has 15 annotated fields (the docs say 9). The checker must print `sections 8/8` and `refs ok N/N` with N equal.
- (d) No contradiction or missing decision prevents implementation. The task writes one new file under `audit/drift/` and `Files to touch` lists it.
- (e) Teach-back: the deliverable is one drift report, `audit/drift/2026-11-05_DRIFT_REPORT_gaslab.md`, with one section for each of the 8 GASLab documents and one quoted finding for each doc-versus-code difference. The decisive check is step 1, `check_report.py`, which must print `REPORT OK` with `refs ok N/N`.

## Result of the check
- Step 1 after the commit: `sections 8/8, findings 47, refs ok 80/80` / `REPORT OK`, exit 0.
- The 14 `Code: ABSENT` commands were re-run one by one. Each printed the output written in the report.
- Findings by document: README 1, PRD 4, HLD 7, LLD 4, DLD 4, BDD 1, GAS_VOCABULARY 19, ADR 7.
- Findings by class: DIVERGENCE 23, MISSING 10, MODEL 10, HARDCODED 3, UNDOCUMENTED 1.

## Assumptions worked past
- The README `Boundary` line is reported as drift because `apps/wired/wired/composition.py` imports `gaslab` types directly. The R1 exception for a call into another lab does not cover this: the line claims a local mirror.
- HLD:37 (COMLab builds `GasLabDnaView`) is reported although the caller is `apps/wired`, not a lab. The line names COMLab as the actor.
- Not reported (doubtful, R4):
  - `Hcv` described in LLD:62 as an override. DLD:143 and the code docstring both say reserved and unused.
  - `family_map.SIGNATURE_TO_FAMILY` described in DLD:70 and DLD:252 as not used by classification. `ranking.classify_top3` uses it, but the documents say "not by `process()`", which is true.
  - The `validity_gates` keys in the YAML are loaded and validated but never read. HLD:67-71 lists them as loaded, which is true.
  - `engine_state` `REGULATORY_HIGH_IDLE` routes WORN_PISTON_RINGS from one reading through `_append_rpm_routes` (resolution.py:570). HLD:176 and HLD:212 say high-idle enters through `reading_high`. LLD:238 documents the route, so I did not report it.
  - `fuel_delivery_type` default `PORT_INJECTION` in composition.py:416 against the documented `GDI` / `NON_GDI` (DLD:177). The value set that the VIN lab emits is outside P2, so I could not settle it.
  - ADR-0010 calls the 0.005 half-width a single constant. The code uses the literal twice (rule_engine.py:135-136).
  - The YAML header comment says 32 faults. HLD:211 and DLD:259 already record that.
- `bash_guard` refused the commit command while the `Co-Authored-By` trailer was in the message. The commit has no trailer (same as T-AUD-11d). No guard was bypassed.
- The ontology tier citations in YAML comments (for example `real_combustion_fault`, `minor_inefficiency`) differ from GAS_VOCABULARY §10 for several faults. I reported only the clearest case (NOx `high_combustion_temp`, 1000 against 1500). Cowork can decide whether the other loose citations need their own rows.

## Time
phase | start | end | minutes | context at end
- First action, read, report, commit | 2026-11-05T21:04:12Z | 2026-11-05T21:11:42Z | 7 | ABSENT

## VERIFICATION GATE
- Step 1: `REPORT OK` (see above). Step 2: `audit/drift/2026-11-05_DRIFT_REPORT_gaslab.md` only. Step 3: `499714a`, `49ab697`; `git status --porcelain` shows this note only, until the RESULT is written.

## CODE REVIEW
- The row writes one Markdown report. No `.py`, document, test or data file changed. `ruff` and `pyright`: NOT RUN (no Python file touched).
