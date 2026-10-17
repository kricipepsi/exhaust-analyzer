"""C5 probe: every number_input the form renders, driven to its own min and max, through the real
app (AppTest). Reports each bound the form accepts but the run rejects ("Diagnostic calculation
failed: ...").

Baseline = a complete, otherwise-valid form: DNA/VIN on, VIN WME01MC01XH072806 (decodes; narrowband,
MAF, downstream O2), symptom picked, 5 low-idle gas values, the 5 OBD fields OBDLab needs, all 12
mandatory FF PIDs, extended FF ticked. Run: python audit/scratch/C5/boundary_sweep.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from c5_apptest import by_label, errors, new_app, pick_symptom, set_num  # noqa: E402

BASE = {
    "gas_hc": 80, "gas_co": 0.3, "gas_co2": 14.8, "gas_o2": 0.3, "gas_nox": 50,
    "obd_rpm": 800, "obd_ect": 90.0, "obd_stft1": 1.0, "obd_ltft1": 2.0, "obd_o2_up": 0.45,
    "ff_load": 20.0, "ff_rpm": 800, "ff_ect": 90.0, "ff_stft_b1": 1.0, "ff_ltft_b1": 2.0,
    "ff_map": 35, "ff_speed": 0, "ff_ignition": 10.0, "ff_iat": 25.0, "ff_maf": 3.0,
    "ff_throttle": 0.0,
}


def baseline():
    at = new_app()
    at.text_input(key="vin_input").input("WME01MC01XH072806")
    at.run()
    pick_symptom(at, "⬇️ Lack of Power / Hesitation", "Flat / sluggish always")
    by_label(at.checkbox, "Add extended freeze-frame PIDs").check()
    at.run()
    for k, v in BASE.items():
        set_num(at, k, v)
    at.selectbox(key="ff_fss").set_value("CL")
    at.selectbox(key="obd_fss").set_value("CL")
    at.run()
    return at


def click(at):
    by_label(at.button, "🔬 Run Diagnostic Seam").click()
    at.run()
    return errors(at)


def main() -> None:
    t0 = time.time()
    at = baseline()
    base_err = click(at)
    print("baseline errors:", base_err)
    keys = [(n.key, n.min, n.max, n.value) for n in at.number_input]
    print("number_inputs rendered:", len(keys))
    rejected = []
    for key, lo, hi, orig in keys:
        for bound in (lo, hi):
            set_num(at, key, bound)
            err = click(at)
            if err and err != base_err:
                rejected.append((key, bound, err[0][:150]))
        set_num(at, key, orig)
        at.run()
    for r in rejected:
        print("REJECTED", r)
    print(f"bounds tried: {2 * len(keys)}  rejected: {len(rejected)}  ({time.time() - t0:.0f}s)")


if __name__ == "__main__":
    main()
