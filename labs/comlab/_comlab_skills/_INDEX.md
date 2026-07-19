# COMLab Skill Bundle — Master Index

**Version:** 1.0 (2026-06-21 — Stage-4 build; COMLab is built LAST)
**Last updated:** 2026-06-21
**Bundle root:** `labs/comlab/_comlab_skills/`

This index is the only place a coder session needs to look to know which skills
exist, which are mandatory at session start, and which to load on demand for a
given task. `COMLAB_TASKS_START_HERE.md` reads this file at boot (Step 1, before
picking a task). The pattern mirrors `_obdlab_skills/_INDEX.md` and
`_dtclab_skills/_INDEX.md`. New skills are authored per the trigger rules in
`_skills/coding-bootstrap/reference/custom-skill-authoring.md`.

---

## Mandatory at every session start (3 skills)

| # | Skill | Path | Purpose |
|---|---|---|---|
| 1 | **comlab-python** | `_comlab_skills/comlab-python/SKILL.md` | Python 3.14 house style + Immediate Checklist + per-file Inner Loop (syntax → ruff → pyright → targeted pytest). COMLab-scoped: fusion-spine consumes *verdicts* not sensors, no cross-lab imports (mirror types locally), signal/noise named-consumer rule, wiki-provenance citations, default-off flag pattern. |
| 2 | **comlab-verification-loop** | `_comlab_skills/comlab-verification-loop/SKILL.md` | 6-phase outer gate (syntax → type → lint → pytest → **wiki/anti-orphan guard** → diff review). Phase 5 is COMLab-specific — every numeric/enum cites a wiki §, and every contracted consumer field is grep-confirmed read in a live path (anti-orphan). Owns the `VERIFICATION GATE` block. |
| 3 | **comlab-code-review** | `_comlab_skills/comlab-code-review/SKILL.md` | Per-diff self-review producing the `CODE REVIEW` block. Catches design-rule violations the gate misses: cross-lab imports, fusion-spine breaches (sensor/DTC/chemistry logic sneaking in), signal/noise orphans, v6 enum re-introduction, flag-not-default-off. Includes a **structural-craft WARNING axis** (§8 — smells / depth / SRP) so the high-signal checks from the skill-eval aren't lost. **Must be clean** alongside `VERIFICATION GATE` before any task flips to `done`. |

The workspace `CLAUDE.md` is read implicitly and carries workspace-wide rules
(reports `.md` only; archive never delete; petrol-only; no graphify).

The canonical wiki is COMLab-local: `labs/comlab/wiki/00_index.md … 14_*.md`
(+ cross-lab `SEMANTIC_CONTRACT.md`, `OBD_VOCABULARY.md`, `DTC_VOCABULARY.md`).
Read at bootstrap by **line range only** (READ-NARROW) — they are inputs, not
rules, and not loaded as skills.

---

## Sibling bundle — the registry (load for `registry/` tasks)

The v2 registry (`labs/comlab/registry/`) is a separate package with its **own**
3-skill bundle. A task working inside `registry/` (rules, `schema_v2.py`,
`integration_shim.py`) loads these instead of (or alongside) the COMLab mandatory 3:

| Skill | Path |
|---|---|
| **registry-python** | `registry/docs/_registry_skills/registry-python/SKILL.md` |
| **registry-verification-loop** | `registry/docs/_registry_skills/registry-verification-loop/SKILL.md` |
| **registry-code-review** | `registry/docs/_registry_skills/registry-code-review/SKILL.md` |

(Index: `registry/docs/_registry_skills/_INDEX.md`.)

---

## On-demand domain skills

| Skill | Path | Load when… |
|---|---|---|
| **comlab-fusion-consumer** | `_comlab_skills/comlab-fusion-consumer/SKILL.md` | the task is an **orphan-closer** — its `Consumes` line is a single emitted field with **zero live COMLab reads today** (`per_bank_trim_delta`, `control_module_voltage_v`, `w_theo`/`sensor_error_delta`, `ltft_cell_vector`, `per_cylinder_misfire_counts`, `load_state`). Gates the orphan-closer consumer tasks `T-COMV2-{BANK-FUSE-1,VPWR-GATE-1,MAF-LIN-1,LTFT-CELL-1,MISFIRE-LOC-1,CTXMOD-1}` **and** the perception/gate pack `T-COMV2-{FUELSYS-GATE-1,VE-GATE-1,ECU-HW-1,ECU-FUSE-1}` (2026-06-21 correction — those four have no live COMLab reader either; `ECU-FUSE-1` adds a "verify existing perception-axis read" half). |
| **comlab-vault-prep** | `_comlab_skills/comlab-vault-prep/SKILL.md` | the task is one of the **four Phase-2 ingestion-prep tasks** of the COMLab → Vault pack: `T-COM-CODEPREP`, `T-COM-TESTPREP`, `T-COM-WIKIPREP`, `T-COM-DOCPREP`. Load it **alongside** the matching generic prep skill (`4dlab-code-prep` for code/tests, `4dlab-wiki-prep` for the wiki, `4dlab-doc-prep` for the docs). Pins the COMLab invariants the generic procedure does not know: docs exclusion file-list, terminal-fusion-spine consumer framing (COMLab is consumed-by the Wired/UI app layer, not another lab), proposal-stays-proposal edge rule, vocab→`_vocabulary` split. **Not** for code-clean, graphify, or the vault build. Authored 2026-06-26 (VAULT pack) per the ≥3-task trigger — it gates 4 prep tasks sharing one read-only invariant set. |

Authored 2026-06-21 per the trigger rule (a surface that gates **≥ 3 atomic tasks**,
carries a non-obvious read-only invariant — mirror-from-emitter, default-off flag,
two-grep anti-orphan gate — that the coder consumes, not derives). The orphan-closer
pack is 6 tasks sharing exactly that surface.

**Candidates for later authoring** (do NOT pre-author — wait until the surface
gates ≥ 3 tasks):

| Skill | Likely surface | Trigger |
|---|---|---|
| `comlab-test-harness` | `tests/` harness (descriptor categorical, no master-row projection, golden-master regression) | the `T-COMTST-*` pack — 3 of 4 done; if a follow-up harness pack reopens ≥ 3 tasks, promote it |
| `comlab-fusion-scoring` | `wiki §08`/`§09` scoring→fusion + calibration | when the additive-vs-Bayesian ranker rework lands as ≥ 3 tasks |
| `comlab-fault-atlas` | `comlab/core/fault_atlas_router.py` + `wiki §06` family routing | if atlas routing needs a dedicated derivation surface across ≥ 3 tasks |

---

## On-demand verification skills (none currently)

Upgrades on top of the 6-phase loop, authored per the "≥ 3 tasks gated by this
surface" rule when a phase needs them. None yet.

---

## Skill-load protocol (paste into every coder session after Step 1 of `COMLAB_TASKS_START_HERE.md`)

> **Skill load protocol.** I will `Read` `_comlab_skills/comlab-python/SKILL.md`,
> `_comlab_skills/comlab-verification-loop/SKILL.md`, and
> `_comlab_skills/comlab-code-review/SKILL.md` at session start (mandatory). If the
> task works inside `registry/`, I will instead/also load the three
> `registry/docs/_registry_skills/` skills. I will additionally load only the
> on-demand skills whose **Load when…** rule matches the task I am about to work on
> (currently none authored). I will apply the Immediate Checklist to every diff, run
> the per-file Inner Loop after every Edit (Python 3.14 via
> `/agent_workspace/.venv-wired/bin/python`), and produce both a `VERIFICATION GATE` block
> and a `CODE REVIEW` block in `tasks/progress_notes/<task-id>.md` before flipping a
> task to `done`.

---

## Build status

All 3 COMLab mandatory skills built 2026-06-21:

- `comlab-python`: Python 3.14 house style + Inner Loop + fusion-spine boundary
  (consumes verdicts) + signal/noise named-consumer rule + default-off flag pattern.
- `comlab-verification-loop`: Phase-5 wiki-provenance + anti-orphan guard (every
  contracted field grep-confirmed read in a live path).
- `comlab-code-review`: per-diff `CODE REVIEW` block with fusion-spine checks,
  signal/noise orphan catch, and the structural-craft WARNING axis (§8).

---

## Hard constraints (recap)

- **Fusion spine, built LAST.** Consume the four labs' **verdicts**
  (`schemas/ingestion.py::OrchestratorInboundRequest`), never raw sensors.
- **No cross-lab Python imports.** Mirror each lab's types locally.
- **Signal/noise governs every field.** New field/enum/fault ships only with a
  named existing consumer (analytics / fault-atlas routing) or a same-change
  proposal. "Future use" is not a consumer. Anti-orphan is a Stage-4-close gate.
- **No v6 / v1.** No v6 enum names (`MixtureClass`, `GasRuleFlag`, `OBDFlag`,
  4-value `DTCRoutingTag`, `HistoricalSignature`).
- **Default-off flags.** New fusion capability ships behind an explicit flag,
  single-point byte-identical; live activation is a separate follow-up.
- **Wiki is canonical.** Every enum value, score weight, threshold, and confidence
  cap carries a `# wiki: §N` provenance comment.
- **Python 3.14 ONLY** via `/agent_workspace/.venv-wired/bin/python`. No version mixing.
- **No graphify / KG rebuild.** The graph is frozen — query, never rebuild.
- **Folder convention.** `wiki/` = lab wiki only; vocabulary/contract → `docs/Vocabulary/`;
  design docs → `docs/`.
- **Three mandatory skills are non-negotiable.** Session does not begin coding until
  all three (or the registry trio for `registry/` tasks) are loaded.
- **Dual-gate finish.** A task flips to `done` only when both `VERIFICATION GATE`
  and `CODE REVIEW` are clean.
