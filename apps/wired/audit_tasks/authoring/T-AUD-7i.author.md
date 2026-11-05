# T-AUD-7i — authoring sidecar (Windows Cowork, 2026-11-05, scheduled session 4dapp-cowork-2)

### Verified context ###
1. F-D3-19 (`audit/reports/R1_D3_20261017.md:184-191`): `paths.py` on `72bf92c` lists 14 lines for `ROADMAP.md` and
   the dnalab START_HERE (`recheck/T-AUD-7i/paths_base.out`). The three targets exist (`ls`).
2. `ROADMAP.md` holds 8 backtick `` `4DLabV2/ `` prefixes; line 44's `4DLabV2/` is inside an `ARCHIVE/` path.
3. Rehearsal (`make_rh.py` on the repo, then `git checkout --`): 14 → 3 lines (`:44` ARCHIVE, `:62` `v2/` and
   `v6/` prose); 2 files, 10+/10-.

### Rulings and the tradeoff that lost ###
- Re-point the boot docs a coder reads first (ROADMAP is boot step 2). Lost: the whole F-D3-19 table (96 MISSING,
  many of them prose or v7 file names; it needs its own survey).
- Keep `ROADMAP.md:44` (the ARCHIVE pointer) and the `v2/`/`v6/` prose mentions. Lost: a zero count.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | REHEARSED | `1 ROADMAP.md:44`, `2 ROADMAP.md:62` |
| step 2 | REHEARSED (diff stat) / DEFERRED (commit) | `2 files changed, 10 insertions(+), 10 deletions(-)` |

### Exclusivity ###
No other implementer runs. Built on `fix/T-AUD-7h` (`72bf92c`).

### Progress hook ###
T-AUD-7i: ROADMAP and the dnalab START_HERE name paths that resolve (F-D3-19 boot docs).

### Cold read ###
cold read: not triggered (docs row; rulings are verbatim old/new text, rehearsed end to end).

### Correction history ###
