# Progress Note — T-AUD-22f

## Readiness Challenge
- **(a) Starting state matches task:** Branch `agy/T-AUD-22f` (worktree per lane rule) at spec commit `28ea491` (`git log --oneline fix/T-AUD-22e..HEAD`), `git status --porcelain` empty, `check_code_claims.py --group comlab --files 'labs/comlab/comlab/config/*.yaml'` fails with `CLAIMS FAIL 213 error(s)` (P1=213, P2), `era_limits 9 linked 0` (P3), full `--group comlab` fails with `CLAIMS FAIL 213 error(s)` (P4), and all precondition files `checked`.
- **(b) Test fails for intended reason:** Every error from `check_code_claims.py` is `uncovered` on the 213 non-auto candidates in the 6 `labs/comlab/comlab/config/*.yaml` files; existing rows `CK0001`-`CK1380` (1,379 rows, 1 skipped id from prior resync) pass with 0 errors.
- **(c) Independently derived decisive expected value:** Direct scan of `candidates_comlab.csv` finds 213 non-auto candidates (`proposals/entries.yaml` 147, `symptom_prior.yaml` 22, `proposals/proposals.yaml` 17, `eras_sensitivity_masks.yaml` 16, `proposals/taxonomy_backbone.yaml` 10, `tag_discriminator.yaml` 1) and 9 threshold lines in `eras_sensitivity_masks.yaml` (`gas_co_max_pct`, `gas_hc_max_ppm`, `lambda_tolerance` × 3 horizons), matching P1–P5.
- **(d) No contradiction or missing decision:** Rulings R1–R7 and lane rules (`T-AUD-22f.go.txt`) align with `codeaudit/README.md`, `wikiaudit/README.md`, and `check_code_claims.py`; `claims_comlab.csv` is UTF-8 with LF line endings.
- **(e) Teach-back:** Append classified claim rows (and `NON_DOMAIN` rows where appropriate) starting at `CK1381` in candidates order to `apps/wired/audit_tasks/codeaudit/claims_comlab.csv` covering all 213 P1 candidates without altering `CK0001`-`CK1380`. Done is verified by `check_code_claims.py` passing (`CLAIMS OK`) on both the config glob and the full `comlab` group, `era_limits 9 linked 9`, and `0` removed lines in `git diff`.

## Assumptions worked past
1. `eras_sensitivity_masks.yaml` `description` lines (`K0384`, `K0391`, `K0400`) mirror `model_year_range` (R4 `NON_DOMAIN`) and Euro category labels (descriptive only per `ADR-0004`); classified `NON_DOMAIN` with empty `citation` (matching all existing `NON_DOMAIN` rows in `CK0001`-`CK1380`).
2. `K0402` (`HORIZON_MODERN`, `gas_co_max_pct: 0.2`) numerically matches `W1110` (`≤ 0.20 % vol`, UK MOT CO limit at raised idle ~2500 rpm), so it links `same_as=W1110` with `suspect` empty per R5 ("link ... when the value agrees, and write `suspect` ... when it does not"); noted here that UK MOT natural idle is `≤ 0.30 %` (`W1109`) and `labs/comlab/wiki/04_horizon_eras.md` §CONCEPT_ERA_MASK lists `0.5 %`.
3. In `proposals/entries.yaml`, dataset sample counts (`K2005` `7,079`, `K2021`/`K2032` `31,740,965`) and `consumer` path labels (`K2001` `2500 RPM`) are `NON_DOMAIN` per R2; RepairPal/CarMD empirical frequencies/shares (`K2023`-`K2031`) are `TYPICAL_RANGE`; `K1967` (`gas_signature`) expands to 4 `DIAGNOSTIC_THRESHOLD` rows linked to `W1115`/`W0617`/`W0615`/`W0011`; `K2115`/`K2120` (`0.1V`/`0.9V` O2 bias) are `TYPICAL_RANGE`; and `taxonomy_backbone.yaml` `K2245`/`K2247` (`5V` sensor reference) are `ANALYSER_SPEC` (consistent with `CK0956`/`CK1152`).

## Step 1 Disclosure & Suspect Claims
- **Step 1 `classes`:** `ANALYSER_SPEC=41 DIAGNOSTIC_THRESHOLD=553 INTERNAL_PARAMETER=475 NON_DOMAIN=270 PHYSICAL_CONSTANT=9 RULE_OF_THUMB=40 TYPICAL_RANGE=226` (total claims: `1614`; appended `235` rows `CK1381`–`CK1615` covering `213` P1 candidates).
- **Step 1 `suspect` and `same_as_wiki`:** `suspect 75 same_as_wiki 47` (`10` new `suspect` claims, `5` new `same_as_wiki` links: `CK1394`→`W1110`, `CK1411`→`W1115`, `CK1412`→`W0617`, `CK1413`→`W0615`, `CK1414`→`W0011`).
- **New `suspect` claims (`10`):**
  - `CK1384` (`K0386`, `eras_sensitivity_masks.yaml:17`, `CO threshold=1.0 % vol`): above Euro 2 with-cat idle limit `0.5 %` (`W0125`) and UK MOT natural-idle limit `≤ 0.30 %` (`W1109`); below non-cat `4.5 %` (`W0124`); also differs from COMLab `wiki/04_horizon_eras.md` §CONCEPT_ERA_MASK (`1.5 %`).
  - `CK1385` (`K0387`, `eras_sensitivity_masks.yaml:18`, `HC threshold=150 ppm`): differs from UK MOT HC legal limit `≤ 200 ppm` at raised idle (`W1111`) and Euro 2 `1200 ppm` (`W0126`, itself flagged suspect); also differs from COMLab `wiki/04_horizon_eras.md` §CONCEPT_ERA_MASK (`300 ppm`).
  - `CK1386` (`K0388`, `eras_sensitivity_masks.yaml:19`, `lambda tolerance=0.10`): `±0.10` (`0.90–1.10`) is wider than the UK MOT lambda legal limit `0.97–1.03` (`±0.03`, `W1112`) at raised idle.
  - `CK1389` (`K0393`, `eras_sensitivity_masks.yaml:32`, `CO threshold=0.5 % vol`): above Euro 3 CO idle limit `0.3 %` (`W0127`), UK MOT natural-idle limit `≤ 0.30 %` (`W1109`), and UK MOT raised-idle limit `≤ 0.20 %` (`W1110`); `0.5 %` is the Euro 2 idle limit (`W0125`); also differs from COMLab `wiki/04_horizon_eras.md` §CONCEPT_ERA_MASK (`1.0 %`).
  - `CK1390` (`K0394`, `eras_sensitivity_masks.yaml:33`, `HC threshold=55 ppm`): differs from UK MOT HC legal limit `≤ 200 ppm` at raised idle (`W1111`) and Euro 3/4 `200 ppm` (`W0128`, `W0130`); also differs from COMLab `wiki/04_horizon_eras.md` §CONCEPT_ERA_MASK (`200 ppm`).
  - `CK1391` (`K0395`, `eras_sensitivity_masks.yaml:34`, `lambda tolerance=0.05`): `±0.05` (`0.95–1.05`) is wider than the UK MOT lambda legal limit `0.97–1.03` (`±0.03`, `W1112`) at raised idle.
  - `CK1395` (`K0403`, `eras_sensitivity_masks.yaml:49`, `HC threshold=15 ppm`): differs from UK MOT HC legal limit `≤ 200 ppm` at raised idle (`W1111`) and Euro 5 `200 ppm` (`W0132`); `15 ppm` matches healthy post-cat typical reading (`W1105`); also differs from COMLab `wiki/04_horizon_eras.md` §CONCEPT_ERA_MASK (`150 ppm`).
  - `CK1396` (`K0404`, `eras_sensitivity_masks.yaml:50`, `lambda tolerance=0.02`): `±0.02` (`0.98–1.02`) is tighter than the UK MOT lambda legal limit `0.97–1.03` (`±0.03`, `W1112`) at raised idle.
  - `CK1517` (`K2095`, `proposals/entries.yaml:492`, `CO delta=-5 %`): leaking/stuck-open fuel injector causes rich fueling which normally increases tailpipe CO rather than decreasing it by `-5%`.
  - `CK1545` (`K2122`, `proposals/entries.yaml:529`, `CO delta=+410 %`): `0.9 V` O2 rich bias (`O2_SENSOR_BIASED_HIGH`) causes the ECU to lean out fueling, yielding low CO (`W1564` `0.0–0.2 % vol`, `W0485` `lambda > 1.0`) rather than `+410%` CO.

## VERIFICATION GATE
- Step 1 (`check_code_claims.py --group comlab --files 'labs/comlab/comlab/config/*.yaml'`): PASS (`CLAIMS OK group=comlab scope=labs/comlab/comlab/config/*.yaml candidates 213 covered claims 1614`; prior decisive failure `CLAIMS FAIL 213 error(s)` absent).
- Step 2 (`era_limits`): PASS (`era_limits 9 linked 9`; prior `era_limits 9 linked 0` resolved).
- Step 3 (`check_code_claims.py --group comlab`): PASS (`CLAIMS OK group=comlab candidates 1427 covered claims 1614`; prior `CLAIMS FAIL 213 error(s)` absent).
- Step 4 (`git diff` removed lines & `git status --porcelain`): PASS (`0` removed lines in `claims_comlab.csv`; only `claims_comlab.csv`, `T-AUD-22f.md`, and `RESULT_T-AUD-22f.md` touched).

## CODE REVIEW
- Checked all 235 appended rows (`CK1381`–`CK1615`): UTF-8 with LF endings, no mojibake, `CK0001`–`CK1380` untouched (`0` `-` lines in `git diff`), all 213 P1 candidates covered in candidates order, `OrchestratorLabBP.md §"Era-to-EURO Mapping Matrix"` set as `citation` exclusively on the 9 `eras_sensitivity_masks.yaml` threshold rows, all 9 era thresholds linked to `W` or flagged `suspect`.

## Time
phase | start | end | minutes | context at end
---|---|---|---|---
classify-and-verify | 2026-11-15T18:53:07Z | 2026-11-15T18:59:05Z | 6.0 | ABSENT

