# T-SHIP-UI-3 — per-field `?` hover tooltips (function + range)
**Pack:** ship · **Blocked by:** T-SHIP-UI-2 (**done**, 8e0d08b) · **Lane:** coder
**Write scope:** `apps/ui/app.py`, `apps/ui/ui_payload.py` (help-dict home), `apps/ui/tests/`,
progress note, ledger row. Nothing outside `apps/ui/`.

## Owner requirement (2026-07-08, verbatim intent)
Hovering the `?` beside EVERY input field must show:
1. a short, concise explanation of the field's function;
2. the input limit/range.

## Spec
1. **One shared table, one source of truth.** Add `FIELD_HELP: dict[str, FieldHelp]` (help
   text + min + max + unit) in `ui_payload.py`. Widgets take BOTH their `help=` string AND
   their `min_value=`/`max_value=` from this table — tooltip and enforcement cannot drift.
2. **Tooltip format (two lines):**
   `<one lay-readable sentence: what the engine reads it for>`
   `Range: <min>–<max> <unit>` (checkboxes/selects: list the accepted options instead).
3. **Sources for the text** (do not invent): function → FieldMap §5-§11 "Consumer" column,
   lay-worded; ranges → FieldMap "Range / unit" column and the min/max already enforced in
   `app.py` (where they disagree, FieldMap wins — fix the widget, note the diff). Advanced
   C2..C9 fields: function from the producer-state consumer comments
   (`apps/wired/v7/load_corpus.py:228-276`) + reveal contracts; ranges tolerance-wide per the
   band reports (`v3/reports/V3_*_SYNTH_BANDS_*.md`), stated as plausible input bounds.
4. **Coverage is total:** every `st.number_input/selectbox/checkbox/text_input` that feeds
   the payload gets `help=` — sidebar, all 8 expanders, DTC/FF/$06 rows included.
5. **Test:** unit test asserting (a) every widget key produced by `ui_payload` mapping has a
   `FIELD_HELP` entry; (b) every numeric entry's min/max equals the widget call's bounds
   (share the constants so this is a direct identity check); (c) every help string is
   non-empty and contains "Range:" or "Options:".

## Success criteria
100% payload-feeding widgets carry the two-line tooltip; tooltip range == enforced range by
construction; ruff/pyright clean; `apps/ui/tests` green (existing 5 + new); both gate blocks.
FORBIDDEN: touching engine/labs; changing payload semantics; new fields.
