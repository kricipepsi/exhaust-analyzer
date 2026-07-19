"""Deterministic Run 4 patch on graph.json — KG audit ISSUE-2 + ISSUE-4 resolution.

Promotes two INFERRED edges to EXTRACTED after wiki spot-check confirmation.
Idempotent: re-running produces no changes.
"""

import json
from pathlib import Path

GRAPH_PATH = Path(__file__).resolve().parent / "graph.json"
PATCH_MARKER = "kg_audit_run4_2026-05-20"

# -- Edge 1: LEAN_MIXTURE --escalates_to--> LEAN_MISFIRE (ISSUE-2, INFERRED 0.85)
# Wiki anchor: GAS_WIKI §7.3 line 464 — "route to LEAN_MISFIRE (§7.5)"
EDGE1_SOURCE = "gas_wiki_cs_lean_mixture"
EDGE1_TARGET = "gas_wiki_cs_lean_misfire"
EDGE1_RELATION = "escalates_to"
EDGE1_NEW_LOCATION = "§7.3 line 464"

# -- Edge 2: LEAN_MIXTURE --mistaken_for_via_masking_rule--> IGNITION_MISFIRE (ISSUE-4, INFERRED 0.75)
# Wiki anchor: GAS_WIKI §8.4 line 773 — "override any LEAN verdict"; §7.4 line 472 — "confirmed misfire (not lean)"
EDGE2_SOURCE = "gas_wiki_cs_lean_mixture"
EDGE2_TARGET = "gas_wiki_cs_ignition_misfire"
EDGE2_RELATION = "mistaken_for_via_masking_rule"
EDGE2_NEW_LOCATION = "§8.4 line 773; §7.4 line 472"


def locate_edge(links, source, target, relation):
    """Find an edge by exact (source, target, relation) triple. Returns (index, edge_dict)."""
    for i, edge in enumerate(links):
        if (
            edge.get("source") == source
            and edge.get("target") == target
            and edge.get("relation") == relation
        ):
            return i, edge
    raise ValueError(
        f"Edge not found: {source} --{relation}--> {target}"
    )


def patch_edge(edge, new_location):
    """Apply promotion patch to a single edge. Returns True if changes were made."""
    changed = False

    if edge.get("confidence") != "EXTRACTED":
        edge["confidence"] = "EXTRACTED"
        changed = True

    # Drop numerical confidence score on promoted edges
    if "confidence_score" in edge:
        del edge["confidence_score"]
        changed = True

    if edge.get("source_location") != new_location:
        edge["source_location"] = new_location
        changed = True

    if edge.get("_patched") != PATCH_MARKER:
        edge["_patched"] = PATCH_MARKER
        changed = True

    return changed


def assert_invariants(graph, original_link_count):
    """Post-condition checks."""
    links = graph["links"]

    # No forbidden relations
    forbidden = [
        e for e in links
        if e.get("relation") in ("semantically_similar_to", "conceptually_related_to")
    ]
    assert len(forbidden) == 0, f"Forbidden relations found: {forbidden}"

    # Link count unchanged (promotion, not addition/deletion)
    assert len(links) == original_link_count, (
        f"Link count changed: {original_link_count} → {len(links)}"
    )

    # No orphan nodes introduced (every node referenced in links exists in nodes)
    node_ids = {n["id"] for n in graph["nodes"]}
    for edge in links:
        assert edge["source"] in node_ids, f"Orphan source: {edge['source']}"
        assert edge["target"] in node_ids, f"Orphan target: {edge['target']}"

    # No INFERRED edges below 0.85 remain
    inferred_below = [
        e for e in links
        if e.get("confidence") == "INFERRED"
        and e.get("confidence_score", 1.0) < 0.85
    ]
    assert len(inferred_below) == 0, (
        f"INFERRED edges below 0.85 remain: {inferred_below}"
    )


def main():
    graph = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    links = graph["links"]
    original_link_count = len(links)

    changes = 0

    # Patch edge 1
    idx1, edge1 = locate_edge(links, EDGE1_SOURCE, EDGE1_TARGET, EDGE1_RELATION)
    if patch_edge(edge1, EDGE1_NEW_LOCATION):
        changes += 1
        print(f"Edge 1 patched: {EDGE1_SOURCE} --{EDGE1_RELATION}--> {EDGE1_TARGET}")
    else:
        print("Edge 1: no changes needed (already patched)")

    # Patch edge 2
    idx2, edge2 = locate_edge(links, EDGE2_SOURCE, EDGE2_TARGET, EDGE2_RELATION)
    if patch_edge(edge2, EDGE2_NEW_LOCATION):
        changes += 1
        print(f"Edge 2 patched: {EDGE2_SOURCE} --{EDGE2_RELATION}--> {EDGE2_TARGET}")
    else:
        print("Edge 2: no changes needed (already patched)")

    if changes == 0:
        print("No changes — graph.json is already up to date.")
        return

    # Write back
    GRAPH_PATH.write_text(
        json.dumps(graph, indent=2, ensure_ascii=False, sort_keys=False) + "\n",
        encoding="utf-8",
    )

    # Verify post-conditions on the written file
    graph2 = json.loads(GRAPH_PATH.read_text(encoding="utf-8"))
    assert_invariants(graph2, original_link_count)

    print(f"graph.json written ({changes} edge(s) touched). All invariants pass.")


if __name__ == "__main__":
    main()
