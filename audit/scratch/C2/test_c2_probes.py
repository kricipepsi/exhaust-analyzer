"""C2 falsification probes for labs/gaslab. Each test asserts the CLAIM; a failure is a finding.

Run from the repo root:
    PYTHONDONTWRITEBYTECODE=1 python -m pytest -p no:cacheprovider -q audit/scratch/C2/test_c2_probes.py
Audit scratch only — changes no source.
"""

from __future__ import annotations

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _c2 import IDLE, ONT, GasLabContext, R, dna, lam, process, run  # noqa: E402
from gaslab.audits import _is_catch_all, _signatures_overlap, find_uncovered_overlaps  # noqa: E402
from gaslab.resolution import apply_differentiators  # noqa: E402
from gaslab.rule_engine import _matching_fault_candidates, _specificity  # noqa: E402


# ---------------------------------------------------------------- F1
def test_f1_non_exhaust_sample_must_not_get_a_fault_verdict():
    """GASWIKI-04 §4.1/§4.2 + vocab §5: sum < 14 -> INVALID; CO+CO2 <= 6 -> heavy dilution."""
    r = R(0, 0.1, 0.0, 2.1, 0)  # CO2 0 %: no combustion product at all; sum 2.2 %
    p = process(r, GasLabContext(dna=dna(), engine_state=IDLE))
    obs = (p.chemical_state.value, p.sample_validity.value, round(p.lambda_chem, 3))
    assert obs[:2] == ("SAMPLE_INVALID", "INVALID"), f"observed {obs}"


# ---------------------------------------------------------------- F2
def test_f2_vr_rupture_reachable_for_real_fuel_delivery_types():
    """GASWIKI-06A §7.19 / vocab §3.1: VACUUM_REGULATOR_DIAPHRAGM_RUPTURE dna_gate none (FPR universal)."""
    r = R(1500, 5.0, 10.5, 0.1, 10)  # inside the VR signature, triangle-valid
    out = {f: run(r, dna(fuel_delivery_type=f))[0] for f in ("PORT_INJECTION", "CARBURETOR", "NON_GDI")}
    assert out["PORT_INJECTION"] == "VACUUM_REGULATOR_DIAPHRAGM_RUPTURE", f"observed {out}"


# ---------------------------------------------------------------- F3
def test_f3_rpm_confirmed_cam_advanced_not_preempted_by_collision():
    """GASWIKI-04 §4.10: cam-timing rule priority 82 sits ABOVE collision (80)."""
    idle = R(450, 0.7, 11.5, 2.3, 25)   # inside GASWIKI-06B CAM_TIMING_ADVANCED idle vector
    hi = R(200, 0.3, 13.0, 1.2, 600)    # inside its 2500 RPM vector (NOx rises)
    obs = (run(idle, dna(), reading_high=hi), lam(idle))
    assert obs[0][0] == "CAM_TIMING_ADVANCED", f"observed {obs}"


# ---------------------------------------------------------------- F4
def test_f4_healthy_idle_is_not_ignition_retard():
    """GASWIKI-05 FAULT_TIMING_RETARDED idle vector: HC 300-800, NOx 0-5, lambda 1.05-1.15."""
    r = R(10, 0.12, 15.2, 0.30, 20)  # every gas inside the NORMAL bands; lambda 1.014
    obs = (run(r, dna()), lam(r))
    assert obs[0][0] != "TIMING_RETARDED", f"observed {obs}"


def test_f4b_wiki_timing_retarded_vector_emits_timing_retarded():
    r = R(500, 0.10, 10.9, 3.4, 3)  # GASWIKI-05 TIMING_RETARDED idle vector, triangle-valid
    obs = (run(r, dna()), lam(r))
    assert obs[0][0] == "TIMING_RETARDED", f"observed {obs}"


# ---------------------------------------------------------------- F5
def test_f5_2500_confirmation_keeps_worn_valve_seals():
    """GASWIKI-06A §6A.1 + GASWIKI-08 §8.9: HC drops sharply at 2500 => WORN_VALVE_SEALS."""
    idle = R(150, 0.3, 14.0, 0.4, 50)
    hi = R(20, 0.10, 15.0, 0.0, 60)
    obs = (run(idle, dna()), run(idle, dna(), reading_high=hi))
    assert obs[1][0] == "WORN_VALVE_SEALS", f"observed idle-only/with-2500 {obs}"


def test_f5b_wiki_idle_band_routes_to_worn_valve_seals():
    rng = random.Random(3)
    hi = R(20, 0.10, 15.0, 0.0, 60)
    hits, n = {}, 0
    for _ in range(200000):
        hc = rng.randint(300, 500)
        idle = R(hc, round(rng.uniform(0, 1), 2), round(rng.uniform(12, 16), 2),
                 round(rng.uniform(0, 1.0), 2), rng.randint(0, 100))
        if not 14 <= idle.co + idle.co2 + idle.o2 <= 16:
            continue
        n += 1
        if run(idle, dna(), reading_high=hi)[0] == "WORN_VALVE_SEALS":
            hits[hc] = hits.get(hc, 0) + 1
    assert set(hits) - {500}, f"valid idle samples={n}; WORN_VALVE_SEALS hits by idle HC={hits}"


# ---------------------------------------------------------------- F6
def test_f6_flat_rich_rejected_on_rule_engine_path():
    """GASWIKI-04 §4.10 rich branch: 'signature PARTIALLY normalises toward 2500 RPM'."""
    idle = R(400, 3.5, 11.0, 0.5, 5)
    hi = R(200, 3.6, 11.0, 0.1, 150)  # lambda flat, CO rises
    keeps = "CAM_TIMING_RETARDED_MAP" in apply_differentiators(
        ["CAM_TIMING_RETARDED_MAP"], idle, dna(), ONT, IDLE, reading_high=hi)
    obs = (lam(idle), lam(hi), run(idle, dna(), reading_high=hi), f"resolution.py keeps={keeps}")
    assert obs[2][0] != "CAM_TIMING_RETARDED_MAP", f"observed {obs}"


# ---------------------------------------------------------------- F7
def test_f7_coc_override_only_at_high_confidence():
    """vocab §10 preamble + §11 + GASWIKI-02 §2.8: per-vehicle bounds override only when confidence = HIGH."""
    r = R(30, 0.3, 15.0, 0.2, 40)
    obs = {c: run(r, dna(confidence=c, co_low_idle=0.45))[0] for c in ("NONE", "LOW", "HIGH")}
    obs["NONE/no-CoC"] = run(r, dna(confidence="NONE"))[0]
    assert obs["NONE"] == obs["NONE/no-CoC"], f"observed {obs}"


# ---------------------------------------------------------------- F8
def test_f8_collision_keeps_valid_triangle_valid():
    """GASWIKI-04 §4.1 + vocab §5: sum 14-16 => VALID."""
    r = R(400, 1.0, 11.5, 2.5, 30)  # sum 15.0
    obs = (run(r, dna()), lam(r))
    assert obs[0][1] == "VALID", f"observed {obs}"


# ---------------------------------------------------------------- F9
def test_f9_collision_tier_max_scales_with_dna():
    """vocab §10.2: collision tier_max is the active DNA-scaled tier; Euro 1 no-cat = 1.5 %."""
    r = R(150, 1.2, 11.5, 2.4, 40)
    obs = (run(r, dna(euro_emission_category="EURO_1", has_catalyst=False)), lam(r))
    assert obs[0][0] != "RICH_MISFIRE", f"observed {obs}"


# ---------------------------------------------------------------- F10
def test_f10_wideband_o2_bias_low_box_is_satisfiable():
    """rule_engine._calibrate_o2_bias_low_bounds replaces CO/lambda but keeps CO2 13-16 => CO+CO2 >= 18."""
    wb = dna(upstream_o2_type="WIDEBAND_LAMBDA")
    realistic = R(80, 6.0, 9.5, 0.1, 20)  # GASWIKI-04 §4.12: lambda 0.77-0.85, CO 5-8 %, sum 15.6
    corner = R(100, 5.0, 13.0, 0.0, 0)
    obs = (lam(realistic), run(realistic, wb), lam(corner), run(corner, wb))
    assert obs[1][0] == "O2_SENSOR_BIASED_LOW", f"observed {obs}"


# ---------------------------------------------------------------- F11
def test_f11_carbon_above_stoich_ceiling_not_diagnosed():
    """GASWIKI-03 §CO2: ~15.5 % ceiling; GASWIKI-04 §4.1: sum > 16 only via air dilution."""
    obs = {}
    for r in (R(20, 0.2, 17.5, 0.1, 50), R(200, 6.0, 11.5, 0.1, 10)):
        p = process(r, GasLabContext(dna=dna(), engine_state=IDLE))
        obs[str(r)] = (p.chemical_state.value, p.sample_validity.value)
    assert all(v[1] == "INVALID" for v in obs.values()), f"observed {obs}"


# ---------------------------------------------------------------- F12
def test_f12_masking_rule_unconditional_for_small_engines():
    """GASWIKI-04 §4.8: HC>1000 AND O2>3.0 AND NOx<50 => IGNITION_MISFIRE (override)."""
    r = R(1500, 0.2, 10.6, 3.3, 20)
    obs = {c: run(r, dna(cylinder_count=c))[0] for c in (2, 3, 4)}
    assert set(obs.values()) == {"IGNITION_MISFIRE"}, f"observed {obs}"


# ---------------------------------------------------------------- F13
def test_f13_collision_audit_does_not_count_informational_edges():
    """audits.find_uncovered_overlaps docstring: uncovered = overlap with no resolution path;
    resolution.apply_differentiators: physical_check edges never filter."""
    F = ONT["faults"]

    def filtering(e):
        if e.get("dna_gate"):
            return True
        for ed in e.get("differentiator_edges") or []:
            if ed.get("type") == "dna":
                return True
            if ed.get("type") == "rpm_differential" and (ed.get("appears_in_states") or ed.get("route_when_matched")):
                return True
        return False

    names = sorted(n for n in F if n != "SAMPLE_INVALID" and not _is_catch_all(F[n]))
    strict = {(a, b) for i, a in enumerate(names) for b in names[i + 1:]
              if not filtering(F[a]) and not filtering(F[b]) and _signatures_overlap(F[a]["signature"], F[b]["signature"])}
    hidden = strict - set(find_uncovered_overlaps(ONT))
    near = {p: round(min(_specificity(p[0], F), _specificity(p[1], F)) / max(_specificity(p[0], F), _specificity(p[1], F)), 3)
            for p in hidden}
    assert not hidden, f"hidden pairs (specificity ratio): {near}"


# ---------------------------------------------------------------- F14
def test_f14_lambda_code_matches_printed_formula():
    """GASWIKI-02 §2.3 / vocab §6 'formal definition' (Hcv = 1.85)."""
    r = R(20, 0.2, 15.0, 0.2, 50)
    hcv = 1.85
    literal = (r.co2 + r.co / 2 + r.o2 + (hcv / 4 * r.co2 / (r.co2 + r.co)) * r.co2) / (r.co2 + r.co + r.hc * 0.0025)
    obs = (lam(r), round(literal, 4))
    assert abs(obs[0] - obs[1]) < 0.01, f"observed code/printed-formula {obs}"
