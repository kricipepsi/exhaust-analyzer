#!/usr/bin/env python3
"""Flask Web App: 5-Gas Exhaust Analyzer"""

from flask import Flask, render_template, request, flash, redirect, url_for
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from engine.assessor import DiagnosticEngine

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
        except ValueError as e:
            flash(f"Invalid input: all fields must be numbers. {e}")
            return redirect(url_for("index"))
        except Exception as e:
            flash(f"Error during analysis: {e}")
            return redirect(url_for("index"))
    return render_template("index.html", results=results)

if __name__ == "__main__":
    # Run development server
    print("Starting Exhaust Analyzer on http://localhost:5000")
    app.run(debug=True, host="0.0.0.0", port=5000)
