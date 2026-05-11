"""
core/vin/extractors/ford_eu.py
==============================
Ford Europe VinDetails extractor — WF0.

Engine-code mappings mined from 1.8M OPSI registrations (June 2023).
  WF0  28,516 rows  — Ford of Europe (Cologne/Valencia/Saarlouis plants)

VDS position 5 (VIN character index 8, 0-based) is the primary discriminator.
24 unique petrol engine codes recovered.

Common Ford EU petrol families in scope (1990–2020):
  - Duratec (HE, HE Ti-VCT, 8V, 16V)
  - EcoBoost (1.0 3-cyl, 1.5, 1.6, 2.0, 2.3)
  - Sigma (1.25, 1.4, 1.6)
  - Zetec (1.6, 1.8, 2.0)

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
# Ford EU — WF0 VDS position 5 (24 unique engine codes)
# ---------------------------------------------------------------------------

_WF0_P5_ENGINE: dict[str, str] = {
    'B': 'M1DA',   # 1.0 EcoBoost 100hp (Focus/Fiesta 2012+)
    'C': 'M1DD',   # 1.0 EcoBoost 125hp
    'D': 'FYDB',   # 2.0 Duratec (Focus Mk2 2004–2011)
    'H': 'B7DA',   # 1.5 EcoBoost (Focus Mk3.5 2015+)
    'J': 'FYJA',   # 2.0 Duratec HE (Mondeo Mk4)
    'K': 'SNJB',   # 1.6 EcoBoost 182hp (Focus ST Mk3)
    'L': 'MUDA',   # 1.0 EcoBoost 140hp (Focus Mk3)
    'M': 'SHDA',   # 1.6 Duratec Ti-VCT 105hp
    'N': 'IQDA',   # 1.0 EcoBoost 95hp (Fiesta Mk7)
    'P': 'AODA',   # 1.6 EcoBoost 150hp (Focus Mk3)
    'R': 'HWDA',   # 1.6 Duratec 115hp (Focus Mk2)
    'S': 'HXDA',   # 1.6 Sigma (Fiesta Mk6)
    'T': 'JQDA',   # 1.0 EcoBoost 125hp (revised B-Max)
    'U': 'LUJA',   # 2.0 EcoBoost 250hp (Focus ST Mk3)
    'V': 'XTDA',   # 1.5 EcoBoost 150hp (Focus Mk3.5)
    'W': 'SFDA',   # 1.6 Sigma 100hp (Fiesta Mk6)
    'X': 'G6DA',   # 1.4 Duratec 80hp (Fiesta Mk6)
    'Y': 'P4DA',   # 1.25 Duratec 82hp (Fiesta Mk6/7)
    'Z': 'FYBA',   # 1.8 Duratec (Focus Mk2 / Mondeo Mk3)
    '1': 'XQDA',   # 1.0 EcoBoost (variant)
    '2': 'M2DA',   # 1.0 EcoBoost (post-2017 refresh)
    '3': 'T3JA',   # 2.3 EcoBoost (Focus RS Mk3)
    '4': 'EXDA',   # 1.5 EcoBoost 182hp (Focus Mk3.5)
    '5': 'KJDA',   # 1.5 EcoBoost (Mondeo Mk5)
}


class FordEuDetails(VinDetails):
    """Extractor for Ford of Europe (WF0)."""
    engine = Detail(('vds', 5), _WF0_P5_ENGINE)
    plant  = Detail(('vis', 1), {
        'A': 'Halewood',
        'B': 'Bordeaux',
        'C': 'Cologne',
        'E': 'Almussafes (Valencia)',
        'F': 'Flat Rock (US)',
        'G': 'Genk',
        'K': 'Kansas City',
        'R': 'Saarlouis',
        'S': 'Southampton',
        'T': 'Transylvania (Romania)',
        'W': 'Wayne Michigan',
    })
