# T-GASA-17 progress note — verify legal limits and CO 0.45 roots

## Readiness

- (a) Starting state matches: branch `fix/T-GASA-17`, `git log fix/T-AUD-22a..HEAD` = `527680e spec(T-GASA-17)`,
  `git status --porcelain` empty, step 1 tail `VERDICTS FAIL 20 error(s)` (P2). Preconditions print `checked`, no `MISSING`.
- (b) The gate fails for the intended reason: `sources.csv` and `verdicts.csv` hold only headers, so each of the 20
  scope claims gives `no verdict`.
- (c) Decisive expected value, derived independently: the scope file holds 20 ids (`wc -w scope/T-GASA-17.txt`), all
  roots in `claims.csv`; with one verdict each, the checker last line must be `VERDICTS OK scope=T-GASA-17.txt claims 20`.
  This agrees with criterion 1.
- (d) No contradiction or missing decision blocks the work. The verdict format (README § sources.csv, verdicts.csv) and
  R1–R6 fix the method.
- (e) Teach-back: I give each of the 20 root claims one verdict in `verdicts.csv`, each backed by a quote from a
  firecrawl-fetched source file under `sources/` with a row in `sources.csv`, and commit only those three paths. The
  decisive check is `check_verdicts.py --scope scope/T-GASA-17.txt` printing `VERDICTS OK … claims 20` with no `ERROR`.

## Assumptions worked past

- `check_verdicts.py` reads stdout through cp1252 on this console only when I print claim text myself; my one-liners
  call `sys.stdout.reconfigure(encoding='utf-8')`. No effect on the checker.
- The guard denies writes outside `### Files to touch ###`, including `C:/4DApp/recheck/T-GASA-17/`. So I wrote both
  CSVs by hand, with no generator script. All fields that hold commas are quoted, and no field holds a double quote.
- Source ids have gaps (`S003`, `S006`, `S010`). Those fetches were not cited, so I moved them to
  `C:/4DApp/recheck/.firecrawl/T-GASA-17/` (R3). I did not rename the cited files: each keeps the name that firecrawl
  `-o` wrote. The README asks only for `S` + three digits.
- EUR-Lex (both `TXT/?uri=CELEX:` and `TXT/HTML/?uri=CELEX:`) returned the Official Journal front page (4.2 MB, the
  same for every CELEX) or a 404, so no EUR-Lex text was usable. For the EU acts I cite the legislation.gov.uk copies
  instead (the adopted PDFs, or the text as derived from EUR-Lex on 31 Dec 2020). I record their kind as `PRIMARY_LAW`.
- The current eCFR 40 CFR 85 Subpart W holds only OBD tests, because the idle short tests were removed. For the
  two-speed idle text I use the CFR 7-1-11 edition of § 85.2215 on govinfo (S011).
- Firecrawl allows only 2 scrapes at once on this key. A larger `xargs -P 8` batch gave exit 1 for most URLs.

## Searches

- `firecrawl search "In Service Exhaust Emission Standards for Road Vehicles 19th edition DVSA pdf"` →
  `recheck/.firecrawl/T-GASA-17/search-dvsa-isees.json` (top hit: the gov.uk assets PDF, scraped as S009).
- `firecrawl search "\"85.2215\" two speed idle test 2500 rpm 300 rpm"` → `search-85-2215.json` (top hit: the govinfo
  CFR-2011 § 85.2215 PDF, scraped as S011).
- No verdict is `UNSOURCED`, so no `UNSOURCED` search list is needed.

Fetched but not cited (now in `recheck/.firecrawl/T-GASA-17/`): 98/69/EC adopted PDF (5.3.7: the type II idle CO and
the high-idle 2 000 min-1 CO and lambda are *recorded*, with no limit); 94/12/EC adopted PDF (it amends the type I g/km
limits only); eCFR 40 CFR 51 Subpart S App. B (two-speed idle high-speed mode 2200–2800 rpm, the same as S011);
eCFR Part 85 Subpart W (current, OBD only); 715/2007 Art. 10 (a duplicate of S007).

## Verdicts

Step 1: `verdicts CITATION_WRONG=1 CONFIRMED=7 CONTRADICTED=5 PARTLY=7`; `sources 8 primary 8`.

| claim | value (line) | verdict | source value (source) |
|---|---|---|---|
| W0118 | 2200 – 2800 rpm, "SAE J1667 / BAR TSI" | CITATION_WRONG | J1667 is the heavy-duty diesel snap-acceleration smoke test; the band is right per 40 CFR 85.2215 (S004; S011) |
| W0119 | 2500 rpm nominal high idle | CONFIRMED | 2500 ±300 rpm (S011) |
| W0124 | Euro 1 idle CO 4.5 %, "type-approval" | PARTLY | 91/441 type II: 3.5 % at type I setting, 4.5 % within adjustment range (S005) |
| W0125 | Euro 2 idle CO 0.5 %, "type-approval" | PARTLY | 0.5 % is the UK in-service idle limit for cat cars 1/8/95–31/8/2002; not a type-approval value (S009) |
| W0126 | Euro 2 HC 1200 ppm at 2500 rpm | CONTRADICTED | 200 ppm at raised speed for cat cars 1/8/95–31/8/2002; 1200 ppm is the non-cat idle value (S009) |
| W0127 | Euro 3 idle CO 0.3 %, "UK MOT" | PARTLY | 0.3 % from 1/9/2002 only; Euro 3 cars first used before that: 0.5 % (S009) |
| W0128 | Euro 3 HC 200 ppm at 2500 rpm | CONFIRMED | 200 ppm (S009) |
| W0129 | Euro 4 idle CO 0.2 %, "UK MOT" | CONTRADICTED | 0.3 % at natural idle; 0.2 % is the fast-idle limit (S009) |
| W0130 | Euro 4 HC 200 ppm at 2500 rpm | CONFIRMED | 200 ppm (S009) |
| W0131 | Euro 5 idle CO 0.2 %, "type-approval" | CONTRADICTED | idle 0.3 %, high idle 0.2 % (2014/45 footnote 7, Euro 5); type-approval only records (S002; S008) |
| W0132 | Euro 5 HC 200 ppm, "type-approval" | PARTLY | type 2 test is CO only; 200 ppm is the in-service limit (S008; S009) |
| W0133 | Euro 5 years 2009–2010 | PARTLY | new types 1 Sep 2009; all new vehicles 1 Jan 2011 (S007) |
| W0185 | CO normal with cat 0.1 – 0.45 % | CONTRADICTED | legal idle CO 0.3 % (S001) |
| W1027 | Euro 1–2 CO ceiling 4.5 % → 0.5 % | PARTLY | 3.5 % (non-cat from 1/8/86) → 0.5 %; 4.5 % is pre-1986 only (S009) |
| W1083 | CO marginal 0.45 – 1.0 % | PARTLY | lower edge must be 0.3 % (legal idle limit); 1.0 % unsourced design value (S001) |
| W1109 | MOT CO ≤ 0.30 % idle | CONFIRMED | CO up to 0.3% at idle (S001) |
| W1110 | MOT CO ≤ 0.20 % raised idle | CONFIRMED | CO up to 0.2% at fast idle 2500–3000 rpm (S001) |
| W1111 | MOT HC ≤ 200 ppm raised idle | CONFIRMED | HC up to 200ppm at fast idle (S001) |
| W1112 | MOT lambda 0.97 – 1.03 raised idle | CONFIRMED | Lambda between 0.97 and 1.03 at fast idle (S001) |
| W1303 | collision co_tier_max 0.45 % (Euro 4 + cat) | CONTRADICTED | legal idle CO 0.3 % (S001) |

What this means for the fix rows (evidence only, no edit made). T-GASA-F45: the working-cat normal CO maximum for the
Euro 4 baseline must not exceed 0.3 %. T-GASA-FEURO: the `_EURO_THRESHOLDS` idle CO column holds in-service (MOT)
values with type-approval labels. The UK date-banded defaults are 3.5 % (non-cat, 1986+), 0.5 % idle / 0.3 % fast idle
(cat, 1995–Aug 2002) and 0.3 % idle / 0.2 % fast idle (from Sep 2002). HC is 200 ppm at fast idle for every cat band.

## Disputes

1. **W0124 (own knowledge in the register vs primary text).** The `suspect` note says 4.5 % is only the UK MOT
   pre-1986 idle limit. Directive 91/441/EEC 5.3.2.2 (S005) also has 4.5 %, as the maximum within the adjustment range,
   with 3.5 % at the type I setting. Both facts are true. Verdict PARTLY.
2. **W0185, W1303, W1083 (two primary bands).** S001 and S009 give 0.3 % idle for cars first used from 1/9/2002, and
   S009 and S002 give 0.5 % idle for advanced-emission (cat) cars first used 1/8/95–31/8/2002. A 0.45 % maximum is legal
   for the earlier band and illegal for the later one. The wiki states its thresholds for a Euro 4 baseline (wiki 02
   §2.8), which falls in the 0.3 % band, so I chose the 0.3 % verdict.
3. **W0131, 2014/45 footnote (7) (own knowledge vs fetched copy).** On legislation.gov.uk the 0.3 % idle / 0.2 % high
   idle alternative carries footnote (7), "Type-approved in accordance with Directive 70/220/EEC, Regulation (EC) No
   715/2007, Annex I, Table 1 (Euro 5), …". My recollection was that the EUR-Lex original dates this pair by first
   registration (about July 2002) or by 98/69 type-approval rows. I could not check the EUR-Lex text (the fetch was
   blocked). The verdict does not depend on the footnote: S001 and S009 give the same 0.3 % idle limit for any car
   first used from Sep 2002.
4. **W0119 (where the quote sits).** The literal `2500 ±300 rpm` on the S011 page is the tail of the section *before*
   § 85.2215. § 85.2215 itself states the window as 2200–2800 rpm. Both are EPA two-speed idle tests, so the verdict
   is CONFIRMED.

## VERIFICATION GATE

| step | command | expected | observed |
|---|---|---|---|
| 1 | `timeout 60 $PY -I check_verdicts.py --scope scope/T-GASA-17.txt \| tail -4` | `verdicts …`, `sources N primary M`, `VERDICTS OK scope=T-GASA-17.txt claims 20`, no `ERROR` | `verdicts CITATION_WRONG=1 CONFIRMED=7 CONTRADICTED=5 PARTLY=7`; `sources 8 primary 8`; `VERDICTS OK scope=T-GASA-17.txt claims 20`; no `ERROR` line. The previous failure `VERDICTS FAIL 20 error(s)` is gone |
| 2 | `check_claims.py --scope all \| tail -1`; `check_code_claims.py --group gaslab \| tail -1` | `CLAIMS OK scope=all candidates 1168 covered claims 1693`; `CLAIMS OK group=gaslab candidates 188 covered claims 195` | both lines exactly as expected |
| 3 | `git log --oneline fix/T-AUD-22a..HEAD`; `git diff --name-only HEAD~1 HEAD \| sed … \| uniq -c`; `git status --porcelain` | spec commit + one commit; only `sources.csv`, `verdicts.csv`, `sources/S*.md`; only the note and RESULT untracked | `9df583d audit(T-GASA-17) …`, `527680e spec(T-GASA-17) …`; `1 sources.csv`, `8 sources/S*.md`, `1 verdicts.csv`; untracked: this note (the RESULT is written after this run) |

## CODE REVIEW

- Scope: two data files and 8 fetched sources. No code, wiki, register or ontology edit (Out of scope respected).
- Both CSV headers are byte-equal to the README headers (the checker checks the header). `sources.csv` is ASCII.
  `verdicts.csv` is UTF-8 (`±` in two quotes); the mojibake check passes. Line endings are LF.
- Every quote was copied from the fetched file, and the checker finds each one after whitespace normalisation. Every
  LEGAL_LIMIT CONFIRMED or CONTRADICTED verdict cites a `PRIMARY_*` source: all 8 sources are primary.
- Each `sources/` file is cited by at least one verdict (S001 ×7, S002 ×1, S004 ×1, S005 ×1, S007 ×1, S008 ×1,
  S009 ×7, S011 ×1). Uncited fetches are outside the clone (R3).
- Each verdict is on a scope root (the checker refuses a verdict on a `same_as` claim). The 14 linked claims inherit
  their root's verdict.

## Time

| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| first action → commit and verification | 2026-11-14T09:20:57Z | 2026-11-14T09:31:47Z | 10 | ABSENT (no context meter in this session) |

Minutes from `$(( (end - start) / 60 ))` with `date -u -d`. Stop rule 100 min: not reached.
