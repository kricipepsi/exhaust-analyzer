# DNA family — TASKS START HERE

Read this first, every session, before any other action.

## 0. What this pack is

This pack closes the **remaining issues across the DNA family** — the three sibling
codebases that produce `VehicleDNA`:

- `labs/vinlab/` — Part A `VinDNA` (vehicle identity).
- `labs/symptomlab/` — Part B `SymptomDNA` (operator symptom).
- `labs/dnalab/` — the assembly that composes both into `VehicleDNA`.

Cross-lab imports **within the family are allowed in one direction only**:
`dnalab → vinlab + symptomlab`. No lab imports COMLab; COMLab mirrors what it needs.

Two input documents drive the pack:
- `labs/dnalab/docs/audits/AUDIT_2026-06-11_dna_vin_rework_and_dna10_answerability.md`
  (the rework-impact + DBS-answerability audit).
- `labs/dnalab/docs/research/DNAresearch.md` (the symptom-channel + prior research).

## 1. Start sequence

1. Read this file.
2. Read `PROGRESS.md` — the Task log is the source of truth (next task, blocked-by).
3. Run the sandbox Python 3.14 block (workspace `CLAUDE.md`); load the per-lab
   language + verification-loop skills. **graphify pre-step → SKIP** (see §3).
4. **Pick the task the ledger picks:** the first `pending` row whose Blocked-by are
   all `done`. Not a `blocked`/`deferred` row, not one you were handed.
5. Post a one-paragraph scope confirm (field/enum, bound + wiki/contract cite,
   signal/noise consumer) before writing code. Unclear scope/consumer/files → ask
   one question.

## 2. Non-negotiables (signal/noise + proposal routing)

- **Every new field/enum/vocabulary string needs a named consumer.** For this pack
  most consumers live in **COMLab** (`fault_atlas_router`, the symptom prior, the
  context-modifier weights). COMLab is a separate codebase you do **not** edit here.
- **New vocabulary ships as a PROPOSAL, not silently into the live schema.** A new
  symptom string, a new `load_state` value, or a new VinDNA field is registered in
  `labs/comlab/comlab/config/proposals/` (entries.yaml) naming its COMLab consumer
  and code path, **before or with** the DNA-side change. "Future use" is not a
  consumer; a *proposed* consumer that ships in the paired COMLab task is.
- **The contract is COMLab-owned.** `SEMANTIC_CONTRACT.md` (§4.1 VinDNA, §4.2
  SymptomDNA) and `labs/vinlab/VehicleDNA.md` (the tier-string enum source) are
  amended through the proposal, not unilaterally. A DNA task may *draft* the §4.x
  amendment text but flags it for COMLab/semantic sign-off in its progress note.
- **No cross-lab Python imports** beyond `dnalab → vinlab + symptomlab`. Every
  numeric literal in vinlab/ carries a wiki/contract cite.
- **STRICT inner loop after every meaningful edit:** `ruff` → `pyright` →
  `pytest -x -q`, run from the owning lab's root.
- **One task per session.** Fill `VERIFICATION GATE` + `CODE REVIEW` in
  `progress_notes/<id>.md`, flip the ledger row to `done`, then STOP.

## 3. Do NOT run graphify

Each lab's `graph/` is a frozen, verified, off-runtime artefact — no code reads it.
graphify is **not** in the inner loop or the verification gate. If you catch
yourself about to run it: STOP and escalate to the owner.

## 4. Done means

Both gate blocks clean in the progress note **and** any field the task contracted to
consume is `grep`-confirmed read in a live path (the COMLab consumer, or its
registered proposal entry). Green pytest alone is not done. A new schema field with
no live/proposed consumer is an orphan — a signal/noise breach — and blocks `done`.
Git: owner commits by explicit path; never stage any `graph/` or `.sandbox-py/`.
