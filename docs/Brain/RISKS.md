# 4DLabV2 — Risks (seed)

| ID | Risk | Mitigation |
|---|---|---|
| R1 | "v2" name collision (legacy `v2/` archived vs `4DLabV2/`) | rebuild in place (D-V2-1a); banner in `ARCHIVE/README.md`; grep-gate the token |
| R2 | Outbound ref breaks on a lab move (lab doc → retained substrate) | grep both directions; `MANIFEST.md` lists outbound targets; Phase-6 link-check |
| R3 | Per-lab graphs drift | Stop-hook refresh on `v2_current/`; `v1_baseline/` frozen read-only |
| R4 | A `*Simple` variant holds an active ledger | grep each as target before archiving; nothing archived while a live path points at it |
| R5 | "while I'm here" code change during a structural move | move adds no field, changes no logic; discoveries → proposal §12, not the diff |
| R6 | Root `graphify-out/` re-run by mistake | out of scope; per-lab graphs additive; reaffirmed in `AGENTS.md` |
