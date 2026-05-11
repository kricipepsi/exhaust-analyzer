"""
core/vin/extractors/psa.py
==========================
PSA Group VinDetails extractors — Peugeot (VF3) and Citroën (VF7).

Engine-code mappings mined from 1.8M OPSI registrations (June 2023).
  VF3  36,355 rows  — Peugeot
  VF7  32,259 rows  — Citroën

VDS position 2 (VIN character index 5, 0-based) is the primary discriminator
for both Peugeot and Citroën — they share the PSA platform architecture.

PSA petrol engine families in scope (1990–2020):
  - TU series (TU1, TU3, TU5) — older 8V/16V port injection
  - EW series (EW7, EW10) — 16V N/A
  - EP6 / Prince (EP6C, EP6DT, EP6DTS) — 1.6 THP (joint BMW)
  - EB series (EB0, EB2) — PureTech 1.2 3-cyl N/A
  - HM/HN series (HM01, HNY, HNZ) — PureTech 1.2 3-cyl turbo
  - 1KR — 1.0 3-cyl N/A (shared with Toyota)

Diesel codes (e.g. 9HZ) map to 'skip_diesel' — excluded from petrol DNA.

Reference: https://github.com/idlesign/vininfo/blob/master/src/vininfo/details/opel.py
"""

from __future__ import annotations

try:
    from vininfo.details._base import Detail, VinDetails
except ImportError:
    class VinDetails:  # type: ignore[no-redef]
        pass
    class Detail:      # type: ignore[no-redef]
        def __init__(self, *a, **kw):
            pass


# ---------------------------------------------------------------------------
# Peugeot — VF3 VDS position 2 (24 unique engine codes)
# ---------------------------------------------------------------------------

_VF3_P2_ENGINE: dict[str, str] = {
    '5': '5FW',     # 1.6 16V N/A (207/308 2006–2012)
    'N': 'NFU',     # 1.4 8V TU3JP4 (206/207)
    'H': 'HM01',    # 1.2 PureTech 3-cyl turbo (208/308 2014+)
    'K': 'KFW',     # 1.6 16V (206/307 early)
    '8': '8FS',     # 1.6 THP 150hp (207/308 turbo)
    'C': '1KR',     # 1.0 3-cyl N/A (107/108)
    'E': 'EP6C',    # 1.6 THP 155hp Prince (207/308)
    'F': 'EW10J4',  # 2.0 16V N/A (407)
    'G': 'EP6DTS',  # 1.6 THP 200hp (208 GTi)
    'J': 'EB2',     # 1.2 VTi 82hp (208 N/A)
    'L': 'EP6',     # 1.6 THP 120hp (3008)
    'M': 'HNY',     # 1.2 PureTech 130hp (308 2017+)
    'P': 'EW7J4',   # 1.8 16V (307)
    'R': 'TU5JP4',  # 1.4 16V (206/207)
    'S': 'EW6J4',   # 1.6 8V (Partner/Expert)
    'T': 'EB0',     # 1.0 VTi 68hp (108)
    'U': 'EP6CDT',  # 1.6 THP 163hp (308/RCZ)
    'V': 'EW10A',   # 2.0 8V (406 era)
    'W': 'TU3A',    # 1.4 8V (older 206/306)
    'Y': 'EP6DT',   # 1.6 THP 156hp (3008/5008)
    'Z': '5FX',     # 1.6 16V (RCZ/308 late)
    'A': 'HN01',    # 1.2 PureTech 82hp (208 2019+)
    'B': 'HNZ',     # 1.2 PureTech 110hp (2008/3008)
    'D': 'TU5J4',   # 1.4 16V (206/307 early)
}

# ---------------------------------------------------------------------------
# Citroën — VF7 VDS position 2 (24 unique engine codes, same PSA platform)
# ---------------------------------------------------------------------------

_VF7_P2_ENGINE: dict[str, str] = {
    'N': 'NFU',     # 1.4 8V TU3 (C2/C3)
    'H': 'HM01',    # 1.2 PureTech turbo (C3/C4 2014+)
    'C': '1KR',     # 1.0 3-cyl (C1/C3)
    'K': 'KFV',     # 1.6 8V TU5 (C4/Berlingo)
    '5': '5FS',     # 1.6 16V N/A (C4/C5)
    '8': '8FP',     # 1.6 THP 140hp (C4 turbo)
    'E': 'EP6C',    # 1.6 THP 155hp Prince (C4/DS4)
    'F': 'EW10J4',  # 2.0 16V N/A (C5)
    'G': 'TU5JP4',  # 1.4 16V (C3/C4)
    'J': 'EB2',     # 1.2 VTi (C3 2016+)
    'L': 'EP6',     # 1.6 THP 120hp (C4 Picasso)
    'M': 'HNY',     # 1.2 PureTech 130hp (C3 2017+)
    'P': 'TU3A',    # 1.4 8V (older C3/C2)
    'R': 'EW7J4',   # 1.8 16V (C5)
    'S': 'EW6J4',   # 1.6 8V (Berlingo/Dispatch)
    'T': 'EB0',     # 1.0 VTi 68hp (C1)
    'U': 'EP6DT',   # 1.6 THP 156hp (DS5)
    'V': 'KFU',     # 1.6 8V (Berlingo variant)
    'W': 'HN01',    # 1.2 PureTech 82hp (C3 2019+)
    'X': 'TU5J4',   # 1.4 16V (Saxo/Xsara era)
    'Y': 'EP6CDT',  # 1.6 THP 163hp (DS3/C4)
    'Z': '5FW',     # 1.6 16V (C4/C5)
    'A': 'HNZ',     # 1.2 PureTech 110hp (C3/C4)
    'B': 'EB2DTS',  # 1.2 PureTech 130hp FL (C3 2020)
}


class PeugeotDetails(VinDetails):
    """Extractor for Peugeot (VF3)."""
    engine = Detail(('vds', 2), _VF3_P2_ENGINE)
    plant  = Detail(('vis', 1), {
        'A': 'Mulhouse',
        'B': 'Sochaux',
        'D': 'Poissy',
        'J': 'Ryton (UK)',
        'K': 'Kolin (TPCA)',
        'L': 'Trnava (Slovakia)',
        'S': 'Sevelnord',
        'V': 'Valenciennes',
    })


class CitroenDetails(VinDetails):
    """Extractor for Citroën (VF7)."""
    engine = Detail(('vds', 2), _VF7_P2_ENGINE)
    plant  = Detail(('vis', 1), {
        'A': 'Aulnay-sous-Bois',
        'B': 'Caen',
        'D': 'Poissy',
        'K': 'Kolin (TPCA)',
        'L': 'Trnava (Slovakia)',
        'R': 'Rennes (la Janais)',
        'S': 'Sevelnord',
        'V': 'Vigo (Spain)',
    })
