# Code-literal audit register (T-AUD-22)

Operator order 2026-11-13: every domain-valued literal in production code, and in the data files the code loads, is
unverified until a primary source confirms it. Companion of the GASLab wiki register
(`labs/gaslab/audit_tasks/wikiaudit/`, T-GASA-WIKIAUDIT); the verification rows check both against one source list.

| file | written by | content |
|---|---|---|
| `extract_code_candidates.py` | Cowork | `--group gaslab|comlab|rest` writes `candidates_<group>.csv`: one row per source line holding a numeric literal. |
| `candidates_<group>.csv` | the script | `cand_id, file, line, sha, auto, text`; `auto=NON_DOMAIN` for trivial literals (-1, 0, 1, 2), indices, `range`/`round` arguments. |
| `check_code_claims.py` | Cowork | Checks `claims_<group>.csv`: coverage, line identity, class, fields, values in the line, `same_as`, encoding. |
| `claims_<group>.csv` | inventory rows (T-AUD-22a gaslab, later comlab, rest) | One row per claim. |

Groups: `gaslab` = `labs/gaslab/gaslab/*.py` (the ontology is in the wiki register); `comlab` = COMLab code, config
and registry rules; `rest` = OBDLab, DTCLab, DNALab, SymptomLab, `apps/wired`, `apps/ui`. VINLab is out (VIN work
parked, operator 2026-11-07).

## claims_<group>.csv

Header, exactly: `claim_id,cand_id,file,line,quantity,value,unit,condition,class,citation,same_as,suspect`

The fields and the eight classes are those of `labs/gaslab/audit_tasks/wikiaudit/README.md` § claims.csv, with:
- `claim_id`: `GK` (gaslab), `CK` (comlab) or `RK` (rest) + four digits, unique, in candidates order.
- `citation`: the source the code names for the literal (a `# wiki: GASWIKI-02 §2.8` comment, a docstring reference,
  a constant's name that points to a document), as written. Empty when the code names none.
- `same_as`: a wiki-register claim (`W0001`-`W1693`) or an earlier claim of the same group that states the same
  quantity, condition and value. A code value that differs from the claim its citation names gets no `same_as` and a
  `suspect` text naming that claim.
- `value`: as written in the code (`0.45`, `250`, `1.03`); every number must appear in the line.
