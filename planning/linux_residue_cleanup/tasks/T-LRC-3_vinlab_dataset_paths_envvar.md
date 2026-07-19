# T-LRC-3 — vinlab tools: Windows dataset paths → env-var + Linux default

**Pack:** Linux Residue Cleanup · **Lab:** VINLab · **Blocked by:** — (OWNER decision, see below) · **Status:** blocked
**Load skills:** `comlab-python` (or `vinlab-python` if present), `comlab-verification-loop`, `comlab-code-review`.

> **BLOCKED — owner input required before running.** These tools read an external `vehicle-data` /
> `DBS` dataset that lives **outside the repo**. The owner must confirm the Linux dataset root (or
> rule "env-var only, no default"). Record it in `LINUX_RESIDUE_CLEANUP_PROGRESS.md` §"Owner decisions",
> then flip this row to `pending`. Do not invent a path.

### Goal ###
Replace the hardcoded Windows dataset paths in the five VINLab tools with an environment variable
(`VEHICLE_DATA_ROOT`, plus the existing `DBS_ROOT`) resolving to the owner-confirmed Linux default,
so the tools run natively. Done when no `C:\…` literal remains in `labs/vinlab/tools/`, each tool
imports/compiles, the inner loop is green, and a tool honours the env var when set.

### Success criteria ###
- `grep -rnF 'C:\' labs/vinlab/tools/` returns **zero** lines.
- `.venv-wired/bin/python -m py_compile` on each of the five tools exits 0.
- `ruff check` and `pyright` on the five files are clean.
- Smoke: with `VEHICLE_DATA_ROOT=/tmp/vd` set, importing `build_vds_map` resolves its data path under
  `/tmp/vd` (not a `C:\` literal) — asserted in Verification.

### Context ###
`WINDOWS_RESIDUE_FOLLOWUPS.md` §"Needs a CODER" enumerates the offenders (confirm current line numbers
by grep before editing — line numbers drift):
- `labs/vinlab/tools/build_vds_map.py:25` — `Path(r"C:\Users\muto\claude\4DApp\vehicle-data\petrol_vin")`
- `labs/vinlab/tools/build_wmi_map.py:20` — same default
- `labs/vinlab/tools/extract_opsi_engine_codes.py:24` — `r"C:\Users\muto\claude\4DApp\vehicle-data"`
- `labs/vinlab/tools/tecdoc_ktype_bridge.py:22,31,35` — `vehicle-data`, `4DLab\DNALab\VINLab`, `ktype_bridge_map.csv`
- `labs/vinlab/tools/build_vref_db.py:34` — `DBS_ROOT` default `r"C:\DBS"` (already `os.environ`-overridable; just fix the default)
Pattern to follow: `ROOT = Path(os.environ.get("VEHICLE_DATA_ROOT", "<linux-default>"))` then build sub-paths
from `ROOT`. VINLab is isolated (no cross-lab imports) — touch only `labs/vinlab/tools/`.

### Consumer (signal/noise) ###
N/A — no new field/enum/fault. Runtime path config only.

### Deliverables ###
1. `labs/vinlab/tools/build_vds_map.py` — Windows path literal → `VEHICLE_DATA_ROOT` env + Linux default.
2. `labs/vinlab/tools/build_wmi_map.py` — same.
3. `labs/vinlab/tools/extract_opsi_engine_codes.py` — same.
4. `labs/vinlab/tools/tecdoc_ktype_bridge.py` — three path literals → env-derived.
5. `labs/vinlab/tools/build_vref_db.py` — fix `DBS_ROOT` default to the Linux default (keep override).

### Files to touch ###
- `labs/vinlab/tools/build_vds_map.py` (MODIFY)
- `labs/vinlab/tools/build_wmi_map.py` (MODIFY)
- `labs/vinlab/tools/extract_opsi_engine_codes.py` (MODIFY)
- `labs/vinlab/tools/tecdoc_ktype_bridge.py` (MODIFY)
- `labs/vinlab/tools/build_vref_db.py` (MODIFY)

### Out of scope ###
The relative-path tools that are already Linux-safe (`tecdoc_cyl_from_*.py`, `tecdoc_cylinder_enricher.py`,
`tecdoc_engine_enricher.py`) unless a grep shows a `C:\` literal in them. No dataset/logic changes, no new
features, no `4DLabV2/` prefix work (T-LRC-5). Surgical: every changed line is a path-source swap. GRAPH
GUARDRAIL: no graphify.

### Verification ###
```bash
cd /agent_workspace
# (a) no Windows absolute paths remain in vinlab tools
! grep -rnF 'C:\' labs/vinlab/tools/
# (b) each tool compiles
for f in build_vds_map build_wmi_map extract_opsi_engine_codes tecdoc_ktype_bridge build_vref_db; do
  .venv-wired/bin/python -m py_compile "labs/vinlab/tools/$f.py" || exit 1
done
# (c) inner loop
.venv-wired/bin/ruff check labs/vinlab/tools/
.venv-wired/bin/pyright labs/vinlab/tools/
# (d) env var honoured
VEHICLE_DATA_ROOT=/tmp/vd .venv-wired/bin/python -c "import os,importlib; os.environ.setdefault('VEHICLE_DATA_ROOT','/tmp/vd'); m=importlib.import_module('labs.vinlab.tools.build_vds_map'); print('env honoured')"
```
All steps must pass.

### Progress hook ###
`LINUX_RESIDUE_CLEANUP_PROGRESS.md` T-LRC-3: Status=done, Verification="vinlab tools env-var driven; no C:\\ remains; inner loop green".
