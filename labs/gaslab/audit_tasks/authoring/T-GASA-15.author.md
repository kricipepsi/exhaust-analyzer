# T-GASA-15 — authoring sidecar (Windows Cowork, 2026-11-14)

Input: operator order 2026-11-13 (ledger row T-GASA-WIKIAUDIT); handoff `C:/4DApp/handoffs/HANDOFF_20261113_2315.md`.
Rehearsal copy: `C:/4DApp/recheck/T-GASA-15/lab/`.

### Verified context ###
1. **The audited files hold 1565 digit-bearing lines; 397 carry only non-domain tokens** (section numbers, ids,
   dates, versions, anchors). Sample of 40 auto rows read: all non-domain. Observed (`extract_candidates.py`).
2. **680 candidates to classify are in `wiki/`; 234 in the vocabulary; 254 in the ontology.** Observed (count of
   `candidates.csv` by file and `auto`).
3. **The CO 0.1 – 0.45 % "normal with cat" range sits at C0214 (wiki 03:60), C0245 (03:138), C0600 (07:47), C0796
   (11:56); wiki 03:66 (C0218) states `CO < 0.3 %` with a working cat.** Observed (grep of `candidates.csv`).
4. **`check_claims.py` rejects** a duplicate id, a file/line mismatch, an unknown class, an empty condition, a value
   number absent from the line, an unknown candidate, and every uncovered candidate (680 with a header-only file).
   Observed (crafted rows on the copy).

### Rulings and the tradeoff that lost ###
- **Inventory before verification, split by file group.** 1168 lines will not verify in one session. Lost: one
  verification row per topic, grepped (fast, but cannot show that every number was seen).
- **Wiki first (680), vocabulary + ontology next (488, T-GASA-16) with `same_as` links.** The ontology mostly copies
  wiki values; linking avoids checking a value twice. Lost: one inventory row (past half a context window of output).
- **The register lives in the repo** (`labs/gaslab/audit_tasks/wikiaudit/`), so the fix rows cite it. Lost:
  `C:/4DApp/recheck/` (git-ignored, not reviewable on the branch).
- **T-AUD-22 shares `sources.csv` with the verification rows**; its code-literal inventory is a separate row set.
- Difficulty 3 (classification needs domain judgement; no code). Roster: Opus 5.5 medium. Process for 3: survey (facts
  1-3), no plan. Docs row: no second-model review; Cowork samples the classes at review.

### Gate rehearsal ###
| step | state | evidence |
|---|---|---|
| step 1 | DEFERRED | `CLAIMS OK scope=wiki candidates 680`; pre-state `CLAIMS FAIL 680 error(s)` (P2) |
| step 2 | DEFERRED | `seeds flagged 4 of 4`; pre-state: no `claims.csv`, the command raises |
| step 3 | DEFERRED | the repair commit on top of the correction commit, `1 file changed` |
| step 4 | SIMULATED | cp1252→UTF-8 round trip of `a6145dd:claims.csv` written in place: `content equal after decode: True`; `484 insertions(+), 484 deletions(-)`; `check_claims.py` `CLAIMS OK` (restored) |

### Exclusivity ###
No other implementer runs.

### Progress hook ###
T-GASA-15: the wiki's 680 numeric lines classified into claims.csv; CLAIMS OK; suspects listed.

### Cold read ###
own pass 2026-11-14: literals `CO < 0.3 %` (wiki 03, 1 hit) and `0.1 – 0.45` at the four seed candidates present · closed sets: R2 scope = non-auto `wiki/` rows of `candidates.csv`; R4 suspect set = claims that contradict another claim or the implementer's knowledge · counts: 680 = P1 = P2 · traceability: criteria 1-4 → steps 1-3 and the note · first action re-run leaves the tree clean (checked on 5690cd4) · no finding.
cold read 2026-11-14 FOCUSED reader; trigger grep hit (R2, R4); 0 findings, 0 patched, 0 not-a-conflict — 20070 tok, 5 calls
cold read 2026-11-14 DELTA reader (correction 1); trigger patch; 0 findings — 3 calls (the reader read the patched file whole; it runs no git)

### Correction history ###
- **Correction 1 (2026-11-14, review of `a6145dd`).** Build passed every gate, but 570 fields on 484 lines of
  `claims.csv` are double-encoded (UTF-8 decoded as cp1252, re-encoded: `â€“`, `Â°`, `Î»`). The checker had no encoding
  check (author gap): `mojibake()` added, it fails `a6145dd` and passes the round-tripped file. R6, criteria 4-5 and
  step 4 added; first action re-pinned. Classification sampled (25 random, 12 NON_DOMAIN, all 18 LEGAL_LIMIT): sound.
  Lost alternative: Cowork repairs the file (a silent repair of a failure).
