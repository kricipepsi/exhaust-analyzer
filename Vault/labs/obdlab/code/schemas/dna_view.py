"""OBDLab DNA view — typed DNA-first input per NewArchProposal §4 Step 2 / §5.

ObdLabDnaView is the OBDLab-owned mirror of the COMLab DNA projection.
Never import this from comlab, dnalab, or vinlab — this file is the only
DNA surface OBDLab sees.
"""

from enum import StrEnum

from pydantic import BaseModel, Field


class AirMeteringStrategy(StrEnum):
    """Air metering strategy per OBD_VOCABULARY.md §4.2.

    Source: OBD_VOCABULARY.md §4.2, SEMANTIC_CONTRACT.md §6.2.
    """
    DUAL_MAF_MAP_CROSSCHECK = "DUAL_MAF_MAP_CROSSCHECK"  # wiki: OBD_VOCABULARY.md §4.2 — both sensors present
    MAP_ONLY_SPEED_DENSITY  = "MAP_ONLY_SPEED_DENSITY"   # wiki: OBD_VOCABULARY.md §4.2 — no MAF sensor
    MAF_ONLY                = "MAF_ONLY"                 # wiki: OBD_VOCABULARY.md §4.2 — no MAP sensor



class O2SensorType(StrEnum):
    """Upstream O2 sensor type per OBD_VOCABULARY.md §4.3.

    Source: OBD_VOCABULARY.md §4.3, SEMANTIC_CONTRACT.md §6.3.
    Drives OBDLab-internal O2NormalizationMode selection (§11).
    """
    NARROWBAND_0_TO_1V = "NARROWBAND_0_TO_1V"  # wiki: OBD_VOCABULARY.md §4.3 — voltage swing 0.1-0.9V
    WIDEBAND_LINEAR    = "WIDEBAND_LINEAR"      # wiki: OBD_VOCABULARY.md §4.3 — linear lambda/AFR
    WIDEBAND_NB_SIM    = "WIDEBAND_NB_SIM"      # wiki: OBD_VOCABULARY.md §4.3 — aftermarket WB in NB simulation mode, reads pid_oxygen_sensor_volts


class InductionType(StrEnum):
    """Forced induction type per SEMANTIC_CONTRACT.md §8.

    Source: SEMANTIC_CONTRACT.md §8.
    Used by Physics_Gate_3 (NA engine VE ceiling) per OBDLab_KG_Wiki.md §4.
    """
    NATURALLY_ASPIRATED = "NATURALLY_ASPIRATED"  # wiki: SEMANTIC_CONTRACT.md §8
    TURBOCHARGED        = "TURBOCHARGED"          # wiki: SEMANTIC_CONTRACT.md §8


class VinConfidence(StrEnum):
    """VIN decode confidence per SEMANTIC_CONTRACT.md §8.

    Source: SEMANTIC_CONTRACT.md §8, OBD_VOCABULARY.md §8.
    Gates DNA-relative checks via the three-branch pattern:
    HIGH strict, PARTIAL log-and-fallback, NONE/None static.
    """
    HIGH    = "HIGH"     # wiki: SEMANTIC_CONTRACT.md §8 — all WMI/year/engine_code resolved
    PARTIAL = "PARTIAL"  # wiki: SEMANTIC_CONTRACT.md §8 — year resolved, engine_code unknown
    NONE    = "NONE"     # wiki: SEMANTIC_CONTRACT.md §8 — WMI not found in registry


class ObdLabDnaView(BaseModel):
    """Typed DNA view consumed by OBDLab — per NewArchProposal §4 Step 2 / §5.

    This is the OBDLab-owned mirror of the COMLab DNA projection.
    None at the call boundary is permitted and treated as confidence == NONE.

    Source: NewArchProposal_ImplementationPlan.md §4 Step 2.
    """
    engine_displacement_liters: float | None = Field(default=None)  # wiki: OBDLab_KG_Wiki.md §10 — for VE formula
    rated_rpm: int | None = Field(default=None)                     # wiki: OBDLab_KG_Wiki.md §3.1 — DNA-relative RPM ceiling

    stress_idle_rpm_target: int | None = Field(default=None)        # wiki: OBD_VOCABULARY.md §3.2 — per-vehicle stress RPM
    air_metering_strategy: AirMeteringStrategy # wiki: OBDLab_KG_Wiki.md §6.2 — VE routing switch
    upstream_o2_type: O2SensorType             # wiki: OBDLab_KG_Wiki.md §11 — O2 normalization switch
    induction_type: InductionType              # wiki: OBDLab_KG_Wiki.md §4 — Physics_Gate_3
    confidence: VinConfidence                  # wiki: NewArchProposal §3.3 — three-branch gate
class ObdEmissionsView(BaseModel):
    """Minimal emissions view after purge. Only includes egr_equipped flag used by composition."""
    egr_equipped: bool = Field(default=False)
