"""VINLab — VIN decoder module.

Decodes a 17-character VIN into a structured VinDNA dataclass.
Petrol passenger vehicles, model years 1990-2020 only.

Runtime: zero MySQL, zero network. All data baked into vinlab/data/ at build time.

Public API:
    decode(vin, *, data_dir=None) -> VinDNA
    VinDNA              — the output dataclass
    VINDecodeError      — raised for out-of-scope or malformed VINs
    ChassisNumberError  — raised for wrong-length inputs (subclass of VINDecodeError)
"""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from vinlab.decoder import ChassisNumberError, RobustVINDecoder, VINDecodeError
from vinlab.models import VinDNA

_DEFAULT_DATA_DIR = Path(__file__).parent / "data"


@lru_cache(maxsize=None)
def _get_decoder(data_dir: Path) -> RobustVINDecoder:
    """Return a RobustVINDecoder for `data_dir`. Cached per distinct data_dir."""
    return RobustVINDecoder(data_dir)


def decode(vin: str, *, data_dir: Path | None = None) -> VinDNA:
    """Decode a 17-char VIN into a VinDNA. Offline, no network, no MySQL."""
    if data_dir is None:
        data_dir = _DEFAULT_DATA_DIR
    return _get_decoder(data_dir).decode_vin_payload(vin)


__all__ = ["ChassisNumberError", "decode", "VinDNA", "VINDecodeError"]
