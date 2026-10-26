# P5 — deploy_surface (dependency and deploy surface)

- target: P5, the instrument pipeline. Question: does what Render builds equal what the app imports, and what does the runtime pull in?
- git sha: `6f73135` (audit-r1). Production code (`labs/`, `apps/`, `requirements.txt`, `render.yaml`, `app.py`) is identical to `origin/main` @ `8463d21` (`git diff --stat origin/main HEAD -- labs apps requirements.txt render.yaml app.py` is empty).
- date: 2026-10-26. Time spent: about 30 minutes wall-clock, 19:43 to 20:13 UTC.
- baseline: `bash audit/tools/baseline.sh` gives the same pytest counts per package as `audit/reports/baseline_20261017.txt`: comlab 522 passed, 4 skipped, 2 errors; dnalab 27; dtclab 590; gaslab 208/2/4; obdlab 388/2; symptomlab 63; vinlab 203/8; wired 11. Only the git line and the timings differ. The erosion and isolation sections did not change either (4 violations).
- scope ruling for `apps/vault`: it has no top-level README. `apps/vault/audit/reports/README.md` and `VAULT_LIVE_START_HERE.md` describe it as a vault-tooling and frontmatter lane, and `find apps/vault -name '*.py'` returns nothing. It holds no Python, no manifest is built from it, and the deployed closure never imports it. **Excluded** from sections 1–4. **Included** in the secret scan (section 5), which covers every tracked file.
- `labs/vinlab/tools`: the inventory reports it separately as offline builders (15 files). It is outside the deployed closure.

## Instrument

`audit/scratch/P5/`:

- `render_build.sh`: rebuilds Render from `render.yaml`. Steps: `git archive origin/main`, then CPython **3.14.3** (`PYTHON_VERSION`), then a fresh venv, then the build command `pip install -r requirements.txt` unmodified (pip 25.3, bundled).
- `cases.py`: runs inside that venv, one process per case. It uses `streamlit.testing` AppTest on the root `app.py` shim, which reaches `build_diagnose_payload()` → `wired.composition.diagnose()` exactly as the page does. A `sys.addaudithook` records subprocess, socket, file-write and sqlite events and attributes each one to the innermost first-party frame.
- `surface.py`: writes `surface.json`. Sections:
  - 0: start command
  - 1: UI cases
  - 2: import inventory, plus a requires-python probe
  - 2c: first-party distribution names against PyPI
  - 3: pip-audit
  - 4: capability census
  - 5: secret census
- `controls/`: planted fixtures. The secret-scan control values are built at run time and never stored.

Run: `P5_RENDER=<dir> P5_PIPAUDIT=<pip-audit> P5_PY310=… P5_PY311=… python audit/scratch/P5/surface.py`.

**Determinism**: run twice, then `cmp audit/scratch/P5/surface.json <run1 copy>` reports no difference (the output is identical).

**Controls** (all from the committed `surface.json`):

| section | positive control (must flag) | flagged | clean control (must not flag) | flagged |
|---|---|---|---|---|
| 1 cases / audit hook | page running `subprocess.run`, a temp-file write, and user text in `unsafe_allow_html` | yes | same page with `html.escape` and no subprocess or write | no |
| 2 inventory | pkg importing `yaml` undeclared, declaring `requests` unused | yes | declares `pyyaml`, imports `yaml` | no |
| 2c names | `requests` exists on PyPI | yes | `p5-no-such-dist-zq9x` | no |
| 3 pip-audit | `requests==2.19.0` (CVE-2018-18074) | yes | `six==1.17.0` | no |
| 4 capabilities | subprocess, socket, `write_text`, `open('a')`, `unsafe_allow_html`, `components.html` | yes | read-only `open`, plain `st.markdown` | no |
| 5 secrets | firecrawl-shaped key, assigned `api_key`, `.env` file | yes | `"fc-color"`, `os.environ[...]`, `<your-password>` | no |

The clean control in section 1 failed on the first run. A `<frozen importlib>` pseudo-path resolved inside the Render tree and was counted as first-party. I fixed the attribution and re-ran; all twelve outcomes above come from the fixed instrument.

## 1. Render build simulation and the three UI drives

- **Build**: exit 0. 48 third-party distributions plus 8 editable first-party (7 labs and `wired`); `pip freeze` is in `surface.json` → `render_dists`. The audit venv (uv, the same day) resolves the same version for every shared distribution (diff empty).
- **Start command**: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0` with `PORT=8599`, cwd at the tree root. `/_stcore/health` returned `200 ok`, `/` returned `200`, and the server log had no `Error` or `Traceback` lines.
- **sys.path modes**:
  - *faithful*: what `streamlit run` builds, with the script directory (the repo root) first.
  - *comlab*: faithful plus `labs/comlab`, the F-C1-5 work-around.

| case | what the user does | faithful (as deployed) | comlab work-around | listed finding |
|---|---|---|---|---|
| blank | open the page, click Run | `Diagnostic calculation failed: build_vehicle_dna: missing required triage keys: ['tier_1', 'tier_2']` | same | F-C4-9 (identical to the live text recorded 2026-10-17) |
| unticked | untick GASLab, OBDLab, DTCLab, DNA/VIN; Run | `… missing required triage keys: ['tier_1', 'tier_2', 'occurs_during', 'engine_state', 'load_state']` | same | F-C4-9 (with DNA off, five keys are missing) |
| minimal | OBDLab and DTCLab unticked (F-C5-2); symptom "Lack of Power / Flat always"; 5 gas HC 80, CO 0.3, CO₂ 14.8, O₂ 0.3, NOx 50; no VIN | `Diagnostic calculation failed: No module named 'registry'` | `EF-004 ecu_fault conf=0.90 abstained=False mode=FULL_FUSION` | F-C1-5 / F-C4-1; work-around: F-C1-1, F-C1-11 |
| minimal_vin | as minimal, with VIN `WME01MC01XH072806` | `No module named 'registry'` | `EF-004 ecu_fault 0.90 FULL_FUSION` | same |

**Comparison with T-AUD-1** (F-C1-5, F-C4-9, F-C5-1, F-C5-2, F-C5-13, R1-L1):

- F-C1-5 was UPHELD with the note "Live run did not reach it (failed earlier on F-C4-9)". The deployed page does reach it: F-C4-9 masks it only while no symptom is picked. A user who picks a symptom and types a valid 5-gas sample gets `No module named 'registry'` on every run, with or without a VIN. This adds reach evidence to an already listed finding; it is not a new finding.
- With the work-around in place, a stoichiometric sample with OBD and DTC switched off is reported as a 0.90 ECU fault in `FULL_FUSION` mode. Both are already listed (F-C1-1 healthy→fault, F-C1-11 degradation mode).
- Not driven here: F-C5-1 (blank gas field with a symptom picked), F-C5-2 (OBD/DTC ticked), F-C5-13 (malformed DTC token), R1-L1.

## Findings

### F-P5-1 — Two first-party distribution names are taken on PyPI; `wired` depends on `dnalab` by bare name, so one missing `-e` line deploys a stranger's 2021 package
severity: MEDIUM
kind: security (supply chain)
anchor: `apps/wired/pyproject.toml:10-18` — `dependencies = [ "comlab", "dnalab", … ]` (no version, no source)
claim violated: `requirements.txt:2` — "Labs + wired installed editable from this repo"
repro: `python audit/scratch/P5/surface.py` (section `2c_dist_names`); manual equivalent: `grep -v labs/dnalab requirements.txt > r.txt && pip install --dry-run --report rep.json -r r.txt`
probe: `audit/scratch/P5/surface.py::section_names`
observed:
- PyPI `dnalab` exists: 0.1.0, wheel and sdist uploaded 2021-02-22, no summary and no project URL.
- PyPI `wired` exists: 0.4, an unrelated IoC container. The other six lab names return 404.
- Dry run with the `-e labs/dnalab` line removed: `dnalab: pypi 0.1.0`, while every other first-party dist stays `local-editable`. pip reports no error.
- Today's full build is correct: `pip freeze` shows `dnalab` as the local editable 1.0.0.

expected: first-party requirements that cannot resolve to PyPI, for example direct references (`dnalab @ file:…`) or a constraints file. The way it is written today, a later edit to the manifest can swap in third-party code without any error.

### F-P5-2 — The deployed closure is unpinned: 47 of 48 third-party distributions float, and there is no lockfile or constraints file
severity: MEDIUM
kind: robustness
anchor: `requirements.txt:2-4` — "third-party deps resolve transitively (pydantic, pyyaml). Streamlit pinned to the version smoke-tested in-repo." / `streamlit==1.59.0`
claim violated: same line. Only streamlit is held to the smoke-tested version; everything that streamlit, pydantic and PyYAML pull in is whatever PyPI serves on the build day.
repro: `python audit/scratch/P5/surface.py` → `2_inventory.deployed_closure`, `spec_matrix`
observed: `{'third_party_dists': 48, 'pinned_by_a_manifest': ['streamlit'], 'unpinned_transitive': 47, 'lockfile': []}`. Today's build resolves pydantic 2.14.1, PyYAML 6.0.3, pillow 12.3.0, starlette 1.10.0, uvicorn 0.54.0 and others. No repo file records which set the 2026-07-19 published build ran, so the drift since then cannot be measured (UNDECIDED). pydantic carries three different specs and no pin: comlab `>=2.6,<3.0`, dtclab and obdlab `>=2.5`, gaslab `>=2`. The resolved version satisfies all of them (`resolved_violates` is empty for every dist).
expected: a reproducible deploy set (a lock or constraints file generated from a tested venv).

### F-P5-3 — pip-audit: pillow 12.3.0 in the deployed closure has 37 advisories and cannot be upgraded without a streamlit bump; the build tool pip 25.3 has 5
severity: LOW (pillow is not reached by app code; see reach)
kind: security
anchor: `requirements.txt:4` — `streamlit==1.59.0`, which requires `pillow<13,>=7.1.0` (`importlib.metadata.requires('streamlit')`)
claim violated: none stated. This is the known-vulnerable count the prompt asks for.
repro: `python audit/scratch/P5/surface.py` → `3_pip_audit`. pip-audit 2.10.1 with `-r <frozen closure> --no-deps -s pypi`, querying PyPI on 2026-10-26.
observed:
- Status RAN: 48 distributions audited, 0 skipped, 37 matches, all `pillow 12.3.0`, all fixed in 13.0.0. The ids are CVE-2026-96636…96644, CVE-2026-96778, CVE-2026-112390…112406 (with gaps), CVE-2026-112891…112901 (with gaps), CVE-2026-114501, and GHSA-78g4-xqwv-q3g8. The full list with GHSA aliases is in `surface.json`.
- Build tool `pip 25.3`: PYSEC-2026-1796 (CVE-2026-1703), PYSEC-2026-196 (CVE-2026-8643), PYSEC-2026-2875 (CVE-2026-3219), PYSEC-2026-2876 (CVE-2026-6357), PYSEC-2026-3721 (CVE-2026-13346). Fixed in 26.0 to 26.2. These matter at build time only, and the inputs are this repo plus PyPI.

reach (pillow): **not reached by this app's code**. `apps/ui/app.py` has no `st.image`, `file_uploader` or `camera_input` (grep returns nothing), and `page_icon` is the emoji `"🔧"`. `PIL` is absent from `sys.modules` after every case in section 1. The only importer in the closure is `streamlit/elements/lib/image_utils.py`. Server-side code paths that AppTest does not run are **UNDECIDED** (the real server was only health-checked).
expected: no known-vulnerable distribution in the closure, or a recorded acceptance. The pillow advisories are reportable for the record even though the app does not reach pillow.

### F-P5-4 — `dnalab` declares no dependencies but imports `vinlab` and `symptomlab` at import time; installed from its own manifest it cannot be imported
severity: LOW
kind: contract
anchor: `labs/dnalab/pyproject.toml:5-8` — `name = "dnalab" … requires-python = ">=3.12"` (no `dependencies`); `labs/dnalab/dnalab/assembly.py:7-9` — `from symptomlab import resolve …`, `from vinlab import decode …`
claim violated: `labs/dnalab/docs/ADR_DNALab.md` ADR-0002 — "`dnalab → vinlab + symptomlab`" (the dependency is sanctioned but undeclared)
repro: `python3.14 -m venv v && v/bin/pip install labs/dnalab && v/bin/python -I -c "import dnalab"`
observed: `ModuleNotFoundError: No module named 'symptomlab'`. The deployment works only because the root `requirements.txt` installs all labs. `apps/wired/pyproject.toml` declares `symptomlab`, which `wired` never imports (inventory `declared_unused: ['symptomlab']`); it is there to cover dnalab's gap. Not the same as R0-3, which concerns the rule-5 wording, not the manifest.
expected: dnalab's pyproject lists `vinlab` and `symptomlab`.

### F-P5-5 — COMLab claims `requires-python >=3.10`; pip installs it on 3.10, and the package then fails to import
severity: LOW
kind: contract
anchor: `labs/comlab/pyproject.toml:10` — `requires-python = ">=3.10"`
claim violated: the same line (an installable claim).
repro: `python audit/scratch/P5/surface.py` → `2_inventory.requires_python_probe` (installs each lab on the oldest interpreter it admits, then imports every submodule)
observed: comlab on 3.10: `install_ok: true`, `import_all_ok: false`, `ImportError: cannot import name 'StrEnum' from 'enum'`. dtclab, gaslab, obdlab, symptomlab and vinlab on 3.11: install and import OK. dnalab (`>=3.12`) and wired (`>=3.14`) were not probed.
expected: `>=3.11` or higher.

### F-P5-6 — The tracing install hint names a `[tracing]` extra that no manifest defines; `opentelemetry` is imported at 11 sites and declared nowhere
severity: LOW
kind: doc-drift
anchor: `labs/comlab/comlab/observability/_tracer.py:118` — `'pip install -e ".[tracing]" --break-system-packages. '`
claim violated: the same hint. `labs/comlab/pyproject.toml` `[project.optional-dependencies]` has only `dev`.
repro: `python3.14 -m venv v && v/bin/pip install --dry-run "labs/comlab[tracing]"`
observed: `WARNING: comlab 0.1.0 does not provide the extra 'tracing'`. The inventory classifies `opentelemetry` as UNADJUDICATED (installed nowhere, so no distribution can be named): 7 sites in comlab, all guarded or lazy (`_tracer.py:107-113, 177`, `fault_atlas_router.py:152`), and 4 `find_spec`/`import_module` literals in `wired/tracing.py`. Runtime impact: none, because `render.yaml` does not set `OTEL_TRACES_EXPORTER`, so the no-op tracer is used. This relates to R0-4 (tests need opentelemetry), but R0-4 concerns the test suite, not this hint.
expected: a `tracing` extra listing the OTel API, SDK and OTLP-gRPC exporter, or a hint that names the real packages.

### F-P5-7 — Lab manifests disagree with each other and mix test tools into runtime requirements
severity: LOW
kind: contract
anchor: `labs/comlab/requirements.txt:3-4` — `pytest>=8.0`, `pytest-cov>=5.0` (no section header, so read as runtime, next to pydantic and PyYAML)
claim violated: `labs/comlab/pyproject.toml:12-15` — runtime `dependencies = ["pydantic>=2.6,<3.0", "PyYAML>=6.0"]`, test tools under `[dev]`
repro: `python audit/scratch/P5/surface.py` → `2_inventory.packages.*.pyproject_vs_requirements`, `spec_matrix`
observed:
- comlab: `only_requirements: ['pytest', 'pytest-cov']`.
- symptomlab: `pyyaml: pyproject '' vs requirements '>=6.0'`.
- pyyaml specs across manifests: `>=6.0` in comlab, obdlab and symptomlab/requirements; unconstrained in dtclab, gaslab and symptomlab/pyproject.
- pydantic floors: `>=2`, `>=2.5`, `>=2.6,<3.0`; only comlab caps at `<3`.
- vinlab: `requirements.txt` "Runtime — none. stdlib only" agrees with the pyproject and the inventory (0 third-party imports).

None of these affects the Render build, which installs from the pyprojects through the root file.
expected: one source of runtime dependencies per lab, and matching specs across labs.

### Already listed (instrument evidence, no new finding)

| observation in this run | dup-of | what this instrument adds |
|---|---|---|
| deployed page, symptom picked and valid gas → `No module named 'registry'`; inventory: `registry` is imported by comlab (`fault_atlas_router.py:1953`), declared by no manifest (`<no-dist:registry>`), and itself imports undeclared `pydantic` (3 sites) | F-C1-5 (= F-C4-1) | proves the deployed UI reaches it on a first valid use (the ledger says the live run did not reach it) |
| blank form, and every module unticked → `missing required triage keys` | F-C4-9 | message is byte-identical to the live text; DNA off widens it to 5 keys |
| with the work-around: stoichiometric gas, OBD and DTC off → `EF-004 ecu_fault 0.90`, `FULL_FUSION` | F-C1-1, F-C1-11 | — |
| `apps/ui/app.py` imports `vinlab` (inventory `ui.used_dists.vinlab`, guarded) | F-C5-12 | — |
| `_skills/firecrawl-web-scraping-search/API.md`: 1 `firecrawl_key` match in the **`origin/main` tree** (6,434 files); 0 in the audit-r1 tree (6,517); 2 commits in history (`8463d21`, `a4074f4`) | R0-1 | the untrack and gitignore exist only on audit-r1; **production `main` still tracks the key, and Render's build checkout contains it**. Streamlit static serving is off by default, so it is not served over HTTP |
| `google_api_key` (6 files) and `assigned_secret` (`apiKey`, 2 files) in `labs/comlab/research/**` saved Gemini pages | R0-6 | the `apiKey` assignments in `lazy.min.js.download` are the same Google web-client noise |

## Capability surface (section 4, and dynamic events from section 1)

- Population: 87 first-party files, the static import closure of root `app.py`, including lazy imports and `labs/comlab/registry`. Unit: call site.
- Static hits: `file_write` 4, `unescaped_html` 6. No subprocess, socket, eval/exec, pickle or `yaml.load` site.

| sink | site | user input reaches it? |
|---|---|---|
| `sqlite3.connect` | `labs/vinlab/vinlab/db/tecdoc_query.py:33, 65, 80, 98` | Yes. The VIN text field leads to `vinlab.decode` and then a lookup by engine code. Every URI is `file:…vref.db?mode=ro`, and every query is parameterised (`WHERE engine_code = ?`). The audit hook saw `?mode=ro` at runtime, so no write and no SQL built from strings. |
| `st.markdown(unsafe_allow_html=True)` | `apps/ui/app.py:142` (CSS), `:695` (spacer) | No (constant strings) |
| same | `apps/ui/app.py:961, 981, 999, 1020` (verdict and sibling cards interpolating `fault_code`, `fault_name`, `fault_family`, `display_headline`, `fault_id`) | Not by the taint probe. The marker `<b id=p5taint>P5TAINT</b>` went into every free-text widget available when OBD and DTC are unticked (`Free-text notes`). 4 unsafe-HTML elements rendered and 0 contained the marker. The DTC and Monitor-ID text inputs were **not** tainted, because a run with DTCLab ticked cannot complete (F-C5-2). For those inputs: **UNDECIDED** |
| runtime first-party events (audit hook, all cases) | only the two read-only sqlite connects above | — |
| third-party (the framework surface) | `streamlit`, `uvicorn`, `starlette`, `websockets` and `anyio` serve the socket the browser talks to (that is the input surface itself); GitPython (`git`, 8 files importing subprocess) is used by streamlit; `requests`/`urllib3` are present | Only through Streamlit's own widget protocol. No first-party code opens a socket or starts a process. |
| env-gated egress | `comlab/observability/_tracer.py`: OTLP gRPC to `OTEL_EXPORTER_OTLP_ENDPOINT` when `OTEL_TRACES_EXPORTER` is set | No. It is environment-controlled, not set in `render.yaml`, and the SDK is not installed. |

## Census accounting (mechanism · unit · population · blind spot)

- **Import inventory** — ast walk of every `.py` file (tests excluded) in the 9 production package roots and `apps/ui/{app,ui_payload}.py`. Counts `Import`, `ImportFrom` (level 0), and `import_module`/`__import__`/`find_spec` with a literal argument. Unit: import site and distribution.
  - Totals: comlab 111 sites, registry 31, dnalab 17, dtclab 70, gaslab 50, obdlab 69, symptomlab 14, vinlab 41, wired 46, ui 8.
  - Non-literal dynamic imports: 0 in every package.
  - **UNADJUDICATED**: 11 sites (comlab `opentelemetry` 7, wired `opentelemetry` 4), plus 9 in the offline `vinlab/tools` (`mysql` 6, `tools` 3).
  - Blind spot: code reached only through `exec` or `runpy` strings (the root shim's `runpy` target is covered explicitly); vendored code.
  - The root `requirements.txt` reports `comlab`, `dnalab`, `dtclab`, `gaslab`, `obdlab` and `symptomlab` as "declared, unused" by `apps/ui`. That is expected: the root file is the deploy manifest and has to install wired's dependencies editable. It is not a defect.
- **pip-audit** — RAN, 48/48 audited.
  - Blind spot: the editable first-party labs (not on PyPI), advisories missing from PyPI/OSV, and reachability (decided by hand above).
- **Capability census** — ast call sites over 87 files, plus audit-hook events from 5 cases × 2 modes.
  - Blind spot: aliased callables (`x = subprocess.run; x()`) and sinks reached only inside third-party code. Plain `st.markdown` is excluded on purpose (Streamlit escapes it).
- **Secret census** — 11 regex kinds plus credential file names over all tracked text blobs.
  - Populations: HEAD (6,517 files, 0 unreadable, 0 credential-named files) and `origin/main` (6,434 files).
  - History: only a firecrawl pickaxe (2 commits).
  - Blind spot: binary blobs, encoded or split secrets, kinds without a regex, and other kinds in history.

## Approaches that found nothing

- Spec conflicts: every resolved version satisfies every manifest spec that names it (`resolved_violates` is empty for all 10 named distributions).
- Python version: `.python-version` `3.14` agrees with `render.yaml` `3.14.3`, and the build and start ran on 3.14.3.
- Build closure versus audit closure: the uv and pip resolves on the same day give the same versions.
- Untracked or extra files: the Render tree is `git archive origin/main`, the build needed nothing untracked, and `vref.db` and the other data files are tracked.
- First-party subprocess, socket, eval/exec, pickle or unsafe YAML: 0 sites. All YAML loads were checked as part of that census.
- Runtime file writes by first-party code during the cases: 0 (audit hook).

**Not examined**:
- A browser-driven run against the live server (only the health endpoint and `/` were fetched).
- Memory and CPU limits of the Render free plan.
- The `dnalab` 0.1.0 package contents (deliberately not downloaded or executed).
- History scans for kinds other than firecrawl.
- The requires-python claims of dnalab (`>=3.12`) and wired (`>=3.14`).
- UI cases with OBD/DTC ticked, malformed DTC tokens, and blank gas with a symptom picked (already covered by F-C5-1, F-C5-2 and F-C5-13).

findings: H=0 M=2 L=5
