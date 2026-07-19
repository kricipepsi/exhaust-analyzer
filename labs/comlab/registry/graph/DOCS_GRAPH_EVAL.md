# Graph health — document graph (`/agent_workspace/labs/comlab/registry/graph/v2_docs/graph.json`)

Single-graph condition check (reads the canonical graph only — no LLM pass, no re-extraction).

| metric | value |
|---|---|
| nodes | 1045 |
| links | 992 |
| density | 0.0009 |
| dangling | 0 |
| isolated | 0 |
| confidence split | {'EXTRACTED': 992} |
| top hubs (degree) | corpus_audit_5_per_case_disposition_table_5_per_case_disposition_table:251, registry_audit_2_rule_inventory_2_rule_inventory:106, case_library_lean_condition_lean_condition:55, case_library_misfire_misfire:46, chemistry_coverage_2_chemistry_states_observed_in_the_curated_corpus_2_chemistry_states_observed_in_the_curated_corpus:37 |

**Condition: GOOD.**
- 0 dangling, 0 isolated — graph is structurally sound.
