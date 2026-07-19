#!/usr/bin/env python3
"""eval-doc-graph — classify a Pass-3 LLM document graph against the deterministic
baseline, as a CHECKER (never an adder).

Reads two graphify node-link graphs (`graph.json`): the canonical deterministic
baseline (e.g. graph/v2_docs/graph.json) and the Pass-3 LLM scratch graph
(e.g. graph/v2_docs_llm/graph.json). Emits a CONFIRMED / GAP / NOISE
classification report. Writes NOTHING into either graph.

Division of labour (deliberate): this script does the OBJECTIVE part — set-math
over edges, confidence gating, relation gating, health metrics. It cannot decide
whether a candidate GAP has a *named consumer* in COMLab analytics / fault-atlas
routing — that is human/agent judgment. So it emits CANDIDATE_GAP rows for the
agent to confirm (name the consumer + chunk anchor) or demote to NOISE.

Usage:
    python eval_doc_graph.py BASELINE_GRAPH_JSON LLM_GRAPH_JSON [--out REPORT.md]
"""
import json, sys, argparse, collections

# ---- TYPE CONFIG (document graph) -------------------------------------------
# Signal relations: a NEW edge of this relation, EXTRACTED, between two existing
# nodes, is a candidate GAP — it carries diagnostic/routing meaning a consumer
# can read. Source: relation vocabulary observed in v2_docs/graph.json.
SIGNAL_RELATIONS = {
    "CONSUMES", "GATED_BY", "ROUTES_TO", "VERIFIES",
    "ENUMERATES", "DERIVED_FROM", "MIRRORS_CONTRACT_IN",
    "SUPERSEDES", "OWNED_BY",
}
# Generic relations: even when EXTRACTED, these carry no consumer value on their
# own. A new MENTIONS/DESCRIBES edge is prose adjacency, not a diagnostic link.
GENERIC_RELATIONS = {"MENTIONS", "DESCRIBES"}
CONSUMER_ANCHOR = "COMLab analytics / fault-atlas routing"
GRAPH_TYPE = "document"
ISOLATED_OK = False  # docs: every node should be wired; isolated nodes are a defect


def load(path):
    g = json.load(open(path))
    return g, g.get("nodes", []), g.get("links", g.get("edges", []))


def edge_key(e):
    return (e.get("source"), e.get("target"), e.get("relation"))


def classify(baseline_path, llm_path):
    _, bnodes, blinks = load(baseline_path)
    _, _lnodes, llinks = load(llm_path)
    bnode_ids = {n.get("id") for n in bnodes}
    bedge_set = {edge_key(e) for e in blinks}
    ledge_set = {edge_key(e) for e in llinks}

    buckets = collections.defaultdict(list)
    for e in llinks:
        k = edge_key(e)
        conf = (e.get("confidence") or e.get("confidence_tag") or "?").upper()
        rel = e.get("relation")
        both_nodes = e.get("source") in bnode_ids and e.get("target") in bnode_ids
        if k in bedge_set:
            buckets["CONFIRMED"].append(k)                 # proves baseline completeness
        elif conf != "EXTRACTED":
            buckets["NOISE_inferred"].append((k, conf))    # LLM-inferred — reject
        elif not both_nodes:
            buckets["NOISE_new_node"].append(k)            # invents a node — reject
        elif rel in GENERIC_RELATIONS:
            buckets["NOISE_generic_rel"].append(k)         # prose adjacency — no consumer
        elif rel in SIGNAL_RELATIONS:
            buckets["CANDIDATE_GAP"].append((k, e))        # agent: name consumer or demote
        else:
            buckets["CANDIDATE_GAP_unknown_rel"].append((k, e))
    buckets["BASELINE_ONLY"] = [edge_key(e) for e in blinks if edge_key(e) not in ledge_set]
    return buckets, len(blinks), len(llinks)


def health(path):
    _, nodes, links = load(path)
    node_ids = {n.get("id") for n in nodes}
    deg = collections.Counter()
    for e in links:
        deg[e.get("source")] += 1
        deg[e.get("target")] += 1
    conf = collections.Counter((e.get("confidence") or "?") for e in links)
    dangling = sum(1 for e in links
                   if e.get("source") not in node_ids or e.get("target") not in node_ids)
    isolated = sum(1 for nid in node_ids if deg[nid] == 0)
    n = len(nodes)
    density = round(len(links) / (n * (n - 1)), 4) if n > 1 else 0.0
    return dict(nodes=n, links=len(links), density=density, dangling=dangling,
                isolated=isolated, confidence=dict(conf.most_common()),
                top_hubs=deg.most_common(5))


def render_health_only(path):
    """Single-graph condition check — runnable now on any canonical graph, no LLM
    pass and no re-extraction. Answers 'is this graph in good condition?'."""
    h = health(path)
    L = [f"# Graph health — {GRAPH_TYPE} graph (`{path}`)\n",
         "Single-graph condition check (reads the canonical graph only — no LLM pass, "
         "no re-extraction).\n",
         "| metric | value |", "|---|---|"]
    for m in ("nodes", "links", "density", "dangling", "isolated"):
        L.append(f"| {m} | {h[m]} |")
    L.append(f"| confidence split | {h['confidence']} |")
    L.append(f"| top hubs (degree) | {', '.join(f'{n}:{d}' for n, d in h['top_hubs'])} |")
    flags = []
    if h["dangling"]:
        flags.append(f"{h['dangling']} DANGLING edge(s) — endpoint missing from the node set (always a defect)")
    if h["isolated"] and not ISOLATED_OK:
        flags.append(f"{h['isolated']} ISOLATED node(s) — unexpected for the {GRAPH_TYPE} graph (every node should be wired)")
    verdict = "GOOD" if not flags else "CHECK"
    L.append(f"\n**Condition: {verdict}.**")
    if verdict == "GOOD":
        note = "0 dangling" + (", 0 isolated" if not ISOLATED_OK else f", {h['isolated']} isolated (expected for this tier)")
        L.append(f"- {note} — graph is structurally sound.")
    for f in flags:
        L.append(f"- {f}")
    return "\n".join(L)


def render(buckets, nb, nl, hb, hl, baseline_path, llm_path):
    n_gap = len(buckets["CANDIDATE_GAP"]) + len(buckets["CANDIDATE_GAP_unknown_rel"])
    n_noise = (len(buckets["NOISE_inferred"]) + len(buckets["NOISE_new_node"])
               + len(buckets["NOISE_generic_rel"]))
    L = []
    L.append(f"# PASS-3 cross-check — {GRAPH_TYPE} graph (checker, not adder)\n")
    L.append(f"- Baseline: `{baseline_path}` ({nb} edges)")
    L.append(f"- LLM Pass-3: `{llm_path}` ({nl} edges)")
    L.append(f"- Consumer anchor for a real GAP: **{CONSUMER_ANCHOR}**\n")
    L.append("## Classification of every LLM edge\n")
    L.append("| Class | Count | Meaning / action |")
    L.append("|---|---|---|")
    L.append(f"| CONFIRMED | {len(buckets['CONFIRMED'])} | present in baseline — proves completeness, no action |")
    L.append(f"| CANDIDATE_GAP | {len(buckets['CANDIDATE_GAP'])} | EXTRACTED signal edge, both nodes exist, missing from baseline — **agent must name a consumer or demote to NOISE** |")
    L.append(f"| CANDIDATE_GAP_unknown_rel | {len(buckets['CANDIDATE_GAP_unknown_rel'])} | as above but relation not in the known signal set — inspect |")
    L.append(f"| NOISE_inferred | {len(buckets['NOISE_inferred'])} | confidence != EXTRACTED — rejected |")
    L.append(f"| NOISE_new_node | {len(buckets['NOISE_new_node'])} | endpoint absent from baseline — rejected |")
    L.append(f"| NOISE_generic_rel | {len(buckets['NOISE_generic_rel'])} | MENTIONS/DESCRIBES — prose adjacency, no consumer value |")
    L.append(f"| BASELINE_ONLY | {len(buckets['BASELINE_ONLY'])} | in baseline, LLM did not find — informational |")
    L.append(f"\n**Verdict inputs:** {n_gap} candidate GAP(s) for consumer-naming, {n_noise} NOISE edge(s) rejected.\n")

    L.append("## Candidate GAPs — agent fills consumer + chunk anchor\n")
    if n_gap == 0:
        L.append("_None. Pass 3 surfaced no EXTRACTED signal edge the deterministic pass missed — "
                 "i.e. the baseline is complete on this run._\n")
    else:
        L.append("For each row name the **existing** COMLab/fault-atlas consumer + code path that "
                 "would read it. No consumer ⇒ demote to NOISE (or record as a proposal candidate "
                 "in `comlab/config/proposals/`). Promote nothing into the baseline graph: route a "
                 "real GAP back through `4dlab-doc-prep` (make it explicit in a chunk, re-run the "
                 "deterministic pass).\n")
        L.append("| src → tgt | relation | source anchor | named consumer (FILL) | disposition (FILL) |")
        L.append("|---|---|---|---|---|")
        for k, e in buckets["CANDIDATE_GAP"] + buckets["CANDIDATE_GAP_unknown_rel"]:
            anchor = e.get("source_file") or e.get("source_location") or "?"
            L.append(f"| {k[0]} → {k[1]} | {k[2]} | {anchor} | | |")
    L.append("")
    L.append("## Health delta (baseline → LLM)\n")
    L.append("| metric | baseline | LLM Pass-3 |")
    L.append("|---|---|---|")
    for m in ("nodes", "links", "density", "dangling", "isolated"):
        L.append(f"| {m} | {hb[m]} | {hl[m]} |")
    L.append(f"| confidence split | {hb['confidence']} | {hl['confidence']} |")
    L.append("\n> A high INFERRED share in the LLM graph is expected and is exactly what the gate "
             "filters out — report it, do not act on it.\n")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("baseline")
    ap.add_argument("llm", nargs="?", default=None,
                    help="Pass-3 LLM graph. Omit for a single-graph HEALTH-ONLY check.")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if a.llm is None:
        report = render_health_only(a.baseline)
    else:
        buckets, nb, nl = classify(a.baseline, a.llm)
        hb, hl = health(a.baseline), health(a.llm)
        report = render(buckets, nb, nl, hb, hl, a.baseline, a.llm)
    if a.out:
        open(a.out, "w").write(report)
        print(f"wrote {a.out}")
    else:
        print(report)


if __name__ == "__main__":
    main()
