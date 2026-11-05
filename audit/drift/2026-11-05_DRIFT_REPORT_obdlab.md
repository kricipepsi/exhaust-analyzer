# OBDLab drift report (2026-11-05): design documents against current code

## labs/obdlab/README.md

- [MISSING] The role line lists downstream-O2 masking, and the lab package has no masking code. Doc: `labs/obdlab/README.md:4` "masking, Mode $06 discriminators". Code: ABSENT (`grep -rniE 'mask' labs/obdlab/obdlab --include=*.py` -> no output, exit 1).

## labs/obdlab/docs/PRD_OBDLab.md

- [MODEL] The payload table types normalized_obd_lambda as a plain float, and the model allows None. Doc: `labs/obdlab/docs/PRD_OBDLab.md:127` "`normalized_obd_lambda` | `float` | [0.7, 1.3]". Code: `labs/obdlab/obdlab/schemas/payload.py:74` "normalized_obd_lambda: float | None = Field(ge=0.7, le=1.3)".
- [DIVERGENCE] The assumptions table says a cold engine emits lambda 1.0, and the translator emits None. Doc: `labs/obdlab/docs/PRD_OBDLab.md:207` "Cold engine defaults (`lambda=1.0`, `trim_delta=0.0`) are COMLab-acceptable". Code: `labs/obdlab/obdlab/core/sensor_signal_translator.py:151` "normalized_lambda: float | None = None".
- [DIVERGENCE] The document says no bare ValueError is raised, and the VE engine raises one for an unknown strategy. Doc: `labs/obdlab/docs/PRD_OBDLab.md:107` "no bare `ValueError`/`AssertionError`". Code: `labs/obdlab/obdlab/core/ve_engine.py:95` "Unknown air_metering_strategy: {strategy}".
- [DIVERGENCE] Success criterion 3 expects zero HIGH_IDLE_LOAD occurrences in obdlab, and the YAML config note still names it. Doc: `labs/obdlab/docs/PRD_OBDLab.md:230` "scan finds zero occurrences in `obdlab/`". Code: `labs/obdlab/obdlab/config/obd_translation_rules.yaml:40` "Supersedes former HIGH_IDLE_LOAD at 2200-2600 RPM".

## labs/obdlab/docs/HLD_OBDLab.md

- [DIVERGENCE] The pipeline diagram says a frozen engine yields lambda 1.0, and the translator yields None. Doc: `labs/obdlab/docs/HLD_OBDLab.md:106` "frozen → normalized_obd_lambda=1.0, NO_FAULT". Code: `labs/obdlab/obdlab/core/sensor_signal_translator.py:151` "normalized_lambda: float | None = None".
- [DIVERGENCE] The non-functional table requires zero HIGH_IDLE_LOAD tokens in obdlab, and the YAML config note holds one. Doc: `labs/obdlab/docs/HLD_OBDLab.md:250` "0 occurrences in `obdlab/`". Code: `labs/obdlab/obdlab/config/obd_translation_rules.yaml:40` "Supersedes former HIGH_IDLE_LOAD at 2200-2600 RPM".
- [DIVERGENCE] The document says every numeric literal carries a wiki citation, and the inferred-MAP branch uses a 25.0 intake-temperature fallback with no citation on the line. Doc: `labs/obdlab/docs/HLD_OBDLab.md:251` "every literal in `obdlab/` carries a `# wiki:` citation comment". Code: `labs/obdlab/obdlab/core/ve_engine.py:181` "ve_pct = self._calc_ve_standard(maf, inferred_map, rpm, displacement, iat or 25.0)".
- [DIVERGENCE] The document says COMLab fills freeze_frame_pids from DTCLab before the OBDLab call, and the composition only copies DTC codes into active_dtcs. Doc: `labs/obdlab/docs/HLD_OBDLab.md:53` "populates freeze_frame_pids from DTCLab before calling OBDLab". Code: `apps/wired/wired/composition.py:691` "with the user's DTC codes as ``active_dtcs``.".
- [UNDOCUMENTED] The composition copies Mode $06 and idle-trim fields from the raw OBD inputs into COMLab's OBD payload outside OBDLivePayload, and no integration row lists them. Doc: `labs/obdlab/docs/HLD_OBDLab.md:69` "COMLab consumes the payload as a frozen contract surface (see §7)." Code: `apps/wired/wired/composition.py:496` "mode06_catalyst_margin_pct=float(obd_inputs[".
- [UNDOCUMENTED] The composition builds the DNA view and falls back to MAP_ONLY_SPEED_DENSITY when the VIN output has no strategy, while OBDLab itself defaults to the dual strategy. Doc: `labs/obdlab/docs/HLD_OBDLab.md:52` "builds ObdLabDnaView from the VIN/DNA record". Code: `apps/wired/wired/composition.py:573` "MAP_ONLY_SPEED_DENSITY".

## labs/obdlab/docs/LLD_OBDLab.md

- [DIVERGENCE] The cold-engine defaults block sets normalized_obd_lambda to 1.0, and the translator sets None. Doc: `labs/obdlab/docs/LLD_OBDLab.md:303` "normalized_obd_lambda = 1.0". Code: `labs/obdlab/obdlab/core/sensor_signal_translator.py:151` "normalized_lambda: float | None = None".
- [DIVERGENCE] The forbidden-pattern table bans HIGH_IDLE_LOAD anywhere in obdlab, and the YAML config note holds it. Doc: `labs/obdlab/docs/LLD_OBDLab.md:356` "`HIGH_IDLE_LOAD` anywhere in `obdlab/`". Code: `labs/obdlab/obdlab/config/obd_translation_rules.yaml:40` "Supersedes former HIGH_IDLE_LOAD at 2200-2600 RPM".
- [DIVERGENCE] The convention says every numeric literal carries a wiki comment, and the MAP-only branch uses an uncited 25.0 fallback. Doc: `labs/obdlab/docs/LLD_OBDLab.md:27` "Convention: every numeric literal in `obdlab/` carries a `# wiki: <source>`". Code: `labs/obdlab/obdlab/core/ve_engine.py:147` "ve_pct = self._calc_ve_standard(emulated_maf, map_kpa, rpm, displacement, iat or 25.0)".
- [DIVERGENCE] The document says both linearity helpers return 0.0 on a zero denominator, and the delta helper zeroes only the affected term and returns the other term. Doc: `labs/obdlab/docs/LLD_OBDLab.md:287` "Both guard against a zero denominator". Code: `labs/obdlab/obdlab/core/maf_linearity.py:43` "err_stress = 0.0".
- [DIVERGENCE] The forwarding contract says COMLab fills freeze_frame_pids from DTCLab data, and the composition adds only active_dtcs. Doc: `labs/obdlab/docs/LLD_OBDLab.md:335` "(default `{}`) is populated by **COMLab**". Code: `apps/wired/wired/composition.py:691` "with the user's DTC codes as ``active_dtcs``.".
- [UNDOCUMENTED] The degraded-mode text lists missing inputs and omits that a missing intake temperature silently becomes 25.0 in the VE formula. Doc: `labs/obdlab/docs/LLD_OBDLab.md:132` "**Degraded mode:** when `displacement`, `maf`, `map`, or `rpm` is missing". Code: `labs/obdlab/obdlab/core/ve_engine.py:113` "ve_pct = self._calc_ve_standard(maf, map_kpa, rpm, displacement, iat or 25.0)".

## labs/obdlab/docs/DLD_OBDLab.md

- [MODEL] The payload table types normalized_obd_lambda as a plain float, and the model allows None. Doc: `labs/obdlab/docs/DLD_OBDLab.md:172` "`normalized_obd_lambda` | `float` | `[0.7, 1.3]`". Code: `labs/obdlab/obdlab/schemas/payload.py:74` "normalized_obd_lambda: float | None = Field(ge=0.7, le=1.3)".
- [DIVERGENCE] The document says the ObdEmissionsView sub-model was pruned, and the DNA view module still defines it and exports it. Doc: `labs/obdlab/docs/DLD_OBDLab.md:128` "the `ObdEmissionsView` sub-model — all pruned (PURGE-2) for lack of a live". Code: `labs/obdlab/obdlab/schemas/dna_view.py:73` "class ObdEmissionsView(BaseModel):".
- [DIVERGENCE] The document forbids HIGH_IDLE_LOAD throughout obdlab, and the YAML config note holds it. Doc: `labs/obdlab/docs/DLD_OBDLab.md:111` "is forbidden throughout `obdlab/`". Code: `labs/obdlab/obdlab/config/obd_translation_rules.yaml:40` "Supersedes former HIGH_IDLE_LOAD at 2200-2600 RPM".
- [UNDOCUMENTED] The payload table documents one default (voltage 14.0), and the translator also invents 25.0 for intake temperature and 0.0 for throttle, load and both bank-1 trims. Doc: `labs/obdlab/docs/DLD_OBDLab.md:184` "`[0, 18]`, default `14.0`". Code: `labs/obdlab/obdlab/core/sensor_signal_translator.py:256` ", 25.0),".

## labs/obdlab/docs/BDD_OBDLab.md

- [DIVERGENCE] The cold-engine scenario expects lambda 1.0, and the translator emits None. Doc: `labs/obdlab/docs/BDD_OBDLab.md:48` "normalized_obd_lambda = 1.0 (stoichiometric safe default)". Code: `labs/obdlab/obdlab/core/sensor_signal_translator.py:151` "normalized_lambda: float | None = None".
- [DIVERGENCE] The vocabulary scenario expects HIGH_IDLE_LOAD nowhere in the obdlab codebase, and the YAML config note holds it. Doc: `labs/obdlab/docs/BDD_OBDLab.md:298` "HIGH_IDLE_LOAD appears nowhere". Code: `labs/obdlab/obdlab/config/obd_translation_rules.yaml:40` "Supersedes former HIGH_IDLE_LOAD at 2200-2600 RPM".

## labs/obdlab/docs/OBD_VOCABULARY.md

- [MISSING] The document says four VINLab switches propagate into OBDLab, and the lab code has no euro_emission_category switch. Doc: `labs/obdlab/docs/OBD_VOCABULARY.md:97` "VINLab emits four switches that propagate into OBDLab and Gas Lab". Code: ABSENT (`grep -rniE 'euro' labs/obdlab/obdlab --include=*.py` -> no output, exit 1).
- [MODEL] The document lists a calculated_ve node with range 0-100 percent, and the payload field is ve_pct with an upper bound of 200. Doc: `labs/obdlab/docs/OBD_VOCABULARY.md:149` "`calculated_ve` | Ideal-gas air-loop equation | 0 – 100 %". Code: `labs/obdlab/obdlab/schemas/payload.py:80` "ve_pct: float = Field(ge=0.0, le=200.0)".
- [DIVERGENCE] The document defines engine_warmed as coolant at or above 70, and the thermal gate uses 75. Doc: `labs/obdlab/docs/OBD_VOCABULARY.md:151` "`engine_warmed` | `coolant_temp_c >= 70` | bool". Code: `labs/obdlab/obdlab/core/semantic_consistency_checker.py:21` "_CUTOFF_ECT_COLD = 75".
- [DIVERGENCE] The ECT band table freezes trim analytics below 70, and the bucketing rule freezes them below 75. Doc: `labs/obdlab/docs/OBD_VOCABULARY.md:748` "`COLD_OPEN_LOOP` | < 70°C". Code: `labs/obdlab/obdlab/config/obd_translation_rules.yaml:9` "value: 75.0".
- [DIVERGENCE] The trim node range is -200 to +200, and the validated trims reach 127 each, so the sum reaches 254 with no bound in the payload. Doc: `labs/obdlab/docs/OBD_VOCABULARY.md:38` "STFT + LTFT, virtual node | % | -200 – +200". Code: `labs/obdlab/obdlab/config/physical_sensor_bounds.json:31` ": 127.0,".
- [DIVERGENCE] The bucket table gives STRESS_IDLE a fixed 3500-4500 RPM band with 40-60 percent load, and the rule uses the target RPM plus or minus 10 percent with 10-60 percent load. Doc: `labs/obdlab/docs/OBD_VOCABULARY.md:88` "`STRESS_IDLE` | 3500 – 4500 (VIN-dependent) | 40 – 60%". Code: `labs/obdlab/obdlab/config/obd_translation_rules.yaml:39` "value: [10.0, 60.0]".
- [MODEL] The document types stress_idle_rpm_target as an int in the range 2800-5000, and the DNA view allows None with no range. Doc: `labs/obdlab/docs/OBD_VOCABULARY.md:135` "stress_idle_rpm_target: int  # range 2800-5000, VIN-derived". Code: `labs/obdlab/obdlab/schemas/dna_view.py:68` "stress_idle_rpm_target: int | None = Field(default=None)".
- [MODEL] The O2NormalizationMode block lists three members, and the code enum has a fourth member O2_CHANNEL_FAULT. Doc: `labs/obdlab/docs/OBD_VOCABULARY.md:192` "class O2NormalizationMode(StrEnum):". Code: `labs/obdlab/obdlab/schemas/vocabulary.py:33` "O2_CHANNEL_FAULT =".
- [MISSING] The precondition list says to mark fuel_trim_invalid when a condition fails, and the lab code has no such marker. Doc: `labs/obdlab/docs/OBD_VOCABULARY.md:374` "otherwise mark `fuel_trim_invalid`". Code: ABSENT (`grep -rn 'fuel_trim_invalid' labs/obdlab/obdlab` -> no output, exit 1).

## labs/obdlab/docs/ADR_OBDLab.md

- [DIVERGENCE] ADR-0005 says COMLab catches the whole OBDLab family with one except clause, and the VE engine raises a bare ValueError. Doc: `labs/obdlab/docs/ADR_OBDLab.md:203` "COMLab catches the whole family with one `except ObdLabError`". Code: `labs/obdlab/obdlab/core/ve_engine.py:95` "Unknown air_metering_strategy: {strategy}".
