# GASLab source audit register (T-GASA-WIKIAUDIT)

Operator order 2026-11-13: every domain number in the GASLab wiki (`labs/gaslab/wiki/`), `docs/GAS_VOCABULARY.md`
and `gaslab/data/gas_lab_ontology.yaml` is unverified until a primary source confirms it. This folder is the register.

| file | written by | content |
|---|---|---|
| `extract_candidates.py` | Cowork | Writes `candidates.csv`: one row per digit-bearing line of the audited files. |
| `candidates.csv` | the script | `cand_id, file, line, sha, auto, text`. `auto=NON_DOMAIN` marks a line whose digits are all section numbers, ids, dates, versions or anchors. |
| `check_claims.py` | Cowork | Checks `claims.csv`: coverage, line identity, class, required fields, values present in the line. |
| `claims.csv` | inventory rows (T-GASA-15 wiki, T-GASA-16 vocab + ontology) | One row per claim. |
| `sources.csv`, `verdicts.csv` | verification rows (later) | One row per source; one verdict per claim. |

## claims.csv

Header, exactly: `claim_id,cand_id,file,line,quantity,value,unit,condition,class,same_as,suspect`

- **One claim = one number (or one range) for one quantity under one condition.** A table row with three numbers is
  three claims. A line can hold several claims; each needs its own row.
- `claim_id`: `W` + four digits, unique, in file order (`W0001` …).
- `cand_id`, `file`, `line`: copied from `candidates.csv`.
- `quantity`: what is measured, in a few words: `CO tailpipe`, `HC ceiling`, `lambda window`, `CO2 peak`.
- `value`: the number as written, with its comparator or range: `≤ 35`, `0.1 – 0.45`, `~15.5`, `> 2000`. Every number
  in `value` must appear in the line text (the checker enforces this).
- `unit`: `ppm`, `% vol`, `rpm`, `kPa`, `°C`, `µm`, `-` (dimensionless), …
- `condition`: the state the value applies to: `idle, warm, working cat`; `2500 rpm`; `pre-cat`; `any`.
- `class`: one of
  - `LEGAL_LIMIT`: a statutory or test-scheme pass/fail limit (MOT, EU directive, EPA, UNECE).
  - `PHYSICAL_CONSTANT`: chemistry or physics fact (stoichiometric AFR, CO2 maximum, formula constants, absorption
    wavelengths of a molecule).
  - `ANALYSER_SPEC`: instrument fact (sensor type, accuracy class, response time, OIML/ISO class limits).
  - `TYPICAL_RANGE`: the normal value of a healthy engine or system under a stated condition.
  - `DIAGNOSTIC_THRESHOLD`: a cut-off or band that names a fault or a severity.
  - `RULE_OF_THUMB`: an approximate relation stated as a heuristic (`1 % wasted fuel ≈ 200 ppm HC`).
  - `INTERNAL_PARAMETER`: a GASLab design value with no outside truth (confidence weights, scores, caps, counts of
    rules).
  - `NON_DOMAIN`: the line holds no domain number (a section number, an example index, a count of files). One
    `NON_DOMAIN` row covers the whole line; leave `quantity` … `condition` empty.
- `same_as`: the `claim_id` of an earlier claim that states the same quantity, condition and value elsewhere. Empty
  for the first statement.
- `suspect`: empty, or a short reason the value may be wrong: it contradicts another claim (name its `claim_id`), or it
  contradicts what you know (state what you know). The verification rows check suspect claims first.

## sources.csv, verdicts.csv, sources/ (verification rows)

`check_verdicts.py --scope scope/<ROW>.txt` checks them. A row's scope file lists root claims (claims with no
`same_as`); a linked claim takes its root's verdict.

`sources.csv` header: `source_id,url,title,publisher,kind,fetched_file,fetched_date`
- `source_id` `S` + three digits; `fetched_file` `sources/S<NNN>.md`, the firecrawl output, committed;
  `fetched_date` ISO date.
- `kind`: `PRIMARY_LAW` (statute, directive, regulation), `PRIMARY_REGULATOR` (DVSA, EPA, a ministry's own manual),
  `PRIMARY_STANDARD` (SAE, ISO, OIML, UNECE text), `OEM`, `TRADE` (analyser maker, trade training), `ACADEMIC`,
  `SECONDARY`. A `LEGAL_LIMIT` claim is CONFIRMED or CONTRADICTED only by a `PRIMARY_*` source.

`verdicts.csv` header: `claim_id,verdict,source_id,quote,source_value,note`
- `verdict`:
  - `CONFIRMED`: the source states the same value for the same quantity and condition.
  - `CONTRADICTED`: the source gives a different value for the same quantity and condition (or, for a "normal" range,
    a legal limit that the range exceeds).
  - `PARTLY`: the value is right but its condition or attribution is wrong (an MOT limit labelled a Euro
    type-approval limit), or only one end of a range holds.
  - `CITATION_WRONG`: the source the claim cites does not say it.
  - `UNSOURCED`: no source found; `note` names the searches made.
- `quote`: words copied from the fetched file, at least 12 characters; the checker finds them there.
- `source_value`: what the source says, required for CONTRADICTED, PARTLY and CITATION_WRONG.
