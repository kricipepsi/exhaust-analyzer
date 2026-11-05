# T-AUD-11g progress note

## Readiness challenge
(a) Starting state matches task: branch `fix/T-AUD-11g`, HEAD `8a81707` (spec commit, descendant of `d8dd7d4`, recorded as base), `git status --porcelain` empty. Preconditions printed `checked` only.
(b) The test fails for the intended reason: step 1 on the absent report raises `FileNotFoundError` for `audit/drift/2026-11-05_DRIFT_REPORT_comlab.md`. Cowork's good sample prints `sections 8/8, findings 1, refs ok 2/2` / `REPORT OK` (exit 0). The bad sample prints `REPORT BAD` (exit 1).
(c) Decisive expected value: `sections 8/8`, `refs ok N/N` with both N equal, `REPORT OK`. I derived N from the bullet count: 73 bullets, 53 with two refs and 20 `Code: ABSENT` bullets with one ref, so N = 53*2 + 20 = 126. The checker printed `refs ok 126/126`.
(d) No contradiction or missing decision prevents implementation.
(e) Teach-back: the deliverable is one drift report with 8 sections in P1 order, each finding quoting the document and the code. The decisive check is `check_report.py` printing `REPORT OK` with `sections 8/8` and equal `refs ok N/N`.

## Time
| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| first action to commit | 2026-11-05T21:23:45Z | 2026-11-05T21:36:25Z | 12.7 | ABSENT |

Minutes computed with a `datetime` one-liner. The stop rule (90 min) did not trigger.

## Method
- Read the 8 P1 documents in order. Read the P2 code that each claim names (aggregator, router, schemas, KG loader, symptom router, projection, config files, `apps/wired/wired/composition.py`).
- Built the report with a throwaway script under `C:/4DApp/recheck/T-AUD-11g-impl/` (`build.py`, `findings.py`). The script finds each line number from an anchor string, so no line number was typed by hand. The script is outside the clone and not a deliverable.
- Counts: 73 findings (37 DIVERGENCE, 23 MODEL, 12 MISSING, 1 UNDOCUMENTED). Per document: README 0, PRD 13, HLD 15, LLD 22, DLD 8, BDD 2, CROSS_LAB_DEPENDENCIES 6, SEMANTIC_CONTRACT 7 (sum 73).

## Assumptions worked past
- The LLD says its snippets are representative and that the code wins. I report a snippet only when it names a concrete value, class, method or field that the code contradicts or lacks.
- `labs/comlab/README.md`: no drift found. Its stage and status lines describe plans or history. `FU-1` and `cam_timing.json` exist (`config/kg/cam_timing.json`, 34-value `ChemicalSignature`).
- DLD `2.2` and `2.1` sizes: the DLD is a commitment document. I report the file-size lines because they state a measurable number that the files contradict. I do not report the "~120 rule rows" figure (the registry has 104 rows).
- `ERR-CONTRACT-001/002` mapping in `validate_payload` (LLD `10`, HLD `4.1`): the code embeds the codes in validator messages (`ingestion.py:322`, `:121`) but never wraps `ValidationError`. I treated this as partly met and left it out of the report.
- `PRD 6.2` `ERR-VIN-400` row: reported once, under the LLD row that names `validate_payload` as the raiser. VINLab owns VIN decoding, so the PRD row alone is a cross-lab claim.
- `SEMANTIC_CONTRACT.md` `12.1` names registry rule ids `MW-001`..`MW-009` on the live REG-V2 path (`labs/comlab/registry/`, outside P2). `config/global_fault_registry.json` holds `ERR-MW-001`..`ERR-MW-008` with other logic. Not reported: the claim concerns the v2 registry, not P2.
- `SEMANTIC_CONTRACT.md` `13` and the HLD/PRD scope lines ("Euro 6+ not represented in any schema"): `EuroEmissionCategory` holds `EURO_6` and `EURO_7`. Left out: the enum classifies the vehicle, and the out-of-scope items are GPF, LSPI and SAI technology.
- Claims about other labs (`DNALab_TO_COMLab_FLOW`, VINLab `VehicleDNA.md`, GASLab/OBDLab/DTCLab internals) are not settled by P2 code and are not reported.
- Doc line references that are approximate (`~L1845` for the `registry.integration_shim` import in HLD `8`; the code line is 1953) are not reported as drift. R1 treats a range that the value satisfies as no drift.
- CROSS_LAB_DEPENDENCIES status cells that say `pending` for a consumer the router now implements are reported as DIVERGENCE (DEP-2, 6, 8, 9). Rows that say only "consumer S4" (DEP-3, 11, 12, 13) are plans, so R4 says no drift.
- The commit trailer: `bash_guard` refused the commit text that held the word Claude in the trailer, so the commit has no `Co-Authored-By` line. `AGENTS.md` names this guard rule.

## VERIFICATION GATE
Run from `C:/4DApp/repo` after the commit (`e3d6a8f`), `PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1`.
- Step 1: `sections 8/8, findings 73, refs ok 126/126` / `REPORT OK`, exit 0. Previous decisive failure (`FileNotFoundError`, no report) is gone.
- Step 2: `git diff --name-only HEAD~1 HEAD` printed `audit/drift/2026-11-05_DRIFT_REPORT_comlab.md` only.
- Step 3: `git log --oneline -3` printed `e3d6a8f`, `8a81707`, `d8dd7d4`. `git status --porcelain` printed only the note (and, after this write, the RESULT).
- No test suite runs for this row. Verdict: CLEAN.

## CODE REVIEW
- Scope: the commit changes one file, the report. No document, code, test or data file changed (R3).
- Format (R2): 8 `## <path>` sections in P1 order, one bullet per finding on one line, a class tag from the five R1 classes, a Doc ref and a Code ref or `Code: ABSENT (command -> output)`. The checker confirms every quote occurs on its line.
- Quote check: no quote holds a `"` character. Several quotes are short (for example `0.5 }`, `0.1.0`) because the drifting value sits on a line with `"` characters. The sentence names the value.
- Risk: the 20 `ABSENT` claims state only what their command shows. Each command ran with no output. Commands use `grep` with BRE alternation `\|`.
- Risk: BDD and HLD claims about `SINGLE_POINT` and `GAS_DOMINANT` rest on reading `_map_degradation` and the REG-V2 shim (`registry/integration_shim.py:1194` reads `degradation_mode` from the sanitized payload). I did not run a session.
- Not run: no pytest, ruff or pyright (no `.py` file changed).
