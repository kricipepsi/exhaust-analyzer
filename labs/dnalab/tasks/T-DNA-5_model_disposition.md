# T-DNA-5 — `model` disposition via DBS variance check (DNA10 Q8)

### Goal ###

Decide, with evidence, whether `VinDNA` needs a `model` field. Today: DTCLab's own
mirror (`dtclab/.../dna_view.py`) **requires** `model: str`, but COMLab's
`DtcLabDnaView` omits it and `VinDNA` never emits it — a latent inconsistency. DNA10
Q8 and `DNAresearch.md` ask whether finer identity (`model`/variant) changes the
diagnosis or whether `engine_code` + displacement + induction already pins it.

This is settled empirically against DBS (audit: DBS answers Q8), not by opinion.

### Method (light DBS analysis) ###

Group `DBS/docs/vehicles_petrol_specimens.csv` by `P15_engine_code` and measure
within-engine_code spread of the CoC targets that actually drive diagnosis —
`V112_lambda`, `V101_CO_low_idle`, `V111_CO_high_idle`, `P14_rated_rpm`. If
within-code variance is low (the same engine_code pins the targets regardless of
`D3_commercial_name`/model), `model` adds no diagnostic signal and stays absent.

### Named signal/noise consumer ###

`DtcLabDnaView.model` (DTCLab mirror). Decision outputs one of:
- **KEEP-EMPTY (expected):** `model` adds no signal → it does **not** ship on
  `VinDNA`; relax DTCLab's mirror requirement to `Optional`/drop via **COMLab-D**.
  No new field — the signal/noise rule forbids adding an inert field.
- **ADD (only if variance justifies):** `model` ships with DTCLab routing as its named
  consumer (proposal), citing the variance finding.

### Success criteria ###

- `docs/research/Q8_model_variance.md`: the within-engine_code variance numbers, the
  decision, and the rationale (measured, with the column/grouping used).
- If KEEP-EMPTY: a COMLab-D line for relaxing the DTCLab mirror `model` requirement
  (DNA task does not edit DTCLab code).
- If ADD: a proposal entry + draft contract §4.1 amendment naming the DTCLab consumer.
- No `VinDNA` schema change unless the variance evidence justifies it.

### Files to touch ###

- `labs/dnalab/docs/research/Q8_model_variance.md` (CREATE — the finding)
- `labs/comlab/comlab/config/proposals/entries.yaml` (ADD COMLab-D note, or the ADD
  proposal — whichever the decision yields)

### Out of scope ###

Editing DTCLab code (COMLab-D). Any change to `make`/`model_year` (those already ship).
Re-deriving VIN decode resolution (DNA10 Q2, already answered in the audit).

### On completion ###

Both gates clean in `progress_notes/T-DNA-5.md` (here the "gate" is the data finding +
decision, since this is an analysis/decision task with no production code unless ADD);
flip T-DNA-5 → `done`. STOP.

### Verification ###

```bash
cd $HOME/mnt/4DLab/4DLabV2
python3.14 - <<'PY'
import csv, statistics as st
from collections import defaultdict
g=defaultdict(list)
with open('DBS/docs/vehicles_petrol_specimens.csv',encoding='utf-8',errors='replace') as f:
    for r in csv.DictReader(f,delimiter=';'):
        v=r.get('V112_lambda','').strip()
        if r.get('P15_engine_code') and v:
            try: g[r['P15_engine_code']].append(float(v))
            except ValueError: pass
sp=[st.pstdev(v) for v in g.values() if len(v)>3]
print('engine_codes w/ >3 specimens:',len(sp))
print('median within-code lambda stdev:', round(st.median(sp),4) if sp else 'n/a')
PY
```
