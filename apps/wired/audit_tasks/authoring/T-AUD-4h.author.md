# T-AUD-4h — authoring sidecar (Windows Cowork, 2026-11-05)

### Verified context ###
1. **F-C3-3 rest holds** at the 4g tip: `diagnose` sends `dtc.raw_dtcs` to DTCLab only; `_run_obdlab` gets the OBD
   dict unchanged; the only producer of `active_dtcs` under `apps/` is the corpus loader. Observed (read; survey
   `C:/4DApp/recheck/scratch/survey_T-AUD-4g.md` B). F-C3-3's "100 % CODES_RECENTLY_CLEARED" part was fixed by T-AUD-4c.
2. **Rehearsal** (`C:/4DApp/recheck/T-AUD-4h/rehearse.py`): the corpus hand-feeds `active_dtcs` (= user codes, 207 of
   207), so the route is measured on the UI shape (`UI=1`): 4 gate changes, 0 verdicts. The FF gate: 1 verdict change
   (era2_012) of 8 cold freeze frames. Observed (`rehearse.out`, `rehearse_ui.out`).
3. **Pins** (Cowork's `apply_fix.py` on the working copy, restored): P3, including the three mutants. Observed.

### Rulings and the tradeoff that lost ###
- Route all three DTC modes ($03, $07, $0A). Lost: confirmed + pending only (a permanent code is also a confirmed
  fault; OBDLab's gate is a membership check, so a wider set only blocks more often on a real O₂/CKP code).
- An explicit `obd.active_dtcs` wins. Lost: a merge of both lists (no producer sends both except the corpus, where they
  are equal).
- FF trims gated at 70 °C on the freeze frame's own ECT (OBDLab's trim-gate threshold, §9). Lost: 75 °C (§4.1, the
  thermal freeze), which is OBDLab's lambda/VE freeze, not its trim gate.
- Plan NONE, difficulty 3: two small guards, measured pins. Code row, so a second review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | RAN | base shim `40`, registry `5 failed, 498 passed`; rehearsed fix `44`, `5 failed, 502 passed`; mutants 1 failed each |
| step 2 | RAN | base wired 46; rehearsed fix wired 49; comlab `526/4/2 errors`, obdlab `391/2`, ui 30 (base and fix) |
| step 3 | RAN | `git status --porcelain` empty after the suites with the render test deselected |
| step 4 | RAN | `rehearse.py ff` and `UI=1 rehearse.py dtc` on the rehearsed fix: both 0 verdict and 0 gate changes |
| step 5 | RAN | ruff `All checks passed!` on the rehearsed fix |

### Exclusivity ###
No other implementer runs. T-AUD-4d follows.

### Progress hook ###
T-AUD-4h: the user's DTC codes reach OBDLab's O₂/CKP gates; cold freeze-frame trims are not scored.

### Cold read ###
own pass 2026-11-05: P1-P4 measured · literals found once (the `obd_output = _run_obdlab(...)` line,
`ECT_WARM_THRESHOLD = 70  # wiki: §9`, `DTC_TEXT_FIELDS`, `elif source == "ff":`, F-C3-3's "`active_dtcs` is not
routed"); new names absent at base · counts: shim 40 + 4 = 44, registry 498 + 4 = 502, wired 46 + 3 = 49, mutants
1 + 1 + 1 · traceability: criteria 1-4 → steps 1-5 · no finding. cold read: skipped (the second review covers the
code).

### Correction history ###
(none)
