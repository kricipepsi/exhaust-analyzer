"""OBDLab canonical vocabulary — 7 StrEnums from OBDLab_KG_Wiki.md §6.

All values are the wire-format strings consumed across lab boundaries per
SEMANTIC_CONTRACT.md §4.4. Renames are breaking changes.
"""

from enum import StrEnum
from typing import Any


class RpmStateBucket(StrEnum):
    """Engine RPM state bucket per OBDLab_KG_Wiki.md §6.1 / §8.

    Source: OBDLab_KG_Wiki.md §6.1, OBD_VOCABULARY.md §3.
    """
    STABILIZED_IDLE         = "STABILIZED_IDLE"         # wiki: §6.1 — 650–900 RPM, load <30%
    REGULATORY_HIGH_IDLE    = "REGULATORY_HIGH_IDLE"    # wiki: §6.1 — 2200–2800 RPM, 2-speed idle test
    STRESS_IDLE             = "STRESS_IDLE"             # wiki: §6.1 — VIN-derived 3000–4500 RPM, clinical no-load
    COLD_OPEN_LOOP_INVALID  = "COLD_OPEN_LOOP_INVALID"  # wiki: §6.1 / §4.1 — ECT < 75°C, freeze all analytics




class O2NormalizationMode(StrEnum):
    """O2 sensor normalisation strategy per OBDLab_KG_Wiki.md §6.3 / §11.

    Source: OBDLab_KG_Wiki.md §6.3.
    Driven by VinDNA.upstream_o2_type.
    """
    NARROWBAND_VOLTAGE_TO_LAMBDA       = "NARROWBAND_VOLTAGE_TO_LAMBDA"       # wiki: §6.3 — 0.1–0.9 V → lambda mapping §11.1
    WIDEBAND_PASSTHROUGH               = "WIDEBAND_PASSTHROUGH"                # wiki: §6.3 — direct lambda/AFR value §11.2
    WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA  = "WIDEBAND_NB_SIM_VOLTAGE_TO_LAMBDA"  # wiki: §6.3 — WB sensor, NB sim output → 3-zone mapping §11.3
    O2_CHANNEL_FAULT                   = "O2_CHANNEL_FAULT"                   # wiki: §11 — out-of-range input; clamped lambda, payload flagged


class VEValidity(StrEnum):
    """VE cross-check validity per OBDLab_KG_Wiki.md §6.4 / §10.3.

    Source: OBDLab_KG_Wiki.md §6.4.
    """
    VALID                    = "VALID"                    # wiki: §6.4 — VE within expected range
    FAULT_VE_IDLE_COLLAPSE   = "FAULT_VE_IDLE_COLLAPSE"   # wiki: §6.4 — VE < 50% at STABILIZED_IDLE
    FAULT_MAF_CONTAMINATION  = "FAULT_MAF_CONTAMINATION"  # wiki: §6.4 — VE < 65% at STRESS_IDLE + positive TFT
    FAULT_VE_SENSOR_SKEW     = "FAULT_VE_SENSOR_SKEW"     # wiki: §6.4 — VE > 90% at idle on NA engine
    UNKNOWN                  = "UNKNOWN"                  # wiki: §6.4 — insufficient inputs to compute


class TrimAnalyticsGate(StrEnum):
    """Analytics precondition gate per OBDLab_KG_Wiki.md §6.5 / §9.

    Source: OBDLab_KG_Wiki.md §6.5.
    """
    VALID                   = "VALID"                   # wiki: §6.5 — all preconditions satisfied
    ENGINE_COLD             = "ENGINE_COLD"             # wiki: §6.5 — coolant_temp_c < 70
    OPEN_LOOP               = "OPEN_LOOP"               # wiki: §6.5 — fuel_sys_status != Closed_Loop
    O2_FAULT_ACTIVE         = "O2_FAULT_ACTIVE"         # wiki: §6.5 — active P0130–P0161
    CKP_CMP_FAULT_ACTIVE    = "CKP_CMP_FAULT_ACTIVE"    # wiki: §6.5 — active P0335 / P0340
    CODES_RECENTLY_CLEARED  = "CODES_RECENTLY_CLEARED"  # wiki: §6.5 — < 1 drive cycle since codes_cleared
    WOT_ACTIVE              = "WOT_ACTIVE"              # wiki: §6.5 — throttle at wide-open
    DFCO_ACTIVE             = "DFCO_ACTIVE"             # wiki: §6.5 — decel fuel cut-off
    SEMANTIC_ERROR          = "SEMANTIC_ERROR"          # wiki: §6.5 — Physics Gate violation (§4)


class NodeMAFStatus(StrEnum):
    """MAF sensor data provenance per OBDLab_KG_Wiki.md §6.6.

    Source: OBDLab_KG_Wiki.md §6.6.
    """
    REAL_SENSOR_FEED   = "REAL_SENSOR_FEED"    # wiki: §6.6 — MAF sensor physically present and reading
    VIRTUAL_EMULATION  = "VIRTUAL_EMULATION"   # wiki: §6.6 — MAP_ONLY route, MAF value is computed


class NodeMAPStatus(StrEnum):
    """MAP sensor data provenance per OBDLab_KG_Wiki.md §6.6.

    Source: OBDLab_KG_Wiki.md §6.6.
    """
    REAL_SENSOR_FEED   = "REAL_SENSOR_FEED"    # wiki: §6.6 — MAP sensor physically present and reading
    BACK_CALCULATED    = "BACK_CALCULATED"     # wiki: §6.6 — MAF_ONLY route, MAP value is inferred


class FuelSystemStatus(StrEnum):
    """Fuel system loop status mirror per DTC_VOCABULARY.md §8.

    No cross-lab import — per the boundary rule, OBDLab owns its copy.
    Sourced verbatim from DTC_VOCABULARY.md §8.
    """
    CL = "CL"  # wiki: §8 — closed loop; O₂ feedback active
    OL = "OL"  # wiki: §8 — open loop; base map (cold start)
    OL_DRIVE = "OL_DRIVE"  # wiki: §8 — open loop driving (WOT, decel)
    OL_FAULT = "OL_FAULT"  # wiki: §8 — open loop due to O₂ sensor fault

    @classmethod
    def from_wire(cls, value: Any) -> "FuelSystemStatus | None":
        """Coerce raw wire-format string or enum to FuelSystemStatus enum."""
        if isinstance(value, cls):
            return value
        if isinstance(value, str):
            mapping = {
                "Closed_Loop": cls.CL,
                "Open_Loop_Cold": cls.OL,
                "Open_Loop_Fault": cls.OL_FAULT,
                "Open_Loop_Driving": cls.OL_DRIVE,
                "CL": cls.CL,
                "OL": cls.OL,
                "OL_DRIVE": cls.OL_DRIVE,
                "OL_FAULT": cls.OL_FAULT,
            }
            return mapping.get(value)
        return None


class O2FailureMode(StrEnum):
    """O2 sensor failure taxonomy per OBDLab_KG_Wiki.md §6.7.

    Source: OBDLab_KG_Wiki.md §6.7.
    """
    NO_FAULT            = "NO_FAULT"            # wiki: §6.7 — healthy baseline, no fault detected
    STUCK_LEAN          = "STUCK_LEAN"          # wiki: §6.7 — pinned < 0.2 V (narrowband)
    STUCK_RICH          = "STUCK_RICH"          # wiki: §6.7 — pinned > 0.85 V (narrowband)
    WIDEBAND_OFFSET_CANDIDATE = "WIDEBAND_OFFSET_CANDIDATE"  # wiki: o2-logic/03 §BIASED_OFFSET / o2-logic/08

