"""
core/vin/extractors/__init__.py
================================
Registers all brand extractors with vininfo's WMI table at import time.

IMPORTANT: vininfo's WMI dict stores Brand *instances*, not classes.
The Vin constructor calls assembler.brands (a @property on an instance)
to iterate over available extractors. Storing a class instead of an
instance causes "TypeError: 'property' object is not iterable".
"""

from __future__ import annotations


def register_all_extractors() -> None:
    """Patch vininfo's WMI registry with our custom extractors."""
    try:
        from vininfo.brands import Brand
        from vininfo.dicts.wmi import WMI
    except ImportError:
        return

    from .vw import AudiDetails, SEATDetails, SkodaDetails, VWGroupDetails
    _register_vw_group(Brand, WMI, VWGroupDetails, AudiDetails, SkodaDetails, SEATDetails)

    # Wave 2 extractors
    from .bmw import BMWDetails, MiniDetails
    from .fiat import FiatDetails
    from .ford_eu import FordEuDetails
    from .hyundai_kia import HyundaiDetails, KiaKNADetails, KiaU5YDetails
    from .mercedes import MercedesDetails, MercedesOlderDetails
    from .psa import CitroenDetails, PeugeotDetails
    from .toyota_eu import ToyotaEuDetails

    _register_wave2(
        Brand, WMI,
        BMWDetails, MiniDetails,
        MercedesDetails, MercedesOlderDetails,
        FordEuDetails,
        PeugeotDetails, CitroenDetails,
        ToyotaEuDetails,
        HyundaiDetails, KiaU5YDetails, KiaKNADetails,
        FiatDetails,
    )


def _make_brand(Brand, extractor, manufacturer: str, year_position=None, uses_sae=False):
    """
    Create a Brand subclass and return an *instance* of it.
    WMI values must be instances (vininfo calls instance.brands, not cls.brands).
    """
    cls = type(
        f'_{manufacturer.replace(" ", "")}Brand',
        (Brand,),
        {
            'extractor': extractor,
            'year_position': year_position,   # None = don't decode year from VIN
            'uses_sae_checkdigit': uses_sae,
        }
    )
    return cls(manufacturer)


def _register_wave2(
    Brand, WMI,
    BMWDetails, MiniDetails,
    MercedesDetails, MercedesOlderDetails,
    FordEuDetails,
    PeugeotDetails, CitroenDetails,
    ToyotaEuDetails,
    HyundaiDetails, KiaU5YDetails, KiaKNADetails,
    FiatDetails,
) -> None:
    """Register Wave 2 brand extractors with vininfo's WMI table."""

    wave2_wmis = {
        # BMW Group
        'WBA': (BMWDetails,           'BMW'),
        'WBY': (BMWDetails,           'BMW i'),
        'WBS': (BMWDetails,           'BMW M'),
        'WMW': (MiniDetails,          'Mini'),
        # Mercedes-Benz
        'WDD': (MercedesDetails,      'Mercedes-Benz'),
        'WDC': (MercedesDetails,      'Mercedes-Benz'),
        'WDB': (MercedesOlderDetails, 'Mercedes-Benz'),
        # Ford Europe
        'WF0': (FordEuDetails,        'Ford Europe'),
        # PSA Group
        'VF3': (PeugeotDetails,       'Peugeot'),
        'VF7': (CitroenDetails,       'Citroen'),
        # Toyota EU
        'SB1': (ToyotaEuDetails,      'Toyota'),
        'JTD': (ToyotaEuDetails,      'Toyota'),
        'VNK': (ToyotaEuDetails,      'Toyota'),
        # Hyundai-Kia
        'TMA': (HyundaiDetails,       'Hyundai'),
        'KMH': (HyundaiDetails,       'Hyundai'),
        'U5Y': (KiaU5YDetails,        'Kia'),
        'KNA': (KiaKNADetails,        'Kia'),
        # Fiat
        'ZFA': (FiatDetails,          'Fiat'),
    }

    for wmi_code, (extractor, mfr_name) in wave2_wmis.items():
        existing = WMI.get(wmi_code)
        if existing is None or isinstance(existing, str):
            WMI[wmi_code] = _make_brand(Brand, extractor, mfr_name)


def _register_vw_group(Brand, WMI, VWGroupDetails, AudiDetails, SkodaDetails, SEATDetails) -> None:
    """Register VW Group WMI prefixes with correct Brand instances."""

    # Map: WMI code → (extractor class, display manufacturer string)
    vw_wmis = {
        'WVW': (VWGroupDetails, 'Volkswagen'),
        'WV1': (VWGroupDetails, 'Volkswagen Commercial'),
        'WV2': (VWGroupDetails, 'Volkswagen Commercial'),
        'WAU': (AudiDetails,   'Audi'),
        'TMB': (SkodaDetails,  'Škoda'),
        'VSS': (SEATDetails,   'SEAT'),
    }

    for wmi_code, (extractor, mfr_name) in vw_wmis.items():
        existing = WMI.get(wmi_code)
        # Only overwrite plain-string entries (no extractor) or missing entries.
        # Never clobber an entry that already has a real VinDetails extractor.
        if existing is None or isinstance(existing, str):
            WMI[wmi_code] = _make_brand(Brand, extractor, mfr_name)
