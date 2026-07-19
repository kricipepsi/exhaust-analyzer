# Registry revival audit — `labs/comlab/registry/` — 2026-06-20 (architect, Cowork)

**Why:** you moved the v2 registry out of `ARCHIVE/` into `labs/comlab/registry/` and asked for an audit *before* it's trusted by the new version, so obsolete files don't leak in. This is that audit. Verified on the mandated interpreter (`.sandbox-py`, Python 3.14.5).

## Headline

- **The move already fixed the blocker.** With `registry` importable in-lab, `from registry.integration_shim import …` resolves and the **2 previously-failing tests now pass** (`tests/unit/test_fault_atlas_router_v2.py` → 4 passed). The full suite should now be **0 failed** (coder to confirm). DELTA-2's hard blocker is cleared.
- **But the folder carries obsolete baggage** that should not ride into the new version. One item is a real latent bug (`ignition_fault`); the rest is caches, stale bytecode, and a parallel project's process docs sitting at the lab's import root.
- **I could not delete anything** — the sandbox mount refuses deletes (`Operation not permitted`). All PURGE/RELOCATE actions below are **host-side, for the coder.**

## Classification

### KEEP — the runtime module (firewall-clean v2 registry)
`__init__.py` · `integration_shim.py` (Jun 12, the entry `route_case_with_diagnostics`) · `schema_v2.py` · `shim/payload_mirrors.py` (the local Pydantic mirrors that keep the no-COMLab-imports firewall) · `rules/` (the 15 rule files named in `_EXPECTED_RULE_FILES`).

### PURGE — caches + stale bytecode (the actual injection vector)
`__pycache__/` (all levels) · `.pytest_cache/` · `.ruff_cache/`. These hold **30 `cpython-312` + 4 `cpython-313` `.pyc`** — bytecode from Python versions the repo forbids (3.14-only). Stale `.pyc` can shadow a source edit and silently run old code. **Coder, run on the host:**
```powershell
# PowerShell, from C:\Workspace\labs\comlab\registry
Get-ChildItem -Recurse -Directory -Include __pycache__,.pytest_cache,.ruff_cache | Remove-Item -Recurse -Force
```
```bash
# or bash
find . -type d \( -name __pycache__ -o -name .pytest_cache -o -name .ruff_cache \) -exec rm -rf {} +
```

### RESOLVE — latent bug: the `ignition_fault` orphan
`rules/` has **16** JSON files; the shim's `_EXPECTED_RULE_FILES` lists **15** — **`ignition_fault.json` is not in it** — yet `schema_v2.py:94` defines `IGNITION_FAULT = "ignition_fault"`. Effect: in **production** (default `expected_files=_EXPECTED_RULE_FILES`) the rule is **never loaded**; in **test mode** (`expected_files=None`, which globs `*.json`) it **is** loaded. So registry's own tests exercise a rule production ignores — a v1/v2 divergence hiding in plain sight. **Decide one:**
- if `ignition_fault` is a real fault family → add `"ignition_fault.json"` to `_EXPECTED_RULE_FILES` (and confirm rule quality), **or**
- if vestigial → remove `rules/ignition_fault.json` **and** the `IGNITION_FAULT` enum member.

This is the clearest "obsolete file injecting into the new version" — handle before DELTA-2 wires anything to the shim's output.

### RELOCATE — non-runtime docs/tasks at the lab import root
Move out of `registry/` (to `registry/docs/` or `ARCHIVE/`, per "archive never delete"); they are a parallel project's process files and risk confusing the boot drill / manager pipeline — note the **duplicate `START_HERE` and `PROGRESS`** inside a lab:
`CHEMISTRY_COVERAGE.md` · `CORPUS_AUDIT.md` · `REGISTRY_AUDIT.md` · `REGISTRY_PROGRESS.md` · `REGISTRY_START_HERE.md` · `REGISTRY_START_HERE_AUDIT_RESPONSE.md` · `SCHEMA_V2_SPEC.md` · `Vol5.md` · `cvsgaps.md` · `registry_tasks/` (old REG-V2 + AUDIT task files — registry is already built) · `_registry_skills/` (skill defs; not imported — move under `.claude/skills/` or archive).

### REVIEW — your call, low risk
- **`pyrightconfig.json`** = `{"extraPaths": [".."]}`. A *second* pyright config inside the lab; pyright uses the nearest config, so analyzing `registry/` uses this, not `pyproject.toml [tool.pyright]`. Harmless (it makes `registry` resolve standalone) but it's a duplicate. Keep, or fold the path into `pyproject` and delete.
- **`corpus_curated.csv` (188K) + `corpus_meta.json` (136K) + `tools/build_corpus.py` + `tests/test_build_corpus.py`.** **Not runtime** — the shim loads `rules/`, never the corpus. Stale (May 31). Keep only if you still want the corpus-build tests; otherwise archive the heavy data.

## Integration follow-ups (after cleanup — not this audit)
1. Decide whether `registry/tests/` joins the COMLab inner loop (they validate the rule JSON).
2. Confirm the full suite is `0 failed` on the mandated interpreter once caches are purged.
3. Then DELTA-2 can proceed against a clean, importable registry.

## What I changed
Nothing deleted (sandbox can't). No source edited. This report only.
