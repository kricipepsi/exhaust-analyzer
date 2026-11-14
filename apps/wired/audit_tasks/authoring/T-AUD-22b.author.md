# T-AUD-22b — authoring sidecar (Windows Cowork, 2026-11-14)

Input: ledger row T-AUD-22 (operator order 2026-11-13); T-AUD-22a accepted (gaslab slice). Tool change by Cowork in the
spec commit: `check_code_claims.py` gains `--files GLOB` (slice scope) and the double-encoding check its README promised.

### Verified context ###
1. **COMLab group: files 52, candidates 3794, auto 1220, to_classify 2574; 293 in `.py` files**, the rest in registry
   rules JSON (1031), `global_fault_registry.json` (393), KG JSON (553), config YAML (331). Observed
   (`extract_code_candidates.py --group comlab`, per-file count).
2. **Header-only `claims_comlab.csv`: `--files '*.py'` gives `CLAIMS FAIL 293 error(s)`; no scope gives 2574.** Observed.
3. **Seed K0012 `delta_engine.py:178` `_FLATCAM_ELEV_O2_MIN: float = 2.0  # ... elevated O2 ≥ ~2.5`;
   `Vault/labs/obdlab/wiki/delta-relations/07_gas-transition-matrix-2speed.md:38` GAS-FC-001 high-speed O2 2.50.**
   Observed (sed, grep).
4. **80 of 293 py candidates carry a `# wiki:` / `# convention:` citation; 213 none.** Observed (regex count).
5. **Both registers drift on the tip:** `check_code_claims.py --group gaslab` 55 `drift`, wiki `check_claims.py --scope
   all` 189 `drift` (T-GASA-18 inserted lines). Ids and values unchanged. Observed. → row T-AUD-22-RESYNC.
6. **Mojibake check works:** a planted `â‰¥` in `claims_gaslab.csv` gives `ERROR GK0048: value is double-encoded`.
   Observed (restored after).

### Rulings and the tradeoff that lost ###
- **COMLab splits by file kind, Python first** (293, the code that runs; the JSON/YAML slices follow: rules a-l 413,
  rules m-z 599, global registry 393, KG 553, config YAML 331). Lost: one COMLab row (2574 lines, past a session).
- **Checker scope by glob** (`--files`), not separate claims files per slice: one register per group, as README says.
  Lost: per-slice files (simpler checker, but the verification rows would read seven files).
- **R4 citation check added** (open the cited doc in the clone): a code value that differs from its own citation is
  the class of defect the operator found. Lost: list-only (faster, but defers the cheapest finding).
- **P3 dropped** (wiki register check): it drifts on the tip, and this row neither reads its lines nor writes it.
  Lost: keep it as a "register unchanged" gate (step 3's porcelain covers that).
- Difficulty 3, Opus 5.5 medium per roster. Survey = facts 1-6. Plan NONE. Docs row: no second-model review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | DEFERRED | pre-state `CLAIMS FAIL 293 error(s)` (P2); post-state needs the claims file |
| step 2 | DEFERRED | pre-state: no claims file, the command raises |
| step 3 | DEFERRED | the spec commit plus one commit, `1 file changed` |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-AUD-22b: COMLab Python literals (293 lines) classified, citation-checked; CLAIMS OK scope=*.py.

### Cold read ###

### Correction history ###
(none)
