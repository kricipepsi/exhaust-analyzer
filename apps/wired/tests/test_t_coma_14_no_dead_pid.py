"""T-COMA-14 (F-C1-21): every PID in the registry dispatch table resolves to a field its source schema has, so no rule
row is silently dead. Tags: NEW fails on the base; PIN passes on the base and after.
"""

from __future__ import annotations

import pytest

_SOURCES = {
    "obd": ("comlab.schemas.ingestion", "OBDLiveDataPayload"),
    "ff": ("comlab.schemas.ingestion", "FreezeFrameRecord"),
}


def _fields(source: str) -> set[str]:
    import importlib

    module, name = _SOURCES[source]
    return set(getattr(importlib.import_module(module), name).model_fields)


@pytest.mark.parametrize("source", sorted(_SOURCES))
def test_every_dispatch_field_exists_in_its_schema(source):
    """NEW (ff) and PIN (obd): no (source, field) pair in _PID_DISPATCH names a field its schema lacks."""
    from registry.integration_shim import _PID_DISPATCH

    fields = _fields(source)
    dead = sorted({f"{pid}:{fld}" for pid, chain in _PID_DISPATCH.items() for src, fld in chain
                   if src == source and fld not in fields})
    assert dead == []


def test_rm004_keeps_its_other_evidence():
    """NEW: RM-004 keeps its chemistry, long-trim and DTC rows; only the dead fuel_pressure row is gone."""
    from registry.integration_shim import RegistryV2Router

    rule = next(r for r in RegistryV2Router().rules if r.rule_id == "RM-004")
    assert [e.pid for e in rule.obd_evidence] == ["longft1"]
    assert rule.chemistry_evidence and rule.dtc_evidence
