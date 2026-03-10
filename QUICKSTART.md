# 5-Gas Exhaust Analyzer – Quick Start

## Run It

```bash
cd exhaust-analyzer
pip install -r requirements.txt
python app.py
```

Open: http://localhost:5000

## Input Guide

- **Lambda (λ)**: Air/fuel ratio relative to stoichiometric (1.00 = stoich)
- **CO**: Carbon monoxide (% volume)
- **CO2**: Carbon dioxide (% volume)
- **O2**: Oxygen (% volume)
- **HC**: Unburned hydrocarbons (ppm)
- **NOx**: Nitrogen oxides (ppm)

Enter values for both **Idle** (~800 rpm, warm engine) and **High Idle** (~1500-2000 rpm).

## Normal Ranges (Petrol, 1990s–2000s)

| Condition | Lambda | CO | CO2 | O2 | HC | NOx |
|-----------|--------|----|-----|----|----|-----|
| Idle | 0.98–1.02 | <0.2% | 12–14% | 0.3–1.0% | 50–150 ppm | <100 ppm |
| High Idle | 0.98–1.02 | <0.3% | 13–15% | 0.5–1.5% | 30–120 ppm | 50–200 ppm |

## Fault Patterns Detected

- **Rich mixture** – λ < 0.9, high CO, low O2
- **Lean mixture** – λ > 1.1, high O2, high NOx
- **Misfire** – HC > 2000 ppm, low CO/CO2, high O2
- **EGR stuck open (idle)** – elevated HC with normal λ
- **Catalyst failure** – high CO + high HC (+ high O2 if completely failed)
- **Ignition timing** – high NOx with normal/lean λ
- **O2 sensor failure** – λ stuck, O2 not switching
- **MAF sensor fault** – misreporting airflow → lean or rich
- **Weak fuel pump** – lean under load
- **Clogged air filter** – slightly rich, reduced CO2
- **Oxygen sensor lazy** – slow switching

Each pattern produces:
- Health score (0–100)
- Ranked list of likely culprits
- Specific recommendations

## Example Scenarios

See `test_scenarios.py` for 10 realistic test cases covering normal, rich, lean, misfire, EGR, timing, O2 sensor, MAF, fuel pump, air filter.

## Extending

Add new patterns in `knowledge/knowledge_base.py` → `FAULT_PATTERNS`. Each entry:
```python
"pattern_name": {
    "indicators": {
        "lambda": ">1.10",
        "co": "low",
        # ...
    },
    "culprits": ["Cause 1", "Cause 2"],
    "notes": "Explanation"
}
```

Supported indicator comparisons: `<value`, `>value`, `low`, `high`, `moderate`, `variable`. See `engine/assessor.py` `match_patterns()` for implementation.

## Deployment Options

- **Standalone**: `python app.py` (development only)
- **Production**: Use WSGI server (gunicorn, waitress) + reverse proxy (nginx, Apache). Set `FLASK_APP=app.py`, `FLASK_ENV=production`.
- **Docker**: Create Dockerfile with Python 3.10, copy files, install requirements, expose 5000.
- **Static hosting**: Not applicable (requires Python backend).

## Files

```
exhaust-analyzer/
├── app.py                 # Flask entrypoint
├── requirements.txt       # Python deps (Flask only)
├── knowledge/
│   └── knowledge_base.py  # Normal ranges & patterns
├── engine/
│   └── assessor.py        # Diagnostic logic
├── static/
│   └── style.css          # Modern responsive UI
├── templates/
│   └── index.html         # Form + results + Chart.js
├── test_scenarios.py      # Automated tests
└── README.md              # Full documentation
```
