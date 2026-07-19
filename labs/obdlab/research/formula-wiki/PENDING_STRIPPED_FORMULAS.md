# Formula wiki — PENDING (formulas stripped in source export)

Per the CLAUDE.md readability gate, the formulas below are **referenced in the volume
docs but their display equations / inline math symbols were image-stripped** during the
Google-Docs→md export. They are **NOT reconstructed here.** Where the *same* formula
survives in another readable source, the wiki entry above carries it (cross-ref noted).
Where it survives nowhere readable, it is listed as needing a readable re-export
(plain-text/LaTeX math, e.g. a Gemini export like `FuelTrimW.md`).

| # | Formula referenced | Doc:line | Recoverable elsewhere? | Disposition |
|---|---|---|---|---|
| 1 | Brettschneider λ (display block) | Vol7.md:4–5 ; Vol1 prose | YES — full LaTeX in `wikiResearch.md` | Carried as **F-GAS-01** (sourced to wikiResearch) |
| 2 | vsum constituent-weighted equation | Vol7.md:7–8 | PARTIAL — thresholds (14–18 %, CO+CO₂≤6 %) in prose; exact weighting not | **F-GAS-03** carries thresholds; weighting **PENDING re-export** |
| 3 | Total fuel trim display block | Vol3.md:8 | YES — standard `STFT+LTFT` (fuel-trim/01) | Carried as **F-FT-01** |
| 4 | VE display block | Vol3.md (VE section) | YES — full LaTeX in `OBD_ImplProp.md`/`wikiResearch.md` | Carried as **F-AIR-01** |
| 5 | Calculated vs Absolute Load math | Vol3.md (load section) | YES — `AddObdFields.md` | Carried as **F-AIR-04** |
| 6 | Wideband Ip→λ numeric scale (mA cells) | Vol2.md MD2 | NO numeric scale readable | Sign logic in **F-O2-01**; **mA scale PENDING re-export** |
| 7 | Secondary-ignition KV/ms spec values | Vol2.md MD6 | NO | Concept in pids-protocol/03; **values PENDING re-export** |
| 8 | GDI rail-pressure spec numbers | Vol2.md MD5 | PARTIAL | Concept in pids-protocol/04; **psi specs PENDING re-export** |
| 9 | T15 rich/lean fault-limit + 70 % load cells | Vol2.md MD12/13 | NO | Logic in ecu-diagnosis/08; **limits PENDING re-export** |
| 10 | EGR % thresholds / NOx-reduction limit cells | Vol2.md MD11 | PARTIAL (NOx 1370 °C, >2800 ppm in Vol7) | partly via Vol7; **EGR % cells PENDING re-export** |
| 11 | Euro 1–6 g/km limit cells (later tiers) | Vol6.md standards table | NO (only Euro1/2 CO survive) | taxonomy/01 has eras+dates; **g/km cells PENDING re-export** |
| 12 | Inferred-BARO deviation threshold (inHg) | Vol2.md MD4 | NO numeric | Concept in pids-protocol/02; **threshold PENDING re-export** |

**To clear an item:** provide a readable re-export of the named doc (formulas as
text/LaTeX, not images), exactly as was done for `FuelTrimW.md`. The wiki entry will
then be promoted from PENDING to a full formula card.
