"""VE computation engine per OBDLab_KG_Wiki.md §10.

Implements the Speed-Density Ideal Gas formula (§10.1) with 3-branch
polymorphic routing (§10.2) and VE-fault triggers (§6.4 / §10.3).
Source: OBDLab_KG_Wiki.md §10, BP §1.
"""

import logging
from typing import Any

from obdlab.schemas.dna_view import (
    AirMeteringStrategy,
    InductionType,
    ObdLabDnaView,
)
from obdlab.schemas.vocabulary import (
    NodeMAFStatus,
    NodeMAPStatus,
    RpmStateBucket,
    VEValidity,
)

logger = logging.getLogger(__name__)

# wiki: §10.1 — molar mass of air (g/mol)
MM_AIR: float = 28.97
# wiki: §10.1 — universal gas constant (J/(mol·K))
R_GAS: float = 8.314
# wiki: §10.1 — °C to K offset
K_OFFSET: float = 273.15

# wiki: BP §1.B / §1.C — expected VE fractions per (bucket, MAP_ONLY|MAF_ONLY)
_EXPECTED_VE: dict[tuple[str, str], float] = {
    # MAP_ONLY_SPEED_DENSITY targets
    (RpmStateBucket.STABILIZED_IDLE.value, AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY.value): 0.65,
    (RpmStateBucket.REGULATORY_HIGH_IDLE.value, AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY.value): 0.80,
    (RpmStateBucket.STRESS_IDLE.value, AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY.value): 0.80,
    # MAF_ONLY targets
    (RpmStateBucket.STABILIZED_IDLE.value, AirMeteringStrategy.MAF_ONLY.value): 0.70,
    (RpmStateBucket.REGULATORY_HIGH_IDLE.value, AirMeteringStrategy.MAF_ONLY.value): 0.82,
    (RpmStateBucket.STRESS_IDLE.value, AirMeteringStrategy.MAF_ONLY.value): 0.82,
}

# wiki: §10.3 / §6.4 — VE fault trigger thresholds
_CUTOFF_VE_COLLAPSE = 50.0     # wiki: §6.4 — VE% below which idle VE collapse triggers
_CUTOFF_MAP_COLLAPSE = 45.0    # wiki: BP §2 — MAP must be > 45 kPa for collapse trigger
_CUTOFF_VE_CONTAMINATION = 65.0  # wiki: §6.4 — VE% below which MAF contamination triggers
_CUTOFF_TFT_CONTAMINATION = 15.0  # wiki: §6.4 — TFT > 15% for MAF contamination
_CUTOFF_VE_SKEW = 90.0         # wiki: §6.4 — VE% above which sensor skew triggers

# wiki: §10.2 — branches that do not use MAF sensor
_MAP_ONLY_STRATEGIES = frozenset({AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY.value})
_MAF_ONLY_STRATEGIES = frozenset({AirMeteringStrategy.MAF_ONLY.value})


class VEEngine:
    """VE computation engine with 3-branch polymorphic routing per §10.2.

    Public entry point: compute_ve().
    """

    def compute_ve(
        self,
        pids: dict[str, Any],
        bucket: RpmStateBucket,
        dna_view: ObdLabDnaView | None = None,
    ) -> tuple[float | None, NodeMAFStatus, NodeMAPStatus, VEValidity]:
        """Compute volumetric efficiency via the matching routing branch.

        Args:
            pids: sanitized PID dict (must contain mass_airflow_gps, manifold_vacuum_kpa,
                  engine_rpm, intake_air_temp_c as available).
            bucket: current RpmStateBucket.
            dna_view: typed DNA view or None.

        Returns:
            (ve_pct, maf_status, map_status, validity).
            ve_pct is None when computation is impossible (e.g., missing critical input).
        """
        displacement = dna_view.engine_displacement_liters if dna_view else None
        strategy = (
            dna_view.air_metering_strategy if dna_view
            else AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK
        )

        if strategy == AirMeteringStrategy.DUAL_MAF_MAP_CROSSCHECK:
            return self._ve_dual(pids, displacement)

        if strategy == AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY:
            return self._ve_map_only(pids, bucket, displacement)

        if strategy == AirMeteringStrategy.MAF_ONLY:
            return self._ve_maf_only(pids, bucket, displacement)

        raise ValueError(f"Unknown air_metering_strategy: {strategy}")

    # ------------------------------------------------------------------
    # DUAL_MAF_MAP_CROSSCHECK — standard formula §10.1
    # ------------------------------------------------------------------

    def _ve_dual(
        self, pids: dict[str, Any], displacement: float | None,
    ) -> tuple[float | None, NodeMAFStatus, NodeMAPStatus, VEValidity]:
        """Standard VE formula §10.1 — both MAF and MAP present."""
        maf = pids.get("mass_airflow_gps")
        map_kpa = pids.get("manifold_vacuum_kpa")
        rpm = pids.get("engine_rpm")
        iat = pids.get("intake_air_temp_c")

        if maf is None or map_kpa is None or rpm is None or rpm == 0 or displacement is None:
            return (None, NodeMAFStatus.REAL_SENSOR_FEED, NodeMAPStatus.REAL_SENSOR_FEED, VEValidity.UNKNOWN)

        ve_pct = self._calc_ve_standard(maf, map_kpa, rpm, displacement, iat or 25.0)
        validity = self._classify_validity(ve_pct, pids)
        return (ve_pct, NodeMAFStatus.REAL_SENSOR_FEED, NodeMAPStatus.REAL_SENSOR_FEED, validity)

    # ------------------------------------------------------------------
    # MAP_ONLY_SPEED_DENSITY — emulate MAF from MAP §10.2
    # ------------------------------------------------------------------

    def _ve_map_only(
        self, pids: dict[str, Any], bucket: RpmStateBucket, displacement: float | None,
    ) -> tuple[float | None, NodeMAFStatus, NodeMAPStatus, VEValidity]:
        """Emulate MAF from MAP+RPM+Displacement, then compute VE.

        Emulated_MAF = MAP × (RPM/60) × (Disp/2) × MM / (R × IAT_K) × target_VE
        """
        map_kpa = pids.get("manifold_vacuum_kpa")
        rpm = pids.get("engine_rpm")
        iat = pids.get("intake_air_temp_c")

        if map_kpa is None or rpm is None or rpm == 0 or displacement is None:
            return (None, NodeMAFStatus.VIRTUAL_EMULATION, NodeMAPStatus.REAL_SENSOR_FEED, VEValidity.UNKNOWN)

        target_ve = self._expected_ve(bucket, AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY)
        if target_ve is None:
            return (None, NodeMAFStatus.VIRTUAL_EMULATION, NodeMAPStatus.REAL_SENSOR_FEED, VEValidity.UNKNOWN)

        iat_k = (iat or 25.0) + K_OFFSET  # wiki: §10.1
        # wiki: §10.2 — MAP_ONLY emulation (corrected units)
        emulated_maf = (
            map_kpa * (rpm / 60.0) * (displacement / 2.0) * MM_AIR
            / (R_GAS * iat_k)
            * target_ve
        )

        ve_pct = self._calc_ve_standard(emulated_maf, map_kpa, rpm, displacement, iat or 25.0)
        # wiki: §6.4 UNKNOWN — no independent cross-check possible (emulated MAF algebraically cancels)
        validity = VEValidity.UNKNOWN
        return (ve_pct, NodeMAFStatus.VIRTUAL_EMULATION, NodeMAPStatus.REAL_SENSOR_FEED, validity)

    # ------------------------------------------------------------------
    # MAF_ONLY — back-calculate MAP from MAF §10.2
    # ------------------------------------------------------------------

    def _ve_maf_only(
        self, pids: dict[str, Any], bucket: RpmStateBucket, displacement: float | None,
    ) -> tuple[float | None, NodeMAFStatus, NodeMAPStatus, VEValidity]:
        """Back-calculate MAP from MAF+RPM+Displacement, then compute VE.

        Inferred_MAP = MAF × R × IAT_K / ((RPM/60) × (Disp/2) × MM × target_VE)
        """
        maf = pids.get("mass_airflow_gps")
        rpm = pids.get("engine_rpm")
        iat = pids.get("intake_air_temp_c")

        if maf is None or rpm is None or rpm == 0 or displacement is None:
            return (None, NodeMAFStatus.REAL_SENSOR_FEED, NodeMAPStatus.BACK_CALCULATED, VEValidity.UNKNOWN)

        target_ve = self._expected_ve(bucket, AirMeteringStrategy.MAF_ONLY)
        if target_ve is None:
            return (None, NodeMAFStatus.REAL_SENSOR_FEED, NodeMAPStatus.BACK_CALCULATED, VEValidity.UNKNOWN)

        iat_k = (iat or 25.0) + K_OFFSET  # wiki: §10.1
        # wiki: §10.2 — MAF_ONLY back-calculation (corrected units)
        inferred_map = (
            maf * R_GAS * iat_k
            / ((rpm / 60.0) * (displacement / 2.0) * MM_AIR * target_ve)
        )

        ve_pct = self._calc_ve_standard(maf, inferred_map, rpm, displacement, iat or 25.0)
        # wiki: §6.4 UNKNOWN — no independent cross-check possible (back-calculated MAP algebraically cancels)
        validity = VEValidity.UNKNOWN
        return (ve_pct, NodeMAFStatus.REAL_SENSOR_FEED, NodeMAPStatus.BACK_CALCULATED, validity)

    # ------------------------------------------------------------------
    # Standard VE formula §10.1
    # ------------------------------------------------------------------

    @staticmethod
    def _calc_ve_standard(
        maf: float, map_kpa: float, rpm: int, displacement: float, iat_c: float,
    ) -> float:
        """Speed-Density Ideal Gas VE formula per §10.1.

        VE (%) = [MAF × 8.314 × (IAT_C + 273.15)]
                 / [MAP × (RPM/60) × (Disp/2) × 28.97] × 100
        Wiki formula has R/MM transposed; this implementation uses the
        physically correct placement (see unit analysis in _calc_ve_standard).
        """
        iat_k = iat_c + K_OFFSET                      # wiki: §10.1
        numerator = maf * R_GAS * iat_k               # wiki: §10.1 — R in numerator
        denominator = (
            map_kpa * (rpm / 60.0) * (displacement / 2.0) * MM_AIR  # wiki: §10.1 — MM in denominator
        )
        if denominator == 0.0:
            return 0.0
        return (numerator / denominator) * 100.0

    # ------------------------------------------------------------------
    # Expected VE lookup per bucket + strategy
    # ------------------------------------------------------------------

    @staticmethod
    def _expected_ve(bucket: RpmStateBucket, strategy: AirMeteringStrategy) -> float | None:
        """Expected VE fraction for MAP_ONLY or MAF_ONLY emulation target."""
        return _EXPECTED_VE.get((bucket.value, strategy.value))

    # ------------------------------------------------------------------
    # VE-fault classification §6.4 / §10.3
    # ------------------------------------------------------------------

    def _classify_validity(
        self, ve_pct: float, pids: dict[str, Any],
    ) -> VEValidity:
        """Classify VE result against fault triggers per §6.4 / §10.3.

        FAULT_VE_IDLE_COLLAPSE:  ve < 50 AND bucket=STABILIZED_IDLE AND MAP > 45 kPa
        FAULT_MAF_CONTAMINATION: ve < 65 AND bucket∈{STRESS_IDLE, REGULATORY_HIGH_IDLE} AND TFT > 15
        FAULT_VE_SENSOR_SKEW:    ve > 90 AND bucket=STABILIZED_IDLE AND induction=NATURALLY_ASPIRATED
        UNKNOWN:                 insufficient inputs (handled by callers returning UNKNOWN)
        VALID:                   otherwise
        """
        bucket_raw = pids.get("rpm_state_bucket")
        map_kpa = pids.get("manifold_vacuum_kpa")
        tft = pids.get("total_trim_correction_delta")
        # wiki: §6.4 — compute raw trim from fuel trims when aggregated delta not yet available
        if tft is None:
            sft1 = pids.get("shrtft1")
            lft1 = pids.get("longft1")
            if sft1 is not None and lft1 is not None:
                tft = float(sft1) + float(lft1)
        induction_raw = pids.get("induction_type")

        # FAULT_VE_IDLE_COLLAPSE — wiki: §6.4
        if (
            bucket_raw == RpmStateBucket.STABILIZED_IDLE.value
            and ve_pct < _CUTOFF_VE_COLLAPSE
            and map_kpa is not None
            and map_kpa > _CUTOFF_MAP_COLLAPSE
        ):
            return VEValidity.FAULT_VE_IDLE_COLLAPSE

        # FAULT_MAF_CONTAMINATION — wiki: §6.4
        if (
            bucket_raw in (
                RpmStateBucket.STRESS_IDLE.value,
                RpmStateBucket.REGULATORY_HIGH_IDLE.value,
            )
            and ve_pct < _CUTOFF_VE_CONTAMINATION
            and tft is not None
            and tft > _CUTOFF_TFT_CONTAMINATION
        ):
            return VEValidity.FAULT_MAF_CONTAMINATION

        # FAULT_VE_SENSOR_SKEW — wiki: §6.4
        if (
            bucket_raw == RpmStateBucket.STABILIZED_IDLE.value
            and ve_pct > _CUTOFF_VE_SKEW
            and induction_raw == InductionType.NATURALLY_ASPIRATED.value
        ):
            return VEValidity.FAULT_VE_SENSOR_SKEW

        return VEValidity.VALID
