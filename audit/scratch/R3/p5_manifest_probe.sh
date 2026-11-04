#!/usr/bin/env bash
# T-AUD-1b probes (repo root): (1) closure of requirements.txt vs constraints.txt pins; (2) F-P5-1 repro without -e labs/dnalab;
# (3) F-P5-4 repro: dnalab installed from its own manifest (+ local symptomlab/vinlab via find-links? no: by path) importable.
# Output: JSON on stdout. Needs network for PyPI (pip resolver).
set -uo pipefail
ROOT=$(pwd); W=${TMPDIR:-/tmp}/r3_p5; rm -rf "$W"; mkdir -p "$W"
PY=$(ls -d .venv-audit/bin/python); BASE=$($PY -c 'import sys;print(sys.base_prefix)')/bin/python3.14
$BASE -m venv "$W/v" >/dev/null && "$W/v/bin/pip" -q install -U pip >/dev/null 2>&1
"$W/v/bin/pip" install -q --dry-run --ignore-installed --report "$W/full.json" -r requirements.txt >/dev/null 2>"$W/full.err"; echo "full_rc=$?" > "$W/rc"
grep -v '^-e labs/dnalab' requirements.txt > "$W/req_nodna.txt"; sed -i "s#-c constraints.txt#-c $ROOT/constraints.txt#; s#^-e #-e $ROOT/#" "$W/req_nodna.txt"
"$W/v/bin/pip" install -q --dry-run --ignore-installed --report "$W/nodna.json" -r "$W/req_nodna.txt" >/dev/null 2>"$W/nodna.err"; echo "nodna_rc=$?" >> "$W/rc"
$PY - "$W" <<'PY'
import json,sys,re,pathlib
W=pathlib.Path(sys.argv[1]); rc=dict(l.strip().split('=') for l in open(W/'rc'))
pins={}
for l in open('constraints.txt'):
    l=l.split('#')[0].strip()
    if l: n,v=l.split('=='); pins[re.sub(r'[-_.]+','-',n).lower()]=v.strip()
def rep(p):
    if not p.exists(): return None
    out={}
    for it in json.load(open(p))['install']:
        m=it['metadata']; out[re.sub(r'[-_.]+','-',m['name']).lower()]=(m['version'], bool(it.get('is_direct') and 'dir_info' in it.get('download_info',{})), it['download_info']['url'][:60])
    return out
full=rep(W/'full.json'); nodna=rep(W/'nodna.json')
third={k:v for k,v in (full or {}).items() if not k.startswith('fourdapp-')}
res={"rc":rc,
 "full_dists":len(full or {}),"third_party":len(third),
 "third_party_unpinned":sorted(k for k in third if k not in pins),
 "third_party_version_mismatch":sorted(k for k,v in third.items() if k in pins and pins[k]!=v[0]),
 "pins_not_in_closure":sorted(k for k in pins if k not in third),
 "nodna_dnalab":(nodna or {}).get('fourdapp-dnalab'),
 "nodna_err_tail":open(W/'nodna.err').read().strip().splitlines()[-1:] }
print(json.dumps(res,indent=1,sort_keys=True))
PY
