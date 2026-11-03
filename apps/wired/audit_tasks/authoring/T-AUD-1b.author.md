# T-AUD-1b — authoring sidecar (Windows Cowork, 2026-11-03)

### Verified context ###
1. **Findings re-read:** `repo/audit/FINDINGS.md:194-198` (F-P5-1 MEDIUM, F-P5-2 MEDIUM, F-P5-4 LOW, F-P1-1 = F-P5-4).
2. **PyPI (P1):** `dnalab` 200 (taken), `comlab` 404, `fourdapp-comlab` 404, `fourdapp-wired` 404, `4dapp-comlab` 404.
3. **Resolution (P2):** fresh `py -3.14` venv, `pip install --dry-run --report -r requirements.txt` on `78a48b6`: 55
   entries, 47 third-party, 38.7 s. Render (P5 `surface.json` `render_dists`, 57) adds `pip` and `six` only (P3).
4. **Imports (P5):** only dnalab imports other labs (symptomlab, vinlab); wired imports all seven.
5. **Readers of dist names:** none in product code (`importlib.metadata`/`pkg_resources` only in `audit/scratch/`).
6. **Tree hygiene:** `./labs/dnalab` dry-run writes only ignored paths (`dnalab.egg-info/`, `__pycache__/`).
7. **Baselines (P4) on `78a48b6`:** wired `36 passed`, ui `30 passed`, the 2 deploy probes `2 passed`; tree clean.

### Rulings and the tradeoff that lost ###
- Rename dists `fourdapp-*` (R1). Lost: drop inter-lab deps from wired (F-P5-4 stays open, and a missing `-e` line
  becomes a late ImportError instead of a resolve error).
- Constraints from the Windows report plus `six==1.17.0` (R3). Lost: a Linux-generated lock (no Linux host in this loop).
- Plan NONE. Lost: a plan gate (it would review a restatement of R1-R3; the open risk, the Render build, is unmeasurable
  here). The operator's merge to `main` is the deploy gate.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | DEFERRED | the venv is the row's R3.1 |
| step 2 | DEFERRED | needs R1-R3; the base resolves (P2) |
| step 3 | DEFERRED | needs R1-R2; on the base the dnalab dry-run exits 0 (the defect) |
| step 4 | REHEARSED | base `36 passed`; +5 R4 tests = 41 |
| step 5 | REHEARSED | base `30 passed` |
| step 6 | REHEARSED | base `2 passed` |
| step 7 | DEFERRED | the test file does not exist yet |

### Exclusivity ###
No other implementer runs. `fix/T-AUD-1b` is cut from `fix/T-AUD-1c` (`78a48b6`).

### Progress hook ###
T-AUD-1b: a requirements file missing one `-e` line fails to resolve; the closure installs at the pins; 41 passed.

### Cold read ###
own pass 2026-11-03: literals ok (FINDINGS lines 194-198, the 8 manifests, `78a48b6`) · counts: 5 tests, 36+5 = 41 ·
traceability: criteria 1-5 → steps 1-7; every CREATE/MODIFY → a deliverable · JUDGEMENT criteria: 0.
cold read 2026-11-03 FOCUSED reader; trigger grep hit (rulings); 1 finding, 1 patched, 0 not-a-conflict — 3 calls.
Finding: the rename-back mutant fails 2 tests, not 3 (`test_no_bare_lab_dependency` reads dependencies, not names);
R4 now names the 2. Unsettled note settled: `requirements.txt` `-e` lines are `-e labs/<x>` and `-e apps/wired`, so
step 3's `sed 's#-e #-e C:/4DApp/repo/#'` makes them absolute.

### Correction history ###
- **01 (2026-11-03, hand-back B3 after round 1).** f1 UNSATISFIABLE (soft): step 3 ran in the venv step 2 had just
  filled, so `fourdapp-*` resolved locally and both dry-runs exited 0. UPHELD, owner COWORK (my verification design;
  the rehearsal ran step 3's dnalab dry-run in a venv with nothing installed). The implementer's venv2 reading
  settles it: exit 1, `No matching distribution found for fourdapp-dnalab`. f2 CONTRADICTION (hard): the commit was
  refused. Re-derived from the implementer transcript: the refused text was `git add … && git -c user.name=Claude …
  commit -m "…\n\nCo-Authored-By: Claude …"; git log …`. bash_guard bisect: the commit alone ADMITTED; `git add … &&`
  + commit with the trailer REFUSED. A compliant form exists, but `AGENTS.md` § git never said to run the commit as
  its own command: UPHELD, owner COWORK (contract gap; the B1 class recurs). Corrections: step 3 uses venv2; round 2
  makes the commit as its own command; `AGENTS.md` § git gains that rule (split form re-checked: both ADMITTED).
