Architectural Evolution and Era-Based Classification of Petrol Vehicle Diagnostics
The historical progression of gasoline internal combustion engine management systems is defined by a continuous co-evolution of environmental regulations and diagnostic capabilities.1 Over three decades, engine control architectures transitioned from primitive closed-loop analog strategies to highly complex, multi-variable cyber-physical models.3 To understand the physical and chemical anomalies captured within the cases_petrol_master_v5 diagnostic database, it is necessary to establish a rigorous chronological framework.6 By analyzing the fuel delivery systems, sensor designs, aftertreatment hardware, and onboard communication protocols, these diagnostic cases can be classified into three distinct historical eras: Era A (1990–2000), Era B (2000–2010), and Era C (2010–2020).4
Combustion Chemistry and On-Board Diagnostic Frameworks
Tailpipe emissions testing relies on the chemical mass balance of the combustion process.6 By measuring the raw concentrations of carbon monoxide (), carbon dioxide (), unburned hydrocarbons (), oxygen (), and oxides of nitrogen (), the air-fuel equivalence ratio () can be calculated.6 This calculation is performed using the Brettschneider equation, which establishes a stoichiometric balance based on the atomic ratios of the fuel 6:

Here,  represents the hydrogen-to-carbon ratio (typically  for standard gasoline),  is the oxygen-to-carbon ratio, and  is the conversion factor for the hydrocarbon analyzer.6 While the complete Brettschneider equation accounts for  concentration, legacy workshops operating four-gas analyzers omit this channel because  contributes negligibly to the overall oxygen balance, adding only approximately   equivalent per  of .6
In a properly operating closed-loop control system, this chemical calculation matches the engine control unit (ECU) feedback value ().6 However, when feedback loops degrade, a major diagnostic phenomenon emerges: the "Truth-versus-Perception" gap.6 This gap is defined by a significant divergence between the actual chemical composition of the exhaust gas and the ECU’s sensor-driven interpretation of that gas.6
This perception gap typically stems from localized sensor bypass or chemical degradation.6 For example, a pre-catalytic exhaust leak allows ambient air to be drawn into the exhaust manifold via venturi effects during exhaust gas pressure pulses.6 The upstream oxygen sensor registers this localized oxygen concentration () and reports a false lean mixture to the ECU.6 In response, the ECU's fuel trim logic drives the short-term and long-term fuel trims ( and ) highly positive to enrich the mixture 6:

This action physically floods the combustion chambers with excess fuel, creating a highly rich actual mixture characterized by high carbon monoxide () and low oxygen () at the tailpipe.6 Despite this rich mixture, the ECU continues to report a lean Diagnostic Trouble Code (DTC), such as P0171, demonstrating a complete perception inversion.6 Understanding these physical and chemical interactions is critical for classifying the anomalies detailed in the database.6
Historical Taxonomy of Diagnostic Eras
The technological shifts across these three decades reflect the regulatory requirements of their respective periods.1 Each era represents a step-change in control-loop speed, diagnostic resolution, and aftertreatment complexity.4



     1990–2000 (Era A)                   2000–2010 (Era B)                   2010–2020 (Era C)
┌─────────────────────────┐         ┌─────────────────────────┐         ┌─────────────────────────┐
│ • Port Fuel Injection   │         │ • CAN-Bus OBD-II / EOBD │         │ • Gasoline Direct Inj.  │
│ • Narrowband O2 Sensors │  ────>  │ • Dual-Bed Catalysts    │  ────>  │ • Particulate Filters   │
│ • Standalone 4-Gas      │         │ • Upstream Wideband O2  │         │ • Hybrid Powertrains    │
│ • Legacy Analog OBD-I   │         │ • Digital Fuel Trims    │         │ • Model-Based Control   │
└─────────────────────────┘         └─────────────────────────┘         └─────────────────────────┘


Era A: 1990–2000 (The Dawn of OBD-I, Early OBD-II, and Narrowband Closed-Loop Control)
This period represents the initial transition from carbureted fuel delivery to early electronic Multi-Point Port Fuel Injection (PFI).11 It is defined by simple closed-loop emissions strategies designed to comply with the US Clean Air Act Amendments of 1990 and early Euro 1 and Euro 2 regulations.1
Vehicles in this era utilize Port Fuel Injection (PFI), where fuel is injected into the intake runner immediately ahead of the intake valve.11 Airflow is monitored using primitive hot-wire Mass Air Flow (MAF) meters or Speed-Density calculations relying on Manifold Absolute Pressure (MAP) sensors.3 Evaporative emission control (EVAP) systems utilize simple vacuum-operated purge valves without advanced pressure diagnostics.4
Oxygen sensing is restricted to narrowband Zirconia-electrolyte sensors.8 These sensors behave as a galvanic cell, generating a non-linear voltage output swinging between  (lean) and  (rich), centered on a stoichiometric midpoint of .8 Heated oxygen sensors (HO2S) with internal resistance heaters are introduced to reduce cold-start open-loop time.8
Onboard diagnostics are highly fragmented.3 Early OBD-I systems rely on flashing check engine lights (MIL) to output proprietary trouble codes.4 While OBD-II became mandatory in the United States in 1996, communication protocols are slow and limited to K-Line (ISO 9141-2) or pulse-width modulation (SAE J1850).4 No Controller Area Network (CAN) bus protocols are used on the diagnostic link.4 emissions aftertreatment is limited to simple three-way catalytic converters (TWC).6 Downstream catalyst monitoring is absent or highly primitive, and freeze-frame data captures are non-standardized or unavailable.3
Era B: 2000–2010 (EOBD Mandates, CAN Bus Standardization, and Port Fuel Injection Dominance)
This era is characterized by the maturation of OBD-II diagnostics, the introduction of mandatory European On-Board Diagnostics (EOBD), and the transition to high-speed digital communications.4
Port Fuel Injection remains the dominant fuel delivery architecture.10 Variable Valve Timing (VVT) via hydraulic oil-control solenoids becomes widespread.6 Evaporative emission systems are highly scrutinized, utilizing evaporative system leak diagnostics (such as P0455) that monitor fuel tank pressure drops via dedicated vacuum decay monitors.4
First-generation wideband oxygen sensors are introduced on upstream exhaust systems to support continuous, proportional fuel trim control.8 These sensors utilize a Nernst cell combined with an oxygen pump cell to maintain a constant internal balance, outputting a variable current that corresponds directly to the exact lambda value.8 Downstream oxygen sensors are universally mandated to monitor catalytic converter efficiency.6
EOBD becomes mandatory for all petrol vehicles in the European Union in 2001.4 This mandates standard 16-pin DLC connectors and generic Diagnostic Trouble Codes (DTCs).3 In 2008, the United States mandates that all vehicles implement OBD-II diagnostics exclusively over a high-speed Controller Area Network (CAN) bus according to ISO 15765-4.4 Standardized freeze-frame data, including Engine Coolant Temperature (ECT), engine load, and engine speed, are universally captured.3 Aftertreatment shifts to highly efficient, dual-bed three-way catalytic converters.6 Downstream  sensors are continuously monitored for voltage switching to detect catalyst oxygen storage capacity degradation.6
Era C: 2010–2020 (TGDI Dominance, Gasoline Particulate Filters, and Hybrid System Integration)
This era is characterized by aggressive downsizing, turbocharging, and high-pressure fuel injection to satisfy stringent Euro 6, EPA Tier 3, and China 6 emissions standards.10
Port Fuel Injection is largely replaced by high-pressure Gasoline Direct Injection (GDI) and Turbocharged GDI (TGDI) systems.10 Fuel is injected directly into the combustion chamber at pressures reaching up to  via mechanical High-Pressure Fuel Pumps (HPFP) driven by the camshaft.21 To mitigate GDI particulate emissions and intake valve carbon buildup, some manufacturers deploy dual-injection systems combining port and direct injection on the same engine.10 Highly advanced wideband sensors with integrated heater control and fast light-off capabilities are standard.8 High-pressure fuel rail sensors and differential exhaust pressure sensors are introduced.6
To comply with Euro 6c and 6d particle number (PN) limits, Gasoline Particulate Filters (GPFs) are integrated into the exhaust system downstream of the three-way catalytic converter.10 These wall-flow ceramic filters capture fine particulates ( and smaller) and undergo passive regeneration during vehicle deceleration overruns, where fuel is cut off and oxygen becomes available in the hot exhaust stream.10
Integrated hybrid powertrains introduce complex start-stop thermal management challenges, such as cold catalyst light-off enrichment strategy hangs.6 Highly boosted downsized engines suffer from Low-Speed Pre-Ignition (LSPI)—a highly damaging combustion anomaly where oil-fuel droplets ignite prematurely during the compression stroke, requiring rapid knock-sensor feedback and transient spark timing retard.6
Systematic Era Classification of Petrol Vehicle Diagnostic Cases
The complete database of petrol vehicle diagnostic cases is classified into three eras based on the diagnostic parameters, sensor architectures, and mechanical systems present in each case.6
Era A (1990–2000): Early OBD and Standard Exhaust Bench Diagnostics
The cases classified in Era A represent vehicles operating on pre-CAN, early OBD-II, or OBD-I architectures.4 They are characterized by a reliance on four-gas exhaust analyzer profiles, standalone troubleshooting rules, manual fuel regulators, and narrowband Zirconia sensor failures.3

Case ID / Range
Diagnostic Features & Gas Chemistry Profile
Era Assignment Justification
PDF-4G-01 to PDF-4G-05

YAML-PDF_4G_01 to YAML-PDF_4G_05
: –, : –, : –, : –,  (unmeasured). Trims: flat .6
These cases represent legacy four-gas exhaust analyzer profiles without digital OBD integration or lambda reporting.6 This represents the manual exhaust gas diagnostic methodologies of the 1990s, where tailpipe gas compositions were analyzed on a standalone workshop bench to isolate engine faults.3
RULE-CO-1

RULE-NOx-1

YAML-RULE_CO_1

YAML-RULE_CO2_1

YAML-RULE_NOx_1
Static stoichiometric and chemical rules: , , .6
These generic threshold-based rules were designed for early emissions screening guides.6 They rely on basic static limits to identify rich/lean faults before the development of modern model-based ECU diagnostics.3
EXP-N001
, , , , , , . Active DTC: P0171.6
This case features a 1999 model year vacuum brake booster diaphragm.6 The transient lean condition manifests exclusively during brake pedal depression under high intake manifold vacuum, a classic diagnostic scenario of early OBD-II vehicles.3
EXP-N003
, , , , , , . Active DTC: P0172.6
This case models a 1997 model year Fuel Pressure Regulator (FPR) with a blocked return line.6 Dual-line mechanical fuel systems with a return line to the fuel tank are characteristic of 1990s fuel systems.11 High fuel line pressure () drives extreme richness that the ECU cannot correct.6
EXP-N006
, , , , , , . No active DTCs.6
This case features a 1996 model year MAP sensor calibration drift on a Speed-Density engine.6 MAP-driven fuel calculation without mass airflow verification was the standard fuel management strategy of the mid-1990s.11
EXP-N002
, , , , , , . Active DTC: P0171.6
An upstream narrowband Zirconia sensor is poisoned by RTV silicone.6 Silicone poisoning blocks the porous platinum electrode of narrowband sensors, a common failure mode in the 1990s due to the use of silicone-gasket chemicals.6
EXP-N005
, , , , , , . No active DTCs.6
A frayed engine ground strap creates alternator AC ripple on the sensor ground circuit.6 This unshielded analog signal interference mimics healthy narrowband oxygen sensor switching, blinding the ECU to a physical lean mixture—a diagnostic issue typical of early analog wiring harnesses.6
CSV-083

YAML-CSV83

CASE-047
, , , –.6
The "probe in open air" sentinel represents a classic workshop calibration check.6 The gas analyzer registers ambient atmospheric conditions, confirming the exhaust probe has been removed from the tailpipe.3
CSV-081

YAML-CSV81

CASE-046
 (physically impossible, exceeding the  limit for gasoline).6
An impossible carbon dioxide reading indicating NDIR bench calibration drift or sensor cell saturation.6 This requires analyzer recalibration against reference gas, a common maintenance requirement of 1990s workshop gas benches.3
CASE-041
, , , , calculated .6
An exhaust leak at the sample probe tip dilutes the sample with ambient air.6 The low  and high  yield a calculated lambda that is physically impossible for a running engine, representing a classic probe placement failure.3
case_006
, , , , calculated .6
A non-starter with no fuel delivery captured during cranking.6 Zero hydrocarbons and atmospheric oxygen confirm that no fuel is entering the combustion chambers.6
case_040
, , , , calculated . Active DTC: P0335.6
A non-starter with no spark caused by a crankshaft position (CKP) sensor failure.6 The P0335 code and zero RPM signal confirm that the ECU cannot synchronize ignition timing, preventing combustion.4
ECU-003

YAML-TC47

CSV-045

YAML-CSV45

CSV-125

CSV-126
–, –, –, –. Active DTC: P0201.6
These cases represent a shorted or open MOSFET injector driver on the ECU's discrete PCB circuitry.6 The driver failure prevents fuel delivery to cylinder 1, a diagnostic failure mode typical of early robust OBD-II powertrain control modules.4

Era B (2000–2010): CAN-Bus OBD-II/EOBD Port Fuel Injection Diagnostics
The cases classified in Era B utilize standardized OBD-II and EOBD communication protocols over high-speed CAN buses.4 They are characterized by standard freeze-frame parameters, dual-bed catalytic converter monitoring, variable valve timing phaser lags, and upstream wideband oxygen sensor diagnostics.3



┌─────────────────────────────────────────────────────────────────────────────┐
│                       ERA B REPRESENTATIVE CASES                           │
├─────────────────────────────────────────────────────────────────────────────┤
│ • CSV-001 to CSV-100 (Core OBD-II Generic Fault Cases)                      │
│ • REAL-001 to REAL-005 (Real Vehicle CAN Scans)                             │
│ • MECH-001 to MECH-004, MECH-006 (Standard Mechanical Faults)               │
│ • ECU-001, ECU-002, ECU-007 to ECU-009 (Logic / Microcontroller Faults)     │
│ • EXT-201 to EXT-240 (Comprehensive Field Freeze Frame Cases)                │
│ • case_001 to case_050 (EOBD Standard Fuel Trim & Sensor Monitors)          │
└─────────────────────────────────────────────────────────────────────────────┘



Case ID / Range
Diagnostic Features & Gas Chemistry Profile
Era Assignment Justification
CSV-001 to CSV-100 (Excluding GDI / advanced cases)
: variable, : variable, : variable, : variable, : variable. Active DTCs: P0171, P0172, P0300, P0420.6
This core validation database utilizes standard generic OBD-II diagnostic parameters.6 These cases model port fuel injection failures (vacuum leaks, leaking injectors, lazy O2 sensors, dead coils, mechanical compression, catalytic storage degradation) monitored by early CAN systems.6
YAML-CSV1 to YAML-CSV100 (Excluding GDI / advanced cases)
Standard database format conversions of the core CSV- series cases.6
Standard validation cases mapping generic OBD-II fault criteria into software platforms.6 Direct utilization of SAE J1979 standard parameters.3
REAL-001 to REAL-005
Extreme gas and diagnostic readings:  up to ,  up to ,  up to .6
Standard CAN-bus connected powertrain controllers captured under real-world vehicle failure modes.6 Includes cold-start flooding, catalyst degradation, and fuel pump failure cases typical of standard passenger cars.6
MECH-001 to MECH-004

MECH-006
: elevated (–), : depressed (–), : elevated (–).6
Mechanical engine wear profiles (worn piston rings, head gasket failures, intake vacuum leaks, low multi-cylinder compression).6 Diagnosed utilizing standardized generic OBD-II fuel trim monitors.3
ECU-001

ECU-002

ECU-007 to ECU-009
: variable, : variable, : variable, : variable. Active DTCs: P0171, P0113, P0300.6
Electronic hardware and software faults (reference voltage drifts, microcontroller computation errors, alternator ripple ghosts, crankshaft speed noise) typical of 2000s OBD-II engine control modules.4
TC-011

TC-021

TC-046

TC-048
: variable, : variable, : variable, : variable. Active DTC: P0171.6
Diagnostic test cases modeling standard port injection trim dynamics and air leak conditions under standard EOBD/CAN interfaces.6
YAML-TC1 to YAML-TC48 (Excluding GPF/GDI)
Standard digital format conversions of the TC- series diagnostic models.6
Software test cases designed to verify the diagnostic capability of software algorithms on CAN-compliant engine systems.6
PDF-HI-001 to PDF-HI-010
: –, : –, : –.6
Standardized "high-idle" () emissions verification test profiles.6 High-idle testing was widely mandated in the 2000s to verify catalytic converter efficiency.3
YAML-PDF_HI_001 to YAML-PDF_HI_010
Digital database representations of the high-idle validation profiles.6
Standard database mappings of the high-idle emissions verification profiles, relying on standard port injection and catalytic converter configurations.6
CSV-101 to CSV-112

CSV-117 to CSV-124

CSV-127

CSV-128
Combustion values with variable secondary parameters.6
Port fuel injection, VVT lagging, valve stem seal snaps, standard PCV leaks, fuel delivery/failing pump diagnosed using EOBD standard parameters.4
EXP-N004
, , , , , , . Active DTC: P0171.6
Exhaust manifold crack upstream of the oxygen sensor.6 Ambient air is drawn into the crack during exhaust pressure pulses, causing a false lean reading and positive trims, which physically rich-floods the engine.6 This represents a classic perception-inversion symptom.6
EXP-N008
, , , , , , . No active DTCs.6
High oil consumption ( per ).6 The three-way catalytic converter masks the oil hydrocarbons at the tailpipe, but rising long-term fuel trims betray the gradual reduction in catalytic oxygen storage capacity.6 This is a silent mechanical decline profile typical of mid-2000s vehicles.6
EXP-N009

CASE-019
, , , , , , . Active DTC: P0171.6
Models a 2006 model year hot-film MAF sensor with dust contamination.6 Dust accumulation on the heated platinum film causes the sensor to under-report the actual air mass entering the engine, causing a physical lean condition.6 MAF contamination was a widespread diagnostic failure mode on Euro 4 platforms.7
EXP-N010
, , , , . Active DTC: P0441.6
EVAP purge valve stuck open causing intake vapor flooding.6 The unmetered fuel vapors flood the intake, driving fuel trims negative under high purge flow conditions.4
EXP-N011
, , , , . No active DTCs.6
Cracked PCV hose causing an intermittent intake vacuum leak.6 The unmetered air entering the intake manifold causes a hunting idle and fluctuating fuel trims as the ECU attempts to compensate.4
EXP-N012
, , , , . No active DTCs.6
Collapsed muffler baffle causing exhaust restriction.6 The restricted exhaust flow increases backpressure, reducing volumetric efficiency and depressing  under load.4
EXP-N015
, , , , , , . No active DTCs.6
Upstream wideband oxygen sensor reference current () drift.6 Wideband planar sensors, introduced in the mid-2000s, suffer from internal reference cell micro-cracks.6 This drift causes the ECU to calculate a false stoichiometric mixture while the tailpipe runs physically lean, generating high  ().6
EXP-N016
, , , , . Active DTC: P0300.6
Dual-mass flywheel mechanical play causing crankshaft speed jitter.6 The CKP sensor registers this rotational speed jitter as misfires, causing the ECU to throw a false P0300 code despite perfect tailpipe chemistry—a classic mechanical diagnostic anomaly of the mid-2000s.4
EXP-N019
, , , , , , . No active DTCs.6
A "double-liar" scenario where a MAF sensor under-reports airflow and an oxygen sensor is biased rich.6 The opposing sensor biases cancel each other out in the ECU's control loop, leaving the engine to run physically lean without triggering fuel trim adaptations.6
EXP-N020

CASE-022
, , , , , , . No active DTCs.6
The ECU's barometric pressure calculation is stuck at sea-level while the vehicle is at high altitude.6 The resulting speed-density density calculation is skewed, causing over-fueling and highly negative trims.6
EXP-N021
, , , , , , . Active DTC: P0171.6
A lean misfire feedback death spiral.6 A severe vacuum leak triggers a misfire, dumping unburned oxygen and fuel.6 The O2 sensor registers the oxygen and drives trims positive, enriching the mixture until the engine floods, while the ECU continues to report a lean DTC.6
EXP-N022
, , , , . No active DTCs.6
A  clogged air filter causing high pumping losses.6 The intake restriction reduces overall air mass and engine output, though stoichiometry is maintained, representing a standard maintenance neglect profile.6
EXP-N024
, , , , . Active DTC: P0304.6
Load-dependent ignition coil breakdown.6 Spark occurs normally at idle but breaks down under high cylinder pressures, dumping raw fuel and air under load—a diagnostic issue standard on 2000s coil-on-plug systems.4
EXP-N027
, , , , , , . Active DTC: P0128.6
Thermostat stuck open (P0128).6 The engine fails to reach operating temperature, causing the ECU to remain in a cold-start enrichment mapping, elevating  and .4
EXP-N028
, , , , . Active DTC: P0053.6
Oxygen sensor heater circuit performance loss.6 The sensor heater fails to maintain operating temperature, causing the sensor to drop out of closed-loop operation under low exhaust temperatures.6
EXP-N029
, , , , . No active DTCs.6
Intake Manifold Runner Control (IMRC) swirl flaps stuck open at idle.6 The lack of charge motion at low engine speeds causes poor fuel mixing, elevating hydrocarbons despite a stoichiometric mixture.6
EXT-201 to EXT-240
Combustion values with standardized OBD-II freeze frame parameters (ECT, RPM, LOAD, STFT, LTFT, MAF, vehicle speed).6
Standard field diagnostic records.6 These represent standard CAN-era OBD-II troubleshooting utilizing standardized freeze frame records and oxygen sensor switching speed (cross-counts) parameters.3
CASE-010 to CASE-030
Combustion and fuel trim parameters, active DTCs: P0134, P0171, P0420, P0011, P0128, P0101, P0507.6
Standard service center records utilizing high-speed CAN diagnostic tools and standard port-fuel injected engines.4
case_001 to case_050 (Excluding specific GDI/advanced cases)
Combustion values with standardized fuel trims, active DTCs: P0171, P0172, P0300, P0420, P0134, P0131, P0132, P0106, P2096, P0190.6
Standardized EOBD diagnostic records.6 These cases focus on port fuel injection failures and generic diagnostic trouble codes.4

Era C (2010–2020): High-Pressure GDI, TGDI, and Hybrid Powertrain Diagnostics
The cases classified in Era C represent modern direct-injection, turbocharged, or hybrid drivetrains.10 They are characterized by advanced emissions control hardware (GPFs), high-pressure common rail diagnostics, and low-speed pre-ignition (LSPI) events.6

Case ID / Range
Diagnostic Features & Gas Chemistry Profile
Era Assignment Justification
MECH-005
, , , , , , .6
Carbon deposits on intake valves in a GDI engine.6 This is a diagnostic failure mode unique to direct-injection gasoline systems, where the lack of port fuel washing allows intake valve carbon to accumulate, causing cold-start lean misfires.11
EXP-N025
, , , , , , . Active DTC: P2452.6
Euro-6 Gasoline Particulate Filter (GPF) partial clog.6 GPFs were introduced starting in 2017/2018 to meet Euro 6c particle number limits for GDI vehicles.19 The P2452 code monitors the GPF differential pressure sensor circuit.6
EXP-N026

CASE-035
, , –, –, –. Active DTC: P0324.6
Turbo-GDI Low-Speed Pre-Ignition (LSPI) event.6 LSPI occurs strictly in highly boosted downsized direct-injection engines under high load and low RPM, a diagnostic challenge unique to 2010s TGDI engines.10 The P0324 trouble code indicates a knock control system communication error.6
EXP-N013

CASE-031
, , , , , , . Active DTC: P0172 / P0087.6
GDI High-Pressure Fuel Pump (HPFP) internal seal leak.6 Fuel leaks directly into the engine oil via the mechanical drive of the pump, and is subsequently drawn back into the intake via the PCV system, causing highly negative fuel trims.6 Camshaft-driven HPFPs are unique to GDI/TGDI architectures.10 Low rail pressure triggers P0087.6
EXP-N014

CASE-033
–, –, –, –, –. Active DTC: P0300.6
GDI intake valve carbon sequestration.6 The porous carbon deposits on the intake valves soak up fuel during cold start, causing a transient lean misfire.6 Once the engine warms up, the fuel is released, causing a transient rich spike.6 This was widely recognized as a major GDI diagnostic challenge in the 2010s.10
EXP-N018

CASE-039
, , –, , –. Trims: .6
Hybrid vehicle cold catalyst strategy hang.6 Following an electric-to-ICE transition, the engine management system fails to exit the cold-start fast-light-off enrichment phase, hanging in open loop despite a warm coolant temperature ().6 Fully integrated hybrid powertrain diagnostic strategies are unique to the 2010s.5
EXP-N030
, , , , , , . Active DTC: P0171.6
Hybrid exhaust gas heat recovery system glycol leak.6 Coolant leaks into the exhaust system, poisoning the oxygen sensor.6 The sensor stuck low (perceived lean) drives the ECU trims positive, creating a physical rich condition.6 Integrated exhaust-coolant heat exchangers are modern technologies introduced in the 2010s to improve hybrid engine warm-up efficiency.5
CASE-009
, , , , . Standard E10 petrol calibration.6
High ethanol fuel blend (E10) combustion calibration.6 Standard E10 fuel calibration requires the ECU to adapt to a lower stoichiometric air-fuel ratio () compared to pure gasoline ().6 Widespread E10 mandates and corresponding ECU adaptation strategies were established in the 2010s.22
CASE-032
, , , , . No active DTCs.6
Turbocharger compressor seal leak allowing engine oil to soak into the intercooler.6 High hydrocarbons occur only under boost conditions ( at high load), while the idle remains perfectly clean.6 Boost-dependent oil ingestion diagnostics are typical of downsized TGDI architectures.10
CASE-034
, , , , . Active DTC: P0299.6
Turbocharger wastegate stuck open, preventing boost pressure from building.6 Mass airflow at  is severely low ( vs expected ), while the ECU adapts to maintain stoichiometry.6 Underboost trouble codes (P0299) are classic TGDI diagnostics.6
CASE-036
, , , , . Active DTC: P0171.6
GDI high-pressure injector tip deposits.6 Carbon buildup on the injector tip distorts the spray pattern, preventing proper atomization under engine load, causing localized lean conditions and rising fuel trims.6 Spray-guided GDI injector degradation is a modern diagnostic failure mode.10
CASE-037
, , , , , , . Active DTC: P0234.6
Turbocharged charge-pipe split post-compressor.6 Pressurized air leaks out under boost, causing the engine to run physically rich.6 High-pressure boost leak diagnostics with active overboost monitor (P0234) are typical of downsized TGDI architectures.6
CASE-038
, , , , , , . Active DTC: P0300.6
GDI common-rail fuel pressure drift.6 High-pressure rail drops to  (target ), causing poor fuel atomization and a severe lean misfire.6 Rail pressure sensor diagnostics and low-pressure common-rail misfire faults are unique to the GDI era.10
CASE-040
, , , , . Active DTC: P0234.6
Turbocharger blow-off valve (BOV) transient diaphragm leak.6 High hydrocarbons and transient rich spikes occur only during gear-shift throttle closures, while steady-state cruise remains stoichiometric.6 Transient boost release diagnostics are standard in modern TGDI platforms.10
CSV-113

CSV-114

CSV-129

CSV-130

EXT-211

EXT-212

EXT-238

EXT-239

case_019

case_020
: elevated up to , : up to , : elevated up to , calculated  up to . Active DTCs: P0401, P0411.6
These cases represent advanced emissions feedback loop failures typical of Euro 5 and Euro 6 vehicles.19 These include stuck-open EGR valves causing dilution-induced misfires at idle and continuous flow faults in Secondary Air Injection (SAI) valves, which are diagnosed using advanced ECU rationality checks.4

Synthesis of Cross-Decadal Diagnostic Strategies
The transition across these three diagnostic eras demonstrates a continuous expansion of the boundaries of engine control loop systems.3
In Era A, the diagnosis was primarily post-facto and focused on the tailpipe.3 Technicians utilized four-gas analyzers as standalone diagnostic benches, measuring tailpipe gas concentrations to manually deduce combustion anomalies, independent of the primitive onboard processors.3 The diagnostic resolution of this era was limited by the analog nature of its feedback loops and a lack of standardized communication protocols.3
In Era B, diagnostics shifted from external measurement to onboard, digital interpretation.4 The standardization of OBD-II and EOBD protocols over high-speed CAN buses shifted the analytical burden to the onboard controller.4 The ECU began continuously calculating short-term and long-term fuel trims to keep stoichiometry within a tight window, utilizing narrowband and early wideband sensors.6 This allowed for the identification of a wide range of common engine faults, such as vacuum leaks and catalyst degradation.6
In Era C, diagnostics transitioned into a highly integrated, model-based validation environment.10 The introduction of GDI, TGDI, and hybrid architectures created severe physical challenges, such as intake valve carbon sequestration and Low-Speed Pre-Ignition.6 Modern ECUs must validate a web of variables, monitoring high-pressure common rail fuel loops and differential backpressure across Gasoline Particulate Filters.6
Ultimately, this historical progression highlights the critical importance of a multi-dimensional diagnostic approach.3 When diagnosing modern, highly complex engine systems, relying on isolated trouble codes is no longer sufficient.3 By cross-examining actual tailpipe chemistry against the ECU's perceived parameters, technicians can identify sensor biases and "Truth-versus-Perception" gaps.6 This comprehensive strategy is essential for isolating root causes and ensuring the efficient operation of modern passenger vehicles.4
Works cited
The Benefits and Costs of the Clean Air Act 1990 to 2020 - Preliminary Draft Report - EPA, accessed on May 20, 2026, https://www.epa.gov/sites/default/files/2015-07/documents/may2010_2nd_prospective.pdf
Overview of the DOE Advanced Combustion Engine R&D Program - Department of Energy, accessed on May 20, 2026, https://www.energy.gov/sites/prod/files/2014/09/f18/ace_rd_overview_2014_amr.pdf
How Do I Know if My Car Is Obd2 Compliant? - Foxwell Diag, accessed on May 20, 2026, https://www.foxwelldiag.com/blogs/car-diagnostic/car-obd2-compliant
What Is OBDII? History of On-board Diagnostics (OBD) - Geotab, accessed on May 20, 2026, https://www.geotab.com/blog/obd-ii/
Global Networks and Competitive Strategic Alliances in the Automotive Industry. The Case of declining Europe. - IRIS-BOA - UniMiB, accessed on May 20, 2026, https://boa.unimib.it/retrieve/e39773b3-b109-35a3-e053-3a05fe0aac26/phd_unimib_700973.pdf
cases_petrol_master_v5.csv
How do I know whether my vehicle is OBD-II compliant? - Software, accessed on May 20, 2026, https://obdsoftware.my.site.com/s/article/how-do-i-know-whether-my-vehicle-is-obd-ii-compliant
How to Test an Oxygen Sensor: Step-by-Step Guide (DIY) - Blikai, accessed on May 20, 2026, https://www.blikai.com/blog/sensors/how-to-test-an-oxygen-sensor-step-by-step-guide-diy
Zissis Samaras - Concawe, accessed on May 20, 2026, https://www.concawe.eu/wp-content/uploads/2017/01/Concawe_Presentation_Samaras_Final.pdf
GASOLINE PARTICULATE FILTERS (GPFs) - BM Catalysts, accessed on May 20, 2026, https://bmcats.com/app/uploads/2024/05/0074_BMC_GPF_A4_4PP_-0524_web.pdf
What Are the Different Types of Fuel Injection Systems? - OnAllCylinders, accessed on May 20, 2026, https://www.onallcylinders.com/2025/03/19/what-are-the-different-types-of-fuel-injection-systems/
Two-Wheeled Urban Vehicles—A Review of Emissions Test Regulations and Literature - Semantic Scholar, accessed on May 20, 2026, https://pdfs.semanticscholar.org/523c/f7ce9be2e6cfde9397bb8604ac03ef75b496.pdf
How to Buy the Right O2 Sensor - eBay, accessed on May 20, 2026, https://www.ebay.com/motors/blog/diy/how-to-buy-o2-sensor
Since when is CAN bus mandatory for new vehicles? - Mechanics Stack Exchange, accessed on May 20, 2026, https://mechanics.stackexchange.com/questions/18770/since-when-is-can-bus-mandatory-for-new-vehicles
History of gasoline direct injection - F5R Team, accessed on May 20, 2026, https://f5r.eu/?history-of-gasoline-direct-injection
The Role of Oxygen Sensors in Modern Vehicles - IC Components, accessed on May 20, 2026, https://www.ic-components.com/blog/oxygen-sensor-guide-functionality,types,and-maintenance.jsp
Bosch Oxygen Sensor Overview and Applications | PDF - Scribd, accessed on May 20, 2026, https://www.scribd.com/doc/183660529/Bosch-Oxygen-Sensors
Code P1135 Toyota: A Case Study - In The Garage with CarParts.com, accessed on May 20, 2026, https://www.carparts.com/blog/code-p1135-toyota-a-case-study/
Gasoline particulate filter - Wikipedia, accessed on May 20, 2026, https://en.wikipedia.org/wiki/Gasoline_particulate_filter
Corning Celebrates its 1 Millionth Gasoline Particulate Filter, accessed on May 20, 2026, https://www.corning.com/worldwide/en/about-us/news-events/news-releases/2018/06/corning-celebrates-its-1-millionth-gasoline-particulate-filter.html
Gasoline direct injection - Bosch Mobility, accessed on May 20, 2026, https://www.bosch-mobility.com/en/solutions/powertrain/gasoline/gasoline-direct-injection/
Forté technical tips - The Gasoline Particulate Filter, accessed on May 20, 2026, https://www.forteuk.co.uk/news/forte-technical-tips-the-gasoline-particulate-filter/
Gasoline Particulate Filters - DieselNet, accessed on May 20, 2026, https://dieselnet.com/tech/gasoline_particulate_filters.php
(PDF) A Fuel Efficiency Horizon for U.S. Automobiles - ResearchGate, accessed on May 20, 2026, https://www.researchgate.net/publication/280229675_A_Fuel_Efficiency_Horizon_for_US_Automobiles
accessed on May 20, 2026, https://dieselnet.com/tech/gasoline_particulate_filters.php#:~:text=The%20Euro%206%20regulations%20set,WLTC%20test%20cycle%20(Euro%206c)
Population and Activity of Onroad Vehicles in MOVES3 (EPA-420-R-20-023, November 2020), accessed on May 20, 2026, https://www.epa.gov/sites/default/files/2020-11/documents/420r20023.pdf
