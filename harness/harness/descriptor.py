"""Module descriptor — typed schema for the generative test harness.

Lab-agnostic: imports no lab runtime code. Each forked suite supplies its own
ModuleDescriptor via a builder function (e.g. build_gaslab_descriptor()).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class FieldRange:
    """One input field's plausible range (for boundary/noise generators)."""

    name: str
    type_: str  # "int", "float", "bool", "str", "Optional[float]"
    min_: float | None = None
    max_: float | None = None
    enum_values: list[str] | None = None


@dataclass
class FaultBox:
    """One fault signature's region in feature space.

    Dimensions map CSV column names to (min, max) in that column's units.
    Boxes may overlap — overlap analysis is T-TH-2.
    """

    signature: str
    dimensions: dict[str, tuple[float, float]]
    source: str  # wiki citation


@dataclass
class ModuleDescriptor:
    """Lab-agnostic module descriptor consumed by the generative harness.

    Fields:
        name: Human-readable label for the module.
        fields: Plausible-range descriptors for every input column.
        boxes: Fault-box table {signature: FaultBox}.
        build_args: (row: dict) -> tuple of args for entry_point.
        entry_point: Callable that runs the module.
        extract_expected: (row: dict) -> dict of expected values.
        diff: (actual, expected: dict) -> list of mismatch strings.
    """

    name: str
    fields: list[FieldRange]
    boxes: dict[str, FaultBox]
    build_args: Callable[[dict[str, str]], tuple]
    entry_point: Callable[..., Any]
    extract_expected: Callable[[dict[str, str]], dict[str, Any]]
    diff: Callable[[Any, dict[str, Any]], list[str]]

    def get_field(self, name: str) -> FieldRange | None:
        for f in self.fields:
            if f.name == name:
                return f
        return None


# ---------------------------------------------------------------------------
# GASLab descriptor builder (moved to labs/gaslab/tests/fixtures/descriptor.py)
# ---------------------------------------------------------------------------

try:
    # If labs/gaslab is on PYTHONPATH, tests/fixtures/descriptor.py is importable as tests.fixtures.descriptor
    from tests.fixtures.descriptor import build_gaslab_descriptor
except ImportError:
    try:
        from gaslab.tests.fixtures.descriptor import build_gaslab_descriptor
    except ImportError:
        def build_gaslab_descriptor() -> ModuleDescriptor:
            raise ImportError(
                "build_gaslab_descriptor could not be imported. "
                "Ensure labs/gaslab is in your PYTHONPATH."
            )

