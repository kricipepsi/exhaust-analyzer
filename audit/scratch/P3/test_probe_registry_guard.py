"""P3 probe: the wired REG-V2 activation guard has no caller and no test; drive it on the shipped registry.

Claim (apps/wired/WIRED_PROGRESS.md:58): "`registry_guard.py` must expect 73 rules (not 68) or harness raises
`RegistryActivationError`". Run (repo root): python -m pytest -q -p no:cacheprovider audit/scratch/P3/test_probe_registry_guard.py -s
"""
import subprocess

from wired.registry_guard import _count_rules, _DEFAULT_RULES_DIR, _EXPECTED_RULE_COUNT, assert_registry_ready


def test_guard_on_shipped_registry():
    n = _count_rules(_DEFAULT_RULES_DIR)
    print(f"shipped rules={n} expected={_EXPECTED_RULE_COUNT}")
    try:
        assert_registry_ready()
        print("assert_registry_ready: passes")
    except Exception as ex:  # noqa: BLE001
        print("assert_registry_ready raises:", type(ex).__name__, ex)


def test_guard_has_no_caller():
    out = subprocess.run(["git", "grep", "-n", "assert_registry_ready", "--", "*.py"], capture_output=True,
                         text=True).stdout.splitlines()
    callers = [l for l in out if "def assert_registry_ready" not in l and "__all__" not in l
               and "audit/scratch" not in l]
    print("callers:", callers)
    assert callers == []
