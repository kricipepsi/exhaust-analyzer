# REVIEW T-COMA-32 — ACCEPT, score 97 (Windows Cowork, 2026-11-14)

Inline row, re-rated difficulty 1 (two literal edits, no design; registered as 2). `fix/T-COMA-32` on `fix/T-COMA-31`
`c8d844f`: commits `4b6129c` (fix) and `3f545af` (correction 1). Found by T-AUD-22c (CK0403, CK0469/CK0470).

Ruling: EL-002 says "downstream O2 sees excess oxygen (lean)" but gated `o2_downstream ge 0.45` V, the rich side of a
narrowband sensor (OBD_VOCABULARY §12.1: centre ~0.45 V, lean 0.10-0.20 V): flipped to `lt 0.45`, no new number.
MW-004 says "low intake vacuum" but gated `map_kpa lt 30.0` (strong vacuum): the row is removed, because a corrected
`gt X` needs a source-verified weak-vacuum MAP value. Lost: flip to an unverified number. The same inversion in
`global_fault_registry.json` ERR-MW-005 is an ANDed atlas gate: deferred row T-COMA-33.

Facts: new pins 2 passed; with the old rules 2 failed (and the restated mechanical-wear pin failed too: 3 of 34).
comlab 602, registry 508 -> 510 passed 5 skipped, wired 186, ui 75, ruff clean. v7 corpus (314, wired.diagnose, dump
`C:/4DApp/recheck/T-COMA-32/dump.py`): 0 verdicts changed, family accuracy 224 before and after. The corpus cannot tell
old from new for these rules (no case has map_kpa; EL-002 wins no case). Register: `resync_register.py --drop-gone`
(new option) dropped CK0470; CK0403/CK0469 marked RESOLVED; `CLAIMS OK` 650/691.

## Second review
APPROVE WITH CORRECTIONS (ds, `C:/4DApp/recheck/codex/T-COMA-32_review.md`).
- M1 (MW-004 pin allows an unverified `gt X`) — upheld: no MAP row of any direction until T-COMA-33.
- M2 (EL-002 cites OBD_VOCABULARY §6) — upheld: §6 is "Fault families"; now §12.1, pinned.
- L1 (weak "lean" assertion) — upheld: exact clause. L2, L3 — nits. L4 (register) — verified (`DROPPED ... CK0470`).
- Validation note (corpus cannot exercise the rules) — recorded above.

## Score
97: a wrong citation and a loose pin needed a correction.
