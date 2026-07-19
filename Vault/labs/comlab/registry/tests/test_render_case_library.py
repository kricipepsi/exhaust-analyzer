"""Unit tests for tools/render_case_library.py."""

import csv
import json
import re
from pathlib import Path
from registry.tools.render_case_library import main


def test_render_case_library_determinism(tmp_path):
    """emits the HTML deterministically on re-run."""
    # Resolve paths relative to test file location
    test_dir = Path(__file__).resolve().parent
    registry_dir = test_dir.parent
    csv_path = registry_dir / "corpus_curated.csv"
    meta_path = registry_dir / "corpus_meta.json"
    html_path = registry_dir / "docs" / "case_library.html"

    # Verify files exist before testing
    assert csv_path.is_file(), f"Missing {csv_path}"
    assert meta_path.is_file(), f"Missing {meta_path}"

    # First run
    main()
    assert html_path.is_file(), "case_library.html was not generated"
    first_content = html_path.read_text(encoding="utf-8")

    # Second run
    main()
    second_content = html_path.read_text(encoding="utf-8")

    assert first_content == second_content, "Rendering is not deterministic (content differs on re-run)"


def test_every_csv_row_rendered_once():
    """Every row in corpus_curated.csv appears exactly once."""
    test_dir = Path(__file__).resolve().parent
    registry_dir = test_dir.parent
    csv_path = registry_dir / "corpus_curated.csv"
    html_path = registry_dir / "docs" / "case_library.html"

    # Parse HTML content
    main()
    content = html_path.read_text(encoding="utf-8")

    # Read curated CSV cases
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        csv_cases = list(reader)

    # Check case counts
    assert len(csv_cases) == 252, f"Expected 252 cases in CSV, got {len(csv_cases)}"

    # Search for data-case-id attributes in HTML
    for case in csv_cases:
        case_id = case["case_id"]
        # Match data-case-id="{case_id}"
        pattern = f'data-case-id="{case_id}"'
        matches = len(re.findall(re.escape(pattern), content))
        assert matches == 1, f"Case {case_id} rendered {matches} times, expected exactly once"


def test_family_counts_match_meta():
    """Family counts rendered on the page match corpus_meta.json curation counts."""
    test_dir = Path(__file__).resolve().parent
    registry_dir = test_dir.parent
    meta_path = registry_dir / "corpus_meta.json"
    html_path = registry_dir / "docs" / "case_library.html"

    # Parse metadata to calculate family counts
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    expected_family_counts = {}
    for c in meta["cases"]:
        if c.get("disposition") != "drop":
            fam = c.get("expected_top_fault_family") or ""
            expected_family_counts[fam] = expected_family_counts.get(fam, 0) + 1

    main()
    content = html_path.read_text(encoding="utf-8")

    # Verify that the badges show the correct counts per family
    for fam, expected_count in expected_family_counts.items():
        # Match `<span class="family-badge" data-family="{fam}">{count}</span>` or similar pattern
        # The script outputs: data-family-target="{fam}" with <span class="family-badge" data-family="{fam}">{count}</span>
        escaped_fam = fam.replace('"', '&quot;').replace('<', '&lt;').replace('>', '&gt;')
        pattern = rf'data-family="{re.escape(escaped_fam)}">{expected_count}</span>'
        assert re.search(pattern, content), f"Family '{fam}' expected count {expected_count} badge not found in HTML"


def test_no_unescaped_user_text():
    """All text fields from the CSV are properly HTML escaped in the output."""
    test_dir = Path(__file__).resolve().parent
    registry_dir = test_dir.parent
    csv_path = registry_dir / "corpus_curated.csv"
    html_path = registry_dir / "docs" / "case_library.html"

    # Make sure we have cases with special characters like <, >, &, ", '
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        csv_cases = list(reader)

    main()
    content = html_path.read_text(encoding="utf-8")

    # Check each column that contains user-supplied text
    text_fields = ["description", "reasoning", "expected_top_fault", "expected_state"]

    for case in csv_cases:
        for field in text_fields:
            val = case.get(field, "")
            if not val:
                continue

            # If the raw value has HTML special characters, they must be escaped in the output
            if any(char in val for char in ['&', '<', '>', '"', "'"]):
                # The raw unescaped string should NOT appear in the HTML
                assert val not in content, f"Unescaped value '{val}' of field '{field}' found in HTML"

                # The escaped value SHOULD appear
                import html
                escaped = html.escape(val)
                assert escaped in content, f"Escaped value '{escaped}' of field '{field}' not found in HTML"
