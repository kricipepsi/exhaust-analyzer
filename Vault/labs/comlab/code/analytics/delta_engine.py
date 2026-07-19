"""Delta engine — COMLab's stateless two-operating-point delta calculator.

This is the long-open *FU-2* consumer for the OBDLab `delta-relations/*` research
(6 ΔTrim profile chunks + a 2-speed Δgas matrix + ΔO₂ feeders). The emitter labs
stay stateless and single-point; the cross-state Δ math lives here, in COMLab
(`delta-relations/07`: "the per-state frame is produced by the emitters; the
cross-state Δ math is COMLab").

When a case carries an optional ``second_operating_point`` frame, the engine
differences it against the primary (low-idle) channels carried on the request and
emits a typed :class:`DeltaSignature`. The signature is read by
``fault_atlas_router.execute_triage_loop`` Phase 5 as a **primary** rank term: the
delta-matched fault family is promoted above the base-weighted static signatures,
which become the fallback (a new ``SINGLE_POINT`` degradation mode names the
absent-second-frame path).

Diagnostic order (mandatory — `delta-relations/06`):
    1. architecture gate FIRST — speed-density NULLs ΔTrim for a real leak;
       forced induction INVERTS its sign. Applying a profile without first
       branching on air-metering / induction *creates* misclassifications.
    2. validity gate — vsum 14-18 % / dilution / RPM-settle must hold on BOTH
       frames before a delta is trusted (`delta-relations/08`).
    3. per-signal band checks — ΔTrim is only read at STRESS_IDLE; Δgas/ΔO₂ only
       at REGULATORY_HIGH_IDLE; a band mismatch ABSTAINS rather than differencing
       against a baseline measured at a different RPM (SWEEP_MANIFEST §7).

Stateless, static-only, pure math — mirrors ``PowerLossAnalytics``. No I/O, no
logging, no tracing (the caller owns those).

Source: labs/obdlab/research/chunks/delta-relations/01-08; SWEEP_MANIFEST §7;
research/PROPOSAL_DeltaLab_cross_lab_delta_module.md.
"""

from __future__ import annotations

from typing import Literal, Optional

from pydantic import BaseModel, Field

from comlab.schemas.ingestion import (
    OrchestratorInboundRequest,
    SecondOperatingPointFrame,
)
from comlab.schemas.vocabulary import (
    AirMeteringStrategy,
    EngineStateBucket,
    InductionType,
    SampleValidity,
)

# ---------------------------------------------------------------------------
# Typed output models
# ---------------------------------------------------------------------------

TrimSignLit = Literal["POSITIVE", "NEGATIVE", "FLAT", "NULL"]
TrimProfileLit = Literal[
    "VACUUM_LEAK",
    "FUEL_STARVATION",
    "MAF_UNDERREPORT",
    "EXHAUST_BACKPRESSURE",
    "NONE",
    "ABSTAIN",
]
GasProfileLit = Literal[
    "WORN_PISTON_RINGS",
    "WORN_VALVE_SEALS",
    "FLAT_CAM",
    "EGR_STUCK_CLOSED",
    "RICH_ATTENUATING",
    "NONE",
    "ABSTAIN",
]
DegradationModeLit = Literal[
    "FULL_FUSION", "GAS_DOMINANT", "SINGLE_POINT", "FATAL_INCOMPLETE"
]


class DeltaTrimResult(BaseModel):
    """ΔTrim across the RPM step (delta-relations/01-05), architecture-gated."""

    delta_total_trim: float | None = None
    low_total_trim: float | None = None
    elevated_total_trim: float | None = None
    sign: TrimSignLit = "FLAT"  # NULL == architecture-nulled (speed-density)
    profile: TrimProfileLit = "NONE"


class DeltaGasResult(BaseModel):
    """Δgas across the RPM step (delta-relations/07)."""

    d_hc: int | None = None
    d_co: float | None = None
    d_co2: float | None = None
    d_o2: float | None = None
    d_lambda: float | None = None
    d_nox: int | None = None
    gas_profile: GasProfileLit = "NONE"


class DeltaO2Result(BaseModel):
    """ΔO₂ feeders (SWEEP_MANIFEST §7). Named-only — subtraction passthrough.

    The o2-logic deltas (Δswitch_freq, Δvoltage_bias, Δdownstream_response) are not
    yet quantified, so this result never sets a profile; it carries the raw deltas
    forward for a future O2-FU consumer.
    """

    d_switch_freq: float | None = None
    d_voltage_bias: float | None = None
    d_downstream_response: float | None = None


class DeltaValidityVerdict(BaseModel):
    """Per-frame sample-validity verdict for the second reading (delta-relations/08)."""

    low_frame_valid: bool = True
    elevated_frame_valid: bool = True
    trusted: bool = False
    reason: str = ""


class ArchitectureGateVerdict(BaseModel):
    """Air-metering / induction gate applied BEFORE any ΔTrim profile (delta-relations/06)."""

    air_metering_strategy: Optional[AirMeteringStrategy] = None
    induction_type: Optional[InductionType] = None
    trim_nulled: bool = False  # speed-density: ΔTrim ≈ 0 for a real leak
    trim_inverted: bool = False  # forced induction: post-turbo leak inverts ΔTrim sign
    note: str = ""


class DeltaSignature(BaseModel):
    """The cross-lab delta signature consumed by fault_atlas_router Phase 5.

    ``present`` and ``confidence`` are the byte-identity contract: Phase 5 fires
    only on ``present and confidence > 0``. ``present=False`` is the single-point
    sentinel (no second frame); ``confidence == 0.0`` covers untrusted / nulled /
    abstaining frames, all of which leave the static rank path untouched.
    """

    present: bool = False
    degradation_mode: DegradationModeLit = "SINGLE_POINT"
    validity: DeltaValidityVerdict = Field(default_factory=DeltaValidityVerdict)
    architecture: ArchitectureGateVerdict = Field(default_factory=ArchitectureGateVerdict)
    trim: DeltaTrimResult = Field(default_factory=DeltaTrimResult)
    gas: DeltaGasResult = Field(default_factory=DeltaGasResult)
    o2: DeltaO2Result = Field(default_factory=DeltaO2Result)
    primary_profile: str = "NONE"
    target_fault_family: str | None = None
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class DeltaEngine:
    """Static methods only — pure two-point delta math, no state.

    Mirrors ``PowerLossAnalytics``: every numeric band/tolerance is a class
    attribute carrying a ``# wiki:`` citation back to the delta-relations chunk
    it traces to.
    """

    # -- per-signal bands (SWEEP_MANIFEST §7 — do not silently mix) --
    _TRIM_BAND = EngineStateBucket.STRESS_IDLE  # wiki: delta-relations/01 — ΔTrim @ 3500-4500
    _GAS_BAND = EngineStateBucket.REGULATORY_HIGH_IDLE  # wiki: delta-relations/07 — Δgas @ ~2500

    # -- ΔTrim profile thresholds (delta-relations/02-05; trims in %) --
    _DTRIM_LEAK_MAX: float = -10.0  # wiki: delta-relations/02 — vacuum leak ΔTrim ≤ -10
    _DTRIM_SUPPLY_MIN: float = +10.0  # wiki: delta-relations/03,04 — starvation/MAF ΔTrim ≥ +10
    _DTRIM_BACKPRESS_MAX: float = -10.0  # wiki: delta-relations/05 — backpressure ΔTrim ≤ -10
    _VACLEAK_LOW_MIN: float = +15.0  # wiki: delta-relations/02 — vacuum leak low-idle +15..+25
    _STARVE_LOW_MAX: float = +5.0  # wiki: delta-relations/03 — fuel starvation low-idle 0..+5
    _MAF_LOW_MAX: float = +8.0  # wiki: delta-relations/04 — MAF under-report low-idle 0..+8
    _BACKPRESS_ELEV_MAX: float = -12.0  # wiki: delta-relations/05 — backpressure elevated ≤ -12
    _BACKPRESS_LOW_ABS: float = +5.0  # wiki: delta-relations/05 — backpressure starts ≈ 0 at low idle

    # -- Δgas profile thresholds (delta-relations/07; HC ppm, NOx ppm) --
    _DHC_RINGS_MIN: int = +100  # wiki: delta-relations/07 — worn rings ΔHC ≥ +100 (15→180)
    _DHC_VALVE_MAX: int = -50  # wiki: delta-relations/07 — worn valve seals ΔHC ≤ -50 (120→15)
    _FLATCAM_ELEV_O2_MIN: float = 2.0  # wiki: delta-relations/07 — flat cam breathing misfire, elevated O2 ≥ ~2.5
    _DNOX_EGR_MIN: int = +800  # wiki: delta-relations/07 — EGR stuck-closed ΔNOx ≥ +800 (1500→2800)
    _DLAMBDA_RICH_MIN: float = +0.05  # wiki: delta-relations/07 — rich faults attenuate, Δλ ≥ +0.05

    # -- architecture (delta-relations/06) --
    _TURBO_INVERT_STFT: float = -20.0  # wiki: delta-relations/06 — post-turbo leak ≈ -20 % STFT

    # -- validity gate (delta-relations/08; % volume) --
    _VSUM_MIN: float = 14.0  # wiki: delta-relations/08 — valid sample vsum ≥ 14
    _VSUM_MAX: float = 18.0  # wiki: delta-relations/08 — valid sample vsum ≤ 18
    _DILUTION_COCO2_MIN: float = 6.0  # wiki: delta-relations/08 — dilution fail if CO+CO2 ≤ 6

    # -- confidence --
    _DELTA_PRIMARY_CONF: float = 0.92  # wiki: delta-relations/01 — two-point delta is the primary axis
    _UNGATED_ARCH_CONF: float = 0.70  # wiki: delta-relations/06 — cap when architecture is unknown

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    @staticmethod
    def compute_delta_signature(
        request: OrchestratorInboundRequest,
    ) -> DeltaSignature:
        """Compute the two-point :class:`DeltaSignature` for *request*.

        No ``second_operating_point`` → single-point sentinel (``present=False``).
        Otherwise: architecture gate → validity gate → per-signal band deltas →
        assemble. Any untrusted / nulled / abstaining path yields ``confidence=0.0``
        so the caller's static rank path is left byte-identical.
        """
        frame = request.second_operating_point
        if frame is None:
            return DeltaEngine._single_point_sentinel()

        # WHY: delta-relations/06 makes architecture a prerequisite; reading ΔTrim
        # before speed-density / forced-induction branching misclassifies leaks.
        arch = DeltaEngine._architecture_gate(frame)
        # WHY: delta-relations/08 keeps noisy or diluted operating-point pairs inert,
        # preserving the single-point rank path unless both frames are trustworthy.
        validity = DeltaEngine._validity_gate(request, frame)
        if not validity.trusted:
            return DeltaSignature(
                present=True,
                degradation_mode="FULL_FUSION",
                validity=validity,
                architecture=arch,
                primary_profile="UNTRUSTED",
                confidence=0.0,
            )

        trim = DeltaEngine._delta_trim(request, frame, arch)
        gas = DeltaEngine._delta_gas(request, frame)
        o2 = DeltaEngine._delta_o2(request, frame)
        return DeltaEngine._assemble(arch, validity, trim, gas, o2)

    @staticmethod
    def apply_rank_score(
        static_score: float,
        candidate_family: str | None,
        signature: DeltaSignature | None,
    ) -> tuple[float, bool]:
        """Apply the shared v1/v2 delta rank policy to one candidate.

        Delta computation owns the architecture, validity, and per-signal band
        gates. Rank consumers only promote the matching family with the trusted
        signature confidence; every sentinel/abstain path remains inert.
        """
        if (
            signature is None
            or not signature.present
            or signature.confidence <= 0.0
            or not signature.target_fault_family
            or candidate_family != signature.target_fault_family
        ):
            return static_score, False
        promoted = max(static_score, signature.confidence)
        return promoted, promoted > static_score

    # ------------------------------------------------------------------
    # Sentinels
    # ------------------------------------------------------------------

    @staticmethod
    def _single_point_sentinel() -> DeltaSignature:
        """Absent second frame → the static single-point signature is the fallback."""
        return DeltaSignature(
            present=False,
            degradation_mode="SINGLE_POINT",  # wiki: delta-relations/01
            validity=DeltaValidityVerdict(
                trusted=False, reason="no second operating-point frame"
            ),
            primary_profile="NONE",
            confidence=0.0,
        )

    # ------------------------------------------------------------------
    # Step 1 — architecture gate (delta-relations/06) — MANDATORY, runs first
    # ------------------------------------------------------------------

    @staticmethod
    def _architecture_gate(
        frame: SecondOperatingPointFrame,
    ) -> ArchitectureGateVerdict:
        """Branch on air-metering / induction BEFORE any ΔTrim profile.

        Speed-density (MAP-only) NULLs ΔTrim for a real leak — route to IAC /
        MAP-at-idle instead of profile 02. Forced induction INVERTS the sign — a
        post-turbo leak reads ≈ -20 % STFT, the opposite of an NA vacuum leak.
        """
        ams = frame.air_metering_strategy
        ind = frame.induction_type

        trim_nulled = ams == AirMeteringStrategy.MAP_ONLY_SPEED_DENSITY
        trim_inverted = ind in (
            InductionType.TURBOCHARGED,
            InductionType.SUPERCHARGED,
        )

        if trim_nulled:
            note = "speed-density: ΔTrim nulled for a real leak — route to IAC/MAP-at-idle"
        elif trim_inverted:
            note = "forced induction: ΔTrim sign inverted (post-turbo leak ≈ -20% STFT)"
        elif ams is None and ind is None:
            note = "architecture unknown — ΔTrim confidence capped (delta-relations/06 risk)"
        else:
            note = "naturally-aspirated MAF path — ΔTrim profiles apply directly"

        return ArchitectureGateVerdict(
            air_metering_strategy=ams,
            induction_type=ind,
            trim_nulled=trim_nulled,
            trim_inverted=trim_inverted,
            note=note,
        )

    # ------------------------------------------------------------------
    # Step 2 — validity gate (delta-relations/08)
    # ------------------------------------------------------------------

    @staticmethod
    def _validity_gate(
        request: OrchestratorInboundRequest,
        frame: SecondOperatingPointFrame,
    ) -> DeltaValidityVerdict:
        """Both frames must pass vsum / dilution / RPM-settle before a delta is trusted."""
        gas = request.gas_lab_output
        low_valid, low_reason = DeltaEngine._frame_gas_valid(
            gas.gas_hc, gas.gas_co, gas.gas_co2, gas.gas_o2, gas.gas_nox
        )
        # GASLab's own triangle-gate verdict on the low frame is authoritative when present.
        if gas.sample_validity == SampleValidity.INVALID:
            low_valid, low_reason = False, "low frame sample_validity=INVALID"

        elev_valid, elev_reason = DeltaEngine._frame_gas_valid(
            frame.gas_hc, frame.gas_co, frame.gas_co2, frame.gas_o2, frame.gas_nox
        )
        if frame.sample_validity == SampleValidity.INVALID:
            elev_valid, elev_reason = False, "elevated frame sample_validity=INVALID"

        if not frame.rpm_stable:
            elev_valid = False
            elev_reason = "elevated frame RPM not settled"  # wiki: delta-relations/08

        trusted = low_valid and elev_valid
        if trusted:
            reason = "both frames valid"
        elif not low_valid:
            reason = f"low frame rejected — {low_reason}"
        else:
            reason = f"elevated frame rejected — {elev_reason}"

        return DeltaValidityVerdict(
            low_frame_valid=low_valid,
            elevated_frame_valid=elev_valid,
            trusted=trusted,
            reason=reason,
        )

    @staticmethod
    def _frame_gas_valid(
        hc: int | None,
        co: float | None,
        co2: float | None,
        o2: float | None,
        nox: int | None,
    ) -> tuple[bool, str]:
        """vsum 14-18 % + dilution CO+CO2 > 6 % (delta-relations/08).

        When the gas channel is absent on a frame, validity is not gated on gas
        (the frame may be trim-only) — return valid so a trim-only delta can run.
        """
        if co is None or co2 is None or o2 is None:
            return True, "gas channel absent — not gas-gated"
        # HC ppm → % volume (1 % = 10 000 ppm); NOx ppm → %.
        # wiki: delta-relations/08 — validity vsum is computed in % volume.
        hc_pct = (hc or 0) / 10000.0
        nox_pct = (nox or 0) / 10000.0
        vsum = hc_pct + co + co2 + o2 + nox_pct
        if vsum < DeltaEngine._VSUM_MIN:
            return False, f"vsum {vsum:.1f} < {DeltaEngine._VSUM_MIN} (dilution)"
        if vsum > DeltaEngine._VSUM_MAX:
            return False, f"vsum {vsum:.1f} > {DeltaEngine._VSUM_MAX} (near-ambient/exhaust leak)"
        if (co + co2) <= DeltaEngine._DILUTION_COCO2_MIN:
            return False, f"CO+CO2 {co + co2:.1f} ≤ {DeltaEngine._DILUTION_COCO2_MIN} (dilution)"
        return True, "valid"

    # ------------------------------------------------------------------
    # Step 3a — ΔTrim (delta-relations/01-05); validated @ STRESS_IDLE
    # ------------------------------------------------------------------

    @staticmethod
    def _delta_trim(
        request: OrchestratorInboundRequest,
        frame: SecondOperatingPointFrame,
        arch: ArchitectureGateVerdict,
    ) -> DeltaTrimResult:
        """ΔTrim = TotalTrim(elevated) − TotalTrim(low), architecture-gated."""
        # Per-signal band: ΔTrim is only defined at STRESS_IDLE (3500-4500).
        if frame.rpm_state_bucket != DeltaEngine._TRIM_BAND:
            return DeltaTrimResult(profile="ABSTAIN")  # wiki: SWEEP_MANIFEST §7 — band mismatch

        low_total = DeltaEngine._total_trim(
            request.obd_live_data.total_trim_correction_delta
            if request.obd_live_data is not None
            else None,
            request.obd_live_data.shrtft1 if request.obd_live_data is not None else None,
            request.obd_live_data.longft1 if request.obd_live_data is not None else None,
        )
        elev_total = DeltaEngine._total_trim(
            frame.total_trim_correction_delta, frame.shrtft1, frame.longft1
        )
        if low_total is None or elev_total is None:
            return DeltaTrimResult(profile="NONE")  # trim channel absent on a frame

        delta = elev_total - low_total

        # Architecture gate (delta-relations/06) — applied BEFORE profile match.
        if arch.trim_nulled:
            return DeltaTrimResult(
                delta_total_trim=delta,
                low_total_trim=low_total,
                elevated_total_trim=elev_total,
                sign="NULL",
                profile="NONE",  # route to IAC/MAP-at-idle, not a leak profile
            )
        if arch.trim_inverted:
            delta = -delta  # post-turbo leak inverts the sign

        sign = DeltaEngine._sign(delta)
        profile = DeltaEngine._match_trim_profile(delta, low_total, elev_total)
        return DeltaTrimResult(
            delta_total_trim=delta,
            low_total_trim=low_total,
            elevated_total_trim=elev_total,
            sign=sign,
            profile=profile,
        )

    @staticmethod
    def _match_trim_profile(
        delta: float, low_total: float, elev_total: float
    ) -> TrimProfileLit:
        """Classify ΔTrim by sign + low-idle starting band (delta-relations/02-05)."""
        if delta <= DeltaEngine._DTRIM_LEAK_MAX:
            # Negative ΔTrim: vacuum leak (starts high +) vs backpressure (starts ≈ 0).
            if low_total >= DeltaEngine._VACLEAK_LOW_MIN:
                return "VACUUM_LEAK"  # wiki: delta-relations/02
            if (
                abs(low_total) <= DeltaEngine._BACKPRESS_LOW_ABS
                and elev_total <= DeltaEngine._BACKPRESS_ELEV_MAX
            ):
                return "EXHAUST_BACKPRESSURE"  # wiki: delta-relations/05
            return "ABSTAIN"  # negative Δ but neither low-idle band matches
        if delta >= DeltaEngine._DTRIM_SUPPLY_MIN:
            # Positive ΔTrim: fuel starvation vs MAF under-report — separated by
            # low-idle starting band; overlapping (+5..+8) is ambiguous → ABSTAIN.
            if low_total <= DeltaEngine._STARVE_LOW_MAX:
                return "FUEL_STARVATION"  # wiki: delta-relations/03
            if low_total <= DeltaEngine._MAF_LOW_MAX:
                return "MAF_UNDERREPORT"  # wiki: delta-relations/04
            return "ABSTAIN"
        return "NONE"  # within noise band — no diagnostic delta

    @staticmethod
    def _total_trim(
        total: float | None, shrtft: float | None, longft: float | None
    ) -> float | None:
        """Total trim = STFT + LTFT, falling back to the pre-aggregated total (chunk 01)."""
        if shrtft is not None and longft is not None:
            return shrtft + longft
        return total

    # ------------------------------------------------------------------
    # Step 3b — Δgas (delta-relations/07); validated @ REGULATORY_HIGH_IDLE
    # ------------------------------------------------------------------

    @staticmethod
    def _delta_gas(
        request: OrchestratorInboundRequest,
        frame: SecondOperatingPointFrame,
    ) -> DeltaGasResult:
        """Δgas = {ΔHC, ΔCO, ΔCO₂, ΔO₂, Δλ, ΔNOx} across the step (chunk 07)."""
        if frame.rpm_state_bucket != DeltaEngine._GAS_BAND:
            return DeltaGasResult(gas_profile="ABSTAIN")  # wiki: SWEEP_MANIFEST §7 — band mismatch

        gas = request.gas_lab_output
        d_hc = DeltaEngine._isub(frame.gas_hc, gas.gas_hc)
        d_co = DeltaEngine._fsub(frame.gas_co, gas.gas_co)
        d_co2 = DeltaEngine._fsub(frame.gas_co2, gas.gas_co2)
        d_o2 = DeltaEngine._fsub(frame.gas_o2, gas.gas_o2)
        d_nox = DeltaEngine._isub(frame.gas_nox, gas.gas_nox)
        d_lambda = DeltaEngine._fsub(frame.lambda_chem, gas.lambda_chem)

        profile = DeltaEngine._match_gas_profile(
            d_hc, d_nox, d_lambda, frame.gas_o2
        )
        return DeltaGasResult(
            d_hc=d_hc,
            d_co=d_co,
            d_co2=d_co2,
            d_o2=d_o2,
            d_lambda=d_lambda,
            d_nox=d_nox,
            gas_profile=profile,
        )

    @staticmethod
    def _match_gas_profile(
        d_hc: int | None,
        d_nox: int | None,
        d_lambda: float | None,
        elev_o2: float | None,
    ) -> GasProfileLit:
        """Classify Δgas by the sign of the change across the step (chunk 07).

        Worn rings (oil burn intensifies) and worn valve seals (oil induction
        clears) both read "elevated HC" at idle — only the sign of ΔHC resolves them.
        """
        if d_hc is not None:
            if d_hc >= DeltaEngine._DHC_RINGS_MIN:
                # Rising HC: flat-cam breathing misfire pushes O₂ up too; rings do not.
                if elev_o2 is not None and elev_o2 >= DeltaEngine._FLATCAM_ELEV_O2_MIN:
                    return "FLAT_CAM"  # wiki: delta-relations/07
                return "WORN_PISTON_RINGS"  # wiki: delta-relations/07
            if d_hc <= DeltaEngine._DHC_VALVE_MAX:
                return "WORN_VALVE_SEALS"  # wiki: delta-relations/07
        if d_nox is not None and d_nox >= DeltaEngine._DNOX_EGR_MIN:
            return "EGR_STUCK_CLOSED"  # wiki: delta-relations/07
        if d_lambda is not None and d_lambda >= DeltaEngine._DLAMBDA_RICH_MIN:
            return "RICH_ATTENUATING"  # wiki: delta-relations/07
        return "NONE"

    # ------------------------------------------------------------------
    # Step 3c — ΔO₂ (SWEEP_MANIFEST §7) — named-only passthrough
    # ------------------------------------------------------------------

    @staticmethod
    def _delta_o2(
        request: OrchestratorInboundRequest,
        frame: SecondOperatingPointFrame,
    ) -> DeltaO2Result:
        """Subtraction-only passthrough; never sets a profile (not yet quantified)."""
        return DeltaO2Result(
            d_switch_freq=None,  # low-frame O₂ feeders not carried on the request yet
            d_voltage_bias=None,
            d_downstream_response=None,
        )

    # ------------------------------------------------------------------
    # Step 4 — assemble (ΔTrim precedence, Δgas corroborates)
    # ------------------------------------------------------------------

    # Profile → existing FaultFamilyLit (response.py:34) — never invents a family.
    _TRIM_FAMILY: dict[str, str] = {
        "VACUUM_LEAK": "vacuum_leak",
        "FUEL_STARVATION": "lean_condition",
        "MAF_UNDERREPORT": "lean_condition",
        "EXHAUST_BACKPRESSURE": "exhaust_leak",
    }
    _GAS_FAMILY: dict[str, str] = {
        "WORN_PISTON_RINGS": "mechanical_wear",
        "WORN_VALVE_SEALS": "mechanical_wear",
        "FLAT_CAM": "cam_timing",
        "EGR_STUCK_CLOSED": "lean_condition",
    }

    @staticmethod
    def _assemble(
        arch: ArchitectureGateVerdict,
        validity: DeltaValidityVerdict,
        trim: DeltaTrimResult,
        gas: DeltaGasResult,
        o2: DeltaO2Result,
    ) -> DeltaSignature:
        """ΔTrim profile takes precedence; Δgas corroborates / supplies a family if trim is silent."""
        target: str | None = None
        primary = "NONE"

        if trim.profile in DeltaEngine._TRIM_FAMILY:
            target = DeltaEngine._TRIM_FAMILY[trim.profile]
            primary = trim.profile
        elif gas.gas_profile in DeltaEngine._GAS_FAMILY:
            target = DeltaEngine._GAS_FAMILY[gas.gas_profile]
            primary = gas.gas_profile

        if target is None:
            confidence = 0.0
        elif arch.air_metering_strategy is None and arch.induction_type is None:
            # Architecture unknown — cap so an un-gated trim profile cannot win outright.
            confidence = DeltaEngine._UNGATED_ARCH_CONF  # wiki: delta-relations/06 risk
        else:
            confidence = DeltaEngine._DELTA_PRIMARY_CONF  # wiki: delta-relations/01

        return DeltaSignature(
            present=True,
            degradation_mode="FULL_FUSION",
            validity=validity,
            architecture=arch,
            trim=trim,
            gas=gas,
            o2=o2,
            primary_profile=primary,
            target_fault_family=target,
            confidence=confidence,
        )

    # ------------------------------------------------------------------
    # Subtraction helpers (None-safe — only difference when both frames carry the channel)
    # ------------------------------------------------------------------

    @staticmethod
    def _isub(elevated: int | None, low: int | None) -> int | None:
        if elevated is None or low is None:
            return None
        return elevated - low

    @staticmethod
    def _fsub(elevated: float | None, low: float | None) -> float | None:
        if elevated is None or low is None:
            return None
        return elevated - low

    @staticmethod
    def _sign(delta: float) -> TrimSignLit:
        if delta >= DeltaEngine._DTRIM_SUPPLY_MIN:
            return "POSITIVE"
        if delta <= DeltaEngine._DTRIM_LEAK_MAX:
            return "NEGATIVE"
        return "FLAT"
