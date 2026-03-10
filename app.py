#!/usr/bin/env python3
"""Flask Web App: 5-Gas Exhaust Analyzer with MOT Query"""

from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
import sys
import os
from dataclasses import asdict

# Add project root to path for knowledge module import
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from engine.assessor import DiagnosticEngine
from knowledge.mot_query_api import query_vehicle_info, get_reference_values
from knowledge.diagnostic_api import analyze_emissions

app = Flask(__name__)
app.secret_key = "exhaust-analyzer-demo"  # for flash messages

@app.route("/", methods=["GET", "POST"])
def index():
    results = None
    if request.method == "POST":
        try:
            # Collect idle measurements
            idle = {
                "lambda": float(request.form.get("lambda_idle")),
                "co": float(request.form.get("co_idle")),
                "co2": float(request.form.get("co2_idle")),
                "o2": float(request.form.get("o2_idle")),
                "hc": float(request.form.get("hc_idle")),
                "nox": float(request.form.get("nox_idle")),
            }
            # Collect high idle measurements
            high = {
                "lambda": float(request.form.get("lambda_high")),
                "co": float(request.form.get("co_high")),
                "co2": float(request.form.get("co2_high")),
                "o2": float(request.form.get("o2_high")),
                "hc": float(request.form.get("hc_high")),
                "nox": float(request.form.get("nox_high")),
            }
            engine = DiagnosticEngine(rpm=800)  # idle rpm
            results = engine.assess(idle, high)

            # Gather vehicle info and OBD data for unified analysis
            vehicle_make = request.form.get("vehicle_make", "").strip()
            vehicle_model = request.form.get("vehicle_model", "").strip()
            vehicle_year = request.form.get("vehicle_year", "").strip()
            vehicle_fuel = request.form.get("vehicle_fuel_type", "").strip()
            vehicle_catalyst = request.form.get("vehicle_has_catalyst") == "on"

            dtc_codes_raw = request.form.get("dtc_codes", "").strip()
            dtc_list = [code.strip().upper() for code in dtc_codes_raw.splitlines() if code.strip()]

            stft = ltft = None
            stft_raw = request.form.get("stft", "").strip()
            ltft_raw = request.form.get("ltft", "").strip()
            try:
                stft = float(stft_raw) if stft_raw else None
            except:
                pass
            try:
                ltft = float(ltft_raw) if ltft_raw else None
            except:
                pass

            fuel_trims = {}
            if stft is not None or ltft is not None:
                fuel_trims = {"stft": stft, "ltft": ltft}

            data = {
                "idle": idle,
                "high": high,
                "dtc_codes": dtc_list,
                "fuel_trims": fuel_trims,
                "vehicle_info": {
                    "make": vehicle_make,
                    "model": vehicle_model,
                    "year": vehicle_year,
                    "fuel_type": vehicle_fuel,
                    "has_catalyst": vehicle_catalyst
                } if all([vehicle_make, vehicle_model, vehicle_year, vehicle_fuel]) else None
            }

            # Unified analysis via helper
            results = perform_full_analysis(data)
        except ValueError as e:
            flash(f"Invalid input: all fields must be numbers. {e}")
            return redirect(url_for("index"))
        except Exception as e:
            flash(f"Error during analysis: {e}")
            return redirect(url_for("index"))
    return render_template("index.html", results=results)

@app.route("/mot-query", methods=["GET", "POST"])
def mot_query():
    """MOT test determination based on vehicle details."""
    result = None
    if request.method == "POST":
        try:
            # Get form data
            make = request.form.get("make", "").strip()
            model = request.form.get("model", "").strip()
            first_use_date = request.form.get("first_use_date", "").strip()
            fuel_type = request.form.get("fuel_type", "petrol").strip()
            engine_code = request.form.get("engine_code", "").strip() or None
            has_catalyst = request.form.get("has_catalyst") == "on"
            dgw_kg = request.form.get("dgw_kg", type=int)
            seat_count = request.form.get("seat_count", type=int)

            if not all([make, model, first_use_date]):
                flash("Make, model, and first use date are required.")
                return redirect(url_for("mot_query"))

            result = query_vehicle_info(
                make=make,
                model=model,
                first_use_date=first_use_date,
                fuel_type=fuel_type,
                engine_code=engine_code,
                has_catalyst=has_catalyst,
                dgw_kg=dgw_kg,
                seat_count=seat_count
            )
        except Exception as e:
            flash(f"Query error: {e}")
            return redirect(url_for("mot_query"))

    return render_template("mot_query.html", result=result)

@app.route("/api/mot/query", methods=["POST"])
def api_mot_query():
    """JSON API endpoint for MOT test determination (for mobile app)."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "JSON body required"}), 400

    required = ["make", "model", "first_use_date", "fuel_type"]
    if not all(k in data for k in required):
        return jsonify({"error": f"Missing required fields: {required}"}), 400

    try:
        result = query_vehicle_info(
            make=data["make"],
            model=data["model"],
            first_use_date=data["first_use_date"],
            fuel_type=data["fuel_type"],
            engine_code=data.get("engine_code"),
            has_catalyst=data.get("has_catalyst", False),
            dgw_kg=data.get("dgw_kg"),
            seat_count=data.get("seat_count")
        )
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/analyze", methods=["POST"])
def api_analyze():
    """JSON API endpoint for exhaust gas analysis (mobile app integration)."""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "JSON body required"}), 400

        results = perform_full_analysis(data)
        return jsonify(results)
    except Exception as e:
        app.logger.error(f"API analysis error: {e}")
        return jsonify({"error": str(e)}), 500

def perform_full_analysis(data):
    """
    Perform complete analysis from data dict.
    Expected data:
      - idle: {lambda, co, co2, o2, hc, nox}
      - high: {lambda, co, co2, o2, hc, nox}
      - dtc_codes: list of DTC strings (optional)
      - fuel_trims: {stft: float, ltft: float} (optional)
      - vehicle_info: {make, model, year, fuel_type, has_catalyst} (optional for MOT compliance)
    Returns results dict with top-level keys: raw_idle, raw_high, idle, high_idle, overall, advanced_diagnosis, mot_compliance.
    """
    idle = data.get("idle", {})
    high = data.get("high", {})

    # Basic engine assessment using DiagnosticEngine
    try:
        engine = DiagnosticEngine(rpm=800)
        basic = engine.assess(idle, high)
    except Exception as e:
        app.logger.error(f"DiagnosticEngine error: {e}")
        basic = {"idle": {}, "high_idle": {}, "overall": {"health_score": 0, "urgent": False, "recommendations": ["Error during basic assessment"]}}

    # Build results structure expected by template
    results = {
        "raw_idle": idle,
        "raw_high": high,
        "idle": basic.get("idle", {}),
        "high_idle": basic.get("high_idle", {}),
        "overall": basic.get("overall", {})
    }

    # Determine vehicle category
    vehicle_category = None
    vehicle_info = data.get("vehicle_info", {})
    if vehicle_info.get("fuel_type"):
        fuel = vehicle_info["fuel_type"].lower()
        catalyst = vehicle_info.get("has_catalyst", False)
        if fuel == "diesel":
            vehicle_category = "diesel"
        elif fuel in ("petrol", "gas"):
            vehicle_category = "petrol_catalyst" if catalyst else "petrol_non_catalyst"
        else:
            vehicle_category = "petrol_catalyst"

    # Advanced diagnostic analysis
    dtc_list = data.get("dtc_codes", [])
    fuel_trims = data.get("fuel_trims")
    try:
        advanced = analyze_emissions(
            vehicle_category=vehicle_category,
            gas_readings=high,
            dtc_codes=dtc_list,
            fuel_trims=fuel_trims
        )
        results["advanced_diagnosis"] = asdict(advanced)
    except Exception as e:
        app.logger.error(f"Advanced diagnosis error: {e}")
        results["advanced_diagnosis"] = None

    # MOT compliance check if vehicle info provided
    if all(k in vehicle_info for k in ("make", "model", "year", "fuel_type")):
        try:
            ref = get_reference_values(
                make=vehicle_info["make"],
                model=vehicle_info["model"],
                first_use_date=vehicle_info["year"],
                fuel_type=vehicle_info["fuel_type"],
                has_catalyst=vehicle_info.get("has_catalyst", False)
            )
            checks = []
            passed = True

            def num(val):
                try:
                    return float(val)
                except:
                    return None

            # Lambda high
            if ref.get('lambda_high') is not None:
                actual = num(high.get('lambda'))
                if actual is not None:
                    lam_min = ref.get('lambda_min', (ref['lambda_high'] - 0.03))
                    lam_max = ref.get('lambda_max', (ref['lambda_high'] + 0.03))
                    ok = lam_min <= actual <= lam_max
                    checks.append({'parameter': 'Lambda (high idle)', 'actual': actual,
                                   'limit': f'{lam_min}-{lam_max}', 'pass': ok})
                    if not ok: passed = False

            # CO high
            if ref.get('co_high') is not None:
                actual = num(high.get('co'))
                if actual is not None:
                    ok = actual <= ref['co_high']
                    checks.append({'parameter': 'CO (high idle)', 'actual': actual,
                                   'limit': f"<= {ref['co_high']}%", 'pass': ok})
                    if not ok: passed = False

            # HC high
            if ref.get('hc_high') is not None:
                actual = num(high.get('hc'))
                if actual is not None:
                    ok = actual <= ref['hc_high']
                    checks.append({'parameter': 'HC (high idle)', 'actual': actual,
                                   'limit': f"<= {ref['hc_high']} ppm", 'pass': ok})
                    if not ok: passed = False

            # CO idle
            if ref.get('co_idle') is not None:
                actual = num(idle.get('co'))
                if actual is not None:
                    ok = actual <= ref['co_idle']
                    checks.append({'parameter': 'CO (idle)', 'actual': actual,
                                   'limit': f"<= {ref['co_idle']}%", 'pass': ok})
                    if not ok: passed = False

            results['mot_compliance'] = {
                'passed': passed,
                'vehicle': f"{vehicle_info['make']} {vehicle_info['model']} ({vehicle_info['year']})",
                'test_type': ref.get('mot_test_type'),
                'checks': checks,
                'description': ref.get('description')
            }
        except Exception as e:
            app.logger.error(f"MOT compliance error: {e}")

    return results

@app.route("/health")
def health():
    """Health check endpoint for monitoring."""
    return jsonify({"status": "ok", "service": "exhaust-analyzer", "timestamp": datetime.utcnow().isoformat() + "Z"})

if __name__ == "__main__":
    print("Starting Exhaust Analyzer on http://localhost:5000")
    print("Routes: / (emission analyzer), /mot-query (MOT test lookup), /api/mot/query (JSON API), /health")
    app.run(debug=True, host="0.0.0.0", port=5000)
