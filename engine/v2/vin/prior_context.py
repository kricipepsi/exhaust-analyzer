"""
prior_context.py — VIN-derived engine context for advanced diagnostics.

PriorContext is passed as an optional last argument to run_advanced_diagnostics().
When context=None (the default) the engine produces byte-identical output to the
pre-VIN version — fully additive, zero regression risk.

EngineDNA is the offline Layer-C product of the VIN resolver (core/vin/__init__.py).
It is also accepted as a manually-supplied dict via the UI engine code selector.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal


@dataclass(frozen=True)
class EngineDNA:
    """
    Offline engine specification resolved from VIN or manual entry.

    Fields
    ------
    source          : 'vininfo+dna' | 'wmi_only' | 'manual' | 'unknown'
    confidence      : 'high' = DNA hit, 'partial' = WMI only, 'none' = failed
    make            : Manufacturer string, e.g. 'VW Group', 'BMW'
    engine_code     : Alphanumeric engine code, e.g. 'CAVD', 'N20B20', 'M271'
    year            : Exact model year if VIN encodes it (EU brands often don't)
    year_range      : (year_min, year_max) from DNA row when exact year unknown
    displacement_l  : Engine swept volume in litres
    cylinders       : Cylinder count
    induction       : 'na' | 'turbo' | 'super' | 'twincharged'
    intercooler     : True if charge-air cooler fitted; derived from TecDoc or turbo+year rule
    injection       : 'mpfi' | 'gdi' | 'tsi' | 'unknown'
    fuel_type       : 'petrol' | 'lpg' | 'cng' | 'flex'
    o2_arch         : 'narrowband' | 'wideband' | 'unknown'
    spec_idle_gps   : Expected idle exhaust mass-flow (g/s) — default disp_l x 2.0
    known_issues    : Curated high-prevalence faults from DNA table
    common_models   : Representative model/trim names for display
    """
    source: Literal['vininfo+dna', 'wmi_only', 'manual', 'unknown'] = 'unknown'
    confidence: Literal['high', 'partial', 'none'] = 'none'

    make: str | None = None
    engine_code: str | None = None
    year: int | None = None
    year_range: tuple | None = None

    displacement_l: float | None = None
    cylinders: int | None = None
    induction: Literal['na', 'turbo', 'super', 'twincharged'] | None = None
    intercooler: bool | None = None
    injection: Literal['mpfi', 'gdi', 'tsi', 'unknown'] | None = None
    fuel_type: Literal['petrol', 'lpg', 'cng', 'flex'] | None = 'petrol'
    o2_arch: Literal['narrowband', 'wideband', 'unknown'] | None = 'unknown'
    spec_idle_gps: float | None = None
    known_issues: list = field(default_factory=list)
    common_models: list = field(default_factory=list)

    def __post_init__(self) -> None:
        # Auto-compute spec_idle_gps if not supplied but displacement is known
        if self.spec_idle_gps is None and self.displacement_l is not None:
            # Frozen dataclass — use object.__setattr__ to bypass the freeze
            object.__setattr__(self, 'spec_idle_gps', round(self.displacement_l * 2.0, 2))

    @classmethod
    def from_dna_row(cls, row: dict, source: str = 'vininfo+dna') -> EngineDNA:
        """Build an EngineDNA from a raw data/engine_dna.json row dict."""
        yr_min = row.get('year_min')
        yr_max = row.get('year_max')
        yr_range = (yr_min, yr_max) if yr_min and yr_max else None
        return cls(
            source=source,
            confidence='high',
            make=row.get('manufacturer'),
            engine_code=row.get('engine_code'),
            year=None,  # exact year comes from VIS if available
            year_range=yr_range,
            displacement_l=row.get('displacement_l'),
            cylinders=row.get('cylinders'),
            induction=row.get('induction'),
            intercooler=row.get('intercooler'),
            injection=row.get('injection'),
            fuel_type=row.get('fuel_type', 'petrol'),
            o2_arch=row.get('o2_arch', 'unknown'),
            spec_idle_gps=row.get('spec_idle_gps'),
            known_issues=row.get('known_issues', []),
            common_models=row.get('common_models', []),
        )

    @classmethod
    def unknown(cls) -> EngineDNA:
        """Sentinel returned when VIN cannot be resolved at all."""
        return cls(source='unknown', confidence='none')

    @classmethod
    def partial(cls, make: str, year: int | None = None) -> EngineDNA:
        """Returned when WMI resolves manufacturer but VDS engine code is absent."""
        return cls(source='wmi_only', confidence='partial', make=make, year=year)


@dataclass(frozen=True)
class PriorContext:
    """
    Optional diagnostic context derived from VIN + user-supplied runtime fields.

    All fields have sensible defaults so callers only need to populate
    what they know.  When context=None is passed to run_advanced_diagnostics()
    none of this is consulted and the function behaves identically to v1.

    Fields
    ------
    dna             : EngineDNA from VIN resolver or manual entry
    engine_temp     : 'cold' | 'warm' — inhibits truth-gate + catalyst mask when cold
    codes_cleared   : True if DTCs were recently cleared — disables LTFT in analysis
    altitude_band   : 'sea_level' | 'mid' | 'high_alt' — applies CO offset
    mileage_bracket : 'low' | 'mid' | 'high' — boosts ring/seal confidence at high miles
    oil_consumption : 'normal' | 'high' — boosts ring confidence
    symptoms        : List of symptom keys from the multiselect (see symptom_weights.py)
    """
    dna: EngineDNA = field(default_factory=EngineDNA.unknown)
    engine_temp: Literal['cold', 'warm'] = 'warm'
    codes_cleared: bool = False
    altitude_band: Literal['sea_level', 'mid', 'high_alt'] = 'sea_level'
    mileage_bracket: Literal['low', 'mid', 'high'] = 'mid'
    oil_consumption: Literal['normal', 'high'] = 'normal'
    symptoms: list = field(default_factory=list)
