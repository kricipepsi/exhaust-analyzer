# T-AUD-22a progress note — GASLab code-literal inventory

## Baseline (First action, 2026-11-14T09:00:14Z)

```
$ cd C:/4DApp/repo && git branch --show-current && git log --oneline fix/T-GASA-16..HEAD && git status --porcelain && cd apps/wired/audit_tasks/codeaudit && C:/4DApp/.venv/Scripts/python.exe -I extract_code_candidates.py --group gaslab && git status --porcelain .
fix/T-AUD-22a
c9ff31b spec(T-AUD-22a): code-literal register tools; GASLab code inventory
files 9 candidates 205 auto_non_domain 17 to_classify 188
```
Both `git status --porcelain` runs printed nothing. Preconditions loop printed `checked` and no `MISSING` line.

## Readiness challenge

- (a) Starting state matches the task: branch `fix/T-AUD-22a`, one spec commit `c9ff31b` after `fix/T-GASA-16` (`48d607a`),
  P1 line exact, clean tree, `candidates_gaslab.csv` re-written byte-identical.
- (b) The test fails for the intended reason: with no `claims_gaslab.csv` step 1 cannot pass; P2 (Cowork's rehearsal)
  is `CLAIMS FAIL 188 error(s)`, all `uncovered`. The decisive failure is coverage of the 188 non-auto candidates.
- (c) Independently derived decisive value: I counted the non-auto rows in `candidates_gaslab.csv` myself
  (205 rows, 17 with `auto=NON_DOMAIN`, 188 without), which equals the P1 `to_classify 188` that step 1 must print.
- (d) No contradiction or missing decision prevents implementation. Stale citations (below) are resolved under R4's
  fallback branch and recorded; no stop applies.
- (e) Teach-back: I write `claims_gaslab.csv`, one or more classified rows per non-auto candidate, each with the code's
  citation and a `same_as` link to the wiki-register claim it copies, and a `suspect` where the code value contradicts
  a register claim or a linked register claim is suspect. The decisive check is `check_code_claims.py --group gaslab`
  printing `CLAIMS OK group=gaslab candidates 188 …` with no `ERROR`, plus the 4-of-4 seed check.

## Assumptions worked past

1. **Stale citations.** The code cites `GAS_WIKI §6.1`, `§6.2`, `§7.7`, `§8.4`, `§8.5`, `§8.6`, `§8.7` and
   `GASWIKI-05 §7.14`, `§7.15`. No `GAS_WIKI` document exists (`ls labs/gaslab/docs labs/gaslab/wiki`); the v2 wiki has
   no §6.x, §8.6, §8.7, and its §7.7 / §8.4 / §8.5 hold other topics (poisoning agents, lambda-mismatch test, weird-gases
   tree), and `05_fault_atlas_part_a.md` has no §7.x (`grep -n "^#" labs/gaslab/wiki/*.md`). A citation "points to" a
   register claim only when the cited section exists and holds a claim with the same quantity, condition and value.
   Otherwise `same_as` takes R4's no-citation branch: the first register claim (lowest `W` id) that matches.
   The citation itself is still copied as written (R3). The reviewer can re-point any link from the CSV alone.
2. **Band edges.** When the code uses one edge of a band that the cited claim states (`normal_borderline.max` = 100 of
   `35 – 100`, `normal_with_cat.max` = 0.45 of `0.1 – 0.45`, the 250 floor of `250 – 600`), `same_as` names that band
   claim: verifying the band verifies the edge. `<` against `≤` on the same number is treated as the same value.
3. **Citation for lines without their own comment.** A line inside a multi-line condition with no comment takes the
   comment of the first line of the same condition when that comment names a document (`rule_engine.py` 334-337,
   349-352); otherwise the nearest enclosing comment block that names a document (`rule_engine.py` 388-391 and
   402-406 take `# Rich timing branch rule (Priority 40 fallback) — wiki: GAS_WIKI §4.10, §7.24`; `rule_engine.py` 63
   takes the `GAS_WIKI §4.2 dilution screen` comment on the line above). `contracts.py` 183-202 take the trailing
   comment of the same `Field(...)` statement. `brettschneider.py` 45 (`return 1.0`) sits under a comment block that
   names no document: citation empty.
4. **Class of a linked claim** is copied from the register claim it links to, so one verification verdict covers both.
5. **Unit-conversion literals** (`/ 100.0`, `/ 1_000_000.0`) and zero assignments are not claims: `NON_DOMAIN` when the
   line holds nothing else; no row of their own when the line also holds a domain claim.
6. **Process disclosure.** Before the first gated write I dumped read-only views to `C:/4DApp/recheck/T-AUD-22a/`
   (`cands.txt`, `wclaims.txt`, `tools/wdump.py`) through Bash; AGENTS.md § Environment names that folder for
   throwaway files. A later `Write` there was refused by `impl_guard`, so I wrote no further scratch files. The claim
   spec was written into `claims_gaslab.csv` itself (the authorised path) and rewritten in place into the final CSV by
   a stdin Python script. A long heredoc could not be used: the shell wrapper fails with `unexpected EOF while looking
   for matching` on an apostrophe inside the heredoc. The three recheck files are left in place, untracked and outside
   the clone.

## Work

`claims_gaslab.csv` committed as `e82f870` on `fix/T-AUD-22a`: 195 rows (`GK0001`-`GK0195`) cover all 188 non-auto
candidates. Lines with several claims (the Euro table rows K0061-K0064, the two-speed precondition K0121, the RULE_WVT idle
pair K0171 and K0177) have one row per claim.

### Step 1 figures (criterion 4)

- `classes ANALYSER_SPEC=17 DIAGNOSTIC_THRESHOLD=132 INTERNAL_PARAMETER=24 LEGAL_LIMIT=9 NON_DOMAIN=3 PHYSICAL_CONSTANT=7 RULE_OF_THUMB=2 TYPICAL_RANGE=1`
- `suspect 25 same_as_wiki 174`
- Empty `citation`: **6 of 195** rows. 3 are `NON_DOMAIN` (K0007, K0009, K0031). 3 are domain claims: GK0001/K0004
  (`return 1.0` sentinel, comment block names no document), GK0033/K0037 and GK0034/K0038 (`process.py` payload clamp;
  the comment block names a consumer, not a document).
- 18 domain claims have no `same_as`: the 6 own-finding suspects (below), and 12 with no register claim for the value:
  K0024 (λ_measured 0.5–2.0), K0032/K0033 (cylinder 1–16, bank 1–4 schema bounds), K0068 (λ 0.985–1.015, wiki says
  "→ 1.0"), K0111 (WORN_ENGINE HC 150–300 at 2500, wiki "~ unchanged"), K0114/K0115 (CO ≤ 0.10, wiki "≈ 0"),
  K0116/K0117 (λ 0.995–1.005, wiki "1.0 (stoich)"), K0120 (λ < 0.95 or > 1.05, wiki "λ mismatch"), K0158 (wideband
  O2_SENSOR_BIASED_HIGH λ 1.12–1.18), K0168 (CO > 0.0, "CO present").

### Suspect claims (25), with reasons

Own findings, where the code value differs from the register claim the citation names (R4/R5):
- GK0078 / K0087 `resolution.py:411` HC ≥ 200 at 2500 (CAM_TIMING_RETARDED_MAP): W0703 gives 200–600 ppm; the code drops
  600 and caps at the Euro HC ceiling. For Euro 3–5 that ceiling is 200 ppm, so the window becomes exactly 200 ppm.
- GK0183 / K0193 `rule_engine.py:400`: the same defect in the rich-timing fallback.
- GK0079 / K0088 `resolution.py:415` CO ≤ 4.5 at 2500: W0704 gives 1.5–4.5 %. The lower bound in the code is the Euro idle
  CO ceiling, 0.2–4.5 % (`_rich_co_ceiling`, unless a HIGH-confidence `co_high_idle` overrides it). The cited vocab
  §10.2 has no 4.5 % value.
- GK0184 / K0194 `rule_engine.py:402`: the same defect in the rich-timing fallback.
- GK0091 / K0100 `resolution.py:460` HC 75–500 idle (WORN_VALVE_SEALS router): the register gives 300–500 (W0573, W0639).
  The 75 comes from the v1 range 75–250, which the wiki marks superseded (W0586).
- GK0094 / K0103 `resolution.py:464` λ 0.96–1.0 at 2500 (WORN_VALVE_SEALS): W0642 is λ 0.96 at idle rising to 1.0 at 2500,
  and W0582 is ~1.0 at 2500. The code uses the idle value as the floor of the 2500 window.

Seeds (R5), linked and flagged:
- GK0090 / K0099 `resolution.py:448` CO ≤ 0.45: `as W1298`. 0.45 % is the working-cat CO maximum flagged at W0185,
  above the 0.3 % legal idle CO limit (W0127).
- GK0174 / K0184 `rule_engine.py:370` collision CO tier max 0.45: `as W1303` (the same 0.45 % defect).
- GK0049 / K0060 `resolution.py:39` Euro 1 CO 4.5: `as W0124`. Type-approval limits are g/km values; 4.5 % is the UK
  MOT non-cat idle limit.
- GK0051 / K0061 `resolution.py:40` Euro 2 HC 1200: `as W0126`. The UK MOT cat-car HC limit is 200 ppm; 1200 matches
  the old non-cat limit.

Inherited from a suspect register claim (`as W<id>`; the reason is in the register row):
- GK0006 / K0010 Hcv 1.85 `as W1263` (→ W0090: the usual petrol default is 1.7261).
- GK0008 / K0012 HC_FACTOR 0.0025 `as W1258` (→ W0085: the standard factor is 6 × 1e-4).
- GK0054 / K0063 and GK0056 / K0064, Euro 4 and Euro 5 CO 0.2: `as W0129` and `as W0131`. 0.2 % is the fast-idle limit;
  natural idle is 0.3 %.
- GK0062 / K0071 and GK0162 / K0172, CAM_MAF O2 1.0–2.5 at 2500: `as W0721` (the signature should persist, not fall).
- GK0063 / K0072 and GK0163 / K0173, CAM_MAF λ 1.03–1.09 at 2500: `as W0723` (a fall from the idle λ is normalisation).
- GK0083 / K0092 TIMING_OVER_ADVANCED idle CO2 11.5–13: `as W0452` (a "clean" idle with deficit-band CO2).
- GK0112 / GK0113, K0121 λ 0.98–1.02: `as W0884` (light-off is a temperature threshold, not a λ band).
- GK0114 / K0122 weak-cat CO2 14.5–16.0: `as W0887` (above the ~15.5 % CO2 ceiling, W0194).
- GK0139 / K0148 λ floor 0.85: `as W0566` (the summary for the same fault gives λ < 0.90).
- GK0149 / K0160 coolant CO2 ≤ 12.0: `as W1468` (the wiki gives CO2 < 11.5 %, W0759).
- GK0150 / K0161 coolant HC ≥ 300: `as W1469` (the wiki gives HC 200–400, W0656).

### Other findings for the verification and fix rows (not claims, not edited)

- **Stale citations** (assumption 1): `GAS_WIKI §6.1` (validity_gates 27-31, rule_engine 61), `§6.2` (validity_gates
  48), `§7.7` (rule_engine 65-66, 86-87), `§4.4` (rule_engine 84: the v2 §4.4 is leak-vs-sampling and holds no 16–18
  band), `§8.4`, `§8.5`, `§8.6`, `§8.7` (rule_engine 293-377), `GASWIKI-05 §7.14`, `§7.15` (rule_engine 164-165, 189).
  The v2 sections with these numbers do not exist or hold other topics.
- K0158 λ 1.12–1.18 (wideband O2_SENSOR_BIASED_HIGH) has no source in the register; its citation `GASWIKI-05 §7.15` does
  not exist.
- K0139 `rule_engine.py:61` routes a triangle sum < 14 % to EXHAUST_AIR_LEAK before the INVALID gate (W0283). W0437 is
  flagged for the same reachability conflict. Linked to W0283 and not marked suspect (T-GASA-1 design decision).
- K0024 `lambda_measured` payload bound is 0.5–2.0, against the 0.5–2.5 envelope of `lambda_chem` (W1191). It is a
  different quantity, so not suspect.
- `GAS_VOCABULARY.md:484` says the per-vehicle λ and idle-CO overrides apply "at any confidence". The code
  (`rule_engine.py:138-153`) applies them only at DNA confidence HIGH (T-GASA-6). This wiki/code disagreement is for
  the wiki rows.

VERIFICATION GATE
```
$ cd C:/4DApp/repo/apps/wired/audit_tasks/codeaudit; PY=C:/4DApp/.venv/Scripts/python.exe
# 1.  timeout 60 $PY -I check_code_claims.py --group gaslab | tail -4
classes ANALYSER_SPEC=17 DIAGNOSTIC_THRESHOLD=132 INTERNAL_PARAMETER=24 LEGAL_LIMIT=9 NON_DOMAIN=3 PHYSICAL_CONSTANT=7 RULE_OF_THUMB=2 TYPICAL_RANGE=1
suspect 25 same_as_wiki 174
CLAIMS OK group=gaslab candidates 188 covered claims 195
#     (full run | grep -c ERROR → 0)
# 2.  seed check
seeds flagged 4 of 4
# 3.  (cd labs/gaslab/audit_tasks/wikiaudit && check_claims.py --scope all | tail -1)
CLAIMS OK scope=all candidates 1168 covered claims 1693
# 4.  git log --oneline fix/T-GASA-16..HEAD && git diff --stat HEAD~1 HEAD | tail -1 && git status --porcelain
e82f870 docs(T-AUD-22a): GASLab code-literal register claims_gaslab.csv (188 candidates, 195 claims)
c9ff31b spec(T-AUD-22a): code-literal register tools; GASLab code inventory
 1 file changed, 196 insertions(+)
?? apps/wired/audit_tasks/progress_notes/T-AUD-22a.md
```
Expected success: all four as the task states (P1 188, P3 unchanged). Previous decisive failure absent: P2's
`CLAIMS FAIL 188 error(s)` (all `uncovered`) is gone, with 0 `ERROR` lines. The RESULT is created after this run, so it
shows as untracked as well.

CODE REVIEW
- Scope: one data file, no code. `git diff --stat HEAD~1 HEAD` = 1 file. No tool, code, ontology, wiki or register file
  touched (`git status --porcelain` shows only the note and RESULT).
- Encoding: UTF-8, LF, written by `csv.DictWriter`. A mojibake scan (`Ã`, `â€`, `Â`) over every field found none. `≤ ≥ – λ §`
  are stored as written.
- Header is exactly the README header; `claim_id`s are contiguous `GK0001`-`GK0195` in candidates order (the checker
  passes the format, line, value and `same_as` checks).
- Every `same_as` was checked against the register by id. Every inherited `as W<id>` was added only where that register
  row has a non-empty `suspect`.
- Residual judgement risk: the fallback links for stale citations, and the band-edge links (assumptions 1–2). Both can be
  re-pointed from the CSV alone, with no data loss.

## Time

| phase | start (UTC) | end (UTC) | minutes | context at end |
|---|---|---|---|---|
| first action → verification after commit | 2026-11-14T09:00:14Z | 2026-11-14T09:13:17Z | 13.05 | ABSENT (no context meter exposed to the session) |

Stop rule 75 min not reached.
