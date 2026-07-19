#!/usr/bin/env python3
"""Build/update the 4DLab Obsidian vault from a finished, graphified lab.

Vault tooling for the `4dlab-vault` skill — NOT lab diagnostic code, and not
subject to the lab inner-loop/gates. It mirrors a finished lab's code/tests/wiki/docs
into `Vault/labs/<lab>/`, injects consumer-aware frontmatter on the notes named
in the lab's vault-map, and installs the `.base` views. Idempotent; dry-run by
default.

It NEVER runs graphify and NEVER auto-derives `consumers` — those are authored
in `assets/vault-map.<lab>.yaml`. The canonical graph stays at the lab's
`graphify-out/graph.json` and is not copied.

Usage:
    python3 build_lab_vault.py --lab obdlab --repo /abs/path/to/4DLabV2 [--dry-run]
    python3 build_lab_vault.py --lab obdlab --repo /abs/path/to/4DLabV2   # apply
    python3 build_lab_vault.py --vocab --repo /abs/path/to/4DLabV2 [--dry-run]
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML is required to read the vault-map. Install it in your venv "
             "(uv pip install pyyaml) and re-run.")

IGNORE = shutil.ignore_patterns(
    "__pycache__", "*.pyc", ".pytest_cache", ".ruff_cache", "*.egg-info",
    ".gitkeep", ".DS_Store",
)
# Frontmatter key order kept fixed so re-runs produce identical output (idempotent).
FM_ORDER = ["node_type", "lab", "module", "subsystem",
            "implements", "consumers", "drift_guards", "tags", "source"]

# Per-lab source-path overrides. Default (no entry) = OBDLab layout.
# GASLab wiki lives at labs/gaslab/wiki/ instead of labs/<lab>/research/chunks/.
LAB_SRC_PATHS = {
    "obdlab": {
        "wiki_subpath":          "research/chunks",
        "wiki_source_template":  "labs/{lab}/research/chunks/{note}",
        "required_graph_tiers":  ("v2_code", "v2_tests", "v2_wiki", "v2_docs"),
    },
    "gaslab": {
        "wiki_subpath":          "wiki",
        "wiki_source_template":  "labs/{lab}/wiki/{note}",
        # Owner waived prose Pass-3 for GASLab on 2026-06-11: Phase-2 prep is enough.
        "required_graph_tiers":  ("v2_code", "v2_tests"),
    },
    "dtclab": {
        "wiki_subpath":          "wiki",
        "wiki_source_template":  "labs/{lab}/wiki/{note}",
        # "skip graph testing" (owner, 2026-06-11): prose Pass-3 waived; only AST tiers required.
        "required_graph_tiers":  ("v2_code", "v2_tests"),
    },
    "symptomlab": {
        "wiki_subpath":          "wiki",
        "wiki_source_template":  "labs/{lab}/wiki/{note}",
        # Pass-3 skip LIFTED (owner, 2026-06-12): wiki is canonical, prose graphs built
        # (T-SYMGRAPH-LLM) — all four tiers required.
        "required_graph_tiers":  ("v2_code", "v2_tests", "v2_wiki", "v2_docs"),
    },
    "vinlab": {
        "wiki_subpath":          "wiki",
        "wiki_source_template":  "labs/{lab}/wiki/{note}",
        # "skip graph testing" (owner, 2026-06-12): prose Pass-3 waived; only AST tiers required.
        "required_graph_tiers":  ("v2_code", "v2_tests"),
    },
    "dnalab": {
        "wiki_subpath":          "wiki",
        "wiki_source_template":  "labs/{lab}/wiki/{note}",
        # "skip graph testing" (mirror VIN/GAS/DTC, 2026-06-13): prose Pass-3 waived; only AST tiers required.
        "required_graph_tiers":  ("v2_code", "v2_tests"),
    },
    "comlab": {
        "wiki_subpath":          "wiki",
        "wiki_source_template":  "labs/{lab}/wiki/{note}",
        # "skip graph testing" (owner, 2026-06-26): prose Pass-3 waived; only AST tiers required.
        # Liftable per T-COM-GRAPH-LLM -> ("v2_code","v2_tests","v2_wiki","v2_docs").
        "required_graph_tiers":  ("v2_code", "v2_tests"),
    },
}


# Keyed non-lab corpora. `ui` is doc-only; `registry` is a COMLab sub-package
# that still has code/tests/docs tiers and a custom vault destination.
APP_SRC_PATHS = {
    "ui": {
        "src_root":             "apps/ui",          # not labs/<lab>
        "docs_notes":           ["4DLab_UI_FieldMap.md", "StreamliteUI.md"],  # explicit list, not a glob
        "required_graph_tiers": (),                 # prose Pass-3 waived; no AST corpus
        "vault_area":           "apps",             # -> Vault/apps/ui/
    },
    "registry": {
        "src_root":             "labs/comlab/registry",
        "code_entries":         (
            "__init__.py",
            "schema_v2.py",
            "integration_shim.py",
            "corpus_curated.csv",
            "corpus_meta.json",
            "rules",
            "shim",
            "tools",
        ),
        "tests_subpath":        "tests",
        "docs_subpath":         "graph/v2_docs/ingest_ready",
        "note_source_template": "labs/comlab/registry/graph/v2_docs/ingest_ready/{note}",
        "required_graph_tiers": ("v2_code", "v2_tests", "v2_docs"),
        "vault_dest":           "labs/comlab/registry",
        "source_summary":       "code, tests, docs=graph/v2_docs/ingest_ready",
        "graph_source":         "labs/comlab/registry/graph/",
    },
}


def log(msg: str, dry: bool) -> None:
    print(("[dry-run] " if dry else "[build]  ") + msg)


def yaml_scalar(s: str) -> str:
    return '"' + str(s).replace('"', '\\"') + '"'


def render_frontmatter(d: dict) -> str:
    """Deterministic YAML frontmatter from a dict of our known field types."""
    lines = ["---"]
    for key in FM_ORDER:
        if key not in d:
            continue
        val = d[key]
        if key == "tags":
            lines.append(f"tags: [{', '.join(val)}]")
        elif isinstance(val, list):
            if not val:
                lines.append(f"{key}: []")
            else:
                lines.append(f"{key}:")
                lines.extend(f"  - {yaml_scalar(v)}" for v in val)
        else:
            lines.append(f"{key}: {yaml_scalar(val)}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def strip_frontmatter(text: str) -> str:
    """Remove a leading YAML frontmatter block if present (for idempotent rewrite)."""
    if not text.startswith("---"):
        return text
    end = text.find("\n---", 3)
    if end == -1:
        return text
    nl = text.find("\n", end + 1)
    return text[nl + 1:] if nl != -1 else ""


def copy_tree(src: Path, dst: Path, dry: bool) -> None:
    if dry and dst.exists():
        log(f"up-to-date {dst}", dry)
        return
    log(f"copy {src} -> {dst}", dry)
    if dry:
        return
    dst.mkdir(parents=True, exist_ok=True)
    shutil.copytree(src, dst, dirs_exist_ok=True, ignore=IGNORE)


def copy_entries(src: Path, dst: Path, entries: tuple[str, ...], dry: bool) -> None:
    """Copy explicit files/directories from one keyed corpus into a vault tier."""
    for entry in entries:
        item_src = src / entry
        item_dst = dst / entry
        if item_src.is_dir():
            copy_tree(item_src, item_dst, dry)
            continue

        if dry and item_dst.exists():
            log(f"up-to-date {item_dst}", dry)
            continue
        log(f"copy {item_src} -> {item_dst}", dry)
        if dry:
            continue
        item_dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(item_src, item_dst)


def write_file(path: Path, content: str, dry: bool) -> None:
    log(f"write {path}", dry)
    if dry:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def upsert_markdown_section(path: Path, heading: str, section: str, dry: bool) -> None:
    """Replace one level-2 section while preserving other provenance entries."""
    log(f"upsert {heading} in {path}", dry)
    if dry:
        return

    if path.exists():
        lines = path.read_text(encoding="utf-8").splitlines()
    else:
        lines = ["# Vault provenance", "", "Generated by build_lab_vault.py.", ""]

    replacement = section.strip().splitlines()
    out: list[str] = []
    inserted = False
    i = 0
    while i < len(lines):
        if lines[i].strip() == heading:
            if not inserted:
                out.extend(replacement)
                inserted = True
            i += 1
            while i < len(lines) and not lines[i].startswith("## "):
                i += 1
            continue
        out.append(lines[i])
        i += 1

    if not inserted:
        if out and out[-1] != "":
            out.append("")
        out.extend(replacement)

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")


def build_vocabulary_area(repo: Path, vault: Path, assets: Path, dry: bool) -> int:
    """Idempotent: copy canonical vocab bodies into Vault/_vocabulary/ and inject frontmatter."""
    vocab_map_path = assets / "vault-map.vocabulary.yaml"
    if not vocab_map_path.exists():
        sys.exit(f"Vocabulary map not found: {vocab_map_path}")
    spec = yaml.safe_load(vocab_map_path.read_text(encoding="utf-8"))
    entries = spec.get("vocabulary", {}) or {}
    if not entries:
        print("No vocabulary entries in map — nothing to do.")
        return 0

    # signal/noise gate
    empty = [n for n, m in entries.items() if not (m or {}).get("consumers")]
    if empty:
        sys.exit("Signal/noise breach — these vocab notes have no named consumer:\n  "
                 + "\n  ".join(empty) + "\nName a consumer or comment out the entry.")

    print(f"\n=== build _vocabulary/ area ({len(entries)} note(s)) ===")
    print(f"repo={repo}\nvault={vault}\nmap={vocab_map_path}\n")

    for note, meta in entries.items():
        canonical_path = repo / meta["canonical"]
        if not canonical_path.exists():
            print(f"  WARNING: canonical source not found: {canonical_path}")
            continue
        canonical_body = canonical_path.read_text(encoding="utf-8")
        canonical_md5 = hashlib.md5(canonical_body.encode()).hexdigest().upper()

        fm = {
            "node_type": meta.get("node_type", "wiki"),
            "lab": meta["lab"],
            "module": meta["module"],
            "subsystem": meta.get("subsystem", ""),
            "implements": meta.get("implements", []),
            "consumers": meta.get("consumers", []),
            "drift_guards": meta.get("drift_guards", []),
            "tags": meta.get("tags", []),
            "source": meta.get("source", str(canonical_path.relative_to(repo))),
        }
        dst = vault / "_vocabulary" / note
        if dry:
            log(f"vocab {note} <- {canonical_path} (md5={canonical_md5})", dry)
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(render_frontmatter(fm) + canonical_body, encoding="utf-8")
        log(f"vocab {note} written (body md5={canonical_md5})", dry)

    # provenance
    prov_path = vault / "_meta" / "PROVENANCE.md"
    prov_lines = []
    if prov_path.exists():
        prov_lines = prov_path.read_text(encoding="utf-8").splitlines()
    # append vocab section if not already present
    vocab_marker = "## _vocabulary/"
    if not any(line.startswith(vocab_marker) for line in prov_lines):
        if not dry:
            prov_path.parent.mkdir(parents=True, exist_ok=True)
            with prov_path.open("a", encoding="utf-8") as f:
                f.write(f"\n{vocab_marker}\n- built: {date.today().isoformat()}\n")
                for note_, meta_ in entries.items():
                    cp = repo / meta_["canonical"]
                    body = cp.read_text(encoding="utf-8") if cp.exists() else ""
                    f.write(f"- `{note_}`: source `{meta_['canonical']}`"
                            f"  md5 `{hashlib.md5(body.encode()).hexdigest().upper()}`\n")
        log(f"provenance appended to {prov_path}", dry)

    print("\nDone." + (" (dry-run — nothing written)" if dry else ""))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--lab", default=None, help="lab slug, e.g. obdlab")
    ap.add_argument("--repo", required=True, type=Path, help="abs path to 4DLabV2")
    ap.add_argument("--vault", type=Path, help="vault root (default: <repo>/Vault)")
    ap.add_argument("--map", type=Path, help="vault-map yaml (default: assets/vault-map.<lab>.yaml)")
    ap.add_argument("--assets", type=Path, help="assets dir (default: ../assets next to this script)")
    ap.add_argument("--dry-run", action="store_true", help="print actions, write nothing")
    ap.add_argument("--vocab", action="store_true", help="build _vocabulary/ area from vault-map.vocabulary.yaml")
    a = ap.parse_args()
    dry = a.dry_run

    repo = a.repo.resolve()
    vault = (a.vault or repo / "Vault").resolve()
    assets = (a.assets or Path(__file__).resolve().parent.parent / "assets").resolve()

    if a.vocab:
        return build_vocabulary_area(repo, vault, assets, dry)

    if not a.lab:
        sys.exit("Either --lab or --vocab is required.")

    map_path = (a.map or assets / f"vault-map.{a.lab}.yaml").resolve()

    app_config = APP_SRC_PATHS.get(a.lab, {})
    is_app = bool(app_config)
    paths = LAB_SRC_PATHS["obdlab"]
    if is_app:
        lab_src = repo / app_config["src_root"]
        code_src = lab_src
        tests_src = lab_src / app_config["tests_subpath"] if "tests_subpath" in app_config else lab_src
        wiki_src = lab_src
        docs_src = lab_src / app_config.get("docs_subpath", "")
        required_graph_tiers = app_config["required_graph_tiers"]
        tier_graphs = [
            lab_src / "graph" / tier / "graph.json" for tier in required_graph_tiers
        ]
    else:
        lab_src = repo / "labs" / a.lab
        paths = LAB_SRC_PATHS.get(a.lab, LAB_SRC_PATHS["obdlab"])
        code_src, tests_src = lab_src / a.lab, lab_src / "tests"
        wiki_src = lab_src / paths["wiki_subpath"]
        docs_src = lab_src / "docs"
        required_graph_tiers = paths.get(
            "required_graph_tiers", ("v2_code", "v2_tests", "v2_wiki", "v2_docs")
        )
        tier_graphs = [
            lab_src / "graph" / tier / "graph.json" for tier in required_graph_tiers
        ]

    if is_app:
        if "code_entries" in app_config:
            missing = [
                str(lab_src / entry)
                for entry in app_config["code_entries"]
                if not (lab_src / entry).exists()
            ]
            missing.extend(
                str(p)
                for p in (tests_src, docs_src, *tier_graphs)
                if p is not None and not p.exists()
            )
        else:
            missing = [str(lab_src / note) for note in app_config["docs_notes"] if not (lab_src / note).exists()]
        if missing:
            sys.exit(f"Corpus '{a.lab}' is not eligible — missing:\n  " + "\n  ".join(missing) +
                     "\nOnly complete keyed corpora are copied into the vault.")
    else:
        # --- eligibility: only finished, graphified labs ---
        missing = [str(p) for p in (code_src, tests_src, wiki_src, docs_src, *tier_graphs) if p is not None and not p.exists()]
        if missing:
            sys.exit(f"Lab '{a.lab}' is not eligible — missing:\n  " + "\n  ".join(missing) +
                     "\nOnly finished, graphified labs are copied into the vault.")

    if not map_path.exists():
        sys.exit(f"No vault-map for '{a.lab}': {map_path}")

    spec = yaml.safe_load(map_path.read_text(encoding="utf-8"))
    module = spec.get("module", a.lab)
    frame = spec.get("frame", {}) or {}

    # signal/noise gate: no framed note may have an empty consumers list
    empty = [n for n, m in frame.items() if not (m or {}).get("consumers")]
    if empty:
        sys.exit("Signal/noise breach — these framed notes have no named consumer:\n  "
                 + "\n  ".join(empty) + "\nName a consumer or move them to `plain:`.")

    if is_app:
        if "vault_dest" in app_config:
            lab_dst = vault / app_config["vault_dest"]
        else:
            lab_dst = vault / app_config["vault_area"] / a.lab
    else:
        lab_dst = vault / "labs" / a.lab

    print(f"\n=== build vault for '{a.lab}' (module={module}) ===")
    print(f"repo={repo}\nvault={vault}\nmap={map_path}\n")

    # --- copy code / tests / wiki / docs ---
    if is_app:
        if "code_entries" in app_config:
            copy_entries(lab_src, lab_dst / "code", app_config["code_entries"], dry)
            copy_tree(tests_src, lab_dst / "tests", dry)
            copy_tree(docs_src, lab_dst / "docs", dry)
        else:
            log(f"copy design corpus docs {lab_src} -> {lab_dst / 'docs'}", dry)
            if not dry:
                (lab_dst / "docs").mkdir(parents=True, exist_ok=True)
                for note in app_config["docs_notes"]:
                    shutil.copy2(lab_src / note, lab_dst / "docs" / note)
    else:
        copy_tree(code_src, lab_dst / "code", dry)
        copy_tree(tests_src, lab_dst / "tests", dry)
        copy_tree(wiki_src, lab_dst / "wiki", dry)
        copy_tree(docs_src, lab_dst / "docs", dry)

    # --- inject frontmatter on framed notes ---
    DOCS_NODE_TYPES = {"prd", "hld", "lld", "dld"}
    for note, meta in frame.items():
        nt = meta.get("node_type", "wiki")
        # Design docs live in docs/; wiki notes live in wiki/ (sourced from research/chunks/).
        # Keyed corpora can override the framed tier; registry docs are already doc-prepped.
        if is_app:
            tier = app_config.get("frame_tier", "docs")
            source_path = app_config.get(
                "note_source_template", f"{app_config['src_root']}/{{note}}"
            ).format(note=note)
        elif nt in DOCS_NODE_TYPES:
            tier = "docs"
            source_path = f"labs/{a.lab}/docs/{note}"
        else:
            tier = "wiki"
            source_path = paths["wiki_source_template"].format(lab=a.lab, note=note)
        note_path = lab_dst / tier / note
        fm = {
            "node_type": nt,
            "lab": a.lab,
            "module": module,
            "subsystem": meta.get("subsystem", ""),
            "implements": meta.get("implements", []),
            "consumers": meta.get("consumers", []),
            "drift_guards": meta.get("drift_guards", []),
            "tags": [a.lab, "finished", nt],
            "source": source_path,
        }
        if dry:
            log(f"frame {note} (node_type={nt}, tier={tier}, consumers={len(fm['consumers'])})", dry)
            continue
        if not note_path.exists():
            print(f"  WARNING: framed note not found after copy: {note_path}")
            continue
        body = strip_frontmatter(note_path.read_text(encoding="utf-8"))
        note_path.write_text(render_frontmatter(fm) + body, encoding="utf-8")
        log(f"framed {note}", dry)

    # --- lab landing note ---
    tmpl = (assets / "lab-landing.md.tmpl").read_text(encoding="utf-8")
    landing = tmpl.replace("{{LAB}}", a.lab).replace("{{MODULE}}", module)
    write_file(lab_dst / f"_{a.lab}.md", landing, dry)

    # --- install .base views ---
    for base in sorted(assets.glob("*.base")):
        log(f"install view {base.name} -> _bases/", dry)
        if not dry:
            (vault / "_bases").mkdir(parents=True, exist_ok=True)
            shutil.copy2(base, vault / "_bases" / base.name)

    # --- provenance ---
    if is_app:
        if "code_entries" in app_config:
            graph_note = ", ".join(required_graph_tiers)
            prov = (f"## {a.lab}\n- built: {date.today().isoformat()}\n"
                    f"- source: `{app_config['src_root']}/` ({app_config['source_summary']})\n"
                    f"- framed notes: {len(frame)}\n"
                    f"- canonical graphs required (not copied): `{app_config['graph_source']}` ({graph_note})\n")
        else:
            prov = (f"## {a.lab}\n- built: {date.today().isoformat()}\n"
                    f"- source: `{app_config['src_root']}/` (design docs)\n"
                    f"- framed notes: {len(frame)}\n"
                    f"- canonical graphs required (not copied): none (doc-only design corpus)\n")
    else:
        graph_note = ", ".join(required_graph_tiers)
        if a.lab in ("gaslab", "dtclab", "vinlab", "dnalab", "comlab"):
            graph_note += "; v2_wiki/v2_docs waived by owner direction"
        prov = (f"## {a.lab}\n- built: {date.today().isoformat()}\n"
                f"- source: `labs/{a.lab}/` (code, tests, wiki={paths['wiki_subpath']}, docs)\n"
                f"- framed notes: {len(frame)}\n"
                f"- canonical graphs required (not copied): `labs/{a.lab}/graph/` ({graph_note})\n")
    upsert_markdown_section(vault / "_meta" / "PROVENANCE.md", f"## {a.lab}", prov, dry)

    print("\nDone." + (" (dry-run — nothing written)" if dry else
          "  Open the vault in Obsidian and check the three Bases render."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
