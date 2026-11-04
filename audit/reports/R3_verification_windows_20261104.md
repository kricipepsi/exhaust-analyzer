# R3 verification — Windows Cowork, 2026-11-04 (channel 032)

Source: `audit/reports/R3_fixchain_20261104.md` on `origin/claude/nice-wright-w61ii2` (commit `3fa9e0b`, built on
`fix/T-VINA-13b` `b444481`). Fetched read-only; not merged, not checked out.

Live tree: `C:/4DApp/repo` on `fix/T-VINA-10` at `56caaa1`. That branch carries the accepted `fix/T-VINA-14`
(`2ff9211`, vref.db 1,274 rows) and the T-VINA-10 build under review. Interpreter `C:/4DApp/.venv/Scripts/python.exe`,
`PYTHONDONTWRITEBYTECODE=1`. Every command was run from `C:/4DApp/repo`; any file it changed was restored
(`git status --porcelain` clean but for the T-VINA-10 note and RESULT).

## Verdicts

| finding | sev | verdict | row |
|---|---|---|---|
| F-R3-2 JTE/JTM → Subaru, KNE → Hyundai | HIGH | CONFIRMED | T-VINA-12 (scope extended) |
| F-R3-1 no test protects the merged vref.db rows | MED | NOT REPRODUCED as stated; a narrower gap remains | folded into T-VINA-16 |
| F-R3-3 VSA type-code VIN reads year 2001 | MED | CONFIRMED for VSA; UNVERIFIABLE for WD3, WDA, WDF, WDZ, VDB | T-VINA-17 (new) |
| F-R3-5 four docs still say "never branch" | MED | CONFIRMED | T-AUD-7b (new) |
| F-R3-4 ADR-0006 says "18-pair" | LOW | CONFIRMED (and DNALab HLD/DLD) | T-VINA-18 (new) |

Counts: CONFIRMED 4, NOT REPRODUCED 1, UNVERIFIABLE 0 findings (one sub-claim of F-R3-3 is UNVERIFIABLE).

## F-R3-2 — CONFIRMED
```
grep -nE "^(JTE|JTM|KNE)," labs/vinlab/vinlab/data/wmi.csv
12325:JTE,Subaru,BELGIUM,modern
12331:JTM,Subaru,BELGIUM,modern
12376:KNE,Hyundai,SOUTH KOREA,modern
```
Decode on the live tree, with the extract's owners of the resolved code
(`labs/vinlab/tools/data/tecdoc_1q2019_engine_extract.csv`):
```
JTEHH20V000092225 make Subaru year None code 1AZFE extract owners {'TOYOTA'}
JTMDEREV00D119221 make Subaru year None code 3ZR-FAE extract owners {'TOYOTA'}
KNEDC221246348997 make Hyundai year 2004 code A3E extract owners {'KIA'}
```
Row: the same defect class as `build_wmi_map.py` keeping the last of several vPIC makes per WMI, already registered
as T-VINA-12. Its scope now names JTE, JTM and KNE.

## F-R3-1 — NOT REPRODUCED as stated
The claim ("restoring the 72-row database leaves every suite green") held at `b444481`. On the live tree it does not:
```
git show 5bf69e5^:labs/vinlab/vinlab/data/vref.db > labs/vinlab/vinlab/data/vref.db     # 72 rows
(cd labs/vinlab && $PY -m pytest -q -p no:cacheprovider --basetemp=<dir>)
FAILED tests/unit/test_euro_unknown_horizon.py::test_out_of_window_row_year_decides
FAILED tests/unit/test_vref_banks_induction.py::test_vref_zero_with_map_v6_gives_one_bank
FAILED tests/unit/test_vref_banks_induction.py::test_vref_one_gives_two_banks
FAILED tests/unit/test_vref_banks_induction.py::test_real_azq_vin_after_merge_is_na_and_maf_only
4 failed, 305 passed, 8 skipped
git show b444481:labs/vinlab/vinlab/data/vref.db > …    # 1,234 rows (13b, without T-VINA-14's 40)
1 failed (test_real_azq_vin_after_merge_is_na_and_maf_only), 308 passed, 8 skipped
git restore labs/vinlab/vinlab/data/vref.db
```
A narrower gap remains: no test pins the row count or a digest of the whole shipped `engine_ref`, so losing merged rows
that no test fixture names goes unnoticed. Folded into T-VINA-16, which changes `engine_ref` again (cylinder column):
that row pins the count and a digest of the shipped table.

## F-R3-3 — CONFIRMED for VSA
```
decode("VSA63823413020157") -> make MERCEDES-BENZ year 2001 o2 WIDEBAND_AFR
grep -n "_TYPE_CODE_WMIS: frozenset" labs/vinlab/vinlab/decoder.py
122:_TYPE_CODE_WMIS: frozenset[str] = frozenset({"WDB", "WDC", "WDD", "WME", "W1K", "W1N"})
grep -nE "^(VSA|WDA|WDF|WD3|WDZ|VDB)," labs/vinlab/vinlab/data/wmi.csv   # all Mercedes-Benz
```
UNVERIFIABLE: WD3, WDA, WDF, WDZ and VDB have no real VIN in the corpus, so whether their position 10 is a year is not
measured. Row T-VINA-17 measures first (the T-VINA-2 method) and adds only the WMIs it can show.

## F-R3-5 — CONFIRMED
```
grep -rniE "never branch" --include=*.md . | grep -v "audit/\|tasks/\|/v2/\|Vault/\|graph/\|_skills"
./docs/Brain/cowork_project/INSTRUCTIONS.md:46
./labs/semantic/SEMANTIC_START_HERE.md:76
./planning/test_rollout/TEST_ROLLOUT_START_HERE.md:30
./v3/PHASE4_HANDOFF.md:106
```
Row T-AUD-7b (the rest of FIX_PLAN T-AUD-7, F-D3-1's git rule): mark each as superseded or align it with
`4DLab_CLAUDE.md`.

## F-R3-4 — CONFIRMED
```
grep -n "18-pair" labs/symptomlab/docs/ADR_SymptomLab.md labs/dnalab/docs/DLD_DNALab.md
labs/symptomlab/docs/ADR_SymptomLab.md:191:The 18-pair catalog invariant is enforced by …   (inside ADR-0006, :178-210)
labs/symptomlab/docs/ADR_SymptomLab.md:217:The legacy 18-pair catalog …                     (ADR-0007, historical: correct)
labs/dnalab/docs/DLD_DNALab.md:147:> 18-pair catalog …
sed -n 160p labs/dnalab/docs/HLD_DNALab.md   # "… SymptomValidator(len==18) — the live catalog is now 18 pairs …"
```
ADR-0008 (`:245`) states 21 pairs. Row T-VINA-18 (docs): ADR-0006 `:191`, DNALab HLD `:160` and DLD `:147`.

## Not taken from the cloud report
The report's §3 observations (cross-brand rows, 57 VINs with map and TecDoc cylinder counts that differ) are listed
there, not reported as findings. The cylinder conflict is already T-VINA-16's scope; the cross-brand lookup is the
known code-only key (T-VINA-14 out of scope).
