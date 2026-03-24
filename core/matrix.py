"""Diagnostic matrix matching using custom safe expression evaluator with confidence scoring."""

from typing import Dict, Any, List
import re


_SAFE_BUILTINS = {'abs': abs, 'min': min, 'max': max, 'round': round}


def _safe_eval(expr: str, context: dict) -> bool:
    expr = expr.replace('&&', ' and ').replace('||', ' or ')
    expr = re.sub(r'([a-zA-Z_]\w*)\.(\w+)', r"\1['\2']", expr)
    try:
        code = compile(expr, '<logic>', 'eval')
    except SyntaxError:
        return False
    for name in code.co_names:
        if name not in context and name not in _SAFE_BUILTINS:
            return False
    try:
        eval_globals = {"__builtins__": {}}
        eval_globals.update(_SAFE_BUILTINS)
        return bool(eval(code, eval_globals, context))
    except Exception:
        return False


def _evaluate_pid_condition(condition: str, value: float) -> bool:
    cond = condition.strip().replace('%', '')
    m = re.match(r'([><=]+)\s*([-+]?\d*\.?\d+)', cond)
    if not m:
        return False
    op, threshold = m.groups()
    threshold = float(threshold)
    try:
        if op == '>':
            return value > threshold
        elif op == '>=':
            return value >= threshold
        elif op == '<':
            return value < threshold
        elif op == '<=':
            return value <= threshold
        elif op == '==':
            return abs(value - threshold) < 0.001
        return False
    except:
        return False


def match_case(
    low_idle: Dict[str, float],
    calculated_lambda: float,
    measured_lambda: float,
    knowledge_base: Dict[str, Any],
    high_idle: Dict[str, float] = None,
    dtc_codes: List[str] = None,
    freeze_frame: Dict[str, float] = None,
    tier4_low: Dict[str, float] = None,
    tier4_high: Dict[str, float] = None
) -> Dict[str, Any]:
    matrix = knowledge_base.get('diagnostic_matrix', [])

    if high_idle is None:
        high_idle_ctx = {
            'co': low_idle.get('co', 0),
            'co2': low_idle.get('co2', 0),
            'hc': low_idle.get('hc', 0),
            'o2': low_idle.get('o2', 0),
            'lambda': low_idle.get('lambda', 1.0),
            'nox': low_idle.get('nox', 0),
        }
    else:
        high_idle_ctx = high_idle

    base_context = {
        'low_idle': low_idle,
        'calculated_lambda': calculated_lambda,
        'measured_lambda': measured_lambda,
        'high_idle': high_idle_ctx,
        'dtc_codes': dtc_codes or [],
        'freeze_frame': freeze_frame or {},
        'tier4_low': tier4_low or {},
        'tier4_high': tier4_high or {}
    }

    best_case = None
    best_confidence = -1.0

    for case in matrix:
        logic_str = case.get('base_logic') or case.get('logic', '')
        if not logic_str:
            continue
        try:
            matches_base = _safe_eval(logic_str, base_context)
        except Exception:
            continue
        if not matches_base:
            continue

        confidence = case.get('confidence_boosters', {}).get('base_confidence', 0.7)

        # Tier 2: OBD DTC Boost
        if dtc_codes and 'modular_addons' in case:
            addons = case['modular_addons']
            if 'tier2_obd_dtc' in addons:
                matching = set(dtc_codes) & set(addons['tier2_obd_dtc'])
                if matching:
                    weight = case.get('confidence_boosters', {}).get('dtc_match_weight', 0.2)
                    confidence += weight

        # Tier 3: Live PID Boost - evaluate any condition in modular_addons.tier3_pids
        if tier4_low and 'modular_addons' in case:
            addons = case['modular_addons']
            if 'tier3_pids' in addons:
                pids_cfg = addons['tier3_pids']
                for key, condition in pids_cfg.items():
                    # Resolve value: try key directly, then common alternatives
                    value = tier4_low.get(key)
                    if value is None:
                        if key == 'lambda':
                            value = tier4_low.get('44') or tier4_low.get('lambda')
                        elif key == 'downstream_lambda':
                            value = tier4_low.get('downstream_lambda')
                        # add more aliases as needed
                    if value is not None and _evaluate_pid_condition(condition, value):
                        weight = case.get('confidence_boosters', {}).get('trim_match_weight', 0.1)
                        confidence += weight

        confidence = min(confidence, 1.0)

        if confidence > best_confidence:
            best_confidence = confidence
            best_case = case.copy()
            best_case['confidence_score'] = confidence

    if best_case:
        return best_case

    return {
        "case_id": "FALLBACK_001",
        "name": "Unclassified Condition",
        "verdict": "No matching diagnostic pattern found.",
        "action": "Perform manual inspection or gather additional data.",
        "health_score": 50,
        "confidence_score": 0.0
    }
