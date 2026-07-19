import sys, csv, random, re, datetime
sys.path.insert(0,"/agent_workspace/labs/vinlab")
from vinlab.decoder import RobustVINDecoder, VINDecodeError, ChassisNumberError, pre_clean_vin
from pathlib import Path

CSVFILE="/agent_workspace/docs/Nio_vozila_3.csv"
DATA=Path("/agent_workspace/labs/vinlab/vinlab/data")
SEED=42; N=200
dec=RobustVINDecoder(DATA)

rows=[]
with open(CSVFILE,encoding="latin-1",newline="") as fh:
    for row in csv.DictReader(fh,delimiter=";"):
        vin=(row.get("E-VIN") or "").strip()
        eng=(row.get("P15-Oznaka motorja") or "").strip()
        fuel=(row.get("P13-Vrsta goriva (oznaka)") or "").strip()
        if len(vin)==17 and eng and fuel.upper()=="P":
            rows.append((vin,eng))
random.seed(SEED); sample=random.sample(rows,N)

def norm(s): return re.sub(r"[^A-Z0-9]","",s.upper())
CORRUPT=re.compile(r"[^\x20-\x7E]")           # non-printable / mojibake
JUNK_PREFIX=("TIP","TRI","TUP","UNK-")

decode_ok=decode_rej=0
resolved=exact=contained=miss=none=0
corrupt_codes=[]; misses=[]
for vin,eng in sample:
    try:
        dec.decode_vin_payload(vin); decode_ok+=1
    except (VINDecodeError,ChassisNumberError): decode_rej+=1
    try:
        v=pre_clean_vin(vin); brand=dec._resolve_wmi(v).get("brand","")
        erow=dec._resolve_engine(v,brand,[])
    except Exception: erow=None
    code=(erow or {}).get("engine_code","").strip() if erow else ""
    if not code:
        none+=1; continue
    resolved+=1
    if CORRUPT.search(code) or code.startswith(JUNK_PREFIX):
        corrupt_codes.append((vin,eng,code))
    ne,nc=norm(eng),norm(code)
    if nc==ne: exact+=1
    elif nc and (nc in ne or ne in nc): contained+=1
    else:
        miss+=1
        if len(misses)<20: misses.append((vin,eng,code))

pct=lambda x: f"{x} ({x/N:.1%})"
now=datetime.date.today().isoformat()
out=f"""# VINLab — Engine-number-from-VIN test report

**Date:** {now}  ·  **Lab:** `labs/vinlab`  ·  **Source:** `docs/Nio_vozila_3.csv`
**Sample:** {N} random VINs, `random.seed({SEED})`, filtered to petrol (`P13-Vrsta goriva (oznaka) == "P"`), 17-char VIN, non-empty `P15-Oznaka motorja`.
**Population after filter:** {len(rows):,} rows.

## What "engine number" means here
The CSV field `P15-Oznaka motorja` is the engine code. VINLab does **not** expose an
engine number in its public output (`VinDNA`); the code is computed only inside the
decoder by `_resolve_engine`, keyed on brand + VDS = `vin[3:8]` against
`vinlab/data/vds_engine_map.csv` (a frozen lookup table the decoder reads).
This test therefore reads that private method, not the official `decode()` result.

## Results
| Metric | Count |
|---|---|
| `decode()` succeeded | {pct(decode_ok)} |
| `decode()` rejected (out-of-scope) | {pct(decode_rej)} |
| Engine code resolved (non-empty) | {pct(resolved)} |
| No engine code resolved | {pct(none)} |
| **Exact match to P15** (normalized) | {pct(exact)} |
| **Near match** (one code contained in other) | {pct(contained)} |
| Resolved but wrong | {pct(miss)} |

Exact + near = **{exact+contained} / {N} = {(exact+contained)/N:.1%}** of the sample.
Match rate among *resolved* codes only: exact {exact}/{resolved}, near {contained}/{resolved}.

## Two root causes
**1. Structural — VDS does not encode the engine variant.** `vin[3:8]` maps to at most
one code per brand, so distinct engines sharing a VDS collapse to a single guess:
"""
for vin,eng,code in misses[:6]:
    out+=f"- `{vin}` — P15 `{eng}` → resolved `{code}`\n"
out+=f"""
**2. Data quality — `vds_engine_map.csv` holds corrupted codes.** {len(corrupt_codes)} of the
{resolved} resolved codes in this sample are mojibake or carry junk prefixes
(`TIP`/`TRI`/`TUP`/`UNK-`):
"""
for vin,eng,code in corrupt_codes[:10]:
    out+=f"- `{vin}` — P15 `{eng}` → resolved `{code!r}`\n"

out+=f"""
## Conclusion
On held-out data, engine numbers are **not** reliably recovered from VIN by VINLab:
~{(exact+contained)/N:.0%} of petrol VINs yield a matching P15 code. The route is limited
by design (VDS granularity) and further degraded by corrupted rows in the frozen
`vds_engine_map.csv`. Fixing the map's mojibake/junk entries would lift the ceiling but
cannot overcome the structural VDS-granularity limit.

## Reproduce
`python3 tools/vin_engine_number_report.py` (petrol filter, seed {SEED}, N={N}).
"""
Path("/agent_workspace/labs/vinlab/VIN_engine_number_test_report.md").write_text(out,encoding="utf-8")
# also save the runnable script into the lab's tools/ for reproducibility
Path("/agent_workspace/labs/vinlab/tools/vin_engine_number_report.py").write_text(open(__file__).read(),encoding="utf-8")
print("exact",exact,"contained",contained,"miss",miss,"none",none,"resolved",resolved)
print("corrupt",len(corrupt_codes),"decode_ok",decode_ok,"decode_rej",decode_rej,"pop",len(rows))
print("WROTE /agent_workspace/labs/vinlab/VIN_engine_number_test_report.md")
