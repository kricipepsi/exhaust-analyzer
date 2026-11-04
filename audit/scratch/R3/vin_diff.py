"""Compare two vin_snapshot.py JSON dumps; print changed VINs (make / engine / year / vref window / tech fields)."""
import json, sys
a, b = (json.load(open(p))["vins"] for p in sys.argv[1:3])
fields = sys.argv[3].split(",") if len(sys.argv) > 3 else ["make", "engine", "year", "vref", "disp", "cyl", "fuel", "ind", "euro", "o2", "conf"]
def show(x, f):
    return x.get("error", "ERR") if "error" in x else {k: x[k] for k in f}
rows = []
for vin in sorted(set(a) | set(b)):
    x, y = a.get(vin, {"error": "absent"}), b.get(vin, {"error": "absent"})
    if show(x, fields) != show(y, fields):
        rows.append({"vin": vin, "before": show(x, fields), "after": show(y, fields)})
print(json.dumps(rows, indent=0, sort_keys=True))
