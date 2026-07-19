// 4DLab UI — shared components
// Streamlit-flavoured form primitives + helpers.

const { useState, useRef, useEffect, useCallback } = React;

// ── Expander ────────────────────────────────────────────────────────
function Expander({ title, icon, helpText, defaultOpen = false,
                    sidebar = false, disabled = false, pill = null,
                    children }) {
  const [open, setOpen] = useState(defaultOpen);
  return (
    <div className={[
      "expander",
      open ? "open" : "",
      sidebar ? "sidebar-ex" : "",
      disabled ? "disabled" : "",
    ].filter(Boolean).join(" ")}>
      <button type="button" className="head"
              onClick={() => setOpen(o => !o)}
              aria-expanded={open}>
        <span className="chev">▶</span>
        <span className="label">
          {icon && <span>{icon}</span>}
          <span>{title}</span>
          {pill && <span className="pill">{pill}</span>}
        </span>
        {helpText && (
          <span onClick={(e) => e.stopPropagation()}>
            <HelpIcon text={helpText} />
          </span>
        )}
      </button>
      {open && <div className="body">{children}</div>}
    </div>
  );
}

// ── Help circle ('?') ───────────────────────────────────────────────
function HelpIcon({ text }) {
  // Allow simple **bold** markup
  const html = String(text)
    .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
    .replace(/\*\*(.+?)\*\*/g, "<em>$1</em>")
    .replace(/\n/g, "<br/>");
  return (
    <span className="help" tabIndex={0} aria-label="Help">?
      <span className="tip" dangerouslySetInnerHTML={{ __html: html }} />
    </span>
  );
}

// ── Square checkbox ─────────────────────────────────────────────────
function SquareCheckbox({ checked, onChange, label, disabled = false,
                          children }) {
  return (
    <label className={"sqcheck" + (disabled ? " disabled" : "")}>
      <input type="checkbox" checked={!!checked} disabled={disabled}
             onChange={e => onChange && onChange(e.target.checked)} />
      <span className="box" />
      <span className="lbl">{label || children}</span>
    </label>
  );
}

// Vertical stack of square checkboxes used as single-select group
// (mirrors the _check_radio helper in app.py). Always one checked.
function SquareRadioStack({ options, value, onChange }) {
  return (
    <div className="sq-radio-stack" role="radiogroup">
      {options.map(opt => {
        const v = typeof opt === "object" ? opt.value : opt;
        const l = typeof opt === "object" ? opt.label : opt;
        const on = v === value;
        return (
          <label key={v} className="sqcheck" role="radio" aria-checked={on}>
            <input type="checkbox" checked={on}
                   onChange={() => {
                     // unchecking the active one re-checks it (like _check_radio)
                     if (!on) onChange && onChange(v);
                   }} />
            <span className="box" />
            <span className="lbl">{l}</span>
          </label>
        );
      })}
    </div>
  );
}

// ── Number input with +/- stepper (Streamlit st.number_input look) ──
function NumField({ label, value, onChange, min, max, step = 1,
                    unit, hint, helpText, disabled = false, decimals }) {
  const dec = decimals != null ? decimals
    : (String(step).split(".")[1] || "").length;
  const clamp = (n) => {
    if (Number.isNaN(n)) return value;
    if (min != null && n < min) n = min;
    if (max != null && n > max) n = max;
    return Number(n.toFixed(dec));
  };
  const handle = (delta) => {
    const cur = typeof value === "number" ? value : Number(value) || 0;
    onChange && onChange(clamp(cur + delta * step));
  };
  return (
    <div className="field">
      <label className="field-lbl">{label}</label>
      <div className="field-row">
        <div className={"numwrap" + (disabled ? " disabled" : "")}>
          <input type="number" value={value ?? ""} min={min} max={max}
                 step={step} disabled={disabled}
                 onChange={e => {
                   const v = e.target.value;
                   if (v === "" || v === "-") { onChange && onChange(v); return; }
                   const n = Number(v);
                   if (!Number.isNaN(n)) onChange && onChange(clamp(n));
                 }} />
          {unit && <span className="unit-suffix">{unit}</span>}
          <span className="stepper">
            <button type="button" tabIndex={-1} disabled={disabled}
                    onClick={() => handle(+1)} aria-label="Increase">+</button>
            <button type="button" tabIndex={-1} disabled={disabled}
                    onClick={() => handle(-1)} aria-label="Decrease">−</button>
          </span>
        </div>
        {helpText && <HelpIcon text={helpText} />}
      </div>
      {hint && <div className="caption-inline">{hint}</div>}
    </div>
  );
}

// ── Text input ──────────────────────────────────────────────────────
function TextField({ label, value, onChange, placeholder, hint, helpText,
                     maxLength, monospace = false }) {
  return (
    <div className="field">
      {label && <label className="field-lbl">{label}</label>}
      <div className="field-row">
        <input type="text"
               value={value ?? ""}
               placeholder={placeholder}
               maxLength={maxLength}
               style={monospace ? { fontFamily: "var(--mono)", letterSpacing: ".02em" } : null}
               onChange={e => onChange && onChange(e.target.value)} />
        {helpText && <HelpIcon text={helpText} />}
      </div>
      {hint && <div className="caption-inline">{hint}</div>}
    </div>
  );
}

function TextArea({ label, value, onChange, placeholder, rows = 3,
                    hint, helpText, monospace = true }) {
  return (
    <div className="field">
      {label && <label className="field-lbl">{label}</label>}
      <div className="field-row field-row-top">
        <textarea rows={rows} value={value ?? ""} placeholder={placeholder}
                  style={monospace ? null : { fontFamily: "var(--font)" }}
                  onChange={e => onChange && onChange(e.target.value)} />
        {helpText && <HelpIcon text={helpText} />}
      </div>
      {hint && <div className="caption-inline">{hint}</div>}
    </div>
  );
}

function Selectbox({ label, value, onChange, options, hint, helpText }) {
  return (
    <div className="field">
      {label && <label className="field-lbl">{label}</label>}
      <div className="field-row">
        <select value={value ?? ""} onChange={e => onChange && onChange(e.target.value)}>
          {options.map(o => {
            const v = typeof o === "object" ? o.value : o;
            const l = typeof o === "object" ? o.label : o;
            return <option key={v ?? ""} value={v ?? ""}>{l}</option>;
          })}
        </select>
        {helpText && <HelpIcon text={helpText} />}
      </div>
      {hint && <div className="caption-inline">{hint}</div>}
    </div>
  );
}

// ── Sub-folder indent reveal ────────────────────────────────────────
function SubFolder({ tag, children }) {
  return (
    <div className="subfolder">
      <div className="spacer" />
      <div className="body-sub">
        {tag && <div className="subfolder-tag">{tag}</div>}
        {children}
      </div>
    </div>
  );
}

// ── Callout / inline tags ───────────────────────────────────────────
function Callout({ kind = "info", icon, children }) {
  const ico = icon || ({ warn: "⚠", ok: "✓", err: "✕", info: "ℹ" })[kind];
  return (
    <div className={"callout " + kind}>
      <span className="ico">{ico}</span>
      <span>{children}</span>
    </div>
  );
}

// ── Range slider for misfire cylinder ───────────────────────────────
function RangeField({ label, value, min, max, step = 1, onChange, hint, helpText }) {
  return (
    <div className="field">
      <label className="field-lbl">{label}</label>
      <div className="field-row">
        <div className="range-row" style={{ flex: 1 }}>
          <input type="range" min={min} max={max} step={step} value={value}
                 onChange={e => onChange && onChange(Number(e.target.value))} />
          <span className="v">{value}</span>
        </div>
        {helpText && <HelpIcon text={helpText} />}
      </div>
      {hint && <div className="caption-inline">{hint}</div>}
    </div>
  );
}

// ── DNA decoder (sample VINs) ───────────────────────────────────────
// Three deterministic sample decodes that exercise every visibility rule
// in FieldMap §2. Anything else → confidence NONE (drops to basic mode).
const SAMPLE_DNA = {
  // VW 2.0 TDI — small turbo with EGR, wideband λ, downstream O₂
  "WVWZZZ1JZ3W386752": {
    confidence: "HIGH",
    make: "Volkswagen",
    engine_code: "BKD",
    displacement_l: 2.0,
    year_range: [2003, 2008],
    induction_type: "TURBO",
    fuel_delivery_type: "DI",
    number_of_banks: 1,
    cylinder_count: 4,
    has_maf_sensor: true,
    has_map_sensor: true,
    upstream_o2_type: "WIDEBAND_LAMBDA",
    downstream_o2_present: true,
    egr_equipped: true,
    has_catalyst: true,
    euro_emission_category: "EURO_4",
    resolved_horizon: "MODERN",
    stress_idle_rpm_target: 2500,
    target_lambda_v112: 1.000,
    co_low_idle: 0.30,
    co_high_idle: 0.20,
  },
  // Civic 1.5 i-VTEC — small NA I4, narrowband, single bank, MAF only, no EGR
  "1HGCM82633A123456": {
    confidence: "HIGH",
    make: "Honda",
    engine_code: "L15A",
    displacement_l: 1.5,
    year_range: [2006, 2011],
    induction_type: "NA",
    fuel_delivery_type: "PFI",
    number_of_banks: 1,
    cylinder_count: 4,
    has_maf_sensor: true,
    has_map_sensor: false,
    upstream_o2_type: "NARROWBAND",
    downstream_o2_present: true,
    egr_equipped: false,
    has_catalyst: true,
    euro_emission_category: "EURO_4",
    resolved_horizon: "MODERN",
    stress_idle_rpm_target: 2500,
    target_lambda_v112: 1.000,
    co_low_idle: 0.50,
    co_high_idle: 0.30,
  },
  // GM V8 5.3 — two banks, MAF, narrowband, EGR-equipped
  "1G1YY26U985123456": {
    confidence: "HIGH",
    make: "Chevrolet",
    engine_code: "LS4",
    displacement_l: 5.3,
    year_range: [2005, 2009],
    induction_type: "NA",
    fuel_delivery_type: "PFI",
    number_of_banks: 2,
    cylinder_count: 8,
    has_maf_sensor: true,
    has_map_sensor: true,
    upstream_o2_type: "NARROWBAND",
    downstream_o2_present: true,
    egr_equipped: true,
    has_catalyst: true,
    euro_emission_category: "EURO_4",
    resolved_horizon: "MODERN",
    stress_idle_rpm_target: 2500,
    target_lambda_v112: 1.000,
    co_low_idle: 0.50,
    co_high_idle: 0.30,
  },
  // Partial decode — manufacturer only
  "WBA12345678901234": {
    confidence: "PARTIAL",
    make: "BMW",
    engine_code: null,
    displacement_l: null,
  },
};

function decodeVIN(vin) {
  const v = String(vin || "").trim().toUpperCase();
  if (v.length !== 17) return null;
  if (SAMPLE_DNA[v]) return SAMPLE_DNA[v];
  return { confidence: "NONE", make: null };
}

// Expose to window so app.jsx (separate Babel scope) can use them
Object.assign(window, {
  Expander, HelpIcon, SquareCheckbox, SquareRadioStack,
  NumField, TextField, TextArea, Selectbox,
  SubFolder, Callout, RangeField,
  decodeVIN, SAMPLE_DNA,
});
