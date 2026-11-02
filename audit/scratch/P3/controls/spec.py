"""Suite spec for the planted controls (same shape as reachability.SUITES etc.)."""
_S = "audit/scratch/P3/controls/suite"
SUITES = {"ctl": (_S, [_S + "/p3ctl"])}
PROD_ROOTS = {"p3ctl": _S + "/p3ctl"}
NAMED = [(_S + "/p3ctl/core.py", "verdict")]
VERDICT = [_S + "/p3ctl/core.py"]
EXPECT_CLASS = {
    "test_clean_behaviour_value": "behaviour", "test_clean_behaviour_control_dependent": "behaviour",
    "test_planted_interface_shape": "interface", "test_planted_placeholder_constant": "placeholder",
    "test_planted_placeholder_double": "placeholder", "test_planted_placeholder_early_return": "placeholder",
    "test_planted_misnamed_verdict_is_high": "interface",
}
