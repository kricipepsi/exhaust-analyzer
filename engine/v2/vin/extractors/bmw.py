"""
core/vin/extractors/bmw.py
==========================
BMW Group VinDetails extractors — BMW and Mini.

Engine-code mappings mined from 1.8M OPSI registrations (June 2023).
  WBA  8,914 rows  — BMW passenger cars (primary)
  WBY    391 rows  — BMW i-series electric (not petrol — rare hits)
  WBS    129 rows  — BMW M GmbH
  WMW  2,000 rows  — Mini (Oxford)

VDS position 0 (VIN character index 3, 0-based) is the primary discriminator
for BMW (WBA). Mini uses VDS position 1 (character index 4).

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
# BMW — WBA/WBS VDS position 0 (20 unique engine codes)
# ---------------------------------------------------------------------------

_WBA_P0_ENGINE: dict[str, str] = {
    'J': 'B58B30A',   # 3.0 inline-6 turbo (2016+)
    '2': 'B38A15A',   # 1.5 3-cyl turbo (F20/F30)
    '8': 'B38B15A',   # 1.5 3-cyl turbo (variant)
    '1': 'N13B16A',   # 1.6 turbo (F20 2011–2015)
    'A': '194E1',     # N52B30 2.5/3.0 N/A (E90 era)
    'C': '164E2',     # N46B20 2.0 N/A (E46/E90)
    'K': 'N52B25A',   # 2.5 N/A (E90 325i)
    'N': 'N55B30A',   # 3.0 turbo (F30 2009–2016)
    'P': 'N20B20A',   # 2.0 turbo (F30 2012–2016)
    'R': 'B48A20A',   # 2.0 turbo (F30 2015+)
    'S': 'B48B20A',   # 2.0 turbo variant (G20)
    'T': 'N46B20B',   # 2.0 N/A (E90 era)
    'U': 'N52B30A',   # 3.0 N/A (E90 330i)
    'V': 'N43B20A',   # 2.0 DI N/A (E90 318i)
    'W': 'N53B30A',   # 3.0 DI N/A (E90 330i late)
    'X': 'N42B18A',   # 1.8 N/A (E46)
    'Y': 'N45B16A',   # 1.6 N/A (E87 116i)
    'Z': 'N45B20A',   # 2.0 N/A (E87 120i)
    'F': 'N20B16A',   # 1.6 turbo (rare)
    'G': 'N54B30A',   # 3.0 twin-turbo (E90 335i)
    'H': 'N43B16A',   # 1.6 DI (E87 116i late)
}

# ---------------------------------------------------------------------------
# Mini — WMW VDS position 1 (12 unique engine codes)
# ---------------------------------------------------------------------------

_WMW_P1_ENGINE: dict[str, str] = {
    'F': 'N12B16A',   # 1.6 N/A (R56 One 2006–2013)
    'U': 'N16B16A',   # 1.6 turbo (R56 JCW)
    'X': 'N18B16A',   # 1.6 turbo (R56 S 2010+)
    'R': 'N16B16A',   # 1.6 turbo (variant)
    'M': 'B38A15A',   # 1.5 3-cyl (F56 2014+)
    'A': 'W10B16A',   # 1.6 N/A (R50 2001–2006)
    'B': 'W11B16A',   # 1.6 supercharged (R53 Cooper S)
    'D': 'N14B16A',   # 1.6 turbo (R56 S early 2007–2010)
    'E': 'B46A20A',   # 2.0 turbo (F60 Countryman)
    'G': 'B48A20A',   # 2.0 turbo (F56 S 2014+)
    'H': 'B38B15A',   # 1.5 3-cyl variant
    'N': 'N12B16C',   # 1.6 N/A late (R56 facelift)
}


class BMWDetails(VinDetails):
    """Extractor for BMW passenger cars (WBA, WBS)."""
    engine = Detail(('vds', 0), _WBA_P0_ENGINE)
    plant  = Detail(('vis', 1), {
        'A': 'Munich',
        'B': 'Munich (variant)',
        'E': 'Regensburg',
        'R': 'Rosslyn (South Africa)',
        'V': 'Leipzig',
        'G': 'Graz (Magna Steyr)',
    })


class MiniDetails(VinDetails):
    """Extractor for Mini (WMW)."""
    engine = Detail(('vds', 1), _WMW_P1_ENGINE)
    plant  = Detail(('vis', 1), {
        'A': 'Oxford',
        'B': 'Graz (Magna Steyr)',
    })
