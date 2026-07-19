# HANDOFF — 4DLabV2 Linux migration: state at 2026-06-27 (resume next session)

**For:** the next Cowork (architect) session on this Linux Mint box + the human manager.
**From:** Cowork, 2026-06-26 → 27. **Prior runbook:** `HANDOFF_2026-06-26_linux_migration.md` +
`LINUX_MINT_MIGRATION_PROPOSAL.md` (still valid; this file records what was actually executed and what's left).

---

## 0. TL;DR

The 4DLabV2 working tree is placed at `/agent_workspace` (lean), the config/canon is adapted to Linux,
the two omp coders are configured and pinned, and the architect/coder lane separation is enforced and
verified. **Three things block the finish, all needing you:** (1) `/login` each coder profile,
(2) drop the parent `4DLab/CLAUDE.md` so the shared venv can be built, (3) bring the real `.git`.
Until the venv exists, the inner-loop verification can't run.

---

## 0a. UPDATE — 2026-06-27 (session 2): venv built, parent CLAUDE.md adapted in-mount

Two of the three blockers above are now resolved by Cowork; only the logins and `.git` remain on you.

**Done this session:**
- **#14 shared venv — BUILT and verified.** `/agent_workspace/.venv-wired` created with `uv` on the
  host's permanent `python3.14` (3.14.6); its interpreter **symlinks to** the host uv install — it *is*
  the already-set environment the owner asked to reuse, not a copy. All 8 packages installed editable
  (`comlab dnalab dtclab gaslab obdlab symptomlab vinlab wiredv2`) + `pytest pytest-cov ruff pyright
  jsonschema`. Verified: **gaslab inner loop green** (ruff clean · pyright 0 errors · 208 passed),
  comlab collects 513 tests, 987+ tests discoverable.
- **`.sandbox-py` open question — RESOLVED: it is obsolete.** That cache + the "download-fallback"
  ritual existed only for the Windows-era *resetting* sandbox. This host is **native and persistent**,
  so there is **one** venv, built once. Do **not** recreate `.sandbox-py`.
- **Parent `4DLab/CLAUDE.md` — adapted to Linux and brought in-mount** as
  **`/agent_workspace/4DLab_CLAUDE.md`** (Windows `.venv-wired`/sandbox sections replaced with the
  single-shared-venv model; git ritual → bash + "git not yet initialized" note; bootstrap-table paths
  → `/agent_workspace`, parent-level rows marked `[off-mount]`). The three previously-dangling pointers
  now resolve: `CLAUDE.md` (infra), `AGENTS.md` line 29 ("Progress the app forward") and line 46 (infra).
  Original Windows copy preserved at `/home/m/Desktop/migration` + `/home/m/Desktop/claude/CLAUDE.md`.
- **Mount access confirmed:** the bash tool runs **natively** — `/agent_workspace`,
  `/home/m/Desktop/migration`, `/home/m/Desktop/claude` are all directly reachable (no `/sessions/.../mnt`).

**Pending issues logged (none block the coders from starting):**
- **pyright needs the interpreter.** Run the inner loop from an **activated** venv
  (`source /agent_workspace/.venv-wired/bin/activate`) or pass
  `--pythonpath /agent_workspace/.venv-wired/bin/python`; otherwise pyright reports false
  "pydantic missing-import" errors. (Captured in `4DLab_CLAUDE.md` → Python environment.)
- **comlab undeclared test dep.** comlab's tests import `jsonschema` but its `pyproject.toml` doesn't
  declare it — added to the venv as a stopgap; a coder should add `jsonschema` to comlab `[dev]` extras
  to make it real (signal/noise: dependency should be declared, not implicit).
- **obdlab 4 pre-existing failures.** `labs/obdlab/tests/unit/test_dna_view.py::test_dna_enum_values_in_wiki`
  (anchors 1–3 + one more) fail on an enum-vs-wiki **data mismatch** — tests import and run fine, so it's a
  content/code issue for a coder, **not** an env problem. 384 obdlab tests pass.
- **Cross-tree pytest artifact.** Collecting `labs` + `apps` together throws ~39 duplicate-test-basename
  import errors. Invocation artifact only — **run the loop per-lab** (lab isolation) and it's clean.

**Still on you (unchanged):** (1) `/login` each coder profile (`omp --profile codex|agy` → `/login`),
(2) bring the real `.git` (you're deferring this until you provide the data).

---

## 1. Environment facts (verified this session)

- **Host:** Linux Mint, user `m`, host `m-Teemo`. **Cowork and the omp coders run natively on this host
  and share one filesystem — there is no sandbox isolation.** Any venv built here is usable by both.
- **Workspace:** `/agent_workspace` = 4DLabV2 **child-only**, lean **552 MB** (24k files).
- **Backup (only rollback until `.git` arrives):** `/home/m/Desktop/migration` — the full raw copy,
  left **untouched**. Anything excluded from the mount can be fetched from here.
- **Python:** `python3.14` = **3.14.6** (uv) at `/home/m/.local/bin/python3.14`. Bare interpreter has
  **no packages** — a venv is required.
- **omp:** **16.1.19** at `/home/m/.local/bin/omp`. Default agent dir `/home/m/.omp/agent` (already logged
  in on the default profile). Per-coder profiles now at `/home/m/.omp/profiles/{codex,agy}/agent`.
- **Coder models available in catalog:** `gpt-5.5` (provider `openai-codex`),
  `gemini-3.5-flash` (provider `google-antigravity`).

---

## 2. Done & verified  (§10 Definition-of-Done items that pass now)

- [x] `/agent_workspace` = 4DLabV2 contents; lean mount; caches/`graphify-out`/`ARCHIVE`/Windows cruft/
      dead Windows venvs excluded or removed; **per-lab graphs intact** (105 graph dirs).
- [x] `AGENTS.md` at root (capitalised); **0 stale lowercase `agents.md` refs** (the single remaining hit
      is intentional doc text in `CLAUDE.md` explaining the rename).
- [x] `CLAUDE.md` reframed as the **architect (Cowork) entrypoint** (`@AGENTS.md`, Linux environment
      section replacing the false Windows rules). `CLAUDE.local.md` created for machine paths.
- [x] Line endings normalised to **LF** across 1,432 files.
- [x] `.agent/` coder plane complete: `coders/{codex,agy}/AGENTS.md`+`MEMORY.md`, `assignments.md`,
      `rules/lane-guard.md`.
- [x] **Lane separation (D3) enforced** via omp **TTSR** rules in `.omp/rules/` — `lane-guard-no-graphify`
      and `lane-guard-no-assignments` — confirmed firing on violations, silent on legit actions.
- [x] Coder profiles isolated + pinned: **Codex → `openai-codex/gpt-5.5`**,
      **Agy → `google-antigravity/gemini-3.5-flash`**, both `memory.backend: mnemopi`.
- [x] Launchers `run-codex.sh` / `run-agy.sh` present, executable, syntax-clean.
- [x] **Graphs queryable without rebuild** — all 7 labs have `v2_current/graph.json`; obdlab health check
      passed (1245 nodes, 1664 links, 0 dangling).

**Blocked (cannot pass yet):**
- [ ] Inner loop `ruff → pyright → pytest` — needs the shared venv (`.venv-wired`).
- [ ] Coder role self-report ("summarise your role and boundaries") — needs `/login` per profile.
- [ ] `.env` ignored / no secrets committed — N/A until `.git` arrives (secrets already kept out of tree).

---

## 3. Decisions locked this session

| # | Decision |
|---|---|
| D1 | **Child-only** mount; lean. `labs/vinlab/mysql_data` (482 MB) and top-level `ARCHIVE/` (641 MB) **excluded** — fetch from the Desktop copy if needed. |
| Git | **No git now.** You will bring the real `.git` for 4DLab (and the UI) later. No `git init` was run (would clash with the incoming repo). |
| D3 | Lane-guard = omp **TTSR** rules (`.omp/rules/*.md`) + hard boundaries in each coder's identity file. Architect vs coder separation is the priority and is enforced. |
| Config | `tools.discoveryMode: explicit` (from proposal §2.6) is **invalid** in omp 16.1.19 (valid: `auto\|off\|mcp-only\|all`) — left at `auto`. Profiles use the **native `--profile`** flag (supersedes `PI_CODING_AGENT_DIR`). `memory.backend: mnemopi` set per profile. |
| Models | Codex = `gpt-5.5`, Agy = `gemini-3.5-flash`, both via **Pro subscription, no API keys**. |
| Refs | **Replace-all** lowercase `agents.md` → `AGENTS.md` (27 files), incl. the migration docs — *note:* `HANDOFF_2026-06-26…` and `LINUX_MINT_MIGRATION_PROPOSAL.md` now read oddly where they narrate the rename. Restore those two from the Desktop copy if you want the original wording. |
| Windows residue | ~85 files still contain PowerShell/`C:\` command examples → **leave for now, fix per-file** as labs are worked (boot canon is already Linux-correct). |

---

## 4. Artifacts created / changed this session

**New files (in `/agent_workspace`):**
- `CLAUDE.md` (reframed), `CLAUDE.local.md`, updated `AGENTS.md`.
- `.agent/coders/codex/{AGENTS.md,MEMORY.md}`, `.agent/coders/agy/{AGENTS.md,MEMORY.md}`,
  `.agent/assignments.md`, `.agent/rules/lane-guard.md`.
- `.omp/rules/lane-guard-no-graphify.md`, `.omp/rules/lane-guard-no-assignments.md`.
- `run-codex.sh`, `run-agy.sh`.

**New files (outside the mount):**
- `/home/m/.omp/profiles/codex/agent/config.yml`, `/home/m/.omp/profiles/agy/agent/config.yml`.

**Bulk edits:** renamed `agents.md`→`AGENTS.md`; de-staled 27 files; CRLF→LF on 1,432 files; removed
3 dead Windows venvs (265 MB) + stray `app/`/`.venv`.

---

## 5. Action items for YOU (ordered — these unblock the rest)

1. **Authenticate the coders (one-time each):**
   - `omp --profile codex` → `/login` → ChatGPT/Codex Pro (for `gpt-5.5`).
   - `omp --profile agy`   → `/login` → Google/Gemini Pro (for `gemini-3.5-flash`).
   - Then they launch with identity loaded via `./run-codex.sh` and `./run-agy.sh`.
2. **Drop the parent `4DLab/CLAUDE.md`** into `/agent_workspace` (or paste it). It's the authoritative
   venv/sandbox recipe; needed to build the shared `.venv-wired` (+ `.sandbox-py`) correctly.
3. **Bring the real `.git`** for 4DLab (and the UI) when ready → restores history/rollback.

---

## 6. Remaining tasks (the to-do)

- **#14 — Build the shared venv** (after action item #2). Reconstructed recipe (handoff §6 Step E),
  pending the parent doc to confirm how `.sandbox-py` differs from `.venv-wired`:
  ```bash
  cd /agent_workspace
  python3.14 -m venv .sandbox-py
  python3.14 -m venv .venv-wired && source .venv-wired/bin/activate
  pip install -e apps/wiredV2 -e labs/comlab -e labs/dnalab -e labs/dtclab \
              -e labs/gaslab -e labs/obdlab -e labs/symptomlab -e labs/vinlab
  ```
  Open question: does `.sandbox-py` (the pytest runner) also need the editable installs? Parent recipe decides.
- **#15 — Finish verification** once venv + logins exist: inner loop green, and each coder correctly
  self-reports its role/boundaries (Codex ≠ Agy; reports via `progress_notes`; not the architect; won't graphify).
- **#16 — Windows-command residue:** ~85 files with PowerShell/`C:\` examples; fix per-file as labs are picked up.
- **#10 — Git:** add a Linux `.gitignore` (with `.env`), `core.ignorecase false`, once the real `.git` lands.
- **Optional polish:** per-profile Codex↔Agy mutual-exclusion TTSR mirror rule (identity files already
  enforce this); optional `smol`/`plan` model roles per coder.

---

## 7. How to resume next session (quick start)

1. Boot order is unchanged: `START_HERE.md` → `ROADMAP.md` → active lab `wiki/`+`graph/` →
   `labs/<lab>/tasks/PROGRESS.md` (first `pending` row = next runnable).
2. If the parent `4DLab/CLAUDE.md` is now present → build the venv (§6 #14) → run §6 #15 verification.
3. To restore anything excluded from the mount:
   ```bash
   # e.g. vinlab DB data
   rsync -a /home/m/Desktop/migration/labs/vinlab/mysql_data/ /agent_workspace/labs/vinlab/mysql_data/
   ```
4. Assign a coder by writing a pointer in `.agent/assignments.md` (e.g. `Codex → T-OBDV2-7`), one task per coder.

---

## 8. Notes / watch-outs

- The two migration-runbook docs now self-reference `AGENTS.md` after the replace-all (cosmetic; restore
  from the Desktop copy if the original narration matters).
- Secrets: per-coder `.env` (if any) goes in each omp **profile** agent dir, `chmod 600` — never in
  `/agent_workspace`.
- Don't `graphify` / rebuild graphs — frozen; the TTSR rule will interrupt a coder that tries.
