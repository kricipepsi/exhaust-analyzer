# 5-Gas Exhaust Analyzer

A web-based diagnostic tool that analyzes exhaust gas measurements (CO, CO2, O2, HC, NOx, Lambda) at idle and high idle to assess engine health and suggest potential faults.

## Features

- Input measurements for both idle and high idle conditions
- Automatic comparison to normal ranges derived from automotive expertise
- Pattern matching against known fault signatures (rich, lean, misfire, EGR, catalyst, timing)
- Ranked list of likely culprits with confidence scores
- Actionable recommendations for further checks
- Clean, responsive web UI (Flask + Jinja2)

## Knowledge Base

The diagnostic rules are extracted from our comprehensive automotive emissions document (`memory/emissions.md`), covering:

- Normal gas concentration ranges for typical 1990s–2000s petrol engines
- Five-gas interpretation patterns from industry references (MOTOR Magazine, Omitec, Automotive Test Solutions)
- Euro emissions standards context
- UK MOT test limits

## Quick Start

1. Ensure Python 3.10+ and Flask are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Flask development server:
   ```bash
   python app.py
   ```

3. Open browser to http://localhost:5000

4. Fill in measurements (both idle and high idle sections) and click "Analyze".

## Sample Data (for testing)

Idle:
- Lambda: 0.95
- CO: 1.5%
- CO2: 13.0%
- O2: 0.4%
- HC: 200 ppm
- NOx: 80 ppm

High Idle:
- Lambda: 0.97
- CO: 1.2%
- CO2: 14.0%
- O2: 0.8%
- HC: 120 ppm
- NOx: 150 ppm

This dataset indicates a **rich mixture** (moderate deviations).

## Project Structure

```
exhaust-analyzer/
├── app.py                 # Flask application
├── requirements.txt       # Python dependencies
├── knowledge/
│   └── knowledge_base.py  # Normal ranges and fault patterns
├── engine/
│   └── assessor.py        # Diagnostic engine
├── static/
│   └── style.css          # Simple styling
└── templates/
    └── index.html         # Form + results page
```

## How It Works

1. **Input validation** – checks for plausible numeric ranges (e.g., CO < 20%, O2 < 25%)
2. **Deviation detection** – compares each gas reading to normal range for the condition (idle vs high idle)
3. **Pattern matching** – evaluates fault signatures based on which gases are out of spec and in what direction
4. **Scoring** – health score 0–100 based on number and severity of deviations
5. **Recommendations** – generates targeted next-check list based on detected issues

## Future Enhancements

- Store results in SQLite for tracking over time
- Add support for lambda estimation from O2/CO/CO2 when lambda sensor absent
- Include vehicle-specific baseline adjustments (engine size, ASP, etc.)
- Export report to PDF
- Mobile-friendly UI with charts
- Integration with OBD-II readers for automated data capture

## Limitations

- Designed for petrol (gasoline) engines only
- Diesel and modern GDI engines have different normal ranges
- Does not account for altitude, temperature, or fuel composition variations
- Pattern matching is heuristic, not a substitute for professional diagnosis

## Credits

Knowledge extracted from `memory/emissions.md` – a comprehensive reference compiled from industry sources including MOTOR Magazine, Omitec, Automotive Test Solutions, and VEMS calibration experience.
