Scope confirmation — T-V3-P4-C3B (C3 signal-pack COMMIT)

I'm the coder for T-V3-P4-C3B, the first unblocked pending row (blocker T-V3-P4-C3A is done). Mode STRICT, dual-gate.

What I will do (ship exactly the C3A Scenario-1 simulation — nothing unsimulated):
- Corpus (cases_petrol_v7.csv): add 4 electrical columns — koeo_map_baro_delta_kpa, module_voltage_loaded_v, dlc_signal_ground_drop_v, bidirectional_fuel_response_ok_bool — populated for the 22 C3 cases from c3_synthetic_seed_2026-07-05 (synthetic=true, incl. the 4 stay-abstained seed values below-gate). Other 272 rows blank. Δλ columns NOT added (deferred, C3A decision).
- Wire producer/consumer mirroring C2B: fields → ingestion.py (OBDLiveDataPayload) → composition.py (_run_obdlab) → load_corpus.py; _PID_DISPATCH + a C3 override in integration_shim.py::_score_rule computing ControlPlausibilityState with the Scenario-1 gates exactly as simulated (lean-bias gnd>0.20; rich-bias koeo_map_baro≥5.0; processor bidir==False ∧ Vmod<12.0; any→CONTROL_REFERENCE_FAULT), boosting EF-001/002/003 (+0.10) and pruning SF-001/002. No registry JSON edits.
- Mint V3_YARDSTICK_2026-07-05-C3B (new csv hash; oracle unchanged 3088a7c3…; run_suite.py untouched); record file; rebind scoreboard. Prior yardsticks immutable.
- Add a shim unit test (3 sub-gates + ABSTAIN incl. one stay-abstained); fill both gate blocks; flip the ledger row.

Signal/noise consumer: CONTROL_REFERENCE_FAULT is read by the EF boost / SF prune branch this task adds in _score_rule; all 4 columns feed that one state (no orphan).

What I will NOT touch: Δλ columns; stronger lift for CSV-125/126 (→C3C); registry JSON; abstain dial (MARGIN=0.02); oracle/run_suite.py; Vault/; no graphify.

One parity risk I'll surface, not hide (task success-criterion #4): the C3A sim applied the boost via an external monkeypatch over unmodified raw_inputs. Adding a live OBD column flips YAML-RULE_NOx_1 from has_obd=False→True, injecting load_corpus OBD defaults the sim never applied. The other 21 already have OBD. So the live score may deviate from the simulated 228 on that one case — I'll report the actual number and reconcile the delta explicitly rather than force-match. Target is top3_family = 228/294, REGRESSIONS: (empty).

Let me begin. First, the corpus CSV.

  Ran 1 shell command

Baseline CSV hash confirmed matches the pinned 3df2e8cb…. The C2 columns are appended at the end. I'll append the 4 C3 columns similarly. Let me write a deterministic Python script to do the CSV edit (append 4 columns, fill 22 C3 rows from the seed). Let me read the seed JSON to get exact values.

  Read 1 file

The seed CSV I already read has the exact per-case values. I'll use the CSV seed as the authoritative source (it's what the sim consumed via the JSON, and both are byte-locked). Let me write the corpus-edit script using the seed CSV values directly.

● Write(v3/apply_c3b_corpus.py)
Wrote 72 lines to v3/apply_c3b_corpus.py
#!/usr/bin/env python3
"""T-V3-P4-C3B — append the 4 C3 electrical columns to the live v7 corpus.

Deterministic corpus edit (idempotent): adds
  koeo_map_baro_delta_kpa, module_voltage_loaded_v,
  dlc_signal_ground_drop_v, bidirectional_fuel_response_ok_bool
to cases_petrol_v7.csv, populated for the 22 C3 cases from the frozen
`c3_synthetic_seed_2026-07-05.csv` side file, blank for all other rows.

Δλ columns (gas_obd_lambda_delta, lambda_perception_delta) are NOT added
… +62 lines

  Thought for 7s

The csv.DictWriter default lineterminator is \r\n — the repo is LF-normalized. I must force \n to avoid rewriting the whole file to CRLF.

● Update(v3/apply_c3b_corpus.py)
Added 1 line, removed 1 line
            filled += 1

    with CORPUS.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


  Thought for 5s

Before running, let me verify the CSV's current quoting/line-ending style so my rewrite matches byte-for-byte in unrelated rows (only the C3 additions should change).

  Thought for 16s, ran 1 shell command

The file is CRLF-terminated (315 CR = 315 LF = 315 rows) with quoted JSON fields — not LF as I assumed. Rewriting with the wrong terminator or quoting style would corrupt 293 untouched rows. Let me detect the exact style and test on a copy, diffing to confirm only C3 columns change.

  Thought for 7s, ran 1 shell command

The file is uniformly CRLF. Let me fix the terminator and test on a copy, diffing to prove only the intended changes land.

● Update(v3/apply_c3b_corpus.py)
Added 1 line, removed 1 line
            filled += 1

    with CORPUS.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\n")
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\r\n")
        writer.writeheader()
        writer.writerows(rows)


  Thought for 11s

A full CSV round-trip risks re-quoting the 293 untouched rows differently. Safer: append columns by line surgery — case_id is the first field (no commas/quotes), so I read it as the prefix before the first comma, and append ,val<CRLF> without touching existing bytes. Let me rewrite the script this way.

● Write(v3/apply_c3b_corpus.py)
Added 33 lines, removed 26 lines
#!/usr/bin/env python3
"""T-V3-P4-C3B — append the 4 C3 electrical columns to the live v7 corpus.

Deterministic corpus edit (idempotent): adds
Deterministic, idempotent corpus edit. Adds
  koeo_map_baro_delta_kpa, module_voltage_loaded_v,
  dlc_signal_ground_drop_v, bidirectional_fuel_response_ok_bool
to cases_petrol_v7.csv, populated for the 22 C3 cases from the frozen
`c3_synthetic_seed_2026-07-05.csv` side file, blank for all other rows.

Δλ columns (gas_obd_lambda_delta, lambda_perception_delta) are NOT added
(deferred — the C3A Scenario-1 decision). Mirrors the C2B corpus-append pattern.
Column *append* is done by pure line surgery so the 293 untouched rows keep
their exact bytes (CRLF endings + existing JSON quoting are preserved). Each
data line's ``case_id`` is the first field (no commas/quotes), read as the
prefix before the first comma. Δλ columns are NOT added (C3A Scenario-1 decision).
No back-solve: values are copied verbatim from the seed side file.
"""
from __future__ import annotations

]


def load_seed() -> dict[str, dict[str, str]]:
    """case_id -> {column: value} for the 22 C3 cases (verbatim from the seed CSV)."""
def load_seed() -> dict[str, list[str]]:
    """case_id -> [value per C3_COLUMNS] for the 22 C3 cases (verbatim from seed CSV)."""
    with SEED.open(newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    seed: dict[str, dict[str, str]] = {}
    for r in rows:
        seed[r["case_id"]] = {c: r[c] for c in C3_COLUMNS}
    return seed
    return {r["case_id"]: [r[c] for c in C3_COLUMNS] for r in rows}


def main() -> int:
    seed = load_seed()
    with CORPUS.open(newline="", encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        fieldnames = list(reader.fieldnames or [])
        rows = list(reader)
    raw = CORPUS.read_bytes()
    if b"koeo_map_baro_delta_kpa" in raw:
        print("C3 columns already present — no change.")
        return 0

    for col in C3_COLUMNS:
        if col not in fieldnames:
            fieldnames.append(col)

    text = raw.decode("utf-8")
    # Split keeping the CRLF terminators intact via splitlines(keepends=True).
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    filled = 0
    for r in rows:
        vals = seed.get(r["case_id"])
        for col in C3_COLUMNS:
            r[col] = vals[col] if vals is not None else ""
    for idx, line in enumerate(lines):
        # Preserve the exact line terminator ("\r\n" here).
        term = ""
        body = line
        for t in ("\r\n", "\n", "\r"):
            if line.endswith(t):
                term, body = t, line[: -len(t)]
                break
        if idx == 0:
            out.append(body + "," + ",".join(C3_COLUMNS) + term)
            continue
        case_id = body.split(",", 1)[0]
        vals = seed.get(case_id)
        if vals is not None:
            filled += 1
            out.append(body + "," + ",".join(vals) + term)
        else:
            out.append(body + "," + "," * (len(C3_COLUMNS) - 1) + term)

    with CORPUS.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames, lineterminator="\r\n")
        writer.writeheader()
        writer.writerows(rows)

    CORPUS.write_bytes("".join(out).encode("utf-8"))
    print(f"C3 columns appended: {C3_COLUMNS}")
    print(f"rows filled (expect 22): {filled}")
    return 0

  Ran 1 shell command

Corpus edit clean: 4 columns appended, 22 C3 rows filled, 0 untouched-column changes, 0 non-C3 leakage. Let me verify line endings preserved and record the new hash.

  Ran 1 shell command

CSV done. New hash 9f530695… (I'll bind this in the mint step). CRLF preserved, case order identical. Task 1 complete. Now the schema fields.
API Error: 400 You have exceeded your daily token limit. You can resume at 2026-07-06 00:00 UTC.

✻ Crunched for 19m 32s

  7 tasks (1 done, 1 in progress, 5 open)
  ◼ ingestion.py: add 4 C3 payload fields
  ◻ composition.py + load_corpus.py: map C3 columns
  ◻ integration_shim.py: _PID_DISPATCH + ControlPlausibilityState
  ◻ Mint V3_YARDSTICK_2026-07-05-C3B + rebind
  ◻ Add shim unit test + run score/diff/gates
   … +1 pending, 1 completed