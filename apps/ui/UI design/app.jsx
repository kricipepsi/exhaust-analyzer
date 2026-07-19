// 4DLab UI — main app
// Sidebar (Modules → VIN → Context → Symptom → Status) + 7 central expanders.
// Field content sourced from uploads/4DLab_UI_FieldMap.md.

const { useState, useEffect, useMemo } = React;

// Tier 1/2 catalogue — FieldMap §4.4 (18 valid pairs)
const SYMPTOM_TREE = [
  { v: "vehicle_wont_start", l: "🚫 Vehicle Won't Start", t2: [
    { v: "fast_crank_whining", l: "Fast crank / whining" },
    { v: "no_crank_silent", l: "No crank / silent" },
    { v: "normal_crank_zero_rpm", l: "Normal crank / zero RPM" },
  ]},
  { v: "rough_idle_shudder", l: "🔧 Rough Idle / Shudder", t2: [
    { v: "cold_engine_only", l: "Cold engine only" },
    { v: "hot_engine_only", l: "Hot engine only" },
    { v: "constant_shudder", l: "Constant shudder" },
  ]},
  { v: "lack_of_power_hesitation", l: "⬇️ Lack of Power / Hesitation", t2: [
    { v: "flat_sluggish_always", l: "Flat / sluggish always" },
    { v: "only_high_rpm_highway", l: "Only at high RPM / highway" },
    { v: "sudden_jerk_stumble", l: "Sudden jerk / stumble" },
  ]},
  { v: "poor_economy_fuel_odor", l: "⛽ Poor Economy / Fuel Odour", t2: [
    { v: "just_poor_mpg", l: "Just poor MPG" },
    { v: "strong_fuel_smell", l: "Strong fuel smell" },
    { v: "right_after_fillup", l: "Right after fill-up" },
  ]},
  { v: "engine_dies_or_stalls", l: "🛑 Engine Dies / Stalls", t2: [
    { v: "when_coasting_to_stop", l: "When coasting to stop" },
    { v: "intermittent_random", l: "Intermittent / random" },
    { v: "only_when_hot", l: "Only when hot" },
  ]},
  { v: "visible_exhaust_smoke", l: "💨 Visible Exhaust Smoke", t2: [
    { v: "black_smoke", l: "Black smoke" },
    { v: "blue_oily_smell", l: "Blue / oily smell" },
    { v: "white_sweet_smell", l: "White / sweet smell" },
  ]},
];

// Mode $06 lookup mock — keyed by MID_<HEX>_TID_<HEX>
const MID_LOOKUP = {
  "MID_01_TID_01": "Catalyst Bank 1 — switch ratio",
  "MID_01_TID_02": "Catalyst Bank 1 — frequency",
  "MID_02_TID_01": "Catalyst Bank 2 — switch ratio",
  "MID_A1_TID_05": "O₂ Sensor B1S1 — lean→rich transition",
  "MID_A2_TID_0B": "O₂ Sensor B1S2 — switching time",
  "MID_A3_TID_07": "O₂ Sensor B2S1 — response",
  "MID_31_TID_80": "EGR Monitor — flow rate",
  "MID_3C_TID_88": "EVAP Monitor — leak detection",
  "MID_71_TID_0B": "Misfire Counts — cylinder 1",
};

// Initial state factories ───────────────────────────────────────────
const emptyGas = () => ({ co: 0.0, co2: 0.0, hc: 0, o2: 0.0, nox: 0, lambda: 1.000 });
const emptyOBD = () => ({
  rpm: 0, ect: 0, load: 0,
  stft1: 0, ltft1: 0, stft2: 0, ltft2: 0,
  maf: 0, map: 0,
  o2_up: 0.45, o2_dn: 0.0,
});
const emptyFF = () => ({
  load: 0, rpm: 0, ect: 0, stft1: 0, ltft1: 0,
  map: 0, speed: 0, ignition: 0, iat: 0,
  maf: 0, throttle: 0, fuel_status: "CL",
  // extended
  stft2: 0, ltft2: 0, o2_b1s1: 0.45,
  baro: 101, egr: 0, runtime: 0, fuel_level: 0,
});

// Helpers ───────────────────────────────────────────────────────────
function dnaCommitted(modules, dna) {
  return modules.dna && dna && dna.confidence === "HIGH";
}
function isBasicMode(modules, dna) {
  return !dnaCommitted(modules, dna);
}

// Helper text bodies (FieldMap §1.4 `?` guides)
const HELP = {
  modules: `Tick the data you'll enter today. Each ticked module opens its panel in the centre and sends that channel to the engine. Tick **DNA / VIN** to decode the car and auto-hide fields that don't apply; leave it off for a basic, show-all diagnosis.`,
  vin: `Enter the full 17-character VIN. A good decode auto-fills the hardware profile and hides fields that don't apply. If it can't decode, the UI switches to **basic input mode** — all DNA-dependent fields show in their safe, narrowband-default form.`,
  symptom: `Pick the main complaint, then the sub-filter. Only the 18 catalogued pairs are offered. **Cranking / Won't-start** relaxes the gas-chemistry checks. Engine state **Cranking** or **Won't start** suppresses trim and λ analytics.`,
  gasLow: `Engine at **V10 Low Idle RPM**, fully warm (ECT ≥ 75 °C), stabilised closed-loop idle. Probe ≥ 30 cm into the tailpipe (sidebar Probe-Depth check confirms CO + CO₂ ≥ 12 %). All five gases are required — no 4-gas fallback. The engine recomputes λ from the gases; enter the analyser's own **Measured λ** reading if OBDLab is not connected (it becomes the lambda perception source).`,
  gasHigh: `Hold at **V11 High Idle RPM** — the COC stress-idle target (\`stress_idle_rpm_target\` from VIN, target λ ≈ \`target_lambda_v112\`). Engine fully warm (ECT ≥ 75 °C). Same six fields as low idle. **Turbo / supercharged:** let boost settle fully before reading.`,
  obdLow: `Capture at **V10 Low Idle RPM** — stabilised, closed-loop, ECT ≥ 75 °C. **Bank-2** boxes appear only on V-engines; **MAF / MAP** appear only for the sensors fitted; the upstream-O₂ box auto-switches between V, λ and AFR to match the decoded sensor. In basic mode (no DNA) only Bank-1 trims, RPM, ECT, load and a generic O₂ box show.`,
  obdHigh: `Capture at **U2 RPM** (stationary noise test point) — ECT ≥ 75 °C, same DNA-gated field set as low idle. On turbocharged cars the VE-ceiling check (Physics Gate 3) relaxes — read only after boost has fully settled.`,
  dtc: `Enter codes exactly as the scanner reports them (P0171, P0420, P0300). Tick the MIL boxes to match the dash lamp. Codes are grouped by scanner mode: **$03** confirmed, **$07** pending, **$0A** permanent.`,
  ff: `This is the **single snapshot** the ECU stored when it set the code — not a live reading. Enter the 12 mandatory PIDs from the freeze-frame screen. Extended PIDs are optional; Bank-2 and EGR rows appear only if the car has them.`,
  m06: `Mode $06 reports each on-board monitor's self-test. Read the MID/TID and margin from the scanner. **>15%** passes; **1–15%** marginal; **≤0%** critical fail. Add one row per monitor — the component name is filled in from the MID/TID.`,
};

// Common labels ─────────────────────────────────────────────────────
const FUEL_OPTS = ["E0", "E5", "E10"];
const MILEAGE_OPTS = [
  "Unknown",
  "Low (< 80,000 km)",
  "Mid (80,000 – 150,000 km)",
  "High (> 150,000 km)",
];
const DTC_MEM_OPTS = ["Normal", "Recently cleared (<50 mi)"];
const OCCURS_OPTS = ["Always", "Cold only", "Hot only", "Intermittent"];
const ENGSTATE_OPTS = ["Running", "Cranking", "Won't start"];
const FF_FUEL_STATUS = ["CL", "OL", "OL_DRIVE", "OL_FAULT"];
const M06_STATE = [
  { v: "passed", l: "Passed" },
  { v: "pending", l: "Pending / marginal" },
  { v: "fail", l: "Critical fail" },
];

// Upstream-O₂ field metadata — polymorphic by sensor type
function upstreamO2Meta(type) {
  switch (type) {
    case "WIDEBAND_LAMBDA":
      return { label: "Upstream O₂", unit: "λ", min: 0.7, max: 1.3, step: 0.001, def: 1.000 };
    case "WIDEBAND_AFR":
      return { label: "Upstream O₂", unit: "AFR", min: 10.0, max: 20.0, step: 0.01, def: 14.7 };
    case "NARROWBAND":
    case "WIDEBAND_NB_SIM":
    default:
      return { label: "Upstream O₂", unit: "V", min: 0.0, max: 1.0, step: 0.01, def: 0.45 };
  }
}

// =================================================================
// App
// =================================================================
function App() {
  // Top-level state
  const [modules, setModules] = useState({
    gaslab: true, obdlab: true, dtclab: true, dna: true,
  });
  const [vin, setVin] = useState("");
  const [dna, setDna] = useState(null);
  const [dnaCommittedFlag, setDnaCommittedFlag] = useState(false);

  // Context
  const [fuel, setFuel] = useState("E10");
  const [mileage, setMileage] = useState("Unknown");
  const [dtcMem, setDtcMem] = useState("Normal");

  // Symptom
  const [tier1, setTier1] = useState("");
  const [tier2, setTier2] = useState("");
  const [misfireCyl, setMisfireCyl] = useState(1);
  const [occurs, setOccurs] = useState("Always");
  const [engState, setEngState] = useState("Running");
  const [notes, setNotes] = useState("");

  // GASLab
  const [gasLow, setGasLow] = useState(emptyGas());
  const [gasHigh, setGasHigh] = useState(emptyGas());

  // OBDLab
  const [obdLow, setObdLow] = useState(emptyOBD());
  const [obdHigh, setObdHigh] = useState(emptyOBD());

  // DTC
  const [mil, setMil] = useState(false);
  const [milFlash, setMilFlash] = useState(false);
  const [dtcConfirmed, setDtcConfirmed] = useState("");
  const [dtcPending, setDtcPending] = useState("");
  const [dtcPerm, setDtcPerm] = useState("");

  // Freeze frame
  const [ff, setFf] = useState(emptyFF());
  const [ffExtended, setFfExtended] = useState(false);

  // Mode $06 monitors
  const [m06, setM06] = useState([
    { id: "MID_A1_TID_05", state: "passed", margin: 65 },
  ]);

  // Tweaks — let user preview DNA-gated visibility without retyping VINs
  const TWEAK_DEFAULTS = /*EDITMODE-BEGIN*/{
    "dnaOverride": "off",
    "ovrBanks": 2,
    "ovrMaf": true,
    "ovrMap": true,
    "ovrO2Type": "NARROWBAND",
    "ovrDownstream": true,
    "ovrEgr": true,
    "ovrInduction": "TURBO",
    "ovrCylinders": 6
  }/*EDITMODE-END*/;
  const [t, setTweak] = useTweaks(TWEAK_DEFAULTS);

  // Auto-decode VIN as user types (only triggers when 17 chars committed)
  useEffect(() => {
    const v = vin.trim().toUpperCase();
    if (v.length === 17) {
      setDna(decodeVIN(v));
    } else {
      setDna(null);
      setDnaCommittedFlag(false);
    }
  }, [vin]);

  // Reset DNA-commit when module toggles off
  useEffect(() => {
    if (!modules.dna) setDnaCommittedFlag(false);
  }, [modules.dna]);

  // Effective DNA — manual tweak override, sample VIN, or none
  const effectiveDNA = useMemo(() => {
    if (t.dnaOverride === "high") {
      return {
        confidence: "HIGH",
        make: "Tweak Override",
        engine_code: "—",
        displacement_l: 2.0,
        number_of_banks: t.ovrBanks,
        cylinder_count: t.ovrCylinders,
        has_maf_sensor: t.ovrMaf,
        has_map_sensor: t.ovrMap,
        upstream_o2_type: t.ovrO2Type,
        downstream_o2_present: t.ovrDownstream,
        egr_equipped: t.ovrEgr,
        induction_type: t.ovrInduction,
      };
    }
    if (t.dnaOverride === "basic") return null;
    return dnaCommittedFlag && modules.dna ? dna : null;
  }, [t, dna, dnaCommittedFlag, modules.dna]);

  const isBasic = !effectiveDNA || effectiveDNA.confidence !== "HIGH";
  const banks = effectiveDNA?.number_of_banks ?? 1;
  const hasMaf = !!effectiveDNA?.has_maf_sensor;
  const hasMap = !!effectiveDNA?.has_map_sensor;
  const o2Type = effectiveDNA?.upstream_o2_type ?? "NARROWBAND";
  const o2Present = !!effectiveDNA?.downstream_o2_present;
  const egrOk = !!effectiveDNA?.egr_equipped;
  const cylCount = effectiveDNA?.cylinder_count ?? 4;
  const induction = effectiveDNA?.induction_type ?? "NA";

  // Probe-depth + validation
  const probeTotal = (gasLow.co || 0) + (gasLow.co2 || 0);
  const probeOk = probeTotal >= 12.0;
  const validationErrors = useMemo(() => {
    const e = [];
    if (gasLow.co > 15) e.push("CO exceeds 15% physical bound.");
    if (gasLow.co2 > 22) e.push("CO₂ exceeds 22% physical bound.");
    if (gasLow.hc > 20000) e.push("HC exceeds 20 000 ppm bound.");
    if (gasLow.o2 > 22) e.push("O₂ exceeds 22% physical bound.");
    if (gasLow.nox > 5000) e.push("NOx exceeds 5 000 ppm bound.");
    if (gasLow.lambda < 0.5 || gasLow.lambda > 2.0) e.push("λ outside 0.5–2.0 bound.");
    return e;
  }, [gasLow]);

  // ── Render ──────────────────────────────────────────────────────
  return (
    <div className="app">
      <Sidebar
        modules={modules} setModules={setModules}
        vin={vin} setVin={setVin} dna={dna}
        dnaCommittedFlag={dnaCommittedFlag} setDnaCommittedFlag={setDnaCommittedFlag}
        effectiveDNA={effectiveDNA} isBasic={isBasic}
        fuel={fuel} setFuel={setFuel}
        mileage={mileage} setMileage={setMileage}
        dtcMem={dtcMem} setDtcMem={setDtcMem}
        tier1={tier1} setTier1={setTier1}
        tier2={tier2} setTier2={setTier2}
        misfireCyl={misfireCyl} setMisfireCyl={setMisfireCyl}
        cylCount={cylCount}
        occurs={occurs} setOccurs={setOccurs}
        engState={engState} setEngState={setEngState}
        notes={notes} setNotes={setNotes}
        probeTotal={probeTotal} probeOk={probeOk}
        validationErrors={validationErrors}
      />

      <main className="main">
        <div className="col-header">
          <h2 className="page-title">🔧 4DLab Petrol Diagnostic Engine</h2>
          <p className="page-sub">
            Knowledge-graph-based exhaust gas analysis. Tick the data channels
            you'll enter on the left, then fill in only the panels they open
            below.
            <br />
            <strong>Take measurements only on a warmed-up engine (ECT ≥ 75 °C).</strong>
            {' '}
            {isBasic && modules.dna && (
              <span className="inline-tag basic">basic mode</span>
            )} {!isBasic && (
              <span className="inline-tag dna">DNA committed · {effectiveDNA.make}</span>
            )}
          </p>
        </div>

        {/* 1 — GASLab Low Idle */}
        <Expander icon="📊" title="GASLab (Low Idle)"
                  pill={modules.gaslab ? "V10 idle" : "module off"}
                  helpText={HELP.gasLow}
                  disabled={!modules.gaslab}
                  defaultOpen>
          <div className="caption">RPM source: <strong>V10 Low Idle RPM</strong> (OPSI). Fixed 6-field grid — DNA-independent.</div>
          <GasGrid v={gasLow} onChange={setGasLow} />
          <div className="foot-note">
            <span className="label">consumer →</span> <code>GasLabPayload.gas_co / gas_co2 / gas_hc / gas_o2 / gas_nox / lambda_measured</code> →
            <code> gaslab_adapter → lab_pipeline_aggregator</code>
          </div>
        </Expander>

        {/* 2 — GASLab High Idle */}
        <Expander icon="📊" title="GASLab (High Idle)"
                  pill={modules.gaslab ? "V11 stress" : "module off"}
                  helpText={HELP.gasHigh}
                  disabled={!modules.gaslab}>
          <div className="caption">
            RPM source: <strong>V11 High Idle RPM</strong> (OPSI).
            {effectiveDNA?.stress_idle_rpm_target && (
              <> &nbsp;Hold ≈ <strong>{effectiveDNA.stress_idle_rpm_target} RPM</strong>
                (target λ ≈ <strong>{effectiveDNA.target_lambda_v112?.toFixed(3) ?? "1.000"}</strong>, COC reference).</>
            )}
            {induction !== "NA" && (
              <> &nbsp;<span className="inline-tag">{induction.toLowerCase()}</span> — let boost settle.</>
            )}
          </div>
          <GasGrid v={gasHigh} onChange={setGasHigh} />
          <div className="foot-note">
            <span className="label">consumer →</span> <code>GasLabPayload (high-idle channel)</code> →
            <code> gaslab_adapter → perception_contradiction</code>
          </div>
        </Expander>

        {/* 3 — OBDLab Low Idle */}
        <Expander icon="📈" title="OBDLab (Low Idle)"
                  pill={modules.obdlab ? "V10 idle · live PIDs" : "module off"}
                  helpText={HELP.obdLow}
                  disabled={!modules.obdlab}>
          <div className="caption">
            RPM source: <strong>V10 Low Idle RPM</strong> (OPSI). Stabilised closed-loop, ECT ≥ 75 °C.
            {isBasic && <span className="inline-tag basic" style={{marginLeft:8}}>basic — Bank 1 only, generic O₂</span>}
          </div>
          <ObdGrid v={obdLow} onChange={setObdLow}
                   banks={banks} hasMaf={hasMaf} hasMap={hasMap}
                   o2Type={o2Type} o2Present={o2Present}
                   isBasic={isBasic} />
          <div className="foot-note">
            <span className="label">consumer →</span> <code>OBDLivePayload (low-idle)</code> →
            <code> pid_ingestion_validator → o2_normalizer → trim_vector_aggregator → obdlab_adapter</code>
          </div>
        </Expander>

        {/* 4 — OBDLab High Idle */}
        <Expander icon="📈" title="OBDLab (High Idle)"
                  pill={modules.obdlab ? "U2 stationary noise" : "module off"}
                  helpText={HELP.obdHigh}
                  disabled={!modules.obdlab}>
          <div className="caption">
            RPM source: <strong>U2 RPM</strong> (stationary noise test point, OPSI).
            {induction === "TURBO" && (
              <> &nbsp;<span className="inline-tag">turbo</span> — VE-ceiling check relaxes; read after boost settles.</>
            )}
          </div>
          <ObdGrid v={obdHigh} onChange={setObdHigh}
                   banks={banks} hasMaf={hasMaf} hasMap={hasMap}
                   o2Type={o2Type} o2Present={o2Present}
                   isBasic={isBasic} />
          <div className="foot-note">
            <span className="label">consumer →</span> <code>OBDLivePayload (high-idle)</code> →
            <code> obdlab_adapter → lab_pipeline_aggregator</code>
          </div>
        </Expander>

        {/* 5 — DTCLab DTC */}
        <Expander icon="🗒️" title="DTCLab (DTC)"
                  pill={modules.dtclab ? "Modes $03 / $07 / $0A" : "module off"}
                  helpText={HELP.dtc}
                  disabled={!modules.dtclab}>
          <div className="stack" style={{gap: 14}}>
          <div className="stack-sm">
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <SquareCheckbox checked={mil} onChange={setMil}
                              label="MIL illuminated (solid)" />
              <HelpIcon text="**Check-engine lamp on solid.** Set when one or more confirmed DTCs are emissions-related. → `active_mil`." />
            </div>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <SquareCheckbox checked={milFlash} onChange={setMilFlash}
                              label="MIL flashing (Class-A misfire)" />
              <HelpIcon text="**Lamp flashing** — active Class-A misfire that may damage the catalyst. Stop driving. → `mil_flashing`." />
            </div>
          </div>
            <TextArea
              label="Confirmed DTCs — Mode $03"
              value={dtcConfirmed}
              onChange={setDtcConfirmed}
              placeholder="P0171, P0420, P0300"
              hint="Comma- or space-separated. Each code must match the DTC regex (P/B/C/U + 4 hex digits)."
              helpText="**Active / confirmed DTCs (Mode $03).** Codes the ECU has illuminated for. Format: 1 letter (P/B/C/U) + 4 hex digits. Comma- or space-separated." />
            <TextArea
              label="Pending DTCs — Mode $07"
              value={dtcPending}
              onChange={setDtcPending}
              placeholder="P2002"
              helpText="**Pending DTCs (Mode $07)** — detected once but not yet promoted to confirmed. One more fail cycle and they'll move to $03." />
            <TextArea
              label="Permanent DTCs — Mode $0A"
              value={dtcPerm}
              onChange={setDtcPerm}
              placeholder="P0420"
              helpText="**Permanent DTCs (Mode $0A).** Cannot be cleared by scan-tool — only by the ECU's own readiness drive cycle. Indicate the ECU's persistent fault memory." />
          </div>
          <div className="foot-note">
            <span className="label">consumer →</span> <code>DTCLabPayload.confirmed_dtcs / pending_dtcs / permanent_dtcs / active_mil / mil_flashing</code> →
            <code> routing_tag_mapper → fault_atlas_router</code>
          </div>
        </Expander>

        {/* 6 — DTCLab FF */}
        <Expander icon="📟" title="DTCLab (Freeze Frame)"
                  pill={modules.dtclab ? "Mode $02 · single snapshot" : "module off"}
                  helpText={HELP.ff}
                  disabled={!modules.dtclab}>
          <div className="caption">12 mandatory PIDs. Use the sub-folder below for the 7 extended PIDs.</div>
          <FFGrid ff={ff} setFf={setFf} />

          <div style={{marginTop: 14}}>
            <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <SquareCheckbox
                checked={ffExtended}
                onChange={setFfExtended}
                label="Add extended freeze-frame PIDs" />
              <HelpIcon text="Reveals 7 optional snapshot PIDs (Bank-2 trims, upstream O₂ B1S1, barometric, commanded EGR, run-time, fuel level). Bank-2 / O₂ / EGR rows further gated by VinDNA." />
            </div>
            {ffExtended && (
              <SubFolder tag="extended PIDs (Mode $02 supplemental)">
                <FFExtGrid ff={ff} setFf={setFf} banks={banks}
                           o2Present={o2Present} egrOk={egrOk}
                           isBasic={isBasic} />
              </SubFolder>
            )}
          </div>
          <div className="foot-note">
            <span className="label">consumer →</span> <code>FreezeFrameRecord (12 mandatory + 7 extended)</code> →
            <code> dtclab_adapter → freeze_frame_analyzer</code>
          </div>
        </Expander>

        {/* 7 — DTCLab $06 */}
        <Expander icon="🧪" title="DTCLab ($06 Monitors)"
                  pill={modules.dtclab ? `${m06.length} monitor${m06.length===1?"":"s"}` : "module off"}
                  helpText={HELP.m06}
                  disabled={!modules.dtclab}>
          <div className="caption">3 fields per monitor row. Target component is looked up from <code>mode_06_hex_dictionary.json</code> — read-only.</div>
          <div className="stack" style={{gap: 0}}>
            {m06.map((row, i) => (
              <Mode06Row key={i} idx={i} row={row}
                         onChange={(patch) => {
                           setM06(prev => prev.map((r, j) => j === i ? { ...r, ...patch } : r));
                         }}
                         onDelete={() => setM06(prev => prev.filter((_, j) => j !== i))}
                         canDelete={m06.length > 1} />
            ))}
          </div>
          <button type="button" className="add-row-btn"
                  onClick={() => setM06(prev => [...prev,
                    { id: "", state: "passed", margin: 0 }])}>
            <span className="plus">+</span> Add monitor row
          </button>
          <div className="foot-note">
            <span className="label">consumer →</span> <code>Mode06MonitorResult dict</code> →
            <code> mode06_evaluator → dtclab_adapter</code>
          </div>
        </Expander>
      </main>

      <TweaksPanel title="DNA visibility preview">
        <TweakSection label="DNA override" />
        <TweakRadio label="DNA state"
                    value={t.dnaOverride}
                    options={[
                      { value: "off", label: "Off (VIN)" },
                      { value: "high", label: "Force HIGH" },
                      { value: "basic", label: "Force basic" },
                    ]}
                    onChange={(v) => setTweak("dnaOverride", v)} />
        <div style={{ fontSize: 10.5, color: "rgba(41,38,27,.55)",
                      lineHeight: 1.45, marginTop: -2 }}>
          'Force HIGH' uses the gates below instead of any decoded VIN —
          quick way to preview every visibility rule.
        </div>

        <TweakSection label="If HIGH — gates" />
        <TweakRadio label="Banks" value={t.ovrBanks}
                    options={[{ value: 1, label: "1" }, { value: 2, label: "2" }]}
                    onChange={(v) => setTweak("ovrBanks", v)} />
        <TweakToggle label="MAF sensor" value={t.ovrMaf}
                    onChange={(v) => setTweak("ovrMaf", v)} />
        <TweakToggle label="MAP sensor" value={t.ovrMap}
                    onChange={(v) => setTweak("ovrMap", v)} />
        <TweakSelect label="Upstream O₂ type" value={t.ovrO2Type}
                    options={["NARROWBAND", "WIDEBAND_AFR",
                              "WIDEBAND_LAMBDA", "WIDEBAND_NB_SIM", "NONE"]}
                    onChange={(v) => setTweak("ovrO2Type", v)} />
        <TweakToggle label="Downstream O₂" value={t.ovrDownstream}
                    onChange={(v) => setTweak("ovrDownstream", v)} />
        <TweakToggle label="EGR equipped" value={t.ovrEgr}
                    onChange={(v) => setTweak("ovrEgr", v)} />
        <TweakSelect label="Induction" value={t.ovrInduction}
                    options={["NA", "TURBO", "SUPER"]}
                    onChange={(v) => setTweak("ovrInduction", v)} />
        <TweakSlider label="Cylinder count" value={t.ovrCylinders}
                    min={2} max={12} step={1}
                    onChange={(v) => setTweak("ovrCylinders", v)} />
      </TweaksPanel>
    </div>
  );
}

// =================================================================
// Sidebar
// =================================================================
function Sidebar(p) {
  return (
    <aside className="sidebar">
      <div className="col-header">
        <h1 className="brand">🧬 DNALab</h1>
        <p className="brand-sub">Enter data to enhance diagnose.</p>

        {/* 4.0 — Modules block */}
        <div className="section-title">Modules and Context</div>
      </div>
      <Expander icon="🧩" title="Modules"
                pill={Object.values(p.modules).filter(Boolean).length + " / 4"}
                helpText={HELP.modules}
                sidebar defaultOpen>
        <div className="stack-sm">
          <SquareCheckbox checked={p.modules.gaslab}
            onChange={(v) => p.setModules(m => ({ ...m, gaslab: v }))}
            label="GASLab" />
          <SquareCheckbox checked={p.modules.obdlab}
            onChange={(v) => p.setModules(m => ({ ...m, obdlab: v }))}
            label="OBDLab" />
          <SquareCheckbox checked={p.modules.dtclab}
            onChange={(v) => p.setModules(m => ({ ...m, dtclab: v }))}
            label="DTCLab" />
          <SquareCheckbox checked={p.modules.dna}
            onChange={(v) => p.setModules(m => ({ ...m, dna: v }))}
            label="DNA / VIN" />
        </div>
      </Expander>

      {/* 4.1 — VIN Lookup */}
      {p.modules.dna && (
        <Expander icon="🔍" title="VIN Lookup"
                  pill={p.dna?.confidence ?? null}
                  helpText={HELP.vin}
                  sidebar defaultOpen>
          <TextField
            label="VIN (17 characters)"
            value={p.vin}
            onChange={(v) => p.setVin(v.toUpperCase())}
            placeholder="e.g. WVWZZZ1JZ3W386752"
            maxLength={17}
            monospace
            helpText="Enter the full 17-character VIN. The decoder produces a `VinDNA` with confidence HIGH / PARTIAL / NONE — only **HIGH** commits to gate fields. Try the sample buttons below for known good decodes." />
          <div className="sample-vins">
            <button type="button" className="btn"
                    onClick={() => p.setVin("WVWZZZ1JZ3W386752")}>VW 2.0 TDI</button>
            <button type="button" className="btn"
                    onClick={() => p.setVin("1HGCM82633A123456")}>Civic 1.5</button>
            <button type="button" className="btn"
                    onClick={() => p.setVin("1G1YY26U985123456")}>GM V8 5.3</button>
            <button type="button" className="btn"
                    onClick={() => p.setVin("WBA12345678901234")}>BMW (partial)</button>
            <button type="button" className="btn ghost"
                    onClick={() => p.setVin("")}>clear</button>
          </div>

          {p.dna && p.dna.confidence === "HIGH" && (
            <>
              <div className="dna-summary">
                <div className="row"><span className="k">make</span><span className="v">{p.dna.make}</span></div>
                <div className="row"><span className="k">engine</span><span className="v">{p.dna.engine_code} · {p.dna.displacement_l}L</span></div>
                <div className="row"><span className="k">induction</span><span className="v">{p.dna.induction_type}</span></div>
                <div className="row"><span className="k">banks · cyl</span><span className="v">{p.dna.number_of_banks} bank · {p.dna.cylinder_count} cyl</span></div>
                <div className="row"><span className="k">O₂ arch</span><span className="v">{p.dna.upstream_o2_type}{p.dna.downstream_o2_present ? " · downstream" : ""}</span></div>
                <div className="row"><span className="k">EGR</span><span className="v">{p.dna.egr_equipped ? "yes" : "no"}</span></div>
                <div className="row"><span className="k">euro</span><span className="v">{p.dna.euro_emission_category}</span></div>
              </div>
              <SquareCheckbox
                checked={p.dnaCommittedFlag}
                onChange={p.setDnaCommittedFlag}
                label="Use this decoded DNA" />
              {p.dnaCommittedFlag && (
                <Callout kind="ok">DNA committed for this session — fields gated by hardware.</Callout>
              )}
            </>
          )}
          {p.dna && p.dna.confidence === "PARTIAL" && (
            <Callout kind="info">
              {p.dna.make ?? "Manufacturer"} identified — engine not decoded.
              UI stays in <strong>basic mode</strong> until a HIGH decode arrives.
            </Callout>
          )}
          {p.dna && p.dna.confidence === "NONE" && (
            <Callout kind="warn">
              VIN decode unavailable — using <strong>basic input mode</strong>.
            </Callout>
          )}
        </Expander>
      )}

      {!p.modules.dna && (
        <Callout kind="info">
          DNA / VIN module off — running in <strong>basic input mode</strong>.
          DNA-gated fields are hidden.
        </Callout>
      )}

      {/* 4.3 — Context expanders */}
      <Expander icon="⛽" title="Fuel Blend" sidebar
                helpText={"Affects Brettschneider stoichiometric constants (Hcv, Ocv, AFR). E0 = pure petrol → 14.7:1 stoich; E10 → 14.1:1; E5 sits between."}>
        <SquareRadioStack options={FUEL_OPTS} value={fuelLong(p.fuel)}
          onChange={(v) => p.setFuel(v.split(" ")[0])} />
      </Expander>
      <Expander icon="🛣️" title="Mileage" sidebar
                helpText={"Adjusts wear-related fault priors in `fault_atlas_router` — ring wear, valve seals, timing-chain stretch, turbo seal degradation."}>
        <SquareRadioStack options={MILEAGE_OPTS} value={p.mileage} onChange={p.setMileage} />
      </Expander>
      <Expander icon="🗒️" title="DTC Memory Status" sidebar
                helpText={"`Recently cleared` inhibits trim-derived symptoms because the ECU hasn't re-learned fuel adaptation yet (< 50 mi since clear)."}>
        <SquareRadioStack options={DTC_MEM_OPTS} value={p.dtcMem} onChange={p.setDtcMem} />
      </Expander>

      {/* 4.4 — Symptom */}
      <Expander icon="🩺" title="Primary Symptom"
                helpText={HELP.symptom} sidebar defaultOpen>
        <Selectbox
          label="Primary symptom (Tier 1)"
          value={p.tier1}
          onChange={(v) => { p.setTier1(v); p.setTier2(""); }}
          options={[{ value: "", label: "— Select primary symptom —" },
                    ...SYMPTOM_TREE.map(s => ({ value: s.v, label: s.l }))]}
          helpText="Top-level driver complaint. Routes the diagnosis to a fault family → `SymptomDNA.tier_1_primary_symptom`. Only the 6 catalogued families are offered." />
        {p.tier1 && (
          <SubFolder tag="tier 2 — subfield filter">
            <Selectbox
              value={p.tier2}
              onChange={p.setTier2}
              options={[{ value: "", label: "— Select sub-filter —" },
                        ...((SYMPTOM_TREE.find(s => s.v === p.tier1)?.t2) ?? [])
                          .map(t => ({ value: t.v, label: t.l }))]}
              helpText="Sub-field filter dependent on Tier 1. **Only the 18 catalogued Tier 1 × Tier 2 pairs** are offered — source `allowed_combinations.yaml`." />
            {p.tier1 === "rough_idle_shudder" && (
              <RangeField label={`Misfiring cylinder (1–${p.cylCount})`}
                value={Math.min(p.misfireCyl, p.cylCount)}
                min={1} max={p.cylCount} step={1}
                onChange={p.setMisfireCyl}
                helpText={`Suspect misfire cylinder. Cap = \`cylinder_count\` from VinDNA (currently ${p.cylCount}). Shown only for rough-idle / misfire Tier 1.`} />
            )}
          </SubFolder>
        )}
        <div style={{ marginTop: 12 }}>
          <div className="field-lbl"
               style={{ marginBottom: 6, display: "flex", alignItems: "center",
                        justifyContent: "space-between" }}>
            <span>Occurs during</span>
            <HelpIcon text="When the symptom appears → `environmental_conditions.occurs_during`. Cold-only / hot-only narrow temperature-related faults; intermittent suppresses high-confidence verdicts." />
          </div>
          <SquareRadioStack options={OCCURS_OPTS} value={p.occurs} onChange={p.setOccurs} />
        </div>
        <div style={{ marginTop: 12 }}>
          <div className="field-lbl"
               style={{ marginBottom: 6, display: "flex", alignItems: "center",
                        justifyContent: "space-between" }}>
            <span>Engine state</span>
            <HelpIcon text="Engine state at observation → `environmental_conditions.engine_state`. **Cranking** or **Won't start** suppresses trim and λ analytics in the pipeline." />
          </div>
          <SquareRadioStack options={ENGSTATE_OPTS} value={p.engState} onChange={p.setEngState} />
        </div>
        <div style={{ marginTop: 12 }}>
          <TextArea label="Free-text notes" value={p.notes} onChange={p.setNotes}
            placeholder="Any additional observations…" monospace={false}
            helpText="Free-form description → `SymptomDNA.free_text_notes`. Shown in the report and the `symptom_router` evidence panel. Not parsed." />
        </div>
      </Expander>

      <div className="sidebar-divider" />

      {/* 4.5 — Status panels */}
      <div className="ref-panel">
        <div className="ref-panel-title">Probe Depth Check</div>
        {p.probeOk
          ? <Callout kind="ok">Total CO + CO₂ = {p.probeTotal.toFixed(1)} % (adequate).</Callout>
          : <Callout kind="warn">Total CO + CO₂ = {p.probeTotal.toFixed(1)} % is low. Insert probe ≥ 30 cm into tailpipe.</Callout>}
      </div>
      <div className="ref-panel">
        <div className="ref-panel-title">Validation</div>
        {p.validationErrors.length === 0
          ? <Callout kind="info">Inputs within physical bounds.</Callout>
          : <Callout kind="err">{p.validationErrors.join(" ")}</Callout>}
      </div>

      <button type="button" className="btn primary"
              style={{ width: "100%", marginTop: 18, padding: "10px 14px",
                       fontSize: 14, fontWeight: 600 }}
              onClick={() => window.alert("(demo) Run diagnosis fires lab_pipeline_aggregator with the ticked module channels.")}>
        🔍 Run Diagnosis
      </button>
    </aside>
  );
}

// Map E0/E5/E10 → display label
function fuelLong(short) {
  return { "E0": "E0", "E5": "E5", "E10": "E10" }[short] || short;
}

// =================================================================
// GASLab — 6 fields, 3 per row
// =================================================================
function GasGrid({ v, onChange }) {
  const set = (k) => (n) => onChange({ ...v, [k]: n });
  return (
    <>
      <div className="grid-3">
        <NumField label="CO" unit="%" min={0} max={15} step={0.01}
                  value={v.co} onChange={set("co")}
                  helpText="**Carbon monoxide** at the tailpipe. Healthy idle < 0.5 %. Range 0–15 %, step 0.01. Probe must sit ≥ 30 cm in the pipe — sidebar Probe-Depth check confirms total CO + CO₂ ≥ 12 %." />
        <NumField label="CO₂" unit="%" min={0} max={22} step={0.1}
                  value={v.co2} onChange={set("co2")}
                  helpText="**Carbon dioxide.** Healthy warm idle ≈ 14–15 %. Low CO₂ with elevated O₂ hints at dilution / probe-depth issues. Range 0–22 %." />
        <NumField label="HC" unit="ppm" min={0} max={20000} step={1}
                  value={v.hc} onChange={set("hc")}
                  helpText="**Unburnt hydrocarbons.** Healthy idle < 100 ppm. Spikes flag misfire, oil burn or cat inefficiency. Range 0–20 000 ppm." />
      </div>
      <div className="grid-3" style={{marginTop: 14}}>
        <NumField label="O₂" unit="%" min={0} max={22} step={0.01}
                  value={v.o2} onChange={set("o2")}
                  helpText="**Residual oxygen.** Stoichiometric idle < 1 %; rising O₂ with rising HC = misfire / exhaust leak. Range 0–22 %." />
        <NumField label="NOx" unit="ppm" min={0} max={5000} step={1}
                  value={v.nox} onChange={set("nox")}
                  helpText="**Oxides of nitrogen.** > 100 ppm at idle suggests EGR / combustion-temp issues; < 50 ppm with lean λ flags ECU/sensor inversion. Range 0–5 000 ppm." />
        <NumField label="Measured λ (analyser)" unit="λ"
                  min={0.5} max={2.0} step={0.001}
                  value={v.lambda} onChange={set("lambda")}
                  hint="No-OBD fallback for perception-contradiction (T-FX-7)"
                  helpText="**Wideband λ reading from the analyser.** When OBDLab is off, this value passes through `perception_contradiction.select_perception_lambda` to the perception-contradiction detector in place of the OBD lambda. Range 0.500–2.000." />
      </div>
    </>
  );
}

// =================================================================
// OBDLab — 4 per row, DNA-gated
// =================================================================
function ObdGrid({ v, onChange, banks, hasMaf, hasMap, o2Type, o2Present, isBasic }) {
  const set = (k) => (n) => onChange({ ...v, [k]: n });
  const o2 = upstreamO2Meta(isBasic ? "NARROWBAND" : o2Type);

  // Effective gates in basic mode:
  const showB2 = !isBasic && banks === 2;
  const showMaf = isBasic ? false : hasMaf;
  const showMap = isBasic ? false : hasMap;
  const showO2 = isBasic ? true : (o2Type !== "NONE");
  const showDn = isBasic ? false : o2Present;

  return (
    <>
      <div className="grid-4">
        <NumField label="Engine RPM" unit="rpm" min={0} max={8000} step={1}
                  value={v.rpm} onChange={set("rpm")}
                  helpText="Stabilised RPM at the **V10 (low)** / **U2 (high)** measurement point. Range 0–8 000, int." />
        <NumField label="Coolant temp ECT" unit="°C" min={-40} max={140} step={1}
                  value={v.ect} onChange={set("ect")}
                  helpText="Coolant temperature. **Must be ≥ 75 °C** — the thermal gate freezes trim / λ analytics below this. Range −40 – 140 °C." />
        <NumField label="Calc load" unit="%" min={0} max={100} step={0.1}
                  value={v.load} onChange={set("load")}
                  helpText="Calculated engine load PID 04. Idle 15–25 %, WOT → ~100 %." />
        <NumField label="STFT B1" unit="%" min={-100} max={99.22} step={0.01}
                  value={v.stft1} onChange={set("stft1")}
                  helpText="**Short-term fuel trim, Bank 1.** Healthy ± 5 %. Compared with LTFT and B2 to localise lean / rich faults." />
        <NumField label="LTFT B1" unit="%" min={-100} max={99.22} step={0.01}
                  value={v.ltft1} onChange={set("ltft1")}
                  helpText="**Long-term fuel trim, Bank 1.** Healthy ± 5 %. > +10 % = lean correction; < −10 % = rich correction." />

        {showO2 && (
          <NumField
            label={<span>{o2.label} <span className="inline-tag dna-gated">{o2Type}</span></span>}
            unit={o2.unit} min={o2.min} max={o2.max} step={o2.step}
            value={v.o2_up} onChange={set("o2_up")}
            helpText={`**Upstream O₂ sensor.** Polymorphic by \`upstream_o2_type\` — currently ${o2Type}. Narrowband: 0.1–0.9 V switching. Wideband λ: 0.7–1.3 around 1.0. Wideband AFR: ≈14.7:1 stoich. Normalised via \`o2_normalizer\` for cross-check with \`lambda_chem\`.`}
          />
        )}
      </div>

      {(showB2 || showMaf || showMap || showDn) && (
        <SubFolder tag="DNA-gated fields">
          <div className="grid-4">
            {showB2 && (
              <>
                <NumField label="STFT B2" unit="%" min={-100} max={99.22} step={0.01}
                          value={v.stft2} onChange={set("stft2")}
                          helpText="Short-term fuel trim, **Bank 2**. V-engine only. Bank-divergent trims (|B1 − B2| > 5 %) hint at one-side faults: injector, vacuum leak, O₂ sensor on that bank." />
                <NumField label="LTFT B2" unit="%" min={-100} max={99.22} step={0.01}
                          value={v.ltft2} onChange={set("ltft2")}
                          helpText="Long-term fuel trim, **Bank 2**. Compare with B1 for asymmetry." />
              </>
            )}
            {showMaf && (
              <NumField label="MAF" unit="g/s" min={0} max={655.35} step={0.01}
                        value={v.maf} onChange={set("maf")}
                        helpText="Mass-airflow PID 10. Drives the VE-ceiling check (Physics Gate 3). Range 0–655.35 g/s." />
            )}
            {showMap && (
              <NumField label="MAP / manifold vacuum" unit="kPa" min={0} max={255} step={1}
                        value={v.map} onChange={set("map")}
                        helpText="Manifold absolute pressure PID 0B. Idle ≈30–40 kPa NA / 100–130 kPa boost. Feeds VE engine." />
            )}
            {showDn && (
              <NumField label="Downstream O₂ S12" unit="V" min={0} max={1.5} step={0.01}
                        value={v.o2_dn} onChange={set("o2_dn")}
                        helpText="**Post-catalyst narrowband.** Steady 0.7–0.8 V = healthy cat. Active 0.3–0.7 V sweep with P0420 = cat inefficient." />
            )}
          </div>
        </SubFolder>
      )}
    </>
  );
}

// =================================================================
// Freeze Frame — 12 mandatory @ 4 per row
// =================================================================
function FFGrid({ ff, setFf }) {
  const set = (k) => (n) => setFf({ ...ff, [k]: n });
  return (
    <>
      <div className="grid-4">
        <NumField label="Calc load" unit="%" min={0} max={100} step={0.1}
                  value={ff.load} onChange={set("load")}
                  helpText="Engine load at the moment the ECU stored this snapshot. Single-value PID 04. Range 0–100 %." />
        <NumField label="Engine RPM" unit="rpm" min={0} max={16383} step={1}
                  value={ff.rpm} onChange={set("rpm")}
                  helpText="RPM at the moment the DTC set. **Freeze-frame range is wider** than live (0–16 383)." />
        <NumField label="Coolant temp ECT" unit="°C" min={-40} max={215} step={1}
                  value={ff.ect} onChange={set("ect")}
                  helpText="ECT at the snapshot. Below 75 °C flips `ff_ect_warmup = true` and downstream analytics relax." />
        <NumField label="STFT B1" unit="%" min={-100} max={99.22} step={0.01}
                  value={ff.stft1} onChange={set("stft1")}
                  helpText="Short-term fuel trim, Bank 1, **at the snapshot**. Healthy ± 5 %." />

        <NumField label="LTFT B1" unit="%" min={-100} max={99.22} step={0.01}
                  value={ff.ltft1} onChange={set("ltft1")}
                  helpText="Long-term fuel trim, Bank 1. > +25 % at low load = lean adaptation pinned." />
        <NumField label="MAP" unit="kPa" min={0} max={255} step={1}
                  value={ff.map} onChange={set("map")}
                  helpText="Manifold pressure at snapshot. Combined with RPM → `ff_load_high_at_low_rpm` flag." />
        <NumField label="Vehicle speed" unit="km/h" min={0} max={255} step={1}
                  value={ff.speed} onChange={set("speed")}
                  helpText="Snapshot road speed. 0 km/h at idle, > 0 → fault triggered while driving." />
        <NumField label="Ignition advance" unit="°BTDC" min={-64} max={63.5} step={0.5}
                  value={ff.ignition} onChange={set("ignition")}
                  hint="Neg = ATDC"
                  helpText="Ignition timing at snapshot. **Severe retard** (> 10 ° below expected) flips `ff_timing_retard_severe = true` → knock protection." />

        <NumField label="Intake air temp IAT" unit="°C" min={-40} max={215} step={1}
                  value={ff.iat} onChange={set("iat")}
                  helpText="IAT at snapshot. IAT > ECT in cold start = bias on one sensor → `ff_iat_ect_biased` flag." />
        <NumField label="MAF" unit="g/s" min={0} max={655.35} step={0.01}
                  value={ff.maf} onChange={set("maf")}
                  helpText="Mass-airflow at snapshot. Compared with RPM & load for VE consistency." />
        <NumField label="Throttle" unit="%" min={0} max={100} step={0.1}
                  value={ff.throttle} onChange={set("throttle")}
                  helpText="Throttle position at snapshot. 0–20 % idle / cruise; > 80 % = WOT enrichment expected." />
        <div className="field">
          <div className="field-row" style={{ alignItems: "flex-start" }}>
            <div style={{ flex: 1 }}>
              <label className="field-lbl">Fuel-system status</label>
              <div className="sq-radio-stack" style={{ paddingTop: 2 }}>
                <SquareRadioStack options={FF_FUEL_STATUS}
                  value={ff.fuel_status}
                  onChange={(v) => setFf({ ...ff, fuel_status: v })} />
              </div>
            </div>
            <HelpIcon text={"**Fuel-system status at snapshot.** CL = closed-loop, OL = open-loop, OL_DRIVE = accel enrichment, OL_FAULT = forced open-loop due to fault. Open-loop at low load → `ff_open_loop_at_fault` derived flag."} />
          </div>
        </div>
      </div>
    </>
  );
}

// Extended FF — 7 PIDs, 4 per row, DNA-gated
function FFExtGrid({ ff, setFf, banks, o2Present, egrOk, isBasic }) {
  const set = (k) => (n) => setFf({ ...ff, [k]: n });
  const showB2 = !isBasic && banks === 2;
  const showO2 = !isBasic && o2Present;
  const showEgr = !isBasic && egrOk;
  return (
    <div className="grid-4">
      {showB2 && (
        <>
          <NumField label="STFT B2" unit="%" min={-100} max={99.22} step={0.01}
                    value={ff.stft2} onChange={set("stft2")}
                    helpText="Short-term fuel trim, **Bank 2**, at snapshot. V-engines only." />
          <NumField label="LTFT B2" unit="%" min={-100} max={99.22} step={0.01}
                    value={ff.ltft2} onChange={set("ltft2")}
                    helpText="Long-term fuel trim, **Bank 2**, at snapshot. Compare with B1 for asymmetry." />
        </>
      )}
      {showO2 && (
        <NumField label="Upstream O₂ B1S1" unit="V" min={0} max={1.275} step={0.001}
                  value={ff.o2_b1s1} onChange={set("o2_b1s1")}
                  helpText="Narrowband upstream sensor voltage **at the frozen snapshot** (not live). Range 0.000–1.275 V, step 0.001." />
      )}
      <NumField label="Barometric pressure" unit="kPa" min={0} max={255} step={1}
                value={ff.baro} onChange={set("baro")}
                helpText="Atmospheric pressure at snapshot. < 92 kPa hints at altitude effects on mixture." />
      {showEgr && (
        <NumField label="Commanded EGR" unit="%" min={0} max={100} step={0.1}
                  value={ff.egr} onChange={set("egr")}
                  helpText="% EGR commanded by ECU at snapshot. EGR-equipped engines only." />
      )}
      <NumField label="Run time since start" unit="s" min={0} max={65535} step={1}
                value={ff.runtime} onChange={set("runtime")}
                helpText="Seconds since engine start at snapshot. Short runtime + cold ECT → warm-up bias on chemistry." />
      <NumField label="Fuel level" unit="%" min={0} max={100} step={0.1}
                value={ff.fuel_level} onChange={set("fuel_level")}
                helpText="Fuel tank level at snapshot. < 15 % can trigger EVAP / pump issues." />
    </div>
  );
}

// =================================================================
// Mode $06 monitor row
// =================================================================
function Mode06Row({ idx, row, onChange, onDelete, canDelete }) {
  const lookup = MID_LOOKUP[row.id?.toUpperCase()] || null;
  return (
    <div className="repeat-row">
      <div className="row-head">
        <span>Monitor #{idx + 1}</span>
        {canDelete && (
          <button className="row-del" onClick={onDelete}>✕ remove</button>
        )}
      </div>
      <div className="grid-3">
        <TextField label="Monitor ID"
          value={row.id}
          onChange={(v) => onChange({ id: v.toUpperCase() })}
          placeholder="MID_A2_TID_0B" monospace
          helpText="**Monitor / Test ID** in `MID_<HEX>_TID_<HEX>` form. E.g. `MID_A2_TID_0B` = O₂ sensor B1S2 switching time. Looked up in `mode_06_hex_dictionary.json`." />
        <div className="field">
          <div className="field-row" style={{ alignItems: "flex-start" }}>
            <div style={{ flex: 1 }}>
              <label className="field-lbl">Result state</label>
              <SquareRadioStack options={M06_STATE}
                value={row.state} onChange={(v) => onChange({ state: v })} />
            </div>
            <HelpIcon text="**Monitor self-test result.** Passed = > 15 % margin; Pending = 1–15 % margin; Critical fail = ≤ 0 % (past limit). Maps to `Mode06MonitorState`." />
          </div>
        </div>
        <NumField label="Margin" unit="%" min={-100} max={100} step={1}
                  value={row.margin}
                  onChange={(v) => onChange({ margin: v })}
                  hint="Neg = past limit"
                  helpText="% margin from monitor limit. **> 15 % pass · 1–15 % marginal · ≤ 0 % critical fail.** Read directly from the scanner's Mode $06 output." />
      </div>
      <div className="lookup-display">
        <span className="lkl">target_component →</span>
        {lookup ? lookup : <em>(enter MID_*_TID_* above to look up)</em>}
      </div>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
