"""Script 4: Power Loss Analytics — the mathematical estimator.

Scale-independent calculator for two UI-facing performance metrics:

    1. Kinetic Power Loss %      how much mechanical power is missing
    2. Catalyst Health Index %   how well the cat is converting CO + HC

The Gas Lab is context-blind: it knows raw gas concentrations but not how
many cylinders the engine has. This script applies the cylinder dilution rule
and pre-vs-post-cat baseline math to translate raw chemistry into a percent.

Sub-components (per OrchestratorLabBP.md component tree, line 1422):
    - Combustion_Inefficiency_Scaling_Calculator   ignition-failure vs partial-burn branches
    - Piston_Count_Dilution_Normalizer             4.0 / cylinder_count weighting
    - Kinetic_Power_Loss_Estimator                 clamp + round
    - Pre_vs_Post_Cat_Sensor_Cross_Validator       wideband lambda vs narrowband voltage
    - Catalyst_Conversion_Efficiency_Engine        CO*0.70 + HC*0.30

Source: COMLab_LLD.md §7.
"""

from __future__ import annotations

from comlab.schemas.ingestion import OrchestratorInboundRequest
from comlab.schemas.response import PerformanceAnalytics, SeverityLit


class PowerLossAnalytics:
    """Static methods only — this class is pure math, no state.

    Reference test cases (BP lines 240-281), to verify in phase 2:
        4-cyl single misfire (HC 3200, O2 5.1, CO 0.1, lambda 1.25)  -> 23.3%
        8-cyl same chemistry                                         -> 11.6%
        partial combustion  (HC 850, O2 3.8, CO 3.8, lambda 0.88)    -> 22.9%
    """

    # -- severity band boundaries (wiki: OBD_VOCABULARY misfire signature math) --
    _CRITICAL_THRESHOLD: float = 20.0  # lld: §7 — >= 20% → CRITICAL_IMMEDIATE_STOP
    _WARNING_THRESHOLD: float = 10.0  # lld: §7 — >= 10% → WARNING_DEGRADED_PERFORMANCE

    # -- ignition failure gate (BP line 212) --
    _IGNITION_O2_FLOOR: float = 2.0  # lld: §7 — O2% must exceed this for ignition pathway
    _IGNITION_LAMBDA_FLOOR: float = 1.05  # lld: §7 — lambda must exceed this for lean pathway
    _IGNITION_O2_FACTOR: float = 4.5  # lld: §7 — O2 spike dominates in misfire
    _IGNITION_HC_FACTOR: float = 1.2  # lld: §7 — HC secondary term in misfire
    _RICH_CO_FACTOR: float = 6.0  # lld: §7 — CO dominates rich partial burn
    _RICH_HC_FACTOR: float = 0.8  # lld: §7 — HC secondary term in partial burn
    _PPM_PER_PERCENT: float = 10000.0  # wiki: OBD_VOCABULARY — ppm to % volume
    _DILUTION_REFERENCE_CYLINDERS: float = 4.0  # wiki: OBD_VOCABULARY — 4-cyl reference
    _PCT_MIN: float = 0.0  # lld: §7 — percent clamp floor
    _PCT_MAX: float = 100.0  # lld: §7 — percent clamp ceiling
    _PCT_ROUND_DIGITS: int = 1  # lld: §7 — UI-facing percent precision


    # -- catalyst baseline constants (BP line 439) --
    _CO_BASELINE_RICH: float = 0.65  # lld: §7 — engine-out CO baseline when pre-cat lambda ≤ 1.000
    _CO_BASELINE_LEAN: float = 0.15  # lld: §7 — engine-out CO baseline when pre-cat lambda > 1.000
    _HC_BASELINE_PPM: float = 250.0  # lld: §7 — engine-out HC baseline (PPM)
    _CO_WEIGHT: float = 0.70  # lld: §7 — CO conversion weight in catalyst health index
    _HC_WEIGHT: float = 0.30  # lld: §7 — HC conversion weight in catalyst health index
    _STOICH_LAMBDA: float = 1.000  # wiki: OBD_VOCABULARY §12.1 — stoichiometric λ
    _NARROWBAND_STOICH_LOW_V: float = 0.4  # wiki: OBD_VOCABULARY §12.1 — stoich window low
    _NARROWBAND_STOICH_HIGH_V: float = 0.5  # wiki: OBD_VOCABULARY §12.1 — stoich window high
    _NARROWBAND_RICH_LAMBDA: float = 0.950  # wiki: OBD_VOCABULARY §12.1 — rich outside stoich

    @staticmethod
    def estimate_kinetic_loss(
        gas_hc: float,
        gas_o2: float,
        gas_co: float,
        lambda_chem: float,
        cylinder_count: int,
    ) -> float:
        """Sub-Components: Combustion_Inefficiency_Scaling_Calculator +
        Piston_Count_Dilution_Normalizer + Kinetic_Power_Loss_Estimator.

        Returns power loss percent in [0.0, 100.0], rounded to 1 decimal.

        Algorithm (BP line 212):
            hc_pct = gas_hc / 10000.0
            if lambda_chem > 1.05 and gas_o2 > 2.0:   # ignition failure pathway
                raw = (gas_o2 * 4.5) + (hc_pct * 1.2)
            else:                                      # partial-burn / rich pathway
                raw = (gas_co * 6.0) + (hc_pct * 0.8)
            return clamp(raw * 4.0 / cylinder_count, 0, 100)
        """
        hc_pct = gas_hc / PowerLossAnalytics._PPM_PER_PERCENT

        if (
            lambda_chem > PowerLossAnalytics._IGNITION_LAMBDA_FLOOR
            and gas_o2 > PowerLossAnalytics._IGNITION_O2_FLOOR
        ):
            raw = (
                gas_o2 * PowerLossAnalytics._IGNITION_O2_FACTOR
            ) + (hc_pct * PowerLossAnalytics._IGNITION_HC_FACTOR)
        else:  # partial-burn / rich pathway
            raw = (
                gas_co * PowerLossAnalytics._RICH_CO_FACTOR
            ) + (hc_pct * PowerLossAnalytics._RICH_HC_FACTOR)

        diluted = (
            raw * PowerLossAnalytics._DILUTION_REFERENCE_CYLINDERS / cylinder_count
        )
        clamped = max(
            PowerLossAnalytics._PCT_MIN,
            min(PowerLossAnalytics._PCT_MAX, diluted),
        )
        return round(clamped, PowerLossAnalytics._PCT_ROUND_DIGITS)

    @staticmethod
    def derive_pre_cat_lambda(
        horizon: str,
        pre_cat_wideband_lambda: float | None = None,
        pre_cat_narrowband_volt: float | None = None,
    ) -> float:
        """Sub-Component: Pre_vs_Post_Cat_Sensor_Cross_Validator.

        Modern cars report wideband lambda directly. Legacy cars only have a
        narrowband voltage swing; we map voltage range [0.4, 0.5] -> lambda 1.00,
        else -> 0.95 (mildly rich).

        wiki: OBD_VOCABULARY §12.1 — narrowband 3-zone voltage mapping.
        """
        if pre_cat_wideband_lambda is not None:
            return pre_cat_wideband_lambda  # lld: §7 — wideband passthrough

        if pre_cat_narrowband_volt is not None:
            in_stoich_window = (
                PowerLossAnalytics._NARROWBAND_STOICH_LOW_V
                <= pre_cat_narrowband_volt
                <= PowerLossAnalytics._NARROWBAND_STOICH_HIGH_V
            )
            if in_stoich_window:
                return PowerLossAnalytics._STOICH_LAMBDA
            return PowerLossAnalytics._NARROWBAND_RICH_LAMBDA

        return PowerLossAnalytics._STOICH_LAMBDA

    @staticmethod
    def calculate_catalyst_health_index(
        gas_co: float,
        gas_hc: float,
        pre_cat_lambda: float = 1.000,
    ) -> float:
        """Sub-Component: Catalyst_Conversion_Efficiency_Engine.

        Returns Catalyst Health Index in [0.0, 100.0], rounded to 1 decimal.

        Algorithm (BP line 439):
            engine_out_co_baseline = 0.65 if pre_cat_lambda <= 1.000 else 0.15
            engine_out_hc_baseline = 250.0  # PPM
            co_eff = max(0, (baseline - gas_co) / baseline * 100)
            hc_eff = max(0, (baseline - gas_hc) / baseline * 100)
            chi    = co_eff * 0.70 + hc_eff * 0.30
        """
        co_baseline = (
            PowerLossAnalytics._CO_BASELINE_RICH
            if pre_cat_lambda <= PowerLossAnalytics._STOICH_LAMBDA
            else PowerLossAnalytics._CO_BASELINE_LEAN
        )

        co_eff = max(
            PowerLossAnalytics._PCT_MIN,
            (co_baseline - gas_co) / co_baseline * PowerLossAnalytics._PCT_MAX,
        )
        hc_eff = max(
            PowerLossAnalytics._PCT_MIN,
            (PowerLossAnalytics._HC_BASELINE_PPM - gas_hc)
            / PowerLossAnalytics._HC_BASELINE_PPM
            * PowerLossAnalytics._PCT_MAX,
        )

        chi = (
            co_eff * PowerLossAnalytics._CO_WEIGHT
            + hc_eff * PowerLossAnalytics._HC_WEIGHT
        )
        clamped = max(
            PowerLossAnalytics._PCT_MIN,
            min(PowerLossAnalytics._PCT_MAX, chi),
        )
        return round(clamped, PowerLossAnalytics._PCT_ROUND_DIGITS)

    def compute(
        self,
        request: OrchestratorInboundRequest,
        cylinder_count: int,
        downstream_o2_present: bool = False,
        has_catalyst: bool = True,
        lambda_perception_delta: float = 0.0,
        o2_sensor_bias_verdict: str | None = None,
    ) -> PerformanceAnalytics:
        """Stage D — returns the populated PerformanceAnalytics block.

        Calculates:
          - kinetic_power_loss_pct from gas chemistry deltas + cylinder
            dilution per OBD_VOCABULARY misfire math
          - catalyst_efficiency_index_pct from CO/HC conversion ratios —
            only when downstream_o2_present == True AND has_catalyst == True;
            else None (de-cat vehicles cannot produce a meaningful CHI)
          - severity_level mapping power_loss_pct into
            CRITICAL/WARNING/OPTIMAL bands

        lambda_perception_delta and o2_sensor_bias_verdict are populated
        earlier by the perception-contradiction detector (Stage A) —
        Stage D passes them through unchanged.

        Pure function; no I/O.

        lld: §7
        """
        gas = request.gas_lab_output

        # -- kinetic power loss --
        power_loss = self.estimate_kinetic_loss(
            gas_hc=float(gas.gas_hc),
            gas_o2=gas.gas_o2,
            gas_co=gas.gas_co,
            lambda_chem=gas.lambda_chem,
            cylinder_count=cylinder_count,
        )  # lld: §7

        # -- catalyst efficiency (gated on downstream O2 presence + catalyst present) --
        # wiki: O2_MODEL_STRATEGY.md §9.1 — de-cat vehicles have no catalyst to measure
        if downstream_o2_present and has_catalyst:
            cat_idx = self.calculate_catalyst_health_index(
                gas_co=gas.gas_co,
                gas_hc=float(gas.gas_hc),
                pre_cat_lambda=gas.lambda_chem,  # lld: §7 — pre-cat λ ≈ gas chemistry λ
            )
        else:
            cat_idx = None  # lld: §7 — no downstream O2 or de-cat → cannot compute

        # -- severity level mapping --
        severity = self._map_severity(power_loss)  # lld: §7

        return PerformanceAnalytics(
            kinetic_power_loss_pct=power_loss,
            catalyst_efficiency_index_pct=cat_idx,
            lambda_perception_delta=lambda_perception_delta,
            o2_sensor_bias_verdict=o2_sensor_bias_verdict,
            severity_level=severity,  # type: ignore[arg-type]
        )

    def _map_severity(self, power_loss_pct: float) -> SeverityLit:
        """Map kinetic_power_loss_pct into severity bands.

        lld: §7 — severity registry.
        """
        if power_loss_pct >= self._CRITICAL_THRESHOLD:
            return "CRITICAL_IMMEDIATE_STOP"  # lld: §7 — ≥ 20% power loss
        if power_loss_pct >= self._WARNING_THRESHOLD:
            return "WARNING_DEGRADED_PERFORMANCE"  # lld: §7 — ≥ 10% power loss
        return "OPTIMAL_HEALTH"  # lld: §7 — < 10% power loss
