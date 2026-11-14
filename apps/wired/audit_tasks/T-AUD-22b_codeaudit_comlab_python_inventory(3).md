### Routing ###
`audit`, row T-AUD-22b (T-AUD-22, second slice: the numeric literals of COMLab's Python code; operator order
2026-11-13). Docs row in the app clone `C:/4DApp/repo`, on branch `fix/T-AUD-22b` (built on the accepted
`fix/T-GASA-18`, `3fa251f`, which holds both registers this row links to).
- **Test length: 1/5.** One checker run, under 10 s.
- **Runs real compute: NO.**
- **Expected wall-clock: 30 min.** Stop rule: at 90 min, finish the current file, commit, write `## Time` and a partial
  RESULT that names the first candidate not done, then stop.
- **Plan: NONE.** The register format and its checker are fixed (`codeaudit/README.md`, `check_code_claims.py`).
- **Overnight:** no.

### Goal ###
Every numeric literal in the `.py` files of the COMLab group (`labs/comlab/comlab/**/*.py`,
`labs/comlab/registry/**/*.py`) that carries a domain value is listed in
`apps/wired/audit_tasks/codeaudit/claims_comlab.csv` as a classified claim with the citation the code gives, checked
against the document that citation names, and linked by `same_as` to a GASLab wiki-register claim where one states the
same value. This row lists and classifies; it verifies nothing on the web. Done is
`check_code_claims.py --group comlab --files '*.py'` printing `CLAIMS OK` (step 1).

### Pinned values ###
| id | value | population | command |
|---|---|---|---|
| P1 | `files 52 candidates 3794 auto_non_domain 1220 to_classify 2574` | the COMLab group on the spec commit | `extract_code_candidates.py --group comlab` |
| P1b | `293` non-auto candidates in `.py` files | `candidates_comlab.csv` on the spec commit | `check_code_claims.py --group comlab --files '*.py'` on a header-only file (P2) |
| P2 | header-only `claims_comlab.csv`: `CLAIMS FAIL 293 error(s)` (all `uncovered`) | Cowork's rehearsal | step 1 |

`$PY` is `C:/4DApp/.venv/Scripts/python.exe`. `extract_code_candidates.py`, `check_code_claims.py`,
`candidates_comlab.csv` and `README.md` in `apps/wired/audit_tasks/codeaudit/`, and everything in
`labs/gaslab/audit_tasks/wikiaudit/`, are Cowork's: read them, do not edit them. The wiki register's own checker
prints `drift` errors on this commit (T-GASA-18 moved lines; re-key row T-AUD-22-RESYNC): the `W` ids and their
values are unchanged, and this row does not run that checker.

### Rulings that bind ###
- **R1** The register format is `codeaudit/README.md` § claims_<group>.csv, which points to the wiki register README
  for the fields and classes. Read both before the first row.
- **R2** Scope is the non-auto rows of `candidates_comlab.csv` whose `file` ends in `.py` (P1b). Each needs at
  least one row in `claims_comlab.csv`: a classified claim, or one `NON_DOMAIN` row (a loop bound, a format width, a
  default of 0.0, a list length). `claim_id`s run `CK0001` upward in candidates order. The data-file rows (`.json`,
  `.yaml`) are later slices: list none of them.
- **R3** `citation` is the reference the code gives for the literal: the comment on its line, the comment block or
  docstring it sits under, or a constant name that names a document. Copy it as written; empty when none.
- **R4** When the citation names a document in the clone (search `labs/` and `Vault/` by file name, for example
  `Vault/labs/obdlab/wiki/delta-relations/07_gas-transition-matrix-2speed.md`), open it at the cited section. If the
  code value differs from the value the document or the citing comment itself states, the claim gets a `suspect` text
  naming the document and its value. If the document is not found, `suspect` stays empty and the claim is counted in
  the note as "citation not found".
- **R5** `same_as` names a GASLab wiki-register claim (`W0001`-`W1693`) only when that claim states the same quantity,
  condition and value; otherwise an earlier `CK` claim of this file that states the same; otherwise empty.
- **R6** `suspect` is also required on every claim that contradicts your own knowledge (a physical or legal value you
  know to be different), with the reason. Known one: `_FLATCAM_ELEV_O2_MIN = 2.0` at candidate `K0012`
  (`delta_engine.py:178`): its own comment and delta-relations/07 give O2 2.5 (step 2).
- **R7** `claims_comlab.csv` is UTF-8 as written in the source; the checker rejects double-encoded fields. No web
  access in this row.

### First action ###
```bash
cd C:/4DApp/repo && git branch --show-current && git log --oneline fix/T-GASA-18..HEAD && git status --porcelain && cd apps/wired/audit_tasks/codeaudit && C:/4DApp/.venv/Scripts/python.exe -I extract_code_candidates.py --group comlab && git status --porcelain .
```
```
fix/T-AUD-22b
<Cowork's spec(T-AUD-22b) commit>
files 52 candidates 3794 auto_non_domain 1220 to_classify 2574
```
Both `git status --porcelain` runs print nothing: the script re-writes `candidates_comlab.csv` byte-identical.
Anything else is a stop.

### Success criteria ###
1. Step 1 prints `CLAIMS OK group=comlab scope=*.py candidates <P1b>` and no `ERROR` line.
2. Step 2 prints `seeds flagged 1 of 1`.
3. The note discloses the step 1 `classes`, `suspect` and `same_as_wiki` figures, the count of claims with an empty
   `citation`, the count of "citation not found", and lists every `suspect` claim with its reason.
4. One new commit on `fix/T-AUD-22b` after the spec commit that adds `claims_comlab.csv` and nothing else.

### Context ###
- The operator found the GASLab wiki's CO 0.45 % "normal" above the legal limit and that the same number was
  hard-coded. A code literal that differs from the document it cites is a finding even when neither is verified yet.
- T-AUD-22a classified the 188 GASLab code literals (`claims_gaslab.csv`). COMLab's P1 lines split by file kind:
  this row is the Python code; the registry rules, the KG and fault-registry JSON, and the config YAML follow.

### Preconditions ###
```bash
cd C:/4DApp/repo && for p in apps/wired/audit_tasks/codeaudit/README.md apps/wired/audit_tasks/codeaudit/check_code_claims.py apps/wired/audit_tasks/codeaudit/candidates_comlab.csv labs/gaslab/audit_tasks/wikiaudit/README.md labs/gaslab/audit_tasks/wikiaudit/claims.csv labs/comlab/comlab/analytics/delta_engine.py Vault/labs/obdlab/wiki/delta-relations/07_gas-transition-matrix-2speed.md; do test -f "$p" || echo "MISSING $p"; done; echo checked
```
Expected: `checked`, and no `MISSING` line.

### Deliverables ###
1. `repo/apps/wired/audit_tasks/codeaudit/claims_comlab.csv`, committed on `fix/T-AUD-22b`.
2. `repo/apps/wired/audit_tasks/progress_notes/T-AUD-22b.md`.
3. `repo/apps/wired/audit_tasks/results/RESULT_T-AUD-22b.md`.

### Files to touch ###
- `repo/apps/wired/audit_tasks/codeaudit/claims_comlab.csv` (CREATE: R1-R7)
- `repo/apps/wired/audit_tasks/progress_notes/T-AUD-22b.md` (CREATE)
- `repo/apps/wired/audit_tasks/results/RESULT_T-AUD-22b.md` (CREATE)
- `repo/apps/wired/audit_tasks/codeaudit/candidates_comlab.csv` (RUNTIME: re-written byte-identical by the first action)

### Out of scope ###
- Editing any code, config, wiki or vocabulary value, even a suspect one: the verification rows decide, then fix rows
  edit.
- The COMLab data files (`.json`, `.yaml`): later T-AUD-22 slices. The GASLab group: `claims_gaslab.csv` stays as it is.
- Web lookups (R7). Pushing: Cowork pushes after acceptance.

### Verification ###
In-scope gates (blocking). Run from `C:/4DApp/repo` in Git Bash.
```bash
cd C:/4DApp/repo/apps/wired/audit_tasks/codeaudit
PY=C:/4DApp/.venv/Scripts/python.exe
# 1.
timeout 60 $PY -I check_code_claims.py --group comlab --files '*.py' | tail -4
# 2.
timeout 60 $PY -I -c "import csv; r=list(csv.DictReader(open('claims_comlab.csv',encoding='utf-8'))); s={'K0012':'2.0'}; f={x['cand_id'] for x in r if x['cand_id'] in s and x['suspect'].strip() and s[x['cand_id']] in x['value']}; print(f'seeds flagged {len(f)} of 1')"
# 3.
cd C:/4DApp/repo && git log --oneline fix/T-GASA-18..HEAD && git diff --stat HEAD~1 HEAD | tail -1 && git status --porcelain
```
Expected:
- step 1: a `classes …` line, `suspect N same_as_wiki M`, `CLAIMS OK group=comlab scope=*.py candidates <P1b> covered claims N`;
  no `ERROR`.
- step 2: `seeds flagged 1 of 1`.
- step 3: the spec commit and your one commit; `1 file changed`; only the note and the RESULT untracked.

Repo-wide gates: none (no code or test changes).
