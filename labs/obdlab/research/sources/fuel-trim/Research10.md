Here is a breakdown of the answers to your technical research questions. This analysis draws from industry resources, technical forums, and official documentation to help ground your diagnostic module in realistic fleet behavior.

---

### 1. Realistic STFT/LTFT Magnitudes and Signs per Fault Family at Warm Idle (1990–2010 Petrol)

#### What are the typical ranges for a healthy engine at warm idle?
In closed‑loop operation, the STFT and LTFT values for a healthy engine should be between **±5%**. Slightly higher readings can be acceptable, but once you see **double‑digit** numbers (≥ ± 10 %), it usually signals a genuine problem. One authoritative service tip puts the threshold even tighter, recommending that trims above ±8 % warrant a thorough diagnostic check.

#### How do the faults break down by family?

| Fault Family | Typical STFT at Warm Idle | Typical LTFT at Warm Idle | Sign | Mechanism |
| :--- | :--- | :--- | :--- | :--- |
| **Vacuum leak / unmetered air** (unmetered air) | Low or normal (ECM counteracts) | **High positive** (e.g., +15…+25 %) | + | ECM adds fuel to compensate for excess air. LTFT absorbs the correction. |
| **MAF sensor under‑reporting** | Normal or slightly high | **High positive** | + | ECM adds fuel to compensate for falsely low airflow reading. |
| **Fuel delivery problem** (low pressure, clogged injector) | High (ECM tries to compensate) | **High positive** | + | Lean condition drives trims up. |
| **Rich mixture / over‑fueling** (leaking injector, high pressure) | Low or normal | **High negative** (e.g., –10…–25 %) | – | ECM pulls fuel to compensate. |
| **O2 / AFR sensor biased** | May be erratic | **Moderate positive or negative** | ± | Sensor offset causes false lean or rich reading. |

In a real‑world example from a BMW 330i, an intake vacuum leak produced LTFT values of +24 % / +25 % while STFT remained near 0 %, because the LTFT had already absorbed the entire long‑term correction.

#### How do manufacturers decide when to set a DTC?
The P0171 / P0172 (lean / rich) codes are triggered when the **sum of STFT + LTFT** exceeds a calibrated threshold. Toyota documents that a total trim within ±35 % is still considered normal; the actual DTC threshold is often lower, around ±18 % on many vehicles. This means that after a code sets, the trims may already be quite large before the driver ever sees a warning light.

---

### 2. Do Real STFT/LTFT PIDs Ever Reach ±100 % / ±127 %?

Yes, the PID values can reach the full ±100 % range, but this is **rare in normal closed‑loop operation** and is more of a **sentinel convention** than a realistic measured trim. The ±99 % values you sometimes see on a scan tool indicate that the ECM is attempting to deliver the maximum possible fuel correction; it is a diagnostic flag rather than a physically plausible trim value.

#### Shorted / open O₂ sensor – what does a scan‑tool actually report?
- **Narrowband sensor voltage range:** A healthy narrowband sensor swings between **0.1 V** (lean) and **0.9 V** (rich), with a pivot point around **0.45 V**.
- **Shorted sensor:** If the O₂ sensor signal circuit is shorted to a reference voltage, all O₂ sensor voltage readings on the scan tool will read approximately **5.0 V**.
- **Open circuit / sensor heater failure:** The sensor produces little or no voltage. In many systems, the ECM will detect a flat signal near 0 V or a signal that does not cross the stoichiometric pivot point, setting a DTC like P0134 (open circuit).

Thus, the ±127 bound on fuel trim PIDs is a **range limit sentinel**—you might see a shorted O₂ cause the ECM to drive fuel trims to one extreme, but the PID itself will still saturate at the ±127 bound.

---

### 3. OBD‑II Protocols and Availability of Commanded λ / λ Perception Δ (Question 4)

**Commanded equivalence ratio (λ) is a standard OBD‑II PID**, but its availability across the 1990–2010 fleet is **not universal**.

- **Standard PIDs for λ:** The SAE J1979 standard defines multiple modes and PIDs for air‑fuel ratio data:
  - **PID 0x13** – commanded equivalence ratio.
  - **PID 0x1D** – a newer, higher‑resolution PID.
  - **PIDs 0x24–0x2B** and **0x34–0x3B** provide sensor‑specific λ data for bank 1 / sensor 1 etc.

- **Mutual exclusivity:** A vehicle will support either PID 0x13 or PID 0x1D, never both. The data from PIDs 0x24‑0x2B or 0x34‑0x3B must be parsed together with the supported λ PID.

- **Manufacturer / model‑year coverage:** Many generic scan tools do not request these higher‑level PIDs. A Porsche forum post notes that you need a manufacturer‑specific data logger to obtain PIDs 0x34 and 0x36 because most standard OBD‑II readers do not support them.

- **Practical advice:** To compute a `lambda_perception_delta` in your module, you **must first check the vehicle’s supported PIDs** using Mode 1 PID 0x00. If none of the λ PIDs are supported, you cannot obtain commanded λ. In that case, you can fall back to using **STFT as a proxy** for how far the ECM is actively chasing the λ target.

---

### 4. VE Cross‑Check on Single‑Air‑Sensor (MAP‑only or MAF‑only) Engines

**Yes, a valid VE cross‑check is possible, but it requires an assumed, or “target”, VE value rather than a direct cross‑check between two independent measurements.**

- **MAF‑only engines (no MAP):**  
  The standard VE formula requires both MAF and MAP. Without a MAP sensor, the ECM and a scan tool cannot directly compute a measured VE. However, you can **infer MAP** from MAF, RPM, displacement, and IAT using the ideal gas law. Once you have an inferred MAP, you can then calculate a “virtual” VE. The accuracy of this inference depends on how well the engine matches the assumed volumetric efficiency at that operating point; for diagnostic purposes, it is still useful for detecting large MAF sensor errors or air metering problems.

- **MAP‑only (speed‑density) engines (no MAF):**  
  Similarly, you can **infer MAF** from MAP, RPM, displacement, and IAT. The inferred MAF can then be used to compute a VE that can be compared against a target VE for that engine family. This approach is widely used in aftermarket tuning and diagnostics: the ECU adjusts its VE table until the measured λ matches the target λ, thereby back‑calculating a correct air mass.

- **Bottom line:** While a true “cross‑check” against a second independent air meter is not possible, **single‑sensor engines can still support meaningful VE‑based diagnostics** by comparing the calculated VE against an expected, or “target”, VE for that engine and operating condition.

---

### 5. Fuel Trim Support and Trustworthiness Pre‑2001

- **OBD‑II mandate in the US:** Model year **1996 and newer** vehicles are OBD‑II compliant, which includes fuel trim PIDs as a mandatory part of the emissions monitoring system.
- **Pre‑2001 coverage:** While the hardware is present, **live data support can be spotty**, especially on early OBD‑II implementations and certain European models. A forum discussion notes that “a few manufacturers that we know have some OBD‑II/EOBD support” before 2001, but it is far from universal.

**Trustworthiness of pre‑2001 fuel trims:**
Fuel trim data from this era is **generally reliable** for gross fault detection (e.g., a large vacuum leak), but it may be less accurate for fine‑grained diagnostics. The main limitation is that the **resolution and update rate** of the data stream can be lower than on modern vehicles, making it harder to capture fast transient behavior.

---

### 6. Downstream O₂ Behavior as a Masking Indicator (Secondary Trim)

**Yes, on some engine management systems (notably Bosch Motronic ME7 and similar), the downstream O₂ sensor does influence fuel trims.** This is not a “secondary trim loop” in the way a post‑cat sensor actively controls fuel; rather, the ECM uses the downstream signal to **adapt or verify the upstream control loop**.

- **How it works:** In the Bosch ME7 strategy, a further trim control based on the signal(s) from the rear O₂ sensor(s) corrects the adaptation factor. This helps to detect any deviation from the characteristic curve of the upstream oxygen sensor (e.g., sensor poisoning).
- **Scan‑tool detectable metrics:** You can monitor both upstream and downstream sensor voltages. A healthy downstream sensor will show a **smoother, more stable signal** than the upstream, oscillating in a narrower voltage range (often 0.3–0.6 V). If the downstream waveform begins to spike as rapidly as the upstream, the catalytic converter is losing efficiency and may no longer be masking an upstream sensor problem.
- **Detection of masking:** If you see large, sustained fuel trims **but** the downstream sensor does not show the expected smoothed signal and instead closely follows the upstream pattern, that suggests the catalyst is no longer masking the upstream drift, and the ECM may be entering a secondary correction mode.

---

### 7. Scan‑Tool Metrics to Distinguish a Lazy / Aged O₂ Sensor from a Biased or Dead One

#### Key metrics exposed via generic OBD‑II scan tools:

| Metric | What it reveals | Healthy threshold / behavior |
| :--- | :--- | :--- |
| **O₂ sensor voltage** | Instantaneous signal | 0.1–0.9 V, crossing 0.45 V several times per second. |
| **Short‑Term Fuel Trim (STFT)** | ECM reaction to sensor signal | Varies with voltage; stable STFT ≈0 % indicates no net correction. |
| **Freeze frame data** | Sensor voltage at the moment a DTC was set | Shows if the voltage was stuck, extremely low, or extremely high. |
| **P0133 (Slow response)** | Slow sensor switching | Set when the sensor fails to switch lean‑to‑rich or rich‑to‑lean within a calibrated time (e.g., 20–40 ms). |

#### Differentiating the failure modes:

| Failure mode | Scan‑tool behavior | Typical DTC |
| :--- | :--- | :--- |
| **Lazy / aged** (slow response) | Voltage signal switches less frequently (< 1 Hz) or takes longer than 20–40 ms to cross the 0.45 V midpoint. STFT may show slow‑to‑correct patterns. | P0133 |
| **Biased low** (constant lean reading) | Voltage stays **below 0.1–0.2 V**, even when the fuel mixture is known to be rich. ECM drives fuel trims high positive. | P0131 (circuit low voltage) |
| **Biased high** (constant rich reading) | Voltage stays **above 0.8–0.9 V**, even when lean. ECM drives fuel trims high negative. | P0132 (circuit high voltage) |
| **Dead / open circuit** | Voltage **stays at a fixed level** (e.g., 0 V or a bias voltage) and does not respond to throttle changes. | P0134 (open circuit) |

**Bottom line:** The key differentiator is the **sensor’s dynamic response**:
- **Lazy = slow switching** (P0133)
- **Biased = wrong voltage amplitude** (P0131 / P0132)
- **Dead = no switching** (P0134)

Some systems also report **O₂ sensor cross‑counts**—the number of times per second the signal crosses the stoichiometric pivot. A lazy sensor will show a sharply reduced cross‑count rate. This metric is often used by the ECM itself to set the P0133 DTC.

---

### Summary of Fleet Realities (1990–2010 Petrol)

| Category | Verdict |
| :--- | :--- |
| **Fuel trim ranges** | Normal: ±5 %; Diagnostic attention: > ±8 %; Code setting: often > ±18 %. |
| **±127 PIDs** | Sentinel values; rarely observed in closed loop with a properly functioning sensor. |
| **Commanded λ availability** | Not universal. Supported PIDs vary; use Mode 1 PID 0x00 to detect presence. |
| **VE cross‑check on single‑air‑meter engines** | Possible by inferring the missing air meter; requires a “target VE” for comparison. |
| **Pre‑2001 fuel trim trust** | Data is present but may have lower resolution/update rate. Gross faults are reliably detectable. |
| **Downstream O₂ trim influence** | Present in many systems (e.g., Bosch ME7). Can be used to detect masking of upstream drift. |
| **Sensor fault metrics via scan tool** | Voltage, STFT, freeze frame, and the presence of P0131/P0132/P0133/P0134 are the primary indicators. Cross‑counts (if available) quantify “laziness.” |