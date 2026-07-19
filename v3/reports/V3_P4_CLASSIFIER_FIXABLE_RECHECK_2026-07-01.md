# V3 P4 classifier-fixable recheck — 2026-07-01

## Headline

2 CLASSIFIER_FIXABLE cases rechecked against `POST_T_V3_3D`: 1 already-bank / 0 classifier-fix / 1 re-bucket.

Self-check: replayed 294 accuracy cases; drift=0.

## Per-case status

| case_id | expected | top3 | rank | covered | abstain | emitted_state | verdict |
| --- | --- | --- | --- | --- | --- | --- | --- |
| era2_008 | cam_timing / ERR-CT-004 | sensor_fault, cam_timing, catalyst_failure | 2 | False | margin | SAMPLE_INVALID | ALREADY_BANKS |
| CASE-039 | ecu_fault / ERR-EF-002 | rich_mixture, sensor_fault, catalyst_failure | None | False | margin | EGR_STUCK_OPEN | RE-BUCKET_TO_SIGNAL |

## era2_008 — ALREADY_BANKS

- Current run: winner `sensor_fault` / `SF-001`; top3 families `sensor_fault, cam_timing, catalyst_failure`; expected-family rank `2`; abstained `True` (`margin`).
- Reachability: required state `VVT_FAILURE`; T-V3-D2 said `CLASSIFIER_FIXABLE`; live replay says `passes required bound signature: hc=420 in [0,20000]; co=0.4 in [0,15]; co2=13 in [0,16]; o2=0.4 in [0,22]; nox=75 in [0,5000]; lambda=0.941 in [0.5,2.5]; sample_validity=INVALID`.
- Replay candidates: candidates `VVT_FAILURE`; resolved `VVT_FAILURE`; definitive `SAMPLE_INVALID`; emitted `SAMPLE_INVALID`.
- Idle vector: {'hc': 420, 'co': 0.4, 'co2': 13.0, 'o2': 0.4, 'nox': 75} lambda=0.941; sample_validity=INVALID; high_idle={'hc': 250, 'co': 0.5, 'co2': 12.5, 'o2': 0.5, 'nox': 55} high_lambda=0.9726807679238872.
- Minimal classifier fix: No classifier fix needed: expected family is already emitted in the POST_T_V3_3D top-3; abstain, not rank, is the remaining blocker.
- FT-8 neighbour risk: {"sample_invalid_boundary_neighbours": ["CASE-010", "CASE-018", "CASE-021", "CASE-035", "CASE-045", "CSV-052", "CSV-095", "CSV-129", "CSV-130", "ECU-008", "EXP-N012", "EXP-N022", "EXP-N023", "EXT-206", "EXT-210", "EXT-238", "EXT-239", "PDF-HI-008", "REAL-001", "REAL-002", "REAL-003", "TC-048", "YAML-CSV52", "YAML-CSV95", "YAML-PDF_4G_04", "case_002", "case_006", "case_007", "case_040", "era1_008", "era2_001", "era2_008", "era3_007"]}
- Same competition_group collisions: not present in POST_T_V3_3D results.json or global_fault_registry.json

## CASE-039 — RE-BUCKET_TO_SIGNAL

- Current run: winner `rich_mixture` / `RM-001`; top3 families `rich_mixture, sensor_fault, catalyst_failure`; expected-family rank `None`; abstained `True` (`margin`).
- Reachability: required state `POA_SIGNATURE`; T-V3-D2 said `CLASSIFIER_FIXABLE`; live replay says `passes required bound signature: hc=600 in [500,20000]; co=2.5 in [0,15]; co2=11.5 in [0,14.5]; o2=0.5 in [0,22]; nox=45 in [0,5000]; lambda=0.855 in [0.5,2.5]; sample_validity=VALID`.
- Replay candidates: candidates `POA_SIGNATURE, EGR_STUCK_OPEN, VVT_FAILURE, INCOMPLETE_OXIDATION`; resolved `POA_SIGNATURE, EGR_STUCK_OPEN, VVT_FAILURE, INCOMPLETE_OXIDATION`; definitive `None`; emitted `EGR_STUCK_OPEN`.
- Idle vector: {'hc': 600, 'co': 2.5, 'co2': 11.5, 'o2': 0.5, 'nox': 45} lambda=0.855; sample_validity=VALID; high_idle=None high_lambda=n/a.
- Minimal classifier fix: POA_SIGNATURE is reachable only as a co-surviving catch-all; the emitted state stays EGR_STUCK_OPEN because the idle-only gas row has no high-idle/ECU-strategy discriminator. A classifier-only POA win would require broad EGR_STUCK_OPEN narrowing or catch-all priority reversal, not a safe one-case bin fix.
- FT-8 neighbour risk: {"egr_stuck_open_resolved_neighbours": ["CASE-010", "CASE-018", "CASE-020", "CASE-021", "CASE-023", "CASE-031", "CASE-033", "CASE-035", "CASE-037", "CASE-039", "CASE-045", "CASE-048", "CSV-018", "CSV-022", "CSV-041", "CSV-100", "CSV-103", "CSV-104", "CSV-113", "CSV-114", "CSV-115", "CSV-116", "CSV-117", "CSV-118", "CSV-119", "CSV-120", "CSV-125", "CSV-126", "CSV-128", "ECU-001", "ECU-003", "ECU-009", "EXP-N002", "EXP-N003", "EXP-N004", "EXP-N007", "EXP-N010", "EXP-N012", "EXP-N013", "EXP-N014", "EXP-N017", "EXP-N018", "EXP-N020", "EXP-N021", "EXP-N026", "EXP-N027", "EXP-N030", "EXT-209", "EXT-210", "EXT-211", "EXT-212", "EXT-216", "EXT-217", "EXT-219", "EXT-221", "EXT-222", "EXT-223", "EXT-224", "EXT-225", "EXT-227", "EXT-236", "EXT-240", "MECH-001", "MECH-002", "MECH-004", "MECH-006", "PDF-4G-02", "PDF-4G-03", "PDF-HI-001", "REAL-004", "TC-021", "YAML-CSV18", "YAML-CSV22", "YAML-CSV41", "YAML-PDF_4G_02", "YAML-PDF_HI_001", "YAML-TC12", "YAML-TC37", "case_002", "case_017", "case_023"], "poa_egr_collision_neighbours": ["CASE-021", "CASE-033", "CASE-035", "CASE-039", "CASE-045", "CSV-022", "CSV-103", "CSV-104", "CSV-113", "CSV-114", "CSV-117", "CSV-118", "CSV-119", "CSV-120", "EXP-N014", "EXP-N018", "EXP-N021", "EXP-N026", "EXP-N030", "EXT-216", "EXT-224", "EXT-227", "EXT-236", "MECH-001", "MECH-002", "MECH-006", "PDF-HI-001", "REAL-004", "YAML-CSV22", "YAML-PDF_HI_001", "YAML-TC37"]}
- Same competition_group collisions: not present in POST_T_V3_3D results.json or global_fault_registry.json

## Gate notes

- No engine, lab, registry, oracle, corpus, scorer, or yardstick files are edited.
- `CASE-039` is not a safe classifier-only commit: the broad EGR/POA overlap has a large neighbour set, so the honest Phase-4 path is an ECU/control signal contract rather than an in-place threshold nudge.
- `era2_008` already banks in the differential; a T-V3-P4-0B fix for it would be a no-op.
