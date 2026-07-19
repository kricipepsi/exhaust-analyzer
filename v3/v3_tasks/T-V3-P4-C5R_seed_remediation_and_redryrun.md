### Goal ###
Remediate the C5-SYNTH seed and re-run the C5 dry-run so C5B can be sized on honest numbers.
Fix ONLY the audit findings in `progress_notes/AUDIT_C5-SYNTH_C5A_2026-07-06.md` — no new scope.
Read-only vs live state; all writes under `v3/`. One task, one session, STOP after the gates.
### Fixes (each maps to an audit finding) ###
1. **EXP-N022 (Blocker 1):** decide the architecture from evidence, not convenience. The corpus row
   carries VIN `WBA…` (BMW → MAF-equipped). Unless research shows otherwise, model it MAF-equipped:
   seed `maf_gps_idle`/`maf_gps_2500` with plausible values consistent with a post-MAF vacuum leak
   (near-normal g/s; the leak air is unmetered) and keep the trim pattern. If instead you can
   ground a speed-density reading of the case, then per cluster5.md §Speed-Density its trims must
   be near-zero and it moves to STAY-ABSTAINED (yield 5→4, disclose). Cite whichever grounds you
   use. Do NOT keep the current contradiction (speed-density label + MAF-car trim pattern).
2. **Web corroboration (Blocker 2):** perform the actual firecrawl research for every band —
   outputs saved under `.firecrawl/` (gitignored), per-band citation with URL in
   `V3_C5_SYNTH_BANDS_2026-07-06.md` §Citations and the seed manifest. If a band moves after real
   corroboration, regenerate the seed (generator stays deterministic; document the band diff).
3. **Disclosure (Blocker 3):** amend the dry-run report + progress notes to state the full
   scoreboard picture: all 5 WOULD_BANK remain abstained; covered 211→207 (name the 4);
   era3_015 leaves covered-as-passing; top3_family 241→246; coverage 71.8%→70.4%;
   on-covered 83.89%→85.02%. The owner signs off C5B on THIS picture.
4. **FT-8 (Deviation 4):** re-derive the union per contract §7 (68 cases: static passes_cases +
   runtime, incl. C3 lean-bias winners) and re-run the neighbour audit on it. Keep the full-corpus
   regression check too.
5. **Consumer overlay (Deviation 5):** strip `NF-001/NF-002` prune unless you can point at a C5
   contract line requiring it; re-run s_commit without it and report the delta. Boost sizing is a
   C5B decision — present the +0.10 as a candidate sized by the sim, not a committed constant.
6. **Band table (Deviation 6):** drop or mark-unused the ERR-LC-003 / ERR-SF-004 bands (no such
   oracle codes among the 10).
### Success criteria ###
1. Regenerated seed + bands report + manifest, byte-identical on rerun, EXP-N022 coherent, real
   citations with URLs, `.firecrawl/` artifacts present.
2. Re-run dry-run: zero-overlay drift=0; s_commit with corrected seed + 68-union FT-8 audit +
   no NF prune (or contract-cited); updated `V3_C5_SIGNAL_DRYRUN_2026-07-06.{md,json}`.
3. Amended progress notes for SYNTH and C5A with the full disclosure of Fix 3 and a pointer to the
   audit note. Do not delete history — append an `## AMENDED (C5R)` section.
4. `py_compile`+`ruff`+`pyright` clean on both scripts; scorer unchanged (`241/294`, `Hash lock: ok`).
### Out of scope ###
No live corpus/engine/registry/shim/rules edit; no schema change; no yardstick mint; no abstain-dial
change; no C5B work; no new task authoring (architect lane). Never `Vault/`. No `graphify`. No secrets.
### Verification ###
```bash
cd /agent_workspace
/agent_workspace/.venv-wired/bin/python -m py_compile v3/gen_c5_synth_seed.py v3/c5_signal_sim.py
/agent_workspace/.venv-wired/bin/python -m ruff check v3/gen_c5_synth_seed.py v3/c5_signal_sim.py
/agent_workspace/.venv-wired/bin/python -m pyright v3/gen_c5_synth_seed.py v3/c5_signal_sim.py
/agent_workspace/.venv-wired/bin/python v3/gen_c5_synth_seed.py && /agent_workspace/.venv-wired/bin/python v3/gen_c5_synth_seed.py  # byte-identical
/agent_workspace/.venv-wired/bin/python v3/c5_signal_sim.py --self-check
/agent_workspace/.venv-wired/bin/python v3/c5_signal_sim.py --scenario all --write v3/reports/V3_C5_SIGNAL_DRYRUN_2026-07-06.json
ls .firecrawl/ | head   # research artifacts must exist
git status --porcelain  # only v3/ (+ .firecrawl gitignored)
```
Gate: all 6 fixes verifiably landed; EXP-N022 decision cited; FT-8 union = contract's 68; full
disclosure present; drift=0; scorer untouched.
### Progress hook ###
PROGRESS note `T-V3-P4-C5R`: Status=done, fixes 1–6 each with evidence, final yield (+5 or +4)
with the abstain/coverage picture stated.
### Depends on ###
AUDIT_C5-SYNTH_C5A_2026-07-06 (this spec's source of truth). **Unblocks C5B spec authoring
(architect) + owner sign-off.**
