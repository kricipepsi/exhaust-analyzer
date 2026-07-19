# Multi-Sensor Fusion for Automotive Diagnostics — Gemini research (converted)

> Converted from the saved Google Gemini page `deltares3/Multi-Sensor Fusion for Automotive Diagnostics - Google Gemini.html`
> via the html-extractor skill (`--panels`). Only the model's rendered report was kept; app chrome, scripts and the
> agent's plan-echo preamble were stripped. KaTeX equations recovered as inline `$...$` / block `$$...$$`.
> This is the research answer to **prompt E** (cross-referencing the 5-gas delta vector against the OBD delta vector).

---

# High-Fidelity Diagnostic Fusion: Cross-Referencing Heterogeneous 5-Gas and OBD-II Delta Vectors for Petrol Passenger Fleets (1990–2010)

## Executive Summary

Fusing 5-gas tailpipe emissions with OBD-II diagnostic streams significantly improves fault classification accuracy compared to single-modality analysis. The highest-leverage method for cross-referencing these heterogeneous streams is a probability-calibrated late-fusion pipeline. This architecture processes raw measurements through post-hoc calibration via Isotonic Regression, mapping them into unified probability spaces, and executes decision-level fusion using the Proportional Conflict Redistribution (PCR5) rule. This approach successfully converts multi-modal contradictions—such as speed-density vacuum leaks where fuel trims remain static while tailpipe oxygen levels spike—from statistical noise into highly informative diagnostic features, delivering robust fault localization under real-world sensor latency and quantization.

## Temporal Alignment of Unequal Streams across Operating-Point Steps

### Finding

Temporal alignment of a slow 5-gas tailpipe analyzer with an OBD-II scan tool requires addressing three distinct physical and electrical phenomena: gas transport delay, sensor response kinetics, and diagnostic bus latency. Gas transport delay represents the physical transit time of the gas sample from the engine cylinder through the exhaust manifold, catalytic converter, and tailpipe to the analyzer's measurement chamber. This transport delay is highly non-linear and varies as an inverse function of the engine's volumetric exhaust flow rate. During low or curb idle (700–900 RPM), the low exhaust velocity and pressure result in long transport delays, often ranging between 2.0 and 2.5 seconds. At elevated operating points (such as the standard 2500 RPM high idle or a 3750 RPM stress idle), the increased volumetric flow reduces this delay to less than 0.8 seconds.

The total transit-to-measurement delay is modeled by separating the dynamics into three distinct lag components:

$$ \Delta t_{total} = \Delta t_1 + \Delta t_2 + \Delta t_3 $$

where $\Delta t_1$ represents the exhaust transport delay from the engine exhaust manifold to the tailpipe exit, $\Delta t_2$ represents the sample transit time through the physical sampling probe and hose (which can be up to 40 feet in length) to the analyzer, and $\Delta t_3$ represents the response time ( $T_{90}$ ) of the NDIR and electrochemical cells. For standard BAR-97 or OIML Class 0 analytical benches, the response time ( $\Delta t_3$ ) typically ranges from 8 to 10 seconds for primary gases ( $CO$, $CO_2$, $HC$, and $O_2$ ) and up to 15 seconds for nitrogen oxides ( $NO_x$ ). Furthermore, the exhaust gas is convoluted by hydrodynamic dispersion and turbulence during transport, causing physical smoothing of the emission signals.

On the OBD-II side, the parameter stream experiences a variable latency dictated by the active communication protocol of the 1990–2010 fleet. This latency is highly dependent on the vehicle's specific physical layer:

| OBD-II Protocol Standard | Physical Layer Configuration | Typical Bus Baud Rate | Typical Round-Trip Latency | Quantization Limit |
|---|---|---|---|---|
| **ISO 9141-2** [cite: 8, 9] | K-Line (Single-wire, pins 7/15) | 10.4 kbps | 300–400 ms | $0.39\%$ per bit for fuel trims |
| **ISO 14230-4 (KWP2000)** [cite: 9, 10] | K-Line (Single-wire, pin 7) | 10.4 kbps | 200–350 ms | $0.39\%$ per bit for fuel trims |
| **SAE J1850 VPW** [cite: 8, 9] | Single-wire Bus (pin 2) | 10.4 kbps | 250–350 ms | $0.39\%$ per bit for fuel trims |
| **SAE J1850 PWM** [cite: 8, 9] | Differential Pair (pins 2/10) | 41.6 kbps | 100–200 ms | $0.39\%$ per bit for fuel trims |
| **ISO 15765-4 (CAN)** [cite: 8, 9] | Differential CAN (pins 6/14) | 250/500 kbps | 20–50 ms | $0.39\%$ per bit for fuel trims |

To align these asynchronous, unequally sampled streams during an operating point transition, the fusion engine must implement a dual-stage alignment strategy. First, high-frequency OBD-II data is low-pass filtered using a sliding-window average and interpolated onto a common 1 Hz grid to match the slow sampling rate of the NDIR bench. Second, a dynamic lag-compensation rule or a non-linear alignment algorithm, such as Dynamic Time Warping (DTW) or EventDTW, is applied to resolve the physical transport and analyzer response lags.

To extract a highly stable, trustworthy delta vector without dynamic warping, the engine must implement a strict "stabilization hold time" at each stationary point. Consistent with EPA and California BAR Two-Speed Idle (TSI) test standards, each operating point must be held for a minimum of 30 seconds. The transition period and the subsequent 15 seconds must be gated out to allow the physical gas column to purge the sampling probe and to let the NDIR bench achieve chemical and thermal equilibrium. The stabilized delta values must be extracted by averaging the data over the final 5 seconds of the 30-second hold window.

### Evidence/sources

The physical dynamics of exhaust transport delay are modeled using smooth transition regression as a continuous function of exhaust flow. Standardized testing procedures and hold times are defined by the Environmental Protection Agency (EPA) Two-Speed Idle test procedures (40 CFR Part 51, Subpart S) and Virginia administrative codes for emissions inspections (9VAC5-91-440). Multi-sensor alignment and low-pass filtering protocols for mobile emissions systems are established by Biewer et al. (2021) in the LolaDrives framework and general Dynamic Time Warping (DTW) literature.

### Confidence

High. The physical transport dynamics, communication protocols, and standardized testing envelopes are well-characterized across regulatory and academic literature.

### Data gaps / domain-transfer caveats

While the theoretical models for K-Line and CAN bus latencies are highly accurate, real-world OBD-II latency can fluctuate unpredictably due to bus load, diagnostic scan tool quality, and the presence of low-cost passive splitters or telematics devices. Additionally, physical exhaust transport delays can vary on vehicles with modified exhaust systems, aftermarket catalytic converters, or significant exhaust system leaks, which can introduce ambient air dilution and distort the expected transit times.

## Normalising Heterogeneous Deltas and Propagating Uncertainty

### Finding

Fusing a tailpipe gas concentration delta (measured in $\%$ volume or parts per million) with an OBD-II fuel trim delta (measured in $\%$ ) requires transforming these inputs into a dimensionless, comparable scale while accounting for their respective noise floors and sensor uncertainties. Unimodal normalization is achieved by z-scoring the observed delta vector against a baseline distribution of known healthy vehicles at the specific operating point transition:

$$ \bar{\Delta}_i = \frac{\Delta_{i, obs} - \mu_{i, healthy}}{\sigma_{i, healthy}} $$

where $\mu_{i, healthy}$ and $\sigma_{i, healthy}$ represent the mean and standard deviation of channel $i$ across a healthy fleet. For emissions parameters, raw concentration deltas are converted into a dimensionless Excess Air Ratio ( $\lambda$ ) using the Brettschneider equation, which balances the carbon, hydrogen, and oxygen components:

$$ \lambda = \frac{[CO_2] + \frac{[CO]}{2} + [O_2] + \left( \frac{H_{cv}}{4} \times \frac{y}{1 + y} \right) [HC]}{[CO_2] + [CO] + [HC] \times \left(1 + \frac{x}{4} - \frac{z}{2}\right)} $$

where $x$, $y$, and $z$ represent the atomic hydrogen-to-carbon, oxygen-to-carbon, and nitrogen-to-carbon ratios of the fuel.

To prevent measurement noise from triggering false fault classifications, each channel's uncertainty must be propagated into its delta value. For a generic operating transition delta ( $\Delta = X_{elevated} - X_{idle}$ ), the propagated standard uncertainty ( $\sigma_{\Delta}$ ) is calculated using the root-sum-square (RSS) of the individual operating point uncertainties:

$$ \sigma_{\Delta} = \sqrt{\sigma^2_{elevated} + \sigma^2_{idle}} $$

For the 5-gas analyzer, the uncertainty at any point is determined by the maximum permissible error (MPE) specified by standards such as OIML R99 Class 0.

| Gas Component | OIML R99 Class 0 Absolute MPE | OIML R99 Class 0 Relative MPE | Typical Noise Floor |
|---|---|---|---|
| **Carbon Monoxide ( $CO$ )** | $\pm 0.03\%$ vol | $\pm 5\%$ | $0.01\%$ vol |
| **Carbon Dioxide ( $CO_2$ )** | $\pm 0.5\%$ vol | $\pm 5\%$ | $0.1\%$ vol |
| **Hydrocarbons ( $HC$ )** | $\pm 10$ ppm vol (as hexane) | $\pm 5\%$ | $1$ ppm vol |
| **Oxygen ( $O_2$ )** | $\pm 0.1\%$ vol | $\pm 5\%$ | $0.02\%$ vol |
| **Nitrogen Oxides ( $NO_x$ )** [cite: 5, 6] | $\pm 25$ ppm vol | $\pm 4\%$ | $1$ ppm vol |

The sensor uncertainty is the maximum of the absolute and relative errors at the measured concentration:

$$ \sigma_{gas} = \max\left(\text{MPE}_{absolute}, \text{MPE}_{relative} \times C_{measured}\right) $$

For the OBD-II scan tool, fuel trim parameters (Short-Term Fuel Trim, STFT; Long-Term Fuel Trim, LTFT) suffer from quantization error due to their 8-bit representation ( $0.39\%$ per bit, ranging from $-100\%$ to $+99.2\%$ ) [cite: Context]. The standard uncertainty introduced by this quantization interval ( $q = 0.3906\%$ ) is modeled as a uniform distribution:

$$ \sigma_{quant} = \frac{q}{\sqrt{12}} \approx 0.113\% $$

Fusing this with a typical sensor noise variance ( $\sigma^2_{noise} \approx 0.25\%^2$ ), the standard uncertainty of a single fuel trim reading is $\sigma_{trim} \approx 0.51\%$. Propagating this to the delta fuel trim yields:

$$ \sigma_{\Delta_{trim}} = \sqrt{\sigma^2_{trim, elevated} + \sigma^2_{trim, idle}} \approx \sqrt{0.51^2 + 0.51^2} \approx 0.72\% $$

### Evidence/sources

OIML R99 / ISO 3930 Class 0 accuracy limits; BAR-97 analyzer calibration standards; measurement uncertainty propagation theory (ISO/IEC Guide 98-3).

### Confidence

High. Quantization math and regulatory gas analyzer tolerances are legally defined and mathematically precise.

### Data gaps / domain-transfer caveats

The uncertainty models assume a fully warmed-up, calibrated gas bench (typically requiring 30 minutes to achieve full performance). Thermal drift during the initial operating phase can exceed these accuracy bands if not compensated.

## Agreement vs Disagreement as the Core Discriminator

### Finding

In automotive diagnostics, the physical relationship between engine control unit (ECU) compensation and tailpipe chemistry dictates that a disagreement between OBD-II indicators and physical emissions is often more informative than perfect correlation. On vehicles using Mass Air Flow (MAF) fuel control, a physical vacuum leak downstream of the sensor introduces unmetered "pirate air". At idle, this unmetered air constitutes a large percentage of total intake air, forcing the ECU to apply high positive short-term and long-term fuel trims (often $+15\%$ to $+25\%$ ) to maintain stoichiometry. At 2500 RPM, the unmetered air becomes a negligible fraction of the high-velocity intake flow, and the fuel trims drop back toward normal (a delta trim reduction of at least $15\%$ ). Under this scenario, the closed-loop fuel system successfully maintains stoichiometry, meaning the tailpipe gas analyzer records a null lambda delta ( $\Delta \lambda \approx 0$, holding near 1.0). This represents corroborative agreement: the active fuel-loop compensation (OBD) successfully hides the lean condition from the exhaust, but the physical drop in trim at high RPM confirms the diagnostic signature.

On Speed-Density (MAP-based) engines, the physical behavior differs fundamentally. A vacuum leak allows air to enter the intake manifold directly, which increases the manifold absolute pressure (MAP). The ECU interprets this pressure increase as an increase in engine load. Under the Speed-Density equation, the calculated intake air mass increases, prompting the ECU to automatically command more fuel based on its base volumetric efficiency (VE) lookup table. Consequently, the OBD-II fuel trims remain near zero ( $\Delta \text{trims} \approx 0$ ), and the engine idle speed rises. However, because the actual physical air mass leak does not perfectly match the raw VE table estimation, or because of incorrect density calculation from combined intake air temperature (IAT) drift, the air-fuel mixture in the cylinder runs physically lean. The tailpipe analyzer immediately registers this as a highly elevated oxygen concentration and a lean lambda delta ( $\Delta \lambda > 1.05$ ). Here, the disagreement (OBD trim delta is zero, while Gas lambda delta is strongly lean) is the primary diagnostic signature that identifies a Speed-Density vacuum leak.

Another example is an ignition misfire. The misfiring cylinder fails to combust the air-fuel mixture, pumping unburned oxygen ( $O_2$ ) and raw hydrocarbons ( $HC$ ) directly into the exhaust tract. The vehicle's onboard oxygen sensor detects this high oxygen level and reports a false lean condition to the ECU, which responds by adding fuel and driving fuel trims highly positive. The tailpipe analyzer, however, records a simultaneous spike in both $O_2$ and $HC$. This chemically conflicting signature (high oxygen combined with high hydrocarbons) is a direct diagnostic of an ignition-induced misfire, distinguishing it from a physical lean fuel supply issue where hydrocarbons would remain low.

To capture these relationships, the fusion engine must utilize Dempster-Shafer (D-S) evidence theory to model conflicts mathematically. Let the frame of discernment be:

$$ \Theta = \{\text{Healthy (H)}, \text{MAF Vacuum Leak (VL\_MAF)}, \text{MAP Vacuum Leak (VL\_MAP)}, \text{Fuel Supply Restriction (F)}\} $$

Unimodal diagnostic classifiers map the normalized OBD delta vector and gas delta vector to basic belief assignments (BBAs or mass functions), denoted as $m_{OBD}$ and $m_{gas}$. When combining these BBAs using Dempster's rule, the conflict mass ( $K$ ) is calculated as:

$$ K = \sum_{B \cap C = \emptyset} m_{OBD}(B) \cdot m_{gas}(C) $$

Under a speed-density vacuum leak, the OBD classifier assigns its mass to $\{\text{Healthy}\}$ or $\{\text{Fuel Supply Restriction}\}$, while the gas classifier assigns its mass to $\{\text{VL\_MAP}\}$ or $\{\text{VL\_MAF}\}$. This results in a high conflict mass ( $K \to 1.0$ ).

Standard Dempster's combination rule normalizes by dividing by $1 - K$, which redistributes the conflict mass evenly and leads to counter-intuitive classifications (Zadeh's Paradox). To resolve this, the engine must bypass standard normalization and employ conflict-aware operators. Under the **Dubois-Prade Rule**, the conflict mass is allocated directly to the union of the conflicting focal elements, preserving diagnostic ambiguity:

$$ m_{DP}(A) = \sum_{B \cap C = A} m_1(B)m_2(C) + \sum_{B \cap C = \emptyset, B \cup C = A} m_1(B)m_2(C) $$

Alternatively, the **Proportional Conflict Redistribution (PCR5)** rule, developed in Dezert-Smarandache Theory (DSmT), redistributes the conflicting mass back to the specific focal elements involved in the conflict, proportional to their original mass assignments:

$$ m_{PCR5}(A) = m_{OBD}(A) \cdot m_{gas}(A) + \sum_{Y \cap A = \emptyset} \left[ \frac{m_{OBD}(A)^2 \cdot m_{gas}(Y)}{m_{OBD}(A) + m_{gas}(Y)} + \frac{m_{gas}(A)^2 \cdot m_{OBD}(Y)}{m_{gas}(A) + m_{OBD}(Y)} \right] $$

This mathematical formulation ensures that a high conflict mass does not degrade the diagnostic output but instead acts as the primary feature triggering the correct Speed-Density or MAP calibration fault hypothesis.

### Evidence/sources

MAF/MAP system behaviors and diagnostic strategies are documented in trade journals and diagnostic forums. Mathematical formulations for conflict management under Dempster-Shafer theory are derived from Milan Daniel (2011) and Dezert-Smarandache proportional conflict redistribution rules.

### Confidence

High. The physical engine mechanics of MAP vs. MAF control loops are well-established, and the mathematical properties of PCR5/Dubois-Prade are rigorously proven in information fusion theory.

### Data gaps / domain-transfer caveats

Most advanced evidence-fusion algorithms (such as PCR5 and Dubois-Prade) were originally developed for aerospace and military targeting or industrial bearing fault monitoring. Adapting them to automotive emissions diagnostics requires careful tuning of the basic belief assignments to match the specific physical limits of engine-out emissions and fuel-loop adaptation boundaries.

## Fusion Architecture and Calibrated Joint Confidence

### Finding

The optimal architecture for combining the gas-delta and OBD-delta vectors is an uncertainty-aware late-fusion pipeline that applies post-hoc calibration to individual modal classifications before performing decision-level evidential combination.

Unimodal classification models (such as Support Vector Machines, Decision Trees, or Neural Networks) generate raw decision scores that are not naturally comparable across different sensor modalities due to differences in noise floors and feature scales. To resolve this, raw scores must be calibrated post-hoc into empirical probabilities. **Isotonic Regression** is selected for this task as it does not assume a specific distribution shape (unlike Platt Scaling) and is robust in mapping monotonic relationships. Isotonic calibration optimizes the weighted least-squares fit:

$$ \min \sum_{i} (y_i - \hat{p}_i)^2 \quad \text{subject to} \quad \hat{p}_i \ge \hat{p}_j \text{ for } s_i \ge s_j $$

where $s_i$ is the raw classifier output, $y_i$ is the empirical ground-truth class, and $\hat{p}_i$ is the calibrated probability. On test datasets, Isotonic Regression has been shown to reduce Expected Calibration Error (ECE) from 0.260 to 0.006, ensuring that the confidence scores output by each modal classifier accurately represent their true accuracy.

The calibrated probabilities ( $P_{cal}$ ) are mapped to basic belief assignments:

$$ m(F_k) = P_{cal}(F_k) \cdot (1 - \sigma_{\Delta}) $$

$$ m(\Theta) = 1 - \sum_{k} m(F_k) $$

where $\sigma_{\Delta}$ represents the propagated measurement uncertainty calculated in Section 2, which dynamically discounts the mass assigned to specific faults and transfers the remaining belief to the state of total ignorance ( $m(\Theta)$ ), representing epistemic uncertainty.

To handle sensor degradation or communication failures, the architecture implements rigid validity gates:

1. **OBD Validity Gate**: Evaluates packet loss and sample rate. If the OBD stream falls below a 1 Hz sample rate or suffers from a connection drop, the scan tool modality is marked as abstained.
2. **Gas Bench Validity Gate**: Monitors the sample flow rate and condensation traps. If the pressure transducer detects a restricted sample line or an uncompensated temperature drift, the gas modality is marked as abstained.

When a modality is gated out or abstains, the engine automatically assigns its BBA to the vacuous belief state:

$$ m_{abstain}(\Theta) = 1.0, \quad m_{abstain}(F_k) = 0 \quad (\forall k) $$

Under the PCR5 or conjunctive combination rules, a vacuous BBA acts as the identity element:

$$ m_{fused} = m_{valid} \oplus m_{abstain} = m_{valid} $$

This ensures the diagnostic engine collapses gracefully to the remaining active modality without destabilizing the downstream decision logic. The final ranked fault hypothesis is derived by converting the fused mass function ( $m_{fused}$ ) into pignistic probabilities:

$$ BetP(F) = \sum_{Y \subseteq \Theta, Y \neq \emptyset} \frac{|F \cap Y|}{|Y|} \frac{m_{fused}(Y)}{1 - m_{fused}(\emptyset)} $$

This step projects the multi-modal interval estimates $[Belief, Plausibility]$ back into a calibrated, single-point probability distribution for the end-user.

### Evidence/sources

Late-fusion calibration and uncertainty frameworks are detailed in JTIE Stekom (2024). The mathematical formulations for pignistic transformations are derived from general Dempster-Shafer decision rules, and post-hoc calibration studies are sourced from Platt Scaling and Isotonic Regression comparisons.

### Confidence

High. Late-fusion structures with validation gates are standard in safety-critical ADAS and aerospace perception stacks.

### Data gaps / domain-transfer caveats

The late-fusion paradigm assumes the errors between the two classifiers are conditionally independent. If a common failure (such as an alternator drop or system ground noise) affects both sensors, this assumption breaks down.

## Paired Gas + OBD Multi-Point Ground Truth and Validation

### Finding

No comprehensive, publicly accessible research or commercial dataset exists that pairs high-resolution, multi-point 5-gas NDIR analyzer data with sub-second OBD-II generic PID streams for passenger vehicles with confirmed, physically injected faults. Existing datasets in this domain suffer from significant limitations and mismatches:

- **Barreto Datasets (dailyRoutes / 19drivers)**: Provide decoded OBD-II streams (such as fuel trims, MAP, RPM, and speed) across fixed routes, but contain **no physical tailpipe gas analyzer measurements** and focus exclusively on driving style and driver authentication.
- **LolaDrives PEMS Dataset (Biewer et al., 2021)**: Pairs OBD-II diagnostic data with real-world mobile emissions measurements, but is limited to uncalibrated, low-accuracy indicative measurements (with $\pm 15\%$ error for $NO_x$ ) and lacks stationary, multi-point operating transitions under confirmed physical fault states.
- **JRC OBFCM Telemetry Dataset**: Focuses on long-term on-board fuel and energy monitoring data for modern plug-in hybrids and diesel fleets, but lacks raw 5-gas concentration measurements and is restricted to vehicles manufactured after 2018 (out of scope for the target 1990–2010 fleet).
- **Vermont HEV Dataset (Holmen & Robinson, 2020)**: Integrates 1 Hz tailpipe emissions and vehicle power metrics, but is highly specific to hybrid-electric vehicles (2010 Toyota Camry Hybrid) and hilly real-world driving profiles, rather than stationary multi-point diagnostics of conventional petrol platforms.

### Dataset Access Terms

| Dataset Name | Primary Data Modalities | Access Terms / Link | Mismatch / Target Fleet Gap |
|---|---|---|---|
| **Barreto OBD-II** | Decoded OBD PIDs (0.14 Hz) | Open Source / Kagle Barreto | Lacks emissions data entirely. |
| **LolaDrives PEMS** | OBD-II + 1 Hz Mobile Emissions | Open Access / LolaDrives Project | Uncalibrated, lacks stationary multi-point transitions under physical fault conditions. |
| **JRC OBFCM Telemetry** [cite: 54] | OBFCM Fuel, $CO_2$, Energy | Open Access / JRC Publications [cite: 54] | Target fleet mismatch: post-2018 hybrid/diesel passenger vehicles. |
| **Vermont HEV** [cite: 55] | Tailpipe Emissions + Hybrid Power | Open Access / Dryad Repository [cite: 55] | Target fleet mismatch: hybrid propulsion focus, transient road loops. |

### Alternative Validation Strategy

Given the lack of unified multi-modal ground-truth datasets, validation of the cross-referenced delta model must be performed using an alternative three-part engineering protocol:

1. **Synthetic Delta Generation via High-Fidelity Physics Models**: The engine-out and tailpipe emissions must be simulated using physics-based engine models (such as GT-POWER or the EPA's ALPHA simulation framework). The model must represent standard 1990–2010 engine configurations (e.g., a 2.0L naturally aspirated inline-four with standard port fuel injection and a three-way catalytic converter). Vacuum leaks and fuel restrictions can be simulated by modifying the model's manifold leakage parameters or fuel rail pressure constants, generating synthetic 5-gas and OBD-II delta vectors across transitions.
2. **Expert-Elicited Evidential Priors**: Initial BBAs must be populated using diagnostic matrices verified by automotive master technicians. This step establishes a solid baseline for the relationship between physical faults and diagnostic signatures.
3. **Leave-One-Fault-Out Cross-Validation (LOFO-CV)**: During model evaluation, the fusion engine is trained on a subset of simulated and bench-tested fault vectors, leaving one specific physical fault out of the training loop. The engine's performance is then validated on this unseen fault class to ensure that the PCR5 fusion rule generalizes to novel diagnostic patterns and doesn't overfit to specific sensor configurations.

### Evidence/sources

Engine modeling and benchmarking frameworks are derived from EPA National Vehicle Fuel and Emissions Laboratory studies. Validation strategies for late-fusion systems are sourced from equivalent academic applications.

### Confidence

High. The absence of public paired datasets is a known barrier in automotive diagnostic research, and the synthetic modeling/expert-priors validation strategy is standard across equivalent academic and industrial applications.

### Data gaps / domain-transfer caveats

Physical anomalies such as ambient wind gusts or tailpipe exhaust leaks are poorly captured by synthetic 1-D models, requiring noise-injection protocols during validation.

## Cross-reference Logic Table

The following table details the cross-referencing diagnostic rules for identifying common faults using the OBD-II delta vector ( $\Delta_{OBD} = X_{2500} - X_{idle}$ ) and the tailpipe gas delta vector ( $\Delta_{Gas} = X_{2500} - X_{idle}$ ) on 1990–2010 petrol vehicles.

| gas-delta pattern | OBD-delta pattern | agreement/contradiction | diagnostic interpretation | confidence effect | source |
|---|---|---|---|---|---|
| $\Delta O_2 \approx 0$ $\Delta \lambda \approx 0$ (held at 1.0) | $\Delta \text{LTFT} \le -15\%$ $\Delta \text{STFT} \approx 0$ | **Corroborative Agreement**: Closed-loop fuel control successfully compensates for unmetered air at idle. | **MAF Vacuum Leak**: Air leak is a large fraction of total intake at idle, but becomes negligible at 2500 RPM. | **Very High**: Both subsystems show a consistent transition from highly abnormal idle control to normal high-idle operation. | [cite: 32, 33, 34] |
| $\Delta O_2 \le -1.5\%$ vol $\Delta \lambda \le -0.05$ (lean to rich) | $\Delta \text{LTFT} \approx 0$ $\Delta \text{STFT} \approx 0$ | **Strong Contradiction**: Gas analyzer shows a rich shift, while fuel trims remain static. | **EGR Leak or Stuck Open (Speed-Density)**: Inert gas dilution increases MAP, prompting automatic fuel enrichment that is uncompensated by trims at idle. | **High**: The conflict mass PCR5 redistribution rules out MAF-type leaks and isolates MAP/EGR faults. | [cite: 32, 35] |
| $\Delta O_2 \ge +1.5\%$ vol $\Delta \lambda \ge +0.06$ (lean delta) | $\Delta \text{LTFT} \approx 0$ $\Delta \text{STFT} \approx 0$ | **Strong Contradiction**: Gas analyzer registers a lean mixture, while fuel trims remain static. | **Speed-Density (MAP) Vacuum Leak**: Manifold pressure rises due to leak, increasing commanded fuel, but physical air leak causes actual lean burn. | **High**: Confirms MAP-based architecture or MAP calibration drift; rules out closed-loop MAF tracking. | [cite: 32, 34, 35] |
| $\Delta O_2 \ge +2.0\%$ vol $\Delta HC \ge +200$ ppm | $\Delta \text{STFT} \ge +15\%$ [cite: 32, 33] | **Corroborative Agreement**: Both streams show a severe lean condition and compensation limits. | **Fuel Supply Restriction**: Low fuel pressure or restricted injectors prevent adequate fueling at high load/RPM. | **Very High**: Trims peg positive while tailpipe oxygen and HC spike due to lean misfires. | [cite: 32, 33, 35] |
| $\Delta HC \ge +150$ ppm $\Delta O_2 \ge +1.0\%$ vol | $\Delta \text{STFT} \ge +10\%$ | **Apparent Contradiction**: Oxygen and hydrocarbons rise simultaneously, which is chemically conflicting under normal combustion. | **Ignition Misfire (False Lean)**: Unburned oxygen and raw fuel are pumped directly into the exhaust; trims add fuel in response to detected $O_2$. | **High**: Isolates ignition/coil faults from physical lean fuel system delivery issues. | [cite: 32, 33] |
| $\Delta CO \ge +2.0\%$ vol $\Delta HC \ge +100$ ppm | $\Delta \text{MAP} \ge +25$ kPa | **Corroborative Agreement**: High backpressure reduces volumetric efficiency, causing a rich shift and a drop in manifold vacuum. | **Exhaust Restriction (Clogged Catalyst)**: Restricted flow limits gas scavenging; MAP increases due to backpressure. | **High**: Rules out sensor calibration drift and isolates downstream physical blockages. | [cite: 23, 24, 32] |

## Fusion-method Table

The following table compares different information-fusion methods for combining the heterogeneous gas and OBD-II delta vectors into a unified diagnostic output.

| method | what it buys | cost / when it fails | evidence it beats single-modality on a comparable task | maturity |
|---|---|---|---|---|
| **RSS-Weighted Voting** [cite: 25, 58] | Simple to implement; computationally lightweight; directly accounts for known sensor accuracy bands. | Fails to capture non-linear, multi-modal contradictions; does not resolve structural architectural changes (MAP vs. MAF). | Outperforms single-modality by reducing false alarms from noisy individual sensors under steady-state conditions. | Low (primarily a basic filtering step) |
| **Bayesian Update** [cite: 36, 51] | Rigorously updates fault probabilities sequentially; works well under known, stable prior distributions. | Requires precise, hard-to-obtain prior probabilities; struggles with extreme, out-of-distribution conflicts. | Improves classification accuracy under standard sensor noise compared to using OBD-II data alone. | Medium-High (well-established theoretically) |
| **DS Conflict-Aware** [cite: 36, 38, 59] | Explicitly models uncertainty ( $m(\Theta)$ ) and ignorance without requiring prior probabilities. | Normalization constant ( $1/(1-K)$ ) leads to counter-intuitive results (Zadeh's Paradox) under severe conflicts. | Provides higher diagnostic accuracy than single-source classifiers when input streams are highly certain. | Medium (limited by normalization failures) |
| **PCR5 (DSmT)** [cite: 40, 44] | Directly converts conflicts into informative diagnostic features by redistributing conflict mass proportionally. | High computational complexity; requires calibrating complex mass assignment functions. | Delivers up to $20\%$ higher accuracy than classical fusion under high-noise, highly conflicting scenarios. | High (standard in advanced multi-sensor stacks) |
| **Stacking-Logistic (Learned)** [cite: 48, 60] | Automatically learns non-linear interactions and structural exceptions (like Speed-Density variations). | Highly dependent on large, balanced training datasets; vulnerable to overfitting on synthetic data. | Achieves a $15\text{--}25\%$ improvement in classification accuracy over heuristic rule-based frameworks. | Medium-High (widely used in modern machine learning) |

## Consolidated Source Table

| source | type | year | domain | claim supported | access | link |
|---|---|---|---|---|---|---|
|  | peer-reviewed | 2021 | automotive | LolaDrives architecture, uncalibrated OBD/PEMS comparisons, 1 Hz sampling. | free | LolaDrives PEMS |
|  | peer-reviewed | 2010 | automotive | Volumetric-dependent exhaust gas transport delay, dynamic mixing, STR models. | paid | ACS Publications |
|  | standard | 1998 | industrial | Requirements for labels, condensation traps, filters, and gas display resolutions. | free | BSMI Specification |
|  | standard | 2017 | automotive | BAR-97 technical specifications, integration of OBD-II interfaces and gas benches. | free | CA Bureau of Automotive Repair |
|  | standard | 2026 | automotive | OBD-II physical protocol pinouts, communication speeds, initialization, and limits. | free | OBD Tester Guide |
|  | standard | 1998 | industrial | OIML R99 Class 0 absolute and relative accuracy tolerances for 5-gas analyzers. | free | OIML R99 Standard |
|  | industry | 2013 | automotive | Diagnostic logic for MAF vacuum leaks at 2500 RPM vs. idle operating points. | free | Motor Magazine |
|  | anecdotal | 2014 | automotive | Physical behavior of vacuum leaks and MAP sensor drift on Speed-Density vehicles. | free | Reddit Cartalk Archive |
|  | standard | 1993 | automotive | EPA Two-Speed Idle test parameters, mode lengths (30s minimum), and preconditioning rules. | free | EPA Nepis |
|  | standard | 2012 | automotive | Virginia 9VAC5-91-440 two-speed idle test protocol, stabilization, and averaging. | free | Virginia Legislative Information |
|  | dataset | 2024 | automotive | Barreto OBD-II 19drivers and dailyRoutes dataset, parameters, sampling frequencies. | free | Arxiv / Barreto GitHub |
|  | peer-reviewed | 2024 | general fusion | Late-fusion calibration using Isotonic Regression, ECE metrics, and D-S decision logic. | free | JTIE Stekom |
|  | peer-reviewed | 2006 | general fusion | Mathematical definition of Proportional Conflict Redistribution rules (PCR5). | free | UNM Proportional Conflict |

## "Could not be found" list

The following specific parameters and data elements could not be verified in public databases or academic literature:

- **Empirical Fuel Trim Drift Curves for Pre-CAN K-Line Protocols**: Longitudinal datasets quantifying the correlation between physical wire degradation and generic PID response latencies under ISO 9141-2 and KWP2000 are absent from literature.
- **Volumetric Flow Profiles mapped to Dynamic Transport Delay under Blocked Exhaust Conditions**: No validated engineering models exist that map physical exhaust gas transport delay as a direct function of catalytic converter restriction or localized muffler blockages.
- **Unified Multi-Modal Benchmark Datasets**: No publicly available database contains paired 1 Hz 5-gas analyzer outputs (specifically including $NO_x$ and electrochemical $O_2$ cells) and generic OBD-II sub-second PID values on conventional 1990–2010 petrol vehicles under physically simulated faults.

The single highest-leverage method for cross-referencing heterogeneous 5-gas and OBD-II delta vectors is **Proportional Conflict Redistribution (PCR5)** applied to **Isotonic-calibrated decision probabilities**, as it mathematically converts diagnostic contradictions into highly descriptive features that isolate complex architectural and sensor-drift faults.
