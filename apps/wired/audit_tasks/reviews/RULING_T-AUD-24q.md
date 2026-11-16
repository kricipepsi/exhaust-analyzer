# RULING T-AUD-24q — what to fix from the T-AUD-23j small-rule-file verdicts (Windows Cowork, 2026-11-16)

Input: `REVIEW_T-AUD-23j.md` (11 CONTRADICTED). Corpus: v7, 314 cases (output identical to
`recheck/T-AUD-24k/promoted.json`). Variants and never/always probes: `C:/4DApp/recheck/T-AUD-24q/run.sh`, `run.txt`.
**Every variant and every probe changes 0 of 314:** the EL-003 HC gate (never/always), OV ECT > 105 (110/never),
VL-001 MAP > 40 (50/never), OV-001 rpm > 1000 (never), and the VL/IF/EL trims (source band/never). The corpus does
not reach these gates; vacuum_leak and overheating have no expected cases.

## Rulings
1. **No fix: CK0406 EL-003 HC ≥ 200.** The verdict is right for a probe-tip leak (dilution lowers HC; S032). But
   EL-003 mixes two faults: a probe or joint leak, which dilutes the sample, and a manifold leak ahead of the O2
   sensor, where the ECU enriches and HC can rise. The rule description claims both raise HC. Splitting it is a
   design change with no corpus case to test it. It stays CONTRADICTED and is recorded here. Lost: flipping the
   gate (it would be wrong for the manifold case).
2. **No fix: OV ECT > 105.** The source boundary is Ford's fuel-monitor entry upper bound (110 °C), which is not a
   definition of "normal", and the overheating family has no corpus case. T-AUD-24n showed that moving an ECT weight
   can take a rule off its own chemistry. Lost: 110 on a monitor-entry figure.
3. **No fix: VL-001 MAP > 40.** At > 50 it would equal VL-003's GATING MAP value, so the two vacuum-leak rules would
   differ only by trims; no corpus case tests the move. Lost: the T-AUD-24j LC-002 parallel (> 50).
4. **No fix: OV-001 rpm > 1000, the trims.** Not reached; no source gives an ECU-raised hot idle; the trim finding is
   the same as in every earlier slice (RULING_T-AUD-24j, 24k, 24m).
