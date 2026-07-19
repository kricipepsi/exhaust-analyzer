# Diagnostic Protocol for Separating Mechanical Compression Loss, Ignition Misfires, and Internal Coolant Intrusion

## Comparative Framework and Discriminating Power

Distinguishing between mechanical compression loss, pure ignition misfire, and internal coolant intrusion presents a significant challenge in modern automotive diagnostics, as these faults generate highly overlapping symptoms, including cylinder misfire codes, rough idling, power loss, and visible exhaust emissions. A systematic, multi-tiered approach is required to isolate these root causes. Rather than executing invasive teardowns, diagnostic engineers utilize a strategic combination of non-invasive digital screening, dynamic in-cylinder pressure analysis, and chemical exhaust evaluation.

To establish an optimized diagnostic sequence, candidate measurements are evaluated and ranked based on their discriminating power (the scientific certainty with which a test isolates a single root cause) multiplied by their practicality (the accessibility of the equipment, required labor time, and complexity of execution in a standard workshop environment).

| Diagnostic Measurement                                | Primary Separation Capacity                                                                                                         | Discriminating Power (1-10) | Practicality (1-10) | Weighted Index (Power × Practicality) | Feasibility Tier                                 |
| :---------------------------------------------------- | :---------------------------------------------------------------------------------------------------------------------------------- | :-------------------------- | :------------------ | :------------------------------------ | :----------------------------------------------- |
| **Cooling System Headspace Gas Analysis**             | Identifies coolant-combustion breaches, separating head gasket failures from ignition or purely mechanical cylinder sealing issues. | 9                           | 9                   | 81                                    | Tier (b) - 5-gas analyzer or Tier (c) - chemical |
| **OBD-II Mode $06 and Freeze-Frame Diagnostics**      | Localizes the active fault to a specific cylinder and maps occurrences to engine load, temperature, and starting transients.        | 8                           | 10                  | 80                                    | Tier (a) - Generic OBD-II live data              |
| **Dynamic In-Cylinder Pressure Transducer Analysis**  | Directly isolates physical gas sealing failures (valves, piston rings, timing) from pure ignition or fuel delivery faults.          | 10                          | 7                   | 70                                    | Tier (c) - Oscilloscope and transducer           |
| **Two-Point (Idle → 2500 RPM) Tailpipe HC Delta**     | Separates vacuum-dependent valve seal seeping from continuous piston-ring oil blow-by and persistent ignition misfires.             | 8                           | 8                   | 64                                    | Tier (b) - Existing 5-gas analyzer               |
| **Physical Cylinder Leak-Down and Compression Tests** | Confirms and pinpoints localized leakage paths (valves versus rings versus cylinder head boundaries).                               | 9                           | 7                   | 63                                    | Tier (c) - Traditional workshop tools            |
| **Relative Compression via Starter Current Draw**     | Rapidly screens for mechanical cylinder imbalance during cranking before conducting invasive testing.                               | 7                           | 9                   | 63                                    | Tier (c) - Current clamp and oscilloscope        |
| **Oil- versus Fuel-Derived HC Speciation**            | Chemically distinguishes heavy lubricating oil molecules from volatile raw fuel hydrocarbons.                                       | 9                           | 2                   | 18                                    | Tier (d) - Laboratory-only                       |

The most reliable, non-invasive combination of measurements to separate this confusable cluster comprises three distinct tests: OBD-II Mode $06 misfire and freeze-frame tracking to establish the environmental conditions of the failure, cooling system headspace gas analysis to rule in or out a coolant-combustion breach, and dynamic in-cylinder pressure transducer mapping to physically separate mechanical compression loss from an ignition-source misfire.

## Physical Rationale and Chemical Mechanisms

### Combustion Dynamics and Sealing Breaches

The diagnostic separation of these three root causes is governed by the physical principles of thermodynamics, fluid dynamics, and chemical oxidation. An internal combustion engine relies on a sealed chamber to convert thermal energy into mechanical work. During the compression stroke, the physical mass of the trapped fuel-air charge must remain constant.

When a mechanical sealing failure occurs (such as a burnt exhaust valve, broken piston rings, or incorrect valve timing), gas mass escapes the cylinder. The mass flow rate of gas escaping through a physical leak is driven by the pressure differential between the cylinder and the external manifold or crankcase, and can be mathematically modeled using the orifice flow equation:

$$\\dot{m}*{\\text{leak}} = C\_d A*{\\text{leak}} P\_{\\text{cyl}} \\sqrt{\\frac{\\gamma}{R T\_{\\text{cyl}}} \\left( \\frac{2}{\\gamma+1} \\right)^{\\frac{\\gamma+1}{\\gamma-1}}}$$

Where $C\_d$ is the discharge coefficient, $A\_{\\text{leak}}$ is the cross-sectional area of the physical leak, $P\_{\\text{cyl}}$ is the in-cylinder pressure, $T\_{\\text{cyl}}$ is the in-cylinder temperature, $\\gamma$ is the specific heat ratio, and $R$ is the specific gas constant. Because the leakage rate is directly proportional to the in-cylinder pressure $P\_{\\text{cyl}}$, the rate of mass loss rises exponentially as the piston approaches Top Dead Center (TDC), resulting in a severe drop in peak compression pressure and a characteristic distortion of the expansion stroke pressure curve.

In a pure ignition misfire, the physical seal of the cylinder remains completely intact, preserving normal compression pressures during cranking. Because the fuel-air charge fails to ignite, 100% of the intake air and fuel is pumped directly into the exhaust system. This results in a massive tailpipe emission spike where raw hydrocarbons (HC) and unconsumed oxygen ($O\_2$) rise simultaneously. Under normal, healthy combustion conditions, oxygen is fully consumed, keeping tailpipe $O\_2$ levels below 0.5%. During an ignition misfire, the unburned oxygen concentration in the exhaust stream escalates dramatically. On a four-cylinder engine, a complete single-cylinder misfire introduces a predictable oxygen spike of approximately 5% (25% of the atmospheric oxygen level of 20.9%) into the exhaust manifold, providing an immediate thermodynamic indicator of a non-combustion event.

An internal coolant breach represents a unique physical crossover between the high-pressure combustion chamber and the low-pressure, closed-loop cooling system. The cooling system is regulated by a radiator cap to operate at a stable pressure, typically around 15 psi. During the combustion stroke, peak cylinder pressures easily exceed 500 psi under load. This massive pressure differential forces combustion products (primarily carbon dioxide, $CO\_2$, and partially burned hydrocarbons, HC) past the breached head gasket or cylinder head crack and into the cooling water jacket. Under deceleration or starting conditions, the pressure gradient reverses; the high intake manifold vacuum (exceeding 20 in-Hg) draws liquid coolant into the combustion chamber.

### Thermal Degradation of Coolant and Cylinder Cleansing

Automotive coolant typically consists of a 50% by volume solution of ethylene glycol ($C\_2H\_6O\_2$) in distilled water, supplemented by organic or inorganic corrosion inhibitors. The ASTM D3306 standard regulates these coolants, restricting impurities such as chlorides to \< 25 ppm and sulfates to \< 50 ppm to prevent electrolyte-driven corrosion. When this water-glycol mixture is drawn past a head gasket breach into the combustion chamber, it undergoes thermal cracking and partial oxidation under the extreme heat of combustion (\> 2000 K):

$$\\text{C}\_2\\text{H}\_6\\text{O}\_2 + \\text{O}\_2 \\xrightarrow{\\Delta} \\text{HOCH}\_2\\text{CHO} (\\text{Glycolaldehyde}) \\rightarrow \\text{HCHO} (\\text{Formaldehyde}) + \\text{CO} + \\text{H}\_2\\text{O}$$

The high water content of the coolant cannot support combustion and rapidly vaporizes into superheated steam. This steam expands through the exhaust system, condensing upon exiting the tailpipe as a dense, lingering white smoke plume that is physically distinct from the rapidly dissipating water vapor of a healthy cold-start engine. The partial oxidation of ethylene glycol yields volatile organic intermediates, including glycolaldehyde and formaldehyde, which possess a sweet, acrid aroma.

In addition to tailpipe emissions, this steam expansion acts as a solvent inside the combustion chamber. Over multiple operating cycles, the localized steam injection strips away the carbon soot and fuel-lacquer deposits that naturally coat the piston crown and cylinder head. Borescopic inspection of a cylinder experiencing active coolant intrusion reveals a clean, bright, metallic piston surface, whereas healthy cylinders exhibit a dull, dark carbon layer. This steam-cleaning effect serves as a highly reliable visual marker for isolating a localized cylinder boundary breach.

## System Architecture Pre-Gates and Acquisition Protocol

### Pre-Gate Requirements

Before initiating the physical diagnostic protocol, the vehicle and shop equipment must satisfy specific architectural pre-gates to ensure data integrity and technician safety:

  * **OBD-II Interface Compatibility:** The engine control unit (ECU) must support standard OBD-II CAN-bus protocols (specifically SAE J1979/ISO 15765-4) to allow standardized access to Mode $06 diagnostic monitors and freeze-frame parameters.
  * **Physical Cooling System Access:** The engine design must include a removable radiator cap or a pressurized expansion tank neck to allow the direct insertion of headspace sampling adapters. Vehicles utilizing non-pressurized overflow bottles with sealed radiators require specialized inline cooling hose adapters to capture headspace gases.
  * **Physical Port Accessibility:** The cylinder head must allow the removal of spark plugs or glow plugs without requiring the disassembly of structural engine components or the intake manifold. If direct-injection fuel rails or complex intake plenums block access to the plug wells, auxiliary diagnostic pathways (such as relative compression testing) must be used as a pre-screening phase before executing invasive dynamic transducer tests.

### Multi-Phase Diagnostic Test Maneuver

Once the pre-gates are verified, the technician executes a structured, multi-phase diagnostic test maneuver to gather raw physical and chemical data:

#### 1\. Cold Start Phase

  * **State and Soak:** The vehicle must undergo an overnight cold soak, ensuring that the engine block, oil, and coolant have stabilized at ambient workshop temperature (\< 30° C).
  * **Acquisition:** Connect the OBD-II diagnostic tool and start the engine. Immediately record the live Mode $06 misfire counters (MID A2 through MID A7 for cylinders 1 through 6) and observe the tailpipe for visible emissions.
  * **Maneuver Target:** If a severe misfire occurs during the first 60 to 120 seconds and then completely stabilizes, accompanied by white exhaust steam and a sweet smell, the test records a preliminary confirmation of coolant pooling in the cylinder overnight.

#### 2\. Warm-Up Phase

  * **Acquisition:** Run the vehicle under light load (e.g., a simulated dyno run or road test) until the engine coolant temperature reaches its full operating thermal state (85° C to 95° C). This stabilizes thermal expansion across the head gasket boundaries and ensures the catalytic converter is fully active (\> 300° C light-off temperature).

#### 3\. Cooling System Headspace Sniff Test

  * **State:** Engine fully warmed up and idling at standard operating temperature.
  * **Procedure:** Carefully relieve the pressure in the cooling system and remove the radiator or expansion tank cap. Install a physical block-test chamber or a sealed dual-chamber funnel to prevent liquid coolant from entering the gas sampling line. Insert the probe of a calibrated 5-gas analyzer into the air headspace above the coolant level.
  * **Maneuver:** Run the engine at idle for 2 minutes, then perform three rapid throttle snaps to 2500 RPM, holding each snap for 5 seconds. Record the peak hydrocarbon (HC) concentration in parts per million (ppm).

#### 4\. Dynamic In-Cylinder Pressure Transducer Mapping

  * **State:** Engine warm, fuel system completely disabled.
  * **Procedure:** Remove the fuel pump fuse or relay and crank the engine until the residual fuel pressure in the rail is completely exhausted, preventing engine start-up. Remove the ignition coil and spark plug from the target cylinder identified by the Mode $06 misfire logs. Install a high-speed pressure transducer (e.g., Pico TA388 or WPS500X) into the spark plug well using a brass compression hose adapter. Connect the transducer output to Channel A of an oscilloscope.
  * **Cranking Sweep:** Crank the engine for 5 seconds with the throttle held wide open (100% Throttle Position Sensor). Record the raw pressure waveform.
  * **Running Idle Sweep:** Reinstall the ignition and fuel injection components on the remaining healthy cylinders. Start the engine and allow it to run at idle (700 - 900 RPM) with the transducer installed in the isolated, non-firing cylinder. Capture a minimum of 50 consecutive combustion cycles.

#### 5\. Two-Point Exhaust Emission Test

  * **State:** Engine warm, tailpipe exhaust probe inserted at least 300 mm into the tailpipe.
  * **Step 1 (Idle):** Record stable gas values (HC, $CO\_2$, $O\_2$, CO, and Lambda) at a warm idle of 750 RPM for 60 seconds.
  * **Step 2 (Elevated):** Accelerate the engine to a sustained 2500 RPM under zero load. Hold this speed for 60 seconds. Record the transient hydrocarbon spike and the subsequent steady-state gas concentrations.

## Expected Signatures and Quantitative Decision Bands

The execution of the diagnostic protocol yields highly specific quantitative signatures. The table below outlines the precise numeric thresholds, ranges, and behavioral trends that isolate each of the three root causes compared to a healthy baseline engine.

| Diagnostic Parameter                          | Healthy Engine Baseline                           | Mechanical Compression Loss                                      | Pure Ignition Misfire                                            | Coolant Intrusion (Head Gasket Breach)                           |
| :-------------------------------------------- | :------------------------------------------------ | :--------------------------------------------------------------- | :--------------------------------------------------------------- | :--------------------------------------------------------------- |
| **Cranking Compression (transducer-derived)** | \> 90 psi; symmetric decompression ramp           | \< 90 psi; expansion ramp "leaning" \> from TDC                  | Normal ( \> 90 psi); perfectly symmetric pressure towers         | Normal to slightly low cranking compression                      |
| **Running Compression at Idle**               | 65 - 90 psi; exhaust plateau pressure \<          | \< 65 psi; exhaust plateau rises \> (burnt exhaust valve)        | Normal (65 - 90 psi); exhaust plateau matches baseline           | Normal running compression; high cycle-to-cycle peak variance    |
| **Cooling Headspace Hydrocarbons (HC)**       | 0 ppm ($CO\_2$ chemical test remains bright blue) | Normal (0 ppm; chemical fluid remains blue)                      | Normal (0 ppm; chemical fluid remains blue)                      | \> 50 ppm (often exceeds 500 ppm); chemical fluid turns yellow   |
| **Tailpipe Hydrocarbons (HC)**                | \< 100 ppm (post-catalytic converter)             | Marginally elevated (100 - 300 ppm); fails to combust completely | \> 500 ppm per misfiring cylinder                                | Normal to slightly elevated                                      |
| **Tailpipe Oxygen ($O\_2$)**                  | \< 1%                                             | Slightly elevated (1 - 2%)                                       | **Elevated to \~ 5%** (for a single cylinder misfire on a 4-cyl) | Normal to slightly elevated                                      |
| **Tailpipe Carbon Dioxide ($CO\_2$)**         | 14 - 15% (high efficiency)                        | Decreases slightly (10 - 12%)                                    | **Drops by \~ 2-4%** (to 10 - 12% on a 4-cyl engine)             | Normal to marginally lower                                       |
| **Mode $06 Misfire Behavior**                 | 0 or near 0 counts                                | Constant misfires at idle; decreases at higher engine RPM        | Constant or escalating misfires under load or high RPM           | Severe misfires on startup (\< 30s); completely clears when warm |

## Diagnostic Uncertainty and Failure Conditions

While these quantitative ranges provide high diagnostic accuracy, several real-world failure conditions can obscure the signatures:

  * **Catalytic Converter Oxidation Masking:** A highly efficient catalytic converter can oxidize massive volumes of raw hydrocarbons and carbon monoxide, converting them to carbon dioxide and water before they reach the tailpipe. If a vehicle exhibits a single-cylinder ignition misfire, the tailpipe HC reading may initially register under 100 ppm due to catalytic conversion, masking the fault. To bypass this masking effect, the diagnostic engineer must verify the exhaust oxygen ($O\_2$) level; because the converter cannot consume oxygen without a corresponding fuel reduction, the tailpipe $O\_2$ will remain elevated at \~ 5%, signaling an unburned charge. Alternatively, raw gas samples must be drawn pre-catalyst via the upstream oxygen sensor port.
  * **Uniform Mechanical Cylinder Wear:** Relative compression tests via starter current draw rely on comparing one cylinder's compression peak to the adjacent cylinders. If an engine has suffered uniform, severe cylinder bore wear, bore washing from fuel dilution, or multi-cylinder ring wear, the starter current peaks will remain completely uniform, registering a relative contribution score of \> 90% (false pass). To resolve this, absolute compression pressure must be measured directly using an in-cylinder pressure transducer.
  * **Microscopic and Thermal-Dependent Gasket Breaches:** A cylinder head gasket leak may initially present as a microscopic fissure that remains completely sealed when the engine block is cold or idling. Under these conditions, the cooling headspace sniff test and chemical block test will yield false negatives. The breach only opens when the cylinder head undergoes thermal expansion under high-load operating conditions. To capture this intermittent failure, the headspace gas test must be executed immediately after a loaded road test, or with the cooling system pre-pressurized using a cooling system pressure pump to force the gases past the thermal barrier.

## Critical Signal Evaluation and Decisions

### Relative Compression Current and Voltage Ripple

  * **Decision:** Keep with strict diagnostic limitations.
  * **Justification:** Relative compression testing utilizes a high-amperage DC current clamp connected around the main battery cable. During cranking with the fuel system disabled, the starter motor draws current proportional to the mechanical torque required to compress the air charge in each cylinder. A typical four-cylinder gasoline engine draws 100 A to 200 A average current, with initial inrush currents reaching 500 A to overcome engine inertia. A weak cylinder draws less current, resulting in a distinct, repeating drop in the current peaks on the oscilloscope.
  * **Limitations:** Although this test is non-invasive and identifies cylinder imbalance in under a minute, it cannot measure absolute compression pressure. If the starter motor is worn, the battery voltage is low, or the engine exhibits uniform wear across all cylinders, the test fails to diagnose the mechanical fault. It is kept as an initial rapid screening tool, but is rejected as a standalone definitive diagnostic.

### Cylinder Leak-Down and Absolute Compression Tests

  * **Decision:** Keep as the primary localization standard.

  * **Justification:** Traditional absolute compression and leak-down tests are highly invasive but remain mathematically and physically definitive. If a cylinder exhibits low absolute compression (\< 90 psi cranking), a wet compression test is executed by introducing 5 to 10 mL of motor oil into the spark plug well. The oil acts as a physical barrier, sealing the clearance between the piston rings and the cylinder wall. If the compression pressure rises significantly during the subsequent test, it isolates the failure to worn or broken piston rings. If the compression remains unchanged, the leak-down test is executed by locking the piston at TDC compression and introducing 100 psi of compressed air. Listening to the physical escape routes of the air provides immediate localization of the fault:

  * **Throttle Body/Intake Manifold:** Leaking Intake Valve

  * **Tailpipe/Exhaust Manifold:** Leaking Exhaust Valve

  * **Crankcase Oil Filler Cap:** Piston Ring Blow-by

  * **Radiator Neck (bubbling):** Blown Head Gasket

This direct physical feedback makes the leak-down test indispensable for validating mechanical sealing boundaries.

### Snap-Throttle Transient versus Two-Point Step-Speed Analysis

  * **Decision:** Reject the Snap-Throttle transient hydrocarbon plume; Replace with the Two-Point Step-Speed Emission Test.
  * **Justification:** It is frequently claimed that a worn valve stem seal can be diagnosed by snapping the throttle open to emit a transient hydrocarbon spike on the gas analyzer. While the physical seeping of oil under vacuum is a real phenomenon, using a snap-throttle maneuver to capture this on a workshop gas analyzer is highly unreliable. Typical workshop 5-gas analyzers utilize NDIR sensors which suffer from a physical gas transport lag (the time required to pump the exhaust gas through a 3-meter sampling hose) and an optical bench stabilization delay, totaling 2 to 5 seconds. A rapid snap-throttle event produces an instantaneous surge of exhaust volume that dilutes the brief oil-burning plume before the NDIR sensor can resolve the measurement, resulting in high rates of diagnostic omission.
  * **Replacement Protocol:** The snap-throttle test is replaced by a controlled, steady-state Two-Point Step-Speed Emission Test. By holding the engine at a steady idle for 2 minutes (generating high manifold vacuum of 20 - 22 in-Hg to draw oil past the seals) and then immediately stepping to a sustained 2500 RPM, the oil-burning plume is continuously swept into the analyzer over a prolonged 30-to-60-second window. This steady flow overcomes the transport lag of the analyzer, yielding a clear, measurable hydrocarbon spike that decays back to baseline as the pooled oil is consumed. If the piston rings are worn, the hydrocarbon reading will not decay; instead, it will remain elevated or continue to rise at 2500 RPM due to continuous, load-dependent blow-by.

### Chemical Speciation of Oil-Derived and Fuel-Derived Hydrocarbons

  * **Decision:** Reject for standard automotive workshops (classified as lab-only/impractical); Keep as a theoretical scientific benchmark.
  * **Justification:** Distinguishing between engine oil combustion (valve seals or piston rings) and unburned gasoline (ignition misfires) can be achieved by measuring the spectral response ratio between a Flame Ionization Detector (FID) and a Non-Dispersive Infrared (NDIR) analyzer. Lubricating oil consists of heavy, long-chain aliphatic alkanes and complex aromatics ($C\_{15}$ to $C\_{50}$), while gasoline contains lighter, volatile compounds ($C\_4$ to $C\_8$).
  * **The Response Factor Disconnect:** An NDIR sensor calibrated to a propane ($C\_3H\_8$) standard measures infrared absorption at the 3.4 μm C-H alkane stretching band. However, heavy, branched alkanes, unsaturated compounds, and aromatic rings exhibit shifted absorption bands or lack single C-H bonds entirely, causing the NDIR sensor to underestimate the total hydrocarbon concentration of partially burned oil by up to 75% (yielding a low response factor of 0.23 to 0.44). Conversely, a hydrogen-flame FID pyrolyzes all organic carbon bonds, generating ions ($CHO^+$) proportional to the absolute number of carbon atoms, acting as a highly linear total carbon counter.
  * **Diagnostic Utility:** By evaluating the ratio:

$$\\text{Response Ratio} = \\frac{\\text{HC}*{\\text{NDIR}}}{\\text{HC}*{\\text{FID}}}$$

The diagnostic engineer can chemically identify the fuel source. A ratio close to 1.0 indicates light, paraffinic raw fuel from an ignition misfire, while a ratio below 0.4 confirms the presence of heavy, aromatic lubricating oil. However, because FID analyzers require compressed hydrogen ($H\_2$) fuel gas, specialized auxiliary air supplies, and precise thermal control, they cannot be operated in a standard workshop and are rejected for daily field diagnostics.

### Coolant-Combustion Markers and Headspace Analysis

  * **Decision:** Keep.
  * **Justification:** Checking for coolant-combustion markers is the most reliable, non-invasive method to confirm a head gasket failure or cracked cylinder head. The high combustion pressures force exhaust gases directly into the cooling system. By drawing the headspace gases from the radiator neck through a chemical block-test chamber, any carbon dioxide ($CO\_2$) present reacts with the bromothymol blue indicator fluid. The chemical reaction with carbonic acid drops the pH of the fluid, causing an immediate, highly visible color change from bright blue to yellow (or green on diesel engines).
  * **Gas Analyzer Verification:** Using a 5-gas analyzer to sniff the radiator headspace is even more sensitive, registering precise hydrocarbon concentrations. Because a sealed, healthy cooling system contains zero combustion products, any hydrocarbon reading exceeding 50 ppm in the radiator headspace provides absolute confirmation of an internal combustion-to-coolant breach, completely ruling out simple ignition misfires or isolated mechanical valve issues.

### On-Board Diagnostics Mode 06 and Freeze-Frame Data

  * **Decision:** Keep.
  * **Justification:** OBD-II Mode $06 is a continuous software monitor that tracks emissions-related components, including real-time misfire detection. The ECU detects misfires by measuring minute fluctuations in crankshaft rotational speed via the crankshaft position sensor. Every time a cylinder fails to fire, the crankshaft decelerates during that cylinder's scheduled power stroke. Mode $06 stores these raw misfire counts for each individual cylinder (using standardized Monitor IDs such as MID A2 for Cylinder 1 and MID A7 for Cylinder 6) during the current drive cycle, long before the counts exceed the statistical threshold required to illuminate the Check Engine Light.
  * **Freeze-Frame Environmental Mapping:** Freeze-frame data captures a static snapshot of critical operating parameters (Engine RPM, calculated load, engine coolant temperature, and fuel trims) at the exact millisecond the fault code is triggered. This allows the engineer to map the misfire to its physical root cause:
      * **Coolant Seepage:** If the freeze-frame records a misfire occurring exclusively at 0 MPH, at an engine coolant temperature of \< 30° C, immediately upon engine start-up, it confirms coolant has seeped past the head gasket overnight.
      * **Mechanical Loss:** If the misfire is highly active at idle (750 RPM) but completely disappears as engine speed increases to 2500 RPM under zero load, it points to mechanical compression loss. At low engine speeds, the physical duration of the compression stroke is longer (40 milliseconds at 750 RPM versus 12 milliseconds at 2500 RPM), allowing more physical air mass to escape past a leaking valve or ring. At high RPM, the piston moves too fast for significant mass loss to occur, restoring compression and clearing the misfire.
      * **Ignition Breakdown:** If the misfire is absent at idle but escalates rapidly under high engine load (high calculated load percentage) and elevated RPM, it confirms secondary ignition breakdown. Under high load, the throttle plate opens wide, increasing the density of the air charge in the cylinder. This dense air-fuel mixture increases the electrical resistance across the spark plug gap, requiring a higher ionization voltage. If the ignition coil or spark plug insulation is degraded, the spark will arc to the cylinder head wall rather than jumping the plug gap, triggering a load-dependent misfire.

## Reliability and Authority of Source Material

To establish a scientifically robust diagnostic protocol, the underlying technical evidence is classified and evaluated based on its source authority and empirical reliability:

  * **High-Authority Academic and Federal Regulatory Literature:** The detection of ethylene glycol vapor in vehicular exhaust is supported by peer-reviewed research from Yale University and the Caldecott Tunnel emissions study. This study utilized high-resolution Proton Transfer Reaction Mass Spectrometry (PTR-MS) to identify ethylene glycol vapor at mass-to-charge ratio $m/z \\ 45$ in the exhaust of vehicles operating under uphill load with compromised cooling systems. Acetaldehyde also detects at $m/z \\ 45$; however, the Yale research group isolated the glycols by simultaneously running an in-situ gas chromatograph (GC-FID) to subtract the acetaldehyde contribution, which rarely exceeded 25% of the $m/z \\ 45$ signal. This provides an exceptionally high-reliability scientific foundation for the thermal degradation of glycol in internal leaks. Additionally, chemical properties and vapor pressure curves (0.06 mm Hg at 20° C) are sourced directly from the Centers for Disease Control and Prevention (CDC) Agency for Toxic Substances and Disease Registry, ensuring undisputed accuracy.
  * **Industrial Emission Measurement Standards:** The technical principles of FID carbon-counting, selective combustion methods (utilizing non-methane cutters or NMHC removers to isolate methane from total hydrocarbons), and NDIR C-H stretching band absorption are sourced directly from Horiba Process & Environmental instrument designs. These documents represent the gold standard for global emissions regulatory compliance, ensuring the highest level of reliability for chemical speciation limits.
  * **Specialized Diagnostic Tooling and Training Developers:** Technical data regarding relative compression starter-current waveforms, AC-coupled battery voltage ripple, and dynamic in-cylinder pressure transducer mapping are derived from Pico Automotive, Automotive Test Solutions (ATS), and AutoDitex engineering manuals. These organizations are the direct developers of the diagnostic hardware and software used in the field. Their empirical data regarding waveform analysis—such as the requirement that compression halfway points must fall within 20° of TDC to confirm a sealed cylinder—is highly reliable and represents the leading edge of current field diagnostics.
  * **Professional Automotive Diagnostic Publications:** Diagnostic thresholds for tailpipe gases (e.g., the 5% oxygen spike for single-cylinder misfires and the \> 50 ppm radiator headspace hydrocarbon threshold) are sourced from Motor Magazine's technical diagnostic archives and the RepairPal expert tracking database. These sources possess high practical reliability as they represent consolidated field-study data compiled by master diagnostic technicians, although they lack the formal peer-review structure of academic publications.

## Open Questions and Empirical Research Plan

### Identified Literature Gaps

Despite the depth of existing diagnostic guides, three critical gaps remain in the published literature:

  * **Cracked Synthetic Oil Response Factors:** While NDIR-to-FID response factors are well-established for standard raw fuels (ranging from 0.44 to 0.75), equivalent response factors for various synthetic oil blends (PAO, Group III, Group IV) have not been rigorously documented in workshop environments.
  * **Microscopic Thermal-Expansion Thresholds:** There is a lack of data quantifying the exact temperature gradient required to open microscopic head gasket fissures, leading to high false-negative rates during standardized cooling system pressure tests.
  * **Transient Hydrocarbon Settling Times:** Further research is required to characterize the NDIR optical bench settling time for modern, low-emission vehicles where the catalytic converter efficiency can distort the temporal mapping of a hydrocarbon surge.
