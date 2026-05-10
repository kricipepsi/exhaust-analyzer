# Engine V1 — Archived (read-only)

The V1 diagnostic engine has been replaced by V2 (`engine/v2/`). V1 source is
preserved as git tag `v1-final` on the main branch history.

## Accessing V1 source

```bash
# View V1 code at the tagged commit:
git checkout v1-final

# Or extract a specific file without switching branches:
git show v1-final:engine/  # lists V1 engine directory
```

## Why V1 was replaced

V1 plateaued at 44% accuracy after 20+ remediation tasks. The structural causes
were:

- Perception stage that globally overrode other layers
- Undocumented five-stage post-inference cascade
- Sibling faults with identical discriminators
- No validation layer — bad data propagated silently
- Magic-number thresholds with no source provenance
- Empty `vref.db`

V2 addresses all of these with a ground-up Evidence Arbitrator architecture.
See `CHANGELOG.md` for the full V1→V2 migration guide.

## Frozen schema

`schema/v1_reference/` contains frozen V1 schema files for comparison and
corpus provenance. These are **not consumed** by the V2 engine.
