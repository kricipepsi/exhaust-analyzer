# omp × Obsidian Vault Harness — Linux Implementation Plan

**Author:** architect (Cowork) · **Date:** 2026-06-28
**Supersedes (adapts):** `Vault/VAULT_IMPLEMENTATION_PLAN.md` (2026-06-09, Windows-era) and the `ObsidianProp.md` / `apps/omp-obsidian.md` source notes.
**Goal:** run the omp coders (Codex, Agy, +N later) from the Obsidian vault so the architect gets graph-level transparency over the codebase, on the Linux Mint host — without breaking the live edit/test loop or the lane separation.

> **Read order:** §1 verdict → §2 current state → §3 the one decision → §4–§7 the work. The rest is reference.

---

## 1. Verdict (is the research viable?)

Mostly yes — but the single source the plan was drafted from (`apps/omp-obsidian.md`, a note.com article) is **half-right**. I verified omp's real behaviour against the installed binary (`omp/16.1.19`, `/home/m/.local/bin/omp`) and the live repo. The split:

| Claim in `omp-obsidian.md` | Real on this machine? | Action |
|---|---|---|
| omp reads `.clauderules` / `.cursorrules` | **Partly.** omp's Universal Config Discovery loads **Cursor MDC, Cline `.clinerules`, Codex `AGENTS.md`, Gemini `system.md`, Copilot `applyTo`** — *not* a `.clauderules` file. | Keep using **`AGENTS.md` + `.omp/rules/`** (already correct). Ignore `.clauderules`. |
| "omp automatically **scans files on boot**" → symlink the vault as `.omp_vault` | **No.** omp has **no markdown auto-index / boot scan**. It reads files on demand via `read`/`grep`/`find`/`lsp`. The "mental model on first turn" is mnemopi memory compression, not a file index. | **Drop the `.omp_vault` symlink idea entirely** — it buys nothing. |
| `omp --tools read,edit,bash,search` | Flag is real; **`search` is not a tool name.** Real names: `read, edit, bash, grep, find, ast_grep, lsp, write, python, fetch, web_search, …` | Use correct names if we ever restrict tools. |
| "Launch omp inside the vault" | **True and already done** via `--cwd /agent_workspace`. | No change. |

**Net:** the *viable* core is exactly what the repo already practices — `AGENTS.md` as the agent's operating contract, `.omp/rules/` for hard guards, the vault as the agent's working directory. The genuinely new, viable ideas worth adopting from the article corpus are (a) a **vault-awareness contract** for coders, (b) a **scheduled vault-keeper** to fight mirror staleness, and (c) **per-profile shell aliases** for N coders. Everything else is already built or is a myth.

> **Note on `apps/links.md`:** its contents are car-diagnostics links (O2 sensors, fuel trims), **not** agent/vault articles — looks like the wrong file was pasted. The relevant article links live in `apps/wired/obsidian-links.md` and root `links.md`. Their concrete techniques are folded into §4 below; no action needed on `apps/links.md` unless you want it corrected.

---

## 2. Current state (do not rebuild this)

What already exists and works on the host:

- **The workspace root `/agent_workspace` *is* an Obsidian vault.** `.obsidian/` enabled: `graph`, `backlink`, `outgoing-link`, `tag-pane`, `properties`, **`bases`**; community plugins **`realclaudian`** (embeds CLI coding agents — Claude Code / Codex / **Pi** = omp's base — inside the vault) and **`omnisearch`**; plus **`open-in-terminal`**.
- **Coders already launch from the vault root.** `run-codex.sh` / `run-agy.sh` → `omp --profile <c> --cwd /agent_workspace --append-system-prompt .agent/coders/<c>/AGENTS.md`. They share the host venv `.venv-wired` (Python 3.14).
- **Lane separation is enforced in omp.** `omp ttsr list` shows the repo's 2 native rules live: `lane-guard-no-graphify` (blocks coders running `graphify`) and `lane-guard-no-assignments`. Skills are wired via `scripts/wire_skills.sh` → `.agent/skills/` (`skill://` discovery).
- **A curated mirror vault already exists at `Vault/`** — a *read-mostly* copy of finished labs (code/tests/wiki/docs tiers) with `node_type` frontmatter, `[[WikiLinks]]`, three `.base` views (`modules`, `consumers`, `drift-guards`), `System-Map.md`, `_meta/PROVENANCE.md`. Built by `build_lab_vault.py`; rebuilt for **all** labs on 2026-06-28. This is the artifact `VAULT_IMPLEMENTATION_PLAN.md` produced.

So the question is **not** "how do we put coders in a vault" — they're already there. It's: **which vault is the transparency surface, how do we keep it true on Linux, and how do coders use the Obsidian structure rather than ignore it.**

---

## 3. Decision (made 2026-06-28): live root + excludes

Two things were being conflated; they are **independent**:

- **Where Obsidian opens** = the *human/architect* view. Has no effect on coders.
- **Where omp coders run (`--cwd`)** = where real code is edited and `.venv-wired` runs tests. Must be the live root, because `Vault/` holds **copies** (`Vault/labs/comlab/code` is a real dir, not a symlink — edits there never reach real code, and there's no venv). Symlinking the mirror to live code is fragile and fights the harness's cwd-sensitive pytest/pyright (`U-WV2-3`). So coders run `--cwd /agent_workspace` regardless of the view choice.

So "coders run from the live root" does **not** force a noisy view. The fork was only ever about the *view*:

| | **A — Live root + excludes (CHOSEN)** | B — `Vault/` copy-mirror |
|---|---|---|
| What you see | the **live** `labs/`+`apps/` | `.md` copies of finished labs |
| Currency | always current; = what coders edit | stale until `build_lab_vault.py` re-runs |
| Rebuild ritual | **none** | required after every accepted task |
| Slop control | exclude a handful of folders | curated by copy |
| `.base` views | need frontmatter on **live** notes | frontmatter on the copies |

**Decision: Option A.** Obsidian opens on `/agent_workspace`; noise is hidden with `userIgnoreFilters`. You watch the real files change, with zero rebuild loop. The `Vault/` mirror becomes redundant for transparency → **archive it** (§9; rules say archive, never delete). The one cost — the curated `.base` consumer/drift-guard views — is recovered by putting the node frontmatter on the **live** `wiki/`/`docs` notes (already started by `T-VAULT-WIKIFRAME-1`, which framed the live `research/chunks/README.md` files). The rest of this plan assumes A; §4 (coder vault-awareness) and §7 (scaling) are unaffected.

### Obsidian excludes to apply (`.obsidian/app.json` → `userIgnoreFilters`)

Dotfolders (`.venv-wired`, `.git`, `.ruff_cache`, `.pytest_cache`, `.claudian`, `.obsidian`) are already auto-hidden. Add the visible slop:

```json
{
  "newLinkFormat": "shortest",
  "userIgnoreFilters": [
    "ARCHIVE/",
    "harness/",
    "planning/",
    "scratch/",
    "_skills/",
    "graphify-out/"
  ]
}
```

Loose root brain-`.md` docs (HANDOFF_*, MIGRATION_*, AUDIT_*, GRAPH_*, etc.) also clutter the graph — either move them under a single `docs/brain/` folder you add to the ignore list, or accept them as top-level orphans. (Decide before applying; moving files is the only non-trivial bit.) Leaving `harness/` excluded assumes you don't want it in the code graph — flip if you do.

---

## 4. Make coders vault-aware (the real payoff, ~1 small spec)

Today coders treat `.md` notes as inert files. The viable, article-backed move is a short **vault-awareness contract** so they navigate and *leave a trail* in the Obsidian structure. This is additive to the existing five rules — not a rewrite.

**Touch one file:** add a `## Vault conventions` block to the shared `AGENTS.md` (auto-loaded by omp). Keep it to four lines:

1. **Navigate the graph, not just grep.** Already rule 1 (query `labs/<lab>/graph/` before reading blind). Restate that lab wikis and progress notes use `[[WikiLinks]]` — follow them.
2. **Leave backlinks.** When a progress note references a task, wiki topic, or consumer, write it as `[[<note-name>]]` so it shows in Obsidian backlinks/graph. (Zero cost; pure transparency.)
3. **Respect the node frontmatter schema** when you touch a `wiki/` or `docs/` note: keep `node_type / lab / module / implements / consumers / drift_guards / tags / source` intact (schema is authoritative in `_skills/graph/4dlab-vault/reference/frontmatter-schema.md`). Don't invent `node_type` values.
4. **Don't build or edit the mirror.** `Vault/` and `graphify` are architect-lane (lane-guard already blocks graphify). Coders edit live `labs/` only.

**Optional, if you want a hard guard** rather than a prose convention: add a TTSR rule in `.omp/rules/` that fires on edits to `Vault/**` and stops the coder ("`Vault/` is an architect-rebuilt mirror; edit `labs/<lab>/` instead"). One file, same shape as the existing `lane-guard-*.md`. Recommended — it makes Option B safe by construction.

That's the whole coder-side change. No symlinks, no `.clauderules`, no new launcher flags.

---

## 5. Linux adaptation deltas (vs the 2026-06-09 Windows plan)

The stalled plan's bones are fine; only the OS-coupled parts need fixing:

| Item in old plan | Why it stalled | Linux fix |
|---|---|---|
| Obsidian CLI query path (`ObsidianCLI.md`) | Assumed Windows `.com` redirector + desktop running | **Drop as a hard dependency.** The mirror is built by `build_lab_vault.py` over plain file IO — no Obsidian process needed. Treat CLI as optional/manual. |
| `~/.claude/commands/*.md` for `/graph-find`, `/check-impact` | Windows path + assumed Claude Code | omp loads commands from `.omp/commands/[name]/index.ts` **and** `.claude/commands/`. Author them once in-repo (`.claude/commands/`) so both the architect's Claude and omp see them; or skip — the two greps are trivial inline. |
| Absolute `C:\Workspace` paths | Windows | Mostly migrated: root is `/agent_workspace`, venv `/agent_workspace/.venv-wired` (per `CLAUDE.md` env block). **One residual found** — `Vault/labs/comlab/docs/Vocabulary/SEMANTIC_CONTRACT.md:5` still reads `C:\Workspace\`. It's a *mirror* copy, so fix the **source** doc in `labs/comlab/` then rebuild that lab's mirror (don't edit the mirror directly). |
| "build then open in Obsidian to verify Bases" | Manual Windows step | On Linux, `bases` core plugin is enabled; verify via Obsidian desktop on the host **or** assert mechanically (frontmatter present + no unresolved links) in the rebuild script's `--check`. |

---

## 6. Implementation phases (minimal, ordered)

Each phase is one reviewable change. Phases 1–2 are the whole "vault harness"; 3–4 are the transparency loop; 5 is scaling.

**Phase 0 — Confirm baseline (no code).** Run `omp ttsr list` and `cat run-*.sh` to confirm rules load and `--cwd /agent_workspace` is set. (Done in this study — both green.)

**Phase 1 — Clean the live view (the chosen surface).** Add `userIgnoreFilters` to `.obsidian/app.json` (§3 block). Optionally relocate loose root brain-`.md` docs under `docs/brain/`. *Success:* opening `/agent_workspace` in Obsidian shows a graph of `labs/`+`apps/` with no venv/ARCHIVE/cache/skill noise; backlinks resolve.

**Phase 2 — Coder vault-awareness.** Add the `## Vault conventions` block to `AGENTS.md` (§4). Recommended: add `.omp/rules/lane-guard-no-vault-edit.md` (now doubly useful — it stops a coder editing the soon-to-be-archived `Vault/` copies). *Success:* the new rule shows in `omp ttsr list`; a test edit under `Vault/**` is blocked.

**Phase 3 — Recover the `.base` views on the live tree.** Move the three `.base` files (`modules`, `consumers`, `drift-guards`) to a root `_bases/` (or keep in place) pointed at live notes, and ensure the node frontmatter (`node_type … consumers … drift_guards`) is present on the live `labs/<lab>/.../wiki` + `docs` notes you care about — extend the `T-VAULT-WIKIFRAME-1` pattern. Frontmatter on **live** notes is the only thing the `.base` queries need; no copies. *Success:* the three Bases render rows against live notes; every framed note has ≥1 named consumer.

**Phase 4 — Archive the mirror.** Once Phases 1+3 give a clean live view, move `Vault/` → `ARCHIVE/2026-06-2x_vault-mirror/` (archive, don't delete) and drop the `4dlab-vault` *rebuild* path from the architect boot ritual. Keep the frontmatter-schema reference (still authoritative for Phase 3). *Success:* no `build_lab_vault.py` in any routine; `_meta/PROVENANCE.md` no longer needs touching.

**Phase 5 — Launcher hygiene (optional).** Consider `--approval-mode write` in `run-*.sh` (coders auto-apply edits, still prompt on risky ops) and a per-coder `--config`/`--skills` overlay for scoping. *Success:* launchers unchanged-or-safer; inner loop still passes.

**Phase 6 — Scaling to N coders.** See §7.

---

## 7. Scaling from 2 → N coders

Each coder is an **omp profile** (isolated auth/sessions/settings) + an **identity file** + a **launcher**. Adding a coder is mechanical:

1. `omp --profile <name> --alias omp-<name>` once → creates a shell shortcut, isolates auth. Then `omp --profile <name>` → `/login` to its provider.
2. Add `.agent/coders/<name>/AGENTS.md` (copy an existing one; swap identity + the "don't touch the *other* coders" boundary) and an empty `.agent/coders/<name>/MEMORY.md`.
3. Add `run-<name>.sh` (copy `run-codex.sh`; swap `--profile` and the identity path).
4. **Mutual exclusion at scale:** the shared `.omp/rules/lane-guard-no-assignments.md` already blocks *any* coder from editing `assignments.md`. The Codex↔Agy "don't take each other's task / don't edit each other's dir" guard can't live in a shared rule (a project rule can't tell which coder is running) — it belongs in each coder's **profile** rules dir (noted as deferred in `.agent/rules/lane-guard.md`). For N coders, generate one per-profile rule per coder: "edits to `.agent/coders/<other>/**` → STOP."

**Worth building once:** a tiny `scripts/new_coder.sh <name> <provider>` that does steps 2–4 from templates, so coder #3..#N is a single command. Pure scaffolding, architect-lane, no lab impact. Flag for your approval before I spec it — it's the only net-new tooling this plan proposes.

---

## 8. Success criteria

- Opening `/agent_workspace` in Obsidian shows a clean `labs/`+`apps/` graph (no venv/ARCHIVE/cache/skill noise); the view is the live source, so it's never stale. ✔ measurable
- Coders launch from `/agent_workspace` and the new vault-awareness rule appears in `omp ttsr list`. ✔ measurable
- A coder's progress note for a real task contains at least one `[[WikiLink]]` that resolves in Obsidian backlinks. ✔ measurable
- The three `.base` views render against **live** notes; every framed note has ≥1 named consumer. ✔ measurable
- No coder can edit `Vault/**` (until archived) or run `graphify` (lane-guard). ✔ measurable via `omp ttsr test`
- Zero use of the disproven mechanisms: no `.omp_vault` symlink, no `.clauderules`, no reliance on a markdown boot-scan. ✔ by inspection
- Adding coder #3 is one command + login. ✔ measurable

---

## 9. Out of scope / deliberately not doing

- **`.omp_vault` symlink and any "force omp to index the vault" trick** — omp doesn't index; disproven §1.
- **Moving coders into `Vault/`** — it's not runnable; §3.
- **Maintaining the `Vault/` copy-mirror** — superseded by the live-root view (Option A); archive it (Phase 4), don't keep rebuilding it.
- **Re-graphifying anything** — graphs are frozen, architect-lane only.
- **Touching `apps/links.md`** — wrong-content file; left as-is unless you ask.
- **Implementing code in this plan** — architect lane; this is a spec. Phases 1–6 are ready to hand to a coder/your own session as task files on request.

---

## Appendix A — Verified omp 16.1.19 facts (this machine)

- Binary: `/home/m/.local/bin/omp`, `omp/16.1.19`. Session runs natively on the host (shared venv, no separate sandbox interpreter — matches `CLAUDE.md`).
- Flags (from `omp --help`): `--cwd`, `--profile`, `--alias`, `--append-system-prompt <text|file>`, `--system-prompt` (overrides), `--config` (repeatable overlay), `--tools`, `--no-tools`, `--no-lsp`, `--no-skills`, `--skills=<glob>`, `--no-rules`, `--approval-mode=always-ask|write|yolo`, `--no-extensions`.
- Subcommands: `omp config`, `omp ttsr` (`list` / `test`), `omp ssh`, `omp auth-gateway`.
- Config discovery loads from 8 tools across `.omp`, `.claude`, `.codex`, `.gemini`; native formats include Cursor MDC, Cline `.clinerules`, Codex `AGENTS.md`, Gemini `system.md`, Copilot `applyTo`. Internal schemes include `skill://`, `rule://`, `agent://`.
- TTSR rules: regex/AST-triggered, zero upfront context; `.omp/rules/*.md` discovered live (confirmed: 2 native + 18 builtin defaults).
- Built-in tools: `ask, bash, python, calc, ssh, edit, find, grep, ast_grep, ast_edit, lsp, notebook, read, browser, task, poll, todo_write, fetch, web_search, write, generate_image`.
- Memory: mnemopi (on-machine SQLite); `retain` / `recall` / `reflect`.

## Appendix B — Sources

- omp (oh-my-pi) README, AGENTS.md, releases — github.com/can1357/oh-my-pi (`README.md` fetched; TTSR / Universal Config Discovery / `--tools` sections verified).
- Live machine: `omp --version`, `omp --help`, `omp ttsr list` run in `/agent_workspace`.
- Repo evidence: `AGENTS.md`, `CLAUDE.md`, `run-codex.sh`, `run-agy.sh`, `scripts/wire_skills.sh`, `.omp/rules/*`, `.agent/rules/lane-guard.md`, `.agent/coders/*/AGENTS.md`, `Vault/VAULT_IMPLEMENTATION_PLAN.md`, `Vault/System-Map.md`, `Vault/_meta/PROVENANCE.md`, `.obsidian/community-plugins.json`.
- Article corpus (`apps/wired/obsidian-links.md`, root `links.md`): "Connecting Codex to an Obsidian Vault" (lucavettor/Medium); Codex-AI-Agent & Claudian Obsidian plugins (community.obsidian.md, claudian.xyz) — confirm AGENTS.md-as-contract, vault-as-working-dir, scheduled-maintenance patterns adopted in §4/§6.
