"""T-COMA-17: the UI shows one notice per gas-sample reason, after the PRD 5.6 flag notices."""
from __future__ import annotations

from types import SimpleNamespace as NS

import ui_payload as U

FLAGS = {f: False for f, _ in U.ROUTING_NOTICES}


def test_gas_sample_invalid_notice() -> None:
    notices = U.routing_notices(NS(**FLAGS, reasons=["GAS_SAMPLE_INVALID"]))
    assert notices == [U.GAS_SAMPLE_NOTICES[0][1]]
    assert "re-sample" in notices[0]


def test_o2_suspect_notice_follows_flag_notices() -> None:
    flags = dict(FLAGS, cold_start_mode=True)
    notices = U.routing_notices(NS(**flags, reasons=["COLD_START_HYPOTHESIS", "GAS_SAMPLE_O2_SUSPECT"]))
    assert notices == [U.ROUTING_NOTICES[3][1], U.GAS_SAMPLE_NOTICES[1][1]]


def test_no_reasons_attribute_gives_flag_notices_only() -> None:
    assert U.routing_notices(NS(**FLAGS)) == []
