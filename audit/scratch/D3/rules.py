"""D3 check (3): contradictions between governance rules. Quotes both sides with path:line.

Usage (from repo root):  python audit/scratch/D3/rules.py
Each contradiction is a list of sides; a side is (path, regex). The script locates each regex
(multi-line, so quotes that wrap are found), prints path:line and the quoted text, and finishes with
the facts it measured (does the path exist, is the repo a git repo, ...). Exit 1 if any quoted side
can no longer be found (the contradiction would then be NOT REPRODUCED).
"""
from __future__ import annotations

import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(__file__))
from common import ROOT  # noqa: E402

CHECKS: dict[str, dict] = {
    "X1 git ritual: never branch / work on main  vs  fix rows land on a branch (main = production)": dict(sides=[
        ("4DLab_CLAUDE.md", r"Never create branches, worktrees, or stashes\."),
        ("4DLab_CLAUDE.md", r"proceed in the current\s+checkout on \*\*main\*\*"),
        ("v3/CLAUDE.md", r"Never\s+branch, stash, or raise git as a blocker"),
        ("audit/AUDIT_START_HERE.md", r"Every fix row lands on a branch"),
        ("audit/AUDIT_START_HERE.md", r"Every push to `main` redeploys the public app"),
        ("4DLab_CLAUDE.md", r"git is not yet initialized in `/agent_workspace`"),
    ]),
    "X2 who may BUILD a graph: architect-only  vs  coder (Nemo) LLM extract, v3 coders 'build a new index', manifest 'when a task says so'": dict(sides=[
        ("AGENTS.md", r"build subcommands \(update/extract/serve/…\) are architect-lane only"),
        ("DECISIONS.md", r"Architect runs all graph BUILD tasks"),
        ("planning/graph_rollout/GRAPH_ROLLOUT_START_HERE.md", r"never build subcommands"),
        ("planning/graph_rollout/GRAPH_ROLLOUT_START_HERE.md", r"`extract` \(LLM\) is now in-pack as \*\*T-GR-10/11 only\*\* \(Nemo lane"),
        ("planning/graph_rollout/GRAPH_ROLLOUT_PROGRESS.md", r"\| T-GR-10 <!--NEMO LANE--> \|[^\n]*\| Nemo \| pending \|"),
        ("planning/graph_rollout/tasks/T-GR-10_llm_extract_pilot_gaslab.md", r"graphify extract [^\n]*--backend deepseek"),
        ("v3/CLAUDE.md", r"Querying or building a \*new\* index\s+offline is fine"),
        ("GRAPH_MANIFEST.md", r"they re-run graphify\s+\*\*only\*\* when a task file explicitly says so"),
    ]),
    "X3 per-lab graphs frozen / never rebuilt  vs  architect rebuilds per-lab tiers": dict(sides=[
        ("4DLab_CLAUDE.md", r"Per-lab knowledge graphs are frozen — query them, never re-`graphify` them"),
        ("CLAUDE.md", r"query the graph; never rebuild it"),
        ("DECISIONS.md", r"Architect runs all graph BUILD tasks\*\* \(T-GR-2\.\.7, T-GR-9"),
        ("planning/graph_rollout/GRAPH_ROLLOUT_PROGRESS.md", r"6 tiers refreshed \(comlab code/tests/current"),
    ]),
    "X4 signal/noise: consumer must already exist  vs  consumer may be added in the same change": dict(sides=[
        ("ROADMAP.md", r"needs a named,\s+existing consumer in COMLab analytics or fault-atlas routing\. No consumer → it\s+doesn't ship"),
        ("AGENTS.md", r"that consumer \*\*may be one you add in the same change\*\*"),
        ("4DLab_CLAUDE.md", r"the consumer does not have to pre-exist in v1"),
    ]),
    "X5 canonical wiki: docs/GASLab/wikiNEW/ (never copy)  vs  labs/<lab>/wiki/": dict(sides=[
        ("ROADMAP.md", r"\*\*v2 wiki is canonical\*\* for the lab being reworked \(e\.g\. GASLab → `docs/GASLab/wikiNEW/`\)"),
        ("DECISIONS.md", r"Canonical wiki `docs/GASLab/wikiNEW/` \| \*\*Unchanged — link in place\.\*\* Never copy"),
        ("AGENTS.md", r"`labs/<lab>/wiki/` is the canonical source for that lab"),
    ], facts=[("docs/GASLab/wikiNEW exists", lambda: os.path.isdir(os.path.join(ROOT, "docs/GASLab/wikiNEW"))),
              ("labs/gaslab/wiki exists", lambda: os.path.isdir(os.path.join(ROOT, "labs/gaslab/wiki")))]),
    "X6 which task to run: the one the manager assigned  vs  the one the ledger picks, not the one handed": dict(sides=[
        ("START_HERE.md", r"implement the \*\*task ID the manager assigned\*\*"),
        ("AGENTS.md", r"implement exactly the `labs/<lab>/tasks/<id>\.md` the manager assigned"),
        ("4DLab_CLAUDE.md", r"\*\*Run the task the ledger picks, not the one you were handed\.\*\*"),
        (".agent/assignments.md", r"^Agy → T-V3-P4-C5B"),
        ("v3/V3_PROGRESS.md", r"\| T-V3-P4-C5B \| [^\n]*\| done \|"),
    ]),
    "X7 interpreter/venv: sandbox restore (START_HERE)  vs  no .sandbox-py, no download ritual (4DLab_CLAUDE)": dict(sides=[
        ("START_HERE.md", r"Infra \(Python 3\.14 sandbox restore, `\.venv-wired`, git ritual\) is inherited from root\s+`4DLab/CLAUDE\.md`"),
        ("README.md", r"Infra inherited from root `4DLab/CLAUDE\.md`"),
        ("4DLab_CLAUDE.md", r"There is no `\.sandbox-py` and no per-session download ritual"),
        ("labs/comlab/tasks/PROGRESS.md", r"`\.\./\.\./\.sandbox-py/bin/python3\.14`"),
    ]),
    "X8 interpreter: never bare python3  vs  sanctioned python3 commands": dict(sides=[
        ("4DLab_CLAUDE.md", r"always invoke `python3\.14` explicitly\*\*; never bare\s+`python`/`python3`"),
        ("AGENTS.md", r"`python3 scripts/graph_health\.py \[lab\]`"),
        ("AGENTS.md", r"`python3 _skills/graph/4dlab-vault/scripts/vault_query\.py"),
    ]),
    "X9 firecrawl auth claimed automatic  vs  key file no longer in the repo": dict(sides=[
        ("AGENTS.md", r"`FIRECRAWL_API_KEY` is exported automatically by every `run-\*\.sh` launcher"),
        ("AGENTS.md", r"if it does not, STOP and report"),
        ("planning/graph_rollout/GRAPH_ROLLOUT_START_HERE.md", r"auth auto-exported by run-\*\.sh"),
        ("DECISIONS.md", r"real \(authenticated\) firecrawl research"),
        (".gitignore", r"^_skills/firecrawl-web-scraping-search/API\.md$"),
    ], facts=[("API.md tracked by git", lambda: subprocess.run(
        ["git", "ls-files", "--error-unmatch", "_skills/firecrawl-web-scraping-search/API.md"], cwd=ROOT,
        capture_output=True).returncode == 0)]),
    "X10 never edit Vault/  vs  Vault/tasks packs whose procedure flips their own ledger rows": dict(sides=[
        ("AGENTS.md", r"\*\*Never edit `Vault/`\.\*\*"),
        ("4DLab_CLAUDE.md", r"\| GAS→Vault pipeline pack \| `/agent_workspace/Vault/tasks/GAS_VAULT_TASKS_START_HERE\.md` \|"),
        ("Vault/tasks/GAS_VAULT_TASKS_START_HERE.md", r"flip the ledger row to `done`, then STOP"),
        ("DECISIONS.md", r"its `Vault/tasks/` annotations stand"),
    ]),
    "X11 coder roster: two coders (Codex, Agy)  vs  six identities / Nemo lane": dict(sides=[
        ("CLAUDE.md", r"Coders are two omp agents — \*\*Codex\*\* and \*\*Agy\*\*"),
        ("planning/graph_rollout/GRAPH_ROLLOUT_PROGRESS.md", r"<!--NEMO LANE-->"),
    ], facts=[("identities under .agent/coders/", lambda: sorted(os.listdir(os.path.join(ROOT, ".agent/coders"))))]),
}


def locate(path: str, rx: str) -> tuple[int, str] | None:
    fp = os.path.join(ROOT, path)
    if not os.path.exists(fp):
        return None
    txt = open(fp, encoding="utf-8").read()
    m = re.search(rx, txt, flags=re.M)
    if not m:
        return None
    line = txt.count("\n", 0, m.start()) + 1
    return line, re.sub(r"\s+", " ", m.group(0))


def main() -> int:
    missing = 0
    for name, spec in CHECKS.items():
        print(f"\n## {name}")
        for path, rx in spec["sides"]:
            hit = locate(path, rx)
            if hit is None:
                missing += 1
                print(f"  NOT FOUND  {path}  /{rx}/")
            else:
                print(f"  {path}:{hit[0]} — \"{hit[1][:160]}\"")
        for label, fn in spec.get("facts", []):
            print(f"  fact: {label}: {fn()}")
    git = subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], cwd=ROOT, capture_output=True, text=True)
    print(f"\nfact: repo is a git work tree: {git.stdout.strip()}  | /agent_workspace exists: {os.path.exists('/agent_workspace')}")
    print(f"sides not found: {missing}")
    return 1 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
