"""D2 probe — diff Pydantic/dataclass field sets declared in design docs vs the code.

Run from the repo root (venv active):
    python audit/scratch/D2/d2_model_fields.py

Doc side: every ``class <Name>(BaseModel|TypedDict):`` or ``@dataclass`` class in a fenced
python block of the COMLab LLD / HLD / vocabulary docs; field = ``name: type`` line.
Code side: the same class name, resolved by import from comlab.* (pydantic
``model_fields`` / dataclass fields) or, failing that, from sibling labs.
Read-only.
"""
from __future__ import annotations

import dataclasses
import importlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "labs/comlab"))

DOCS = [
    "labs/comlab/docs/COMLab_LLD.md",
    "labs/comlab/docs/COMLab_HLD.md",
    "labs/comlab/docs/Vocabulary/DTC_VOCABULARY.md",
    "labs/comlab/docs/Vocabulary/OBD_VOCABULARY.md",
    "labs/comlab/docs/Vocabulary/SEMANTIC_CONTRACT.md",
]
MODULES = [
    "comlab.schemas.ingestion", "comlab.schemas.response", "comlab.schemas.kg",
    "comlab.schemas.lab_dna_views", "comlab.projection", "comlab.core.symptom_router",
    "comlab.core.ecu_hardware_checker", "comlab.core.perception_contradiction",
    "comlab.core.horizon_context_injector", "comlab.core.fault_atlas_router",
    "comlab.core.lab_pipeline_aggregator", "comlab.schemas.vocabulary",
    "dtclab.schemas.dna_view", "dtclab.schemas.payload",
]
CLASS_RE = re.compile(r"^class\s+(\w+)\((BaseModel|TypedDict)\)\s*:")
DC_RE = re.compile(r"^@dataclass")
FIELD_RE = re.compile(r"^\s{4}([a-z_][a-z0-9_]*)\s*:\s*[^=]")


def doc_models(path: Path):
    lines = path.read_text(encoding="utf-8").splitlines()
    in_code, pending_dc = False, False
    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.strip().startswith("```"):
            in_code = not in_code
            i += 1
            continue
        if in_code and DC_RE.match(ln):
            pending_dc = True
            i += 1
            continue
        m = CLASS_RE.match(ln) if in_code else None
        if in_code and not m and pending_dc:
            m = re.match(r"^class\s+(\w+)\s*[:(]", ln)
        if m:
            pending_dc = False
            name, start, fields = m.group(1), i + 1, []
            j = i + 1
            while j < len(lines) and (lines[j].startswith(" ") or not lines[j].strip()):
                if lines[j].strip().startswith("```"):
                    break
                if lines[j].lstrip().startswith(("def ", "@", '"""', "#")):
                    # stop collecting at first method; docstrings skipped by FIELD_RE
                    if lines[j].lstrip().startswith("def "):
                        break
                fm = FIELD_RE.match(lines[j])
                if fm and fm.group(1) not in ("model_config",):
                    fields.append(fm.group(1))
                j += 1
            if fields:
                yield name, start, fields
            i = j
            continue
        i += 1


def code_classes():
    out = {}
    for mod in MODULES:
        try:
            m = importlib.import_module(mod)
        except Exception as exc:  # noqa: BLE001
            print(f"IMPORT-FAIL {mod}: {exc}")
            continue
        for name, obj in vars(m).items():
            if not isinstance(obj, type) or getattr(obj, "__module__", "") != mod:
                continue
            if hasattr(obj, "model_fields"):
                out.setdefault(name, (mod, list(obj.model_fields)))
            elif dataclasses.is_dataclass(obj):
                out.setdefault(name, (mod, [f.name for f in dataclasses.fields(obj)]))
            elif getattr(obj, "__annotations__", None) and hasattr(obj, "__total__"):
                out.setdefault(name, (mod, list(obj.__annotations__)))
    return out


def main() -> None:
    code = code_classes()
    n = 0
    for d in DOCS:
        for name, line, fields in doc_models(ROOT / d):
            if name not in code:
                print(f"NO-CODE {d}:{line} {name} fields={fields}")
                n += 1
                continue
            mod, cf = code[name]
            od = [f for f in fields if f not in cf]
            oc = [f for f in cf if f not in fields]
            tag = "OK     " if not od and not oc else "DIFF   "
            n += bool(od or oc)
            print(f"{tag} {d}:{line} {name} doc={len(fields)} code={len(cf)} @ {mod}"
                  + (f" only_doc={od}" if od else "") + (f" only_code={oc}" if oc else ""))
    print(f"\nTOTAL DIFF/NO-CODE: {n}")


if __name__ == "__main__":
    main()
