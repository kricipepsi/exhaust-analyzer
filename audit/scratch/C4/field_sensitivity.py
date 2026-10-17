"""C4 probe: does COMLab's verdict depend on each enum-typed OBD channel at all?

Run from repo root: python audit/scratch/C4/field_sensitivity.py
For every viable v7 corpus case that runs with OBD, re-run COMLab with each value of the
field substituted and count cases whose (fault_code, confidence, degradation) changes.
Also greps COMLab+registry code (schemas/tests excluded) for readers of each field.
"""
import csv
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
for p in ("labs/comlab", "apps/wired"):
    sys.path.insert(0, str(ROOT / p))

import logging  # noqa: E402
logging.disable(logging.CRITICAL)

import wired.composition as wc  # noqa: E402
from comlab.core.lab_pipeline_aggregator import LabPipelineAggregator  # noqa: E402
from comlab.schemas.vocabulary import (  # noqa: E402
    EngineStateBucket, NodeMAFStatus, NodeMAPStatus, O2FailureMode, TrimAnalyticsGate, VEValidity)
from v7.load_corpus import row_to_raw_inputs  # noqa: E402

FIELDS = {"trim_analytics_gate": TrimAnalyticsGate, "maf_status": NodeMAFStatus, "map_status": NodeMAPStatus,
          "rpm_state_bucket": EngineStateBucket, "o2_failure_mode": O2FailureMode, "ve_validity": VEValidity}

for f in FIELDS:
    r = subprocess.run(["grep", "-rlw", f, "labs/comlab/comlab", "labs/comlab/registry", "--include=*.py"],
                       cwd=ROOT, capture_output=True, text=True)
    readers = [x for x in r.stdout.split() if "/schemas/" not in x and "/tests/" not in x]
    print(f"readers({f}) = {readers}")

cap = {}
orig = LabPipelineAggregator.process
def spy(self, req, *a, **k):
    cap["req"] = req
    return orig(self, req, *a, **k)
LabPipelineAggregator.process = spy
agg = LabPipelineAggregator()
key = lambda o: (o.diagnostic_verdict.fault_code, round(o.diagnostic_verdict.confidence_score, 4),
                 o.execution_meta.degradation_mode)
sens = dict.fromkeys(FIELDS, 0)
n = 0
with open(ROOT / "apps/wired/v7/data/cases_petrol_v7.csv", newline="", encoding="utf-8") as fh:
    for row in csv.DictReader(fh):
        if row["tag"] != "viable":
            continue
        ri = row_to_raw_inputs(row)
        if "obd" not in ri:
            continue
        try:
            wc.diagnose(ri)
        except Exception:
            continue
        req = cap["req"]
        n += 1
        for f, enum in FIELDS.items():
            outs = {key(orig(agg, req.model_copy(update={"obd_live_data": req.obd_live_data.model_copy(update={f: v})})))
                    for v in enum}
            sens[f] += len(outs) > 1
print(f"cases run with OBD: {n}")
for f in FIELDS:
    print(f"{f:20s} all {len(FIELDS[f])} values substituted -> verdict changed in {sens[f]} cases")
