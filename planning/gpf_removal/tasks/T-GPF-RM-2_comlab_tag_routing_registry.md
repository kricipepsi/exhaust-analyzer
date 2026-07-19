# T-GPF-RM-2 — COMLab: drop GPF_HISTORY tag, discriminator, registry P-codes

**Pack:** GPF Removal · **Lab:** COMLab (tag/routing side) · **Blocked by:** T-GPF-RM-1 · **Status:** pending

## Scope (1 paragraph)

With DTCLab no longer emitting `GPF_HISTORY` (T-GPF-RM-1), remove COMLab's
consumption of that tag and its P-codes. COMLab mirrors the routing vocabulary
locally (no cross-lab import), so the `GPF_HISTORY` enum member, its
`tag_discriminator.yaml` family mapping, and the GPF P-codes embedded in the
`global_fault_registry.json` `catalyst_flow_restriction` fault all live here.
**The `catalyst_flow_restriction` fault itself stays** — it is a legitimate
catalyst fault; only its GPF-specific P-codes and wording are stripped.

## Signal/noise / consumer

Removal. After this task `grep -rn "GPF_HISTORY\|P244A\|P2459" labs/comlab/comlab`
returns zero (graph excluded). The `catalyst_flow_restriction` fault keeps its
`P0420` matcher and all three `target_horizons` — do not weaken it.

## Files to change

- `comlab/schemas/vocabulary.py:462` — delete the `GPF_HISTORY` enum member.
- `comlab/config/tag_discriminator.yaml:109-112` — delete the `GPF_HISTORY:` block
  (family `exhaust_leak` + its wiki comment).
- `comlab/config/global_fault_registry.json` — fault `ERR-CF-003`
  (`catalyst_flow_restriction`, ~L139-169):
  - `p_code_match` (L158-162): remove `"P244A"` and `"P2459"`; **keep** `"P0420"`.
  - `ui_diagnostic_string` (L147): remove the "or GPF soot overload" clause.
  - Leave `target_horizons`, `confidence_scoring`, and the fault id unchanged.
  - Also fix the remediation strings that name GPF: `catalyst_flow_restriction`
    text at L2779 ("If GPF-equipped… GPF if backpressure…") — reword to the TWC
    catalyst case only.
- `comlab/config/kg/catalyst_failure.json` — strip GPF mentions at L58, L64,
  L67-70 (component group "+ GPF Assembly", "GPF soot overload",
  "Mode $06 GPF differential pressure", "Replace the restricted converter or
  GPF") so the fault describes the TWC/substrate case only.
- COMLab wiki: `docs/wiki/DTC_VOCABULARY.md:136,144,435` and
  `docs/wiki/OBD_VOCABULARY.md:482` — remove the `GPF_HISTORY` row and the
  "gated on has_particulate_filter" GPF-codes note.
- `docs/COMLab_LLD.md:254,540,938` — remove `has_particulate_filter` from the
  mirrored view definitions **only if** RM-3 also clears it (these doc lines pair
  with the field readers; coordinate — but the LLD's `GPF_HISTORY`/routing prose
  belongs to this task).
- Tests: `tests/e2e/test_error_codes.py:199` and `tests/unit/test_tag_discriminator.py`
  — drop GPF/`GPF_HISTORY` assertions; keep the catalyst-fault assertions that
  use `P0420`.

## Task-reversal note (do here)

`T-FX-DTCHEX-1` (done) widened `DTC_REGEX` to `[0-9A-F]{3}`. **Leave the regex
as-is** — it serves all hex-tailed codes per wiki §2.3, not just GPF. In
`planning/test_rollout/tasks/T-FX-DTCHEX-1_*.md`, add a one-line note that
`GPF_HISTORY` is **no longer** the regex's downstream consumer (GPF removed by
this pack); the regex stays justified by the general hex-code requirement.

## Success criteria

- No `GPF_HISTORY`, `P244A`, `P2459` in `comlab/` code, config, or COMLab wiki.
- `catalyst_flow_restriction` still present, still matches `P0420`, still spans
  its three horizons; e2e error-code tests green.
- `tag_discriminator.yaml` parses; no dangling family reference.

## Inner loop (coder)

`ruff check labs/comlab` → `pyright labs/comlab` → `pytest -x -q labs/comlab/tests`.
JSON configs: validate they still load (`python3.14 -c "import json,sys; json.load(open(...))"`).

## VERIFICATION GATE
_(coder fills)_

## CODE REVIEW
_(coder fills)_
