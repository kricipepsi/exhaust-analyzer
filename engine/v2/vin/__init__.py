"""
core/vin/__init__.py
====================
Public entry point for the offline VIN resolver.

Three confidence levels:
  'high'    - VIN decoded + engine code found in engine_dna.json
  'partial' - WMI manufacturer resolved but engine code absent or short
  'none'    - VIN failed validation

Brand/model catalogue (OPSI 1990-2020, 1.58M registrations) is loaded from
brand_models.py and used to populate EngineDNA.common_models on every resolve.
"""

from __future__ import annotations

import json
import pathlib
import re
from typing import Optional

from .brand_models import lookup_models
from .extractors import register_all_extractors
from .prior_context import EngineDNA

register_all_extractors()

_DNA_TABLE: dict | None = None


def _load_dna() -> dict:
    global _DNA_TABLE
    if _DNA_TABLE is None:
        path = pathlib.Path(__file__).parent / 'data' / 'engine_dna.json'
        if path.exists():
            rows = json.loads(path.read_text(encoding='utf-8'))
            _DNA_TABLE = {row['engine_code']: row for row in rows if row.get('engine_code')}
        else:
            _DNA_TABLE = {}
    return _DNA_TABLE


def _safe_year(vin_obj) -> int | None:
    try:
        yr = vin_obj.year
        if yr and 1980 <= yr <= 2030:
            return int(yr)
    except Exception:
        pass
    return None


_VIN_RE = re.compile(r'^[A-HJ-NPR-Z0-9]{17}$', re.IGNORECASE)


def _is_valid_vin(vin_str: str) -> bool:
    return bool(_VIN_RE.match(vin_str.replace(' ', '').replace('-', '')))


def _str(val) -> str | None:
    if val is None:
        return None
    s = str(val).strip()
    return s if s else None


def resolve(vin_str: str) -> EngineDNA:
    """Offline-only VIN to EngineDNA. Never raises; returns confidence='none' on failure."""
    vin_clean = vin_str.strip().replace(' ', '').replace('-', '').upper()

    if not _is_valid_vin(vin_clean):
        return EngineDNA(source='unknown', confidence='none')

    try:
        from vininfo import Vin
        vin = Vin(vin_clean)
    except Exception:
        return EngineDNA(source='unknown', confidence='none')

    manufacturer = _str(vin.manufacturer)
    year = _safe_year(vin)
    known_models: list = lookup_models(manufacturer, year)

    engine_code: str | None = None
    try:
        details = vin.details
        if details is not None:
            raw = str(details.engine) if hasattr(details, 'engine') else None
            if raw and len(raw) >= 3:
                engine_code = raw.strip().upper()
    except Exception:
        pass

    dna_row = _load_dna().get(engine_code) if engine_code else None

    if dna_row:
        dna = EngineDNA.from_dna_row(dna_row, source='vininfo+dna')
        merged = list(dict.fromkeys(list(dna.common_models) + known_models))
        return EngineDNA(
            source=dna.source,
            confidence=dna.confidence,
            make=dna.make or manufacturer,
            engine_code=dna.engine_code,
            year=year or dna.year,
            year_range=dna.year_range,
            displacement_l=dna.displacement_l,
            cylinders=dna.cylinders,
            induction=dna.induction,
            intercooler=dna.intercooler,
            injection=dna.injection,
            fuel_type=dna.fuel_type,
            o2_arch=dna.o2_arch,
            spec_idle_gps=dna.spec_idle_gps,
            known_issues=list(dna.known_issues),
            common_models=merged,
        )

    if engine_code:
        return EngineDNA(
            source='wmi_only',
            confidence='partial',
            make=manufacturer,
            engine_code=engine_code,
            year=year,
            common_models=known_models,
        )

    if manufacturer:
        return EngineDNA(
            source='wmi_only',
            confidence='partial',
            make=manufacturer,
            year=year,
            common_models=known_models,
        )

    return EngineDNA(source='unknown', confidence='none')
