#!/usr/bin/env python3
"""
Oil-Burn Diagnostic SIMULATION — Citroën 5FR (EP6CDT 1.6 THP, turbo + GDI)
=========================================================================
STANDALONE simulation for the presentation. It does NOT touch the real labs.
Mocks the post-cat-fuel-trim-enabled pipeline (tasks PCT-1..PCT-10 implement
it for real). Numbers are locked to planning/OIL_CASE_SIGNATURES_5FR.md.

Sensor model (Bosch MED17.4, per 5fr.md / O2NBvsWB.md):
  WIDEBAND upstream (S1, reports lambda) + NARROWBAND downstream (S2, reports
  voltage AND runs a secondary post-cat fuel-trim loop: STFT/LTFT B1S2).

Pipeline:  VIN/DNA -> GAS state -> POST-CAT B1S2 signature -> verdict

Run (data only):      python oil_burn_5fr_sim.py [--json]
Run (into Jaeger):    set OTEL_TRACES_EXPORTER=otlp  (env), then run.
  Each case emits a trace:  oil_case_<id> -> gas_state -> post_cat_trim -> verdict
  Endpoint defaults to localhost:4317 (Jaeger v2 OTLP gRPC). Needs:
    pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc
"""
import json
import os
import sys
import time
from dataclasses import dataclass

ENGINE = {
    "vin": "VF7SA5FR8AW511081", "make": "CITROEN", "engine_code": "5FR",
    "displacement_l": 1.6, "cylinders": 4, "induction": "TURBOCHARGED",
    "fuel": "GDI", "euro": "EURO_5", "idle_rpm": 700, "high_idle_rpm": 2500,
    "target_lambda": 1.00, "upstream_o2": "WIDEBAND_AFR",
    "downstream_o2": "NARROWBAND_0_TO_1V", "downstream_trim_role": "SECONDARY_FUEL_TRIM",
}


@dataclass
class Case:
    name: str
    expect: str
    gas_low: dict
    gas_high: dict
    obd: dict
    note: str = ""

    @property
    def slug(self):
        return self.name.split(" (")[0].lower().replace(" ", "_").replace("->", "").replace("__", "_")


CASES = [
    Case("Worn piston rings", "MW-001",
        {"co": 0.15, "co2": 14.2, "o2": 0.5, "hc": 150, "nox": 45, "lam": 1.002},
        {"co": 0.85, "co2": 13.1, "o2": 0.7, "hc": 380, "nox": 180, "lam": 0.985},
        {"stft_s1": -2, "ltft_s1": +5, "stft_b1s2": -6, "ltft_b1s2": -9, "dfco_b1s2": -3,
         "maf": 3.2, "map": 36, "ect": 92, "dn_v": 0.80},
        "Fixed negative LTFT-B1S2 across all RPM; HC worsens with load."),
    Case("Worn valve stem seals", "MW-002",
        {"co": 0.95, "co2": 13.0, "o2": 0.3, "hc": 450, "nox": 35, "lam": 0.962},
        {"co": 0.10, "co2": 14.7, "o2": 0.4, "hc": 60, "nox": 75, "lam": 1.001},
        {"stft_s1": -8, "ltft_s1": -3, "stft_b1s2": -13, "ltft_b1s2": -4, "dfco_b1s2": -2,
         "maf": 3.0, "map": 34, "ect": 92, "dn_v": 0.85},
        "Highly negative STFT-B1S2 at hot idle; gas cleans up at high idle."),
    Case("Blown head gasket (oil->cyl)", "MW-003",
        {"co": 0.65, "co2": 11.0, "o2": 2.6, "hc": 340, "nox": 18, "lam": 1.085},
        {"co": 1.15, "co2": 11.0, "o2": 2.1, "hc": 440, "nox": 38, "lam": 1.055},
        {"stft_s1": +12, "ltft_s1": +10, "stft_b1s2": +4, "ltft_b1s2": +2, "dfco_b1s2": 0,
         "maf": 3.4, "map": 41, "ect": 99, "dn_v": 0.28},
        "Coolant quench: high O2 + low CO2 + suppressed NOx + ECT>95."),
    Case("PCV stuck open", "MW-008",
        {"co": 1.90, "co2": 11.8, "o2": 0.2, "hc": 610, "nox": 25, "lam": 0.925},
        {"co": 0.45, "co2": 13.8, "o2": 0.4, "hc": 170, "nox": 105, "lam": 0.988},
        {"stft_s1": +15, "ltft_s1": +8, "stft_b1s2": -16, "ltft_b1s2": -9, "dfco_b1s2": -4,
         "maf": 4.5, "map": 45, "ect": 92, "dn_v": 0.85},
        "DIVERGENT split: upstream swings POSITIVE, downstream B1S2 NEGATIVE."),
    Case("Turbo turbine-seal leak", "MW-009",
        {"co": 0.07, "co2": 14.5, "o2": 0.5, "hc": 720, "nox": 28, "lam": 1.000},
        {"co": 0.09, "co2": 14.6, "o2": 0.4, "hc": 130, "nox": 80, "lam": 1.002},
        {"stft_s1": +1, "ltft_s1": 0, "stft_b1s2": -7, "ltft_b1s2": -5, "dfco_b1s2": -14,
         "maf": 3.2, "map": 36, "ect": 92, "dn_v": 0.80},
        "Combustion stoich/clean; B1S2 pinned negative even during DFCO."),
]

FAULT_NAMES = {
    "MW-001": "Worn piston rings", "MW-002": "Worn valve stem seals",
    "MW-003": "Head gasket oil-to-cylinder breach", "MW-008": "PCV stuck open",
    "MW-009": "Turbo turbine-seal oil leak",
}


def gas_state(lo, hi):
    if lo["o2"] >= 2.0 and lo["co2"] < 11.5 and lo["nox"] < 30 and lo["lam"] > 1.05:
        return "COOLANT_LEAK_INTERNAL"
    if lo["hc"] >= 300 and hi["hc"] < 100:
        return "WORN_VALVE_SEALS"
    if lo["hc"] <= 200 and hi["hc"] > lo["hc"] + 150:
        return "WORN_PISTON_RINGS"
    if lo["hc"] >= 500 and hi["hc"] < 250:
        return "POA_SIGNATURE"
    return "INDETERMINATE"


def post_cat_signature(obd):
    up = obd["stft_s1"] + obd["ltft_s1"]
    dn = obd["stft_b1s2"] + obd["ltft_b1s2"]
    if up > 10 and dn < -10:
        return "DIVERGENT"
    if obd["dfco_b1s2"] <= -10:
        return "DFCO_NEGATIVE"
    if obd["ltft_b1s2"] <= -7 and abs(obd["stft_b1s2"]) <= abs(obd["ltft_b1s2"]) + 4:
        return "FIXED_NEGATIVE"
    if obd["stft_b1s2"] <= -10:
        return "TRANSIENT_NEGATIVE"
    return "NEUTRAL"


def diagnose(case):
    st = gas_state(case.gas_low, case.gas_high)
    sig = post_cat_signature(case.obd)
    if st == "COOLANT_LEAK_INTERNAL" and case.obd["ect"] > 95:
        return st, sig, "MW-003", 0.93
    if st == "WORN_VALVE_SEALS":
        return st, sig, "MW-002", 0.90
    if st == "WORN_PISTON_RINGS" or (st == "POA_SIGNATURE" and sig == "FIXED_NEGATIVE"):
        return st, sig, "MW-001", 0.88
    if st == "POA_SIGNATURE":
        if sig == "DIVERGENT":
            return st, sig, "MW-008", 0.90
        if sig == "DFCO_NEGATIVE":
            return st, sig, "MW-009", 0.91
    return st, sig, "NO-MATCH", 0.0


def demand_score(case, state, sig):
    score = 1.0
    reasons = ["gas chemistry"]
    if state == "POA_SIGNATURE":
        score += 1.0
        reasons.append("ambiguous POA family (needs post-cat to split)")
    if sig in ("FIXED_NEGATIVE", "TRANSIENT_NEGATIVE"):
        score += 1.0
        reasons.append("requires post-cat B1S2 trim")
    if sig == "DIVERGENT":
        score += 2.0
        reasons.append("requires SIMULTANEOUS upstream(+) & downstream(-) split")
    if sig == "DFCO_NEGATIVE":
        score += 2.0
        reasons.append("requires DFCO (fuel-cut) transient capture, decoupled from combustion")
    if case.expect == "MW-001":
        score += 1.5
        reasons.append("historic cross-lab conflict (low-idle HC vs rule threshold)")
    return round(score, 1), reasons


# --------------------------------------------------------------- OTLP tracing
def make_tracer():
    """Return (tracer, provider) if OTEL_TRACES_EXPORTER is set and SDK present, else (None, None)."""
    if not os.environ.get("OTEL_TRACES_EXPORTER"):
        return None, None
    try:
        from opentelemetry import trace
        from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
        from opentelemetry.sdk.resources import Resource
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor
    except ImportError:
        print("[trace] opentelemetry SDK not installed — running without traces.\n"
              "         pip install opentelemetry-sdk opentelemetry-exporter-otlp-proto-grpc")
        return None, None
    endpoint = os.environ.get("OTEL_EXPORTER_OTLP_ENDPOINT", "http://localhost:4317")
    service = os.environ.get("OTEL_SERVICE_NAME", "wiredv2-oil-case")
    provider = TracerProvider(resource=Resource.create({
        "service.name": service, "service.namespace": "4dlab",
        "deployment.environment": "local-sim"}))
    provider.add_span_processor(BatchSpanProcessor(OTLPSpanExporter(endpoint=endpoint, insecure=True)))
    trace.set_tracer_provider(provider)
    print(f"[trace] exporting to {endpoint} as service '{service}' — open http://localhost:16686")
    return trace.get_tracer("wiredv2.sim"), provider


def emit_trace(tracer, c, st, sig, fault, conf, dem):
    """Emit one trace per case: oil_case_<id> -> gas_state -> post_cat_trim -> verdict."""
    with tracer.start_as_current_span(f"oil_case_{c.slug}") as root:
        root.set_attribute("case.id", c.slug)
        root.set_attribute("case.vin", ENGINE["vin"])
        root.set_attribute("case.engine_code", ENGINE["engine_code"])
        root.set_attribute("case.expected_fault_code", c.expect)
        root.set_attribute("case.predicted_fault_code", fault)
        root.set_attribute("case.match_status", "PASS" if fault == c.expect else "MISMATCH")
        root.set_attribute("case.demand_score", dem)
        time.sleep(0.02)
        with tracer.start_as_current_span("gas_state") as g:
            g.set_attribute("gas.hc_low_ppm", c.gas_low["hc"])
            g.set_attribute("gas.hc_high_ppm", c.gas_high["hc"])
            g.set_attribute("gas.lambda_low", c.gas_low["lam"])
            g.set_attribute("gas.lambda_high", c.gas_high["lam"])
            g.set_attribute("gas.chemical_state", st)
            time.sleep(0.02)
        with tracer.start_as_current_span("post_cat_trim") as p:
            p.set_attribute("obd.upstream_o2", ENGINE["upstream_o2"])
            p.set_attribute("obd.downstream_o2", ENGINE["downstream_o2"])
            p.set_attribute("obd.stft_b1s2_pct", c.obd["stft_b1s2"])
            p.set_attribute("obd.ltft_b1s2_pct", c.obd["ltft_b1s2"])
            p.set_attribute("obd.dfco_b1s2_pct", c.obd["dfco_b1s2"])
            p.set_attribute("obd.downstream_volt", c.obd["dn_v"])
            p.set_attribute("obd.post_cat_signature", sig)
            time.sleep(0.02)
        with tracer.start_as_current_span("verdict") as v:
            v.set_attribute("fault.code", fault)
            v.set_attribute("fault.family", "mechanical_wear")
            v.set_attribute("fault.name", FAULT_NAMES.get(fault, ""))
            v.set_attribute("fault.confidence", conf)
            time.sleep(0.02)


def run(tracer=None):
    rows = []
    for c in CASES:
        st, sig, fault, conf = diagnose(c)
        ok = (fault == c.expect)
        dem, reasons = demand_score(c, st, sig)
        if tracer is not None:
            emit_trace(tracer, c, st, sig, fault, conf, dem)
        rows.append({"case": c.name, "slug": c.slug, "expect": c.expect, "gas_state": st,
                     "b1s2_signature": sig, "verdict": fault,
                     "fault_name": FAULT_NAMES.get(fault, ""), "confidence": conf,
                     "pass": ok, "demand_score": dem, "demand_reasons": reasons,
                     "upstream_lambda_low": c.gas_low["lam"], "upstream_lambda_high": c.gas_high["lam"],
                     "downstream_v": c.obd["dn_v"], "stft_b1s2": c.obd["stft_b1s2"],
                     "ltft_b1s2": c.obd["ltft_b1s2"], "dfco_b1s2": c.obd["dfco_b1s2"]})
    return rows


def main():
    tracer, provider = make_tracer()
    rows = run(tracer)
    print("=" * 80)
    print(f" OIL-BURN DIAGNOSTIC SIMULATION  —  {ENGINE['make']} {ENGINE['engine_code']} "
          f"({ENGINE['displacement_l']}L {ENGINE['induction']} {ENGINE['fuel']}, {ENGINE['euro']})")
    print(f" VIN {ENGINE['vin']}   upstream={ENGINE['upstream_o2']} (lambda)  "
          f"downstream={ENGINE['downstream_o2']} (volt+B1S2)")
    print("=" * 80)
    hdr = f"{'Case':<28}{'GAS state':<22}{'B1S2 sig':<18}{'Verdict':<8}{'OK':<6}{'Demand'}"
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        print(f"{r['case']:<28}{r['gas_state']:<22}{r['b1s2_signature']:<18}"
              f"{r['verdict']:<8}{('PASS' if r['pass'] else 'FAIL'):<6}{r['demand_score']}")
    print("-" * len(hdr))
    npass = sum(r["pass"] for r in rows)
    print(f"RESULT: {npass}/{len(rows)} routed to expected fault "
          f"({'ALL GREEN' if npass == len(rows) else 'CHECK'})\n")
    print("DEMAND RANKING (most demanding first):")
    for r in sorted(rows, key=lambda x: -x["demand_score"]):
        print(f"  [{r['demand_score']:>4}] {r['case']:<28} {r['verdict']}  "
              f"<- {', '.join(r['demand_reasons'][1:]) or 'gas only'}")

    if "--json" in sys.argv:
        out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "oil_burn_5fr_results.json")
        with open(out, "w") as fh:
            json.dump({"engine": ENGINE, "results": rows}, fh, indent=2)
        print(f"\n[json] wrote {out}")

    if provider is not None:
        provider.shutdown()   # flush batched spans before exit
        print("[trace] spans flushed to Jaeger.")
    print("\n[SIMULATION] post-cat B1S2 trim is mocked; tasks PCT-1..PCT-10 implement it for real.")


if __name__ == "__main__":
    main()
