#!/usr/bin/env python3
"""Extract TecDoc 1Q2019 engine facts for the engine codes of vds_engine_map.csv.

T-VINA-13a. Reads <dbs-root>/1Q2019/ (tab-separated CSV dumps, no header,
column lists from install_database/db.sql) read-only and writes one row per
(folded brand, normalised code) pair of the engine map that TecDoc knows under
an allowed manufacturer. T-VINA-13b merges the output into vref.db.

Match tiers (first non-empty wins, then the petrol filter):
  T0   normalised Description == code, manufacturer folds equal to the brand
  T1   code == a paren alias, the head token or the whole part before the
       parentheses of Description (all-digit head/whole keys not emitted)
  T0A  T0 under the brand's same-company alias (BRAND_ALIASES)

Stdlib only. Usage:
  DBS_ROOT=D:/4DLab/4DLabV2/DBS python tools/extract_tecdoc_1q2019.py [--out PATH]
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

TOOLS_DIR = Path(__file__).resolve().parent
DEFAULT_MAP = TOOLS_DIR.parent / "vinlab" / "data" / "vds_engine_map.csv"
DEFAULT_OUT = TOOLS_DIR / "data" / "tecdoc_1q2019_engine_extract.csv"

TABLES = ("manufacturers", "engines", "items_atributes", "passengercars", "passengercars_link_engines")

# Same-company aliases only (plan, approved in correction 01): map brand fold -> TecDoc manufacturer fold.
# Joint ventures (AUDI (FAW), NISSAN (DONGFENG), ...) and platform shares (HYUNDAI/KIA) are not aliases.
BRAND_ALIASES = {
    "VOLKSWAGEN": "VW",
    "GENESIS": "HYUNDAI",
    "FORD": "FORDUSA",
    "BMWI": "BMW",
}

PETROL_ENGINE_TYPES = frozenset({"Petrol Engine", "Petrol Engine (two-stroke)"})

PORT_INJECTION = frozenset({
    "Intake Manifold Injection/ Carburettor", "Petrol Injection", "Multipoint Injection",
    "Motronic", "Intake Manifold Injection",
})
DIRECT_INJECTION = "Direct Injection"
DUAL_INJECTION = "Manifold Injection/Direct Injection"
CARBURETTOR = frozenset({
    "Carburettor", "Multi-stage Carburettor", "Electronic Carburettor", "Double-barrel Carburettor",
})
TURBOCHARGED = frozenset({
    "Turbo/Intercooler", "Exhaust Turbocharger", "Bi-Turbo/Intercooler", "Turbo", "Regulated 2-stage charging",
})
SUPERCHARGED = frozenset({"Compressor", "G-Charger"})
TWINCHARGER = "Turbocharger/Compressor"
V_ENGINE = frozenset({"V", "VR", "W", "V6", "V8"})
NOT_V_ENGINE = frozenset({"Straight", "BOXER", "Rotor, wankel engine"})
VALVETRAIN = {"DOHC": "DOHC", "SOHC/OHC": "SOHC", "OHV": "OHV", "CIH": "CIH"}

_CAPACITY_RE = re.compile(r"(\d+) ccm")
_EURO_RE = re.compile(r"Euro ?([1-6])(?: \(D\1\))?")
_PAREN_RE = re.compile(r"\s*([^()]+?)\s*\(([^()]+)\)\s*")
OPEN_DATE = "0000"

FIELDS: tuple[str, ...] = (
    "displacement_cc", "cylinder_count", "fuel_delivery_type", "induction_type", "has_turbo",
    "has_gdi", "is_v_engine", "valvetrain_type", "euro_norm",
)
COLUMNS: tuple[str, ...] = (
    "brand", "engine_code", "match_tier", "status", "tecdoc_engine_ids", "tecdoc_description",
    *FIELDS, "my_start", "my_end", "n_cars",
)


@dataclass
class Report:
    """What the run prints besides the CSV (R1, R6)."""

    tables: list[tuple[str, int, int, int]]  # (table, rows read, rows skipped, column count)
    population: int
    map_rows_without_code: int
    hits: Counter[str]  # pairs per tier, before the petrol filter
    no_row: Counter[str]  # other_manufacturer, non_petrol, no_code
    other: Counter[tuple[str, str]]  # (brand, TecDoc manufacturers) of the other-manufacturer pairs
    twincharger_rows: int
    kept_fuel_types: Counter[str]


def _fold_brand(raw: str) -> str:
    """Copy of vinlab.decoder._fold_brand (stdlib rule); test_fold_matches_vinlab pins parity."""
    decomposed = unicodedata.normalize("NFKD", raw)
    without_diacritics = "".join(char for char in decomposed if not unicodedata.combining(char))
    return re.sub(r"[^A-Z0-9]+", "", without_diacritics.upper())


def _normalise_code(raw: str) -> str:
    """Copy of vinlab.db.tecdoc_query._normalise_code: uppercase, alphanumeric only."""
    return re.sub(r"[^A-Z0-9]", "", raw.upper())


def _table_columns(ddl: str, table: str) -> list[str]:
    """Column names of `CREATE TABLE `<table>`` in db.sql, in order."""
    m = re.search(r"CREATE TABLE `%s` \((.*?)\n\)" % re.escape(table), ddl, re.S)
    if m is None:
        raise ValueError(f"db.sql has no CREATE TABLE for {table}")
    return re.findall(r"^\s*`(\w+)`", m.group(1), re.M)


def _read_table(src: Path, table: str, columns: list[str], counts: Counter[str]) -> Iterator[dict[str, str]]:
    """Rows of <src>/<table>.csv as dicts; a row whose field count differs is counted and skipped."""
    with (src / f"{table}.csv").open(encoding="utf-8", newline="") as fh:
        for row in csv.reader(fh, delimiter="\t", quoting=csv.QUOTE_NONE):
            if len(row) != len(columns):
                counts[f"{table}:skipped"] += 1
                continue
            counts[f"{table}:rows"] += 1
            yield dict(zip(columns, row))


def _code_keys(description: str) -> tuple[str, set[str]]:
    """The T0 key and the T1 keys of one engine Description."""
    t0 = _normalise_code(description)
    keys: set[str] = set()
    soft: set[str] = set()
    m = _PAREN_RE.fullmatch(description)
    if m:
        keys.add(_normalise_code(m.group(2)))
        soft.add(_normalise_code(m.group(1)))
    tokens = description.split()
    if tokens:
        soft.add(_normalise_code(tokens[0]))
    keys |= {k for k in soft if not k.isdigit()}  # C1: an all-digit head/whole key is a model name
    keys.discard(t0)
    keys.discard("")
    return t0, keys


def _engine_fields(attrs: dict[str, str]) -> dict[str, str]:
    """The 9 derived fields of one engine, in vref.db vocabulary; blank when TecDoc does not say."""
    capacity = _CAPACITY_RE.fullmatch(attrs.get("Capacity", ""))
    cylinders = attrs.get("NumberOfCylinders", "")
    mixture = attrs.get("FuelMixture", "")
    charge = attrs.get("ChargeType", "")
    construction = attrs.get("EngineConstruction", "")
    euro = _EURO_RE.fullmatch(attrs.get("EmissionNorm", ""))

    if mixture in PORT_INJECTION:
        fuel_delivery, has_gdi = "PORT_INJECTION", "0"
    elif mixture == DIRECT_INJECTION:
        fuel_delivery, has_gdi = "GDI", "1"
    elif mixture == DUAL_INJECTION:
        fuel_delivery, has_gdi = "", "1"
    elif mixture in CARBURETTOR:
        fuel_delivery, has_gdi = "", "0"
    else:
        fuel_delivery, has_gdi = "", ""

    if charge == "Naturally Aspirated Engine":
        induction, has_turbo = "NATURALLY_ASPIRATED", "0"
    elif charge in TURBOCHARGED:
        induction, has_turbo = "TURBOCHARGED", "1"
    elif charge in SUPERCHARGED:
        induction, has_turbo = "SUPERCHARGED", "0"
    elif charge == TWINCHARGER:
        induction, has_turbo = "", "1"  # C3
    else:
        induction, has_turbo = "", ""

    if construction in V_ENGINE:
        is_v = "1"
    elif construction in NOT_V_ENGINE:
        is_v = "0"
    else:
        is_v = ""

    return {
        "displacement_cc": capacity.group(1) if capacity else "",
        "cylinder_count": cylinders if cylinders.isdigit() else "",
        "fuel_delivery_type": fuel_delivery,
        "induction_type": induction,
        "has_turbo": has_turbo,
        "has_gdi": has_gdi,
        "is_v_engine": is_v,
        "valvetrain_type": VALVETRAIN.get(attrs.get("CylinderConstruction", ""), ""),
        "euro_norm": f"euro{euro.group(1)}" if euro else "",
    }


def extract(dbs_root: Path, map_path: Path) -> tuple[list[dict[str, str]], Report]:
    """Join the engine map with TecDoc 1Q2019. Returns the sorted rows and the report data."""
    src = dbs_root / "1Q2019"
    ddl = (src / "install_database" / "db.sql").read_text(encoding="utf-8")
    cols = {t: _table_columns(ddl, t) for t in TABLES}
    counts: Counter[str] = Counter()

    manufacturer = {r["id"]: _fold_brand(r["Description"])
                    for r in _read_table(src, "manufacturers", cols["manufacturers"], counts)}
    description: dict[str, str] = {}
    t0_index: dict[tuple[str, str], set[str]] = defaultdict(set)
    t1_index: dict[tuple[str, str], set[str]] = defaultdict(set)
    known_under: dict[str, set[str]] = defaultdict(set)
    for r in _read_table(src, "engines", cols["engines"], counts):
        eid, maker = r["id"], manufacturer.get(r["manufacturer"], "")
        description[eid] = r["Description"]
        t0, t1_keys = _code_keys(r["Description"])
        t0_index[(maker, t0)].add(eid)
        known_under[t0].add(maker)
        for k in t1_keys:
            t1_index[(maker, k)].add(eid)
            known_under[k].add(maker)

    attrs: dict[str, dict[str, str]] = defaultdict(dict)
    for r in _read_table(src, "items_atributes", cols["items_atributes"], counts):
        if r["IsEngine"] == "1" and r["item_id"] in description:
            attrs[r["item_id"]][r["AttributeType"]] = r["DisplayValue"]
    car_dates = {r["id"]: (r["From"][:4], r["To"][:4])
                 for r in _read_table(src, "passengercars", cols["passengercars"], counts)}
    cars_of: dict[str, set[str]] = defaultdict(set)
    for r in _read_table(src, "passengercars_link_engines", cols["passengercars_link_engines"], counts):
        if r["car_id"] in car_dates:
            cars_of[r["engine_id"]].add(r["car_id"])

    spellings: dict[tuple[str, str], tuple[set[str], set[str]]] = defaultdict(lambda: (set(), set()))
    map_rows_without_code = 0
    with map_path.open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            code = _normalise_code(r["engine_code"] or "")
            if not code:
                map_rows_without_code += 1
                continue
            brands, codes = spellings[(_fold_brand(r["brand"] or ""), code)]
            brands.add(r["brand"])
            codes.add(r["engine_code"])

    rows: list[dict[str, str]] = []
    no_row: Counter[str] = Counter()
    hits: Counter[str] = Counter()
    other: Counter[tuple[str, str]] = Counter()
    twincharger_rows = 0
    kept_fuel_types: Counter[str] = Counter()
    for key in sorted(spellings):
        brand, code = key
        alias = BRAND_ALIASES.get(brand)
        tier, ids = "", set()
        for name, index, maker in (("T0", t0_index, brand), ("T1", t1_index, brand), ("T0A", t0_index, alias)):
            if maker is not None and index.get((maker, code)):
                tier, ids = name, index[(maker, code)]
                break
        if not tier:
            if known_under.get(code):
                no_row["other_manufacturer"] += 1
                other[(brand, ",".join(sorted(known_under[code])))] += 1
            else:
                no_row["no_code"] += 1
            continue
        hits[tier] += 1
        kept = sorted((i for i in ids if attrs[i].get("EngineType") in PETROL_ENGINE_TYPES), key=int)
        if not kept:
            no_row["non_petrol"] += 1
            continue

        per_engine = [_engine_fields(attrs[i]) for i in kept]
        row = {"brand": min(spellings[key][0]), "engine_code": min(spellings[key][1]), "match_tier": tier}
        ambiguous = False
        for f in FIELDS:
            values = {e[f] for e in per_engine}  # blank counts as a value: an id that says nothing does not agree
            agreed = len(values) == 1
            row[f] = next(iter(values)) if agreed else ""
            ambiguous |= not agreed
        family = len({_normalise_code(description[i]) for i in kept}) > 1
        row["status"] = "AMBIGUOUS" if ambiguous else "FAMILY" if family else "OK"
        row["tecdoc_engine_ids"] = ";".join(kept)
        row["tecdoc_description"] = ";".join(sorted({description[i] for i in kept}))

        cars = set().union(*(cars_of.get(i, set()) for i in kept))
        starts = [car_dates[c][0] for c in cars if car_dates[c][0] != OPEN_DATE]
        ends = [car_dates[c][1] for c in cars]
        row["my_start"] = min(starts) if starts else ""
        row["my_end"] = "" if not ends or OPEN_DATE in ends else max(ends)
        row["n_cars"] = str(len(cars))
        rows.append(row)

        twincharger_rows += any(attrs[i].get("ChargeType") == TWINCHARGER for i in kept)
        for i in kept:
            kept_fuel_types[attrs[i].get("FuelType", "")] += 1

    rows.sort(key=lambda r: (_fold_brand(r["brand"]), _normalise_code(r["engine_code"])))
    report = Report(
        tables=[(t, counts[f"{t}:rows"], counts[f"{t}:skipped"], len(cols[t])) for t in TABLES],
        population=len(spellings),
        map_rows_without_code=map_rows_without_code,
        hits=hits,
        no_row=no_row,
        other=other,
        twincharger_rows=twincharger_rows,
        kept_fuel_types=kept_fuel_types,
    )
    return rows, report


def _print_report(rows: list[dict[str, str]], report: Report, out: Path) -> None:
    for table, n, skipped, ncols in report.tables:
        print(f"table {table}: rows {n}, skipped {skipped} (field count != {ncols})")
    print(f"population pairs={report.population} map_rows_without_code={report.map_rows_without_code}")
    print("hits_before_petrol " + " ".join(f"{t}={report.hits[t]}" for t in ("T0", "T1", "T0A")))
    print(f"other_manufacturer by brand -> TecDoc manufacturers (top 25 of {len(report.other)} groups):")
    for (brand, makers), n in sorted(report.other.items(), key=lambda kv: (-kv[1], kv[0]))[:25]:
        print(f"  {brand} -> {makers}: {n}")
    for f in (*FIELDS, "my_start", "my_end"):
        filled = sum(1 for r in rows if r[f])
        print(f"fill {f}={filled}/{len(rows)}")
    print(f"fill n_cars>0={sum(1 for r in rows if r['n_cars'] != '0')}/{len(rows)}")
    print(f"twincharger_rows={report.twincharger_rows}")
    fuel = sorted(report.kept_fuel_types.items())
    print("kept_engine_fuel_types " + " ".join(f"{k or '<absent>'}={v}" for k, v in fuel))
    by_code: dict[str, set[tuple[str, ...]]] = defaultdict(set)
    brands_of: Counter[str] = Counter()
    for r in rows:
        code = _normalise_code(r["engine_code"])
        brands_of[code] += 1
        by_code[code].add(tuple(r[f] for f in FIELDS))
    multi = [c for c, n in brands_of.items() if n > 1]
    differing = sorted(c for c in multi if len(by_code[c]) > 1)
    print(f"code_collisions codes={len(multi)} differing={len(differing)}: {' '.join(differing)}")
    no_row = report.no_row
    print(f"no_row other_manufacturer={no_row['other_manufacturer']} non_petrol={no_row['non_petrol']} "
          f"no_code={no_row['no_code']}")
    by_status = Counter(f"{r['match_tier']}/{r['status']}" for r in rows)
    print("rows " + " ".join(f"{k}={v}" for k, v in sorted(by_status.items())))
    print(f"wrote {out} rows={len(rows)}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Extract TecDoc 1Q2019 engine facts for vds_engine_map.csv codes.")
    parser.add_argument("--dbs-root", default=os.environ.get("DBS_ROOT"),
                        help="folder holding 1Q2019/ (default: $DBS_ROOT)")
    parser.add_argument("--map", type=Path, default=DEFAULT_MAP, help="vds_engine_map.csv")
    parser.add_argument("--out", type=Path, default=DEFAULT_OUT, help="output CSV")
    args = parser.parse_args(argv)
    if not args.dbs_root:
        parser.error("--dbs-root is required when DBS_ROOT is not set")
    dbs_root = Path(args.dbs_root).resolve()
    out = args.out.resolve()
    if out.is_relative_to(dbs_root):
        parser.error("--out must not be under the DBS root")

    rows, report = extract(dbs_root, args.map)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    _print_report(rows, report, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
