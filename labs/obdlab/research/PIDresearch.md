Comprehensive Engineering Report on OBD-II Parameter ID (PID) Module Testing and Diagnostic Methodologies for Legacy Petrol Vehicles (1990–2010)
The implementation of the second-generation on-board diagnostics standard, known as OBD-II, represents a major milestone in automotive engineering.1 Transitioning from the highly fragmented, manufacturer-specific OBD-I systems of the early 1990s, OBD-II established a standardized framework for emissions-related diagnostics, electrical communication protocols, and real-time telemetry querying.1 Mandated in North America by the Environmental Protection Agency (EPA) under regulations in 40 CFR Part 86, OBD-II became compulsory for all light-duty petrol vehicles under 8,500 pounds starting January 1, 1996.1 This requirement was later extended to medium-duty vehicles between 8,500 and 14,000 pounds in 2005.4 The primary regulatory driver, initiated by precursor mandates from the California Air Resources Board (CARB) in 1988, was to establish an on-board monitoring system capable of detecting component failures or degradation that would cause tailpipe emissions to exceed 150% of the vehicle’s certified standards.3 This engineering report provides a detailed study of diagnostic module testing, physical and data link layer architectures, mathematical parameter scaling, and compliance validation for petrol vehicles produced during this era.1
Physical and Data Link Layer Specifications of Legacy Protocols
Legacy OBD-II configurations rely on five distinct physical and data link layer standards to establish a digital connection between external test equipment and the vehicle's electronic control units (ECUs).1 These protocols are exposed through a standardized 16-pin J1962 diagnostic link connector (DLC).5



                     J1962 Female Connector Pinout
                     ___________________________
                    /  1   2   3   4   5   6   7   8 \
                   /   9  10  11  12  13  14  15  16  \
                   ---------------------------------


The electrical implementation of the J1962 connector is protocol-dependent, meaning specific pins must be populated to support the underlying communication bus.8

J1962 Pin
Assignment
Associated Diagnostic Protocol / Function
Electrical/Signaling Characteristics
Pin 2
Bus Positive ()
SAE J1850 (PWM/VPW) 8
Active differential high or single-ended signal path.3
Pin 4
Chassis Ground 8
Power Ground
Zero-volt reference to the vehicle chassis.8
Pin 5
Signal Ground 8
Reference Ground
Low-current reference ground for serial communication.
Pin 6
CAN High (CAN-H)
ISO 15765-4 8
Dominant state drives to 3.5V; recessive at rest at 2.5V.10
Pin 7
K-Line
ISO 9141-2 / ISO 14230-4 8
Bidirectional serial path; idles high at battery voltage () via a 510  pull-up.3
Pin 10
Bus Negative ()
SAE J1850 (PWM only) 8
Complementary low differential line for pulse-width modulation.8
Pin 14
CAN Low (CAN-L)
ISO 15765-4 8
Dominant state drives to 1.5V; recessive at rest at 2.5V.10
Pin 15
L-Line
ISO 9141-2 / ISO 14230-4 8
Unidirectional initialization line (optional).3
Pin 16
Battery Positive ()
Unswitched Battery Power 8
Direct  supply (~12.0V to 14.4V).8

Before the 2008 mandate requiring all vehicles sold in North America to use Controller Area Network (CAN) communication via ISO 15765-4, the automotive market was highly fragmented.2 Manufacturers utilized distinct signaling pathways:
SAE J1850 PWM (Pulse Width Modulation): Primarily used by Ford Motor Company.12 This is a differential two-wire protocol operating at 41.6 kbps.12
SAE J1850 VPW (Variable Pulse Width): Favored by General Motors.12 It is a single-wire protocol operating at 10.4 kbps.7 The bus idles low and uses high-voltage signaling (+7V) with a decision threshold at +3.5V.3
ISO 9141-2: Widely implemented on Asian, European, and Chrysler vehicles.3 This asynchronous serial communication protocol operates at 10.4 kbps over a single K-Line (Pin 7), with optional L-Line (Pin 15) wake-up mechanisms.3
ISO 14230-4 (KWP2000 - Keyword Protocol 2000): Mechanically identical to ISO 9141-2 using the K-Line.8 However, KWP2000 optimizes communication with faster initialization methods (Fast Init) and expanded message structures.9
ISO 15765-4 (CAN): Gradually phased in from 2003 through 2007, and mandated in 2008.8 It operates at 250 kbps or 500 kbps using differential signaling (Pins 6 and 14), providing much faster data rates and improved noise immunity compared to earlier single-wire designs.9
Diagnosing and isolating communication faults within these legacy interfaces requires a structured physical-layer validation process.10 With the ignition in the key-on, engine-off (KOEO) state, a digital multimeter is connected to the J1962 pins to check the voltage.10 Pin 16 must show unswitched battery voltage (), while Pins 4 and 5 must show a low resistance path to ground ().8 For ISO 9141-2 and ISO 14230-4 systems, probing Pin 7 (K-Line) should reveal a voltage fluctuating between 8V and 12V under active communication.10 For SAE J1850 PWM or VPW configurations, checking Pins 2 and 10 will verify signal activity on the bus.8 On transitional vehicles equipped with CAN networks (pre-2008), measuring Pins 6 (CAN-H) and Pin 14 (CAN-L) should show approximately 2.5V at rest relative to ground, yielding a differential recessive voltage of 0V.10
These legacy single-wire protocols are highly sensitive to electrical variations.10 Because the K-Line is pulled high to  by a 510  resistor in the ECU, any system voltage drop below 10.5V—such as during a cold engine crank—can interrupt the communication handshake.3 Furthermore, using passive, unmanaged splitters on a legacy single-wire bus (such as J1850 or K-Line) can introduce signal reflections and excessive capacitive load.10 These issues distort the digital waveform, making the communication bus unstable or inoperative.10
Standardization of Diagnostic Services and Parameter ID (PID) Architecture
The SAE J1979 standard (harmonized with ISO 15031-5) organizes OBD-II communications into ten distinct diagnostic services, or modes.15 A diagnostic request from a scan tool consists of a service byte followed by one or more Parameter ID (PID) bytes.16 The ECU then responds by appending the requested data.7
The diagnostic modes used for legacy emissions testing and vehicle diagnostics are structured as follows:
Mode 01 - Request Current Powertrain Diagnostic Data: Retrieves real-time sensor measurements, switch statuses, and system calculations.15
Mode 02 - Request Powertrain Freeze Frame Data: Provides a snapshot of Mode 01 parameters captured at the exact moment an emissions-related diagnostic trouble code (DTC) was stored.15 Mode 01 and Mode 02 use identical PID structures.15
Mode 03 - Request Emission-Related Diagnostic Trouble Codes: Retrieves stored DTCs from the ECU's non-volatile memory.15
Mode 04 - Clear/Reset Emission-Related Diagnostic Information: Erases stored DTCs, freeze frame data, oxygen sensor test results, and resets diagnostic readiness monitors.7
Mode 05 - Request Oxygen Sensor Monitoring Test Results: Provides test values and thresholds for oxygen sensor operation.15 This mode is used only on pre-CAN legacy physical links; CAN-equipped vehicles migrate this functionality to Mode 06.15
Mode 06 - Request On-Board Monitoring Test Results for Non-Continuously Monitored Systems: Accesses test results for components like the catalytic converter, evaporative emissions (EVAP) system, and secondary air system.15
Mode 07 - Request Emission-Related Diagnostic Trouble Codes Detected During Current or Last Driving Cycle: Retrieves pending codes to identify intermittent malfunctions.15
Mode 08 - Request Control of On-Board System, Test or Component: Allows bidirectional control of actuators (such as purging an EVAP solenoid).10
Mode 09 - Request Vehicle Information: Retrieves static metadata, including the Vehicle Identification Number (VIN), Calibration IDs (Cal ID), and Calibration Verification Numbers (CVN).2
Mode 0A - Request Emission-Related Diagnostic Trouble Codes with Permanent Status: Accesses permanent DTCs that cannot be cleared by Mode 04 or battery disconnection.8 This mode requires a CAN-based link (ISO 15765-4).12
To ensure a scan tool can query a vehicle without protocol collisions, SAE J1979 implements bitwise-encoded initialization PIDs.15 PIDs such as 0x00, 0x20, 0x40, and 0x60 return a 4-byte (32-bit) payload that indicates which subsequent PIDs are supported by the ECU.15 The structure of the 4-byte response for PID 0x00 is mapped bit-by-bit:



Byte A:...
Byte B:...
Byte C:...
Byte D:...


A binary value of 1 indicates the PID is supported, while 0 indicates it is unsupported.19 If the final bit of the payload (the support bit for PID 0x20) is 1, the diagnostic tool can query PID 0x20 to discover support for PIDs 0x21 through 0x40.15 This systematic structure allows scan tools to dynamically map the vehicle's diagnostic capabilities.
The table below provides a comprehensive list of standard Mode 01 Parameter IDs utilized in legacy petrol vehicles, detailing their hex codes, returned byte counts, expected metric ranges, and standard scaling formulas.15

PID (Hex)
Data Bytes
Parameter Description
Operational Metric Range
LaTeX Scaling Formula
Unit
00
4
Supported PIDs [0x01 - 0x20]
Bit Encoded 15
Bit encoded $ ==$ 15
—
01
4
Monitor Status Since DTCs Cleared
Bit Encoded 15
Bit encoded status of readiness monitors 15
—
02
2
DTC Causing Freeze Frame Capture
Decoded as DTC 15
Standard DTC format decoding 15
—
03
2
Fuel System Status
Bit Encoded 15
Bit encoded status of closed-loop fueling
—
04
1
Calculated Engine Load
0 to 100 15
 15

05
1
Engine Coolant Temperature (ECT)
-40 to 215 15
 15

06
1
Short Term Fuel Trim (STFT)—Bank 1
-100 to 99.2 15
 15

07
1
Long Term Fuel Trim (LTFT)—Bank 1
-100 to 99.2 15
 15

08
1
Short Term Fuel Trim (STFT)—Bank 2
-100 to 99.2 15
 15

09
1
Long Term Fuel Trim (LTFT)—Bank 2
-100 to 99.2 15
 15

0A
1
Fuel Pressure (Gauge)
0 to 765 15
 15

0B
1
Intake Manifold Absolute Pressure
0 to 255 15
 15

0C
2
Engine Speed (RPM)
0 to 16,383.75 15
 15

0D
1
Vehicle Speed (VSS)
0 to 255 15
 15

0E
1
Timing Advance (#1 Cylinder)
-64 to 63.5 15
 15

0F
1
Intake Air Temperature (IAT)
-40 to 215 15
 15

10
2
Mass Air Flow (MAF) Rate
0 to 655.35 15
 15

11
1
Throttle Position (TPS)
0 to 100 15
 15

1F
2
Run Time Since Engine Start
0 to 65,535 15
 15

21
2
Distance Traveled with MIL On
0 to 65,535 15
 15

22
2
Fuel Rail Pressure (Relative to Vac)
0 to 5,177.26


2C
1
Commanded EGR duty cycle
0 to 100 15
 20

2D
1
EGR System Error
-100 to 99.2 15
 20

2E
1
Commanded Evaporative Purge
0 to 100 15
 20

2F
1
Fuel Level Input
0 to 100
 20

31
2
Distance Traveled Since Codes Cleared
0 to 65,535
 20

32
2
Evap. System Vapor Pressure
-8,192 to 8,192
 ( is signed) 20

3C
2
Catalyst Temp. (Bank 1, Sensor 1)
-40 to 6,513.5
 20

41
4
Monitor Status This Drive Cycle
Bit Encoded
Bit encoded monitor completion 15
—
42
2
Control Module Voltage
0 to 65.535
 20

43
2
Absolute Load Value
0 to 25,700 20
 20

44
2
Commanded Equivalence Ratio ()
0 to 2
 20
—

Mathematical Formulations for Powertrain Load and Volumetric Efficiency
Accurately evaluating engine diagnostics requires understanding how the engine control module calculates load and breathing characteristics.21 The SAE J1979 standard defines two distinct load parameters: Calculated Engine Load (PID 04) and Absolute Load Value (PID 43).23
Calculated Load vs. Absolute Load
Calculated Engine Load (PID 04) represents the current airflow relative to the peak airflow the engine can draw at sea level, adjusted for barometric pressure.23 Calculated load is designed to reach  () at wide-open throttle (WOT) under normal operating conditions, regardless of altitude or engine RPM.16 The equation is expressed as:

To standardize this calculation across different manufacturers, a more precise formula was introduced:

Where:
 is Standard Temperature and Pressure ( /  and  /  BARO).24
 is the Ambient Air Temperature in degrees Celsius.24
This calculated load value is highly responsive to throttle position and is linearly correlated with intake manifold vacuum, making it an ideal parameter for fuel enrichment scheduling.24
Absolute Load Value (PID 43) represents the actual air mass captured per cylinder intake stroke relative to the theoretical maximum cylinder capacity.24 It is defined as:

Where:
The value  is the density of dry air at standard temperature and pressure ( and ).24
The raw air mass per cylinder stroke is calculated from the mass airflow (MAF) rate and engine speed (RPM):

For naturally aspirated engines, absolute load ranges from  to approximately  () at WOT, reflecting the engine's peak volumetric efficiency.24 On forced-induction (turbocharged or supercharged) engines, absolute load can easily exceed  and reach up to  () as intake air is compressed.24 This makes absolute load an essential parameter for spark advance timing and exhaust gas recirculation (EGR) scheduling.24
Volumetric Efficiency (VE) Modeling
Volumetric Efficiency is a measure of an engine's breathing efficiency.22 It compares the actual mass of air drawn into the cylinders to the theoretical mass of air the engine would hold if it could completely fill its displacement under current manifold conditions.22
Using the Ideal Gas Law (), Speed-Density (MAP-based) systems calculate the theoretical mass of air entering the engine using manifold pressure (MAP) and intake air temperature (IAT).21 The formula for theoretical mass airflow is:

Where:
 is in cubic inches (CID).21
 is the Manifold Absolute Pressure in PSI absolute.21
 is the Intake Air Temperature in degrees Rankine ().21
To calculate volumetric efficiency on a running vehicle, the engineer can compare actual mass airflow (measured by a MAF sensor) to this theoretical airflow calculation.21 The EFILive {CALC.VE} formula provides a direct calculation of volumetric efficiency using standard OBD-II telemetry:

Alternatively, the Zack volumetric flow analysis converts the measured MAF (g/s) to actual volumetric flow rate (AVF) in cubic feet per minute () 28:

Where  is the local air density in :

This is compared to the Theoretical Air Flow (TAF) in :


For metric calculation environments, ScannerDanner provides an alternative volumetric efficiency formula using SI units:

Where the metric air density () in kilograms per cubic meter is:

To account for standard pumping losses under WOT testing, empirical correction factors are applied across the engine's RPM range to adjust theoretical expectations 32:
1500 to 3000 RPM: Multiply theoretical peak airflow by a  correction factor.32
3500 RPM (Peak Torque): Multiply theoretical peak airflow by a  correction factor.32
4000 to 5000 RPM: Multiply theoretical peak airflow by a  correction factor.32
Applying these calculations at idle helps verify basic engine breathing.33 For example, a warm, properly running 1.8-liter Toyota Corolla idling at 750 RPM under closed-loop control pulls against a closed throttle plate.33 This restriction creates a high manifold vacuum of 20 in. Hg, which equates to a manifold absolute pressure of 9.9 in. Hg.34 With only one-third of standard atmospheric pressure available, the maximum possible cylinder charge is limited to 33%.34 Accounting for the engine's low idle volumetric efficiency of approximately 45%, the actual breathing efficiency drops to a typical idle VE of 15%.33 The expected idle airflow calculation is resolved as:

Comparing calculated airflow to actual sensor measurements allows engineers to verify diagnostic accuracy.22 Additionally, on engines equipped with both VSS and MAF sensors, real-time fuel efficiency can be calculated using standard telemetry 35:

On vehicles without a physical MAF sensor, the PCM calculates a synthetic mass airflow rate using RPM, MAP, and IAT telemetry.35 This calculated air mass value is then used to schedule fuel delivery.21 Volumetric efficiency baselines vary significantly by engine design; for example, a larger, low-RPM utility engine like a 1999 7.4-liter Chevrolet Suburban typically exhibits a peak VE of approximately 65%, whereas smaller, higher-RPM performance engines frequently exceed 85% volumetric efficiency.35
Advanced Closed-Loop Diagnostics: Oxygen Sensor Physics and Catalytic Monitoring
OBD-II diagnostics rely on closed-loop fuel control to maintain the engine's air-fuel ratio near the stoichiometric point of 14.7:1, where emissions are minimized.36 This control loop depends on the physical operation of zirconium-ceramic oxygen sensors.37
Oxygen Sensor Physics and Aging
A zirconium-ceramic oxygen sensor consists of a double-platinum-coated ceramic bulb.37 The outer platinum layer is exposed to hot exhaust gases, while the inner cavity vents to the atmosphere through the sensor’s body or wiring harness insulation.37 The difference in oxygen concentration between the exhaust gas and the outside air creates a voltage potential across the ceramic bulb.37 When the fuel mixture is rich (little unburned oxygen in the exhaust), the high concentration difference generates a voltage signal between 0.7V and 0.9V.37 Conversely, a lean mixture (excess unburned oxygen in the exhaust) yields a low concentration difference, causing the sensor output to drop between 0.1V and 0.3V.37 At stoichiometric equilibrium (14.7:1 air-fuel ratio), the sensor output is exactly 0.45V.37
The PCM monitors these voltage changes to continually adjust the fuel mixture, causing the air-fuel ratio to swing back and forth across the stoichiometric point.37 The frequency of these switches depends on the fuel injection architecture 37:
Feedback Carburetors: Slowest response, switching approximately once per second (1 Hz) at 2500 RPM.37
Throttle Body Injection (TBI): Moderate response, switching 2 to 3 times per second (2 to 3 Hz) at 2500 RPM.37
Multiport Fuel Injection (MPFI): Fastest response, switching 5 to 7 times per second (5 to 7 Hz) at 2500 RPM.37
Internal contaminants can poison the sensor bulb, slowing down its response time or causing it to stick at a specific voltage.39 Common contaminants include carbon buildup from rich running conditions, phosphorus from engine oil, and silicone residue from non-sensor-safe gaskets.39 Additionally, coolant leaks that allow antifreeze into the combustion chamber can coat the sensor bulb, leading to premature failure.39



                Upstream O2 Sensor 1 (Rapid Switching)
                
  1.0 V |      /\      /\      /\      /\      /\
        |     /  \    /  \    /  \    /  \    /  \
  0.5 V |----+----+----+----+----+----+----+----+---- (Stoichiometric / 0.45V)
        |   /    \  /    \  /    \  /    \  /    \
  0.0 V | _/      \/      \/      \/      \/      \_
  
  
                Downstream O2 Sensor 2 (Dampened Curve)
                
  1.0 V |
        |
  0.5 V |------------------------------------------- (Stable ~0.65V)
        |
  0.0 V |___________________________________________


Diagnostic Validation Procedures
Verifying oxygen sensor operation and closed-loop control requires a systematic diagnostic procedure 36:
Thermal Stabilization: Warm up the engine until the coolant temperature (ECT, PID 05) exceeds 80°C or 90°C to ensure the system enters closed-loop operation.36
Engine Speed Stabilization: Hold the engine speed at 2000 to 2500 RPM.36 Connect a high-speed oscilloscope or scan tool to monitor the upstream oxygen sensor (Sensor 1) voltage.36 A healthy sensor should switch between rich () and lean () at a frequency of at least 1 Hz.36
Responsiveness Verification (Snap-Throttle Test): Quickly snap the throttle wide open and then release it.18 Snapping the throttle open forces the engine into a rich command, which should immediately drive the sensor voltage above 0.8V.18 When the throttle closes, the engine entering deceleration fuel cut-off should immediately drop the sensor voltage below 0.2V.18 This transition should occur in less than 1 millisecond.36
Manual Enrichment Test: If the sensor output is stuck low, introduce propane or carburetor cleaner into the intake manifold.18 If the sensor voltage immediately climbs above 0.8V, the sensor is functional, and the lean condition is caused by an actual fuel delivery or vacuum issue.18 If the sensor does not respond, verify that the sensor wire is not open; if the electrical values exist at the sensor but do not reach the PCM terminal, a circuit fault is present.18
Catalytic Converter Efficiency Diagnostics
OBD-II regulations mandate monitoring the catalytic converter's health using a downstream oxygen sensor (Sensor 2) located after the catalyst.37 A healthy catalytic converter uses oxygen to convert carbon monoxide () and hydrocarbons () into carbon dioxide () and water ().36 This continuous oxidation process consumes almost all the oxygen in the exhaust stream.36
As a result, a functioning catalytic converter dampens the oxygen fluctuations in the exhaust gas.36 The downstream sensor should produce a relatively flat, stable voltage waveform on the rich side, ideally hovering between 0.6V and 0.7V.36 If the catalytic converter has degraded and lost its oxygen storage capacity, the exhaust gas passes through untreated.36 Under these conditions, the downstream sensor's waveform will begin to mirror the rapid switching pattern of the upstream sensor.36 If the downstream switching frequency exceeds a calibrated percentage of the upstream switching frequency, the PCM stores a P0420 DTC and illuminates the MIL.42
Fuel Trim Telemetry and Diagnostic Strategies for Vacuum Leaks (P0171)
Diagnosing a generic P0171 ("System Too Lean - Bank 1") diagnostic trouble code requires analyzing the differences in how MAF-based and MAP-based engine management systems calculate air mass.38
MAF-Based Engine Fuel Trim Response
In a Mass Air Flow (MAF) system, the sensor measures all air entering the intake tract.21 A vacuum leak introduces unmetered air into the intake manifold downstream of the MAF sensor, often caused by cracked PCV hoses or warped plastic intake manifold gaskets—a common issue on legacy Ford Explorer and F-150 engines.42
Because this unmetered air bypasses the MAF sensor, the PCM does not account for it and commands too little fuel.42 The upstream oxygen sensor detects this excess oxygen and sends a low voltage signal () to the PCM.36 The PCM compensates by increasing fuel delivery, which is reflected as positive short-term and long-term fuel trims (STFT and LTFT).36 When the total fuel trim correction (STFT + LTFT) exceeds a calibrated limit—typically  to —the PCM stores a P0171 code and illuminates the MIL.38
Because a vacuum leak introduces a relatively constant volume of unmetered air, its effect is highly dependent on engine speed and load.42 At idle, the throttle plate is nearly closed, and intake vacuum is high.34 The air entering through the leak represents a large percentage of the total air entering the engine, causing highly positive fuel trims ( or higher).42 When the throttle is opened under load, the engine draws in a much larger volume of metered air.42 The air entering through the vacuum leak remains relatively constant, meaning it becomes a negligible fraction of the total air mass.42 Consequently, the fuel trims return to normal (near ) at higher RPMs, as shown in the table below.42
MAP-Based Engine Fuel Trim Response
In contrast, Manifold Absolute Pressure (MAP) Speed-Density systems do not directly measure intake air mass.21 Instead, the PCM calculates air mass using intake manifold absolute pressure (MAP), intake air temperature (IAT), engine speed (RPM), and a calibrated volumetric efficiency table.21
Because a vacuum leak enters downstream of the throttle plate, it directly increases the manifold pressure (reducing intake vacuum).38 The MAP sensor immediately measures this pressure increase, and the PCM recalculates the higher air density.21 The PCM then automatically increases fuel injection to match the higher pressure.43
Because the MAP sensor accounts for the extra air, the engine does not run lean, and the fuel trims remain near .43 Instead, the primary symptom of a vacuum leak on a MAP-based engine is an elevated or erratic idle speed.38 To combat this high idle, the PCM will command the Idle Air Control (IAC) valve or throttle plate to close, which can be observed as an abnormally low IAC step count or throttle angle percentage.43
Altitude and Sensor Performance Considerations
Engineers must also account for barometric pressure (BARO) when evaluating MAP and MAF sensor diagnostics.18 At sea level, normal barometric pressure is approximately 29.9 in. Hg (101.3 kPa).24 Barometric pressure decreases by approximately 1.0 in. Hg for every 1,000 feet of altitude.32
At an altitude of 2,500 feet, barometric pressure drops to 27.4 in. Hg, which represents 91.6% of sea-level pressure.32 If a vehicle's MAP or BARO sensor drift and under-report barometric pressure, the PCM will underestimate the incoming air density.38 This sensor drift causes the PCM to inject too little fuel, resulting in highly positive fuel trims across all operating ranges—a diagnostic clue that points to a sensor calibration issue rather than a physical vacuum leak.38
The table below contrasts the expected telemetry values for various vacuum leak and sensor fault scenarios at idle and under load.26

Parameter
Standard Baseline (Idle)
MAF System Vacuum Leak (Idle)
MAF System Vacuum Leak (3000 RPM)
MAP System Vacuum Leak (Idle)
Defective/Drifted MAP Sensor (Idle)
04 (Calculated Load)
 26
 (Low)
 (Normal) 24
 (High)
 (Low)
06 / 08 (STFT)
 41
 44
 (Recovered) 44

 (High)
07 / 09 (LTFT)
 41
 42
 42

 (High)
0B (MAP)


 29
 (High)
 (Low)
10 (MAF)
 26
 (Low)
 28
N/A
N/A
11 (TPS Angle)


 (WOT) 16
 (IAC fully closed) 43

O2S1 Voltage
 (Switching)
 (Stuck Lean) 37
 (Switching)
 (Switching)
 (Stuck Lean)

Simulation, Hardware-in-the-Loop, and Compliance Testing Methodologies
Developing and validating OBD-II diagnostic equipment requires robust laboratory testing to ensure compatibility with legacy vehicles.10 This validation relies on specialized physical simulators and automated software test suites to confirm protocol compliance.12
Physical Simulator Platforms
Laboratory validation of OBD-II scan tools and adapters relies on dedicated hardware-in-the-loop (HIL) simulators to replicate legacy vehicle networks.12
The OE91C1300 ASIC: This chip simulates a vehicle's ECU by generating diagnostic trouble codes and sensor data in response to SAE J1979 scan tool requests.7 Operating at 10.4 kbps using the J1850 VPW protocol, it utilizes physical potentiometers connected to analog inputs to vary simulated parameters like RPM, vehicle speed, engine coolant temperature, MAF rate, and oxygen sensor voltages.7 If the fault input pin is pulled low, the chip generates three standard emissions DTCs (P0100, P0200, and P0300) and captures a corresponding freeze frame record.7 The chip also features a physical MIL LED output to indicate fault status.7
The ECUsim 2000 and MPOZ Simulators: These benchtop units simulate up to four virtual ECUs—such as the Powertrain Control Module (PCM), Transmission Control Module (TCM), Instrument Cluster (HEC), and Anti-lock Braking System (ABS)—conforming to the SAE J1979 and ISO 15031-5 standards.12 They support all legacy communication protocols: J1850 PWM, J1850 VPW, ISO 9141-2, ISO 14230-4, and ISO 15765-4.12 Physical knobs allow manual adjustments of key PIDs, and professional software commands over USB allow developers to inject communication errors, configure custom PIDs, and modify freeze frame records.12
Open-Source and Diagnostic Software Toolchains
Automotive software engineers utilize both proprietary and open-source toolchains to test diagnostic adapters and build ECU emulators.13
The Auterra Scan Tool Adapter Stack: This legacy adapter code is written in C and compiled using the CCS PCH compiler for the Microchip PIC18F248 microcontroller.13 Because hardware timers were limited, the J1850 PWM and VPW interfaces were bit-banged using assembly language and verified with a logic analyzer.13 The software translates incoming J1850, ISO 9141, ISO 14230, and ISO 15765-4 vehicle messages into serial commands sent to a host device.13
GitHub-Based Emulators and Testing Utilities: Open-source projects provide accessible diagnostic testing platforms:
ELM327-Emulator: A Python-based emulator that simulates an ELM327 adapter connected to a vehicle, supporting multi-ECU simulation.51 The emulator parses serial or TCP/IP commands and uses an internal dictionary (ObdMessage) to return realistic engine data, such as simulated sensor readings and DTC responses.51
OBDium: A modern, open-source diagnostic application written in Rust designed for real-time telemetry logging and DTC retrieval.50
autodiag: A Python-based scanning tool designed to interface with legacy serial adapters like the ELM320, ELM322, ELM323, and ELM327.53
Linux CAN Emulator: A C++ emulator that processes CAN frames from a USB-to-CAN analyzer and routes standard PID requests to simulated diagnostic service routines.54
Validating legacy OBD-II adapters requires verifying both connection speed and command support.55 Validator software (such as the ELM Scan Adapter Validator) measures adapter latency by sending rapid PID requests.55 High-speed adapters achieve a low ping response (ideally ).55
Testing also confirms that the adapter supports the ELM327 v1.4 command set, specifically verifying that the low-power auto-sleep function works correctly.55 This power-management function detects when the ignition is turned off and puts the adapter into a low-current sleep mode, preventing the adapter from draining the vehicle’s battery if left connected.55
Automated Regulatory Compliance Testing (SAE J1699-3)
To receive emissions certification, vehicle manufacturers must prove that their on-board diagnostic systems fully comply with CARB and EPA regulations.6 This is verified using the open-source SAE J1699 compliance software.56
Standard Definition: The SAE J1699-3 standard defines a set of automated test cases designed to verify that a vehicle's OBD-II system supports the minimum required diagnostic services and PIDs specified in SAE J1979.48
Hardware Interface Requirements: The compliance software runs on a PC and connects to the vehicle's DLC using an approved SAE J2534 Pass-Thru interface (API Version 04.04).48 While a standard J2534-1 device is typically used, a J2534-2 interface is permitted if the vehicle contains multiple 29-bit CAN ECUs that exceed J2534-1 channel capacities by utilizing "Mixed Format Frames on a CAN Network".48
Automated Testing Sequence: The software automatically commands the J2534 interface to initiate connection sequences across all legacy protocols, verifying that the vehicle's ECU responds correctly and does not cause bus collisions.48 It runs structured queries to verify:
The bitwise PID support maps (0x00, 0x20, etc.) match the sensors actually present on the vehicle.15
DTC storage (Mode 03), pending codes (Mode 07), and clearing mechanisms (Mode 04) function correctly.15
Freeze frame data (Mode 02) is correctly captured and matches the conditions that triggered the simulated DTC.15
Mode 09 vehicle metadata (including VIN, Cal ID, and CVN) is transmitted without payload corruption.2
Reporting: Software packages like DiagRA D and Silver Scan-Tool provide a user-friendly interface to run the J1699 engine and generate formatted compliance reports.59 These XML or PDF reports document any failures or timing violations.59 This automated testing process is required for a vehicle to receive OBD-II emissions certification, ensuring that any standard, retail OBD-II scan tool can communicate with the vehicle.1
Conclusions
A complete diagnostic evaluation of legacy petrol vehicles manufactured between 1990 and 2010 requires a solid understanding of both physical-layer electronics and engine physics.1 The transition from legacy, single-wire serial protocols to differential CAN-bus networks changed how diagnostic tools interact with vehicles, requiring precise timing and voltage control.8
Furthermore, effective troubleshooting in this era relies on combining mathematical models—such as volumetric efficiency and calculated load—with real-time sensor telemetry.21 By comparing calculated airflow values with actual oxygen sensor switching rates and fuel trim trends, automotive engineers can systematically isolate vacuum leaks, exhaust restrictions, and sensor degradation without relying on guesswork.28 Finally, utilizing hardware-in-the-loop simulators and standardized SAE J1699 compliance testing ensures that both vehicle ECUs and aftermarket diagnostic tools remain stable, accurate, and fully compliant with environmental regulations.12
Works cited
Clemson Vehicular Electronics Laboratory: On Board Diagnostic Systems, accessed on June 2, 2026, https://cecas.clemson.edu/cvel/auto/systems/OBD.html
What Is OBDII? History of On-board Diagnostics (OBD) - Geotab, accessed on June 2, 2026, https://www.geotab.com/blog/obd-ii/
On-board diagnostics - Wikipedia, accessed on June 2, 2026, https://en.wikipedia.org/wiki/On-board_diagnostics
OBD PIDs | PDF - Scribd, accessed on June 2, 2026, https://www.scribd.com/document/674164999/OBD-PIDs-1
Unlocking On-Board diagnostics: A Guide to OBD 2 Protocol - Embien Technologies, accessed on June 2, 2026, https://www.embien.com/automotive-insights/on-board-diagnostics-a-comprehensive-guide-to-obd-2-protocol
Introduction to the OBD-II Standard - Kvaser, accessed on June 2, 2026, https://kvaser.com/about-can/can-standards/introduction-to-obd-ii/
J1850 VPWM ECU Simulator Overview | PDF | Computer Science - Scribd, accessed on June 2, 2026, https://www.scribd.com/document/518914725/oe91c1300
OBD2 Protocols Explained. CAN, ISO, J1850 and More - OBD Experts, accessed on June 2, 2026, https://www.obdexperts.com/obd2-protocols-explained-can-iso-j1850-and-more/
RAPIDSEA OBD2 Protocol Stack - Avail Diagnostic over OBD CAN bus, accessed on June 2, 2026, https://www.rapidseasuite.com/obd2-protocol-stack
Legacy OBD2 Protocols Guide: KWP2000, ISO9141 & CAN, accessed on June 2, 2026, https://obd-cable.com/legacy-obd2-protocols-guide/
How Do You Fix OBD Communication Failure - Solo Auto Electronics, accessed on June 2, 2026, https://www.solopcms.com/blog/understanding-obd-communication-failures/
ECUsim 2000 OBD Simulator, accessed on June 2, 2026, http://magento-test.scantool.net/ecusim-2000/
endurodave/OBDII-Adapter-Software: OBDII adapter source code and schematic for automotive diagnostic vehicle communication. - GitHub, accessed on June 2, 2026, https://github.com/endurodave/OBDII-Adapter-Software
Automotive ECU Simulator OBD Simulator for Passenger Cars ELM327 Development | eBay, accessed on June 2, 2026, https://www.ebay.com/itm/364434812050
OBD-II PIDs - Wikipedia, accessed on June 2, 2026, https://en.wikipedia.org/wiki/OBD-II_PIDs
OBD-II PIDs - Grokipedia, accessed on June 2, 2026, https://grokipedia.com/page/OBD-II_PIDs
J1979 : E/E Diagnostic Test Modes - SAE International, accessed on June 2, 2026, https://www.sae.org/standards/j1979-e-e-diagnostic-test-modes
OBD II Generic PID Diagnosis - MOTOR, accessed on June 2, 2026, https://www.motor.com/magazine-summary/obd-ii-generic-pid-diagnosis-september-2007/
OBD-II J1979 PID Listing - DashLogic, accessed on June 2, 2026, https://www.dashlogic.com/docs/technical/obdii_pids
OBD-II PIDs and Engine RPM Formula | PDF | Vehicle Technology - Scribd, accessed on June 2, 2026, https://www.scribd.com/document/814472164/OBD-II-PIDs-OBD-II-Resource
Load Control and Calculation - Tuner Tools, accessed on June 2, 2026, https://tunertools.com/pages/load-control-and-calculation
Volumetric Efficiency vs. Fuel Tri - AESwave.com, accessed on June 2, 2026, https://www.aeswave.com/blog/ATG-Volumetric-Efficiency-app.html
OBD II J1979, accessed on June 2, 2026, https://help.emtronaustralia.com.au/emtune/Newtopic2.html
engine load - ScannerDanner Forum, accessed on June 2, 2026, https://www.scannerdanner.com/forum/scannerdanner-book-questions-and-discussion/2429-engine-load.html
Calculated Load vs. Absolute Load - ScannerDanner Forum, accessed on June 2, 2026, https://www.scannerdanner.com/forum/diagnostic-tools-and-techniques/599-calculated-load-vs-absolute-load.html
A Guide for Live Data - Innova, accessed on June 2, 2026, https://www.innova.com/blogs/diagnostics-101/a-guide-for-live-data
Theory: Speed-Density - Moates, accessed on June 2, 2026, https://shop.moates.net/pages/theory-speed-density
Volumetric Efficiency Test and Diagnostics, accessed on June 2, 2026, https://atleducation.org/wp-content/uploads/curriculum/bosch/Volumetric%20Efficiency%20Training/Advanced%20with%20Math/VE%20Advanced%207.21.18.pdf
VE101 - Tuner Tools, accessed on June 2, 2026, https://tunertools.com/pages/ve101
Driveability Corner | The Engine Displacement Matrix | MOTOR Magazine, accessed on June 2, 2026, https://www.motor.com/magazine-summary/driveability-corner-december-2003/
Driveability Corner | Fuel Delivery | Airflow | Load | MOTOR Magazine, accessed on June 2, 2026, https://www.motor.com/magazine-summary/driveability-corner-august-2010/
Driveability Corner | Volumetric Efficiency | MOTOR Magazine, accessed on June 2, 2026, https://www.motor.com/magazine-summary/driveability-corner-october-2010/
obdgpslogger/doc/mpg-calculation at master - GitHub, accessed on June 2, 2026, https://github.com/oesmith/obdgpslogger/blob/master/doc/mpg-calculation
Oxygen Sensors - Part One - autotechnician - servicing the independent workshop, accessed on June 2, 2026, https://autotechnician.co.uk/oxygen-sensors-part-one/
Oxygen Sensor Problem Diagnosis and Information - Auto Parts Direct To You, accessed on June 2, 2026, https://apdty.com/blogs/news/oxygen-sensor-problem-diagnosis-and-information
Complete Guide to P0171 - Fuel Trim System Lean (Bank 1): Symptoms, Fix, Diagnose, accessed on June 2, 2026, https://www.foxwelldiag.com/blogs/car-diagnostic/p0171-fuel-trim-system-lean-bank-1-symptoms-fix-diagnose
Troubleshooting Oxygen Sensors - Walker Products, accessed on June 2, 2026, https://www.walkerproducts.com/o2-sensor-training-guide/troubleshooting-oxygen-sensors/
Reading O2 sensor voltage ranges in Live Data - Innova, accessed on June 2, 2026, https://www.innova.com/blogs/fix-advices/reading-o2-sensor-voltage-ranges-in-live-data
FIXED!!** 2000 Ford f550 chassis with 6.8 no codes, wont pass obd monitors, accessed on June 2, 2026, https://www.scannerdanner.com/forum/post-your-repair-questions-here/5986-2000-ford-f550-chassis-with-6-8-no-codes-wont-pass-obd-monitors.html
P0171 Code: System Too Lean Causes & Fixes (2026 Guide) - Rohnert Park Transmission, accessed on June 2, 2026, https://rohnertparktransmission.com/blog/p0171-system-too-lean-code-guide
[FIXED] Fuel Trims Analyzing - Pending Lean Codes - ScannerDanner Forum, accessed on June 2, 2026, https://scannerdanner.com/forum/post-your-repair-questions-here/1903-fixed-fuel-trims-analyzing-pending-lean-codes.html
Code P0171 - System Too Lean: Symptoms, causes, common problems, diagnostic, accessed on June 2, 2026, https://www.samarins.com/diagnose/p0171.html
P0171 – Fuel trim. System too lean (bank 1) - OBDeleven, accessed on June 2, 2026, https://obdeleven.com/p0171
How Do I Diagnose P0171? : r/askcarguys - Reddit, accessed on June 2, 2026, https://www.reddit.com/r/askcarguys/comments/duwmm2/how_do_i_diagnose_p0171/
ECUsim 2000 - OBD Solutions, accessed on June 2, 2026, https://www.obdsol.com/solutions/development-tools/obd-simulators/ecusim-2000/
J1699/3_202104 : Vehicle OBD II Compliance Test Cases - SAE International, accessed on June 2, 2026, https://www.sae.org/standards/j16993_202104-vehicle-obd-ii-compliance-test-cases
Multiple Protocol OBD ECU Simulator-Microport | PEAK System Exclusive Distributor in Taiwan | CAN Bus Solutions Expert, accessed on June 2, 2026, https://www.microport.com.tw/en/prod/OBD-II-Calibration-and-Diagnostics/OBD-II-ECU-Simulator/Multiple-Protocol-OBD-ECU-Simulator.html
car-diagnostics · GitHub Topics, accessed on June 2, 2026, https://github.com/topics/car-diagnostics
Ircama/ELM327-emulator: ELM327 Emulator for testing software interfacing OBDII via ELM327 adapter supporting multi-ECU simulation - GitHub, accessed on June 2, 2026, https://github.com/ircama/ELM327-emulator
ELM327-emulator - PyPI, accessed on June 2, 2026, https://pypi.org/project/ELM327-emulator/
obd-ii · GitHub Topics, accessed on June 2, 2026, https://github.com/topics/obd-ii?l=c&o=asc&s=forks
langroodi/OBD-II-Emulator - GitHub, accessed on June 2, 2026, https://github.com/langroodi/OBD-II-Emulator
5 Best OBD-II apps 2025 | Works for all ELM327 - YouTube, accessed on June 2, 2026, https://www.youtube.com/watch?v=lffP3B9b3lc
J1699 Project on SourceForge, accessed on June 2, 2026, https://j1699-3.sourceforge.net/
Module Compliance Testing - EnGenius, LLC, accessed on June 2, 2026, http://www.engenius.com/module_compliance.htm
J1699/3_202104: Vehicle OBD II Compliance Test Cases - SAE Mobilus, accessed on June 2, 2026, https://saemobilus.sae.org/standards/j16993_202104-vehicle-obd-ii-compliance-test-cases
Silver Scan-Tool™ - ASAM e.V., accessed on June 2, 2026, https://www.asam.net/members/product-directory/detail/silver-scan-tooltm/
DiagRA® D, accessed on June 2, 2026, http://www.kinsco.co.kr/common/files/cadal/Flyer_DiagRA_D_eng_R.pdf
OBD Certification Public Access - Alliance for Automotive Innovation, accessed on June 2, 2026, https://portal.autosinnovate.org/obd-certification-public-access/
