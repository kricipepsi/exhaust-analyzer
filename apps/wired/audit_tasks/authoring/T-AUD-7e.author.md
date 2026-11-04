# T-AUD-7e — authoring sidecar (Windows Cowork, 2026-11-05, scheduled session 4dapp-cowork-2)

### Verified context ###
1. F-D3-7, F-D3-8 (`audit/reports/R1_D3_20261017.md:74-91`): `rules.py` on `4743cdf` finds every X7, X8 and X9 quote
   (`recheck/T-AUD-7e/rules_base.out`); `paths.py` lists 11 `4DLab/CLAUDE.md` lines.
2. The launchers (`run-*.sh`) read the key from `_skills/firecrawl-web-scraping-search/API.md` only if the file exists;
   `.gitignore:86` ignores it. So the key reaches a coder only when the owner puts the file in the clone.
3. Rehearsal (`make_rh.py` on the repo, then `git checkout --`): `sides not found` 8 → 14; `4DLab/CLAUDE.md` lines
   11 → 7; 5 files, 13+/12-.

### Rulings and the tradeoff that lost ###
- Keep the STOP rule and say where the key comes from. Lost: drop the STOP rule (it guards against invented citations,
  which `4DLab_CLAUDE.md` forbids).
- Leave the four `Vault/tasks` packs, the gaslab ledger history rows and `labs/comlab/tasks/PROGRESS.md:78`. Lost: a
  zero `4DLab/CLAUDE.md` count. `AGENTS.md` forbids `Vault/` edits (F-D3 X10 is its own finding), the ledger rows are
  dated history, and implementers cannot edit ledgers (B9).
- `harness/HARNESS_START_HERE.md:97` still says the only git action is the user's commit (the F-R3-5 class). Pointer
  only here; registered as a residue in the T-AUD-7 rest.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | REHEARSED | `sides not found: 14`; `6` |
| step 2 | REHEARSED | `7`; `0` |
| step 3 | REHEARSED (diff stat) / DEFERRED (commit) | `5 files changed, 13 insertions(+), 12 deletions(-)` |

### Exclusivity ###
No other implementer runs. Built on `fix/T-AUD-7d` (`4743cdf`).

### Progress hook ###
T-AUD-7e: boot docs point at `4DLab_CLAUDE.md`, no sandbox ritual, `python3.14`, firecrawl key not in repo (F-D3-7/8).

### Cold read ###
cold read: not triggered (docs row; rulings are verbatim old/new text, rehearsed end to end).

### Correction history ###
