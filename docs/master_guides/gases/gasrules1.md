# Master Knowledge Document: Exhaust Gas Dependencies and Rules  
**Based on Crypton Diagnostic Equipment Technical Resources**  
*For 4/5-Gas Exhaust Analysis – Petrol Engines*

---

## 1. Core Combustion Chemistry

Complete (ideal) combustion:
```
Fuel (HC + additives) + Air (N₂ + O₂) → CO₂ + H₂O + N₂
```

Real-world incomplete combustion adds:
- **HC** – unburned fuel  
- **CO** – partially burned fuel  
- **O₂** – leftover oxygen  
- **NOx** – oxides of nitrogen (formed at high temperature > 2500 °F)

The **Stoichiometric ratio** for petrol is **14.71 : 1** (14.71 kg air to 1 kg fuel, or 14.71 litres air per 1 litre fuel). At this point **Lambda = 1.000**.

---

## 2. Exhaust Gas Definitions

| Gas | What It Represents | Unit | Key Behaviour |
|-----|---------------------|------|---------------|
| **HC** | Unburned fuel (raw or partially broken) | ppm | Rises with misfire / incomplete burn |
| **CO** | Partially burned fuel (should have become CO₂) | % | High = rich mixture (lack of O₂ / time) |
| **CO₂** | Completely burned fuel – measure of combustion efficiency | % | Highest at stoichiometric, drops with any combustion problem |
| **O₂** | Free oxygen left after combustion | % | High = lean mixture or misfire; Low = rich mixture |
| **NOx** | Oxides of nitrogen from high combustion temps (5‑gas only) | ppm | Load‑dependent, peak near stoichiometric under load |
| **Lambda** | Air/fuel balance – ratio of actual oxygen to oxygen needed for complete combustion | – | 1.000 = stoichiometric; <1 = rich, >1 = lean |
| **AFR** | Lambda × 14.71 (petrol) | – | Direct expression of air‑to‑fuel ratio |

---

## 3. AFR, Lambda, and Their Relationship

- **Lambda = 1.0** ⇒ AFR = 14.71 : 1 (ideal clean burn)
- **Lambda < 1.0** ⇒ rich mixture (excess fuel, AFR < 14.71)
- **Lambda > 1.0** ⇒ lean mixture (excess air, AFR > 14.71)

**AFR = Lambda × 14.71** (for petrol). The Brettschneider/Spindt equations calculate Lambda from all carbon‑ and oxygen‑bearing gases. Lambda is immune to misfire (it reads the balance, not burn quality), but is **sensitive to air leaks** – a 5 % exhaust air leak will shift Lambda 5 % lean (e.g., true 1.000 becomes 1.050).

> ⚠️ Lambda = 1.0 **does not guarantee** correct combustion. A misfiring engine can still show Lambda = 1.0 if the raw fuel and air balance out. Always interpret Lambda **together with HC, CO₂, O₂, CO**.

### Effect of Sustained AFR Deviation

| Too Lean (AFR ≫ 14.7) | Slightly Lean | Slightly Rich | Too Rich (AFR ≪ 14.7) |
|------------------------|---------------|---------------|-------------------------|
| Poor engine power<br>Misfire at cruise speeds<br>Burned valves<br>Burned pistons<br>Scored cylinders<br>Spark knock/ping | High fuel mileage<br>Low exhaust emissions<br>Reduced engine power<br>Some tendency to knock/ping | Maximum engine power<br>Higher emissions<br>Higher fuel consumption<br>Lower tendency to knock/ping | Poor fuel mileage<br>Misfiring<br>Increased air pollution<br>Oil contamination<br>Black exhaust |

| Stoichiometric AFR 14.71 (Lambda = 1) | Best all‑around engine performance |

---

## 4. Gas Inter‑Dependencies – Quick Diagnostic Tables

These tables list measured gas behaviour and typical causes. Use them together with the general rules in Section 5.

### 4.1 Lambda vs. Gas Pattern

| Lambda Value | CO | CO₂ | HC | O₂ | Condition |
|--------------|----|-----|----|----|-----------|
| **< 1.0** (Low) | High | Low | High | Low | Rich Mixture |
| **> 1.0** (High) | Low | Low | Low | High | Exhaust Leak (air dilution) |
| **> 1.0** (High) | Low | Low | High | High | Lean Mixture |
| **= 1.0** | Low | High | Low | Low | Tuned (ideal) |

### 4.2 General Fault Patterns (from `enginefaults.pdf`)

| CO         | CO₂   | HC          | O₂   | Lambda / AFR | Possible Problems / Causes |
|------------|-------|-------------|------|--------------|----------------------------|
| Low‑Moderate | Low   | Low‑Moderate | Low  | Low (rich)   | **Major Engine Faults:** Low compression, insufficient camshaft lift |
| Low‑Moderate | Low   | Low‑Moderate | Low  | Low (rich)   | **Minor Engine Faults:** Ignition timing over‑advanced, spark plug/wire open/ground, ECM compensating for vacuum leak |
| Low        | High  | Low         | High | High (lean)  | Injector misfire, catalytic converter operating correctly |
| High       | Low   | High        | Low  | Low (rich)   | Thermostat/coolant temp sensor faulty – "cold running engine" |
| Low        | High  | Low         | Low  | High (lean)  | Thermostat/coolant temp sensor faulty – "hot running engine" |
| Low        | Low   | Low         | High | High (lean)  | Exhaust leak **after** catalytic converter |
| High       | High  | High        | High | –             | **Combination:** Rich mixture + vacuum leak, injector misfire, catalytic converter not working |
| Low        | High  | Low         | Low  | ≈1.0         | Good combustion efficiency, catalytic converter working properly |

### 4.3 Lean Mixture Patterns (`leanmixture.pdf`)

| CO  | CO₂ | HC  | O₂  | AFR / Ratio | Possible Problems / Causes |
|-----|-----|-----|-----|-------------|----------------------------|
| Low | Low | High| High| **Too Lean** | Lean fuel mixture, ignition misfire, vacuum leaks (between MAF and throttle body), bad EGR valve/mis‑routed vacuum hoses, incorrect carburetor settings, bad injector(s), O₂ sensor failing, ECM malfunction, float level too low |
| Low | High| Low | Low | ≈1.0        | Good combustion efficiency and catalytic converter working properly |

### 4.4 Rich Mixture Patterns (`richmixture.pdf`)

| CO          | CO₂ | HC          | O₂   | AFR / Ratio | Possible Problems / Causes |
|-------------|-----|-------------|------|-------------|----------------------------|
| High        | Low | Low‑Moderate| Low  | **Too Rich** | Rich fuel mixture, leaking injectors, incorrect carburetor adjustment, power valve leaking, choke closed, float level too high, dirty air filter, faulty EVAP canister purge, PCV system problem, ECM malfunction, crankcase contaminated with raw fuel |
| Mod‑High    | Low | Low‑Moderate| Low  | Too Rich     | **All of the above but with catalytic converter operating correctly** (CO partly oxidised) |
| High        | Low | High        | High | Too Rich     | Rich mixture with ignition misfire |
| Low         | High| Low         | Low  | ≈1.0         | Good combustion efficiency and catalytic converter working properly |

> **Note:** High CO, Low CO₂, **very high HC (>1000 ppm)** **and** **very high O₂ (>5 %)** can indicate **incorrect engine valve timing** – what enters gets out only partially burned.

---

## 5. General Diagnostic Rules of Gas Behaviour

From the Crypton “Understanding Engine Exhaust Emissions”:

1. **CO ↔ O₂ inverse relationship**  
   CO↑ → O₂↓, and O₂↑ → CO↓. CO indicates rich running, O₂ indicates lean running.

2. **HC and O₂ together increase when there is a lean misfire**  
   A lean misfire pushes unburned fuel (HC) and excess oxygen (O₂) into the exhaust.

3. **CO₂ decreases with any combustion inefficiency**  
   Whether rich, lean, or misfire, CO₂ drops from its peak (≈15.5 % max).

4. **Rich mixture without misfire:**  
   HC may stay normal until CO reaches 3–4 %, then raw fuel escape causes HC spike.

5. **Recognise specific combinations:**
   - High HC + Low CO + High O₂ → **Lean/E GR‑dilution misfire**
   - High HC + High CO + High O₂ → **Rich misfire** (fuel but no burn)
   - High HC + Normal/low CO + High O₂ → **Mechanical/ignition misfire** (good mixture, no ignition)
   - Normal‑High HC + Normal‑Low CO + High O₂ → **Marginally lean / false air**

6. **NOx rises when combustion temperature is high** – peak near stoichiometric under load. It is suppressed by rich mixtures (cooling effect) and by EGR (inert gas reduces temperature).

7. **Lambda is insensitive to misfire and catalytic converter**  
   The balance of oxygen to combustibles is preserved, so Lambda stays constant before/after catalyst and during misfire, but **air leaks** falsify Lambda lean.

8. **O₂ is the best post‑catalyst indicator of mixture**  
   Because the catalytic converter masks CO and HC, O₂ remains a reliable lean/rich indicator after the catalyst.

---

## 6. Typical Emission Values (Guide Only)

### 6.1 With and Without Catalytic Converter (Good System)

| Condition        | CO %   | CO₂ %   | HC ppm  | O₂ %   | Lambda   | AFR          |
|------------------|--------|---------|---------|--------|----------|--------------|
| **With Catalyst**   | ≤0.5   | ≥14.5   | ≤50     | ≤0.5   | 0.97‑1.03| 14.3:1‑15.1:1 |
| **Without Catalyst**| ≤1.5   | ≥13     | ≤250    | 0.5‑2  | 0.90‑1.10| 13.2:1‑16.2:1 |

### 6.2 Pre‑Catalyst vs. Post‑Catalyst (Efficient System)

| Location         | CO % | CO₂ % | HC ppm | O₂ % | Lambda | AFR  |
|------------------|------|-------|--------|------|--------|------|
| Before Catalyst  | 0.6  | 14.7  | 100    | 0.7  | 1.0    | 14.7 |
| After Catalyst   | 0.1  | 15.2  | 15     | 0.1  | 1.0    | 14.7 |

---

## 7. Catalytic Converter Impact on Readings

- **Oxidising catalysts** (Pt/Pd) burn HC and CO into H₂O and CO₂ when O₂ is available.  
- **Reducing catalyst** (Rh) splits NOx into N₂ and O₂ when CO is present.  
- A **Three‑Way Catalyst (TWC)** requires a rapidly alternating rich/lean feed gas (closed‑loop control) to work efficiently.

**Key effects on tailpipe analysis:**
- A good catalyst **masks** a mild engine misfire or rich mixture: pre‑cat HC/CO may be high, post‑cat they appear normal, while O₂ drops and CO₂ rises.
- **O₂ post‑cat is still reliable** – a lean mixture will still show elevated O₂, rich mixture low O₂.
- A **restricted converter** causes loss of power, hard starting, and a vacuum gauge will show slow return to idle after throttle snap.
- Contamination (lead, silicone, coolant, excess fuel) destroys catalyst efficiency; always fix the root cause before replacing the converter.

**Pre‑ vs Post‑Catalyst checks:**  
Measure HC, CO, CO₂, O₂ before and after. With a good catalyst, post‑cat readings will show drastic reduction in HC and CO, small increase in CO₂, and O₂ near zero (if mixture is correct). If post‑cat values are close to pre‑cat, the converter is not functioning.

---

## 8. Practical Troubleshooting Approach

1. Record baseline values at **idle** and **fast idle (2500 rpm)**.
2. Determine if the problem is **mixture‑related** (CO/O₂/AFR) or **combustion/misfire** (HC spike, CO₂ drop).
3. Use the tables in Section 4 to narrow the search area.
4. Check for **air leaks** (exhaust or intake) that can falsify Lambda and O₂.
5. Confirm catalyst health with pre/post analysis.
6. Remember that Lambda = 1.0 only confirms air/fuel **balance**, not burn quality. Look at CO₂ (high is good) and HC (low is good) for efficiency.

---

## Appendix: Quick‑Reference Rule Card

- **Highest CO₂ + lowest HC + O₂ ≈ CO (both low) = perfect combustion.**
- **CO↑ → rich; O₂↑ → lean or misfire.**
- **CO normal, O₂ high, HC high → misfire (ignition/mechanical).**
- **CO low, O₂ high, HC high → lean misfire.**
- **CO high, O₂ low, HC low‑moderate → rich, no misfire.**
- **CO high, O₂ high, HC high → rich misfire.**
- **Post‑cat, O₂ is the most truthful mixture indicator.**
- **Air leak = falsely high O₂, falsely lean Lambda.**

*This document consolidates information from Crypton’s emission training resources. Tables preserved from original PDFs.*