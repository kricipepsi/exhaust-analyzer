"""C6 era sweep: re-run every decodable corpus case with the horizon VINLab documents as its
fallback (_year_to_horizon, LLD §10) in place of the EURO_1 default, and count verdict changes.
Run: python audit/scratch/C6/era_sweep.py   (from repo root)"""
import sys, copy, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import c6_lib as L  # noqa
import vinlab
from vinlab.overlay.horizon import _year_to_horizon
from v7.load_corpus import load_corpus
import wired.composition as wc
import dnalab.assembly as asm
import dataclasses

real_decode = vinlab.decode

def year_decode(vin, **kw):
    d = real_decode(vin, **kw)
    flags = []
    eng = L.DEC._resolve_engine(d.vin, d.make, flags)
    from vinlab.db.tecdoc_query import lookup_engine_ref
    in_vref = bool(eng and eng.get("engine_code") and lookup_engine_ref(L.DEC.db_path, eng["engine_code"]))
    if not in_vref and d.model_year is not None:
        return dataclasses.replace(d, resolved_horizon=_year_to_horizon(d.model_year))
    return d

import re
stats = collections.Counter(); changed = []; fields = collections.Counter(); examples = []
for cid, raw, cat, ref, tag in load_corpus():
    if not raw.get("vin") or "triage" not in raw:
        continue
    try:
        d = real_decode(raw["vin"])
    except Exception:
        continue
    stats["decodable"] += 1
    try:
        a = wc.diagnose(copy.deepcopy(raw))
    except Exception as e:
        stats["crash"] += 1; continue
    asm._decode_vin = year_decode
    try:
        b = wc.diagnose(copy.deepcopy(raw))
    finally:
        asm._decode_vin = real_decode
    if a.execution_meta.resolved_horizon != b.execution_meta.resolved_horizon:
        stats["horizon_differs"] += 1
    ja, jb = a.model_dump(mode="json"), b.model_dump(mode="json")
    def flat(o, p=""):
        if isinstance(o, dict):
            for k, v in o.items(): yield from flat(v, f"{p}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o): yield from flat(v, f"{p}[{i}]")
        else: yield p, o
    fa, fb = dict(flat(ja)), dict(flat(jb))
    for k in set(fa) | set(fb):
        if fa.get(k) != fb.get(k) and "session" not in k and "timestamp" not in k and "trace" not in k and "latency" not in k and "_ms" not in k:
            fields[re.sub(r"\[\d+\]", "[]", k)] += 1
    if a.execution_meta.resolved_horizon != b.execution_meta.resolved_horizon and len(examples) < 4:
        examples.append((cid, raw["vin"], d.model_year, a.execution_meta.resolved_horizon, getattr(a.execution_meta, "processing_confidence_rating", None), b.execution_meta.resolved_horizon, getattr(b.execution_meta, "processing_confidence_rating", None)))
    if fa.get(".performance_analytics.o2_sensor_bias_verdict") != fb.get(".performance_analytics.o2_sensor_bias_verdict") and stats["o2ex"] < 3:
        stats["o2ex"] += 1
        print("O2BIAS", cid, raw["vin"], d.model_year, fa.get(".performance_analytics.o2_sensor_bias_verdict"), "->", fb.get(".performance_analytics.o2_sensor_bias_verdict"))
    if a.diagnostic_verdict.fault_code != b.diagnostic_verdict.fault_code:
        stats["verdict_differs"] += 1
        changed.append((cid, raw["vin"], d.model_year, L.verdict_str(a), L.verdict_str(b)))
print(dict(stats))
print(fields.most_common(15))
for e in examples: print(e)
for c in changed[:12]:
    print(c)
