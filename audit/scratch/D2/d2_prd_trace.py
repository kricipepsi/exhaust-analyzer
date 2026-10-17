"""D2 probe — PRD requirement -> design home (HLD/DLD/LLD) and BDD scenario.

Run from the repo root:
    python audit/scratch/D2/d2_prd_trace.py [comlab|gaslab]

Step 1: count requirement IDs in the PRD (patterns REQ-/FR-/NFR-/PRD-/R<n>/US-).
Step 2: the PRD has none, so each requirement-bearing unit is taken as one requirement:
        every table row and every bullet under a numbered section (### or ##) of the PRD.
        Key tokens of a unit = its backticked identifiers + error codes + numbers with units.
Step 3: a unit has a "design home" if >= 1 key token occurs in HLD/DLD/LLD (and, for the
        BDD check, in the BDD). Units with no key token are listed as UNKEYED (not checkable
        mechanically -> reported as such, not as orphans).
Read-only.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CHAINS = {
    "comlab": dict(
        prd="labs/comlab/docs/COMLab_PRD.md",
        design=["labs/comlab/docs/COMLab_HLD.md", "labs/comlab/docs/COMLab_DLD.md",
                "labs/comlab/docs/COMLab_LLD.md"],
        bdd="labs/comlab/docs/COMLab_BDD.md"),
    "gaslab": dict(
        prd="labs/gaslab/docs/PRD_GASLab.md",
        design=["labs/gaslab/docs/HLD_GASLab.md", "labs/gaslab/docs/DLD_GASLab.md",
                "labs/gaslab/docs/LLD_GASLab.md"],
        bdd="labs/gaslab/docs/BDD_GASLab.md"),
}
ID_RE = re.compile(r"\b(?:REQ|FR|NFR|PRD|US|UR|KR)-?\d+[A-Za-z0-9.-]*\b|\bR\d{1,3}\b")
TOK_RE = re.compile(r"`([^`]{2,80})`|\b(ERR-[A-Z]+-\d{3})\b|\b(\d+(?:\.\d+)?\s?(?:ms|MB|%|°C|s|px))")
SKIP_SECTIONS = ("Out of scope", "Open questions", "References", "Product vision", "Users")


def units(prd: Path):
    sec = ""
    for n, ln in enumerate(prd.read_text(encoding="utf-8").splitlines(), 1):
        if ln.startswith("#"):
            sec = ln.lstrip("# ").strip()
            continue
        if any(s in sec for s in SKIP_SECTIONS) or not re.match(r"^\d", sec):
            continue
        s = ln.strip()
        if (s.startswith("|") and not set(s) <= set("|-: ")) or re.match(r"^[-*] |^\d+\. ", s):
            if s.startswith("| Gate |") or s.startswith("| Code |") or s.startswith("| Persona"):
                continue
            yield n, sec, s


GENERIC = {"true", "false", "value", "None", "NONE", "HIGH", "rate"}


def toks(text: str):
    """Key tokens: identifier sub-tokens of backticked spans (len>=5 or ALL_CAPS),
    whole error codes, and numbers-with-units (matched verbatim)."""
    out = []
    for m in TOK_RE.finditer(text):
        t = next(g for g in m.groups() if g).strip()
        if m.group(1):
            for sub in re.findall(r"[A-Za-z_][A-Za-z0-9_]*", t):
                if sub not in GENERIC and (len(sub) >= 5 or sub.isupper()):
                    out.append(sub)
            if not re.search(r"[A-Za-z]", t):
                out.append(t)          # pure regex / numeric literal kept whole
        elif len(t) >= 3:
            out.append(t)
    return list(dict.fromkeys(out))


def main() -> None:
    lab = sys.argv[1] if len(sys.argv) > 1 else "comlab"
    c = CHAINS[lab]
    prd = ROOT / c["prd"]
    ids = ID_RE.findall(prd.read_text(encoding="utf-8"))
    print(f"PRD requirement IDs found in {c['prd']}: {len(ids)} {sorted(set(ids))[:10]}")
    design = "\n".join((ROOT / d).read_text(encoding="utf-8") for d in c["design"] if (ROOT / d).exists())
    bdd = (ROOT / c["bdd"]).read_text(encoding="utf-8") if (ROOT / c["bdd"]).exists() else ""
    tot = nodesign = nobdd = unkeyed = 0
    for n, sec, s in units(prd):
        tot += 1
        k = toks(s)
        if not k:
            unkeyed += 1
            print(f"UNKEYED   {c['prd']}:{n} [{sec[:30]}] {s[:110]}")
            continue
        d_hit = [t for t in k if t in design]
        b_hit = [t for t in k if t in bdd]
        if not d_hit:
            nodesign += 1
        if not b_hit:
            nobdd += 1
        tag = ("NO-DESIGN " if not d_hit else "design-ok ") + ("NO-BDD" if not b_hit else "bdd-ok")
        print(f"{tag} {c['prd']}:{n} [{sec[:30]}] keys={k[:5]} {s[:90]}")
    print(f"\nunits={tot} keyed={tot-unkeyed} no_design_home={nodesign} no_bdd={nobdd} unkeyed={unkeyed}")


if __name__ == "__main__":
    main()
