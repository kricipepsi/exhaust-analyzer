# Bases Views

Three `.base` files live in `Vault/_bases/`. Each answers one question the bare
files can't. They read the frontmatter schema (see `frontmatter-schema.md`), so
keep the two in sync — a view that filters on a field the schema dropped will
silently show nothing.

`.base` files are YAML. Embed a view in any note with `![[modules.base#All modules]]`.

## modules.base — "what is in each lab/module?"

Groups every framed note by `lab`, then lists `module` / `subsystem` /
`node_type`. This is the map you open first. Consumes: `lab`, `module`,
`subsystem`, `node_type`, `tags`.

## consumers.base — the signal/noise audit

The most important view. Lists every wiki/design note with its `consumers`.
A blank `consumers` cell is a **red flag** — it means a note shipped without a
named downstream consumer, which the rule forbids. Use this view to catch that
before it spreads. Consumes: `consumers`, `module`, `node_type`, `implements`.

## drift-guards.base — coverage map

Lists each note's `implements` (code) against its `drift_guards` (tests). A note
that implements code but lists no guard is either untested or mis-mapped — both
worth seeing. Consumes: `implements`, `drift_guards`, `module`.

## Extending safely

- **Filter on `node_type` / `tags`**, not on folder paths, so a view keeps
  working if the layout shifts.
- **Every new column must map to a schema field that has a consumer row.** A
  Bases column *is* a consumer — if you add a column for field X, X now has a
  named consumer (this view), which is exactly what the rule wants. Record it in
  `frontmatter-schema.md`.
- **Don't add formulas that fabricate relationships** (e.g. guessing consumers
  from filename similarity). Views display authored data; they don't invent it.
- Test a changed `.base` by opening it in Obsidian — an empty result usually
  means a filter references a field no note actually has.

See `obsidian-md-conventions.md` for full Bases syntax (filters, formulas, view
types) — that file mirrors the upstream Bases reference.
