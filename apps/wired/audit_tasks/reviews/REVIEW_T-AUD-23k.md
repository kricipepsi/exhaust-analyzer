# REVIEW T-AUD-23k — verify 32 v2 router thresholds (Windows Cowork, 2026-11-16)

**Verdict: ACCEPT, score 88.** Docs/data row, so no second-model review (CLAUDE.md step 6). Hydrogen lane (high),
8.9 min (lane `.exit` 13:50:31-13:59:25 CET).

## Facts (Cowork re-ran, branch `fix/T-AUD-23k`, after promote)
- Commits after `fix/T-AUD-24q`: `aeadef8` spec, `3eca37c` lane work, `2697676` merge. Name-status: M `verdicts.csv`;
  A the note and the RESULT. No new source; no D, no R; no `search/` left.
- `check_verdicts.py`: `VERDICTS OK` for T-AUD-23k (32) and the ten earlier scopes. Existing rows removed: `0`.
- Verdicts: CONFIRMED 10, PARTLY 8, UNSOURCED 8, CONTRADICTED 6.
- **Firecrawl credits are exhausted:** `firecrawl status` prints `Credits: -7 / 1,000 (-1% left this cycle)`
  (Cowork, 2026-11-16, MEASURED). The lane's searches returned HTTP 402, and the note lists 3 searches for each
  UNSOURCED claim (§ Searches Behind `UNSOURCED` Claims).

## What the verdicts say (for the ruling row)
- CONTRADICTED: CK0240 module voltage < 12.0 V (see M2), CK0244 total trim ≥ 15 % at idle (OEM normal ±20 %
  combined, S029), CK0248 port-injection rail drop < 280 kPa (Ford demand 35-60 psig), CK0260 downstream > 0.7 V as
  O2 bias (healthy about 0.7 V, S024), CK0283 idle trim ≤ −10 % as rich, CK0284 catalyst index ratio > 0.20 as
  failure (Ford passes ≤ 0.75, S037).
- UNSOURCED, tool outage: CK0237, 0241, 0242, 0243, 0265, 0266, 0267, 0285.

## Findings
- **M1 (Medium):** the 8 UNSOURCED verdicts record an outage, not missing evidence: the search did not run. They
  must be re-verified when credits return, so they are registered as T-AUD-23k2 (blocked on the operator). Score −7.
- **M2 (Medium):** CK0240 cites Ford's 11-16 V monitor battery band. That band says when a monitor result is valid;
  it does not say what a healthy voltage is. With the engine running, a working charging system holds about
  13.5-14.5 V (Cowork's knowledge), so < 12 V under load does point to a fault. PARTLY is the stronger reading. The
  ruling row must not act on this verdict. Score −5.

## What this unblocks
T-AUD-24r (design ruling, measure first): the CONTRADICTED gates CK0244, 0248, 0260, 0283, 0284 on the v7 corpus with
liveness probes. T-AUD-23k2 waits for Firecrawl credits.
