"""Unit tests for vinlab.overlay.cylinder_heuristic — T-VL-7."""

from __future__ import annotations

from vinlab.overlay.cylinder_heuristic import infer_cylinder

# ---------------------------------------------------------------------------
# Brand-specific rule tests — source: T-VL-7 success criteria
# ---------------------------------------------------------------------------


def test_bmw_n52b25():
    hint = infer_cylinder("N52B25", 2.5, "BMW")
    assert hint.count == 6
    assert hint.config == "I6"
    assert hint.source == "brand_rule"


def test_hyundai_g4ke():
    hint = infer_cylinder("G4KE", 2.4, "HYUNDAI")
    assert hint.count == 4
    assert hint.config == "I4"
    assert hint.source == "brand_rule"


def test_honda_k20a():
    hint = infer_cylinder("K20A", 2.0, "HONDA")
    assert hint.count == 4
    assert hint.config == "I4"
    assert hint.source == "brand_rule"


def test_toyota_1gr_fe():
    hint = infer_cylinder("1GR-FE", 4.0, "TOYOTA")
    assert hint.count == 6
    assert hint.config == "V6"
    assert hint.source == "brand_rule"


def test_subaru_ej20():
    hint = infer_cylinder("EJ20", 2.0, "SUBARU")
    assert hint.count == 4
    assert hint.config == "BOXER_4"
    assert hint.source == "brand_rule"


def test_volvo_b5254t():
    hint = infer_cylinder("B5254T", 2.5, "VOLVO")
    assert hint.count == 5
    assert hint.config == "I5"
    assert hint.induction == "TURBOCHARGED"
    assert hint.source == "brand_rule"


def test_mitsubishi_4g93():
    hint = infer_cylinder("4G93", 1.8, "MITSUBISHI")
    assert hint.count == 4
    assert hint.config == "I4"
    assert hint.source == "brand_rule"


def test_mazda_b6():
    hint = infer_cylinder("B6", 1.6, "MAZDA")
    assert hint.count == 4
    assert hint.config == "I4"
    assert hint.source == "brand_rule"


# ---------------------------------------------------------------------------
# Displacement fallback tests — source: T-VL-7 task spec
# ---------------------------------------------------------------------------


def test_disp_fallback_1_0l():
    hint = infer_cylinder("UNKNOWN_CODE", 1.0, "UNKNOWN")
    assert hint.count == 3
    assert hint.config == "I3"
    assert hint.source == "disp_fallback"


def test_disp_fallback_2_0l():
    hint = infer_cylinder("UNKNOWN_CODE", 2.0, "UNKNOWN")
    assert hint.count == 4
    assert hint.config == "I4"
    assert hint.source == "disp_fallback"


def test_disp_fallback_3_0l():
    hint = infer_cylinder("UNKNOWN_CODE", 3.0, "UNKNOWN")
    assert hint.count == 6
    assert hint.config == "V6"
    assert hint.source == "disp_fallback"


def test_disp_fallback_4_5l():
    hint = infer_cylinder("UNKNOWN_CODE", 4.5, "UNKNOWN")
    assert hint.count == 8
    assert hint.config == "V8"
    assert hint.source == "disp_fallback"


# ---------------------------------------------------------------------------
# Edge-case / coverage tests
# ---------------------------------------------------------------------------


def test_empty_code_uses_disp_fallback():
    hint = infer_cylinder("", 2.0, "BMW")
    assert hint.count == 4
    assert hint.source == "disp_fallback"


def test_none_code_uses_disp_fallback():
    hint = infer_cylinder("", 3.0, "TOYOTA")  # empty str (contract: caller passes "")
    assert hint.count == 6
    assert hint.source == "disp_fallback"


def test_unresolved_returns_zero():
    hint = infer_cylinder("XYZ_WEIRD", 0.0, "UNKNOWN")
    assert hint.count == 0
    assert hint.source == "unresolved"


def test_bmw_n20_turbo():
    hint = infer_cylinder("N20B20", 2.0, "BMW")
    assert hint.count == 4
    assert hint.config == "I4"
    # N20 is not a turbo family per the spec


def test_bmw_n55_turbo():
    hint = infer_cylinder("N55B30", 3.0, "BMW")
    assert hint.count == 6
    assert hint.config == "I6"
    assert hint.induction == "TURBOCHARGED"


def test_volvo_b4204t():
    hint = infer_cylinder("B4204T", 2.0, "VOLVO")
    assert hint.count == 4
    assert hint.config == "I4"
    assert hint.induction == "TURBOCHARGED"


def test_volvo_no_t_na():
    hint = infer_cylinder("B4204S", 2.0, "VOLVO")
    assert hint.count == 4
    assert hint.induction == "NATURALLY_ASPIRATED"


def test_nissan_vq_v6():
    hint = infer_cylinder("VQ35DE", 3.5, "NISSAN")
    assert hint.count == 6
    assert hint.config == "V6"


def test_mitsubishi_6g_v6():
    hint = infer_cylinder("6G72", 3.0, "MITSUBISHI")
    assert hint.count == 6
    assert hint.config == "V6"


def test_subaru_ez_boxer6():
    hint = infer_cylinder("EZ30", 3.0, "SUBARU")
    assert hint.count == 6
    assert hint.config == "BOXER_6"


def test_toyota_uz_v8():
    hint = infer_cylinder("1UZ-FE", 4.0, "TOYOTA")
    assert hint.count == 8
    assert hint.config == "V8"


def test_toyota_az_i4():
    hint = infer_cylinder("2AZ-FE", 2.4, "TOYOTA")
    assert hint.count == 4
    assert hint.config == "I4"


def test_mercedes_m271():
    hint = infer_cylinder("M271.940", 1.8, "MERCEDES")
    assert hint.count == 4
    assert hint.config == "I4"


def test_mercedes_m112():
    hint = infer_cylinder("M112.970", 3.2, "MERCEDES-BENZ")
    assert hint.count == 6
    assert hint.config == "V6"


def test_kia_g4fa():
    hint = infer_cylinder("G4FA", 1.4, "KIA")
    assert hint.count == 4
    assert hint.config == "I4"


def test_renault_k4m():
    hint = infer_cylinder("K4M-700", 1.6, "RENAULT")
    assert hint.count == 4
    assert hint.config == "I4"


def test_subaru_fa20():
    hint = infer_cylinder("FA20", 2.0, "SUBARU")
    assert hint.count == 4
    assert hint.config == "BOXER_4"


def test_disp_fallback_5_5l():
    hint = infer_cylinder("BIG_BLOCK", 5.5, "UNKNOWN")
    assert hint.count == 12
    assert hint.config == "V12"
    assert hint.source == "disp_fallback"


def test_disp_fallback_zero():
    hint = infer_cylinder("", 0.0, "UNKNOWN")
    assert hint.count == 0
    assert hint.source == "unresolved"


def test_skoda_dispatches_vw_audi():
    hint = infer_cylinder("BSE", 1.6, "SKODA")
    assert hint.count == 4
    assert hint.config == "I4"
    assert hint.source == "brand_rule"


def test_seat_dispatches_vw_audi():
    hint = infer_cylinder("CGPA", 1.2, "SEAT")
    assert hint.count == 3
    assert hint.config == "I3"


def test_bmw_m62_v8():
    hint = infer_cylinder("M62B44", 4.4, "BMW")
    assert hint.count == 8
    assert hint.config == "V8"


def test_bmw_b48():
    hint = infer_cylinder("B48B20", 2.0, "BMW")
    assert hint.count == 4
    assert hint.config == "I4"


def test_bmw_simple_rule_4cyl():
    hint = infer_cylinder("184S1", 1.8, "BMW")
    assert hint.count == 4
    assert hint.config == "I4"


def test_bmw_simple_rule_6cyl():
    hint = infer_cylinder("256S1", 2.5, "BMW")
    assert hint.count == 6
    assert hint.config == "I6"


def test_psa_xu_family():
    hint = infer_cylinder("XU10J4", 2.0, "PEUGEOT")
    assert hint.count == 4
    assert hint.config == "I4"


def test_psa_es_family():
    hint = infer_cylinder("ES9J4S", 3.0, "CITROEN")
    assert hint.count == 4
    assert hint.config == "I4"


def test_audi_as_vw_group():
    hint = infer_cylinder("CDL", 2.0, "AUDI")
    assert hint.count == 4
    assert hint.config == "I4"


def test_nissan_ga_i4():
    hint = infer_cylinder("GA16DE", 1.6, "NISSAN")
    assert hint.count == 4
    assert hint.config == "I4"


def test_nissan_tb_turbo():
    hint = infer_cylinder("TB48DE", 4.8, "NISSAN")
    assert hint.count == 4
    assert hint.config == "I4"
    assert hint.induction == "TURBOCHARGED"


def test_honda_jseries_v6_if_disp_ok():
    hint = infer_cylinder("J30A", 3.0, "HONDA")
    assert hint.count == 6
    assert hint.config == "V6"


def test_dacia_renault_i3():
    hint = infer_cylinder("H5F", 1.0, "DACIA")
    assert hint.count == 3
    assert hint.config == "I3"


def test_i3_induction_turbo():
    hint = infer_cylinder("B38", 1.2, "BMW")
    # B38 → first digit 3 → ≤4 → disp fallback (1.2L → I3)
    # but the [NBMS] pattern won't match "B38" (only 2 digits after B, not 3)
    # Actually B38 → m = re.match(r'^([NBMS])(\d)(\d)', "B38") → B, 3, 8 → matches!
    # tens = 3, ≤4 → disp=1.2 → I3
    assert hint.count == 3
    assert hint.config == "I3"
    assert hint.induction == "TURBOCHARGED"
