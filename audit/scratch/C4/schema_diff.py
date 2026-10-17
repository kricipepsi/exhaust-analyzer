"""C4 probe: mechanical producer-vs-consumer schema diff across the lab boundaries.

Run from repo root:  python audit/scratch/C4/schema_diff.py
Compares pydantic field sets (name, type, required, numeric bounds) and
StrEnum literal sets between each emitter lab's output model and COMLab's mirror.
"""
from __future__ import annotations

import enum
import typing

import annotated_types as at
from pydantic import BaseModel

import comlab.schemas.ingestion as ci
import comlab.schemas.vocabulary as cv
import dtclab.schemas.freeze_frame as dff
import dtclab.schemas.mode06_result as dm6
import dtclab.schemas.payload as dp
import dtclab.schemas.vocabulary as dv
import gaslab.contracts as gc
import obdlab.schemas.payload as op
import obdlab.schemas.vocabulary as ov


def bounds(fi):
    b = {}
    for m in fi.metadata:
        for k in ("ge", "gt", "le", "lt"):
            if isinstance(m, getattr(at, k.capitalize())):
                b[k] = getattr(m, k)
        if hasattr(m, "pattern") and m.pattern:
            b["pattern"] = m.pattern
    return b


def enum_of(ann):
    for a in typing.get_args(ann) or (ann,):
        if isinstance(a, type) and issubclass(a, enum.Enum):
            return a
        if typing.get_args(a):
            e = enum_of(a)
            if e:
                return e
    return None


def tname(ann):
    s = repr(ann).replace("typing.", "")
    for mod in ("comlab.schemas.vocabulary.", "obdlab.schemas.vocabulary.", "dtclab.schemas.vocabulary.",
                "gaslab.contracts.", "comlab.schemas.ingestion.", "dtclab.schemas.freeze_frame.",
                "dtclab.schemas.mode06_result."):
        s = s.replace(mod, "")
    return s.replace("<enum '", "").replace("'>", "").replace("<class '", "")


def diff_models(label, prod: type[BaseModel], cons: type[BaseModel]):
    print(f"\n=== {label}: {prod.__module__}.{prod.__name__} -> {cons.__module__}.{cons.__name__}")
    pf, cf = prod.model_fields, cons.model_fields
    n = 0
    for name in sorted(set(pf) - set(cf)):
        print(f"  PRODUCER-ONLY  {name}: {tname(pf[name].annotation)}  (dropped at boundary)"); n += 1
    for name in sorted(set(cf) - set(pf)):
        print(f"  CONSUMER-ONLY  {name}: {tname(cf[name].annotation)} required={cf[name].is_required()}"); n += 1
    for name in sorted(set(pf) & set(cf)):
        p, c = pf[name], cf[name]
        pe, ce = enum_of(p.annotation), enum_of(c.annotation)
        if pe and ce:
            ps, cs = {m.value for m in pe}, {m.value for m in ce}
            if ps != cs:
                print(f"  ENUM-DRIFT     {name}: producer-only={sorted(ps-cs)} consumer-only={sorted(cs-ps)}"); n += 1
        elif pe and not ce:
            print(f"  ENUM->UNTYPED  {name}: producer {pe.__name__}({len(pe)}) -> consumer {tname(c.annotation)}"); n += 1
        elif tname(p.annotation).replace("Optional", "") != tname(c.annotation).replace("Optional", "") and not (pe or ce):
            print(f"  TYPE           {name}: {tname(p.annotation)} -> {tname(c.annotation)}"); n += 1
        pb, cb = bounds(p), bounds(c)
        if pb != cb:
            print(f"  BOUNDS         {name}: producer={pb} consumer={cb}"); n += 1
        popt = type(None) in typing.get_args(p.annotation)
        copt = type(None) in typing.get_args(c.annotation)
        if popt and not copt:
            print(f"  OPTIONALITY    {name}: producer may emit None, consumer requires value"); n += 1
    print(f"  -> {n} differences")


def diff_enum(label, a, b):
    sa, sb = {m.value for m in a}, {m.value for m in b}
    tag = "SAME" if sa == sb else "DRIFT"
    print(f"{tag:5} {label}: {a.__module__}.{a.__name__}({len(sa)}) vs {b.__module__}.{b.__name__}({len(sb)})"
          + ("" if sa == sb else f"  left-only={sorted(sa-sb)} right-only={sorted(sb-sa)}"))


print("##### ENUM PAIRS (producer vs COMLab mirror)")
diff_enum("ChemicalSignature", gc.ChemicalSignature, cv.ChemicalSignature)
diff_enum("SampleValidity", gc.SampleValidity, cv.SampleValidity)
diff_enum("EngineStateBucket(gas)", gc.EngineStateBucket, cv.EngineStateBucket)
diff_enum("RpmStateBucket(obd)", ov.RpmStateBucket, cv.EngineStateBucket)
for n in ("VEValidity", "TrimAnalyticsGate", "NodeMAFStatus", "NodeMAPStatus", "FuelSystemStatus", "O2FailureMode"):
    diff_enum(n + "(obd)", getattr(ov, n), getattr(cv, n))
for n in ("DTCRoutingTag", "HistoricalFaultContext", "FuelSystemStatus", "DTCSeverityClass", "DTCState"):
    diff_enum(n + "(dtc)", getattr(dv, n), getattr(cv, n))
diff_enum("Mode06MonitorState(dtc)", dv.Mode06MonitorState, cv.Mode06Status)

print("\n##### MODEL PAIRS")
diff_models("GAS", gc.GasLabPayload, ci.GasLabPayload)
diff_models("OBD", op.OBDLivePayload, ci.OBDLiveDataPayload)
diff_models("DTC", dp.DTCLabPayload, ci.DTCLabPayload)
diff_models("DTC.freeze_frame", dff.FreezeFrameRecord, ci.FreezeFrameRecord)
diff_models("DTC.mode06", dm6.Mode06MonitorResult, ci.Mode06MonitorResult)


# ---------------------------------------------------------------------------
# DNA projection: every VINLab enum value pushed through wired.composition's
# projection helpers into each consumer (OBDLab dna view, GASLab dna view,
# COMLab SessionMetadata / request).
# ---------------------------------------------------------------------------
import vinlab.models as vm  # noqa: E402
from wired import composition as wc  # noqa: E402

print("\n##### DNA PROJECTION (VINLab value -> composition -> consumer)")
base = wc._build_fallback_vin_dna("")
base["confidence"] = "PARTIAL"
probes = {
    "induction_type": [m.value for m in vm.InductionType],
    "air_metering_strategy": [m.value for m in vm.AirMeteringStrategy],
    "emissions.upstream_o2_type": [m.value for m in vm.UpstreamO2Type],
    "emissions.downstream_trim_role": [m.value for m in vm.DownstreamTrimRole],
    "confidence": [m.value for m in vm.VinConfidence],
    "euro_emission_category": [m.value for m in vm.EuroEmissionCategory],
    "fuel_delivery_type": [m.value for m in vm.FuelDeliveryType],
}


def _try(fn):
    try:
        r = fn()
        return "ok"
    except Exception as e:  # noqa: BLE001
        return f"REJECT {type(e).__name__}: {str(e).splitlines()[0][:70]}"


for field, values in probes.items():
    for val in values:
        vd = {**base, "emissions": dict(base["emissions"])}
        if field.startswith("emissions."):
            vd["emissions"][field.split(".", 1)[1]] = val
        else:
            vd[field] = val
        vd["resolved_horizon"] = "HORIZON_ADAPTIVE"
        obd = _try(lambda: wc._build_obd_dna_view(vd))
        gas = _try(lambda: wc._build_gas_dna_view(vd))
        meta = _try(lambda: wc._build_metadata(vd))
        req = _try(lambda: ci.OrchestratorInboundRequest(
            metadata=wc._build_metadata(vd),
            gas_lab_output=ci.GasLabPayload(chemical_state="NORMAL_OPERATION", gas_co=0.1, gas_hc=50,
                                            gas_co2=15.0, gas_o2=0.5, gas_nox=50, lambda_chem=1.0,
                                            sample_validity="VALID"),
            downstream_trim_role=cv.DownstreamTrimRole(vd["emissions"].get("downstream_trim_role", "NONE"))))
        flag = "" if {obd, gas, meta, req} == {"ok"} else "   <-- DRIFT"
        print(f"  {field}={val}: OBDLab={obd} | GASLab={gas} | COMLab.meta={meta} | COMLab.request={req}{flag}")
