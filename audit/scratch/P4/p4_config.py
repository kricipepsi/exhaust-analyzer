"""P4 mutation matrix — shared configuration (targets, suites, isolation layout)."""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
SCRATCH = Path(__file__).resolve().parent

# Lab dirs put on PYTHONPATH (copy-relative). apps/wired is deliberately NOT on the path: it would make
# fl_tasks/v7 importable and change the comlab baseline (2 collection errors, R0-2).
LAB_PATHS = [
    "labs/comlab", "labs/dnalab", "labs/dtclab", "labs/gaslab",
    "labs/obdlab", "labs/symptomlab", "labs/vinlab",
]

# suite -> cwd (copy-relative); run as `python -m pytest`, so cwd is on sys.path too.
SUITES = {
    "comlab": "labs/comlab",
    "gaslab": "labs/gaslab",
    "vinlab": "labs/vinlab",
    "ui": "apps/ui",
}

# id -> (file, qualname, owning suite, module import name)
TARGETS = {
    "router.execute_triage_loop": ("labs/comlab/comlab/core/fault_atlas_router.py",
                                   "FaultAtlasRouter.execute_triage_loop", "comlab",
                                   "comlab.core.fault_atlas_router"),
    "router.route": ("labs/comlab/comlab/core/fault_atlas_router.py",
                     "FaultAtlasRouter.route", "comlab", "comlab.core.fault_atlas_router"),
    "shim._score_rule": ("labs/comlab/registry/integration_shim.py", "_score_rule", "comlab",
                         "registry.integration_shim"),
    "gas.apply_differentiators": ("labs/gaslab/gaslab/resolution.py", "apply_differentiators",
                                  "gaslab", "gaslab.resolution"),
    "gas._definitive_match": ("labs/gaslab/gaslab/rule_engine.py", "_definitive_match", "gaslab",
                              "gaslab.rule_engine"),
    "ui.build_diagnose_payload": ("apps/ui/ui_payload.py", "build_diagnose_payload", "ui",
                                  "ui_payload"),
    "vin._resolve_year": ("labs/vinlab/vinlab/decoder.py", "RobustVINDecoder._resolve_year", "vinlab",
                          "vinlab.decoder"),
    "vin._resolve_wmi": ("labs/vinlab/vinlab/decoder.py", "RobustVINDecoder._resolve_wmi", "vinlab",
                         "vinlab.decoder"),
}

# modules whose __file__ must resolve inside the copy, per suite (control iii)
GUARD_MODULES = {
    "comlab": ["comlab.core.fault_atlas_router", "registry.integration_shim"],
    "gaslab": ["gaslab.resolution", "gaslab.rule_engine"],
    "vinlab": ["vinlab.decoder"],
    "ui": ["ui_payload", "comlab.core.fault_atlas_router", "registry.integration_shim",
           "gaslab.rule_engine", "vinlab.decoder"],
}

SAMPLE_CAP = 150
SEED = 20261026

COPY_EXCLUDE = [".git", ".venv-audit", "Vault", "audit", "v3", "graph", "research", "graphify-out",
                "__pycache__", ".hypothesis", ".pytest_cache", ".firecrawl", "node_modules"]
