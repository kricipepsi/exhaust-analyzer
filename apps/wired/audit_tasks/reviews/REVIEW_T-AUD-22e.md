# REVIEW T-AUD-22e — ACCEPT, score 97 (Windows Cowork, 2026-11-15)

Run: Hydrogen lane (gemini-4-hydrogen-high), 15.5 min agy wall time (19:31-19:47 CET); fence check PASS; handed back
BLOCKED (B12, hard, UNSATISFIABLE) after classifying every candidate. Promoted 52cde52 on fix/T-AUD-22e after the tool
fix f4f0347. Docs row: no second-model review (CLAUDE.md step 6).

## Hand-back B12 — UPHELD (owner Cowork)
`check_code_claims.py` matched numbers in the raw JSON text, so `\u00b110` read as `00b110`-digits and `2000\u20133000`
as `20133000`: 44 correct claims could not pass step 1. Cowork's tool defect: the authoring rehearsal never ran step 1
on rows with an escape before a digit. Fix: `unescape()` before NUM_RE. The implementer declined both cheats (writing
the joined digits, or editing the tool) and stopped with a settling command that reproduced the defect.

## Facts re-derived by Cowork (in the clone, after promote)
- Step 1: `CLAIMS OK group=comlab scope=labs/comlab/comlab/config/kg/* candidates 261 covered claims 1379`.
- Step 2: `schema 22 non_domain 22`. Step 3 and the other scopes (registry, rules, *.py, gaslab): CLAIMS OK.
- Step 4: `0` removed lines; rows CK1027-CK1380 appended (354).
- Spot checks against the source: CK1091 (catalyst_failure.json:87), CK1254 (mechanical_wear.json:189), CK1359,
  CK1374: values and conditions match.

## Findings
- 19 new suspects; the ECT ones (CK1374, CK1376, CK1378) are right on physics: an NTC sensor reads -40 C when open and
  about 0.2-0.3 kohm at 90 C. They go to the verification rows (R6); no edit here.
- -3: the RESULT omits the branch/log paste (lane prompt), and the note's figures are in the RESULT only.

Verdict: ACCEPT.
