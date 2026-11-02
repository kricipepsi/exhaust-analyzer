"""P3 probe: drive the C3 (CONTROL_REFERENCE_FAULT) branch of _score_rule that no suite takes.

Claim (v3/v3_tasks/T-V3-P4-C3B_c3_signal_commit.md:32-33): "On the state: boost EF-001/EF-002/EF-003
(+0.10 DEFINITIVE), prune SF-001/SF-002."
Run: cd labs/comlab && python -m pytest -q -p no:cacheprovider ../../audit/scratch/P3/test_probe_score_rule_c3.py -s
"""
from registry.integration_shim import RegistryV2Router, _Observation, _score_rule

ROUTER = RegistryV2Router()
RULES = {r.rule_id: r for r in ROUTER.rules}
C3 = {"koeo_map_baro_delta_kpa": 6.0}  # >= 5.0 -> rich-bias reference fault (integration_shim.py:607)


def _pair(rid):
    quiet = _score_rule(RULES[rid], _Observation(obd_pids={}))
    c3 = _score_rule(RULES[rid], _Observation(obd_pids=dict(C3)))
    print(f"{rid}: quiet={quiet} c3={c3} base_weight={RULES[rid].base_weight}")
    return quiet, c3


def test_c3_prunes_sf001_sf002():
    for rid in ("SF-001", "SF-002"):
        _, c3 = _pair(rid)
        assert c3 is None


def test_c3_boosts_ef_rules():
    for rid in ("EF-001", "EF-002", "EF-003"):
        quiet, c3 = _pair(rid)
        base = quiet if quiet is not None else RULES[rid].base_weight
        assert c3 == min(base + 0.10, 1.0)


def test_c3_route_case_end_to_end():
    out = ROUTER.route_case({"obd_live_data": dict(C3)})
    print("route_case(C3 only):", {k: out[k] for k in sorted(out) if k in ("rule_id", "fault_family", "score",
                                                                       "confidence", "verdict")} or out)
