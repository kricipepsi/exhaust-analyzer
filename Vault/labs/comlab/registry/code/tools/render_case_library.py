#!/usr/bin/env python3
"""Render case library from curated corpus.

Consumes corpus_curated.csv + corpus_meta.json.
Emits a static, self-contained HTML case library grouped by family under docs/case_library.html.
"""

import csv
import json
import html
from pathlib import Path

__all__ = [
    "main",
    "escape_html",
]


def escape_html(val: str | None) -> str:
    """Safely escape HTML special characters, returning empty string for None."""
    if val is None:
        return ""
    return html.escape(str(val))


def main() -> None:
    # Resolve paths relative to script location
    script_dir = Path(__file__).resolve().parent
    registry_dir = script_dir.parent
    csv_path = registry_dir / "corpus_curated.csv"
    meta_path = registry_dir / "corpus_meta.json"
    output_dir = registry_dir / "docs"
    output_path = output_dir / "case_library.html"

    # Ensure output directory exists
    output_dir.mkdir(parents=True, exist_ok=True)

    # Read metadata to get counts
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    # Calculate expected family counts from metadata (where disposition is not drop)
    meta_family_counts = {}
    for c in meta["cases"]:
        if c.get("disposition") != "drop":
            fam = c.get("expected_top_fault_family") or ""
            meta_family_counts[fam] = meta_family_counts.get(fam, 0) + 1

    # Read curated CSV cases
    cases = []
    with open(csv_path, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            cases.append(row)

    # Group cases by expected_top_fault_family
    grouped_cases = {}
    for case in cases:
        fam = case.get("expected_top_fault_family") or ""
        if fam not in grouped_cases:
            grouped_cases[fam] = []
        grouped_cases[fam].append(case)

    # Sort groups by family name (deterministic), with empty family first if present
    sorted_families = sorted(grouped_cases.keys())

    # Sort cases within each family by case_id (deterministic)
    for fam in sorted_families:
        grouped_cases[fam] = sorted(grouped_cases[fam], key=lambda x: x.get("case_id", ""))

    # Generate HTML content
    html_lines = []
    html_lines.append("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>4DLab Case Library</title>
    <style>
        :root {
            --bg-color: #0b0f19;
            --card-bg: #111827;
            --text-primary: #f3f4f6;
            --text-secondary: #9ca3af;
            --border-color: #1f2937;
            --primary-accent: #6366f1;
            --secondary-accent: #a855f7;
            --success-color: #10b981;
            --warning-color: #f59e0b;
            --danger-color: #ef4444;
            --badge-bg: #1f2937;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--bg-color);
            color: var(--text-primary);
            font-family: 'Outfit', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            line-height: 1.5;
            padding-bottom: 4rem;
        }

        .header {
            background: linear-gradient(135deg, #1e1b4b 0%, #111827 100%);
            border-bottom: 1px solid var(--border-color);
            padding: 2.5rem 2rem;
            position: relative;
            overflow: hidden;
        }

        .header::after {
            content: '';
            position: absolute;
            top: 0;
            right: 10%;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(99, 102, 241, 0.15) 0%, transparent 70%);
            pointer-events: none;
        }

        .header-container {
            max-width: 1400px;
            margin: 0 auto;
        }

        .header h1 {
            font-size: 2.25rem;
            font-weight: 700;
            letter-spacing: -0.025em;
            background: linear-gradient(to right, #818cf8, #c084fc);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }

        .header p {
            color: var(--text-secondary);
            font-size: 1rem;
        }

        .stats-row {
            display: flex;
            gap: 1.5rem;
            margin-top: 1.5rem;
            flex-wrap: wrap;
        }

        .stat-card {
            background: rgba(31, 41, 55, 0.4);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            backdrop-filter: blur(4px);
        }

        .stat-label {
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
        }

        .stat-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--primary-accent);
        }

        .container {
            max-width: 1400px;
            margin: 2rem auto;
            padding: 0 2rem;
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 2rem;
        }

        @media (max-width: 1024px) {
            .container {
                grid-template-columns: 1fr;
            }
        }

        .sidebar {
            position: sticky;
            top: 2rem;
            align-self: start;
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
        }

        .sidebar-title {
            font-size: 0.875rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 1px solid var(--border-color);
        }

        .nav-list {
            list-style: none;
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
            max-height: 70vh;
            overflow-y: auto;
            padding-right: 0.5rem;
        }

        .nav-list::-webkit-scrollbar {
            width: 4px;
        }

        .nav-list::-webkit-scrollbar-thumb {
            background-color: var(--border-color);
            border-radius: 2px;
        }

        .nav-item a {
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: var(--text-secondary);
            text-decoration: none;
            font-size: 0.9rem;
            padding: 0.5rem 0.75rem;
            border-radius: 6px;
            transition: all 0.2s ease;
        }

        .nav-item a:hover {
            background-color: var(--border-color);
            color: var(--text-primary);
            padding-left: 1rem;
        }

        .nav-item.active a {
            background: rgba(99, 102, 241, 0.1);
            border-left: 3px solid var(--primary-accent);
            color: var(--primary-accent);
            font-weight: 600;
        }

        .family-badge {
            background-color: var(--badge-bg);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            font-size: 0.75rem;
            padding: 0.1rem 0.5rem;
            border-radius: 10px;
            font-weight: 600;
        }

        .main-content {
            display: flex;
            flex-direction: column;
            gap: 3rem;
        }

        .controls {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            display: flex;
            gap: 1.5rem;
            align-items: center;
            flex-wrap: wrap;
        }

        .search-wrapper {
            flex: 1;
            min-width: 300px;
            position: relative;
        }

        .search-input {
            width: 100%;
            background-color: var(--bg-color);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.75rem 1rem;
            color: var(--text-primary);
            font-size: 0.95rem;
            transition: border-color 0.2s ease;
        }

        .search-input:focus {
            outline: none;
            border-color: var(--primary-accent);
        }

        .view-toggles {
            display: flex;
            gap: 0.5rem;
        }

        .btn {
            background-color: var(--badge-bg);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
            padding: 0.6rem 1.2rem;
            border-radius: 8px;
            cursor: pointer;
            font-size: 0.875rem;
            font-weight: 600;
            transition: all 0.2s ease;
        }

        .btn:hover {
            border-color: var(--text-secondary);
            color: var(--text-primary);
        }

        .btn.active {
            background-color: var(--primary-accent);
            border-color: var(--primary-accent);
            color: white;
        }

        .family-section {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
            scroll-margin-top: 2rem;
        }

        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: baseline;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 0.75rem;
            margin-bottom: 0.5rem;
        }

        .section-header h2 {
            font-size: 1.5rem;
            font-weight: 700;
            color: #f3f4f6;
            text-transform: capitalize;
        }

        .section-header h2 span {
            color: var(--primary-accent);
        }

        .grid-layout {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(500px, 1fr));
            gap: 1.5rem;
        }

        @media (max-width: 640px) {
            .grid-layout {
                grid-template-columns: 1fr;
            }
        }

        .case-card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            display: flex;
            flex-direction: column;
            gap: 1.25rem;
            transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
        }

        .case-card:hover {
            transform: translateY(-2px);
            border-color: rgba(99, 102, 241, 0.4);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.3);
        }

        .card-top {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 1rem;
        }

        .case-id {
            background: linear-gradient(135deg, var(--primary-accent) 0%, var(--secondary-accent) 100%);
            color: white;
            font-weight: 700;
            font-size: 0.85rem;
            padding: 0.25rem 0.75rem;
            border-radius: 6px;
            letter-spacing: 0.05em;
        }

        .case-desc {
            font-size: 1.05rem;
            font-weight: 600;
            color: var(--text-primary);
            flex: 1;
        }

        .data-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }

        @media (max-width: 480px) {
            .data-grid {
                grid-template-columns: 1fr;
            }
        }

        .data-panel {
            background-color: rgba(17, 24, 39, 0.6);
            border: 1px solid rgba(31, 41, 55, 0.6);
            border-radius: 8px;
            padding: 0.85rem;
        }

        .panel-title {
            font-size: 0.75rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.25rem;
        }

        .metric-row {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            padding: 0.15rem 0;
        }

        .metric-label {
            color: var(--text-secondary);
        }

        .metric-val {
            font-family: monospace;
            font-weight: 600;
            color: var(--text-primary);
        }

        .metric-val.alert {
            color: var(--warning-color);
        }

        .metric-val.highlight {
            color: var(--success-color);
        }

        .verdict-box {
            background: rgba(99, 102, 241, 0.05);
            border: 1px dashed rgba(99, 102, 241, 0.3);
            border-radius: 8px;
            padding: 0.85rem;
        }

        .dtcs-row {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-bottom: 0.5rem;
        }

        .dtc-badge {
            background-color: rgba(245, 158, 11, 0.1);
            border: 1px solid rgba(245, 158, 11, 0.3);
            color: var(--warning-color);
            font-family: monospace;
            font-weight: 700;
            font-size: 0.75rem;
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
        }

        .reasoning-box {
            font-size: 0.875rem;
            color: var(--text-secondary);
            background-color: rgba(31, 41, 55, 0.2);
            border-left: 3px solid var(--secondary-accent);
            padding: 0.75rem;
            border-radius: 0 6px 6px 0;
            font-style: italic;
        }

        .verdict-info {
            display: flex;
            flex-direction: column;
            gap: 0.25rem;
        }

        .verdict-row {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
        }

        .verdict-label {
            color: var(--text-secondary);
        }

        .verdict-val {
            font-weight: 600;
        }

        .verdict-val.accent {
            color: #818cf8;
            font-weight: 700;
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="header-container">
            <h1>4DLab Curated Case Library</h1>
            <p>Static index of all reference cases used to validate the rule registry</p>
            <div class="stats-row">
                <div class="stat-card">
                    <div class="stat-label">Total Curated Cases</div>
                    <div class="stat-value">""")
    html_lines.append(f"{len(cases)}")
    html_lines.append("""</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">Fault Families</div>
                    <div class="stat-value">""")
    html_lines.append(f"{len([f for f in sorted_families if f])}")
    html_lines.append("""</div>
                </div>
            </div>
        </div>
    </header>

    <div class="container">
        <aside class="sidebar">
            <h3 class="sidebar-title">Families</h3>
            <ul class="nav-list">""")

    # Populate sidebar index
    for fam in sorted_families:
        display_fam = fam if fam else "(no family)"
        count = len(grouped_cases[fam])
        html_lines.append(f'                <li class="nav-item" data-family-target="{escape_html(fam)}">')
        html_lines.append(f'                    <a href="#{escape_html(fam)}">')
        html_lines.append(f'                        <span>{escape_html(display_fam)}</span>')
        html_lines.append(f'                        <span class="family-badge" data-family="{escape_html(fam)}">{count}</span>')
        html_lines.append('                    </a>')
        html_lines.append('                </li>')

    html_lines.append("""            </ul>
        </aside>

        <main class="main-content">
            <div class="controls">
                <div class="search-wrapper">
                    <input type="text" class="search-input" id="searchInput" placeholder="Search by case ID, description, reasoning, DTCs...">
                </div>
                <div class="view-toggles">
                    <button class="btn active" id="btnGrid">Grid View</button>
                    <button class="btn" id="btnList">List View</button>
                </div>
            </div>""")

    # Render cases grouped by family
    for fam in sorted_families:
        display_fam = fam if fam else "(no family)"
        count = len(grouped_cases[fam])
        html_lines.append(f'            <section class="family-section" id="{escape_html(fam)}" data-family-sec="{escape_html(fam)}">')
        html_lines.append('                <div class="section-header">')
        html_lines.append(f'                    <h2>{escape_html(display_fam)}</h2>')
        html_lines.append(f'                    <span class="family-badge">{count} cases</span>')
        html_lines.append('                </div>')
        html_lines.append('                <div class="grid-layout" id="layout-' + escape_html(fam) + '">')

        for case in grouped_cases[fam]:
            case_id = case.get("case_id", "")
            description = case.get("description", "")
            reasoning = case.get("reasoning", "")

            # Gas
            hc = case.get("hc", "")
            co = case.get("co", "")
            co2 = case.get("co2", "")
            o2 = case.get("o2", "")
            nox = case.get("nox", "")
            lambda_anal = case.get("lambda_analyser", "")

            # OBD / trims
            stft1 = case.get("stft_b1", "")
            ltft1 = case.get("ltft_b1", "")
            stft2 = case.get("stft_b2", "")
            ltft2 = case.get("ltft_b2", "")
            obd_lambda = case.get("obd_lambda", "")
            map_val = case.get("map", "")
            maf = case.get("maf", "")
            rpm = case.get("rpm", "")
            ect = case.get("ect", "")

            # DTCs
            dtcs_raw = case.get("dtcs", "")
            # Sometimes dtcs is a json string like '["P0171"]' or list format or comma-separated
            dtc_badges = []
            if dtcs_raw:
                try:
                    # Try json list parse
                    dtc_list = json.loads(dtcs_raw.replace("'", '"'))
                    if isinstance(dtc_list, list):
                        dtc_badges = dtc_list
                    else:
                        dtc_badges = [str(dtc_list)]
                except Exception:
                    # Fallback to splitting by comma
                    dtc_badges = [d.strip() for d in dtcs_raw.split(",") if d.strip()]

            # Expected
            expected_fault = case.get("expected_top_fault", "")
            expected_state = case.get("expected_state", "")
            conf_min = case.get("expected_confidence_min", "")
            conf_max = case.get("expected_confidence_max", "")

            html_lines.append(f'                    <div class="case-card" data-case-id="{escape_html(case_id)}" data-family-card="{escape_html(fam)}">')
            html_lines.append('                        <div class="card-top">')
            html_lines.append(f'                            <span class="case-id">{escape_html(case_id)}</span>')
            html_lines.append(f'                            <div class="case-desc">{escape_html(description)}</div>')
            html_lines.append('                        </div>')

            html_lines.append('                        <div class="data-grid">')
            # Gas readings panel
            html_lines.append('                            <div class="data-panel">')
            html_lines.append('                                <div class="panel-title">Gas Chemistry</div>')
            html_lines.append(f'                                <div class="metric-row"><span class="metric-label">HC</span><span class="metric-val">{escape_html(hc)} ppm</span></div>')
            html_lines.append(f'                                <div class="metric-row"><span class="metric-label">CO</span><span class="metric-val">{escape_html(co)}%</span></div>')
            html_lines.append(f'                                <div class="metric-row"><span class="metric-label">CO₂</span><span class="metric-val">{escape_html(co2)}%</span></div>')
            html_lines.append(f'                                <div class="metric-row"><span class="metric-label">O₂</span><span class="metric-val">{escape_html(o2)}%</span></div>')
            html_lines.append(f'                                <div class="metric-row"><span class="metric-label">NOx</span><span class="metric-val">{escape_html(nox)} ppm</span></div>')
            html_lines.append(f'                                <div class="metric-row"><span class="metric-label">λ Analyser</span><span class="metric-val highlight">{escape_html(lambda_anal)}</span></div>')
            html_lines.append('                            </div>')

            # OBD panel
            html_lines.append('                            <div class="data-panel">')
            html_lines.append('                                <div class="panel-title">OBD / Air / Engine</div>')
            if stft1 or ltft1:
                html_lines.append(f'                                <div class="metric-row"><span class="metric-label">Trims B1 (ST/LT)</span><span class="metric-val">{escape_html(stft1)}% / {escape_html(ltft1)}%</span></div>')
            if stft2 or ltft2:
                html_lines.append(f'                                <div class="metric-row"><span class="metric-label">Trims B2 (ST/LT)</span><span class="metric-val">{escape_html(stft2)}% / {escape_html(ltft2)}%</span></div>')
            if obd_lambda:
                html_lines.append(f'                                <div class="metric-row"><span class="metric-label">ECU λ</span><span class="metric-val">{escape_html(obd_lambda)}</span></div>')
            if map_val:
                html_lines.append(f'                                <div class="metric-row"><span class="metric-label">MAP</span><span class="metric-val">{escape_html(map_val)} kPa</span></div>')
            if maf:
                html_lines.append(f'                                <div class="metric-row"><span class="metric-label">MAF</span><span class="metric-val">{escape_html(maf)} g/s</span></div>')
            if rpm:
                html_lines.append(f'                                <div class="metric-row"><span class="metric-label">RPM</span><span class="metric-val">{escape_html(rpm)}</span></div>')
            if ect:
                html_lines.append(f'                                <div class="metric-row"><span class="metric-label">ECT</span><span class="metric-val">{escape_html(ect)}°C</span></div>')
            html_lines.append('                            </div>')
            html_lines.append('                        </div>')

            # Expected Verdict Box
            html_lines.append('                        <div class="verdict-box">')
            html_lines.append('                            <div class="dtcs-row">')
            for badge in dtc_badges:
                html_lines.append(f'                                <span class="dtc-badge">{escape_html(badge)}</span>')
            if not dtc_badges:
                html_lines.append('                                <span class="metric-label" style="font-size:0.75rem;">No DTCs stored</span>')
            html_lines.append('                            </div>')
            html_lines.append('                            <div class="verdict-info">')
            html_lines.append(f'                                <div class="verdict-row"><span class="verdict-label">Expected Fault</span><span class="verdict-val accent">{escape_html(expected_fault)}</span></div>')
            html_lines.append(f'                                <div class="verdict-row"><span class="verdict-label">Expected State</span><span class="verdict-val">{escape_html(expected_state)}</span></div>')
            if conf_min or conf_max:
                html_lines.append(f'                                <div class="verdict-row"><span class="verdict-label">Confidence Range</span><span class="verdict-val">{escape_html(conf_min)} – {escape_html(conf_max)}</span></div>')
            html_lines.append('                            </div>')
            html_lines.append('                        </div>')

            # Reasoning
            if reasoning:
                html_lines.append(f'                        <div class="reasoning-box">{escape_html(reasoning)}</div>')

            html_lines.append('                    </div>')

        html_lines.append('                </div>')
        html_lines.append('            </section>')

    html_lines.append("""        </main>
    </div>

    <script>
        // Client-side search and view toggle
        const searchInput = document.getElementById('searchInput');
        const btnGrid = document.getElementById('btnGrid');
        const btnList = document.getElementById('btnList');
        const cards = document.querySelectorAll('.case-card');
        const sections = document.querySelectorAll('.family-section');
        const navItems = document.querySelectorAll('.nav-list .nav-item');

        // Search logic
        searchInput.addEventListener('input', () => {
            const query = searchInput.value.toLowerCase().strip();
            
            // Loop through each case card
            cards.forEach(card => {
                const text = card.textContent.toLowerCase();
                if (text.includes(query)) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });

            // Hide sections with no visible cards
            sections.forEach(sec => {
                const secId = sec.getAttribute('data-family-sec');
                const visibleCards = sec.querySelectorAll(`.case-card[data-family-card="${secId}"]`);
                let hasVisible = false;
                visibleCards.forEach(c => {
                    if (c.style.display !== 'none') {
                        hasVisible = true;
                    }
                });
                if (hasVisible) {
                    sec.style.display = 'flex';
                } else {
                    sec.style.display = 'none';
                }
            });

            // Update sidebar counts to reflect search results
            navItems.forEach(item => {
                const target = item.getAttribute('data-family-target');
                const badge = item.querySelector('.family-badge');
                const sec = document.getElementById(target);
                if (sec) {
                    const visibleCount = Array.from(sec.querySelectorAll('.case-card')).filter(c => c.style.display !== 'none').length;
                    badge.textContent = visibleCount;
                    if (visibleCount === 0) {
                        item.style.display = 'none';
                    } else {
                        item.style.display = 'block';
                    }
                }
            });
        });

        // String trim utility fallback
        if (!String.prototype.strip) {
            String.prototype.strip = function() {
                return this.trim();
            };
        }

        // Layout toggle logic
        btnGrid.addEventListener('click', () => {
            btnGrid.classList.add('active');
            btnList.classList.remove('active');
            sections.forEach(sec => {
                const layout = sec.querySelector('.grid-layout');
                if (layout) {
                    layout.style.gridTemplateColumns = 'repeat(auto-fill, minmax(500px, 1fr))';
                }
            });
        });

        btnList.addEventListener('click', () => {
            btnList.classList.add('active');
            btnGrid.classList.remove('active');
            sections.forEach(sec => {
                const layout = sec.querySelector('.grid-layout');
                if (layout) {
                    layout.style.gridTemplateColumns = '1fr';
                }
            });
        });

        // Sidebar active state highlights on scroll
        window.addEventListener('scroll', () => {
            let currentSec = '';
            sections.forEach(sec => {
                const secTop = sec.offsetTop;
                if (window.scrollY >= secTop - 100) {
                    currentSec = sec.getAttribute('id');
                }
            });
            navItems.forEach(item => {
                item.classList.remove('active');
                if (item.getAttribute('data-family-target') === currentSec) {
                    item.classList.add('active');
                }
            });
        });
    </script>
</body>
</html>""")

    # Write HTML output
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(html_lines))

    print(f"Rendered {len(cases)} cases successfully to {output_path}")


if __name__ == "__main__":
    main()
