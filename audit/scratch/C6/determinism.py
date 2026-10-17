"""Print a hash of every real-VIN decode; run under two PYTHONHASHSEEDs and compare."""
import hashlib, json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import c6_lib as L
out = []
for v in L.real_vins():
    try:
        out.append(L.decode(v).to_json_payload())
    except L.VINDecodeError as e:
        out.append(str(e))
print(len(out), hashlib.sha256(json.dumps(out, sort_keys=True).encode()).hexdigest()[:16])
