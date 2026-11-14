# T-GASA-15 progress note — WIKIAUDIT claim inventory of the wiki

## Readiness

- (a) Starting state matches: branch `fix/T-GASA-15`, `git log fix/T-GASA-14..HEAD` = `9cc058d spec(T-GASA-15) …`,
  both `git status --porcelain` empty, extractor printed `candidates 1565 auto_non_domain 397 to_classify 1168`;
  `git -C C:/4DApp/repo rev-parse HEAD` = `9cc058d15c51477ed63433048f032953f5f63bf6`. Preconditions printed `checked`.
- (b) Step 1 fails for the intended reason: no `claims.csv` exists yet; with a header-only file every one of the 680
  wiki candidates is `uncovered` (P2 `CLAIMS FAIL 680 error(s)`).
- (c) Independent count: `csv.DictReader(candidates.csv)` rows with `file` starting `wiki/` and empty `auto` = 680
  (14 files, 26–74 each), matching P1.
- (d) No contradiction: register format fixed by `wikiaudit/README.md`, checker by `check_claims.py`; class choice is
  bounded judgement among the eight classes.
- (e) Teach-back: I create `claims.csv` with at least one classified row per in-scope wiki candidate (domain numbers
  split one per quantity/condition, otherwise one `NON_DOMAIN` row), with `suspect` texts on contradictions including
  the four CO 0.45 % seeds. The decisive check is `check_claims.py --scope wiki` printing
  `CLAIMS OK scope=wiki candidates 680 …` and step 2 printing `seeds flagged 4 of 4`.

## Assumptions worked past
- The impl_guard denies writes under `C:/4DApp/recheck/` for this row (AGENTS.md names it the throwaway place, but
  `### Files to touch ###` does not list it). Before the denial, one read-only Bash extract wrote per-file candidate
  dumps to `C:/4DApp/recheck/T-GASA-15/dump_*.txt` (copies of `candidates.csv` rows, outside the clone). After the
  denial I wrote nothing more there. The batch tool lives below in this note and writes only `claims.csv`.

## Batch tool

Each batch runs `python -c "<this block>"` with annotation lines on stdin:
`CID | quantity | value | unit | condition | CLASS | suspect` or `CID | ND` (a `NON_DOMAIN` row). It merges into the
existing `claims.csv` (a batch replaces earlier rows for the same `cand_id`), sorts by `candidates.csv` order,
numbers `W0001…`, and sets `same_as` to the first earlier claim on another line with the same (quantity, value
without spaces, `≈` or `~`, unit, condition). A `suspect` text names other claims as `{Cnnnn}` (the first classified
claim of that candidate) or `{Cnnnn#k}` (its k-th claim); a final pass rewrites these to `W` ids.

```python merge
import csv, re, sys, os
WA = "C:/4DApp/repo/labs/gaslab/audit_tasks/wikiaudit/"
F = ["claim_id","cand_id","file","line","quantity","value","unit","condition","class","same_as","suspect"]
cands = list(csv.DictReader(open(WA + "candidates.csv", encoding="utf-8")))
order = {c["cand_id"]: i for i, c in enumerate(cands)}; byid = {c["cand_id"]: c for c in cands}
old = {}
if os.path.exists(WA + "claims.csv"):
    for r in csv.DictReader(open(WA + "claims.csv", encoding="utf-8", newline="")):
        old.setdefault(r["cand_id"], []).append([r[k] for k in F[4:9]] + [r["suspect"]])
new = {}
for ln in sys.stdin.read().splitlines():
    if not ln.strip() or ln.startswith("#"): continue
    f = [s.strip() for s in ln.split("|")]
    if f[0] not in byid: sys.exit("unknown cand " + f[0])
    if f[1:] == ["ND"]: row = ["", "", "", "", "NON_DOMAIN", ""]
    else:
        f += [""] * (7 - len(f))
        if len(f) != 7: sys.exit("bad line: " + ln)
        row = f[1:]
    new.setdefault(f[0], []).append(row)
old.update(new)
rows, seen, n = [], {}, 0
for cid in sorted(old, key=order.get):
    c = byid[cid]
    for q, v, u, cond, cls, sus in old[cid]:
        n += 1; wid = f"W{n:04d}"; same = ""
        if cls != "NON_DOMAIN":
            key = (q.lower(), re.sub(r"[\s≈~]", "", v), u, cond.lower()); prev = seen.get(key)
            if prev and prev[1] != cid: same = prev[0]
            elif not prev: seen[key] = (wid, cid)
        rows.append([wid, cid, c["file"], c["line"], q, v, u, cond, cls, same, sus])
with open(WA + "claims.csv", "w", encoding="utf-8", newline="") as fh:
    w = csv.writer(fh, lineterminator="\n"); w.writerow(F); w.writerows(rows)
todo = [c["cand_id"] for c in cands if c["file"].startswith("wiki/") and not c["auto"]]
print(f"batch {len(new)} cands; total rows {len(rows)} cands {len(old)} uncovered {sum(1 for t in todo if t not in old)}")
```

Final pass, run once after the last batch (`python -c "<this block>"`): it rewrites each `{Cnnnn}` / `{Cnnnn#k}` in
`suspect` to the `W` id of the k-th classified claim of that candidate, and exits non-zero on an unresolved reference.

```python refs
import csv, re, sys
WA = "C:/4DApp/repo/labs/gaslab/audit_tasks/wikiaudit/"
rows = list(csv.DictReader(open(WA + "claims.csv", encoding="utf-8", newline="")))
F = list(rows[0].keys())
by = {}
for r in rows:
    if r["class"] != "NON_DOMAIN": by.setdefault(r["cand_id"], []).append(r["claim_id"])
bad, n = [], 0
def sub(m):
    global n
    k = int(m.group(2) or 1); ids = by.get(m.group(1), [])
    if k > len(ids): bad.append(m.group(0)); return m.group(0)
    n += 1; return ids[k - 1]
for r in rows: r["suspect"] = re.sub(r"\{(C\d{4})(?:#(\d+))?\}", sub, r["suspect"])
if bad: sys.exit("unresolved " + " ".join(bad))
with open(WA + "claims.csv", "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, F, lineterminator="\n"); w.writeheader(); w.writerows(rows)
print(f"refs rewritten {n}; left {sum(r['suspect'].count('{C') for r in rows)}")
```

## Suspect claims (107, every claims.csv row with a suspect text)

| claim | cand | file:line | quantity | value | unit | reason |
|---|---|---|---|---|---|---|
| W0001 | C0005 | 00_index.md:8 | operating envelope model years | 1990–2010 | year | Euro 1 applied to new petrol cars from 1992/93, so 1990–1992 vehicles are pre-Euro 1 and the "Euro 1–5" label is only approximate for 1990–2010 |
| W0051 | C0079 | 01_role_boundaries_dna_ingestion.md:83 | lambda (analyser measured) example | 1.02 | - | contradicts lambda_chem 0.82 on the same payload (W0050) and the rich gases (CO 4.5 %, O2 0.1 %); the line does not say the 0.20 gap is a deliberate divergence example |
| W0085 | C0125 | 02_combustion_foundations.md:71 | HC_FACTOR (ppm HC to vol % carbon term) | 0.0025 | per ppm | the standard Brettschneider HC term is K1·HC with HC in ppm hexane × 1e-4 and K1 = 6 (the factor 6 this file states at W0104), i.e. 0.0006 per ppm; 0.0025 is about 4× larger and no source is given |
| W0090 | C0131 | 02_combustion_foundations.md:81 | Hcv (H/C ratio) | ≈ 1.85 | - | the usual Brettschneider default Hcv for petrol is 1.7261; 1.85 is within the range of real blends but is not the standard default |
| W0093 | C0131 | 02_combustion_foundations.md:81 | HC_FACTOR (ppm HC to vol % carbon term) | 0.0025 | per ppm | same as W0085: the standard factor is 6 × 1e-4 = 0.0006 per ppm hexane |
| W0099 | C0137 | 02_combustion_foundations.md:103 | analyser lambda accuracy | ±0.05–0.10 | - (absolute) | contradicts the ~±1 % headline accuracy on the same line (W0100): ±1 % at λ 1 is ±0.01, five to ten times tighter |
| W0110 | C0143 | 02_combustion_foundations.md:114 | catalyst light-off lambda window | 0.98 – 1.02 | - | light-off is a catalyst temperature threshold (about 250–300 °C), not a λ band; the row labels a λ window as "light-off" |
| W0118 | C0151 | 02_combustion_foundations.md:129 | REGULATORY_HIGH_IDLE rpm band | 2200 – 2800 | rpm | the line cites SAE J1667, which is the diesel snap-acceleration smoke procedure, not a petrol two-speed idle; the band matches BAR TSI 2500 ± 300 rpm |
| W0124 | C0157 | 02_combustion_foundations.md:140 | CO ceiling | 4.5 | % vol | type-approval limits are g/km drive-cycle values, not idle %; 4.5 % is the UK MOT idle limit for older non-cat cars, and the UK MOT limit for 1992+ cat cars at natural idle is 0.5 % |
| W0126 | C0158 | 02_combustion_foundations.md:141 | HC ceiling | 1200 | ppm | UK MOT cat-car HC limit is 200 ppm; 1200 ppm matches the old non-cat idle HC limit; type-approval limits are g/km, not ppm |
| W0129 | C0160 | 02_combustion_foundations.md:143 | CO ceiling | 0.2 | % vol | the UK MOT limit for post-2002 cat cars is 0.3 % at natural idle and 0.2 % at fast idle, as wiki 11 §11.2.3 states (W1109, W1110); 0.2 % at idle looks like the fast-idle value |
| W0131 | C0161 | 02_combustion_foundations.md:144 | CO ceiling | 0.2 | % vol | as W0129: wiki 11 §11.2.3 gives CO ≤ 0.30 % at idle (W1109); 0.2 % is the fast-idle limit |
| W0133 | C0161 | 02_combustion_foundations.md:144 | Euro 5 application years | 2009–2010 | year | Euro 5 applied to new types from Sep 2009 and to all new cars from Jan 2011 |
| W0143 | C0175 | 02_combustion_foundations.md:181 | CO healthy idle anchor | ≈ 0.6 | % vol | above the 0.3 % idle CO ceiling for cat cars (W0127) and the 0.5 % MOT limit; 0.6 % is healthy only for a no-cat engine, which the row does not say |
| W0152 | C0180 | 02_combustion_foundations.md:200 | catalyst light-off lambda window | 0.98–1.02 | - | as W0110: light-off is a temperature threshold, not a λ band |
| W0164 | C0189 | 02_combustion_foundations.md:221 | analyser lambda accuracy | ~±0.05–0.10 | - (absolute) | as W0099: contradicts the ~±1 % headline accuracy |
| W0176 | C0209 | 03_five_gases_reference.md:44 | HC engine-out ceiling | ≤ 100 | ppm | pre-cat gas and no-cat tailpipe gas are both engine-out, yet no-cat allows ≤ 250 ppm (W0175) and the bands call 50–250 ppm pre-cat normal (W0178) |
| W0185 | C0214 | 03_five_gases_reference.md:60 | CO tailpipe normal | 0.1 – 0.45 | % vol | upper edge 0.45 % is above the 0.3 % legal idle CO limit (UK MOT ≤ 0.30 %, wiki 11 §11.2.3, W1109) and contradicts the post-cat rule CO < 0.3 % in the same file (W0192) |
| W0197 | C0222 | 03_five_gases_reference.md:78 | CO2 tailpipe target | 14.5 – 16.0 | % vol | upper edge 16.0 % is above the ~15.5 % CO2 ceiling stated in the same file (W0194) |
| W0202 | C0227 | 03_five_gases_reference.md:84 | CO2 rise idle to 2500 rpm | 1–2 | % vol | with a working-cat idle CO2 of 14.5–16.0 % (W0197) a further 1–2 % rise passes the ~15.5 % ceiling (W0194) |
| W0231 | C0245 | 03_five_gases_reference.md:138 | CO tailpipe normal | 0.1 – 0.45 | % vol | upper edge 0.45 % is above the 0.3 % legal idle CO limit (UK MOT ≤ 0.30 %, wiki 11 §11.2.3, W1109) and contradicts the post-cat rule CO < 0.3 % (W0192) |
| W0232 | C0245 | 03_five_gases_reference.md:138 | CO rich pattern | > 1.0 | % vol | contradicts the rich indicator CO > ~1.5 % in the same file (W0182, W0259) |
| W0234 | C0246 | 03_five_gases_reference.md:139 | CO2 tailpipe target | 14.5 – 16.0 | % vol | as W0197: 16.0 % is above the ~15.5 % CO2 ceiling (W0194) |
| W0240 | C0247 | 03_five_gases_reference.md:140 | O2 lean pattern | > 1.0 | % vol | contradicts the lean indicator O2 > 2.5 % in the same file (W0260) |
| W0241 | C0247 | 03_five_gases_reference.md:140 | O2 misfire pattern | > 4.0 | % vol | contradicts the misfire indicator O2 > 3.0 % with high HC (W0261) |
| W0246 | C0249 | 03_five_gases_reference.md:142 | lambda misfire pattern (false-lean) | > 1.000 | - | contradicts wiki 02: λ is misfire-immune and stays ≈ 1.000 under misfire (W0094) |
| W0260 | C0259 | 03_five_gases_reference.md:164 | O2 lean indicator | > 2.5 | % vol | contradicts the cheat-sheet lean pattern O2 > 1.0 % (W0240) |
| W0261 | C0259 | 03_five_gases_reference.md:164 | O2 misfire indicator | > 3.0 | % vol | contradicts the cheat-sheet misfire pattern O2 > 4.0 % (W0241) |
| W0270 | C0265 | 03_five_gases_reference.md:177 | CO tailpipe normal | 0.1–0.45 | % vol | as W0185: 0.45 % is above the 0.3 % idle CO limit and the post-cat rule CO < 0.3 % (W0192) |
| W0272 | C0266 | 03_five_gases_reference.md:178 | CO2 tailpipe target | 14.5–16.0 | % vol | as W0197: 16.0 % is above the ~15.5 % CO2 ceiling (W0194) |
| W0321 | C0319 | 04_inter_gas_grammar_validity_gates.md:147 | OBD fuel trims | −27…−45 | % | trims of −27 to −45 % exceed the ±25 % trim rail stated in the same file (W0347) and the usual ECU trim authority of about ±25–30 % |
| W0323 | C0320 | 04_inter_gas_grammar_validity_gates.md:150 | WVT code rule O2 | > 5.0 | % vol | contradicts the wiki WVT rule O2 > 2.0 % (W0311); the wiki says the re-binding is pending |
| W0330 | C0328 | 04_inter_gas_grammar_validity_gates.md:170 | O2 spike pre-cat | ~4 | % vol | the same wiki gives 21/6 ≈ 3.5 % for one dead cylinder on a 6-cyl (W0218) |
| W0331 | C0328 | 04_inter_gas_grammar_validity_gates.md:170 | ECU fuel added chasing false lean | up to 30–77 | % | 30–77 % added fuel is far beyond the ±25 % trim rail in the same file (W0347) and normal ECU trim authority |
| W0340 | C0331 | 04_inter_gas_grammar_validity_gates.md:173 | wideband reported vs actual lambda (lean) | 1.30 vs 1.10 | - | this example is a Δλ of 0.20, outside the 0.12–0.18 band on the same line (W0339) |
| W0403 | C0377 | 05_fault_atlas_part_a.md:39 | CO tailpipe normal | 0.1–0.45 | % vol | as W0185: 0.45 % is above the 0.3 % idle CO limit (W0127) and the post-cat rule CO < 0.3 % (W0192) |
| W0404 | C0377 | 05_fault_atlas_part_a.md:39 | CO2 tailpipe target | 14.5–16 | % vol | as W0197: 16 % is above the ~15.5 % CO2 ceiling (W0194) |
| W0423 | C0381 | 05_fault_atlas_part_a.md:55 | ECU fuel added chasing false lean | up to 30–77 | % | as W0331: far beyond the ±25 % trim rail (W0347) and normal ECU trim authority |
| W0434 | C0385 | 05_fault_atlas_part_a.md:65 | triangle sum for rich misfire | ≈ 15.5 | % vol | wiki 04 and the summary in the same file give ≈ 15 % (W0297, W0542) |
| W0437 | C0387 | 05_fault_atlas_part_a.md:70 | triangle sum for air leak | < 14 or > 16 | % vol | below 14 % the triangle gate halts as INVALID (W0283), so a sum < 14 % cannot reach EXHAUST_AIR_LEAK |
| W0438 | C0388 | 05_fault_atlas_part_a.md:74 | NOx | > 1000 | ppm | wiki 03 gives 500–1500 ppm as healthy under load (W0226) and > 1500 ppm as the fault band (W0227) |
| W0452 | C0392 | 05_fault_atlas_part_a.md:93 | CO2 | 11.5–13 | % vol | the discriminator calls the idle clean (wiki 05 line 95), yet 11.5–13 % is the mild combustion deficit band of wiki 03 (W0200) |
| W0505 | C0414 | 05_fault_atlas_part_a.md:128 | triangle sum for rich misfire | ≈ 15.5 | % vol | wiki 04 and the summary in the same file give ≈ 15 % (W0297, W0542) |
| W0507 | C0416 | 05_fault_atlas_part_a.md:132 | NOx | > 1000 | ppm | as W0438: wiki 03 calls 500–1500 ppm healthy under load (W0226) |
| W0523 | C0429 | 05_fault_atlas_part_a.md:158 | CO tailpipe normal | 0.1–0.45 | % vol | as W0185: 0.45 % is above the 0.3 % idle CO limit (W0127) and the post-cat rule CO < 0.3 % (W0192) |
| W0524 | C0429 | 05_fault_atlas_part_a.md:158 | CO2 tailpipe target | 14.5–16 | % vol | as W0197: 16 % is above the ~15.5 % CO2 ceiling (W0194) |
| W0542 | C0434 | 05_fault_atlas_part_a.md:163 | triangle sum for rich misfire | ≈ 15 | % vol | the gas-vector discriminator and relation in the same file give ≈ 15.5 % (W0434, W0505) |
| W0544 | C0435 | 05_fault_atlas_part_a.md:164 | triangle sum for air leak | outside [14,18] | % vol | contradicts the leak discriminator < 14 or > 16 % (W0437); outside [14,18] is also the SAMPLE_INVALID definition (W0449), so the gate would halt before EXHAUST_AIR_LEAK |
| W0545 | C0436 | 05_fault_atlas_part_a.md:165 | NOx | > 1000 | ppm | as W0438: wiki 03 calls 500–1500 ppm healthy under load (W0226) |
| W0560 | C0454 | 06a_fault_atlas_oil_mechanical.md:39 | lambda | ≈ 1.0 | - | the relation and summary for the same fault give HC 150–300 ppm, O2 1.5–3.0 % and a false-lean λ (W0664, W0678), not a near-unchanged vector with λ ≈ 1.0 |
| W0564 | C0456 | 06a_fault_atlas_oil_mechanical.md:45 | GDI in-scope model years | 2000–2010 | year | European GDI cars were sold from 1997 (Mitsubishi Carisma GDI), so 1997–1999 GDI vehicles sit inside the 1990–2010 envelope but outside this window |
| W0565 | C0457 | 06a_fault_atlas_oil_mechanical.md:49 | CO | > 3.0 | % vol | the relation and summary for the same fault give CO 2.0–5.0 % (W0668) |
| W0566 | C0457 | 06a_fault_atlas_oil_mechanical.md:49 | lambda | < 0.85 | - | the relation and summary for the same fault give λ < 0.90 (W0669) |
| W0571 | C0460 | 06a_fault_atlas_oil_mechanical.md:55 | GDI in-scope model years | 2000–2010 | year | as W0564: European GDI sales began in 1997 |
| W0613 | C0475 | 06a_fault_atlas_oil_mechanical.md:105 | HC | 65 | ppm | the WORN_VALVE_SEALS table and router require HC ≤ 35 ppm at 2500 rpm (W0579, W0640); this field case would not route there |
| W0628 | C0477 | 06a_fault_atlas_oil_mechanical.md:107 | NOx | 38 | ppm | the COOLANT_LEAK_INTERNAL router row requires NOx to stay < 30 ppm at 2500 rpm (W0658) |
| W0668 | C0493 | 06a_fault_atlas_oil_mechanical.md:136 | CO | 2.0–5.0 | % vol | the gas vector for the same fault gives CO > 3.0 % (W0565) |
| W0669 | C0493 | 06a_fault_atlas_oil_mechanical.md:136 | lambda | < 0.90 | - | the gas vector for the same fault gives λ < 0.85 (W0566) |
| W0682 | C0501 | 06a_fault_atlas_oil_mechanical.md:158 | CO | 2.0–5.0 | % vol | as W0668: the gas vector gives CO > 3.0 % (W0565) |
| W0683 | C0501 | 06a_fault_atlas_oil_mechanical.md:158 | lambda | < 0.90 | - | as W0669: the gas vector gives λ < 0.85 (W0566) |
| W0710 | C0522 | 06b_fault_atlas_valvetrain_egr_combustion.md:43 | total fuel trim | −27 % to −45 % | % | as W0321: beyond the ±25 % trim rail (W0347) and usual ECU trim authority |
| W0721 | C0524 | 06b_fault_atlas_valvetrain_egr_combustion.md:48 | O2 | 1.0–2.5 | % vol | the discriminator and wiki 04 say the signature persists or worsens at 2500 rpm (wiki 06b line 49, W0312), yet O2 falls from 2.0–4.5 % at idle (W0715) to 1.0–2.5 % |
| W0723 | C0524 | 06b_fault_atlas_valvetrain_egr_combustion.md:48 | lambda | 1.03–1.09 | - | λ falls from 1.08–1.18 at idle (W0717) to 1.03–1.09, which is normalisation, not the persists-or-worsens tell of the discriminator (wiki 06b line 49) |
| W0724 | C0525 | 06b_fault_atlas_valvetrain_egr_combustion.md:49 | MAF ECU positive fuel trims | +22 % to +42 % | % | +42 % is beyond the ±25 % trim rail (W0347) and usual ECU trim authority |
| W0738 | C0529 | 06b_fault_atlas_valvetrain_egr_combustion.md:59 | NOx | > 1000 | ppm | as W0438: wiki 03 calls 500–1500 ppm healthy under load (W0226) |
| W0739 | C0530 | 06b_fault_atlas_valvetrain_egr_combustion.md:61 | NOx | ~1200 | ppm | EGR is normally closed at idle, so a stuck-closed valve should not raise idle NOx; ~1200 ppm is twelve times the healthy idle ceiling < 100 ppm (W0223) |
| W0741 | C0530 | 06b_fault_atlas_valvetrain_egr_combustion.md:61 | NOx rise idle to 2500 rpm (decisive) | Δ > 1500 | ppm | the stated example ~1200 → 2500 ppm is a rise of only 1300 ppm, below the 1500 ppm decisive delta on the same line |
| W0771 | C0538 | 06b_fault_atlas_valvetrain_egr_combustion.md:109 | NOx | 38 | ppm | as W0628: the COOLANT_LEAK_INTERNAL router and gas vector need NOx < 30 ppm (W0658, W0761) |
| W0775 | C0541 | 06b_fault_atlas_valvetrain_egr_combustion.md:119 | lambda | 0.99–1.01 | - | the NORMAL_OPERATION gas vector gives λ 0.995–1.005 (W0407) |
| W0789 | C0547 | 06b_fault_atlas_valvetrain_egr_combustion.md:125 | triangle sum for air leak | > 16 OR < 14 | % vol | as W0437: below 14 % the triangle gate halts as INVALID (W0283), so < 14 % cannot reach EXHAUST_AIR_LEAK |
| W0790 | C0548 | 06b_fault_atlas_valvetrain_egr_combustion.md:126 | NOx | > 1000 | ppm | as W0438: wiki 03 calls 500–1500 ppm healthy under load (W0226) |
| W0799 | C0556 | 06b_fault_atlas_valvetrain_egr_combustion.md:135 | lambda | ~1 | - | the relation and summary for the same fault in wiki 06a give a false-lean λ with O2 1.5–3.0 % (W0665, W0678) |
| W0801 | C0558 | 06b_fault_atlas_valvetrain_egr_combustion.md:137 | CO | > 3 | % vol | as W0565: wiki 06a relation gives CO 2.0–5.0 % (W0668) |
| W0802 | C0558 | 06b_fault_atlas_valvetrain_egr_combustion.md:137 | lambda | < 0.85 | - | as W0566: wiki 06a relation gives λ < 0.90 (W0669) |
| W0810 | C0562 | 06b_fault_atlas_valvetrain_egr_combustion.md:142 | OBD fuel trims | −27…−45 | % | as W0321: beyond the ±25 % trim rail (W0347) |
| W0814 | C0563 | 06b_fault_atlas_valvetrain_egr_combustion.md:143 | MAF ECU positive fuel trims | +22…+42 | % | as W0724: beyond the ±25 % trim rail (W0347) |
| W0816 | C0565 | 06b_fault_atlas_valvetrain_egr_combustion.md:145 | NOx | > 1000 | ppm | as W0438: wiki 03 calls 500–1500 ppm healthy under load (W0226) |
| W0825 | C0570 | 06b_fault_atlas_valvetrain_egr_combustion.md:159 | MAF ECU positive fuel trims | +22…+42 | % | as W0724: beyond the ±25 % trim rail (W0347) |
| W0827 | C0572 | 06b_fault_atlas_valvetrain_egr_combustion.md:162 | NOx | > 1000 | ppm | as W0438: wiki 03 calls 500–1500 ppm healthy under load (W0226) |
| W0834 | C0579 | 06b_fault_atlas_valvetrain_egr_combustion.md:187 | OBD fuel trims | −27…−45 | % | as W0321: beyond the ±25 % trim rail (W0347) |
| W0835 | C0579 | 06b_fault_atlas_valvetrain_egr_combustion.md:187 | RULE_WVT priority for CAM_TIMING_RETARDED_MAP | 82 | - | wiki 04 puts the rich (Speed-Density) branch that emits CAM_TIMING_RETARDED_MAP at priority 40 fallback (W0316), not 82 |
| W0842 | C0582 | 06b_fault_atlas_valvetrain_egr_combustion.md:190 | NOx | > 1000 | ppm | as W0438: wiki 03 calls 500–1500 ppm healthy under load (W0226) |
| W0854 | C0600 | 07_catalyst_postcat_logic.md:47 | CO tailpipe normal | 0.1 – 0.45 | % vol | upper edge 0.45 % is above the 0.3 % legal idle CO limit (UK MOT ≤ 0.30 %, wiki 11 §11.2.3, W1109) and contradicts the wiki 03 post-cat rule CO < 0.3 % (W0192); it also overlaps the failed-cat breakthrough marker CO > 0.2 % in the same file (W0873) |
| W0867 | C0604 | 07_catalyst_postcat_logic.md:52 | max CO drop across working cat | ≈ 2 | % vol | the example on the same line, 1.0 → ~0.05 %, is a drop of 0.95 %, not ≈ 2 % |
| W0873 | C0607 | 07_catalyst_postcat_logic.md:58 | CO breakthrough (failed cat) | > 0.2 | % vol | overlaps the healthy-cat tailpipe CO range 0.1–0.45 % in the same file (W0854) |
| W0878 | C0609 | 07_catalyst_postcat_logic.md:62 | TWC NOx reduction capacity | ≈ 2000 | ppm | a three-way cat converts NOx as an efficiency set by λ and temperature; a fixed ppm capacity is not a known catalyst property and no source is given |
| W0884 | C0614 | 07_catalyst_postcat_logic.md:74 | catalyst light-off lambda window | 0.98–1.02 | - | as W0110: light-off is a temperature threshold, not a λ band |
| W0887 | C0617 | 07_catalyst_postcat_logic.md:80 | CO2 | 14.5–16 | % vol | 16 % is above the ~15.5 % CO2 ceiling of wiki 03 (W0194) |
| W0900 | C0619 | 07_catalyst_postcat_logic.md:83 | CO2 rise idle to 2500 rpm | 1–2 | % vol | as W0202: from a 14.5 % idle a 1–2 % rise passes the ~15.5 % ceiling (W0194) |
| W0901 | C0619 | 07_catalyst_postcat_logic.md:83 | CO2 peak | ~15–16 | % vol | 16 % is above the ~15.5 % CO2 ceiling of wiki 03 (W0194) |
| W0908 | C0627 | 07_catalyst_postcat_logic.md:102 | catalyst lambda window | 0.97–1.03 | - | wiki 02 gives the catalyst windows as 0.995–1.005 (peak) and 0.98–1.02 (W0108, W0110); 0.97 and 1.03 are its breakthrough edges (W0111, W0112) |
| W0917 | C0636 | 07_catalyst_postcat_logic.md:127 | TWC NOx reduction capacity | ≈ 2000 | ppm | as W0878: no fixed ppm capacity is a known catalyst property |
| W0927 | C0646 | 07_catalyst_postcat_logic.md:148 | TWC NOx reduction capacity | ~2000 | ppm | as W0878: no fixed ppm capacity is a known catalyst property |
| W0933 | C0659 | 08_diagnostic_tactics.md:39 | warm-engine precondition ECT | > 60 | °C | 60 °C is low for a warm engine (normal operating temperature is about 80–90 °C), and wiki 09 treats ECT < 75 °C after a long drive as a cold-running fault (W1005) |
| W0963 | C0674 | 08_diagnostic_tactics.md:71 | CO | < 0.2 | % vol | wiki 05 gives 0.10–0.30 % for the same idle state (W0451) |
| W0964 | C0674 | 08_diagnostic_tactics.md:71 | NOx | ~ 0 | ppm | wiki 05 gives 20–60 ppm for the same idle state (W0454) |
| W0999 | C0703 | 09_era_specific_patterns.md:42 | CO | > 6 | % vol | the atlas gives CO > 3.0 % (W0565) or 2.0–5.0 % (W0668) for the same fault, so > 6 % would miss most cases |
| W1003 | C0706 | 09_era_specific_patterns.md:49 | CO | 3–5 | % vol | a stuck-closed thermostat makes the engine overheat; cold running that never reaches closed loop comes from a stuck-open thermostat (the next row, W1004) |
| W1017 | C0717 | 09_era_specific_patterns.md:92 | Era 1 model years | 1990–1998 | year | contradicts the Era 1 span 1990–2000 in the same file (W0997); Euro 3 applied from 2000/2001, so 1998 is not the Euro 2 to 3 boundary |
| W1019 | C0719 | 09_era_specific_patterns.md:94 | Era 2 model years | 1998–2010 | year | contradicts the Era 2 span 2000–2010 in the same file (W1010); Euro 3 began in 2000/2001, not 1998 |
| W1026 | C0726 | 09_era_specific_patterns.md:104 | Era 1 model years | 1990–1998 | year | as W1017: contradicts Era 1 1990–2000 (W0997) |
| W1027 | C0726 | 09_era_specific_patterns.md:104 | CO ceiling span | 4.5 % → 0.5 % | % vol | as W0124: 4.5 % is not a cat-car idle limit; UK MOT cat cars from 1992 have 0.5 % |
| W1028 | C0727 | 09_era_specific_patterns.md:105 | Era 2 model years | 1998–2010 | year | as W1019: contradicts Era 2 2000–2010 (W1010) |
| W1082 | C0796 | 11_sources_appendices.md:56 | CO tailpipe normal | 0.1 – 0.45 | % vol | upper edge 0.45 % is above the UK MOT idle CO limit ≤ 0.30 % in the same file (W1109) and contradicts the wiki 03 post-cat rule CO < 0.3 % (W0192) |
| W1083 | C0796 | 11_sources_appendices.md:56 | CO marginal | 0.45 – 1.0 | % vol | its lower edge 0.45 % leaves 0.30–0.45 % as ideal, though the MOT idle limit in the same file is ≤ 0.30 % (W1109) |
| W1085 | C0797 | 11_sources_appendices.md:57 | CO2 tailpipe target | 14.5 – 16 | % vol | as W0197: 16 % is above the ~15.5 % CO2 ceiling (W0194) |
| W1128 | C0821 | 11_sources_appendices.md:102 | catalyst light-off temperature | ~400 | °C | TWC light-off (50 % conversion) is usually quoted at about 250–300 °C; ~400 °C is high |

## Step 1 disclosure (criterion 3)

```
classes ANALYSER_SPEC=19 DIAGNOSTIC_THRESHOLD=625 INTERNAL_PARAMETER=94 LEGAL_LIMIT=18 NON_DOMAIN=202 PHYSICAL_CONSTANT=58 RULE_OF_THUMB=69 TYPICAL_RANGE=86
suspect 107
CLAIMS OK scope=wiki candidates 680 covered claims 1171
```

Main suspect themes (each claim and its reason is in the table above):
- **CO "normal with cat" 0.1–0.45 %** (seeds C0214, C0245, C0600, C0796, plus the same range at C0265, C0377, C0429):
  above the UK MOT idle limit ≤ 0.30 % (wiki 11 §11.2.3, W1109) and the wiki 03 post-cat rule CO < 0.3 % (W0192).
  Related: wiki 11 "marginal" CO 0.45–1.0 %, the wiki 02 "healthy idle" anchor CO ≈ 0.6 %, and wiki 07 failed-cat CO > 0.2 %.
- **Euro-scaling table (wiki 02 §2.8):** cites type-approval limits (g/km) for idle %; Euro 1 CO 4.5 % "with cat";
  Euro 2 HC 1200 ppm; Euro 4/5 idle CO 0.2 % is the MOT fast-idle value; Euro 5 dates.
- **Brettschneider constants:** HC_FACTOR 0.0025 vs the standard 6 × 1e-4; Hcv 1.85 vs the usual 1.7261; analyser λ
  accuracy ±0.05–0.10 vs ±1 % on the same line.
- **Catalyst:** λ "light-off window", light-off ~400 °C, the 0.97–1.03 masking window, a fixed 2000 ppm NOx capacity,
  the CO-drop example arithmetic.
- **CO2 ceiling ~15.5 %** vs the 14.5–16.0 % working-cat target, the ~15–16 % peak and the 1–2 % rise at 2500 rpm.
- **Cross-file threshold disagreements:** cheat-sheet rich CO > 1.0 vs > 1.5, lean O2 > 1.0 vs > 2.5, misfire O2 > 4.0
  vs > 3.0, misfire λ > 1.000 vs misfire-immune λ ≈ 1.000, rich-misfire triangle ≈ 15 vs ≈ 15.5, EXHAUST_AIR_LEAK
  triangle (< 14 or > 16 vs outside [14,18]), FPR CO > 3.0/λ < 0.85 vs 2.0–5.0/λ < 0.90 vs Era-1 CO > 6, FLAT_CAMSHAFT
  vector, NORMAL λ 0.99–1.01 vs 0.995–1.005, RETARDED_MAP priority 82 vs 40, timing-advanced idle NOx/CO.
- **Fuel trims beyond the ±25 % rail:** −27…−45 %, +22…+42 %, 30–77 % added fuel.
- **Domain knowledge:** SAE J1667 is a diesel smoke test; a stuck-closed thermostat overheats (it does not run cold);
  stuck-closed EGR should not raise idle NOx; Era/Euro boundary years (1998 vs 2000); GDI from 1997; ECT > 60 °C warm.
- **NOx under load:** HIGH_COMBUSTION_TEMP / EGR_STUCK_CLOSED NOx > 1000 ppm vs wiki 03 healthy under load 500–1500 ppm.

## Decisions the task did not specify

- **Class for test-procedure speeds** (2500 rpm dual-idle / RPM-separation point): `DIAGNOSTIC_THRESHOLD` (trade or OEM
  source type); the BAR two-speed-idle band 2200–2800 and the MOT rows are `LEGAL_LIMIT`.
- **Fault gas vectors and field-case readings** are `DIAGNOSTIC_THRESHOLD` (bands that name a fault); healthy and
  reference values are `TYPICAL_RANGE`; GASLab priorities, confidence ceilings, enum counts and scope years are
  `INTERNAL_PARAMETER`; λ catalyst windows and reaction stoichiometry are `PHYSICAL_CONSTANT`.
- **Illustrative payload example** (wiki 01, C0073–C0079) is classified `TYPICAL_RANGE` with condition
  "illustrative RICH_MIXTURE payload", so the verification rows can skip it.
- **Repeated numbers:** every repeat (relations, summaries) gets its own claim; `same_as` is set automatically only on
  exact (quantity, value, unit, condition) matches (340 rows). Near-matches with different wording keep an empty
  `same_as`: a missed link, never a wrong one.
- **Condition-only numbers:** a 2500 rpm that only names the speed of a gas-vector row is folded into `condition`, not
  claimed separately; where a line uses 2500 rpm on its own, it is claimed.
- **Word numbers** ("four", "Sixteen", "Five") are not claimed: the checker requires digits in `value`.
- **Unit assumption:** wiki 05 C0392 `NOₓ 20–60` has no unit; it is recorded as ppm like the rest of the column.
- **Suspect cross-references:** written as `W` ids by the final pass. Three texts cite a line (`wiki 05 line 95`,
  `wiki 06b line 49`) because that line has no matching claim.
- **auto = NON_DOMAIN candidates:** I reviewed every wiki auto line with a number-like pattern (headings, versions,
  dates, section ids). None holds a missed domain number, so no claims were added under R2.

## VERIFICATION GATE

| step | command | expected | observed |
|---|---|---|---|
| 1 | `timeout 60 $PY -I check_claims.py --scope wiki \| tail -4` | `classes …`, `suspect N`, `CLAIMS OK scope=wiki candidates 680 …`, no `ERROR` | `classes …` (above), `suspect 107`, `CLAIMS OK scope=wiki candidates 680 covered claims 1171`, exit 0, no `ERROR` |
| 2 | seed one-liner | `seeds flagged 4 of 4` | `seeds flagged 4 of 4` |
| 3 | `git log --oneline fix/T-GASA-14..HEAD && git diff --stat HEAD~1 HEAD \| tail -1 && git status --porcelain` | spec commit + one commit; `1 file changed`; only note and RESULT untracked | `a6145dd docs(T-GASA-15) …`, `9cc058d spec(T-GASA-15) …`; `1 file changed, 1172 insertions(+)`; `?? labs/gaslab/audit_tasks/progress_notes/` (the RESULT is written after this run) |

Previous decisive failure absent: P2 `CLAIMS FAIL 680 error(s)` (all `uncovered`) is gone. The step 1 output holds no
`ERROR` and no `uncovered` line.

## CODE REVIEW

- Scope: one data file (`claims.csv`), no code. The two scratch scripts live in this note, and their only output is
  `claims.csv`.
- Header matches `check_claims.FIELDS` exactly; `claim_id` W0001–W1171 contiguous in `candidates.csv` order (R3).
- No `same_as` points into its own line (the checker enforces this). Every `{C…}` reference resolved (`left 0`).
- Wiki, vocabulary, ontology and code untouched; `candidates.csv` byte-identical (status shows no change to it).
- Clean.

## Time

| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| first action → inventory, commit, verification | 2026-11-14T07:59:57Z | 2026-11-14T08:20:50Z | 20.9 | ABSENT (no context meter exposed to the session) |
| note and RESULT | 2026-11-14T08:20:50Z | 2026-11-14T08:21:33Z | 0.7 | ABSENT |
| total | 2026-11-14T07:59:57Z | 2026-11-14T08:21:33Z | 21.6 | ABSENT |

Minutes computed with a `datetime` one-liner from `date -u +%FT%TZ` reads. Stop rule (120 min) not reached.

## Correction 1 redispatch (R6 encoding repair)

### Readiness (correction 1)
- (a) Starting state matches `### First action ###`: branch `fix/T-GASA-15`; `git log fix/T-GASA-14..HEAD` =
  `7387acd spec(T-GASA-15): correction 1 …`, `a6145dd docs(T-GASA-15) …`, `9cc058d spec(T-GASA-15) …`; checker tail
  `CLAIMS FAIL 570 error(s)`; `git status --short` shows only the untracked note and RESULT folders;
  `git diff --quiet a6145dd HEAD -- claims.csv` = unchanged. Preconditions printed `checked`.
- (b) Step 1 fails for the intended reason: 570 double-encoded fields (`–`, `°`) in `claims.csv` from `a6145dd`.
- (c) Independent value: `git show a6145dd:./claims.csv` decoded UTF-8, then `.encode('cp1252').decode('utf-8')`
  succeeds on the whole file, changes 484 of the lines (R6 says 484), keeps the line count, and leaves only
  `§ ° ± µ · × ÷ Δ λ – … ₂ → − ≈ ≤ ≥ ≫` as non-ASCII.
- (d) No contradiction: R6 and criterion 4/5 both ask for one encoding-only commit on `claims.csv`.
- (e) Teach-back: I rewrite `claims.csv` as the cp1252-round-trip of the `a6145dd` text and commit it alone, so every
  field holds the wiki's characters. The decisive checks are step 1 `CLAIMS OK scope=wiki candidates 680 …` with no
  `ERROR`, and step 4 `content equal after decode: True`.

### Assumptions worked past (correction 1)
- The note and RESULT exist (untracked) from the first dispatch. I append to the note and rewrite the RESULT; the
  suspect table above was written from the mis-encoded file, so I repair its text the same way (it is my own file).

### Repair (correction 1)
`claims.csv` rewritten as `git show a6145dd:./claims.csv` decoded UTF-8, re-encoded cp1252 and decoded UTF-8 again
(written with `newline=''`, LF kept). Committed alone as `7696b61`. In this note, 91 lines of the earlier sections held
the same mojibake (the suspect table was copied from the mis-encoded file); the same per-line round-trip repaired them,
and a scan finds 0 `â€`/`Â`/`Î` left.

### VERIFICATION GATE (correction 1)

| step | expected | observed |
|---|---|---|
| 1 | `classes …`, `suspect N`, `CLAIMS OK scope=wiki candidates 680 …`, no `ERROR` | `classes ANALYSER_SPEC=19 DIAGNOSTIC_THRESHOLD=625 INTERNAL_PARAMETER=94 LEGAL_LIMIT=18 NON_DOMAIN=202 PHYSICAL_CONSTANT=58 RULE_OF_THUMB=69 TYPICAL_RANGE=86`; `suspect 107`; `CLAIMS OK scope=wiki candidates 680 covered claims 1171`; exit 0; no `ERROR` |
| 2 | `seeds flagged 4 of 4` | `seeds flagged 4 of 4` |
| 3 | repair, correction, `a6145dd`, `9cc058d`; `1 file changed`; only note and RESULT untracked | `7696b61 fix(T-GASA-15) …`, `7387acd spec(T-GASA-15): correction 1 …`, `a6145dd …`, `9cc058d …`; `1 file changed, 484 insertions(+), 484 deletions(-)`; `?? …/progress_notes/`, `?? …/results/` |
| 4 | `content equal after decode: True` | `content equal after decode: True` |

Previous decisive failure absent: `CLAIMS FAIL 570 error(s)` is gone; step 1 prints no `ERROR` line.
`git diff --name-only HEAD~1 HEAD` = `labs/gaslab/audit_tasks/wikiaudit/claims.csv` only.

### CODE REVIEW (correction 1)
- One data file, encoding only: step 4 proves the new text equals the cp1252 round-trip of `a6145dd`; line count
  unchanged; 484 lines differ, matching R6. Claim counts, classes and suspect count are identical to the first
  dispatch (step 1 lines above equal § Step 1 disclosure).
- Non-ASCII set after repair: `§ ° ± µ · × ÷ Δ λ – … ₂ → − ≈ ≤ ≥ ≫`, all as the wiki writes them.
- Note on process: `bash_guard` refused the first commit attempt because it ran after `cd … &&`; re-run as a bare
  `git -C` command.
- Clean.

### Time (correction 1)

| phase | start | end | minutes | context at end |
|---|---|---|---|---|
| redispatch: first action → repair, commit, verification, note | 2026-11-14T08:25:03Z | 2026-11-14T08:26:11Z | 1.1 | ABSENT (no context meter exposed) |
| note and RESULT | 2026-11-14T08:26:11Z | 2026-11-14T08:27:03Z | 0.9 | ABSENT |
| correction 1 total | 2026-11-14T08:25:03Z | 2026-11-14T08:27:03Z | 2.0 | ABSENT |

The note and RESULT writes after 08:26:11Z are recorded in the RESULT finish line. Stop rule (120 min) not reached.
