# REVIEW T-AUD-22-RESYNC — ACCEPT, score 99 (Windows Cowork, 2026-11-14)

Inline difficulty-1 row (roster 2026-11-13), register tooling, no production code: no second-model review (as the
register tools of T-GASA-15 and T-AUD-22a/b). `fix/T-AUD-22-RESYNC` on `fix/T-AUD-22b` `4b185a4`.

Cause: T-GASA-18 edited and inserted lines in the audited files, so both line-keyed registers reported `drift`
(`claims_gaslab.csv` 55, wiki `claims.csv` 189). New Cowork tool `codeaudit/resync_register.py` diffs each file at the
base commit (`66acf33`, the tip before T-GASA-18) against the tip: moved lines get their new number; replaced lines get
the new number, sha and text and are listed as CHANGED for hand re-classification.

Facts: gaslab-code moved 53, changed 2 (K0099, K0184), claims re-keyed 54; wiki moved 178, changed 11, gone 0, claims
re-keyed 162. The 14 claims on changed lines held 0.45 and now state 0.3, each with
`RESOLVED T-GASA-18 (was <old>; legal idle limit 0.3, T-GASA-17 W0185/W1303)` before any earlier suspect text.
After: `CLAIMS OK group=gaslab candidates 188 covered claims 195`; `CLAIMS OK group=comlab scope=*.py candidates 293
covered claims 301`; `CLAIMS OK scope=all candidates 1168 covered claims 1693`; `VERDICTS OK scope=T-GASA-17.txt
claims 20`. Claim ids unchanged, so every `same_as` and verdict link holds.

Residual: lines that T-GASA-18 added (the vocab 0.3-0.5 note, `GAS_VOCABULARY.md:368`) are not in the register; it
cites S009, already verified in T-GASA-17. Every later fix row re-runs this tool against its own base.

## Score
99.
