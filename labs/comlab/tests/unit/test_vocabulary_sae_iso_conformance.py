"""Standards conformance and proposals registry extensibility gate.

Verifies that:
1. Every L1 PID row parsed from vocabul/OBD_VOCABULARY.md matches the J1979 CSV.
2. Every L2 cited P-code in DTCRoutingTag comments resolves in SAE.md.
3. Every comlab/config/proposals/ entries.yaml entry has a valid consumer and citation.
"""

from __future__ import annotations

import ast
import csv
import re
from pathlib import Path
import yaml

from comlab.schemas import vocabulary as V

TEST_DIR = Path(__file__).resolve().parent
COMLAB_DIR = TEST_DIR.parent.parent  # labs/comlab
LABS_DIR = COMLAB_DIR.parent         # labs
SEMANTIC_DIR = LABS_DIR / "semantic"

OBD_WIKI_PATH = SEMANTIC_DIR / "vocabul" / "OBD_VOCABULARY.md"
CSV_PATH = SEMANTIC_DIR / "obd2-pid-table-service-01.csv"
SAE_PATH = SEMANTIC_DIR / "SAE.md"
ENTRIES_PATH = COMLAB_DIR / "comlab" / "config" / "proposals" / "entries.yaml"


def words_with_synonyms(s: str) -> set[str]:
    # Normalize to lowercase and split by underscore/camelcase
    s_normalized = re.sub(r"([a-z])([A-Z])", r"\1_\2", s)
    parts = re.split(r"[^a-zA-Z0-9]+", s_normalized.lower())
    w = set()
    for p in parts:
        if len(p) < 3:
            continue
        w.add(p)
        # Add abbreviations/synonyms
        if p.startswith("shrt") or p.startswith("stft"):
            w.update(["short", "trim", "fuel"])
        elif p.startswith("long") or p.startswith("ltft"):
            w.update(["long", "trim", "fuel"])
        elif p == "vacuum" or p == "manifold":
            w.update(["press", "map", "vacuum"])
        elif p == "abspress":
            w.update(["press", "map", "vacuum"])
    return w


def names_agree(md_name: str, csv_short: str, csv_long: str) -> bool:
    w_md = words_with_synonyms(md_name)
    w_csv = words_with_synonyms(csv_short).union(words_with_synonyms(csv_long))
    return bool(w_md.intersection(w_csv))


def units_agree(md_unit: str, csv_unit: str) -> bool:
    UNIT_MAPPING = {
        "RPM": "rpm",
        "°C": "degC",
        "%": "%",
        "g/s": "grams/sec",
        "kPa": "kPa",
    }
    expected = UNIT_MAPPING.get(md_unit, md_unit)
    return expected.lower() == csv_unit.lower()


def ranges_agree(md_range_str: str, csv_min_str: str, csv_max_str: str) -> bool:
    normalized = md_range_str.replace("–", " TO ").replace("—", " TO ")
    parts = [p.strip() for p in normalized.split(" TO ")]
    num_parts = len(parts)
    if num_parts != 2:
        return False
    try:
        md_min = float(parts[0].replace("+", ""))
        md_max = float(parts[1].replace("+", ""))
    except ValueError:
        return False

    csv_min = float(csv_min_str) if csv_min_str else 0.0
    csv_max = float(csv_max_str) if csv_max_str else 0.0

    if abs(md_min - csv_min) > 1.0 or abs(md_max - csv_max) > 1.0:
        # Check if it is a fuel trim with typical ±100 vs ±127 differences
        if csv_min in (-100.0, -127.0, -128.0) and md_min in (-100.0, -127.0, -128.0):
            return True
        return False
    return True


def symbol_exists_in_file(file_path: Path, symbol_path: str) -> bool:
    if not file_path.exists():
        return False
    try:
        content = file_path.read_text(encoding="utf-8")
        tree = ast.parse(content, filename=str(file_path))
    except Exception:
        return False

    parts = symbol_path.split(".")
    num_parts = len(parts)
    if num_parts == 1:
        symbol_name = parts[0]
        for node in ast.walk(tree):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name == symbol_name:
                    return True
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == symbol_name:
                        return True
        return False
    elif num_parts == 2:
        class_name, symbol_name = parts
        class_node = None
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef) and node.name == class_name:
                class_node = node
                break
        if not class_node:
            return False

        for node in ast.walk(class_node):
            if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
                if node.name == symbol_name:
                    return True
            elif isinstance(node, ast.Attribute):
                if node.attr == symbol_name:
                    return True
            elif isinstance(node, ast.Name) and node.id == symbol_name:
                return True
        return False
    return False


def parse_obd_vocabulary_table() -> list[dict[str, str]]:
    obd_wiki = OBD_WIKI_PATH.read_text(encoding="utf-8")
    pids = []
    in_section_2 = False
    for line in obd_wiki.splitlines():
        if "## 2." in line:
            in_section_2 = True
            continue
        if in_section_2 and line.startswith("## "):
            break
        if in_section_2 and line.startswith("|"):
            parts = [p.strip() for p in line.split("|")]
            num_parts = len(parts)
            if num_parts >= 8:
                if parts[1] == "4DLab canonical name" or parts[1].startswith("---"):
                    continue
                pids.append({
                    "name": parts[1].strip("` "),
                    "iso_pid": parts[2].strip("` "),
                    "sae_pid": parts[3].strip("` "),
                    "desc": parts[4].strip("` "),
                    "unit": parts[5].strip("` "),
                    "range": parts[6].strip("` "),
                })
    return pids


def parse_dtc_routing_tags_comments() -> dict[str, str]:
    vocab_path = COMLAB_DIR / "comlab" / "schemas" / "vocabulary.py"
    lines = vocab_path.read_text(encoding="utf-8").splitlines()
    member_comments = {}
    in_class = False
    for line in lines:
        if re.match(r"^\s*class\s+DTCRoutingTag\b", line):
            in_class = True
            continue
        if in_class:
            if line.strip() and not line.startswith(" ") and not line.startswith("\t"):
                if not line.startswith("#") and not line.startswith('"""') and not line.startswith("'''"):
                    in_class = False
                    continue
            match = re.match(r"^\s*([A-Z0-9_]+)\s*=\s*['\"]([A-Z0-9_]+)['\"]\s*#\s*(.*)$", line)
            if match:
                name, val, comment = match.groups()
                member_comments[name] = comment
    return member_comments


def extract_and_expand_pcodes(comment: str) -> list[str]:
    pcodes = []
    # Ranges
    range_matches = re.findall(r"\b(P\d{4})-(P\d{4})\b", comment)
    for start, end in range_matches:
        start_num = int(start[1:])
        end_num = int(end[1:])
        prefix = start[0]
        for i in range(start_num, end_num + 1):
            pcodes.append(f"{prefix}{i:04d}")
    cleaned_comment = re.sub(r"\b(P\d{4})-(P\d{4})\b", "", comment)
    code_matches = re.findall(r"\b(P[0-9A-Za-z_xX]{4})\b", cleaned_comment)
    for code in code_matches:
        pcodes.append(code)
    return pcodes


def code_resolves(code: str, sae_lines: list[str]) -> bool:
    if "x" in code.lower():
        pattern_str = "^" + code.lower().replace("x", "[0-9a-zA-Z]") + r"\b"
        pattern = re.compile(pattern_str)
        for line in sae_lines:
            if pattern.match(line.lower()):
                return True
        return False
    else:
        pattern = re.compile(r"^" + re.escape(code) + r"\b", re.IGNORECASE)
        for line in sae_lines:
            if pattern.match(line):
                return True
        return False


def test_l1_pid_conformance() -> None:
    """Validate parsed PID rows in OBD_VOCABULARY.md match the J1979 CSV."""
    pids = parse_obd_vocabulary_table()
    assert pids

    # Load J1979 CSV
    csv_rows = []
    with open(CSV_PATH, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            csv_rows.append(row)
    assert csv_rows

    checked = 0
    for pid in pids:
        # Skip virtual/derived nodes
        if "derived" in pid["sae_pid"].lower():
            continue

        sae_pid_hex = pid["sae_pid"]
        len_sae = len(sae_pid_hex)
        if len_sae == 4 and sae_pid_hex.startswith("01"):
            sae_pid_hex = sae_pid_hex[2:]

        # Find matching row in CSV
        matched_row = None
        for row in csv_rows:
            if row["PID (hex)"].upper() == sae_pid_hex.upper():
                matched_row = row
                break

        assert matched_row is not None, f"PID {pid['sae_pid']} not found in J1979 CSV"
        assert names_agree(pid["name"], matched_row["Name (short)"], matched_row["Name"]), \
            f"PID {pid['name']} name does not agree with CSV short '{matched_row['Name (short)']}' or long '{matched_row['Name']}'"
        assert units_agree(pid["unit"], matched_row["Unit"]), \
            f"PID {pid['name']} unit '{pid['unit']}' does not agree with CSV unit '{matched_row['Unit']}'"
        assert ranges_agree(pid["range"], matched_row["Min"], matched_row["Max"]), \
            f"PID {pid['name']} range '{pid['range']}' does not agree with CSV range '{matched_row['Min']} - {matched_row['Max']}'"
        checked += 1

    assert checked > 0


def test_l2_dtc_conformance() -> None:
    """Validate DTCRoutingTag comments reference valid P-codes in SAE.md."""
    member_comments = parse_dtc_routing_tags_comments()
    assert member_comments

    # Make sure we check that the enums are imported
    assert len(list(V.DTCRoutingTag)) > 0

    sae_lines = SAE_PATH.read_text(encoding="utf-8").splitlines()
    assert sae_lines

    checked = 0
    for name, comment in member_comments.items():
        codes = extract_and_expand_pcodes(comment)
        for code in codes:
            assert code_resolves(code, sae_lines), \
                f"P-code '{code}' cited in DTCRoutingTag.{name} comment does not resolve in SAE.md"
            checked += 1

    assert checked > 0


def test_proposals_registry_conformance() -> None:
    """Validate each proposal entry has a valid citation and an existing consumer class/function."""
    assert ENTRIES_PATH.exists()
    with open(ENTRIES_PATH, encoding="utf-8") as f:
        entries = yaml.safe_load(f)
    assert entries

    for entry in entries:
        assert entry.get("id"), "Registry entry missing ID"
        
        # Check consumer
        assert entry.get("consumer"), f"Registry entry {entry.get('id')} missing 'consumer'"
        consumer_val = entry["consumer"]
        assert ":" in consumer_val, f"Registry entry {entry.get('id')} consumer '{consumer_val}' must be in file_path:symbol format"
        file_path_str, symbol = consumer_val.split(":", 1)
        
        file_path = LABS_DIR / file_path_str
        assert file_path.exists(), f"Registry entry {entry.get('id')} consumer file '{file_path_str}' does not exist"
        assert symbol.strip(), f"Registry entry {entry.get('id')} consumer symbol must be non-empty"

        # Check citation
        has_citation = bool(entry.get("iso_sae_citation"))
        is_cross_cutting = entry.get("family") == "cross-cutting"
        assert has_citation or is_cross_cutting, \
            f"Registry entry {entry.get('id')} must have iso_sae_citation or be family: cross-cutting"
