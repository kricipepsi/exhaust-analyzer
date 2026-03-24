"""Report generation and final verdict assembly."""

from typing import Dict, Any


def _safe_eval_condition(condition: str, context: dict) -> bool:
    """Evaluate a penalty condition string safely."""
    try:
        code = compile(condition, '<penalty>', 'eval')
        for name in code.co_names:
            if name not in context:
                return False
        return bool(eval(code, {"__builtins__": {}}, context))
    except Exception:
        return False


def generate_report(
    low_idle: Dict[str, float],
    measured_lambda: float,
    calculated_lambda: float,
    cat_eff: int,
    cat_status: str,
    matched_case: Dict[str, Any],
    knowledge_base: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Combine all diagnostic data into final verdict.

    Args:
        low_idle: gas readings at low idle
        measured_lambda: wideband O2 lambda reading
        calculated_lambda: lambda from Bretschneider formula
        cat_eff: catalyst efficiency (0-100)
        cat_status: catalyst status string
        matched_case: case dict from matrix matching
        knowledge_base: full knowledge base (for potential future use)

    Returns:
        dict with final assessment keys:
        - overall_health: int (clamped 0-100)
        - assessment: case name
        - verdict: case verdict text
        - action: recommended action
        - calc_lambda: calculated lambda
        - lambda_delta: abs(measured - calculated)
        - cat_efficiency: catalyst efficiency
        - cat_status: catalyst status
        - case_id: matched case identifier
    """
    base_health = matched_case.get('health_score', 50)

    lambda_delta = abs(measured_lambda - calculated_lambda)

    # Apply penalties
    health = base_health
    nox_warning = None
    nox_value = low_idle.get('nox', 0)

    penalties = knowledge_base.get('health_penalties', None)
    if penalties is not None:
        # Data-driven penalty evaluation
        eval_context = {
            'lambda_delta': lambda_delta,
            'cat_eff': cat_eff,
            'nox': nox_value,
            'lambda_val': low_idle.get('lambda', 1.0),
        }
        nox_warning_set = False
        for rule in penalties:
            condition = rule.get('condition', '')
            if _safe_eval_condition(condition, eval_context):
                health -= rule.get('penalty', 0)
                warning = rule.get('warning')
                if warning and not nox_warning_set:
                    nox_warning = warning.format(nox=nox_value)
                    nox_warning_set = True
    else:
        # Fallback: hardcoded logic
        if lambda_delta > 0.05:
            health -= 10
        if cat_eff < 80:
            health -= 15
        if nox_value > 1500:
            health -= 15
            nox_warning = f"Severe NOx ({nox_value} ppm) - possible cooling system, EGR, or catalyst failure"
        elif nox_value > 500 and low_idle.get('lambda', 1.0) > 1.03:
            health -= 10
            nox_warning = f"Elevated NOx ({nox_value} ppm) with lean mixture - check EGR and cooling system"

    # Clamp health 0-100
    health = max(0, min(100, health))

    return {
        'overall_health': health,
        'assessment': matched_case.get('name', 'Unknown'),
        'verdict': matched_case.get('verdict', ''),
        'action': matched_case.get('action', ''),
        'calc_lambda': calculated_lambda,
        'lambda_delta': round(lambda_delta, 3),
        'cat_efficiency': cat_eff,
        'cat_status': cat_status,
        'case_id': matched_case.get('case_id', 'UNKNOWN'),
        'nox_warning': nox_warning
    }
