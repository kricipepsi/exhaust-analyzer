# TecDoc → VINLab Parameter Mapping (BUILD-TIME SPEC)

> **Role under approach C (2026-05-17 architecture pivot):** this document is the **build-time** extraction map. TecDoc is queried **only** by `tools/build_vref_db.py`. Runtime code in `vinlab/` never opens MySQL. See `docs/BUILD_DATA_SOURCES.md` for the full multi-source precedence (vPIC + CSV + TecDoc + YAML).

Generated 2026-05-16 from live TecDoc 1Q2018 MySQL database via MCP server.

**Database: tecdoc @ 127.0.0.1:3306 (MySQL 8.4.9)**
**Rows loaded: 1,636,557** across manufacturers (4,380), models (14,945), engines (25,206),
passanger_cars (67,117), passanger_car_attributes (993,888), engine_attributes (438,998),
passanger_car_engines (62,418), prd (26,938), passanger_car_prd (2,166), engine_prd (501).

---

## Subsystem 1: Engine and Displacement Architecture

| VIN Field | TecDoc Source | Table | Column | Sample Values |
|---|---|---|---|---|
| `engine_displacement_liters` | `Capacity_Technical` | `passanger_car_attributes` | `displayvalue` | `"1998 ccm"`, `"1598 ccm"`, `"1368 ccm"` |
| (fallback) | `Capacity` | `engine_attributes` | `displayvalue` | `"1995 ccm"`, `"1998 ccm"` |
| `cylinder_count` | `NumberOfCylinders` | `passanger_car_attributes` | `displayvalue` | `"4"`, `"6"`, `"8"` |
| (fallback) | `NumberOfCylinders` | `engine_attributes` | `displayvalue` | `"4"`, `"6"`, `"8"` |
| `engine_configuration` | `EngineConstruction` | `engine_attributes` | `displayvalue` | `"ряд"` (Inline), `"V"`, `"VR"`, `"W"`, `"оппозитный двигатель"` (Boxer), `"роторно-поршневой"` (Rotary) |
| (detail) | `CylinderConstruction` | `engine_attributes` | `displayvalue` | `"DOHC"` (8,630), `"OHV"` (6,456), `"SOHC/OHC"` (6,364), `"CIH"` (50) |
| `number_of_banks` | **Derived** from `EngineConstruction` | — | — | `"ряд"` → 1, `"V"` → 2, `"VR"` → 2, `"W"` → 3 or 4, `"оппозитный"` → 2 |

---

## Subsystem 2: Aspiration and Induction Systems

| VIN Field | TecDoc Source | Table | Column | Sample Values |
|---|---|---|---|---|
| `induction_type` | `ChargeType` | `engine_attributes` | `displayvalue` | `"всасывающее устройство"` = Naturally Aspirated (10,080), `"турбо/нагнетатель"` = Turbo/Supercharged (6,258), `"турбонагнетатель"` = Turbo (3,855), `"компрессор"` = Supercharged (98), `"битурбо"` = Bi-Turbo (35) |
| `fuel_delivery_type` | `FuelMixture` | `passanger_car_attributes` or `engine_attributes` | `displayvalue` | `"Впрыскивание во впускной коллектор"` = PFI (11,577), `"Непосредственный впрыск"` = GDI (9,212), `"Карбюратор"` = Carb (935), `"Впрыск с форсункой"` (1,453) |
| `has_maf_sensor` | **Part-level** | `prd` + `passanger_car_pds` | — | MAF products exist in prd (e.g. id 11884 "Reiniger für Luftmassensensoren"). Detect via article linkage to products in `"Приготовление смеси"` assembly group. Also inferrable: PFI manifold injection → likely MAF; GDI → likely MAP-only |
| `has_map_sensor` | **Part-level** | `prd` + `passanger_car_pds` | — | `prd.id=161` "Датчик, давление наддува" (Boost pressure sensor). Present on turbo/supercharged vehicles. Also in `"Контрольные приборы"` assembly group. |
| `primary_load_calculation` | **Derived** | — | — | Induction + FuelDelivery heuristic: NA+PFI → "MAF", Turbo+GDI → "MAP", Carb → "Alpha-N" |

---

## Subsystem 3: Powertrain and Valvetrain Management

| VIN Field | TecDoc Source | Table | Column | Sample Values |
|---|---|---|---|---|
| `valvetrain_type` | `ValveManagement` | `engine_attributes` | `displayvalue` | `"тарельчатый толкатель"` = Bucket Tappet (5,322), `"рокерный толкатель"` = Rocker Arm (596), `"гидравлический толкатель"` = Hydraulic Lifter (549) |
| (VVT detection) | Combined with `CylinderConstruction` | `engine_attributes` | `displayvalue` | DOHC + hydraulic lifter → likely VVT; SOHC/OHC → may have VVT; OHV → unlikely VVT |
| `fuel_type` | `FuelType` | `passanger_car_attributes` | `displayvalue` | `"бензин"` = Gasoline (48,260), `"Дизель"` = Diesel (15,059), `"Бензин/этанол"` = Flex-Fuel (1,611), `"Бензин/автогаз (LPG)"` (527), `"Бензин/природный газ (CNG)"` (537) |
| (fallback) | `FuelType` | `engine_attributes` | `displayvalue` | Same pattern (12,725 gasoline, 11,672 diesel) |
| (engine type) | `EngineType` | `passanger_car_attributes` | `displayvalue` | `"Бензиновый двигатель"` = Petrol Engine, `"Дизельный двигатель"` = Diesel Engine |

---

## Subsystem 4: Emissions Control Specifications

| VIN Field | TecDoc Source | Table | Column | Sample Values |
|---|---|---|---|---|
| `upstream_o2_type` | **Part-level** | `prd` + `passanger_car_pds` | — | Lambda sensors exist in prd under `"Приготовление смеси"` assembly group: id 3922 "Лямбда-зонд", id 3923 "Лямбда-зонд" (universal), id 3924 "Комплект для лямбда-зонда". Wideband vs Narrowband determined by part specifications in `article_attributes`. |
| `egr_equipped` | **Part-level** | `prd` + `passanger_car_pds` | — | EGR products in `"Рециркуляция ОГ"` assembly group: id 758 (vacuum EGR valve), id 1129 (EGR valve), id 1137 (EGR control valve), id 1145 (EGR return valve). If vehicle has EGR parts linked → `true`. |

| (catalyst type) | `CatalysatorType` | `passanger_car_attributes` | `displayvalue` | `"с регулируемым катализатором (3-х ступенчатый)"` = 3-way cat, `"с нерегулируемый катализатором"` = unregulated, `"с дизельным катализатором (оксид. кат.)"` = diesel oxidation cat, `"без катализатора"` = no cat |
| (emission norm) | `EmissionNorm` | `engine_attributes` | `displayvalue` | `"Euro 3"` (761), `"Euro 4 (D4)"` (701), `"Euro 2"` (656), `"Euro 5"` (531), `"Euro 1"` (397), `"Euro 6"` (297) |

---

## Key Linkage Tables

### Vehicle → Engine relationship
```
passanger_cars.id ← passanger_car_engines.id
passanger_car_engines.engineid → engines.id
```

### Vehicle → Parts relationship (for sensor-level attributes)
```
passanger_cars.id ← passanger_car_pds.passangercarid
passanger_car_pds.productid → prd.id
passanger_car_pds.supplierid → suppliers.id
prd.assemblygroupdescription → categorizes the part
```

### Query example: Does vehicle X have EGR?
```sql
SELECT COUNT(*) > 0 AS has_egr
FROM passanger_car_pds pcp
JOIN prd ON pcp.productid = prd.id
WHERE pcp.passangercarid = ?
  AND prd.assemblygroupdescription = 'Рециркуляция ОГ';
```


### Query example: Get all VIN parameters for a passenger car
```sql
SELECT 
  pca.attributetype,
  pca.displaytitle,
  pca.displayvalue
FROM passanger_car_attributes pca
WHERE pca.passangercarid = ?;

-- Plus engine attributes:
SELECT ea.attributetype, ea.displaytitle, ea.displayvalue
FROM passanger_car_engines pce
JOIN engine_attributes ea ON pce.engineid = ea.engineid
WHERE pce.id = ?;
```

---

## MCP Server Status (BUILD-TIME ONLY)

The MCP server below is consumed **only by `tools/build_vref_db.py`** during the build. The shipped `vinlab/` package has no MySQL dependency.

- **Package**: `@benborla29/mcp-server-mysql@2.0.8` (installed globally)
- **Status**: Connected and working
- **Config**: `C:\Users\muto\claude\4DApp\4DLab\VINLab\settings.json` → `mcpServers.mcp_server_mysql`
- **MySQL**: 8.4.9 running at 127.0.0.1:3306, database `tecdoc`, user `root`, no password
- **Data dir**: `C:\Users\muto\claude\4DApp\4DLab\VINLab\mysql_data`
