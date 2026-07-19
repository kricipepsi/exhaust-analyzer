# HANDOFF — next coder session: T-COM-PATHS-1

**Why this is next:** `T-COM-GRAPH-AST` is `done` (2026-06-28, architect lane — graph builds can't run in a
coder session because `lane-guard-no-graphify` blocks the literal `graphify`). With the graphs built, the
COM vault chain's next runnable step is **T-COM-PATHS-1** (coder/vault lane, no blockers). It unblocks the
final author-lane step, `T-COM-VAULT`.

```
T-COM-GRAPH-AST ✅ done → T-COM-PATHS-1 (coder, THIS handoff) → T-COM-VAULT (author, after PATHS-1)
```

---

## Paste-ready prompt for the coder session

> You are a coder (Codex/Agy) on the 4DLab project. Boot order: read `Vault/tasks/COM_VAULT_TASKS_START_HERE.md`
> first (the COM vault pack rules), then your task spec `Vault/tasks/T-COM-PATHS-1_register_comlab_source_paths.md`.
> Load **only** the skills on the PATHS-1 ledger row: `4dlab-vault`, `comlab-python`.
>
> **Your task: T-COM-PATHS-1** — register COMLab's source paths in the vault build script so a COM vault
> build can find the right folders. This is vault-tooling, not lab diagnostic code: **no graphify, no
> re-extraction, no lab inner-loop/test edits.** Edit + dry-run prove-out only.
>
> The whole change is two edits in `_skills/graph/4dlab-vault/scripts/build_lab_vault.py`:
>   1. Add a `comlab` entry to `LAB_SRC_PATHS` (~line 44), mirroring the `dtclab` entry — wiki at
>      `labs/comlab/wiki/`, and `required_graph_tiers: ("v2_code", "v2_tests")` only (prose graphs are
>      waived for this pack).
>   2. Add `comlab` to the provenance "waived" branch (~line 357) so PROVENANCE.md reads the
>      `v2_wiki/v2_docs waived` note.
>   The exact code blocks are in the task spec's "Exact change" section. If more than these two edits are
>   needed, scope only the minimal change that lets `--dry-run --lab comlab` resolve and flag the rest as a
>   follow-up — do not enlarge the diff.
>
> **Environment:** Python 3.14 only, via the shared venv. Call `/agent_workspace/.venv-wired/bin/python`
> directly (never bare `python`/`python3` — the system default is 3.12).
>
> **Prove it (the task's verification block):**
>   - Capture `--dry-run` output for `obdlab` and `dtclab` **before** your edit, then again after; they must
>     be **byte-identical** (regression guard — you must not change other labs).
>   - `--dry-run --lab comlab` must now **resolve** `wiki/` and require only `v2_code`/`v2_tests` — no
>     spurious `research/chunks` or `v2_wiki`/`v2_docs` abort. (The two AST graphs already exist as of
>     2026-06-28, so the eligibility check passes — it will not report graphs-not-built.)
>   - The `source:` provenance for a COMLab wiki note reads `labs/comlab/wiki/<note>`; PROVENANCE shows the
>     waived note.
>     ```bash
>     cd /agent_workspace
>     for lab in obdlab dtclab; do
>       .venv-wired/bin/python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab $lab --repo "$PWD" --dry-run > /tmp/${lab}_before.txt
>     done
>     # ...make the two edits...
>     for lab in obdlab dtclab; do
>       .venv-wired/bin/python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab $lab --repo "$PWD" --dry-run > /tmp/${lab}_after.txt
>       diff /tmp/${lab}_before.txt /tmp/${lab}_after.txt && echo "OK $lab unchanged"
>     done
>     .venv-wired/bin/python _skills/graph/4dlab-vault/scripts/build_lab_vault.py --lab comlab --repo "$PWD" --dry-run | head -40
>     ```
>
> **When done:** fill `VERIFICATION GATE` (OBD+DTC dry-runs unchanged; COM dry-run resolves wiki/ + two
> tiers; provenance correct) and `CODE REVIEW` (minimal two-line diff) in
> `Vault/tasks/progress_notes/T-COM-PATHS-1.md` (open with the confirmed `## Plan`), flip the
> `T-COM-PATHS-1` row in `COM_VAULT_TASKS_START_HERE.md` to `done`, then STOP. One task per session.

---

## After PATHS-1 lands (for the manager)

`T-COM-VAULT` becomes runnable — it's **author lane** (not a coder), loads `4dlab-vault` +
`comlab-vault-prep` + `comlab-verification-loop`, and authors `vault-map.comlab.yaml` + dry-run + the real
build + bases. That's the last step in the COM vault pack.
