"""MAF linearity and theoretical airflow calculation helper.

Source: research/chunks/pids-protocol/05_maf-linearity-theoretical-airflow.md.
"""

# constants per the numeric-literal rule
R: float = 0.287  # wiki: research/chunks/pids-protocol/05
CONSTANT_120: float = 120.0  # wiki: research/chunks/pids-protocol/05
K_OFFSET: float = 273.15  # wiki: research/chunks/pids-protocol/05
PERCENT_MULT: float = 100.0  # wiki: research/chunks/pids-protocol/05


def calculate_w_theo(
    eta_v: float,
    displacement: float,
    map_kpa: float,
    rpm: float,
    iat_c: float,
) -> float:
    """Compute W_theo = (eta_v * V_disp * P_manifold * RPM) / (120 * R * T_intake).

    All values are standard float inputs. Returns theoretical airflow in g/s.
    """
    t_intake_k = iat_c + K_OFFSET  # wiki: research/chunks/pids-protocol/05
    numerator = eta_v * displacement * map_kpa * rpm  # wiki: research/chunks/pids-protocol/05
    denominator = CONSTANT_120 * R * t_intake_k  # wiki: research/chunks/pids-protocol/05
    if denominator == 0.0:  # wiki: research/chunks/pids-protocol/05
        return 0.0
    return numerator / denominator


def calculate_sensor_error_delta(
    maf_stress: float,
    w_theo_stress: float,
    maf_idle: float,
    w_theo_idle: float,
) -> float:
    """Compute the two-point non-linearity delta in percentage deviation.

    Formula: ΔSensor_error = |Sensor_Stress - W_theo_Stress|/W_theo_Stress - |Sensor_Idle - W_theo_Idle|/W_theo_Idle
    """
    if w_theo_stress == 0.0:  # wiki: research/chunks/pids-protocol/05
        err_stress = 0.0
    else:
        err_stress = abs(maf_stress - w_theo_stress) / w_theo_stress  # wiki: research/chunks/pids-protocol/05

    if w_theo_idle == 0.0:  # wiki: research/chunks/pids-protocol/05
        err_idle = 0.0
    else:
        err_idle = abs(maf_idle - w_theo_idle) / w_theo_idle  # wiki: research/chunks/pids-protocol/05

    return (err_stress - err_idle) * PERCENT_MULT  # wiki: research/chunks/pids-protocol/05
