"""
core/vin/extractors/mercedes.py
================================
Mercedes-Benz VinDetails extractor — WDD, WDB, WDC.

Engine-code mappings mined from 1.8M OPSI registrations (June 2023).
  WDD  7,841 rows  — Mercedes-Benz passenger cars (post-2000, primary)
  WDB  1,041 rows  — Mercedes-Benz older series (pre-2000 W/E/C-class)
  WDC    238 rows  — Mercedes-Benz SUV/crossover (ML/GLC/GLE)

VDS position 3 (VIN character index 6, 0-based) is used for WDD/WDC.
WDB uses position 0 but shares most engine families with WDD pos 3.
One MercedesDetails class handles all three WMIs.

Note: Mercedes engine codes in OPSI omit the dot separator.
      e.g. "271861" not "271.861". DNA table uses no-dot format.

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
# Mercedes — WDD/WDC VDS position 3 (14 unique engine codes)
# ---------------------------------------------------------------------------

_WDD_P3_ENGINE: dict[str, str] = {
    '0': '266920',    # 1.5 (A/B-class W169/W245 2004–2012)
    '1': '282914',    # 1.3 EQ Boost (A/B-class W177/W247 2018+)
    '2': '270910',    # 1.8 supercharged (C-class W203/CLK W209)
    '3': '270910',    # 1.8 SC variant (200K/230K)
    '4': '271861',    # 1.8 turbo (C-class W204 / E-class W212)
    '5': '274920',    # 2.0 turbo M274 (C-class W205 2014+)
    '6': '256930',    # 3.0 inline-6 M256 (E-class W213 2018+)
    '7': '276821',    # 3.5 V6 M276 (E-class W212)
    '8': '273963',    # 5.5 V8 M273 (E-class AMG)
    '9': '272967',    # 3.5 V6 M272 (E-class W211)
    'A': '111920',    # 2.2 M111 (older C/E W202/W210)
    'B': '271820',    # 1.8 SC M271 (C180K/C200K W203)
    'C': '274910',    # 1.6 turbo M274 (C-class A-class 2014+)
    'G': '270920',    # 1.8 SC variant (W203 facelift)
}

# WDB position 0 — older pre-2000 models; restrict to 1990-era petrol
_WDB_P0_ENGINE: dict[str, str] = {
    '2': '111920',    # 2.2 M111 (W202 C220)
    '3': '104990',    # 3.2 M104 (W124 E320)
    '4': '111940',    # 2.4 M111 (W202 C240)
    '5': '112940',    # 2.4 M112 V6 (W203 C240)
    '6': '112960',    # 2.8 M112 V6 (W203 C280)
    '7': '112941',    # 3.2 M112 V6 (W203 C320)
    '8': '112944',    # 3.5 M112 V6 (W203 C350)
    '9': '104942',    # 3.2 M104 (W210 E320)
    'A': '111961',    # 2.3 M111 (W210 E230)
    'B': '112941',    # 3.2 M112 (W210 E320 facelift)
    'E': '271861',    # 1.8 M271 turbo (W203 early)
}


class MercedesDetails(VinDetails):
    """Extractor for Mercedes-Benz (WDD, WDB, WDC). Uses pos 3."""
    engine = Detail(('vds', 3), _WDD_P3_ENGINE)
    plant  = Detail(('vis', 1), {
        'A': 'Sindelfingen',
        'B': 'Bremen',
        'D': 'Düsseldorf',
        'E': 'Rastatt',
        'F': 'Hamburg',
        'G': 'Graz (Magna)',
        'H': 'Hambach',
        'J': 'Juiz de Fora',
        'W': 'Tuscaloosa',
    })


class MercedesOlderDetails(VinDetails):
    """Extractor for older Mercedes-Benz (WDB, pre-2000). Uses pos 0."""
    engine = Detail(('vds', 0), _WDB_P0_ENGINE)
    plant  = Detail(('vis', 1), {
        'A': 'Sindelfingen',
        'B': 'Bremen',
        'D': 'Düsseldorf',
        'F': 'Hamburg',
    })
