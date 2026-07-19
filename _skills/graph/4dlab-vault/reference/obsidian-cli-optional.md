# Obsidian CLI — OPTIONAL, query-only

> Read this only if you actually run Obsidian desktop. The vault is **built by
> file tools**; the CLI is never required to build or maintain it. This file
> exists so that *if* you have the CLI, you can script the post-build checks.

## Preconditions (all must hold)

- Obsidian desktop **v1.12+** is running (the CLI talks to it over IPC).
- CLI enabled: Settings → Command line interface → ON.
- **Windows:** `Obsidian.com` redirector sits next to `Obsidian.exe`, and you
  run from a **normal-privilege** terminal (admin terminals fail silently). Git
  Bash resolves `obsidian` to the `.exe` — make a wrapper or use PowerShell.

If colon subcommands return exit 127, the redirector is missing or the shell is
resolving the GUI binary — see `Vault/ObsidianCLI.md` troubleshooting. When in
doubt, skip the CLI; the build does not need it.

## The only commands worth using here

All paths are **vault-relative**. These are the post-build sanity checks that
map to our success criteria:

```bash
obsidian orphans                       # notes with no links in/out — should be ~none
obsidian unresolved                    # broken wikilinks — fix these
obsidian search query="consumers:" path="labs"   # spot notes missing consumers
obsidian base:query path="_bases/consumers.base" # run the signal/noise view headless
obsidian backlinks path="labs/obdlab/docs/DLD_OBDLab.md"
```

Use them to confirm: no unexpected orphans, no unresolved links, and every wiki
note shows a consumer. That's it — everything else in the CLI surface
(`daily:*`, `sync:*`, `themes`, `templates`) is out of scope for this vault.

## What NOT to use the CLI for

- **Building the vault.** Use `scripts/build_lab_vault.py`. The CLI's
  `create`/`property:set` store list values as plain strings, which would
  corrupt our `consumers` / `implements` arrays.
- **Editing wiki notes.** They are mirrors; edit the lab and rebuild.
