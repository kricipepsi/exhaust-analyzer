"""
core/vin/extractors/hyundai_kia.py
===================================
Hyundai and Kia VinDetails extractors — TMA, KMH, U5Y, KNA.

Engine-code mappings mined from 1.8M OPSI registrations (June 2023).
  TMA  9,442 rows  — Hyundai (Nosovice, Czech Republic)
  KMH  7,624 rows  — Hyundai (Ulsan, South Korea / other)
  U5Y  9,814 rows  — Kia (Zilina, Slovakia)
  KNA  7,827 rows  — Kia (South Korea export)

Hyundai (TMA/KMH): VDS position 4 (VIN character index 7, 0-based)
Kia U5Y:           VDS position 1 (VIN character index 4, 0-based)
Kia KNA:           VDS position 4 (VIN character index 7, 0-based)

Hyundai-Kia petrol engine families in scope (1990–2020):
  - Gamma:  G4FA (1.4), G4FC (1.6 MPI), G4FD (1.6 GDI), G4FG (1.6 MPI Theta),
            G4FJ (1.4 T-GDI), G4FP (1.4 GDI)
  - Kappa:  G4LA (1.2), G4LE (1.2 MPI), G4LC (1.0 MPI), G4LD (1.0 T-GDI),
            G4LF (1.4 MPI), G3LD (1.0 T-GDI), G3LE (1.0 T-GDI GT)
            G3LC (1.0 T-GDI Stonic)
  - Nu:     G4NA (2.0 MPI), G4NC (2.0 GDI)
  - Theta:  G4KD (2.0 MPI), G4KH (2.4 GDI), G4KJ (2.4 MPI), G4KE (2.4 MPI)
  - Beta:   G4ED (1.6 MPI — older i30)

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
# Hyundai — TMA/KMH VDS position 4 (16 unique engine codes)
# ---------------------------------------------------------------------------

_HYUNDAI_P4_ENGINE: dict[str, str] = {
    # Kappa family (small displacement)
    '3': 'G4LD',    # 1.0 Kappa T-GDI (i10/i20)
    '2': 'G4FJ',    # 1.4 Kappa T-GDI (i30/i20 N Line)
    'E': 'G4LC',    # 1.0 Kappa MPI (i10 2013+)
    'F': 'G4LE',    # 1.2 Kappa MPI (i20/i10)
    'P': 'G3LD',    # 1.0 T-GDI (i20 N Line 2020+)
    'R': 'G4FP',    # 1.4 Kappa GDI (i20 2014+)
    # Gamma family (mid displacement)
    'A': 'G4FA',    # 1.4 Gamma N/A (i20/i30)
    'C': 'G4FA',    # 1.4 Gamma variant
    '1': 'G4FD',    # 1.6 Gamma GDI (i30/ix35)
    'D': 'G4FC',    # 1.6 Gamma MPI (i30 GD)
    'G': 'G4FG',    # 1.6 Gamma MPI (Tucson)
    # Nu family (2.0)
    'H': 'G4NA',    # 2.0 Nu MPI (ix35/Tucson)
    'K': 'G4NC',    # 2.0 Nu GDI (Tucson)
    # Theta family (2.0+)
    'J': 'G4KD',    # 2.0 Theta II MPI (Sonata/ix35)
    # Beta (older)
    'B': 'G4ED',    # 1.6 Beta MPI (older i30 FD)
    '5': 'G4FJ',    # 1.4 T-GDI variant
}

# ---------------------------------------------------------------------------
# Kia U5Y (Zilina) — VDS position 1 (19 unique engine codes)
# ---------------------------------------------------------------------------

_U5Y_P1_ENGINE: dict[str, str] = {
    'F': 'G4FA',    # 1.4 Gamma N/A (Ceed/Rio)
    'M': 'G4FA',    # 1.4 Gamma variant
    'C': 'G4FD',    # 1.6 Gamma GDI (Ceed)
    '5': 'G4LD',    # 1.0 T-GDI (Stonic/Ceed 2017+)
    'H': 'G4FD',    # 1.6 Gamma (Ceed GT variant)
    'G': 'G4FD',    # 1.6 Gamma (Ceed JD)
    'D': 'G4FC',    # 1.6 Gamma MPI (Ceed ED)
    'E': 'G4FG',    # 1.6 Gamma (Sportage)
    'J': 'G4NA',    # 2.0 Nu MPI (Sportage)
    'K': 'G4KD',    # 2.0 Theta II (Optima EU)
    'N': 'G4FJ',    # 1.4 T-GDI (Ceed 2018+)
    'P': 'G4LC',    # 1.0 Kappa MPI (Picanto)
    'R': 'G4LE',    # 1.2 Kappa (Rio)
    'T': 'G3LC',    # 1.0 T-GDI (Stonic 2017+)
    'U': 'G4FP',    # 1.4 GDI (Rio 2017+)
    'V': 'G4NC',    # 2.0 Nu GDI (Sportage)
    'W': 'G3LD',    # 1.0 T-GDI variant
    'X': 'G4KJ',    # 2.4 Theta II (Sorento)
    'Y': 'G4KH',    # 2.4 Theta II GDI (Sorento)
}

# ---------------------------------------------------------------------------
# Kia KNA (South Korea / export) — VDS position 4 (12 unique engine codes)
# ---------------------------------------------------------------------------

_KNA_P4_ENGINE: dict[str, str] = {
    '2': 'G4LA',    # 1.2 Kappa (Picanto 1)
    '1': 'G4LA',    # 1.2 Kappa variant
    'C': 'G4LE',    # 1.2 Kappa MPI (Picanto 2)
    '4': 'G4LC',    # 1.0 Kappa MPI (Picanto 3)
    '7': 'G3LE',    # 1.0 T-GDI (Picanto GT Line)
    '8': 'G4LF',    # 1.4 Kappa MPI (Rio Mk4)
    '3': 'G4FA',    # 1.4 Gamma N/A (Ceed export)
    '5': 'G4FD',    # 1.6 Gamma GDI (Sportage export)
    '6': 'G4FG',    # 1.6 Gamma MPI (Sportage)
    'A': 'G4FC',    # 1.6 Gamma MPI (Rio/Ceed)
    'B': 'G4FJ',    # 1.4 T-GDI (Stinger / Ceed 2018)
    'D': 'G4LD',    # 1.0 T-GDI (Picanto X-Line)
}


class HyundaiDetails(VinDetails):
    """Extractor for Hyundai EU (TMA, KMH). VDS pos 4."""
    engine = Detail(('vds', 4), _HYUNDAI_P4_ENGINE)
    plant  = Detail(('vis', 1), {
        'A': 'Nosovice (Czech Republic)',
        'B': 'Ulsan (South Korea)',
        'C': 'Chennai (India)',
        'E': 'Encino (US)',
    })


class KiaU5YDetails(VinDetails):
    """Extractor for Kia EU / Slovakia (U5Y). VDS pos 1."""
    engine = Detail(('vds', 1), _U5Y_P1_ENGINE)
    plant  = Detail(('vis', 1), {
        'A': 'Zilina (Slovakia)',
        'B': 'Gwangmyeong (Korea)',
    })


class KiaKNADetails(VinDetails):
    """Extractor for Kia South Korea / export (KNA). VDS pos 4."""
    engine = Detail(('vds', 4), _KNA_P4_ENGINE)
    plant  = Detail(('vis', 1), {
        'A': 'Sohari (Korea)',
        'B': 'Hwaseong (Korea)',
        'C': 'Gwangju (Korea)',
    })
