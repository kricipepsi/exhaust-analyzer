# T-AUD-7a — authoring sidecar (Windows Cowork, 2026-11-03)

### Verified context ###
1. F-D3-1 (`audit/FINDINGS.md:161`, HIGH doc-drift); FIX_PLAN T-AUD-7 says "do first: one line". Routed to the audit
   pack: it is repo-level governance, not a lab (CLAUDE.md routing names no pack for T-AUD-7).
2. Probe `audit/scratch/D3/rules.py` X1 quotes 4 "never branch / main" sides (4DLab_CLAUDE.md:128, :137, :138;
   v3/CLAUDE.md:40) against 2 production-rule sides (AUDIT_START_HERE.md:59, :62). Base: `sides not found: 0`.
3. Rehearsal: R1+R2 applied on `fix/T-AUD-1b`, probe → X1 shows exactly the 4 NOT FOUND, `sides not found: 4`;
   restored with `git checkout --` (status clean). The probe crashes on cp1252 when piped: `PYTHONIOENCODING=utf-8`.

### Rulings and the tradeoff that lost ###
- Rewrite the section to the branch rule. Lost: a one-line amendment under the old ritual (the stale status block
  "git is not yet initialized" would keep contradicting the tree).

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | REHEARSED | X1 block with the 4 NOT FOUND lines and the 2 AUDIT_START_HERE lines |
| step 2 | REHEARSED | `sides not found: 4` |
| step 3 | DEFERRED | needs the implementer's commit |

### Exclusivity ###
No other implementer runs. Built on `fix/T-AUD-1b` (`7689a3f`).

### Progress hook ###
T-AUD-7a: D3 probe X1 resolved (4 sides gone); only the two git docs changed.

### Cold read ###
cold read: not triggered (docs row; rulings are verbatim text, rehearsed end to end).

### Correction history ###
