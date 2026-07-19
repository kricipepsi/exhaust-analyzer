Advanced Diagnostic Synthesis: Truth vs. Perception Logic in the 5-Tier 4D Engine Architecture
The evolution of automotive engine management systems between 1990 and 2020 represents a shift from rudimentary mechanical feedback loops to sophisticated, multi-layered electronic control strategies. At the heart of this evolution is the tension between the physical reality of the combustion process and the electronic perception of that process by the Engine Control Unit (ECU). The 4D Diagnostic Engine Architecture provides a structured framework to navigate this tension, utilizing a five-tier hierarchy to differentiate between what an engine is actually doing and what its sensors are reporting. This report provides an exhaustive analysis of the contradictions inherent in modern petrol engine diagnostics, proposing 30 new real-world cases and systematic table enhancements to test the "Truth vs. Perception" logic across the L1 through L5 tiers..1
The Multi-Tier Diagnostic Paradigm
The 4D Diagnostic Engine is predicated on the understanding that sensor data is not an objective truth but a mediated perception. Layer 1 (L1) represents the raw observational data—Parameter Identification (PID) values such as Mass Air Flow (MAF), Intake Manifold Absolute Pressure (MAP), and Oxygen () sensor voltages..4 These values are the primary inputs used by the ECU to calculate the required fuel mass and ignition timing. However, L1 data is inherently susceptible to sensor bias, electrical noise, and environmental interference..3
Layer 2 (L2) moves into the realm of calculated variables, where the ECU applies internal models to the L1 inputs. This includes the determination of Short-Term Fuel Trim (STFT) and Long-Term Fuel Trim (LTFT), as well as the calculation of engine load and volumetric efficiency..6 Simultaneously, a 5-gas analyzer provides a parallel set of L2 data from the tailpipe— and —which are then processed through the Brettschneider lambda formula to determine the physical air-fuel ratio..8
Layer 3 (L3) is the critical junction of the architecture: the Correlation and Discrepancy Matrix. It is at this level that the "Truth vs. Perception" logic is formally tested. By comparing the ECU’s perceived lambda () against the Brettschneider-calculated lambda (), the diagnostic engine can identify "liar" scenarios..1 A significant discrepancy, measured as , indicates that the ECU’s internal model is no longer representative of the physical reality within the combustion chamber..1
Layer 4 (L4) provides the Diagnostic Strategy and Pattern Matching required to isolate the cause of these discrepancies. It utilizes Temporal Causal Graphs (TCG) to map how deviations in one parameter (e.g., a drop in intake vacuum) lead to changes in others (e.g., rising  and )..2 This tier distinguishes between mechanical failures, such as a vacuum leak or a burnt valve, and electronic hallucinations, such as a ghost misfire caused by alternator ripple..1
Finally, Layer 5 (L5) represents the Decision Fusion and Prognostic tier. It synthesizes the findings from the lower tiers into a comprehensive engine health score, weighing the confidence of each diagnostic pattern against the historical reliability of the sensors involved..2 This tier is responsible for determining whether a vehicle should be flagged for immediate repair or if the perceived fault is a low-confidence anomaly that can be monitored over time..14
Physics of the Brettschneider Reality
The Brettschneider formula serves as the ultimate arbiter of truth in the diagnostic process because it is based on the conservation of mass. Unlike an  sensor, which only measures the concentration of oxygen ions in the exhaust stream, the Brettschneider calculation considers the presence of all carbon-bearing and oxygen-bearing molecules..9 This is essential for identifying conditions where the  sensor is "blind" or "fooled.".17 For instance, in an engine with high pumping losses or poor scavenging, the  sensor might report a lean condition due to excess oxygen that passed through the cylinder without participating in combustion. However, if the fuel was still injected, the tailpipe will contain high levels of  and . The Brettschneider equation accounts for these components, yielding a  value that reveals the engine is actually running rich..12
The standard stoichiometric ratio for gasoline is , which corresponds to ..12 A  value less than 1.0 indicates a rich mixture (excess fuel), while a value greater than 1.0 indicates a lean mixture (excess air)..8 The relationship between gas concentrations and lambda is non-linear and highly sensitive to the presence of unburned fuel. The following table illustrates the typical 5-gas signatures that the 4D engine uses to define physical reality..12
Typical 5-Gas Diagnostic Signatures
Diagnostic State
CO (%)
CO2​ (%)
HC (ppm)
O2​ (%)
λ (Calc)
Stoichiometric (Pass)
0.1 - 0.45
14.5 - 16.0
0 - 35
0.0 - 0.35
0.995 - 1.005
Healthy (Pre-Catalyst)
0.5 - 0.9
13.5 - 14.5
75 - 125
0.3 - 0.7
0.995 - 1.005
Rich Mixture
> 1.0
< 12.5
100 - 500
< 0.2
< 0.950
Lean Mixture
< 0.2
< 12.5
50 - 200
> 1.5
> 1.050
Ignition Misfire
Variable
< 10.0
> 2000
> 4.0
> 1.200
Lean Misfire
< 0.1
< 10.0
500 - 1500
> 5.0
> 1.300

Analysis of the Truth vs. Perception Gap
Discrepancies between ECU perception and tailpipe truth are often the result of "unmetered" events. A vacuum leak is unmetered air entering after the MAF sensor; a leaking fuel pressure regulator is unmetered fuel entering via the vacuum line..21 In both cases, the ECU’s L1 perception of the air-fuel mass is incorrect, forcing the L2 trims to move toward extreme values as the  sensor attempts to pull the system back to stoichiometry..6
However, the most insidious contradictions occur when the feedback sensor itself—the  sensor—is biased. A "lazy"  sensor might switch too slowly, causing the ECU to oscillate the trims in a wide, unstable pattern that the tailpipe gas analyzer sees as a clean average burn..1 Conversely, a sensor contaminated by silicone or coolant might report a constant lean voltage (), causing the ECU to add fuel indefinitely (positive trim maxed out)..17 In this "Liar" scenario, the ECU perceives a lean condition that it is "fixing," while the Truth is a high- rich condition that may eventually melt the catalytic converter..10
The 4D architecture identifies these states by calculating the Lambda_Delta (). In a healthy system, the delta is near zero. In a "Liar" scenario, the delta spikes. For example, in ECU-001 (from the 'cases_petrol_master.csv'), the ECU perceives a lean condition () and sets a P0171 code, but the tailpipe reality is physically rich ()..1 This represents a  of , which is a severe logic inversion that triggers an L5 ECU Health penalty..1
Proposed New Case Studies (1990-2020)
To fully stress-test the 4D architecture, 30 new cases are proposed below. These cases are structured to span three decades of engine technology and to focus on the specific contradictions between L1-L2 perception and L2-L3 truth..1
Case Group 1: Early OBD-II and Vacuum Dynamics (1996-2004)
These cases focus on the era of narrow-band oxygen sensors and the transition from speed-density (MAP) to mass airflow (MAF) systems. The primary contradictions here involve mechanical air ingress and early sensor degradation..13
Case N-001: The Perforated Brake Booster
In a 1999 sedan, a small internal leak in the brake booster diaphragm introduces unmetered air only when the brake pedal is depressed.
Perception: L1 MAP sensor shows a slight drop in vacuum; L2 STFT spikes to +18% during braking events. The ECU perceives an intermittent lean condition.
Truth: Gas analyzer shows  at 3.0% and  at 1.14.
Contradiction: The fault is transient and RPM-independent, baffling the L4 logic until the "Brake Switch" PID is correlated with the trim spike..21
Case N-002: Silicone-Poisoned Upstream O2 A 2002 truck has its upstream  sensor contaminated by improper RTV sealant used during a valve cover repair..24
Perception: L1  voltage is stuck at 0.15V. L2 LTFT maxes out at +25%. ECU throws a P0171 (System Too Lean).
Truth: Tailpipe  is at 5.5% and  is at 450 ppm.  is 0.84.
Contradiction: The ECU is certain it is lean, but the gas analyzer proves a massive rich state. This is a classic "Liar" scenario..10
Case N-003: Clogged Fuel Pressure Regulator Return On a 1997 fuel-injected engine, the return line to the fuel tank is restricted, causing rail pressure to spike to 80 psi (spec is 45 psi)..7
Perception: L1  sensor sees rich. L2 trims move to -25%. ECU throws P0172 (System Too Rich).
Truth:  is at 8.0%.  is 0.75.
Contradiction: While both perception and truth agree on "Rich," the L3 discrepancy arises because the ECU cannot pull enough fuel to reach stoichiometry, revealing a mechanical source beyond injector pulse-width control..11
Case N-004: Exhaust Manifold Venturi Leak A 2001 SUV has a crack in the exhaust manifold pre-cat..29
Perception: Exhaust pulses suck fresh air into the manifold. L1  sensor sees high oxygen and reports "Lean." L2 trims add 20% fuel.
Truth: Tailpipe  is high (2.5%) because the engine is actually running rich to satisfy the "fooled" sensor.
Contradiction: High  and high  exist simultaneously in the tailpipe—a physical impossibility for a healthy engine..12
Case N-005: Intermittent Ground Ripple on O2 Circuit A 2003 compact car has a frayed engine ground, causing alternator noise to "ghost" onto the  signal wire..1
Perception: ECU sees a rapid, high-frequency "switching" signal that mimics a healthy sensor. L2 trims stay at 0%.
Truth: Gas analyzer shows the engine is actually drifting lean () because the real  signal is buried in noise.
Contradiction: L1 perception says "Healthy," but L2 gas truth says "Lean.".1
Case Group 1 Table: 1996-2004 Fault Projections
Case ID
Year
Fault Description
λOBD​
λcalc​
Δλ
DTC
Logic Tier
N-001
1999
Brake Booster Leak
1.10
1.14
0.04
P0171
L4 Transient
N-002
2002
Silicone Poison O2
1.05
0.84
0.21
P0171
L3 Liar
N-003
1997
Fuel Reg. Return Block
0.85
0.75
0.10
P0172
L4 Mech Fuel
N-004
2001
Pre-Cat Exh Leak
1.12
0.92
0.20
P0171
L3 Inversion
N-005
2003
Ground Ripple Noise
1.00
1.08
0.08
None
L3 Blindness
N-006
1996
MAP Sensor Drift
0.95
1.02
0.07
None
L2 Calculated

Case Group 2: Advanced OBD-II and VVT Integration (2005-2012)
This era introduced Variable Valve Timing (VVT) and more complex catalytic converter monitoring. The cases here explore how timing phasers and catalyst masking affect the truth..31
Case N-007: VVT Phaser Sludge Lag A 2008 luxury sedan has oil sludge restricting the flow to the intake cam phaser..32
Perception: The ECU commands 20 degrees of advance, but the L1 Cam Position Sensor (CPS) reports only 5 degrees. ECU throws a P0011 (Cam Timing Over-Advanced/Performance)..33
Truth: At idle, the gas analyzer shows high  (400 ppm) due to excessive valve overlap and poor scavenging.
Contradiction: The ECU perceives a timing error, but the L4 tier must distinguish if the resulting high  is due to a misfire or a timing-induced volumetric efficiency drop..19
Case N-008: Catalyst Masking of Oil Burning A 2011 SUV with high mileage is consuming 1 quart of oil every 500 miles due to worn piston rings..12
Perception: The modern 3-way catalyst is highly efficient. L1 post-cat  sensor shows a steady 0.65V. ECU perceives a healthy catalyst.
Truth: A pre-cat gas sample would show  ppm. The catalyst is burning off the oil, masking the engine's mechanical decline.
Contradiction: The "Perception" of a healthy engine is only maintained because the "Truth" is being altered by the exhaust aftertreatment system. L5 tier identifies this via rising  breakthrough under load..9
Case N-009: MAF Scaling Decay (Under-reporting) A 2006 hatchback has a fine layer of dust on the MAF hot-wire..5
Perception: At 2500 RPM, L1 MAF reports 8.0 g/s (should be 10.5 g/s). L2 trims move to +16%. ECU perceives a lean condition.
Truth: The engine is physically lean ().
Contradiction: The L1 sensor is lying about the air mass. The 4D engine validates this by comparing the MAF value against a calculated Volumetric Efficiency (VE) model..36
Case N-010: Stuck-Open EVAP Purge Valve On a 2009 sedan, the purge valve sticks open, allowing a constant stream of fuel vapor into the intake..38
Perception: After refueling, the engine idles roughly. L2 STFT drops to -15%. ECU throws P0441 (Incorrect Purge Flow).
Truth: Tailpipe  spikes to 2.0% during the purge event.
Contradiction: The ECU perceives an EVAP fault, but the L3 tier sees a "Rich Liar" scenario if the trims cannot stabilize the mixture during the unmetered vapor event..39
Case N-011: PCV Air-Gap Contamination A 2010 crossover has a cracked PCV hose that is intermittently sealing..22
Perception: L1  sensor voltage oscillates wildly. L2 STFT swings from -10% to +10%. ECU throws no codes but engine hunts at idle.
Truth: Gas analyzer shows erratic  and  spikes that match the idle hunting.
Contradiction: L4 logic identifies this as a "Stability Discrepancy" where perception cannot keep pace with a fluctuating mechanical truth..2
Case N-012: High-RPM Restricted Exhaust A 2005 sports car has a collapsed internal baffle in the muffler..44
Perception: At idle, vacuum is 18 inHg (Normal). Under load, engine lacks power. No DTCs..13
Truth: Backpressure at 2500 RPM is 5.0 psi (spec ).  drops to 9.0%..46
Contradiction: ECU perception is "All Systems Normal" based on L1 PIDs, but L2 gas efficiency truth proves the engine is choking..19
Case Group 2 Table: 2005-2012 Fault Projections
Case ID
Year
Fault Description
O2​ (%)
CO (%)
HC (ppm)
CO2​ (%)
Logic Tier
N-007
2008
VVT Phaser Lag
0.45
0.80
400
13.5
L4 Timing
N-008
2011
Cat-Masked Oil Burn
0.10
0.20
25
15.5
L5 Masking
N-009
2006
MAF Dust Under-rep
2.50
0.05
45
12.0
L3 Discrepancy
N-010
2009
Stuck Purge Valve
0.20
2.00
250
13.0
L4 EVAP Path
N-011
2010
Intermittent PCV Leak
1.50
0.15
180
13.5
L4 Stability
N-012
2005
Restricted Muffler
0.80
1.10
150
9.0
L2 Efficiency

Case Group 3: GDI Dominance and High-Pressure Anomalies (2013-2020)
The final era is defined by Gasoline Direct Injection (GDI) and wideband (Air-Fuel) sensors. The contradictions here are more technical, involving internal pump leaks and carbon-driven pre-ignition..25
Case N-013: GDI HPFP Internal Seal Failure A 2015 luxury SUV has a high-pressure fuel pump leaking fuel into the engine oil..25
Perception: Engine oil level is rising. L2 trims are at -30%. ECU throws a P0172 (System Too Rich).
Truth: Tailpipe  is high (4.0%).  is 0.88.
Contradiction: The ECU is pulling fuel from the injectors, but the mixture remains rich because the "Truth" is that the fuel is entering via the crankcase vapors (PCV)..25
Case N-014: GDI Intake Valve Carbon Sequestration A 2017 turbo-GDI engine has massive carbon buildup on the back of the intake valves..3
Perception: L1 MAP sensor shows high load at idle. L2 trims are slightly lean (+8%). ECU perceives a minor intake restriction.
Truth: The carbon acts as a sponge, soaking up fuel during cold starts and releasing it as the engine warms.  spikes to 800 ppm during warm-up.
Contradiction: L4 logic identifies a "Thermal Inversion" where the mixture is lean when cold and rich when hot—opposite of normal enrichment strategies..43
Case N-015: Wideband O2 Current-Source Drift A 2019 sedan uses a wideband sensor where the reference current circuit in the ECU has drifted..16
Perception: ECU sees . Trims are at 0%.
Truth: The engine is physically running at  (Lean).
Contradiction: The "Truth vs. Perception" gap is invisible to the ECU because the feedback loop is internally consistent but externally wrong. L5 Confidence score drops because  is abnormally high ( ppm)..1
Case N-016: Ghost Misfire from Loose Flywheel On a 2014 manual transmission car, the dual-mass flywheel has internal play..1
Perception: The crankshaft position sensor sees tiny speed variations. ECU throws a P0300 (Random Misfire) and flashes the MIL..51
Truth: 5-gas analyzer shows a perfect stoichiometric burn with  ppm.
Contradiction: Physical reality proves there is no misfire. The ECU is "hallucinating" a combustion failure based on mechanical vibration..1
Case N-017: Turbo Bypass Valve (Blow-off) Leak A 2018 turbo-petrol car has a torn diaphragm in the bypass valve..19
Perception: ECU sees a boost-deviation fault (P0299). L2 trims are normal at idle but spike to -15% under boost.
Truth: The MAF measured the air, but the bypass valve leaked it back to the inlet, causing the engine to run rich during boost.
Contradiction: L1 MAF perception says "More Air," but L2 truth says "Too Much Fuel for the Actual Cylinder Air Mass.".11
Case N-018: Hybrid Transition "Cold-Cat" Logic Error A 2020 Hybrid starts its engine after a long electric-only stretch..54
Perception: ECU uses a "Fast Light-off" strategy, retarding timing and richening the mixture.
Truth: The catalyst has cooled below . Gas analyzer shows  at 4.0% and  at 600 ppm.
Contradiction: If the ECU maintains this state too long, L3 discrepancy logic flags it as a "Strategy Hang" where perception is stuck in warm-up mode..18
Case Group 3 Table: 2013-2020 Fault Projections
Case ID
Year
Fault Description
λOBD​
λcalc​
Δλ
NOx​ (ppm)
Tier Logic
N-013
2015
GDI HPFP Oil Leak
0.85
0.88
0.03
15
L4 Source
N-014
2017
GDI Carbon Sponge
1.02
0.94
0.08
45
L4 Thermal
N-015
2019
Wideband Ref Drift
1.00
1.15
0.15
1100
L3 Blindness
N-016
2014
Flywheel Ghost Misfire
1.00
1.00
0.00
25
L4 Hallucination
N-017
2018
Turbo Bypass Leak
0.92
0.85
0.07
30
L4 Air Path
N-018
2020
Hybrid Cold-Cat
0.90
0.88
0.02
150
L5 Strategy

Case Group 4: Integrated Mechanical and Electronic Hallucinations
These cases address the intersection of complex systems where multiple "liars" combine to create a deceptive diagnostic profile..2
Case N-019: The "Double Liar" (MAF and O2 Drift)
A 2007 sedan has a MAF that under-reports and an  sensor that is biased rich.
Perception: L1 MAF says low air (Lean perception); L1  says high fuel (Rich perception). The two faults cancel each other out in the fuel trim logic. L2 trims stay at 0%.
Truth: The engine is running 15% lean, but the ECU "thinks" everything is perfect.
Contradiction: L3 Truth vs. Perception logic reveals the 1.15  and identifies the "Double Liar" state..3
Case N-020: High-Altitude Mapping Error A 2013 vehicle is driven from sea level to 8,000 feet. The internal BARO calculation is stuck at sea level..57
Perception: ECU "perceives" more air than is actually present. It commands fuel for sea-level density. L1  sees rich, pulls trims to -20%.
Truth: Gas analyzer confirms a rich condition if the trims haven't reached their limit.
Contradiction: L4 logic must distinguish between a fuel system fault and an "Environment Perception" fault..49
Case N-021: Lean Misfire Mimicking Rich Condition A 2004 car has a severe vacuum leak that causes a misfire..12
Perception: The misfire sends raw fuel AND unburned oxygen into the exhaust. L1  sensor sees the oxygen and reports "Lean." ECU adds fuel.
Truth: The gas analyzer shows  at 5.0% and  at 2.5%.
Contradiction: The addition of fuel makes the "Truth" richer, but the "Perception" stays lean because the misfire persists. This is the "Feedback Death Spiral.".11
Case N-022: Restricted Air Filter (Speed-Density) On a 2011 MAP-based engine, the air filter is 90% clogged with debris..48
Perception: L1 MAP sensor sees a drop in manifold pressure (higher vacuum) at wide-open throttle. ECU perceives low load and reduces fuel.
Truth: The engine is physically starved for air.  is low;  is low.
Contradiction: L2 efficiency truth proves the engine is not under "Low Load" but is mechanically restricted..13
Case N-023: VVT Solenoid Electrical Resistance Drift A 2015 vehicle has a VVT solenoid whose coil resistance has increased from 8 ohms to 40 ohms..59
Perception: The ECU pulses the solenoid, but it moves too slowly. No circuit code is set because the driver hasn't "opened." ECU perceives a "Lazy Phaser."
Truth: Tailpipe  is elevated at 2500 RPM.
Contradiction: L1 Electrical perception says "Circuit Pass," but L4 Pattern Matching says "Mechanical/Hydraulic Failure.".33
Case N-024: Ethanol-Blended Fuel Contradiction (E85 in Non-Flex) A 2012 non-flex fuel car is accidentally filled with E85..9
Perception: Stoichiometry for E85 is 9.7:1, not 14.7:1. ECU sees a massive lean condition. LTFT maxes at +35%. ECU throws P0171.
Truth: Gas analyzer (set to gasoline constants) shows a "Perfect"  because the chemistry of E85 produces different gas ratios.
Contradiction: The "Perception" of a fault is a result of the ECU using the wrong reference model for the fuel. L5 Tier uses  and  sums to identify the fuel type shift..9
Case Group 4 Table: Multi-System Interaction Projections
Case ID
Year
Fault Description
λOBD​
λcalc​
Trims (%)
Logic Tier
N-019
2007
Double Liar (MAF/O2)
1.00
1.15
0
L3 Blindness
N-020
2013
BARO Calc Stuck
0.92
0.85
-20
L4 Env Fault
N-021
2004
Lean Misfire Spiral
1.25
0.95
+25
L3 Inversion
N-022
2011
Clogged Air Filter
1.00
1.00
0
L2 Pumping
N-023
2015
VVT Solenoid Drift
1.00
1.01
0
L1 Electrical
N-024
2012
E85 in Petrol Tank
1.15
1.00
+35
L5 Model Shift

Case Group 5: Contemporary Diagnostic Edge Cases (2016-2020)
These cases address the most modern systems, including Gasoline Particulate Filters (GPF) and complex thermal management..2
Case N-025: GPF Restricted (Partial Clog) A 2019 Euro-6 vehicle has a partially clogged Gasoline Particulate Filter..19
Perception: L1 differential pressure sensor sees a high . ECU triggers a regeneration cycle.
Truth: Gas analyzer shows  spikes and high  during the regen.
Contradiction: If the GPF is physically damaged, the "Truth" of the tailpipe gas will show high particulates despite the "Perception" that the regen succeeded..46
Case N-026: GDI "LSPI" Pre-Ignition Signature A 2018 turbo-GDI engine experiences Low-Speed Pre-Ignition (LSPI) under high load..49
Perception: L1 Knock Sensor sees a massive spike. ECU retards timing by 15 degrees.
Truth:  spikes to 5000 ppm for a single engine cycle.
Contradiction: ECU perception is "Knock Control," but the L3 Truth is "Structural Threat." L5 Tier flags this as a high-risk engine health event..15
Case N-027: Electric Thermostat Drift (Over-cooling) A 2016 car has an electronically controlled thermostat that fails to close fully..4
Perception: L1 ECT sensor shows  (Normal operating is ). ECU stays in "Warm-up Enrichment" mode.
Truth: Gas analyzer shows  at 1.5% and  at 0.95.
Contradiction: The engine is stuck in a perceived warm-up state, but the physical reality is excessive fuel consumption and catalyst soot-loading..7
Case N-028: Wideband O2 Heater Element Bias On a 2020 vehicle, the heater circuit for the Air-Fuel sensor is under-performing..16
Perception: The sensor is too cold to provide an accurate L1 reading. The ECU uses a "Safe Map."
Truth: Gas analyzer shows the engine is actually oscillating.
Contradiction: L3 logic sees a "Stale Perception" where the ECU has stopped trusting the sensor, but the physical gas is unmanaged..56
Case N-029: Intake Manifold Flap (IMRC) Stuck A 2017 engine has the swirl flaps stuck in the "High RPM" position at idle..35
Perception: No DTC. ECU perceives a healthy intake path.
Truth:  is high at idle (200 ppm) due to poor air-fuel mixing.
Contradiction: L2 truth proves a loss of volumetric efficiency that the L1 sensors cannot "see.".37
Case N-030: Hybrid Exhaust Heat Exchanger Leak A 2019 Hybrid uses an exhaust-to-coolant heat exchanger to warm the engine. It develops a pinhole leak..10
Perception: L1  sensor is contaminated by glycol (antifreeze). It reports "Lean." L2 trims add 25% fuel.
Truth: Tailpipe is a "White Smoke" rich mess. .
Contradiction: This is a "Cross-System Liar" where the cooling system is poisoning the emissions system perception..24
Case Group 5 Table: Modern Edge Case Projections
Case ID
Year
Fault Description
λOBD​
λcalc​
CO (%)
Confidence
Tier Logic
N-025
2019
GPF Partial Clog
1.00
1.00
0.15
85%
L4 Efficiency
N-026
2018
LSPI Signature
1.00
0.85
Variable
40%
L5 Prognostic
N-027
2016
E-Stat Cold Drift
0.95
0.95
1.50
95%
L4 Thermal
N-028
2020
AF Sensor Cold Bias
1.00
1.05
0.10
30%
L3 Blindness
N-029
2017
IMRC Swirl Stuck
1.01
1.01
0.40
75%
L2 Efficiency
N-030
2019
Heat Exchanger Leak
1.10
0.82
4.50
90%
L3 Liar

Proposed Table Enhancements for the 4D Engine
To support the transition from basic diagnostic scanning to high-fidelity "Truth vs. Perception" logic, the master data architecture (as seen in 'cases_petrol_master.csv') must be enhanced. These proposed columns provide the mathematical and logical infrastructure required for L3 discrepancy detection and L5 prognostic scoring..2
Enhancement 1: The Discrepancy Vector (L3 Focus)
The primary tool for identifying a "Liar" scenario is the discrepancy between internal and external lambda..10
Lambda_Delta_Vector: This is a signed float storing . A value of 0.0 indicates perfect calibration. A positive value (e.g., +0.15) indicates the engine is physically leaner than the ECU perceives (ECU is "Rich-Blind"). A negative value indicates the engine is physically richer than perceived (ECU is "Lean-Blind")..1
Perception_Reliability_Index: A 0-100 score based on the stability of the  sensor voltage and its cross-counts. A "lazy" sensor with 2 cross-counts per 10 seconds would receive a score of 20, triggering a "Low Trust" flag in the L3 layer..23
Enhancement 2: The Combustion Integrity Truth (L2-L4 Focus)
Tailpipe gas chemistry provides an objective measure of energy conversion that PIDs cannot replicate..8
Chemical_Efficiency_Score: Calculated as . This represents the percentage of carbon that was fully oxidized. In a healthy engine, this should be . Values below  indicate a fundamental failure in combustion physics (pumping loss, misfire, or bad timing)..8
Oxygen_Usage_Factor: This is the ratio of  to . In a perfect burn, these are balanced. A high  with high  is the signature of a misfire; high  with near-zero  is the signature of pure rich over-fueling..12
Enhancement 3: The Causal Attribution Layer (L4-L5 Focus)
To provide actionable insights, the table must link gas patterns to physical sources..2
TCG_Root_Source: A string column mapping the gas signature to a causal category: IN intake_leak, EX exhaust_leak, FS sensor_bias, ME mechanical_wear, or SY software_hang..2
Load_Correction_Delta: Compares the MAF-reported load against the gas-calculated load. If the MAF says "Low Load" but the exhaust gas volume and temperature say "High Load," this flags a MAF scaling error..37
Enhancement 4: Hybrid and Modern Meta-Data (L5 Focus)
Modern vehicles require contextual data to interpret emissions correctly..54
Thermal_State_Confidence: A boolean flag indicating whether the catalyst is above the light-off temperature (). If False, L3 discrepancies are treated as expected transient states..12
ECU_Consistency_Score: A diagnostic metric that penalizes the ECU if it reports PIDs that are physically impossible (e.g.,  voltage of 5V on a 1V narrow-band sensor)..1
Metadata Enhancement Summary Table
Enhanced Column Name
Tier
Data Type
Diagnostic Utility
Lambda_Delta_Vector
L3
Float
Quantifies the "Liar" or "Blind" delta.
Perception_Trust_Score
L3
Integer
0-100 score of sensor health vs. gas reality.
Combustion_Integrity
L2
Float
Measures true chemical oxidation efficiency.
Oxygen_Usage_Factor
L2
Float
Discriminates between misfire and rich states.
TCG_Class
L4
String
Root cause isolation (Air/Fuel/Mechanical).
Thermal_LightOff
L2
Boolean
Validates if the catalyst is operational.
ECU_Logic_Score
L5
Integer
0-100 score of internal ECU consistency.
Pumping_Loss_Index
L4
Float
Derived from  and MAP to find restrictions.

Deeper Insights into Diagnostic Causality
The proposed cases and table enhancements reveal several fundamental truths about the "Truth vs. Perception" relationship. The first is the concept of "Diagnostic Blindness." This occurs when a sensor fails in a way that remains within the ECU's "plausible" window. For example, a MAF sensor that under-reports by 15% will not trigger a DTC, but it will significantly alter the ..5 The 4D engine solves this by using L2 gas truth as an external "sanity check" for L1 sensor perception..2
The second insight is "Logic Inversion." This is most common in exhaust leaks and misfires where the ECU adds fuel (Perception: "I am lean") which actually drives the physical state into a dangerous rich condition (Truth: "I am rich")..10 The 4D architecture identifies this inversion at the L3 tier by noting a negative correlation between fuel trim movement and  improvement..6
The third insight is "Systemic Masking." As catalytic converters have become more efficient, they have effectively become "filters of truth." A modern cat can hide massive amounts of engine misbehavior until it reaches a catastrophic failure point..12 The L5 Tier of the 4D engine uses a "Pre-Cat Inference Engine" to model what the gases must have been before they entered the catalyst, based on the heat energy generated within the cat (measured via the temp-differential between inlet and outlet)..10
Practical Application and Implementation Strategy
Implementation of this logic requires a shift in how technicians use diagnostic tools. Instead of looking at a "Check Engine Light" as the beginning of the diagnostic process, the 4D architecture treats the gas analyzer as the baseline..8
Baseline Reality Check (L2): The technician connects a 5-gas analyzer and establishes the physical lambda () and chemical efficiency..9
Perception Alignment (L3): The analyzer data is streamed into the 4D engine alongside the OBD-II PIDs. The Lambda_Delta_Vector is calculated. If the delta is , a "Discrepancy Fault" is initiated..1
Pattern Isolation (L4): The engine uses its TCG library (including the 30 new cases) to find a signature that matches the discrepancy. For instance, if  is positive and  is high, the L4 logic points toward "Unmetered Air" or "MAF Under-reporting.".2
Prognostic Decision (L5): The engine fusion layer calculates a confidence score. If the Perception_Trust_Score is low and the ECU_Logic_Score is low, the L5 decision is to replace the feedback sensor and recalibrate the ECU logic..14
Conclusion: The Future of Autonomous Diagnostics
The tension between "Truth" and "Perception" is the defining challenge of modern engine management. As we move toward more complex GDI and hybrid powertrains, the opportunity for the ECU to be "fooled" by its own sensors increases exponentially. The 5-Tier 4D Diagnostic Architecture, reinforced by the proposed 30 cases and systematic table enhancements, provides a robust mathematical and logical framework to ensure that physical reality always remains the ultimate guide for engine health. By quantifying the gap between what an engine says and what it does, we can move from reactive part-swapping to proactive, high-precision diagnostic engineering..2
Works cited
cases_petrol_master.csv
The FACT Fault Diagnosis Architecture. - ResearchGate, accessed on April 29, 2026, https://www.researchgate.net/figure/The-FACT-Fault-Diagnosis-Architecture_fig5_269393623
Electronic Systems Diagnosis Fault in Gasoline Engines Based on Multi-Information Fusion, accessed on April 29, 2026, https://www.researchgate.net/publication/327411175_Electronic_Systems_Diagnosis_Fault_in_Gasoline_Engines_Based_on_Multi-Information_Fusion
Freeze Frame PID Definitions - Innova, accessed on April 29, 2026, https://www.innova.com/blogs/diagnostics-101/freeze-frame-pid-definitions
What a dying Mass Airflow Sensor looks and feels like : r/cars - Reddit, accessed on April 29, 2026, https://www.reddit.com/r/cars/comments/4y19kh/what_a_dying_mass_airflow_sensor_looks_and_feels/
Understanding Long Term Fuel Trim (Bank 1) and How to Diagnose Issues - Foxwell Diag, accessed on April 29, 2026, https://www.foxwelldiag.com/blogs/car-diagnostic/understanding-long-term-fuel-trim-bank-1-and-how-to-diagnose-issues
What Are Short-Term and Long-Term Fuel Trims? - In The Garage with CarParts.com, accessed on April 29, 2026, https://www.carparts.com/blog/what-are-short-term-and-long-term-fuel-trims/
Understanding Engine Exhaust Emissions - Crypton Diagnostic Equipment, accessed on April 29, 2026, https://www.crypton.co.za/Tto%20know/Emissions/exhaust%20emissions.html
Advanced Diagnostics Using The Five Gas Analyzer - Automotive Test Solutions, accessed on April 29, 2026, https://automotivetestsolutions.com/knowledge-base/case-studies/all-case-studies/advanced-diagnostics-using-the-five-gas-analyzer/
Mark Warren A good diagnostician may not know the answers, but he knows what questions to ask to get them. This is the second of, accessed on April 29, 2026, https://emsgas.com/wp-content/uploads/2023/12/MOTOR_022010_05.pdf
Fuel Trim Diagnostics Have Changed - Gears Magazine, accessed on April 29, 2026, https://gearsmagazine.com/magazine/fuel-trim-diagnostics-have-changed/
5-Gas Diagnostic Chart - Walker Exhaust, accessed on April 29, 2026, https://www.walkerexhaust.com/support/tech-tips/five-gas-diagnostic-chart.html
Vacuum Gauge & Transducer Testing - MOTOR Information Systems, accessed on April 29, 2026, https://www.motor.com/magazine-summary/vacuum-gauge-transducer-testing-july-2006/
Electronic Systems Diagnosis Fault in Gasoline Engines Based on Multi-Information Fusion, accessed on April 29, 2026, https://pmc.ncbi.nlm.nih.gov/articles/PMC6164238/
Automotive Internal-Combustion-Engine Fault Detection and Classification Using Artificial Neural Network Techniques | Request PDF - ResearchGate, accessed on April 29, 2026, https://www.researchgate.net/publication/271715403_Automotive_Internal-Combustion-Engine_Fault_Detection_and_Classification_Using_Artificial_Neural_Network_Techniques
Making Sense of Sensors: The Oxygen Sensor - Delphi, accessed on April 29, 2026, https://www.delphiautoparts.com/resource-center/article/making-sense-of-sensors-the-oxygen-sensor
Diagnosing a Lean-Running Engine - MOTOR Information Systems, accessed on April 29, 2026, https://www.motor.com/magazine-summary/lean-codes-january-2018/
5-Gas Analysis | MOTOR - MOTOR Information Systems, accessed on April 29, 2026, https://www.motor.com/magazine-summary/5-gas-analysis-may-1998/
How Exhaust Restrictions Affect Turbo and Engine Performance - Goldfarb & Associates Inc, accessed on April 29, 2026, https://goldfarbinc.com/blogs/news/how-exhaust-restrictions-affect-turbo-and-engine-performance
Fuel Trim Diagnostics - What To Look For In Rich or Lean Conditions, accessed on April 29, 2026, https://apemissions.com/fuel-trim-diagnostics-what-to-look-for-in-rich-or-lean-conditions/
Vacuum Leak: Symptoms, Causes, How to Fix - In The Garage with CarParts.com, accessed on April 29, 2026, https://www.carparts.com/blog/vacuum-leak-symptoms-causes-how-to-fix/
Long-Term & Short-Term Fuel Trim - General Technologies Corp., accessed on April 29, 2026, https://gtc.ca/blog/long-term-fuel-trim-and-short-trim-fuel-trim/
O2 Sensor Cross Counts - Reatta Owners Journal Forum, accessed on April 29, 2026, https://reattaowner.com/forum/topic/1738-o2-sensor-cross-counts/
Diagnosing a Faulty Oxygen Sensor, accessed on April 29, 2026, https://www.wagnerbrake.com/technical/technical-tips/diagnosing-a-faulty-oxygen-sensor.html
Trouble Shooter | Spiking Fuel Trims | MOTOR Magazine, accessed on April 29, 2026, https://www.motor.com/magazine-summary/trouble-shooter-june-2018/
Foreign Service | Mass Airflow (MAF) Sensor | MOTOR Magazine, accessed on April 29, 2026, https://www.motor.com/magazine-summary/foreign-service-november-2007/
Vacuum Leak: Understanding The Symptoms, Causes, Diagnosis, And Costs - Innova, accessed on April 29, 2026, https://www.innova.com/blogs/fix-advices/vacuum-leak-understanding-the-symptoms-causes-diagnosis-and-costs
DIAGNOSE FUEL PUMP - AA1Car, accessed on April 29, 2026, https://www.aa1car.com/library/fuel_pump_diagnose.htm
Diagnosing Exhaust Leaks Upstream of 02 Sensor - Mechanics Stack Exchange, accessed on April 29, 2026, https://mechanics.stackexchange.com/questions/49966/diagnosing-exhaust-leaks-upstream-of-02-sensor
exhaust leak near O2 sensor, is it affecting fuel economy? : r/MechanicAdvice - Reddit, accessed on April 29, 2026, https://www.reddit.com/r/MechanicAdvice/comments/13jfedh/exhaust_leak_near_o2_sensor_is_it_affecting_fuel/
Bad Variable Timing Solenoid Symptoms - AutoZone, accessed on April 29, 2026, https://www.autozone.com/diy/engine/bad-variable-timing-solenoid-symptoms
Is Your VVT Solenoid Acting Up? Common Indicators to Watch For - Foxwell Diag, accessed on April 29, 2026, https://www.foxwelldiag.com/blogs/car-diagnostic/vvt-solenoid-symptoms
P0011 Code: Camshaft Position Timing Over-Advanced (Bank 1) — Symptoms, Causes & Fixes - Foxwell Diag, accessed on April 29, 2026, https://www.foxwelldiag.com/blogs/car-diagnostic/p0011-code-camshaft-position-timing-over-advanced-bank-1
P0011 Code: Camshaft Timing Over-Advanced Causes & Fix - A-Premium, accessed on April 29, 2026, https://a-premium.com/blogs/p0011-code-camshaft-timing-over-advanced-bank-1-what-you-need-to-know
Variable Valve Timing technology made clear - Goss - News & Info, accessed on April 29, 2026, https://www.goss.com.au/news/article/variable-valve-timing-technology-made-clear
GM > Engine > Airflow > General Airflow - HP Tuners, accessed on April 29, 2026, https://www.hptuners.eu/help/vcm_editor_parameters_gm_eng_airflow_general.htm
MAF Sensor Diagnosis - Gears Magazine, accessed on April 29, 2026, https://gearsmagazine.com/magazine/maf-sensor-diagnosis/
Risks of Driving with a Bad Purge Valve - Identifix, accessed on April 29, 2026, https://www.identifix.com/blogs/risks-of-driving-with-a-bad-purge-valve/
Signs of a Bad Purge Valve - AutoZone, accessed on April 29, 2026, https://www.autozone.com/diy/fuel-systems/signs-of-a-bad-purge-valve
Canister Purge Valve Solenoid: Symptoms, Replacement Cost - In The Garage with CarParts.com, accessed on April 29, 2026, https://www.carparts.com/blog/canister-purge-valve-solenoid-symptoms-replacement-cost/
Canister Purge Valve: Symptoms, Function, Testing & Replacement Guide - Bettlink, accessed on April 29, 2026, https://www.bettlink.com/blog/canister-purge-valve-guide
P0171 Code: System Too Lean Causes & Fixes (2026 Guide) - Rohnert Park Transmission, accessed on April 29, 2026, https://rohnertparktransmission.com/blog/p0171-system-too-lean-code-guide
ENGINES AND REAL DATA EVALUATION - LJMU Research Online, accessed on April 29, 2026, https://researchonline.ljmu.ac.uk/id/eprint/5867/1/446357.pdf
What are the Signs or Symptoms of a Clogged Muffler? - CarParts.com, accessed on April 29, 2026, https://www.carparts.com/blog/what-are-the-signs-or-symptoms-of-a-clogged-muffler/
Exhaust Back Pressure: How to Get It Right - Holley Motor Life, accessed on April 29, 2026, https://www.holley.com/blog/post/exhaust_back_pressure_how_to_get_it_right/
Simple Diagnostic Testing - Walker Exhaust, accessed on April 29, 2026, https://www.walkerexhaust.com/support/tech-tips/simple-diagnostic-testing.html
How to Tell If the Catalytic Converter is Clogged - In The Garage with CarParts.com, accessed on April 29, 2026, https://www.carparts.com/blog/how-to-tell-if-the-catalytic-converter-is-clogged/
UNDERSTANDING 5 GAS DIAGNOSIS COMPONENTS ... - 911 SG, accessed on April 29, 2026, https://911sg.com/wp-content/uploads/2023/06/understanding5gas_frpm-smog-tech-institute.pdf
Complete Guide to P0171 - Fuel Trim System Lean (Bank 1): Symptoms, Fix, Diagnose, accessed on April 29, 2026, https://www.foxwelldiag.com/blogs/car-diagnostic/p0171-fuel-trim-system-lean-bank-1-symptoms-fix-diagnose
Reading O2 sensor voltage ranges in Live Data - Innova, accessed on April 29, 2026, https://www.innova.com/blogs/fix-advices/reading-o2-sensor-voltage-ranges-in-live-data
Check Engine Light Codes Explained: P0420, P0300, P0171 & More (DIY Fixes & Costs), accessed on April 29, 2026, https://tendsupplies.com/blog/check-engine-light-codes-explained-p0420-p0300-p0171-more-diy-fixes-costs/
Understanding Freeze Frame Data: Key to Efficient Diagnostics - Becker Car Care Inc., accessed on April 29, 2026, https://beckercarcare.com/blog/understanding-freeze-frame-data/
Use-case – Diagnosing an automotive engine - Fault Diagnosis Toolbox, accessed on April 29, 2026, https://faultdiagnosistoolbox.github.io/usecase/
The change from tailpipe to OBD II emissions testing will require changes in how you approach emissions repairs, and how you exp, accessed on April 29, 2026, https://www.motor.com/magazinepdfs/042002_06.pdf
Emission Control and Exhaust Systems Diagnosis and Repair - Goodheart-Willcox, accessed on April 29, 2026, https://www.g-w.com/assets/files/pdf/sampchap/9798888172094_ch20.pdf
O2-Sensor - Fiero Focus, accessed on April 29, 2026, https://www.fierofocus.com/articles/tt-o2_sensor.html
Successful MAF Sensor Diagnosis - MOTOR Information Systems, accessed on April 29, 2026, https://www.motor.com/magazine-summary/successful-maf-sensor-diagnosis/
Interpreting Fuel Trim Readings | Becker Car Care in Halstead, KS, accessed on April 29, 2026, https://beckercarcare.com/blog/interpreting-fuel-trim-readings/
Common Symptoms of a Bad Variable Valve Timing Solenoid and How to Test It? - ancel, accessed on April 29, 2026, https://www.ancel.com/blogs/news/common-symptoms-of-a-bad-variable-valve-timing-solenoid-and-how-to-test-it
P0014 – Exhaust camshaft timing over-advanced (bank 1) - OBDeleven, accessed on April 29, 2026, https://obdeleven.com/p0014
Does downstream O2 sensor affect fueling and FE in Petrol Engines? - Team-BHP, accessed on April 29, 2026, https://www.team-bhp.com/forum/technical-stuff/132889-does-downstream-o2-sensor-affect-fueling-fe-petrol-engines.html
What Are Camshaft Phasers? - Little Wolf Automotive, accessed on April 29, 2026, https://littlewolfauto.com/what-are-camshaft-phasers/
If an engine is running rich... : r/mechanic - Reddit, accessed on April 29, 2026, https://www.reddit.com/r/mechanic/comments/1isyh38/if_an_engine_is_running_rich/
If an O2 sensor was lazy, accessed on April 29, 2026, https://naxja.org/threads/if-an-o2-sensor-was-lazy.1122931/
Troubleshooting Oxygen Sensors - Walker Products, accessed on April 29, 2026, https://www.walkerproducts.com/o2-sensor-training-guide/troubleshooting-oxygen-sensors/
O2 sensor reading MAXIMUM LEAN but exhaust SOOTY BLACK (rich). Replaced it and got the same thing. Scan tool gives lean code and car idles terribly and stalls at idle. : r/AskMechanics - Reddit, accessed on April 29, 2026, https://www.reddit.com/r/AskMechanics/comments/p3f8pj/o2_sensor_reading_maximum_lean_but_exhaust_sooty/
Symptoms of a Clogged Catalytic Converter - AutoZone.com, accessed on April 29, 2026, https://www.autozone.com/diy/catalytic-converter/symptoms-of-a-clogged-catalytic-converter
