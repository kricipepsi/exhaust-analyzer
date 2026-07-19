# T-VAULT-CODEGRAPH-1 — progress note

## Plan

Part A (DEFAULT, now, no tokens, no owner gate): run `eval-code-graph --health-only` on `graph/v2_code/graph.json`
→ `graph/v2_code/GRAPH_HEALTH.md`; expect Condition GOOD (0 dangling, 0 isolated). Report the confidence split (the
high INFERRED share is a baseline property, not a defect). Part A alone satisfies "check the code graph".

Part B (OPTIONAL, GATED): only if the owner wants it AND docs Pass 3 proved valuable. **First resolve the
precondition** — confirm graphify supports an LLM pass over a `.py` package. If not, STOP at Part A (optionally spec a
deterministic AST-reproducibility diff as the right stability check for AST code). If supported: LLM pass over the code
package, `--backend deepseek` default mode → scratch `graph/v2_code_llm/` → classify with `eval-code-graph` →
`graph/v2_code/PASS3_CROSSCHECK.md`. Treat every CANDIDATE_GAP as a candidate AST blind spot: validate against source
(dynamic dispatch / reflection / runtime-registered call) before calling it a GAP; fix a real blind spot in the
extractor/AST config, never patch `graph.json`. Consumer anchor = graph navigation / drift-guards / design→code→test
spine. Graph-tooling lane — no lab inner-loop/gate.


## VERIFICATION GATE

_(runner fills: Part A verdict + confidence split + canonical byte-unchanged · if Part B run: precondition resolution,
separate-dir guard, default-mode command, CONFIRMED/GAP/NOISE counts, no collateral)_


## CODE REVIEW

_(runner fills: each candidate AST blind spot validated against source or demoted to NOISE · zero edges entered the
canonical graph)_
