# EVAL-VLIVE-1 — Coder comprehension probe (vault-live graph)
**Paste this whole file as message 1 of a fresh coder session. Run it once per model (Agy, then Codex).**

You are a coder agent on the **4DLab** codebase (`/agent_workspace`). This is a
timed **comprehension probe**, not a build task. Answer all probes by
investigating the repo, then stop.

## Rules of the run
- Write your answers **only** to `apps/vault/eval/runs/EVAL-VLIVE-1__<id>.md`,
  where `<id>` is your agent name — `agy` or `codex` (so the two runs never
  collide). **Do not modify, create, or delete any other file.** P5 is sketched
  in your report, not applied.
- For **every** probe give two things: **Answer** (exhaustive but precise — list
  every item, add no extras) and **Source/Method** (the exact command, `file:line`,
  or query you used to get it). The Source/Method line is graded.
- Resources available — use **any**, your choice (which ones you reach for is part
  of what this measures):
  - raw code under `labs/`;
  - the framed-note frontmatter (`implements` / `consumers` / `drift_guards`) on
    design docs + wiki notes;
  - the query tool:
    `/agent_workspace/.venv-wired/bin/python _skills/graph/4dlab-vault/scripts/vault_query.py --vault labs <consumers|drift|code|docs|backlinks>`;
  - the three Obsidian `.base` views (`modules`, `consumers`, `drift-guards`).
- Time/▢ budget: aim to finish in one focused pass. Note your start and end.

## Probes

**P1 — Blast radius.** You are about to change how DTCLab emits its routing tag
(`labs/dtclab/dtclab/core/routing_tag_mapper.py`, the `DTCRoutingTag` it produces).
Before you ship: (a) list **every downstream consumer** of DTCLab's output (file +
what it does with it); (b) list the **DTCLab tests** that guard this area. Flag any
consumer that is **not yet live**.

**P2 — Cross-lab trace.** DNALab produces a `VehicleDNA` envelope. Name **every
place in COMLab that actually READS it** (exact file + function). Name only real
readers — a plausible-looking file that does not actually read it is a wrong answer.

**P3 — Test selection.** You just edited `labs/vinlab/vinlab/overlay/horizon.py`.
(a) Which test(s) must you run? (b) Which downstream consumers in **other** labs
should you sanity-check?

**P4 — Governance.** A teammate wants to add a new field `cold_start_enrichment_pct`
to the GASLab→COMLab payload "for future use." Per this repo's rules, is that
shippable as-is? If not, what exactly must accompany it? **Cite the rule.**

**P5 — Applied (optional).** To make `routing_tag_mapper` reject an *unknown* tag
with a typed error instead of silently passing: name the exact **file + function**
to change, the **single test file** that should assert the new behaviour, and
sketch the diff **in your report**. Do **not** modify the repo.

## Done when
Report saved at `apps/vault/eval/runs/EVAL-VLIVE-1__<id>.md`; every probe has an
Answer + Source/Method line; no other file changed.
