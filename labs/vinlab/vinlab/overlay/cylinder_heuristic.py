"""Cylinder-count inference from engine code + displacement + brand.

Last-resort runtime fallback — fires only when cylinder_count is still 0
after CSV and vref.db lookups. Never overrides real data.

Brand rules are drawn from docs/decypher.md; displacement bands from
the T-VL-7 task spec.  Do not expand the rule table without a follow-up task.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

__all__ = ["CylinderHint", "infer_cylinder"]

# source: T-VL-7 success criteria — controlled vocabulary for config field
# (not stored in VinDNA directly; carried as aux data)
_CONFIG_VOCAB: frozenset[str] = frozenset({
    "I3", "I4", "I5", "I6", "V6", "V8", "V10", "V12",
    "BOXER_4", "BOXER_6", "ROTARY", "W12",
})


@dataclass(frozen=True)
class CylinderHint:
    """Inferred engine attributes from brand naming + displacement fallback.

    Args:
        count: Inferred cylinder count (0 = unresolved).
        config: Engine configuration string (e.g. ``"I4"``, ``"V6"``).
            Empty string when unresolved.
        induction: ``"NATURALLY_ASPIRATED"`` or ``"TURBOCHARGED"``.
            Default is NATURALLY_ASPIRATED.
        source: One of ``"brand_rule"``, ``"disp_fallback"``, ``"unresolved"``.
    """

    count: int = 0
    config: str = ""
    induction: str = "NATURALLY_ASPIRATED"
    source: str = "unresolved"


# ---------------------------------------------------------------------------
# Displacement fallback — source: T-VL-7 task spec displacement band table
# ---------------------------------------------------------------------------

def _displacement_fallback(disp: float) -> CylinderHint:
    """Return conservative cylinder guess from displacement alone."""
    if disp <= 0:
        return CylinderHint()
    if disp <= 1.2:
        return CylinderHint(count=3, config="I3", source="disp_fallback")
    if disp <= 2.5:
        return CylinderHint(count=4, config="I4", source="disp_fallback")
    if disp <= 3.5:
        return CylinderHint(count=6, config="V6", source="disp_fallback")
    if disp <= 5.0:
        return CylinderHint(count=8, config="V8", source="disp_fallback")
    # > 5.0 L
    return CylinderHint(count=12, config="V12", source="disp_fallback")


# ---------------------------------------------------------------------------
# Induction helpers
# ---------------------------------------------------------------------------

def _is_turbo_bmw(code: str) -> bool:
    """BMW turbo families: N54, N55, B58, S55, S63."""
    m = re.match(r"^([NBMS])(\d{2})", code)
    if m:
        family = m.group(1) + m.group(2)
        return family in {"N54", "N55", "B58", "S55", "S63"}
    return False


def _induction(code: str, brand: str, config: str) -> str:
    """Induction heuristic (brand-aware)."""
    # Volvo: T suffix → turbo
    if brand == "VOLVO" and code.endswith("T"):
        return "TURBOCHARGED"
    # BMW turbo families
    if brand == "BMW" and _is_turbo_bmw(code):
        return "TURBOCHARGED"
    # small-displacement I3 modern engines are nearly all turbo
    if config == "I3":
        return "TURBOCHARGED"
    return "NATURALLY_ASPIRATED"


def _make_disp_hint_with_induction(
    disp: float, code: str, brand: str
) -> CylinderHint:
    """Displacement fallback with brand-aware induction applied on top."""
    base = _displacement_fallback(disp)
    if base.count == 0:
        return base
    return CylinderHint(
        base.count, base.config,
        _induction(code, brand, base.config), "brand_rule",
    )


# ---------------------------------------------------------------------------
# Brand-specific rules — source: docs/decypher.md + T-VL-7 task spec
# ---------------------------------------------------------------------------


def _infer_bmw(code: str, disp: float) -> CylinderHint:
    """BMW: [NBMS]XX pattern — first of the two digits encodes cylinders.

    2→4, 4→4, 5→6, 6/7→8, 8→12.
    For numeric codes (leading digit), use simple tens-digit rule
    with displacement tiebreak.
    """
    m = re.match(r"^([NBMS])(\d)(\d)", code)
    if m:
        tens = int(m.group(2))
        if tens == 2:
            return CylinderHint(4, "I4", _induction(code, "BMW", "I4"), "brand_rule")
        if tens == 4:
            return CylinderHint(4, "I4", _induction(code, "BMW", "I4"), "brand_rule")
        if tens == 5:
            return CylinderHint(6, "I6", _induction(code, "BMW", "I6"), "brand_rule")
        if tens in (6, 7):
            return CylinderHint(8, "V8", _induction(code, "BMW", "V8"), "brand_rule")
        if tens == 8:
            return CylinderHint(12, "V12", _induction(code, "BMW", "V12"), "brand_rule")
        # tens = 3 or other → use displacement fallback
        return _make_disp_hint_with_induction(disp, code, "BMW")

    # simple rule (numeric-first codes): displacement is the primary signal.
    # BMW boundary: ≤2.0 → I4, ≥2.5 → I6 (per decypher.md simplified rule).
    if len(code) >= 3 and code[1].isdigit() and code[2].isdigit():
        if disp <= 2.0:
            return CylinderHint(4, "I4", _induction(code, "BMW", "I4"), "brand_rule")
        if disp >= 4.0:
            return CylinderHint(8, "V8", _induction(code, "BMW", "V8"), "brand_rule")
        return CylinderHint(6, "I6", _induction(code, "BMW", "I6"), "brand_rule")

    return _displacement_fallback(disp)


def _infer_hyundai_kia(code: str, disp: float) -> CylinderHint:
    """Hyundai/Kia: G[cyl] prefix — second char is the cylinder digit."""
    m = re.match(r"^G(\d)", code)
    if m:
        cyl = int(m.group(1))
        if cyl in (3, 4, 6, 8):
            return CylinderHint(cyl, f"I{cyl}", "NATURALLY_ASPIRATED", "brand_rule")
    return _displacement_fallback(disp)


def _infer_honda(code: str, disp: float) -> CylinderHint:
    """Honda: J-series (≥3.0L) is V6; most others are I4."""
    # J-series V6 — check before the generic I4 pattern
    if re.match(r"^J\d", code) and disp >= 3.0:
        return CylinderHint(6, "V6", "NATURALLY_ASPIRATED", "brand_rule")
    # Generic Honda I4: D, B, F, K, R, J, L prefix
    if re.match(r"^([DBFKRJL])\d", code):
        return CylinderHint(4, "I4", "NATURALLY_ASPIRATED", "brand_rule")
    return _displacement_fallback(disp)


# Toyota family map — source: T-VL-7 task spec
_TOYOTA_I4: frozenset[str] = frozenset({"AZ", "NR", "NZ", "ZZ", "QR", "AR"})
_TOYOTA_V6: frozenset[str] = frozenset({"GR", "VZ", "JZ", "MZ"})
_TOYOTA_V8: frozenset[str] = frozenset({"UZ"})


def _infer_toyota(code: str, disp: float) -> CylinderHint:
    """Toyota: family prefix → cylinder count."""
    m = re.match(r"^(\d?[A-Z]{1,3})", code)
    if m:
        family = m.group(1).lstrip("0123456789")
        if family in _TOYOTA_I4:
            return CylinderHint(4, "I4", "NATURALLY_ASPIRATED", "brand_rule")
        if family in _TOYOTA_V6:
            return CylinderHint(6, "V6", "NATURALLY_ASPIRATED", "brand_rule")
        if family in _TOYOTA_V8:
            return CylinderHint(8, "V8", "NATURALLY_ASPIRATED", "brand_rule")
    return _displacement_fallback(disp)


def _infer_volvo(code: str, disp: float) -> CylinderHint:
    """Volvo: B[cyl]... — digit after B is the cylinder count; T suffix = turbo."""
    m = re.match(r"^B(\d)", code)
    if m:
        cyl = int(m.group(1))
        if 3 <= cyl <= 8:
            induction = "TURBOCHARGED" if code.endswith("T") else "NATURALLY_ASPIRATED"
            if cyl == 5:
                config = "I5"
            elif cyl == 6:
                config = "I6"
            else:
                config = f"I{cyl}"
            return CylinderHint(cyl, config, induction, "brand_rule")
    return _displacement_fallback(disp)


# Mercedes model-number table — source: decypher.md
_MERCEDES_TABLE: dict[str, tuple[int, str]] = {
    "M111": (4, "I4"),
    "M271": (4, "I4"),
    "M166": (4, "I4"),
    "M112": (6, "V6"),
    "M272": (6, "V6"),
    "M276": (6, "V6"),
    "M113": (8, "V8"),
    "M273": (8, "V8"),
    "M278": (8, "V8"),
    "M104": (6, "I6"),
    "M275": (12, "V12"),
    "M279": (12, "V12"),
    "M137": (12, "V12"),
}


def _infer_mercedes(code: str, disp: float) -> CylinderHint:
    """Mercedes: MXXX engine-code lookup table."""
    m = re.match(r"^(M\d{3})", code)
    if m:
        family = m.group(1)
        if family in _MERCEDES_TABLE:
            cyl, config = _MERCEDES_TABLE[family]
            return CylinderHint(cyl, config, "NATURALLY_ASPIRATED", "brand_rule")
    return _displacement_fallback(disp)


def _infer_vw_audi(code: str, disp: float) -> CylinderHint:
    """VW/Audi: use displacement bands (code prefixes are unreliable).

    Per T-VL-7 task spec notes column: primary signal is displacement
    fallback; the alpha-code prefixes add regional variation.
    """
    base = _displacement_fallback(disp)
    if base.count == 0:
        return base
    return CylinderHint(
        base.count, base.config,
        _induction(code, "VW", base.config), "brand_rule",
    )


_NISSAN_I4: frozenset[str] = frozenset({"GA", "CA", "CR", "QG", "SR", "HR", "MR"})
_NISSAN_V6: frozenset[str] = frozenset({"VQ", "VK"})
_NISSAN_TURBO_I4: frozenset[str] = frozenset({"TB"})


def _infer_nissan(code: str, disp: float) -> CylinderHint:
    """Nissan: family prefix → cylinder count."""
    m = re.match(r"^([A-Z]{2})", code)
    if m:
        prefix = m.group(1)
        if prefix in _NISSAN_I4:
            return CylinderHint(4, "I4", "NATURALLY_ASPIRATED", "brand_rule")
        if prefix in _NISSAN_V6:
            return CylinderHint(6, "V6", "NATURALLY_ASPIRATED", "brand_rule")
        if prefix in _NISSAN_TURBO_I4:
            return CylinderHint(4, "I4", "TURBOCHARGED", "brand_rule")
    return _displacement_fallback(disp)


def _infer_mitsubishi(code: str, disp: float) -> CylinderHint:
    """Mitsubishi: leading digit = cylinder count (4Gxx → 4, 6Gxx → 6)."""
    m = re.match(r"^(\d)[A-Z]", code)
    if m:
        cyl = int(m.group(1))
        if cyl in (3, 4):
            return CylinderHint(cyl, f"I{cyl}", "NATURALLY_ASPIRATED", "brand_rule")
        if cyl in (6, 8):
            config = "V6" if cyl == 6 else "V8"
            return CylinderHint(cyl, config, "NATURALLY_ASPIRATED", "brand_rule")
    return _displacement_fallback(disp)


def _infer_mazda(code: str, disp: float) -> CylinderHint:
    """Mazda: B/F/P/K prefix → I4."""
    m = re.match(r"^([BFKP])\d", code)
    if m:
        return CylinderHint(4, "I4", "NATURALLY_ASPIRATED", "brand_rule")
    return _displacement_fallback(disp)


# Subaru boxer families — source: T-VL-7 task spec
_SUBARU_BOXER_4: frozenset[str] = frozenset({"EJ", "FA", "FB", "EE"})
_SUBARU_BOXER_6: frozenset[str] = frozenset({"EZ"})


def _infer_subaru(code: str, disp: float) -> CylinderHint:
    """Subaru: EJ/FA/FB/EE → BOXER_4; EZ → BOXER_6."""
    m = re.match(r"^([A-Z]{2})", code)
    if m:
        prefix = m.group(1)
        if prefix in _SUBARU_BOXER_4:
            return CylinderHint(4, "BOXER_4", "NATURALLY_ASPIRATED", "brand_rule")
        if prefix in _SUBARU_BOXER_6:
            return CylinderHint(6, "BOXER_6", "NATURALLY_ASPIRATED", "brand_rule")
    return _displacement_fallback(disp)


_RENAULT_I4: frozenset[str] = frozenset({"K4M", "H4M", "K9K", "F4R", "F4P", "K4J"})
_RENAULT_I3: frozenset[str] = frozenset({"H5F", "D4F", "H4Bt"})


def _infer_renault(code: str, disp: float) -> CylinderHint:
    """Renault/Dacia: family lookup table."""
    m = re.match(r"^([A-Z]\d[A-Z])", code)
    if m:
        family = m.group(1)
        if family in _RENAULT_I4:
            return CylinderHint(4, "I4", "NATURALLY_ASPIRATED", "brand_rule")
        if family in _RENAULT_I3:
            return CylinderHint(3, "I3", "NATURALLY_ASPIRATED", "brand_rule")
    return _displacement_fallback(disp)


def _infer_psa(code: str, disp: float) -> CylinderHint:
    """PSA (Peugeot/Citroen): XU/ES/EW prefix → I4."""
    m = re.match(r"^([EX][USW])", code)
    if m:
        return CylinderHint(4, "I4", "NATURALLY_ASPIRATED", "brand_rule")
    # modern PSA: EP/EW families
    m = re.match(r"^([EP])([FWS])", code)
    if m:
        return CylinderHint(4, "I4", "NATURALLY_ASPIRATED", "brand_rule")
    return _displacement_fallback(disp)


# ---------------------------------------------------------------------------
# Brand dispatch table — source: T-VL-7 task spec brand table
# ---------------------------------------------------------------------------

_BRAND_DISPATCH: dict[str, object] = {
    "BMW": _infer_bmw,
    "HYUNDAI": _infer_hyundai_kia,
    "KIA": _infer_hyundai_kia,
    "HONDA": _infer_honda,
    "TOYOTA": _infer_toyota,
    "VOLVO": _infer_volvo,
    "MERCEDES": _infer_mercedes,
    "MERCEDES-BENZ": _infer_mercedes,
    "MERCEDES BENZ": _infer_mercedes,
    "VOLKSWAGEN": _infer_vw_audi,
    "AUDI": _infer_vw_audi,
    "SKODA": _infer_vw_audi,
    "SEAT": _infer_vw_audi,
    "NISSAN": _infer_nissan,
    "MITSUBISHI": _infer_mitsubishi,
    "MAZDA": _infer_mazda,
    "SUBARU": _infer_subaru,
    "RENAULT": _infer_renault,
    "DACIA": _infer_renault,
    "PEUGEOT": _infer_psa,
    "CITROEN": _infer_psa,
}


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def infer_cylinder(code: str, disp_liters: float, brand: str) -> CylinderHint:
    """Infer cylinder_count, engine_configuration, induction from engine code.

    Returns a ``CylinderHint`` with ``count=0`` when unable to resolve.
    This is a **runtime fallback only** — callers must gate on
    ``cylinder_count == 0`` so it never overwrites CSV or vref.db data.

    Args:
        code: Engine code string (e.g. ``"N52B25"``, ``"G4KE"``).
        disp_liters: Engine displacement in litres.
        brand: Manufacturer name (matched case-insensitively).

    Returns:
        ``CylinderHint`` with inferred attributes.
    """
    code = (code or "").strip().upper()
    brand_key = (brand or "").strip().upper()

    if not code:
        return _displacement_fallback(disp_liters)

    handler = _BRAND_DISPATCH.get(brand_key)
    if handler is not None:
        return handler(code, disp_liters)  # type: ignore[operator]

    # Unknown brand — displacement-only fallback
    return _displacement_fallback(disp_liters)
