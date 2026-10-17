"""C6 auditor helper (VINLab / DNALab / SymptomLab). Evidence only, never product code.

Path setup mirrors audit/scratch/C5/c5_lib.py: labs/comlab is put on sys.path so the
composition can reach the verdict (gets past F-C4-1 / F-C1-5).
"""

from __future__ import annotations

import glob
import logging
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
for p in ("labs/comlab", "apps/wired"):
    if str(ROOT / p) not in sys.path:
        sys.path.insert(0, str(ROOT / p))

logging.disable(logging.WARNING)

import vinlab  # noqa: E402
from vinlab import VINDecodeError, _get_decoder, decode  # noqa: E402

DEC = _get_decoder(vinlab._DEFAULT_DATA_DIR)

_TRANS = {
    "A": 1, "B": 2, "C": 3, "D": 4, "E": 5, "F": 6, "G": 7, "H": 8,
    "J": 1, "K": 2, "L": 3, "M": 4, "N": 5, "P": 7, "R": 9,
    "S": 2, "T": 3, "U": 4, "V": 5, "W": 6, "X": 7, "Y": 8, "Z": 9,
}
_W = (8, 7, 6, 5, 4, 3, 2, 10, 0, 9, 8, 7, 6, 5, 4, 3, 2)


def check_digit(vin: str) -> str:
    """Independent 49 CFR 565 check digit (written here, not imported from VINLab)."""
    t = sum((int(c) if c.isdigit() else _TRANS[c]) * _W[i] for i, c in enumerate(vin))
    r = t % 11
    return "X" if r == 10 else str(r)


def with_check(vin16_with_placeholder: str) -> str:
    """Return the VIN with position 9 set to its correct check digit."""
    v = vin16_with_placeholder
    return v[:8] + check_digit(v[:8] + "0" + v[9:]) + v[9:]


def real_vins() -> list[str]:
    """17-char VINs quoted in labs/vinlab/*.md|*.csv (Slovenian OPSI samples, T-VIN-* notes)."""
    vins: set[str] = set()
    for f in glob.glob(str(ROOT / "labs/vinlab/*.md")) + glob.glob(str(ROOT / "labs/vinlab/*.csv")):
        vins |= set(re.findall(r"\b[A-HJ-NPR-Z0-9]{17}\b", open(f, errors="ignore").read()))
    return sorted(v for v in vins if re.match(r"^[A-Z]", v))


def summary(vin: str) -> str:
    try:
        d = decode(vin)
    except VINDecodeError as e:
        return f"{vin} -> {type(e).__name__}: {e}"
    eng = DEC._resolve_engine(d.vin, d.make, [])
    return (f"{vin} -> make={d.make!r} year={d.model_year} engine={eng and eng['engine_code']!r} "
            f"disp={d.engine_displacement_liters} cyl={d.cylinder_count} fuel={d.fuel_delivery_type.value} "
            f"euro={d.euro_emission_category.value} horizon={d.resolved_horizon.value} "
            f"o2={d.emissions.upstream_o2_type.value} down_o2={d.emissions.downstream_o2_present} "
            f"conf={d.confidence.value}")


def verdict_str(res) -> str:
    v = res.diagnostic_verdict
    return (f"{v.fault_code} conf={v.confidence_score:.2f} abst={v.abstained} "
            f"horizon={res.execution_meta.resolved_horizon} mode={res.execution_meta.degradation_mode}")
