#!/usr/bin/env python3
"""eval-code-graph — classify a Pass-3 LLM CODE graph against the deterministic
AST baseline, as a CHECKER (never an adder).

Reads two graphify node-link graphs (`graph.json`): the canonical baseline
(e.g. graph/v2_code/graph.json, built from the AST) and the Pass-3 LLM scratch
graph (e.g. graph/v2_code_llm/graph.json). Emits a CONFIRMED / GAP / NOISE
report. Writes NOTHING into either graph.

WHY THE BAR IS HIGHEST HERE. The code graph's structural edges (calls, contains,
inherits, method, uses, references) come from the AST — they are ground truth, not
prose interpretation. The baseline is also ALREADY ~50% INFERRED. An LLM re-reading
source therefore mostly manufactures INFERRED noise, and any EXTRACTED structural
edge it claims the AST "missed" is suspect: either a real AST blind spot (e.g.
dynamic dispatch, reflection, a runtime-built call the static parse cannot see) or a
hallucination. So a CANDIDATE_GAP on the code graph is not routed to docs-prep; it
must be validated against the AST by hand before it counts as a GAP.

Division of labour: this script does set-math + confidence/relation gating. The
agent decides whether each CANDIDATE_GAP is a true AST blind spot with a consumer.

Usage:
    python eval_code_graph.py BASELINE_GRAPH_JSON LLM_GRAPH_JSON [--out REPORT.md]
"""
import json, sys, argparse, collections

# ---- TYPE CONFIG (code graph) -----------------------------------------------
# AST-structural relations (ground truth). A NEW EXTRACTED edge of one of these,
# between two existing nodes, is a candidate AST blind spot — NOT an automatic
# GAP. rationale_for bridges code symbols to design/wiki reasoning.
SIGNAL_RELATIONS = {
    "calls", "contains", "inherits", "method", "uses", "references",
    "rationale_for",
}
# No relation is auto-noise on structure; on the code graph the discriminator is
# confidence (already 50% INFERRED) plus the AST-truth scrutiny the agent applies.
GENERIC_RELATIONS = set()
CONSUMER_ANCHOR = ("graph navigation / drift-guards / the design→code→test spine "
                   "(NOT COMLab analytics — code edges are structural)")
GRAPH_TYPE = "code"
ISOLATED_OK = False  # code: every symbol node should be wired; isolated nodes are a defect


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
            buckets["CONFIRMED"].append(k)
        elif conf != "EXTRACTED":
            buckets["NOISE_inferred"].append((k, conf))
        elif not both_nodes:
            buckets["NOISE_new_node"].append(k)
        elif rel in GENERIC_RELATIONS:
            buckets["NOISE_generic_rel"].append(k)
        elif rel in SIGNAL_RELATIONS:
            buckets["CANDIDATE_GAP"].append((k, e))         # = candidate AST blind spot
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
    L.append(f"- Baseline (AST): `{baseline_path}` ({nb} edges)")
    L.append(f"- LLM Pass-3: `{llm_path}` ({nl} edges)")
    L.append(f"- Consumer anchor for a real GAP: **{CONSUMER_ANCHOR}**\n")
    L.append("> **Code bar is highest.** The baseline is AST ground truth and already ~50% "
             "INFERRED. Expect Pass 3 here to be almost entirely NOISE. A CANDIDATE_GAP is a "
             "*candidate AST blind spot* — validate it against the source (is it a dynamic call / "
             "reflection the static parse genuinely cannot see?) before calling it a GAP.\n")
    L.append("## Classification of every LLM edge\n")
    L.append("| Class | Count | Meaning / action |")
    L.append("|---|---|---|")
    L.append(f"| CONFIRMED | {len(buckets['CONFIRMED'])} | present in baseline — proves AST completeness, no action |")
    L.append(f"| CANDIDATE_GAP | {len(buckets['CANDIDATE_GAP'])} | EXTRACTED structural edge missing from AST baseline — **validate as AST blind spot + name consumer, else NOISE** |")
    L.append(f"| CANDIDATE_GAP_unknown_rel | {len(buckets['CANDIDATE_GAP_unknown_rel'])} | new relation not in the structural set — inspect |")
    L.append(f"| NOISE_inferred | {len(buckets['NOISE_inferred'])} | confidence != EXTRACTED — rejected (dominant class on code) |")
    L.append(f"| NOISE_new_node | {len(buckets['NOISE_new_node'])} | endpoint absent from baseline — rejected |")
    L.append(f"| BASELINE_ONLY | {len(buckets['BASELINE_ONLY'])} | in AST baseline, LLM did not find — informational |")
    L.append(f"\n**Verdict inputs:** {n_gap} candidate AST blind spot(s) to validate, {n_noise} NOISE edge(s) rejected.\n")

    L.append("## Candidate AST blind spots — agent validates + names consumer\n")
    if n_gap == 0:
        L.append("_None. Pass 3 found no EXTRACTED structural edge the AST missed — the AST graph "
                 "is complete on this run (the expected result)._\n")
    else:
        L.append("For each row: (1) open the source and confirm the edge is a **real** relation "
                 "the static AST could not capture (dynamic dispatch, getattr/reflection, "
                 "runtime-registered call) — if the AST simply *should* have caught it, the LLM "
                 "edge is suspect, mark NOISE; (2) name the consumer (graph navigation, a "
                 "drift-guard, or the design→code→test spine) that reads it. No real blind spot or "
                 "no consumer ⇒ NOISE. Promote nothing into `graph/v2_code/graph.json`; a genuine "
                 "AST gap is fixed in the extractor/AST config, never patched into the graph.\n")
        L.append("| src → tgt | relation | source location | real AST blind spot? (FILL) | consumer (FILL) |")
        L.append("|---|---|---|---|---|")
        for k, e in buckets["CANDIDATE_GAP"] + buckets["CANDIDATE_GAP_unknown_rel"]:
            loc = e.get("source_location") or e.get("source_file") or "?"
            L.append(f"| {k[0]} → {k[1]} | {k[2]} | {loc} | | |")
    L.append("")
    L.append("## Health delta (baseline → LLM)\n")
    L.append("| metric | baseline | LLM Pass-3 |")
    L.append("|---|---|---|")
    for m in ("nodes", "links", "density", "dangling", "isolated"):
        L.append(f"| {m} | {hb[m]} | {hl[m]} |")
    L.append(f"| confidence split | {hb['confidence']} | {hl['confidence']} |")
    L.append("\n> The baseline INFERRED share is already high; a Pass-3 graph that inflates it "
             "further is the noise this gate exists to reject. Report the split, do not act on it.\n")
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
