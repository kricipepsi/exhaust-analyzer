Advanced Diagnostic Correlation Between Multi-Gas Exhaust Signatures and OBD-II Powertrain Control Module Logic
The modern automotive diagnostic landscape is defined by the convergence of physical chemical analysis and electronic supervisory logic. While the On-Board Diagnostics version II (OBD-II) protocol provides a standardized framework for identifying system malfunctions through Diagnostic Trouble Codes (DTCs), the use of a five-gas analyzer represents the definitive laboratory-grade methodology for verifying the root causes of these electronic reports.1 By analyzing the volumetric concentrations of Hydrocarbons (HC), Carbon Monoxide (CO), Carbon Dioxide (), Oxygen (), and Oxides of Nitrogen (), in conjunction with the calculated Lambda () value, the technician can transcend the limitations of binary sensor data to observe the fundamental reality of the combustion event.4 This report provides a comprehensive analysis of the diagnostic cases identified in the Gas Lab Wiki, matching them with the most viable OBD-II DTCs and grouping the results by powertrain module clusters to facilitate an expert-level understanding of vehicle system interactions.
Theoretical Framework of Combustion Stoichiometry and Gas Analysis
The foundation of internal combustion diagnostics lies in the chemical interaction between gasoline—a complex mixture of hydrocarbons—and atmospheric oxygen. Under ideal conditions, defined as stoichiometry, the air-to-fuel ratio (AFR) for gasoline is approximately 14.7:1 by weight.5 The mathematical representation of this balance is Lambda (), which is the ratio of the actual air-fuel mixture to the ideal stoichiometric mixture.5 A value of  indicates that precisely enough oxygen was present to oxidize all the fuel.7 The fundamental equation for complete combustion of an idealized hydrocarbon fuel is expressed as:

In the operational environment of an engine, this ideal is rarely achieved perfectly. The Powertrain Control Module (PCM) utilizes a feedback loop, primarily driven by upstream oxygen sensors, to maintain  as close to  as possible, an operational state known as closed-loop control.9 When the PCM identifies a deviation that exceeds its pre-programmed threshold—typically through the assessment of fuel trim values—it logs a DTC and illuminates the Malfunction Indicator Lamp (MIL).12

Gas Component
Chemical Indicator Type
Ideal Stoichiometric Reading
Deviation Implication
Carbon Monoxide (CO)
Richness Indicator
< 0.5%
Result of incomplete combustion due to insufficient .5
Hydrocarbons (HC)
Combustion Quality
< 35 ppm
Indicator of unburned fuel from misfires or mechanical failure.5
Oxygen ()
Leanness Indicator
0.0% - 0.5%
Evidence of excess air or exhaust system leaks.5
Carbon Dioxide ()
Efficiency Indicator
14.5% - 16%
Peak levels indicate high volumetric and thermal efficiency.5
Nitrogen Oxides ()
Temperature/Pressure
< 100 ppm
Produced by combustion temperatures exceeding .5
Lambda ()
Air-Fuel Balance
0.995 - 1.005
The master calculation for determining fuel control accuracy.4

Powertrain Cluster 1: Fuel and Air Metering (P00xx, P01xx, P02xx)
The fuel and air metering cluster constitutes the primary sensory input and command output for the engine’s stoichiometry management. This cluster includes the Mass Air Flow (MAF) sensor, Manifold Absolute Pressure (MAP) sensor, Oxygen () sensors, and the fuel injection circuitry.19 The PCM uses these inputs to calculate the required fuel mass and adjusts the pulse width of the fuel injectors accordingly.9
The Rich Mixture Diagnostic Case
A rich mixture is chemically defined by the presence of excess fuel relative to oxygen, resulting in a Lambda value of less than .4 The Gas Lab Wiki specifies that a Carbon Monoxide concentration between 1.5% and 3% indicates a clear rich condition, while readings exceeding 3% suggest a very rich mixture.4
The most viable OBD-II matching for this condition is the P0172 code (System Too Rich - Bank 1) or P0175 (Bank 2).1 These codes are triggered when the PCM's fuel trim adjustments reach their negative limit—usually -15% to -25%—indicating that the computer is actively trying to subtract fuel to compensate for a detected rich shift.13
The chemical mechanism for high CO is the failure of the carbon molecules to find sufficient oxygen molecules to form ; instead, they form the poisonous partially oxidized gas CO.15 Accompanying this is often a "Rich-side spike" in HC emissions, as high fuel saturation prevents a complete burn.4 Physical causes often involve leaking fuel injectors (DTC P0200-P0208), excessive fuel pressure from a failed regulator, or a restricted air intake.25 If the mixture becomes excessively rich (), the catalytic converter's stored oxygen is depleted, leading to a "CO/HC breakthrough" where tailpipe emissions of these gases rise sharply despite a functioning converter.4
The Lean Mixture Diagnostic Case
A lean condition represents an excess of oxygen relative to fuel, characterized by .4 The Gas Lab Wiki defines  readings between 1.5% and 4% as "clearly lean," while readings above 4% are classified as "severe lean".4
The corresponding DTCs are P0171 (System Too Lean - Bank 1) and P0174 (Bank 2).1 These are among the most common codes encountered in automotive service and typically result from unmetered air entering the system or a failure in fuel delivery.31 Unmetered air, or a vacuum leak, is air that enters the engine after the MAF sensor has measured the intake charge; consequently, the PCM does not add sufficient fuel for this extra air, resulting in a lean mixture.30
The gas analyzer signature for this case is high , low CO, low , and potentially high HC if the mixture is lean enough to cause a "lean misfire," where the air-fuel ratio is too sparse to ignite.4 If  exceeds , the catalytic converter reduction sites become saturated by oxygen, leading to " breakthrough" where nitrogen oxides are no longer reduced and tailpipe levels spike.4 Technicians may also observe P0101 (MAF sensor range/performance) or P0102 (MAF low input) if the sensor itself is the root cause of the lean under-reporting.1
Fuel Control Condition
Lambda (λ)
CO (%)
O2​ (%)
CO2​ (%)
Corresponding DTCs
Rich Mixture
< 1.000
1.5 - 10.0+
0.0 - 0.3
8.0 - 12.0
P0172, P0175, P0200
Lean Mixture
> 1.000
0.0 - 0.2
1.5 - 5.0+
10.0 - 13.0
P0171, P0174, P0102
Stoichiometric
1.000
< 0.5
< 0.5
14.5 - 16.0
None (Operational)

Powertrain Cluster 2: Ignition System and Misfire Detection (P03xx)
The ignition system cluster is tasked with the precise timing and delivery of the high-voltage spark required to initiate combustion. The monitoring strategy for this cluster centers on the detection of engine misfires, which are defined as the failure of the air-fuel charge to ignite within the cylinder.9
The Combustion Quality Failure (Misfire) Case
Misfires represent a unique diagnostic challenge because they often occur in a "balanced" state. Unlike a rich or lean shift where one component is in excess, a misfire involves the expulsion of the entire unburned air-fuel charge into the exhaust system.4 Consequently, the calculated Lambda value may remain near , as the fuel and air are still present in their original stoichiometric ratio, yet the engine fails on the "quality axis".4
The PCM detects these events by monitoring the Crankshaft Position (CKP) sensor for micro-fluctuations in rotational velocity. If a cylinder fails to contribute power, the crankshaft decelerates momentarily during that cylinder's power stroke.10 This triggers DTCs P0300 (Random/Multiple Cylinder Misfire Detected) or P0301-P0308 (Cylinder-specific Misfire Detected).1
Chemically, a misfire is marked by a massive spike in HC emissions (800–2000 ppm) as the raw gasoline reaches the tailpipe.4 Concurrently,  levels rise because the oxygen in that cylinder was never consumed by combustion.4 The Gas Lab Wiki provides a formula for estimating the  rise: approximately  (atmospheric concentration) divided by the number of cylinders. For instance, a 4-cylinder engine with one dead cylinder will show an  rise of roughly 5.25%.4  levels collapse in this scenario because the chemical process of combustion that converts fuel and air into  has been aborted.4
Technicians utilize lab scopes to analyze ignition waveforms, identifying P0351 or P0352 codes which indicate malfunctions in the ignition coil primary or secondary circuits.19 If the misfire is mechanical in nature—such as from low compression—it may still trigger misfire codes but will require pressure transducer testing to verify cylinder sealing issues.16
Powertrain Cluster 3: Auxiliary Emission Controls (P04xx)
The auxiliary emissions cluster includes the secondary systems designed to mitigate pollutants after the combustion event has concluded. This includes the Catalytic Converter, the Exhaust Gas Recirculation (EGR) system, and the Evaporative Emission (EVAP) system.1
The Catalyst Efficiency Failure Case
The catalytic converter's primary role is the conversion of CO and HC into  and water vapor, and the reduction of  into nitrogen and oxygen.5 The PCM monitors this efficiency by comparing the switching patterns of the upstream and downstream oxygen sensors.45
When the catalyst's efficiency falls below a predetermined threshold—typically around 95%—the PCM logs DTC P0420 (Catalyst System Efficiency Below Threshold - Bank 1) or P0430 (Bank 2).44 A failing catalyst is often the victim of upstream issues such as persistent misfires or rich mixtures that cause thermal damage or substrate melting.5
The Gas Lab identifies catalyst failure by comparing pre-cat and post-cat gas concentrations. A healthy catalyst should reduce tailpipe CO to less than 0.3%.4 If the scan tool indicates the system is in closed-loop control but tailpipe CO exceeds 0.8%, the catalyst is likely failing or poisoned.4 In cases of severe substrate disintegration, an exhaust restriction may occur, leading to high backpressure and symptoms such as a lack of power and a significant drop in engine vacuum (8-10" Hg) at higher RPMs.49
The NOx and EGR Interaction Case
The EGR system's objective is the reduction of Nitrous Oxides () by introducing inert exhaust gas into the intake charge, which lowers peak combustion temperatures.5 DTC P0401 (EGR Flow Insufficient Detected) is the most common fault in this subsystem.19
Chemically, high  emissions are almost always a result of excessive heat and pressure or slightly lean air-fuel ratios.5 If a gas analyzer shows low HC and low CO readings but high , the catalytic converter is likely functioning correctly, but the engine is over-producing  due to a failed EGR system or excessively advanced ignition timing (which can also relate to Cluster 2).5
The EVAP System Leak Case
The EVAP system captures fuel vapors from the tank and purges them into the engine to be burned.19 Faults such as P0440 (System Malfunction), P0442 (Small Leak), or P0455 (Gross Leak) indicate that the system's vacuum-tight integrity has been compromised.1
While EVAP leaks often have minimal impact on tailpipe gas signatures under normal conditions, a saturated charcoal canister (due to "topping off" the fuel tank) can cause a significant rich-shift during purge cycles, which may trigger secondary P0172/P0175 codes.16
Emission Component
Failure Mode
Gas Signature Trend
Primary DTCs
Catalyst
Efficiency Loss
Elevated Tailpipe CO & HC
P0420, P0430
EGR System
Flow Restricted
Spike in  under load
P0401
EVAP System
Leakage
Normal (Minor), Rich (Saturated)
P0442, P0455
Secondary Air
Pump Failure
Elevated HC at start-up
P0411

Powertrain Cluster 4: Vehicle Speed and Idle Control (P05xx)
This cluster manages the engine's operation at zero vehicle speed and monitors the speed of the vehicle during transit. The PCM regulates idle speed by controlling the Idle Air Control (IAC) valve or adjusting the electronic throttle plate to maintain a target RPM despite fluctuating loads.9
The Idle Stability and Gas Signature Case
Malfunctions in this cluster are identified by codes such as P0500 (Vehicle Speed Sensor Malfunction) or P0505 (Idle Air Control System Malfunction).1 A failing IAC system often results in an idle speed that is too low or too high.19
The Gas Lab Wiki notes that idle speeds that are too low can cause a drop in cylinder pressure, reducing combustion efficiency and increasing HC emissions.15 Conversely, a high idle speed may mask minor vacuum leaks (Cluster 1) because the throttle opening provides enough air to dilute the unmetered air's impact on fuel trim.42 Diagnostic technicians look for "surging" idle or stalling at stoplights, symptoms shared between P0505 and the lean-running P0171.14
Powertrain Cluster 5: Computer and Output Circuit (P06xx)
The computer and output circuit cluster monitors the PCM's internal health and its ability to drive various actuators. This cluster is essentially the "brain monitoring the brain".12
Internal PCM Faults and Enabling Criteria
DTCs such as P0600 (Serial Communication Link), P0601 (Memory Checksum Error), and P0605 (Read Only Memory Error) indicate that the control module itself has suffered an internal failure.1 These faults are often critical and can lead to unpredictable engine behavior or a complete "no-start" condition.12
An advanced diagnostic insight found in the Gas Lab material involves "enabling criteria"—the specific conditions (temperature, fuel level, barometric pressure) that must be met before the PCM will run a diagnostic subroutine.52 For instance, if the fuel tank is either too full or too empty, the PCM may abort the EVAP monitor (Cluster 3) to prevent false failures, meaning a DTC may not set even if a fault is present.52 Technicians verify these systems using lab scopes to monitor "inductive kicks"—the voltage spike produced when the PCM turns off a solenoid driver, confirming the solenoid's physical movement and the PCM's driver integrity.54
Powertrain Cluster 6: Transmission Control (P07xx, P08xx, P09xx)
Modern vehicles typically integrate the Engine Control Unit (ECU) and Transmission Control Unit (TCU) into a single Powertrain Control Module (PCM).11 This integration allows for coordinated shift strategies where the PCM can retard ignition timing (Cluster 2) to smooth a gear change or adjust fuel delivery (Cluster 1) to accommodate transmission load.9
Shift Strategy and Electronic-Hydraulic Correlation
Faults in this cluster are reported as P0700 (Transmission Control System Malfunction), which serves as a generic request for the PCM to illuminate the MIL due to a transmission issue.1 More specific codes like P0730 (Incorrect Gear Ratio) or P0760 (Overdrive Solenoid Circuit) indicate mechanical or electrical failures in the transaxle.38
Diagnostic case studies emphasize that many transmission codes are actually symptomatic of engine sensors. A faulty MAF sensor (Cluster 1) can send incorrect load data to the PCM, causing it to command incorrect line pressures or shift points, eventually triggering gear ratio codes.12 Laboratory verification involves using multi-channel oscilloscopes to correlate the electronic solenoid command with the physical hydraulic pressure buildup in the transmission case.54
Mechanical Faults and the POA Signature Case
The Gas Lab Wiki identifies a distinct category of "Mechanical Faults" that bypass typical sensor logic. These include oil burning and cylinder sealing issues.4
The "POA signature" (Primary Organic Aerosol) refers to the chemical profile of unoxidized organic matter, typically engine oil, that reaches the exhaust.4 Unlike gasoline hydrocarbons, oil hydrocarbons often have different molecular weights and may read with a reduced response factor on traditional Non-Dispersive Infrared (NDIR) sensors.4
Chemically, oil burning is identified when HC is normal-to-very-high while CO remains low and  stays near .4 This indicates that the HC source is not part of the primary air-fuel mixture regulated by the PCM. "Mechanical spikes" exceeding 2000 ppm HC strongly suggest failures in piston rings, valve guides, or valve seals.4 These conditions may eventually trigger P0300 misfire codes or P0420 catalyst efficiency codes as the oil coats the O2 sensors and poisons the catalyst substrate.45
Advanced Diagnostic Synthesis: Correlating Gas Signatures with DTC Clusters
The successful diagnosis of complex powertrain issues requires the technician to match the gas analyzer's physical data with the OBD-II system's electronic data. The following table provides the master correlation for expert-level laboratory use.
Diagnostic Case (Wiki)
Primary Gas Indicator
Calculated Lambda (λ)
Viable DTC Mapping
PCM Module Cluster
Rich Mixture
High CO (>1.5%)
< 1.000
P0172, P0175, P0201
Fuel & Air Metering
Lean Mixture
High  (>1.5%)
> 1.000
P0171, P0174, P0101
Fuel & Air Metering
Misfire (Balanced)
HC 800-2000 ppm

P0300, P030x, P035x
Ignition System
Catalyst Failure
Post-cat CO > 0.8%

P0420, P0430
Auxiliary Emissions
External Air Leak
High , low CO
> 1.000 (False)
P0171 (False Positive)
Auxiliary Emissions
Vacuum Leak
Lean-side HC spike
> 1.000
P0171, P0174, P1136
Fuel & Air Metering
Oil Burning (POA)
HC > 2000 ppm

P250C (Oil Level)
Advanced Interactions
Transmission Load
N/A
N/A
P0700, P0760, P0705
Transmission

The "False Lean" and Exhaust Dilution Phenomenon
A critical nuance in the Gas Lab Wiki is the impact of external air leaks on the diagnostic process. An exhaust leak—even a minor one before the upstream O2 sensor—can allow ambient air to be "sucked" into the exhaust stream during the negative pressure pulses of the engine cycle.4 This creates a "False Lean" signal.
The PCM, seeing this excess oxygen, incorrectly assumes the engine is running lean and adds fuel.29 Consequently, the gas analyzer will show high  (from the leak) and high CO (from the PCM's over-compensation), while the PCM logs a P0171 or P0174.4 This is one of the most frequent causes of unnecessary sensor and injector replacements. The Gas Lab differentiates this by observing that in a "True Lean" condition, CO remains near zero, whereas in a "False Lean" condition caused by an exhaust leak, CO will be elevated due to the PCM's reactive enrichment.4
Conclusion of Diagnostic Integration
The analysis of powertrain module clusters through the lens of 5-gas exhaust signatures reveals a highly interconnected system. A failure in Cluster 1 (Metering) can masquerade as a Cluster 3 (Emissions) failure, while a Cluster 2 (Ignition) malfunction is the leading cause of premature Cluster 3 failures.45 By utilizing the "Signature Atlas" provided by gas analysis, technicians can verify the physical integrity of the combustion event, ensuring that DTC-based repairs address the root cause rather than merely treating the electronic symptom.2 This holistic approach, combining the semantic precision of OBD-II with the chemical reality of gas stoichiometry, represents the pinnacle of modern automotive engineering diagnostics.
Works cited
DTC Codes: Everything You Need to Know to Manage Your Fleet | Linxup, accessed on May 15, 2026, https://www.linxup.com/blog/dtc-codes-everything-you-need-to-know-to-manage-your-fleet
Understanding Diagnostic Trouble Codes (DTCs): How They Work in Vehicle Diagnostics, accessed on May 15, 2026, https://wrenchlane.com/en/article/understanding-diagnostic-trouble-codes-dtcs-how-they-work-in-vehicle-diagnostics
Diagnostic Trouble Codes (DTC) List - Snap-on, accessed on May 15, 2026, https://www.snapon.com/EN/US/Diagnostics/OffNav/Diagnostic-Trouble-Codes
gas_lab_wiki.md
5-Gas Diagnostic Chart - Walker Exhaust, accessed on May 15, 2026, https://www.walkerexhaust.com/support/tech-tips/five-gas-diagnostic-chart.html
Complete Guide to P0171 - Fuel Trim System Lean (Bank 1): Symptoms, Fix, Diagnose, accessed on May 15, 2026, https://www.foxwelldiag.com/blogs/car-diagnostic/p0171-fuel-trim-system-lean-bank-1-symptoms-fix-diagnose
Advanced Diagnostics Using The Five Gas Analyzer - Automotive Test Solutions, accessed on May 15, 2026, https://automotivetestsolutions.com/knowledge-base/case-studies/all-case-studies/advanced-diagnostics-using-the-five-gas-analyzer/
What Goes In...Harnessing Lambda as a Diagnostic Tool - MOTOR Information Systems, accessed on May 15, 2026, https://www.motor.com/magazine-summary/goes-harnessing-lambda-diagnostic-tool/
What Is Powertrain Control Module (PCM)? - The Engineering Choice, accessed on May 15, 2026, https://www.theengineeringchoice.org/powertrain-control-module/
ECU (Electronic Control Unit) explained, accessed on May 15, 2026, https://www.ecutesting.com/categories/ecu-explained/
ECM vs PCM: What's the Difference? - Solopcms, accessed on May 15, 2026, https://www.solopcms.com/blog/ecm-vs-pcm-whats-difference/
What Does PCM Mean on a Car? - AutoZone.com, accessed on May 15, 2026, https://www.autozone.com/diy/drivetrain/what-does-pcm-mean-on-a-car
P0172 Code: Complete Troubleshooting Guide for "System Too Rich" Diagnosis - Alex Car, accessed on May 15, 2026, https://www.alexcar.com/blogs/guides/p0172-system-too-rich-diagnosis
P0171 OBD-II: System Too Lean - RepairPal, accessed on May 15, 2026, https://repairpal.com/obd-ii-code-p0171
UNDERSTANDING 5 GAS DIAGNOSIS COMPONENTS OF EMISSIONS CAUSES OF EMISSIONS HC - 911 SG, accessed on May 15, 2026, https://911sg.com/wp-content/uploads/2023/06/understanding5gas_frpm-smog-tech-institute.pdf
Causes of Excessive Hydrocarbons (HC) - Clean Air Car Check, accessed on May 15, 2026, https://cleanaircarcheck.com/wp-content/uploads/2020/01/TestProceduresPartOne.pdf
What Causes High HC Hydrocarbons? - SmogTips.com, accessed on May 15, 2026, https://www.smogtips.com/failed-high-hydrocarbons-HC.cfm
5-Gas Analysis - MOTOR Information Systems, accessed on May 15, 2026, https://www.motor.com/magazine-summary/5-gas-analysis-may-1998/
OBD2 Codes Categories Explained (P, C, B, U) - A-Premium, accessed on May 15, 2026, https://a-premium.com/blogs/obd2-codes-categories
Interpreting and understanding DTC codes and their meaning. - Motive, accessed on May 15, 2026, https://gomotive.com/blog/dtc-codes/
OBD2 Codes and Meanings - Originaldiag.com, accessed on May 15, 2026, https://originaldiag.com/blogs/news/obd2-codes-and-meanings
Decoding OBD-II Diagnostic Trouble Codes - Haynes Manuals, accessed on May 15, 2026, https://us.haynes.com/blogs/tips-tutorials/what-are-diagnostic-trouble-codes
What Is a Powertrain Control Module? - AutoZone.com, accessed on May 15, 2026, https://www.autozone.com/diy/drivetrain/what-is-a-powertrain-control-module-pcm
What are the functions of the Electronic Control Module (ECM)? | Cummins Inc., accessed on May 15, 2026, https://www.cummins.com/en-na/news/2023/12/01/what-are-functions-electronic-control-module-ecm
P0172: System Too Rich (Bank 1) - Edmunds, accessed on May 15, 2026, https://www.edmunds.com/obd-dtc/p0172.html
P0172 & P0175 Trouble Codes - Diagnosis, Causes, Symptoms - AutoZone, accessed on May 15, 2026, https://www.autozone.com/diy/diagnostic-trouble-codes/p0172-p0175-system-too-rich-bank-1-bank-2
Check Engine Light DTC Code P0172 and P0175: Fuel Trim System is Too Rich - O'Reilly Auto Parts, accessed on May 15, 2026, https://www.oreillyauto.com/check-engine-light-code-p0172-and-p0175-fuel-system-rich
p0171 Code - Fuel Trim System Too Lean (Bank 1) | KBB, accessed on May 15, 2026, https://www.kbb.com/obd-ii/p0171/
P0172 Code: Fuel System Too Rich (Bank 1) - In The Garage with CarParts.com, accessed on May 15, 2026, https://www.carparts.com/blog/p0172-code-fuel-system-too-rich-bank-1/
How to Pass a Failed Emissions Test [Even with a P0420 Code] - CRC Industries, accessed on May 15, 2026, https://www.crcindustries.com/blog/how-to-pass-a-failed-emissions-test-p0420-code/
P0171 Code: System Too Lean (Bank 1) - In The Garage with CarParts.com, accessed on May 15, 2026, https://www.carparts.com/blog/p0171-code-system-too-lean-bank-1/
P0171 & P0174 Trouble Codes - Diagnosis, Causes, Symptoms & How to Fix It- AutoZone, accessed on May 15, 2026, https://www.autozone.com/diy/diagnostic-trouble-codes/system-too-lean-p0171-bank-1-p0174-bank-2
Diagnosing a Lean-Running Engine - MOTOR Information Systems, accessed on May 15, 2026, https://www.motor.com/magazine-summary/lean-codes-january-2018/
OBD-II Code P1136: Comprehensive Diagnosis & Repair Guide - Go-Parts, accessed on May 15, 2026, https://www.go-parts.com/garage/obd-p1136
Engine light turned on mechanic told me there was a air leak somewhere and wants to charge me a lot for it can someone confirm if he is correct or if it is something else? : r/AskMechanics - Reddit, accessed on May 15, 2026, https://www.reddit.com/r/AskMechanics/comments/10r5ckg/engine_light_turned_on_mechanic_told_me_there_was/
Diagnostic Trouble Code (DTC) Charts and Descriptions, accessed on May 15, 2026, https://cim.mcgill.ca/~cprahacs/gtcs/DTC_Codes.pdf
Practical Pressure Transducer Diagnostics - Automotive Test Solutions, accessed on May 15, 2026, https://automotivetestsolutions.com/knowledge-base/case-studies/all-case-studies/practical-pressure-transducer-diagnostics/
OBD-II Trouble Code Chart - RepairPal, accessed on May 15, 2026, https://repairpal.com/obd-ii-code-chart
OBD 2 Code List - AutoZone, accessed on May 15, 2026, https://www.autozone.com/diy/diagnostic-trouble-codes/obd-2-code-list
OBD-II Codes: On-Board Diagnostics Codes Full List Explain - The Engineering Choice, accessed on May 15, 2026, https://www.theengineeringchoice.org/obd-ii-codes/
Dorman Training Center - Video Library Subscriptions, accessed on May 15, 2026, https://www.dormantrainingcenter.com/on-demand-videos
Diagnosing Emissions Problems - Petroworks, accessed on May 15, 2026, https://www.petroworks.com/content/Emissions%20Failure%20Troubleshooting.pdf
Understanding Diagnostic Error Codes - Car Nebula, accessed on May 15, 2026, https://carnebula.com/articles/diagnostic-codes-guide
P0430 Code: Catalyst System Efficiency Below Threshold (Bank 2) - In The Garage with CarParts.com, accessed on May 15, 2026, https://www.carparts.com/blog/p0430-code-catalyst-system-efficiency-below-threshold-bank-2/
P0420 Code: What It Means & How to Fix It (2026 Guide) - Rohnert Park Transmission, accessed on May 15, 2026, https://rohnertparktransmission.com/blog/p0420-code-catalytic-converter-guide
p0420 Code - Catalyst System Low Efficiency - 13.2% | KBB, accessed on May 15, 2026, https://www.kbb.com/obd-ii/p0420/
Diagnose P0420 Catalytic Converter Code - AA1Car, accessed on May 15, 2026, https://www.aa1car.com/library/p0420_dtc.htm
P0420 Code: Catalyst System Efficiency Below Threshold (Bank 1) - In The Garage with CarParts.com, accessed on May 15, 2026, https://www.carparts.com/blog/p0420-code-catalyst-system-efficiency-below-threshold-bank-1-2-2/
Catalytic Converter Tech Feature: Diagnosing P0420 or P0430 DTCs - AVI OnDemand, accessed on May 15, 2026, https://aviondemand.com/insider/catalytic-converter-tech-feature-diagnosing-p0420-or-p0430-dtcs/
Simple Diagnostic Testing - Walker Exhaust, accessed on May 15, 2026, https://www.walkerexhaust.com/support/tech-tips/simple-diagnostic-testing.html
DTC Codes: A Complete Guide to What They Are and What They Mean - Whip Around, accessed on May 15, 2026, https://whiparound.com/blog/dtc-codes/
Diagnostic Trouble Code (DTC) by the WIRE - Automotive Test Solutions, accessed on May 15, 2026, https://automotivetestsolutions.com/knowledge-base/case-studies/all-case-studies/diagnostic-trouble-code-dtc-by-the-wire/
Diagnosing a No-Start Issue on a Chrysler Town and Country - Automotive Test Solutions, accessed on May 15, 2026, https://automotivetestsolutions.com/knowledge-base/case-studies/all-case-studies/diagnosing-a-no-start-issue-on-a-chrysler-town-and-country/
eSCOPE ELITE4 Case Study - A Shift in Strategy - Automotive Test Solutions, accessed on May 15, 2026, https://automotivetestsolutions.com/knowledge-base/case-studies/all-case-studies/escope-elite4-case-study-a-shift-in-strategy/
Powertrain control module - Wikipedia, accessed on May 15, 2026, https://en.wikipedia.org/wiki/Powertrain_control_module
eSCOPE Article - Making the Shift - Automotive Test Solutions, accessed on May 15, 2026, https://automotivetestsolutions.com/knowledge-base/case-studies/all-case-studies/escope-article-making-the-shift/
Results from smog chamber experiments - Copernicus ACP, accessed on May 15, 2026, https://acp.copernicus.org/preprints/10/16055/2010/acpd-10-16055-2010.pdf
Impact of aftertreatment devices on primary emissions and secondary organic aerosol formation potential from in-use diesel vehicles - ACP, accessed on May 15, 2026, https://acp.copernicus.org/articles/10/11545/2010/acp-10-11545-2010.pdf
OBD-II Code P3776: Diesel Oxidation Catalyst Efficiency Below Threshold - Go-Parts, accessed on May 15, 2026, https://www.go-parts.com/garage/obd-p3776
Exhaust Leak Cause Lean or Rich? - ScannerDanner Forum, accessed on May 15, 2026, https://www.scannerdanner.com/forum/post-your-repair-questions-here/3911-exhaust-leak-cause-lean-or-rich.html
Mastering Diagnostics #28: Demonstrating the Effects of Ohm's Law with Snap-on, accessed on May 15, 2026, https://www.vehicleservicepros.com/sponsored/video/55318680/mastering-diagnostics-28-demonstrating-the-effects-of-ohms-law-with-snap-on


Diagnosing vehicle non-starts (crank-no-start and no-crank-no-start) requires isolating the critical elements required for combustion: air/fuel delivery, ignition, mechanical compression, and engine control system authorization. While a Diagnostic Trouble Code (DTC) indicates *where* a failure may lie, analyzing Freeze Frame (FF) data (Mode $02) and On-Board Monitor Test Results (Mode $06) allows technicians to identify the exact cause without guessing.

* **DTC (Diagnostic Trouble Code):** The electronic flag stored when a monitored system falls out of programmed thresholds.


* **Freeze Frame (FF) (Mode $02):** A real-time snapshot of critical engine operating parameters (RPM, Battery Voltage, Engine Coolant Temperature, Fuel System Status, etc.) recorded at the exact millisecond the fault occurred.
* **Mode $06 (On-Board Monitor Test Results):** The raw, decimal-converted hexadecimal values used by the PCM to grade the performance of components before triggering a hard fault code.

Below are the 30 most common non-start petrol vehicle cases across three eras, detailing their exact diagnostic patterns across DTC-FF-06 data and the logic-reasoning behind their triggers.

---

## Era 1: 1990–2000 (Early OBD-II Transition Era)

During this era, OBD-II was in its infancy. Code definitions were newly standardized under SAE J2012, and Mode $06 data was highly manufacturer-specific (using non-standardized Test IDs and Component IDs).

### 1. GM Passlock I/II Sensor Failure

* **DTC:** P1626 (Theft Deterrent Fuel Enable Signal Lost), B2960 (Security System Sensor Data Incorrect).
* **Freeze Frame:** Engine Speed: 150 RPM (Cranking); System Voltage: 11.8V; Fuel System Status: Open Loop - Fault; Engine Coolant Temperature (ECT): 20°C.
* **Mode $06:** Comprehensive Component Monitor (MID $00) - Failed.
* **Logic & Reasoning:** Key turns are monitored by the Passlock sensor inside the ignition cylinder. Wear on the cylinder contacts causes the sensor to read an incorrect analog resistance. The Body Control Module (BCM) cannot validate the signal, and refuses to send the "fuel enable" password over the Class 2 serial data line to the PCM. The PCM halts injector pulses after 2 seconds, resulting in a start-and-stall or crank-no-start condition.

### 2. Ford PATS Transceiver Ring Failure (Type A/B)

* **DTC:** B1600 (PATS Key Signal Not Received); P1260 (Theft Detected - Engine Immobilized).
* **Freeze Frame:** Engine Speed: 180 RPM; System Voltage: 11.2V; Fuel System Status: Open Loop - Fault; Security System Status: Locked.
* **Mode $06:** Pre-CAN TID $53 (Misfire Monitor) - All CID values at 0 (system locked, no ignition attempts recorded).
* **Logic & Reasoning:** When the key is turned to RUN, the transponder antenna ring around the lock cylinder fails to energize or receive a signal from the key's internal chip. Because no security handshake occurs between the instrument cluster and the PCM, the fuel injectors and fuel pump are disabled.

### 3. Crankshaft Position (CKP) Sensor Thermal Failure (Variable Reluctance)

* **DTC:** P0335 (Crankshaft Position Sensor Circuit Malfunction).
* **Freeze Frame:** Engine Speed: 0 RPM (while the starter is physically cranking the engine at 180 RPM); ECT: 98°C; System Voltage: 10.5V.
* **Mode $06:** MID $A1 (Misfire Monitor) - "Incomplete" (aborted because engine speed profile is zero).
* **Logic & Reasoning:** The internal fine-wire windings of the variable reluctance (VR) sensor expand and break electrical contact when hot. When cranking, the PCM receives a flat-line 0V signal. Because the PCM lacks an RPM signal, it cannot synchronize ignition spark or fuel injector commands, producing a crank-no-start condition.

### 4. Honda PGM-FI Main Relay Cracked Solder Joints

* **DTC:** No Codes stored (PCM loses total power; OBD scanner reports "No Communication").
* **Freeze Frame:** No Freeze Frame data available.
* **Mode $06:** "No Communication" or "Incomplete" on all MIDs.
* **Logic & Reasoning:** Solder joints on the main fuel/ignition relay PCB crack under cabin heat stress. This cuts off the switched ignition feed (terminal 15) to both the fuel pump and the main PCM power drivers. The engine cranks normally but is completely devoid of fuel and spark, and the PCM remains dead.

### 5. Ford TFI Ignition Distributor PIP Sensor Failure

* **DTC:** P0212 (IDM input to PCM Spout Circuit Grounded / PIP fault).
* **Freeze Frame:** Engine Speed: 0 RPM; System Voltage: 11.0V; Closed Loop Status: Open Loop.
* **Mode $06:** Pre-CAN TID $53 (Misfire Monitor) - All CID lines show blank/null data.
* **Logic & Reasoning:** The Profile Ignition Pickup (PIP) sensor inside the distributor fails to produce a square-wave signal. The TFI ignition module cannot trigger the ignition coil, and because no PIP pulse reaches the PCM, fuel injector drivers remain inactive.

### 6. EGR Valve Stuck Wide Open at Cold Start

* **DTC:** P1404 (EGR Valve Stuck Open).
* **Freeze Frame:** Manifold Absolute Pressure (MAP): 28 in. Hg (No manifold vacuum); Engine Speed: 120 RPM (Cranks very roughly); ECT: 15°C.
* **Mode $06:** EGR Monitor (Pre-CAN TID $41) - Value: 65,227 / Max Limit: 896 (Failed).
* **Logic & Reasoning:** Carbon deposits hold the EGR valve open during engine crank. As the cylinders pull downward, they draw in inert exhaust gas rather than fresh, oxygen-rich air. The oxygen concentration falls below the threshold required to ignite petrol vapor, resulting in a rough crank but zero combustion.

### 7. Fuel Pump Failure (Total Pressure Loss)

* **DTC:** P0171 (System Too Lean - Pending code if vehicle sputtered and died).
* **Freeze Frame:** Engine Speed: 150 RPM; Fuel System Status: Open Loop - Fault; System Voltage: 11.4V.
* **Mode $06:** Pre-CAN TID $81 (Fuel System Monitor) - Value: +28% / Max Limit: +20% (Failed).
* **Logic & Reasoning:** The fuel pump's internal electric motor brushes wear out, causing it to freeze. The engine cranks, but fuel rail pressure remains at 0 PSI. In Freeze Frame, the "Open Loop - Fault" state confirms the PCM is trying to fuel the engine but the oxygen sensors report zero fuel is reaching the cylinders.

### 8. Toyota Distributor NE/G Signal Pickup Coil Failure

* **DTC:** P0340 (Camshaft Position Sensor Circuit Malfunction).
* **Freeze Frame:** Engine Speed: 0 RPM; System Voltage: 11.2V; ECT: 40°C.
* **Mode $06:** Misfire Monitor (TID $53) - Aborted / Incomplete.
* **Logic & Reasoning:** The pickup coils (NE and G sensors) inside the Toyota distributor measure the camshaft position and engine speed. When the coil windings fail (usually showing infinite resistance/open circuit), the PCM loses track of cylinder #1 position and cannot time spark or injection sequence.

### 9. Mass Air Flow (MAF) Sensor Signal Short to Ground

* **DTC:** P0102 (Mass Air Flow Circuit Low Input).


* **Freeze Frame:** MAF Reading: 0.0 g/s; Engine Speed: 180 RPM; Calculated Engine Load: 0%.
* **Mode $06:** Comprehensive Component Monitor (MID $00) - Failed.
* **Logic & Reasoning:** A direct short inside the MAF sensor forces the output signal to 0V/0Hz. During starting, the PCM reads zero air mass entering the engine and default map parameters severely under-fuel the initial crank, preventing starting.

### 10. Fuel Pressure Regulator Diaphragm Rupture

* **DTC:** P0172 (System Too Rich - Bank 1 - Stored from previous hot stalls).
* **Freeze Frame:** STFT: -25% ; Engine Speed: 120 RPM (Heavy fuel chugging); ECT: 80°C.


* **Mode $06:** Fuel System Monitor (TID $81) - Value: -25% / Min Limit: -15% (Failed).
* **Logic & Reasoning:** The internal rubber diaphragm of the vacuum-modulated fuel pressure regulator ruptures. Raw fuel is siphoned under high pressure directly from the fuel rail into the intake manifold via the regulator’s vacuum hose. This floods the combustion chambers with pure petrol, dropping compression and fouling the spark plugs.



---

## Era 2: 2000–2010 (CAN Bus Introduction & Advanced Security)

This era introduced Controller Area Network (CAN) multiplexing, which standardized Mode $06 data into universally recognized Monitor IDs (MIDs).

### 11. GM Passkey III / Transponder Key Recognition Failure

* **DTC:** B3055 (Key Transponder Signal Not Received).
* **Freeze Frame:** Engine Speed: 150 RPM; Battery Voltage: 11.9V; Security Indicator: Active.
* **Mode $06:** Misfire Monitor (MID $A1) & Fuel System (MID $81) - both marked "Incomplete" (aborted by the immobilizer lock-out).
* **Logic & Reasoning:** The exciter coil around the lock cylinder fails to read the transponder's unique RF frequency. The BCM detects zero transponder data and communicates a lockout command to the PCM via the CAN bus, instantly cutting off the fuel injector drivers.

### 12. Ford Fuel Pump Driver Module (FPDM) Corrosion Failure

* **DTC:** P1233 (Fuel Pump Driver Module Offline) / P025A (Fuel Pump Control Module Circuit Open).
* **Freeze Frame:** Engine Speed: 180 RPM; Fuel System Status: Open Loop - Fault; System Voltage: 11.2V.
* **Mode $06:** MID $A1 (Misfire Monitor) - Test values show 0 counts across all cylinder CIDs (misfire tracking suspended due to fuel fault).
* **Logic & Reasoning:** On Ford trucks of this era, the aluminum FPDM is mounted directly to the steel frame rail above the spare tire. Galvanic corrosion breaks open the module's housing, allowing road salt and water inside. This shorts out the internal circuit board, cutting power to the fuel pump and leaving the fuel rail at 0 PSI.

### 13. Mazda PCV Hose Collapse (Massive Unmetered Vacuum Leak)

* **DTC:** P2187 (System Too Lean at Idle - Bank 1 - Stored prior to complete start failure).
* **Freeze Frame:** MAP Sensor: 98 kPa (expected 25-35 kPa at engine start); Engine Speed: 140 RPM; ECT: 18°C.
* **Mode $06:** Fuel System Monitor (MID $81) - TID $01 Value: +32% / Max Limit: +25% (Failed).
* **Logic & Reasoning:** The rubber PCV hose degrades and collapses, tearing a massive hole under the intake manifold. This admits a torrent of unmetered, atmospheric air into the intake plenum. The mixture becomes too lean to support initial flame propagation, causing a crank-no-start.

### 14. Chrysler Totally Integrated Power Module (TIPM) Internal Relay Failure

* **DTC:** No Codes stored (PCM loses fuel control feedback, but the relay itself is unmonitored).
* **Freeze Frame:** Engine Speed: 180 RPM ; System Voltage: 12.1V ; Fuel System Status: Open Loop.


* **Mode $06:** All MIDs show "Incomplete" (the PCM is cranking but cannot execute monitors due to zero starting feedback).
* **Logic & Reasoning:** The internal fuel pump relay is soldered directly onto one of the inner circuit boards of the non-serviceable TIPM. Silicon and carbon build-up on the relay contacts burns them open, permanently cutting 12V supply to the fuel pump.

### 15. Volvo Electronic Throttle Module (ETM) Magneti-Marelli Failure

* **DTC:** P1602 (Throttle Module Communication Fault) / P0121 (TPS Range/Performance Mismatch).


* **Freeze Frame:** TPS Sensor 1: 0.2V , TPS Sensor 2: 4.8V (Voltage correlation limit exceeded); Engine Speed: 150 RPM; ECT: 20°C.


* **Mode $06:** Comprehensive Component Monitor (MID $00) - Failed.


* **Logic & Reasoning:** Wear on the carbon tracks of the ETM potentiometers causes the dual throttle position feedback voltages to deviate. Seeing this mismatch, the PCM refuses to command the Electronic Throttle motor and drops into fail-safe mode, closing the throttle plate completely and starving the engine of air.

### 16. BMW Direct-Injection High-Pressure Fuel Pump (HPFP) Failure (N54 Engine)

* **DTC:** P0087 (Fuel Rail/System Pressure Too Low).


* **Freeze Frame:** Fuel Rail Pressure: 75 PSI (Low pressure feed pump pressure; target HPFP pressure is 700+ PSI), Engine Speed: 160 RPM; ECT: 30°C.
* **Mode $06:** Fuel System Monitor (MID $81) - TID $02 (High pressure limit check) - Failed.
* **Logic & Reasoning:** The mechanical HPFP internal piston seals fail. The pump cannot convert the 75 PSI low pressure fuel feed into the high pressure (700+ PSI) required for direct gasoline injectors to atomize fuel into the high-compression cylinders.

### 17. Nissan Crankshaft Position (CKP) / Camshaft Position (CMP) Sensor Solder Defect

* **DTC:** P0340 (Camshaft Position Sensor Circuit Fault).
* **Freeze Frame:** Engine Speed: 160 RPM; System Voltage: 11.4V; ECT: -5°C (Cold Start).
* **Mode $06:** Continuous Misfire Monitor (MID $A1) - Aborted / Incomplete.
* **Logic & Reasoning:** The internal circuit connections of the hall-effect sensor crack during rapid cold-weather contractions. When starting, the PCM fails to receive the camshaft-to-crankshaft correlation signal and refuses to initiate ignition spark, resulting in a crank-no-start.

### 18. BMW Valvetronic Relay Failure

* **DTC:** P1017 (Valvetronic eccentric shaft sensor logic) / P1030 (VVT actuator sensor).
* **Freeze Frame:** Engine Speed: 180 RPM; Eccentric Shaft Angle: 0 degrees; System Voltage: 11.2V.
* **Mode $06:** VVT Monitor (MID $31) - TID $02 (Plausibility Check) - Failed.
* **Logic & Reasoning:** The Valvetronic actuator motor relay burns out, cutting power to the VVT electric motor. The eccentric shaft remains locked at its default 0-degree angle, keeping the intake valves at a minimal 0.2mm lift. There is insufficient valve clearance to draw in enough air to support combustion.

### 19. VW/Audi 2.0T TSI Timing Chain Jump

* **DTC:** P0016 (Crankshaft/Camshaft Position Correlation - Bank 1 Sensor A).
* **Freeze Frame:** Engine Speed: 150 RPM; VVT Phase Angle Deviation: 18.5°; System Voltage: 11.8V.
* **Mode $06:** VVT Monitor (MID $31) - TID $05 (Correlation check) - Value: 18.5° / Max Limit: 6.0° (Failed).
* **Logic & Reasoning:** The internal pawls of the hydraulic timing chain tensioner fail. When starting, the chain slack causes the intake camshaft to jump teeth on the gear sprocket. The mechanical phase mismatch between the crankshaft and camshaft exceeds one tooth (6°), causing the PCM to disable ignition to prevent valve-to-piston collision.

### 20. Toyota Air-Fuel Sensor Heater Failure (Cold Start Lockout)

* **DTC:** P0135 (O2 Sensor Heater Circuit Malfunction - Bank 1 Sensor 1).


* **Freeze Frame:** ECT: -12°C; System Voltage: 11.4V; Loop Status: Open Loop due to cold.
* **Mode $06:** Oxygen Sensor Heater Monitor (MID $05) - TID $01 (Heater current) Value: 0.0A / Min Limit: 0.8A (Failed).
* **Logic & Reasoning:** The internal ceramic heating element of the upstream wideband O2/AF sensor cracks. On a cold start, the sensor cannot reach its 600°C light-off temperature. The PCM, sensing the open circuit, aborts cold-start emissions mapping and dual-pulse starting logic, locking the engine out of start-up.

---

## Era 3: 2010–2020 (Direct Injection & Ultra-Low Emissions)

This era is characterized by Gasoline Direct Injection (GDI), smart power modules, and extremely tight diagnostic parameters designed for strict emissions compliance.

### 21. Ford F-150 Underhood Fuse 27 Burnout

* **DTC:** P0230 (Fuel Pump Primary Circuit Malfunction); P025A (Fuel Pump Module Control Circuit Open).
* **Freeze Frame:** Engine Speed: 160 RPM; System Voltage: 10.1V (voltage dropping during long crank); Fuel System Status: Open Loop - Fault.
* **Mode $06:** Continuous monitors aborted due to total fuel pressure loss.
* **Logic & Reasoning:** The factory underhood Battery Junction Box (BJB) houses the 20A micro-fuse for the fuel pump in slot F27. The terminals are undersized for the current draw under load, causing severe local resistive heating. The plastic housing of slot F27 melts, breaking electrical contact and permanently cutting power to the Fuel Pump.

### 22. GM Direct-Injection High-Resistance Injector Short Circuit

* **DTC:** P0200 (Injector Control Circuit) ; P0201 (Injector Circuit Open - Cylinder 1).


* **Freeze Frame:** Fuel System Status: Open Loop - Fault; Engine Speed: 150 RPM; System Voltage: 11.5V.
* **Mode $06:** Misfire Monitor (MID $A1) - CID $01 (Cylinder 1 current misfires) - rising rapidly during crank.
* **Logic & Reasoning:** The internal solenoid winding of the high-pressure GDI injector on Cylinder 1 shorts to the injector’s metal casing. During engine cranking, the PCM’s injector driver circuit detects an immediate overcurrent surge and enters a protective shutdown mode, cutting power to all injectors simultaneously to prevent driver destruction.

### 23. VW/Audi 2.0T TSI Intake Valve Carbon Plugging

* **DTC:** P0300 (Random Misfire) ; P050D (Cold Start Rough Idle).


* **Freeze Frame:** ECT: 12°C (Cold Start); Engine Speed: 950 RPM (Engine started, ran extremely rough, and stalled); MAP Sensor: 65 kPa.
* **Mode $06:** Misfire Cylinder Data (MID $A1) - CID $01-$04 (Misfire counts during first 500 cold engine cycles) - Value: 420 counts / Max Limit: 50 (Failed).
* **Logic & Reasoning:** Direct-injection engines do not wash the intake valves with fuel, leading to carbon deposits on the valve stems. During a cold start, these carbon deposits absorb the atomized petrol from the GDI injectors. This starves the cylinders of fuel, causing severe lean misfires. The PCM attempts dual-pulse start-up fueling, but combustion efficiency collapses, causing a stall.

### 24. GM GDI Fuel Rail Pressure (FRP) Sensor Voltage Drift

* **DTC:** P0087 (Fuel Rail Pressure Too Low)  / P0191 (Fuel Rail Pressure Sensor Performance).


* **Freeze Frame:** FRP Sensor Reading: 2800 PSI (Expected: 45 PSI at initial crank); Engine Speed: 150 RPM; ECT: 20°C.
* **Mode $06:** Comprehensive Component Monitor (MID $00) - Failed.


* **Logic & Reasoning:** The GDI high-pressure sensor internal reference element drifts. It falsely reports 2800 PSI of fuel rail pressure to the PCM. The PCM, believing the fuel rail is already pressurized, commands the fuel pump driver module to minimum duty cycle (almost off). No fuel is actually delivered, resulting in an immediate crank-no-start.

### 25. Nissan GDI HPFP Spill Valve Solenoid Open Circuit

* **DTC:** P0090 (Fuel Pressure Regulator 1 Control Circuit).
* **Freeze Frame:** Fuel Rail Pressure: 62 PSI (Normal low pressure feed, but target high pressure is 600+ PSI), Engine Speed: 150 RPM; ECT: 15°C.
* **Mode $06:** Fuel System Monitor (MID $81) - TID $02 (GDI fuel system pressure check) - Failed.
* **Logic & Reasoning:** The electronic spill valve solenoid on the high-pressure fuel pump (driven by the exhaust camshaft lobe) suffers an open circuit. The pump cannot regulate or trap fuel in the pumping chamber, causing direct injection pressure to stay at the low feed-pump level (62 PSI). This pressure is too low to inject fuel into cylinders during the compression stroke.

### 26. Hyundai/Kia Theta II Crankshaft Position Sensor (CKP) Internal Short

* **DTC:** P0335 (Crankshaft Position Sensor "A" Circuit Malfunction) ; P1604 (Startability Malfunction).


* **Freeze Frame:** Engine Speed: 0 RPM (Cranks physically at 180 RPM); System Voltage: 10.8V; Fuel System Status: Open Loop.
* **Mode $06:** Continuous Misfire Monitor (MID $A1) - Marked "Incomplete" (aborted by the speed processing engine).
* **Logic & Reasoning:** A plastic housing fracture in the CKP sensor allows engine oil inside. This shorts out the internal Hall-effect sensor plate. While cranking, the sensor signal stays stuck at a flat 0V. Lacking an RPM input, the PCM cannot time direct-injection pulses or spark plug firing, preventing the engine from starting.

### 27. GM Electronic Throttle Body TPS Sensor Correlation Mismatch

* **DTC:** P2135 (Throttle Position Sensor A/B Voltage Correlation).
* **Freeze Frame:** TP Sensor 1: 1.1V; TP Sensor 2: 3.9V (The sum is 5.0V, matching target correlation); TP Sensor 1 at crank: 1.1V, TP Sensor 2: 2.1V (mismatch detected); Engine Speed: 150 RPM.
* **Mode $06:** Throttle Actuator Control (TAC) Monitor (MID $00) - Failed.
* **Logic & Reasoning:** Heavy wear on the plastic throttle body gears causes physical backlash, or oil intrusion contaminates the internal circuit board. When cranking, the dual sensor voltages (TPS 1 and TPS 2) do not rise and fall in perfect, mirrored symmetry. The PCM flags a correlation error and enters a protective "Engine Shutdown / Fail-Safe" mode, shutting down throttle control.

### 28. BMW Valvetronic Eccentric Shaft Sensor Connector Oil Intrusion

* **DTC:** P1020 (Valvetronic Eccentric Shaft Sensor Signal Range Mismatch).
* **Freeze Frame:** Engine Speed: 150 RPM; VVT Eccentric Shaft Angle: 0 degrees; System Voltage: 11.2V.
* **Mode $06:** Continuous monitors aborted due to active VVT fault.
* **Logic & Reasoning:** The seal on the Valvetronic eccentric shaft sensor connector fails, letting high-pressure engine oil seep directly into the electrical pin housing. This oil bridges the 5V reference circuit and the sensor ground circuit. The 5V reference circuit collapses, causing a total sensor signal failure.

### 29. Mazda SkyActiv GDI Evaporative Purge Solenoid Stuck Open

* **DTC:** P0455 (EVAP Gross Leak Detected) ; P0172 (System Too Rich - Bank 1).


* **Freeze Frame:** STFT: -25% ; Engine Speed: 110 RPM (Cranks with heavy sputtering); ECT: 22°C.


* **Mode $06:** EVAP System Monitor (MID $3B) - TID $02 (Purge Flow Test) - Failed.
* **Logic & Reasoning:** The purge valve solenoid gets stuck wide open due to carbon dust from the charcoal canister. When starting, the high intake vacuum pulls a heavy charge of raw petrol vapor directly from the fuel tank through the canister into the intake manifold. The air-fuel ratio drops below 9:1, flooding the cylinders with fuel and preventing starting.

### 30. Ford EcoBoost Turbocharger Bypass / Diverter Valve Diaphragm Rupture

* **DTC:** P0299 (Turbocharger Underboost Condition).
* **Freeze Frame:** MAP Sensor: 14.1 PSI (At sea level, expected boost pressure is 18+ PSI under load); Engine Speed: 1200 RPM (Starts but stalls immediately under any load attempt); ECT: 45°C.
* **Mode $06:** Boost Pressure Control Monitor (MID $71) - TID $02 (Target vs. Actual Boost) Value: 4.2 PSI Deviation / Max Limit: 3.0 PSI (Failed).
* **Logic & Reasoning:** The rubber diaphragm inside the electronically controlled turbocharger bypass valve tears. The intake charge air leaks directly back into the low-pressure turbocharger inlet. When starting, the actual intake manifold pressure falls far below the PCM's targeted load curve. The PCM registers a severe underboost fault and enters a protective shutdown loop.

By correlating exhaust gas signatures with OBD-II Parameter IDs (PIDs), technicians can perform "logical interpretation" diagnostics to identify root causes before a Diagnostic Trouble Code (DTC) is even triggered. The following profiles outline how various powertrain malfunctions manifest in live data at low idle ($\approx 800$ RPM) versus stress idle ($\approx 4000$ RPM).

### Master Logic for Logical Interpretation

The primary diagnostic differentiator is the **Total Fuel Trim (STFT + LTFT)**.

* **Vacuum Leak Logic:** High positive trims at low idle that normalize at high RPM. At idle, manifold vacuum is highest, and unmetered air is a large percentage of the total intake. At high RPM, the leak becomes a negligible percentage of the total air volume.
* **Fuel Delivery Logic:** Normal trims at idle that become highly positive at high RPM/Load. This indicates the fuel pump or injectors cannot maintain the volume required for high-speed operation.

---

### Case 1: Rich Mixture (Excess Fuel)

**Probable DTCs:** P0172, P0175, P0201 

| PID Category | Parameter | Low Idle ($\approx 800$ RPM) | Stress Idle ($\approx 4000$ RPM) |
| --- | --- | --- | --- |
| **Air & Fuel** | Total Fuel Trim | Negative ($<-10\%$) | Negative ($<-10\%$) |
| **Air & Fuel** | MAF | Normal to High | High (if MAF is over-reporting) |
| **Combustion** | O2 Sensor (Up) | Stuck High ($>0.8\text{V}$) | Stuck High ($>0.8\text{V}$) |
| **Combustion** | Wideband AFR | $< 14.7$ (Rich) | $< 14.7$ (Rich) |
| **Management** | MAP | Normal to High | Low (Rapid Rise) |

**Logical Diagnosis:** If trims are consistently negative across both RPM ranges and the O2 sensor is "lazy" or stuck rich, the PCM is actively subtracting fuel. If MAF readings are higher than $1\text{ g/s}$ per liter of displacement at idle, the MAF itself is the likely culprit.

---

### Case 2: Lean Mixture - Vacuum Leak Profile

**Probable DTCs:** P0171, P0174, P2187

| PID Category | Parameter | Low Idle ($\approx 800$ RPM) | Stress Idle ($\approx 4000$ RPM) |
| --- | --- | --- | --- |
| **Air & Fuel** | Total Fuel Trim | Highly Positive ($>+15\%$) | Normalizes ($\pm 5\%$) |
| **Air & Fuel** | MAF | Low (Unmetered air entry) | Normal (Linear rise) |
| **Combustion** | O2 Sensor (Up) | Stuck Low ($<0.2\text{V}$) | Rapid Oscillations ($0.1-0.9\text{V}$) |
| **Management** | MAP | High (Low Vacuum) | Normalizes |
| **Management** | Idle Control | High IAC Counts / Steps | N/A |

**Logical Diagnosis:** The normalization of fuel trims at $4000$ RPM is the "smoking gun" for a vacuum leak. If the engine stalls at $800$ RPM but runs perfectly at $4000$ RPM, check intake gaskets or PCV hoses.

---

### Case 3: Lean Mixture - Fuel Starvation Profile

**Probable DTCs:** P0171, P0087

| PID Category | Parameter | Low Idle ($\approx 800$ RPM) | Stress Idle ($\approx 4000$ RPM) |
| --- | --- | --- | --- |
| **Air & Fuel** | Total Fuel Trim | Normal ($\pm 5\%$) | Highly Positive ($>+15\%$) |
| **Air & Fuel** | MAF | Normal | Normal (Linear rise) |
| **Combustion** | O2 Sensor (Up) | Rapid Oscillations | Stuck Low ($<0.2\text{V}$) |
| **Management** | Calculated Load | Normal | Low (Lack of power) |

**Logical Diagnosis:** High trims at high RPM indicate the fuel system cannot keep up with demand. This points to a weak fuel pump, clogged filter, or restricted fuel rail.

---

### Case 4: Combustion Quality Failure (Misfire)

**Probable DTCs:** P0300, P030x, P035x

| PID Category | Parameter | Low Idle ($\approx 800$ RPM) | Stress Idle ($\approx 4000$ RPM) |
| --- | --- | --- | --- |
| **Combustion** | Misfire Counters | Rising on specific cylinder | Rising rapidly or Clearing |
| **Air & Fuel** | Total Fuel Trim | Slightly Positive (False Lean) | Variable |
| **Combustion** | O2 Sensor (Up) | Erratic (High $\text{O}_2$ spikes) | Erratic |
| **Management** | Timing Advance | Retarded (Anti-knock logic) | Retarded / Unstable |
| **Management** | MAP | Fluctuating / Pulsing | Unstable |

**Logical Diagnosis:** PCM sees the crank deceleration and increments the counter. Chemically, the "False Lean" occurs because the O2 sensor sees the unburned oxygen from the misfiring cylinder, causing the PCM to add fuel (positive trims) despite raw fuel being present in the exhaust.

---

### Case 5: Catalyst Efficiency Failure

**Probable DTCs:** P0420, P0430 

| PID Category | Parameter | Low Idle ($\approx 800$ RPM) | Stress Idle ($\approx 4000$ RPM) |
| --- | --- | --- | --- |
| **Combustion** | Downstream O2 | Steady ($\approx 0.45\text{V}$) | **Mirroring Upstream** ($0.1-0.9\text{V}$) |
| **Air & Fuel** | Total Fuel Trim | Normal | Normal |
| **Management** | Calculated Load | Normal | Normal |

**Logical Diagnosis:** A healthy catalyst stores oxygen, making the downstream sensor signal "lazy" or steady. If the downstream sensor begins to oscillate in sync with the upstream sensor at $4000$ RPM, the catalyst's oxygen storage capacity is depleted.

---

### Case 6: Mechanical Fault / Oil Burning (POA Signature)

**Probable DTCs:** P250C (Low Oil), P0300 (Secondary) 

| PID Category | Parameter | Low Idle ($\approx 800$ RPM) | Stress Idle ($\approx 4000$ RPM) |
| --- | --- | --- | --- |
| **Air & Fuel** | Total Fuel Trim | Normal ($\pm 3\%$) | Normal ($\pm 3\%$) |
| **Combustion** | O2 Sensor (Up) | Normal switching | Slow / Lazy (Coated in oil) |
| **Management** | MAP | High (Poor Sealing) | Normalizes slightly |
| **Management** | Timing Advance | Normal | Fluctuating (Knock from carbon) |

**Logical Diagnosis:** This case is often "invisible" to OBD trims because oil is not part of the PCM's metered air-fuel calculation. High HC on a gas analyzer ($>2000$ PPM) paired with **normal fuel trims** and **normal Lambda** ($\lambda \approx 1.000$) confirms the hydrocarbons are coming from a mechanical source (rings/valves) rather than a fueling error.

---

### Case 7: Forced Induction Malfunction (Turbo/Supercharger)

**Probable DTCs:** P0234 (Overboost), P0299 (Underboost)

| PID Category | Parameter | Low Idle ($\approx 800$ RPM) | Stress Idle ($\approx 4000$ RPM) |
| --- | --- | --- | --- |
| **Management** | MAP | $\approx 14.7\text{ psi}$ (Ambient) | **Actual vs. Desired Boost** |
| **Air & Fuel** | MAF | Normal | Fails to reach Peak ($< 40 \times \text{Disp.}$) |
| **Management** | Calculated Load | Normal | Low (Underboost) / Limp Mode |

**Logical Diagnosis:** At stress idle ($4000$ RPM) with no load, boost should be minimal. However, under a "Snap Throttle" test, the MAP should immediately rise toward its boost ceiling ($22-30\text{ psi}$ absolute). If MAP fails to rise or MAF doesn't exceed $40$ times the engine displacement in $\text{g/s}$ during a load test, an induction leak or turbo failure is present.

Building on the previous report, here are 25 additional common powertrain Diagnostic Trouble Codes (DTCs) for petrol vehicles from the 1990–2020 era, grouped by their respective powertrain module clusters and including the logic used by the Powertrain Control Module (PCM) to trigger them.

### Cluster 1: Fuel and Air Metering (P00xx, P01xx)

The PCM monitors these sensors to maintain stoichiometry. If a sensor's voltage or frequency deviates from a calibrated range for a specific duration (typically 1 second or more), a code is stored.

* **P0010 – Intake Camshaft Position Actuator Circuit (Bank 1):** Triggered when the PCM monitors the Variable Camshaft Timing (VCT) circuit and detects voltage that exceeds or falls below calibrated limits.


* **P0011 – Intake Camshaft Position Timing - Over-Advanced (Bank 1):** The PCM identifies that the physical camshaft timing is more advanced than the commanded target value.


* **P0012 – Intake Camshaft Position Timing - Over-Retarded (Bank 1):** Logic triggers when the camshaft timing fails to reach the commanded advanced position and remains in a retarded state.


* **P0014 – "B" Camshaft Position Timing - Over-Advanced:** Similar to P0011, this specifically monitors the exhaust (B) camshaft for timing that exceeds target advance limits.


* **P0016 – Crankshaft Position - Camshaft Position Correlation:** Triggered when the PCM identifies a misalignment between the crankshaft and camshaft sensor signals of greater than one tooth.


* **P0102 – Mass Air Flow (MAF) Circuit Low:** The PCM detects that the MAF sensor voltage or frequency is below the minimum operational threshold for a set time.


* **P0103 – Mass Air Flow (MAF) Circuit High:** Logic triggers when the MAF sensor signal exceeds the maximum calibrated limit for the current engine load.


* **P0106 – Manifold Absolute Pressure (MAP) Range/Performance:** The PCM detects the manifold pressure reading is not within a calibrated value relative to engine speed and throttle position.
* **P0113 – Intake Air Temperature (IAT) Sensor Circuit High:** Triggered when the IAT sensor signal indicates a very low temperature (typically meaning high resistance or an open circuit).


* **P0116 – Engine Coolant Temperature (ECT) Range/Performance:** The PCM compares the ECT to other sensors (like IAT) after a soak period; the code sets if they differ by more than a calibrated value (e.g., 17°C).
* **P0121 – Throttle Position Sensor (TPS) Range/Performance:** Triggered when the TPS voltage does not correlate with the mass airflow or manifold pressure readings.


* **P0135 – O2 Sensor Heater Circuit (Bank 1, Sensor 1):** The PCM monitors the current draw of the oxygen sensor's heating element and triggers the code if it identifies an open circuit or improper resistance.



### Cluster 2: Fuel and Air Metering - Injector Circuit (P02xx)

This cluster focuses on the electrical integrity of the fuel delivery actuators.

* **P0200 – Injector Circuit Malfunction:** The PCM monitors the injector drivers and triggers a code if it fails to see the expected voltage drop or "inductive kick" when a pulse is commanded.


* **P0219 – Engine Overspeed Condition:** Logic triggers the code when the engine RPM exceeds the manufacturer-defined safety limit.



### Cluster 3: Ignition System and Misfire (P03xx)

These codes monitor the timing and quality of the combustion event.

* **P0327 – Knock Sensor 1 Circuit Low Input:** Triggered when the PCM detects that the voltage from the knock sensor is below the minimum threshold during engine operation.


* **P0335 – Crankshaft Position (CKP) Sensor Malfunction:** The PCM triggers this when it fails to receive a signal from the CKP or detects erratic pulses while the engine is turning.


* **P0340 – Camshaft Position (CMP) Sensor Circuit:** Triggered if the PCM lacks a valid CMP signal, which it uses to identify Cylinder 1 for fuel injection and ignition timing.

### Cluster 4: Auxiliary Emission Controls (P04xx)

These codes monitor systems designed to reduce tailpipe and evaporative emissions.

* **P0411 – Secondary Air Injection Incorrect Flow:** Triggered when the PCM commands the air pump on but fails to detect the expected change in oxygen sensor voltage or pressure.
* **P0441 – Evaporative Emission (EVAP) Incorrect Purge Flow:** The PCM detects that no vacuum is present in the system when the purge valve is commanded open.
* **P0446 – Evaporative Emission (EVAP) Vent Control Circuit:** Triggered by an electrical fault in the solenoid circuit that controls the EVAP vent valve.
* **P0456 – Evaporative Emission (EVAP) Very Small Leak:** The PCM performs a pressure or vacuum decay test and identifies a leak as small as 0.020".



### Cluster 5: Vehicle Speed and Idle Control (P05xx)

This cluster manages engine speed stability and vehicle transit data.

* **P0506 – Idle Control System RPM Lower Than Expected:** Triggered when the actual engine RPM remains below the target idle speed despite the PCM increasing airflow through the IAC or throttle.


* **P0507 – Idle Control System RPM Higher Than Expected:** Logic triggers when the idle speed stays above target despite the PCM commanding minimum airflow.



### Cluster 6: Computer and Output Circuit (P06xx)

This cluster focuses on the internal health and memory of the control module.

* **P0603 – Internal Control Module Keep Alive Memory (KAM) Error:** Triggered when the PCM loses battery power to its internal memory chip, resulting in the loss of long-term fuel trim and adaptive data.



### Cluster 7: Transmission (P07xx, P08xx)

These codes monitor the hydraulic and electronic coordination of the transaxle.

* **P0841 – Transmission Fluid Pressure Sensor/Switch Performance:** Triggered when the PCM detects a hydraulic pressure reading that is inconsistent with the currently commanded gear or solenoid state.