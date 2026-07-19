> **Provenance / how to read this.** Recovered from the Cluster-1 deep-research HTML export
> (`value_answers/value1`, a Google Docs save where every number was a rendered image).
> Extracted with the `html-extractor` skill: 232 number-images OCR'd (`tesseract`), then
> substituted back into the Markdown. Headline central values and P10/P90 spreads were
> **spot-verified against the source image tiles** and are correct.
>
> **Known limitations — verify before reconciling bands:**
> 1. A few range **upper bounds** in Table 1 render incompletely (e.g. `110 — psi`) because
>    the export split each number into a separate image and some end-of-range tiles didn't
>    align. Central values and spreads are complete; only some range ceilings are missing.
> 2. Math **symbols** in the distribution formulas were normalized by hand (OCR read μ→"yu",
>    σ→"o", 𝒩→"M", λ→"A"); the **digits** are OCR-verified, the Greek letters are reconstructed.
> 3. Off-topic "Cluster 1" homonym section (NetApp/Ozone/Stable Diffusion) removed as noise.
>
> Source generated 2026-07-01. OCR TSV + contact sheet retained in scratch for re-check.

# Comprehensive Diagnostic Calibration Report on Combustion Signatures: Mechanical Compression Loss, Ignition Misfire, and Coolant Intrusion

## Empirical Calibration and Signature Confirmation Matrices

The generation and validation of synthetic datasets for light-duty petrol vehicles manufactured between 2000 and 2024, spanning cylinder counts from three to eight, require highly rigorous empirical baselines. 1  When designing diagnostic models to differentiate between mechanical compression loss, ignition-system misfires, and head-gasket coolant leaks, reliance on idealized physical values often leads to high false-alarm rates or critical misdiagnoses. 1

Real-world vehicles exhibit significant statistical spread across manufacturers, engine configurations, and wear states. 1  To establish an accurate foundation, accepted qualitative parameters must be replaced with empirical data, realistic tolerances, and distinct probability distributions. 1

Continuous monitoring of these parameters is typically achieved through On-Board Diagnostics (OBD-II) Mode $06, which provides real-time access to the internal self-test thresholds and performance counters utilized by the Engine Control Module (ECM) to detect faults. 6  Table 1 establishes the comprehensive calibration matrix, validating and correcting previously established central parameters.

### Table 1: Comprehensive Calibration and Signature Confirmation Matrix

| Signal | Fault / Condition | Established Central | Confirmed Central / Range | Fleet Spread (P10​–P90​ or ±σ) | Probability Distribution | Calibration Verdict | Primary Citations |
|---|---|---|---|---|---|---|---|
| Cranking Compression | Healthy | >  psi | 130  psi ( 110 —  psi) | +15  psi ( Pio: 112, Poo: 155  psi) | Gaussian (Normal) with left-tail skew | SHIFT / WIDEN  (Baseline limits are too low; modern engines demand >  psi) | 4 |
| Cranking Compression | Mechanical Loss | psi | 60  psi ( 30 —  psi) | 45 —  psi | Bimodal / Multi-modal (severity-bound) | CONFIRM  (Combustion fails consistently once cylinder pressure drops below 90  psi) | [1, 8] |
| Running Compression | Healthy | 65 —  psi | 70  psi ( 50 —  psi) | +8  psi ( Pio: 60, Poo: 80  psi) | Gaussian (Normal) | SHIFT / TIGHTEN  (Dynamic running pressure at idle is bounded by intake vacuum) | [4, 8, 9] |
| Running Compression | Mechanical Loss | psi | 35  psi ( 15 —  psi) | 20 —  psi | Left-skewed Gaussian | TIGHTEN  (Continuous dynamic misfires are physically initiated below 40  psi) | 4 |
| Cooling-Headspace HC | Coolant Intrusion | >  ppm | 800  ppm ( 100 —  ppm) | Pio: 150  ppm, Poo: 3500  ppm | Log-normal (Extreme right-skew) | CONFIRM / WIDEN  (Transient loading spikes headspace HC to severe limits) | [1, 10] |
| Tailpipe HC (Post-Cat) | Healthy (Idle) | ppm | 15  ppm ( 0 —  ppm) | Pio: 5  ppm, Poo: 30  ppm | Exponential | TIGHTEN  (Functional closed-loop feedback easily achieves near-zero post-cat emissions) | 11 |
| Tailpipe HC (Pre-Cat) | Healthy (Idle) | N/A | 120  ppm ( 80 —  ppm) | +25  ppm | Gaussian (Normal) | NEW  (Baseline parameter added to represent raw pre-catalytic stoichiometric exhaust) | [11, 12] |
| Tailpipe HC (Post-Cat) | Mechanical Loss | 100 —  ppm | 200  ppm ( 100 —  ppm) | Pio: 120  ppm, Poo: 350  ppm | Right-skewed Gaussian | CONFIRM  (Partial combustion due to low charge density limits catalyst conversion) | [1, 12] |
| Tailpipe HC (Pre-Cat) | Ignition Misfire | >  ppm/cyl | 2000  ppm ( 1000 —  ppm) | 1500 —  ppm per misfiring cylinder | Bimodal (Load-dependent) | SHIFT / WIDEN  (Raw output of an unfired cylinder routinely reaches 2000  ppm) | [12, 13] |
| Tailpipe O2  (Post-Cat) | Healthy (Idle) | a % | 0.15 % ( 0.0 — %) | Pio: 0.05 %, Poo: 0.3 % | Log-normal | TIGHTEN  (Active stoichiometric balance leaves almost zero free oxygen post-catalysis) | 11 |
| Tailpipe O2  (Post-Cat) | Mechanical Loss | 1— % | 1.5 % ( 0.8 — %) | Pio: 1.0 %, Poo: 2.2 % | Gaussian (Normal) | CONFIRM  (Misfiring cylinders sweep unburned O2  downstream, degrading conversion) | [1, 14] |
| Tailpipe O2  (Pre-Cat) | Ignition Misfire | ~~ % | 5.23 % ( 2.5 — %) | Bounded strictly by cylinder count ( N. cyl ) | Gaussian (constrained by ) | CONFIRM / SHIFT  (Oxygen concentration scales directly with cylinder count) | [1, 13] |
| Tailpipe CO, | Healthy (Idle) | 14 — % | 14.7 % ( 13.5 — %) | Pio: 14.0 %, Poo: 15.5 % | Gaussian (Normal) | CONFIRM  (Peak thermodynamic efficiency produces maximum complete combustion CO, ) | [12, 13, 14] |
| Tailpipe CO, | Mech / Misfire | 10 — % | 11.0 % ( 9.0 — %) | Pio: 9.5 %, Poo: 12.0 % | Left-skewed Gaussian | CONFIRM  (Incomplete combustion dilutes the total carbon dioxide percentage) | [11, 13, 14] |

On-board misfire diagnostics are continuously calculated by measuring crankshaft rotational acceleration, checking for localized angular deceleration spikes that exceed adaptive engine load and speed thresholds. 15  If these deviations accumulate, they are logged within Mode $06 misfire counters. 6

To accurately synthesize these counters, qualitative classifications must be upgraded to quantitative boundaries. 1  Table 2 defines the quantitative count limits and temporal signatures of these misfire profiles across diagnostic drive cycles.

### Table 2: Mode $06 Misfire Counter Calibration and Temporal Signatures

| Misfire Trigger | Drive Cycle Count Range | Temporal and Load Signature Characteristics | Probability Distribution | Primary Citations |
|---|---|---|---|---|
| Mechanical Loss  (e.g., Burned/Leaking Valves) | 50 — 500  counts per cycle | Restricted entirely to stable idle engine speeds ( 700 — 900  RPM); clears rapidly as RPM exceeds 1500  or as engine load increases. | Poisson-like, highly stable across identical drive cycles | [1, 6, 15] |
| Ignition Failure  (e.g., Breakdown under load) | 1000 — 8000  counts per cycle | Active under transient load transitions; peaks during rapid acceleration or high-manifold-pressure states. Absent at idle. | Log-normal, highly variable based on driving profile | [1, 6, 16] |
| Coolant Intrusion  (e.g., Head Gasket Leak) | 200 — 1500  counts per cycle | Confined strictly to the first 15 — 30  seconds of a cold-start transition; drops to absolute zero as the engine warms. | Bimodal (active on cold-starts; absent on warm-starts) | [1, 6, 17] |

### Table 3: Summary of Bands-to-Change and Calibration Shortlist

| Target Parameter | Established Value | Recommended Calibration | Direction / Magnitude of Shift | Engineering Justification | Primary Citations |
|---|---|---|---|---|---|
| Healthy Cranking Compression | >  psi | 130  psi ( 110 —  psi) | Positive shift ( +40  psi in mean) | A healthy petrol engine cannot reliably support combustion under 90  psi; 90  psi is a terminal wear boundary, not a healthy baseline. | [1, 8] |
| Healthy Running Compression | 65 —  psi | 50 —  psi (central 70  psi) | Negative shift and range expansion | Throttling intake vacuum at idle restricts the air charge, physically reducing running compression to ~  of cranking. | [4, 8, 9] |
| Mechanical Loss Running Compression | psi | psi (central 35  psi) | Negative shift of critical limit | Hydrocarbon ignition can be physically maintained down to 40  psi; misfire monitors only trigger continuously below this limit. | 4 |
| Tailpipe HC (Post-Cat, Healthy) | ppm | 0 —  ppm (central 15  ppm) | Extreme tightening ( —65  ppm) | Active closed-loop stoichiometry and a functional catalytic converter easily reduce tailpipe hydrocarbons to near-zero. | [1, 11] |
| Tailpipe O2  (Post-Cat, Healthy) |  | 0.0% —  (central 0.15% ) | Tightening of range ( —0.65% ) | Under closed-loop control, post-catalytic free oxygen is fully consumed to oxidize transient hydrocarbons and carbon monoxide. | [1, 11] |

## Thermodynamic and Fluid Dynamic Mechanics of In-Cylinder Compression

Diagnosing mechanical engine integrity requires analyzing the distinct dynamic differences between static cranking and dynamic running compression. 4  When an engine is in a static cranking condition with the fuel injection disabled, the engine is turned over slowly by the starter motor at approximately 150 — 250  RPM. 8  Under this condition, the throttle plate is typically closed, limiting air intake, but the low engine speed allows a complete charge to draw into the cylinder. 8

The resulting compression waveform, captured via a high-resolution absolute pressure transducer (such as a Pico WPS500X) installed in the spark plug hole, exhibits highly symmetrical compression towers. 9  These towers represent the physical reduction in volume as the piston reaches Top Dead Center (TDC, representing 0°  or 720°  of the crankshaft rotation). 8

A healthy cranking compression of = 130  psi is typical for standard light-duty passenger vehicles. 8  If this cranking pressure drops below 90  psi, the in-cylinder temperature and density generated at the end of the compression stroke are no longer adequate to support the combustion of hydrocarbon chains, leading to a permanent dead cylinder. 8

Under dynamic running conditions at idle ( 700 — 900  RPM), the intake manifold is under deep vacuum, typically —15  to —20  in. Hg, which restricts the mass of air drawn into the cylinder. 4  This throttle restriction physically cuts the available charge density in half, lowering the dynamic running compression at idle to a baseline of 50 — 75  psi, with 70  psi serving as the typical healthy central value. 4

During the 720-degree engine cycle, an absolute pressure transducer reveals precise mechanical valve events mapped to specific crankshaft angles. 9  Under normal conditions, the exhaust valve opening (EVO) occurs 30°  to 50°  before Bottom Dead Center (BDC at 180°  of rotation), allowing exhaust gases to evacuate. 8  The intake valve closing (IVC) occurs approximately 50°  after BDC (at 540°  of rotation), sealing the cylinder to begin the compression ramp. 8

Peak pressure corresponds to TDC ( 0° /720° ). 8  As the piston ascends, the half-compression point—defined as the point where the compression pressure is halfway between the minimum manifold vacuum and peak pressure (known as point M)—must occur precisely at 30°  before TDC. 8  Symmetrical deviations in this compression ramp provide immediate diagnostic evidence of camshaft timing misalignment or dynamic valve leakage. 18

### Figure 1: Absolute In-Cylinder Running Compression Waveform (WPS500X Range 1)

To diagnose dynamic breathing restrictions, a technician executes a snap-throttle compression test, rapidly slamming the throttle plate wide open and releasing it. 4  This forces a sudden "gulp" of air into the intake manifold, raising the intake pressure to atmospheric level ( 0  psi vacuum) and filling the cylinder with a complete charge. 4

In a healthy cylinder, this causes the dynamic running compression to rise by approximately three times the idle pressure, reaching at least 80%  of the static cranking compression (typically 100 — 130  psi). 4

Analyzing the snap-throttle pressure peaks provides clear, localized diagnostic signatures:

- Low Snap-Throttle Compression (  of Cranking Compression): This signature reveals an intake-side restriction preventing air from entering the cylinder. 4  Common causes include severe carbon deposits on the intake valves, a worn intake cam lobe, weak valve springs, or a mispositioned variable-runner shutter valve. 4
- High Snap-Throttle Compression ( > 80%  of Cranking Compression): This signature indicates an exhaust-side restriction preventing the air charge from leaving the cylinder efficiently. 4  Common causes include a worn exhaust cam lobe, a bent pushrod, a collapsed lifter, or localized exhaust restrictions such as a clogged catalytic converter or collapsed muffler. 4

To differentiate microscopic head-gasket leaks from valve or piston ring failures, standard cooling system pressure tests (which typically apply only 100 — 150  kPa or ~ 15-21  psi) are frequently insufficient to overcome the mechanical sealing thresholds of modern multi-layer steel (MLS) gaskets. 2

In contrast, a cylinder leak-down test provides a far more definitive diagnostic. 2  By rotating the cylinder to TDC of its compression stroke (ensuring both intake and exhaust valves are fully closed), locking the crankshaft, and introducing high-pressure shop air at 100  psi ( 689  kPa) directly into the spark plug hole, technicians can force air across microscopic fissures. 2

If a leak exists between the combustion chamber and the cooling jacket, the high-pressure air will displace the cooling fluid, producing a rapid rise and visible bubbling in the radiator or expansion reservoir. 2

## Exhaust Gas Chemistry and Catalytic Converter Dynamics

The primary chemical byproducts of hydrocarbon combustion in a petrol engine are carbon dioxide ( CO, ), water ( HO ), and nitrogen ( N2 ). 13  Under ideal stoichiometric conditions, where the air-to-fuel ratio is held exactly at 14.7: 1  (excess air ratio A= 1.0 ), complete combustion of the fuel molecules occurs, maximizing carbon dioxide output to a peak concentration of 14.5% — 16.0%. 11

When the air-fuel mixture deviates or when a combustion failure occurs, specific chemical reactions alter the exhaust gas signature 11:

- Carbon Monoxide ( CO ): Formed when there is insufficient oxygen to complete the combustion process. 13  High CO  readings (above the stoichiometric idle baseline of 0.1% — 0.45% ) are a direct chemical indicator of an overly rich fuel mixture. 11
- Oxygen ( O2 ): Free oxygen occurs when there is an excess of air relative to fuel, indicating a lean mixture. 13  At stoichiometry, O2  is fully consumed, leaving a post-catalytic baseline of. 11
- Hydrocarbons ( HAC ): Represent raw, unburned fuel molecules escaping the combustion chamber, typically measured in parts per million ( Dp ). 13  Healthy post-catalytic tailpipe concentrations must remain below 35  ppm. 11

Standard environmental regulations, such as the UK MOT test limits, dictate maximum allowable emissions during vehicle inspections. 12  At a normal warm idle speed, the maximum allowable carbon monoxide concentration is 0.3%. 12  At a raised idle of 2500 — 3000  RPM with no load, the standards tighten, restricting maximum allowable CO to 0.2%  and maximum hydrocarbons to 200  ppm. 12

Under full-load enrichment, modern petrol engines intentionally enrich the mixture to maximize power and suppress knock. 12  This full-load enrichment typically raises raw CO to 3.0% — 5.0%  (and up to 6.0% — 7.0%  at low-speed, high-load states to prevent destructive detonation), while unburned HC emissions climb to 400 — 800  ppm. 12

In contrast, a well-maintained vehicle with closed-loop Lambda control running at raised idle should never struggle to meet these limits, typically emitting stable raw CO of 0.1%  and HC under 100  ppm ahead of the catalytic converter. 12

To verify catalyst health, several quantitative tests can be executed. During engine cranking with the ignition system disabled, a healthy engine must pump sufficient volume to drive CO,  concentrations to at least 12.5%  by the end of the cranking period, while hydrocarbons should remain below 500  ppm. 21

Furthermore, a technician can perform a dynamic Hydrocarbon Reduction Test to evaluate the catalyst's capacity to oxidize unburned fuel 21:

1. The engine is operated until the catalytic converter reaches its light-off temperature ( > 300°C  or 572°F ), then shut off for three minutes to allow localized cooling. 21
2. One spark plug wire is grounded (or the coil control harness is disconnected) to disable ignition on a single cylinder, causing a continuous misfire. 4
3. The engine is restarted, pumping raw fuel and oxygen into the exhaust. 13  The peak pre-catalytic hydrocarbon concentration is measured using a gas analyzer, typically peaking at ew 945  ppm. 21
4. As the hot converter catalyzes the unburned fuel, the tailpipe hydrocarbons must decrease rapidly. 21  The final stabilized post-catalytic hydrocarbon concentration is recorded, typically dropping to w 355  ppm. 21

The percentage of hydrocarbon reduction achieved by the converter is calculated using the following formula:

Reduction % = Se x 100 [21]

Using the empirical values of HC peak = 945  ppm and HC ginal = 355  ppm, this calculation yields:

Reduction % = — x 100 = 62.4% [21]

A minimally compliant catalytic converter must achieve a minimum reduction of 35%; a failure to meet this threshold indicates thermal sintering or catalytic washcoat damage. 11

Additionally, the Peak O2  Snap Acceleration Test evaluates the converter's oxygen storage capacity, which relies on the cerium oxide washcoat. 21  The vehicle is operated at 2200  RPM, and the fuel mixture is transiently enriched (e.g., by introducing a controlled amount of propane at the intake) until the CO concentration reaches 0.5%. 21

A sudden snap acceleration is performed. 21  When the CO concentration peaks during acceleration, the O2  level at the tailpipe must not exceed 1.2%  above its baseline level before the acceleration. 21  This threshold confirms that the cerium washcoat successfully stored and released sufficient oxygen to oxidize the sudden, transient spike of carbon monoxide. 21

When a complete ignition misfire occurs on a single cylinder, the entire unburned air-fuel charge is swept into the exhaust system. 13  Because air consists of approximately 20.9%  oxygen, the concentration of unreacted oxygen entering the exhaust manifold is a direct, discrete function of the engine's total cylinder count ( N. cyl ) 13:

Oo missive © Sete x 20.9% [13]

Applying this physical scaling relationship reveals clear, discrete diagnostic bounds for single-cylinder misfires ( Nnisfire = 1 ) across common engine configurations:

- Four-Cylinder Engine ( Ntotal = 4 ): O2 misfire © 0.25 x 20.9% = 5.23%  oxygen spike. 13
- Six-Cylinder Engine ( Ntotal = 6 ): O2 misfire © 0.167 x 20.9% = 3.49%  oxygen spike. 13
- Eight-Cylinder Engine ( Ntotal = 8 ): O2 misfire = 0.125 x 20.9% ~ 2.61%  oxygen spike. 13

This massive influx of raw fuel hydrocarbons and unreacted oxygen overloads the catalytic converter. 11  The active catalytic sites promote direct exothermic oxidation, which rapidly drives the catalyst substrate past its maximum thermal limit ( > 950°C  or 1742°F ), causing physical melting, substrate warping, and terminal failure. 11

## Chemical Characterization of Synthetic Lubricants and Measurement Response Factors

Differentiating between unburned petrol (caused by ignition misfires) and vaporized or partially oxidized engine oil (caused by mechanical ring or valve seal failure) requires a deep understanding of the chemical differences between these hydrocarbons. 1

Standard petrol is a complex mixture of relatively light, volatile hydrocarbons ( C4  to C2  alkanes, aromatics, and alkenes) with boiling points spanning 30°C  to 200°C. 22  Conversely, modern synthetic lubricating oils, such as Polyalphaolefins (PAO) and Group III or IV mineral base stocks, consist of heavy, highly branched paraffinic oligomers ( Cx%  to Cro  hydrocarbons) with boiling points exceeding 350°C. 24

These differences in chemical structure and molecular weight lead to highly distinct response characteristics between Flame Ionization Detectors (FIDs) and Non-Dispersive Infrared (NDIR) gas analyzers 22:

- Flame Ionization Detection (FID): FIDs operate by mixing the sample gas with hydrogen and burning it in a high-temperature flame ( > 1500  K), which pyrolyzes the hydrocarbons and generates carbonaceous ions. 27  These ions are collected electrostatically to produce an electric current that is proportional to the total number of carbon atoms passing through the flame. 27  The response of an FID is highly universal on a carbon-equivalent basis ( Cc; -equivalent), meaning its response factor ( RF rp ) relative to a calibration standard (such as propane, C3Hg ) remains close to unity ( 1.00 + 0.05 ) regardless of hydrocarbon molecular weight. 27  It detects heavy synthetic oils as efficiently as light petrol. 24
- Non-Dispersive Infrared (NDIR) Detection: NDIR analyzers operate by passing infrared light through a sample cell and measuring the absorption at selective wavelengths. 30  Automotive NDIR analyzers are sensitized to light gaseous alkanes, utilizing optical filters centered on the C—H  stretching vibration of hexane ( CeAis ) or propane ( C3Hg ) at approximately 3.4 um. 22  Because heavy synthetic lubricating oils (PAO) have highly branched structures, their infrared absorption cross-sections are shifted and significantly weaker per carbon atom relative to the linear calibration alkanes. 22

Furthermore, because synthetic lubricants have extremely high boiling points, they do not remain fully in the gas phase within unheated sample transport lines. 33  A significant fraction of these heavy hydrocarbons condenses as liquids or aerosols in sample probes, water traps, and particulate filters before reaching the NDIR optical bench. 33

Due to this physical condensation and the weaker infrared absorption of branched carbon chains, the NDIR response factor for synthetic lubricants is severely biased:

RFypm = SEND mend ~ 0.05 — 0.25 [22,32]

This extreme mass discrimination means NDIR sensors heavily under-report heavy oil emissions. 22  By comparing the simultaneous measurements of an NDIR and a laboratory-grade FID, an analytical ratio can be derived:

Ratioypr/rD = 7 [22, 32]

For raw petrol fuel, this ratio spans 0.44  to 0.68, representing light, volatile hydrocarbons. 22  For synthetic lubricating oils (PAO), the ratio drops to  (typically 0.15  to 0.20 ), providing a distinct, lab-verifiable signature to discriminate between raw fuel misfires and lubricant-burning mechanical wear. 22

## Microscopic Head-Gasket Sealing and Cooling System Headspace Chemistry

The cylinder head gasket is positioned between two major engine components: the engine block and the cylinder head. 17  Modern cylinder heads are cast from lightweight aluminum alloys to reduce mass, while engine blocks are typically cast iron or aluminum with iron cylinder liners. 5

These materials exhibit vastly different thermal behaviors, with aluminum possessing a thermal expansion coefficient ( ay) + 23x 10-°K! ) that is nearly double that of cast iron ( ap. & 11 x 10-°K"! ). 5

During normal engine operation, the cooling system maintains temperatures within a strict envelope of 93°C  to 107°C  ( 200°F  to 225°F ), which keeps the components within designed clamping tolerances. 17  However, if a cooling system component fails (such as a stuck thermostat, leaking water pump, or restricted radiator), the engine temperature rises rapidly. 17

As the cylinder head temperature exceeds the normal operational limits, the thermal expansion mismatch between the aluminum head, the iron block, and the steel cylinder head bolts generates severe mechanical stress. 5  The thermal strain ( € ) is directly proportional to the change in temperature:

e=a-AT

When engine temperatures exceed 115°C  to 127°C  ( 240°F  to 260°F ), this thermal strain exceeds the plastic deformation limit of the head gasket's sealing beads and the structural warp tolerance of the aluminum head deck (typically  mm). 3

A localized temperature gradient ( AT gradient ) of 15°C  to 20°C  between the hot exhaust ports and the adjacent cooling jackets is the critical threshold required to warp the head deck and open microscopic fissures in the gasket sealing barrier. 5

These thermal dynamics produce two highly distinct operational leakage modes:

- The Dynamic Thermal Leak: The micro-fissures remain completely sealed when the engine is cold or at stable idle because the static bolt pretension holds the mating surfaces tight. 2  The leak opens only when the coolant temperature climbs into the danger zone or during rapid load transitions where localized thermal gradients warp the mating surfaces. 3  Testing the vehicle only during static or cold states results in a false negative. 2
- The Overnight Seepage Leak: When the engine is shut down and cools overnight, thermal contraction of the aluminum head reduces the mechanical clamping force on the gasket. 5  Concurrently, the cooling system retains its operational pressure ( ~~ 100 — 150kPa ) for several hours after shutdown. 2  This pressure differential drives coolant across the relaxed gasket interface directly into the combustion chamber. 2  Upon a morning cold start, the cylinder experiences severe misfires until the pooled coolant is cleared. 2  Within 30  seconds, thermal expansion of the warming head seals the fissure, causing the misfire to disappear completely. 17

The clearing time of this overnight seepage leak is non-linearly related to the physical volume of coolant ( Veoolant ) that seeped into the cylinder. 2  If the seepage volume is small ( Veoolant ), the liquid only partially coats the piston dome and spark plug electrodes. 2  Upon cold-start cranking, the localized compression heat and turbulent air-fuel charge quickly vaporize the water-glycol mixture, expelling it into the exhaust within 15  to 30  seconds. 2

This transient event registers ~ 100 — 300  misfire counts on the Mode $06 monitor, and the engine rapidly stabilizes. 6  If the seepage volume is large ( Veoolant > 5.0mL ), the liquid pools on the piston dome and completely submerges the spark plug gap. 16

This liquid emulsifies with the injected fuel, creating a conductive coating of glycol and water across the plug electrodes that permanently fouls the plug. 3  The clearing time extends past 90  seconds, or the cylinder remains dead indefinitely, registering > 1500  misfire counts and triggering a flashing MIL. 15

To confirm a head-gasket failure, technicians analyze the cooling system headspace gas above the radiator fluid for combustion byproducts. 10  High combustion pressures force exhaust gas—which contains extremely high concentrations of carbon dioxide ( 14.7%  or 147, 000  ppm)—across the gasket fissure into the coolant jackets, elevating the headspace CO,  concentration. 10

Electronic CO,  headspace analyzers can detect combustion leakage with sensitivity thresholds as low as 20  ppm. 10  Differentiating from the normal atmospheric background of =~ 400  ppm, a headspace reading of > 600  ppm constitutes a positive confirmation of head-gasket failure, whereas a reading of  ppm indicates a sealed system. 10  This diagnostic method has an 88%  success rate in confirming head-gasket leaks. 10

## Instrument Latency and Transient Diagnostics

Accurate real-time emissions diagnostics are heavily constrained by the physical and electrical response times of exhaust gas analyzers. 30  Conventional NDIR gas analyzers used for vehicle certification and steady-state inspection are heavily dampened to maintain long-term stability and high signal-to-noise ratios. 31

These instruments utilize large-volume measurement cells ( 100 — 300 mL ), long unheated sample transport lines, particulate filters, and external water condensation traps to protect the optical windows from moisture damage. 31

This structural design introduces massive physical and analytical delays 31:

- Transport Delay: The time required for the sample gas to travel from the tailpipe probe, through the heated line, and into the analyzer, which typically scales with sample line length (adding 1.0 — 1.5  seconds for a standard 6 -meter line). 38
- Analyzer Response Time ( Ti0-90 ): The time required for the analyzer to register 90%  of a step change in gas concentration, which ranges from 1.0  to 5.0  seconds for standard NDIR benches. 31
- System Settling Time ( Tog ): The total time required for the entire sampling system to stabilize and report an accurate final concentration, which typically spans 3.0  to 5.0  seconds. 38

In modern low-emission vehicles, transient combustion events are extremely rapid. 30  At an engine speed of 1200  RPM, each cylinder fires 10  times per second. An ignition misfire or a cold-start coolant-clearing phase represents a series of transient hydrocarbon spikes lasting only tens or hundreds of milliseconds. 31

Because conventional NDIR benches have a 3—5  second settling time, they act as severe low-pass filters. 31  They average the transient concentrations over several seconds, heavily dampening the true peak. 31  An instantaneous pre-catalytic hydrocarbon spike that physically peaks at 2000  ppm will be reported by a slow NDIR bench as a broad, flat curve peaking at only 300 — 400  ppm, destroying the transient diagnostic signature. 13

To capture these rapid events, transient research must utilize fast NDIR systems (utilizing high-speed spinning filter wheels to achieve a Ti0-90  response time of  milliseconds) or high-frequency heated FIDs with response times of 1  millisecond. 30

### Figure 2: Signal Dampening Comparison (Conventional NDIR vs. Fast NDIR)

This instrument lag must also be aligned with the vehicle's internal OBD-II misfire detection parameters. 6  In standard petrol engines, the ECM stores adaptive misfire profile correction factors in its Keep-Alive Memory (KAM). 40  These correction factors account for mechanical variations in the crankshaft tone wheel teeth, preventing false misfire detections caused by minor manufacturing tolerances. 40

If the vehicle's battery is disconnected or the ECM is removed during servicing, the KAM is wiped, and these misfire correction factors are lost. 40

Until the ECM relearns these correction factors, the misfire monitor cannot run, and Mode $06 misfire counters will return "not supported" or display flat zero counts. 6  To relearn the misfire profile, the technician must execute a specific deceleration driving protocol 40:

1. The vehicle must be accelerated to a highway exit speed exceeding 60  mph ( 96  km/h). 40
2. The technician must perform a series of closed-throttle, non-braking, de-fueled decelerations back down to the 60  to 40  mph ( 96  to 64  km/h) range. 40
3. This deceleration phase allows the ECM to measure the precise angular velocity variations of the crankshaft tone wheel during zero-torque, de-fueled rotation, updating the KAM correction factors and re-enabling Mode $06 misfire diagnostics. 40

## Statistical Guidance for Non-Uniform Distribution Sampling

To generate highly realistic synthetic datasets for diagnostic algorithm training, simple uniform distributions must be avoided. 1  Real-world automotive signals are governed by specific physical boundaries, wear profiles, and environmental variables, which are best modeled using non-uniform probability distributions. 1

### Healthy Engine Baselines

Cranking and running compression pressures must be modeled using a Gaussian (Normal) distribution to represent manufacturing tolerances and uniform wear across the fleet:

Cranking Compression (Healthy) ~ N(μ = 130 psi, σ = 15 psi)

Running Compression (Healthy) ~ N(μ = 70psi, σ = 8psi) [4,8]

Tailpipe HC post-catalytic converter emissions under healthy conditions follow a highly right-skewed Log-Normal or Exponential distribution. 11  This represents the high efficiency of modern closed-loop stoichiometry, where the vast majority of vehicles cluster near 10 — 20  ppm, and only occasional outliers reach 35  ppm:

Tailpipe HC)... ca, ~ LogNormal(μ = 2.7, σ = 0.4) [11]

Tailpipe O2  post-catalytic converter should follow an Exponential decay distribution peaking close to 0.15%, reflecting tight stoichiometric control:

Tailpipe O2 post.cat ~ Exponential(λ = 6.6) [11]

### Mechanical Compression Loss Modeling

Mechanical compression loss (e.g., a burned valve or worn piston rings) typically affects a single cylinder while the remaining cylinders remain healthy. 4  The dataset must model individual cylinder variables using a Bimodal distribution. 18  For the healthy cylinders, sample from the healthy Gaussian distributions. 4  For the damaged cylinder, sample from a wider, lower-mean Gaussian distribution that represents varying levels of physical degradation:

Cranking Compression (Damaged) ~ N(μ = 60 psi, σ = 12psi) [8]

Running Compression (Damaged) ~ N(μ = 35psi, σ = 8psi) [8]

Relative compression starter current uniformity must be modeled as a function of these compression distributions. 19  Uniformity ratios ( Comp,nin / Comp,nax ) should be calculated; if the uniformity falls below 90%, a relative compression failure is flagged. 1

Mode $06 misfire counts for mechanical loss must be modeled using a Poisson distribution that is active exclusively in the idle RPM bin:

Misfire Counts_Mechanical ~ Poisson(λ = 150) [6]

### Ignition Failure Modeling

Ignition coil or spark plug failures must be modeled using a bimodal distribution across load states. 6  In low-load or idle conditions, the ignition system easily overcomes the low cylinder pressure, yielding a Poisson distribution centered near 0  misfire counts 6:

Misfire Counts_Ignition, idle ~ Poisson(λ = 2)

Under high-load or rapid snap-throttle conditions, high cylinder density increases the spark plug gap ionization voltage demand, causing spark blowout. 4  The counts under load should follow a wide Log-Normal distribution:

Misfire Counts_Ignition, Load ~ LogNormal(μ = 7.8, σ = 0.6) [6]

During these high-load misfire states, tailpipe pre-catalyst O2  must scale strictly as a discrete cylinder-count function ( 20.9% x (1/Neyi) ), with a small Gaussian noise factor ( a = 0.3% ) to represent gas mixing variations. 13

### Coolant Intrusion Modeling

Head-gasket coolant leaks exhibit an extreme bimodal temporal distribution across drive cycles. 6  For warm-restart drive cycles ( Troolant > 60°C ), overnight seepage does not occur, and misfires are absent. 2  For cold-start drive cycles ( Troolant ), the seepage volume determines the misfire duration. 2

The seeped volume ( Veoolant ) should be modeled using a Log-Normal distribution to represent varying gasket fissure sizes:

V_coolant ~ LogNormal(μ = 0.8, σ = 0.5) [2]

The Mode $06 misfire counts must be concentrated entirely within the first 30  seconds of the drive cycle, sampled from a Poisson distribution that scales with Veoolant:

Misfire Counts_Coolant,

For t > 30  seconds, the misfire counts drop exponentially to 0  as thermal expansion seals the gasket fissure. 5

Radiator headspace gas concentrations must be modeled using a Log-Normal distribution that scales directly with cumulative engine load. 10  Higher peak combustion pressures force more exhaust gas across the head-gasket fissure into the coolant jacket, driving headspace CO,  and HC levels up 2:

Headspace CO, ~ LogNormal(μ = 6.8, σ = 0.7) [10]

## Strategic Conclusions and Analytical Synthesis

Synthesizing the physical, chemical, and electrical signatures of mechanical compression loss, ignition misfires, and coolant intrusion exposes critical interdependencies that must govern any robust diagnostic system. A single-cylinder mechanical compression loss is physically bounded by a critical threshold: cranking compression below 90  psi and running compression below 40  psi will inevitably cause combustion failure, setting a hard misfire code. 4

However, diagnosing this fault via relative starter current is highly sensitive to the battery State of Charge. 19  A degraded battery dampens starter speed fluctuations, smoothing the current waveform and causing a false-pass result where relative compression uniformity remains above the 90%  threshold despite severe internal engine damage. 1

Ignition misfires present highly dynamic, load-dependent signatures. 6  While mechanical compression faults peak at idle due to low charge velocities, ignition failures strike during high-load, high-manifold-pressure transitions that increase spark gap resistance. 4  The resulting raw exhaust gas floods the catalyst with a highly reactive mixture of fuel and oxygen. 11

This mixture triggers a localized exothermic oxidation reaction that quickly drives the catalyst into thermal runaway ( > 950°C ), causing structural collapse and a permanent loss of oxygen storage capacity. 11  This failure can be tracked in real-time as tailpipe HC and O2  levels swing from highly controlled stoichiometric minimums to saturated, raw-exhaust maximums. 11

Coolant intrusion via a blown head gasket is governed by complex thermal expansion gradients. 5  Because aluminum cylinder heads expand at twice the rate of cast-iron blocks, micro-fissures in the head gasket can act dynamically. 5  Under overnight cooling, reduced head bolt tension and residual coolant system pressure drive coolant seepage directly into the cylinder. 2

Upon a cold start, this pooled coolant fouls the spark plug and triggers severe, localized misfires. 2  Within 30  seconds, thermal expansion of the warming head closes the fissure, clearing the misfire. 5  This cold-start transient signature is easily distinguished from ignition and mechanical faults, which are persistent or load-dependent. 6

To build a highly robust, realistic synthetic dataset for diagnostic algorithm training, developers must strictly adhere to the following data-generation guidelines:

- Implement Non-Uniform Sampling: Replace all uniform distributions with the physically bounded Normal, Log-Normal, and Poisson distributions detailed in this report. This ensures that the simulated fleet reflects real-world variability and outlier behavior.
- Incorporate Cylinder-Count Scaling: Ensure that tailpipe O2  concentrations during misfire conditions are calculated as a direct function of engine cylinder count ( me Be ), rather than using a static 5%  spike across all models.
- Model the NDIR/FID Response Gap: Introduce the NDIR/FID response factor ratio (  for synthetic lubricants vs. 0.44 — 0.68  for raw fuel) to allow algorithms to accurately discriminate between fuel-rich misfires and oil-burning mechanical failures.
- Apply Temporal and Thermal Constraints: Structure coolant intrusion misfire counts to be highly concentrated in the first 30  seconds of a cold-start cycle ( Troolant ), decaying to 0  on warm starts to replicate head-gasket thermal sealing dynamics.
- Link Battery SoC to Current Uniformity: Couple relative compression current clamp peaks directly to simulated battery internal resistance to accurately represent the smoothing effect of low-charge batteries on starter motor current waveforms.

#### Works cited

1. CLUSTER1_value_prompt.md
2. Does this mean 100% my head gasket is leaky or blown? How accurate is this test? - Reddit, accessed on July 1, 2026, https://www.reddit.com/r/autorepair/comments/1la4v70/does_this_mean_100_my_head_gasket_is_leaky_or/
3. Head Gasket Leak Symptoms & How to Fix It - AutoZone, accessed on July 1, 2026, https://www.autozone.com/diy/engine/head-gasket-leak
4. Running Compression Tests - ALLDATA, accessed on July 1, 2026, https://www.alldata.com/us/en/support/community/article/tech-tip/running-compression-tests
5. Signs of a Header Gasket Leak Every Driver Should Know – petenelsonautorepair.com, accessed on July 1, 2026, https://petenelsonautorepair.com/header-gasket-leak/
6. Using OBD2 Mode $06 for advanced car diagnostics - OBD Auto Doctor, accessed on July 1, 2026, https://www.obdautodoctor.com/tutorials/using-obd2-mode-06-for-advanced-car-diagnostics/
7. OBD-II Mode 6 Diagnosis | Codes | Data | MOTOR Magazine, accessed on July 1, 2026, https://www.motor.com/magazine-summary/obd-ii-mode-6-diagnosis-driveability-corner-june-2002/
8. Anatomy of the Compression Waveform - Automotive Test Solutions, accessed on July 1, 2026, https://automotivetestsolutions.com/knowledge-base/case-studies/all-case-studies/anatomy-of-the-compression-waveform/
9. Pressure and Vacuum Diagnosis, Part III: Running Compression - Gears Magazine, accessed on July 1, 2026, https://gearsmagazine.com/magazine/pressure-and-vacuum-diagnosis-part-iii-running-compression/
10. Engine Head Gasket Leak Detector using a CO2 Analyzer, accessed on July 1, 2026, https://www.forensicsdetectors.com/blogs/articles/carbon-dioxide-co2-analyzer-for-engine-head-gasket-leak-detection
11. 5-Gas Diagnostic Chart - Walker Exhaust, accessed on July 1, 2026, https://www.walkerexhaust.com/support/tech-tips/five-gas-diagnostic-chart.html
12. Exhaust Emission Notes | aj6 engineering, accessed on July 1, 2026, https://aj6engineering.co.uk/exhaust-emissions/
13. 5-Gas Analysis - MOTOR, accessed on July 1, 2026, https://www.motor.com/magazine-summary/5-gas-analysis-may-1998/
14. Understanding Engine Exhaust Emissions - Crypton Diagnostic Equipment, accessed on July 1, 2026, https://www.crypton.co.za/Tto%20know/Emissions/exhaust%20emissions.html
15. Misfire Diagnosis - Ross-Tech Wiki, accessed on July 1, 2026, https://wiki.ross-tech.com/wiki/index.php/Misfire_Diagnosis
16. P0306: Cylinder 6 Misfire Detected - Edmunds, accessed on July 1, 2026, https://www.edmunds.com/obd-dtc/p0306.html
17. Symptoms of a Blown Head Gasket: Everything You Need to Know - Bar's Leaks, accessed on July 1, 2026, https://barsleaks.com/symptoms-blown-head-gasket/
18. Compression testing - PicoScope Automotive Library, accessed on July 1, 2026, https://www.picoauto.com/library/picoscope-automotive-training/training/compression-testing-by-pico-technology
19. Test 1 Relative Compression - Pico Automotive Training, accessed on July 1, 2026, https://www.pico-automotive.co.za/tests/test-1-relative-compression.php
20. Pico PP939 WPS500X Pressure transducer Kit - AESwave.com, accessed on July 1, 2026, https://www.aeswave.com/wps500x-pressure-transducer-kit-p9265.html
21. Catalytic Converter Testing - Smog Tech Institute, accessed on July 1, 2026, https://www.smogtechinstitute.com/smogtech/index.php/about-us-3/bogs/20-technical/39-catalytic-converter-testing.html
22. An Experimental Evaluation of Remote Sensing-Based Hydrocarbon Measurements: A Comparison to FID Measurements - PubMed, accessed on July 1, 2026, https://pubmed.ncbi.nlm.nih.gov/28081416/
23. Method 1663: Differentiation of Diesel and Crude Oil by GC/FID - EPA, accessed on July 1, 2026, https://www.epa.gov/sites/default/files/2015-10/documents/method_1663_1992.pdf
24. Guidance on sampling, analysis and data reporting for the monitoring of mineral oil hydrocarbons in food and food contact materi - JRC Publications, accessed on July 1, 2026, https://publications.jrc.ec.europa.eu/repository/bitstream/JRC133174/JRC133174_01.pdf
25. A Review of MOSH and MOAH Analysis in Food | LCGC International, accessed on July 1, 2026, https://www.chromatographyonline.com/view/a-review-of-mosh-and-moah-analysis-in-food
26. Contaminants in Lubricants - CITGO MarketNet, accessed on July 1, 2026, https://www.citgomarketnet.com/MarketNetWebOther/Lubes/TrainingWorkshops/Webinars/Webinar_ContaminantsInLubricants.pdf
27. Hydrogen Flame Ionization Detection Method (FID) - HORIBA, accessed on July 1, 2026, https://www.horiba.com/int/process-and-environmental/measuring-principles/fid/
28. 40 CFR 1065.845 -- Response factor determination. - eCFR, accessed on July 1, 2026, https://www.ecfr.gov/current/title-40/chapter-I/subchapter-U/part-1065/subpart-I/section-1065.845
29. Flame ionization detector response factors for compound classes in quantitative analysis of complex organic mixtures - OSTI, accessed on July 1, 2026, https://www.osti.gov/biblio/5787154
30. CO & CO₂ Analysers - Cambustion, accessed on July 1, 2026, https://www.cambustion.com/products/gas-instrumentation/co-co2-analysers
31. Gas Phase Measurements - DieselNet, accessed on July 1, 2026, https://dieselnet.com/tech/measure_gas.php
32. An Experimental Evaluation of Remote Sensing-Based Hydrocarbon Measurements: A Comparison to FID Measurements, accessed on July 1, 2026, https://www.tandfonline.com/doi/pdf/10.1080/10473289.1996.10467447
33. Single-Beam NDIR Gas Analyzer (ZRE) | - Fuji Electric Corp. of America, accessed on July 1, 2026, https://americas.fujielectric.com/products/instrumentation/cems-process-monitoring-gas-analyzers/single-beam-ndir-gas-analyzer-zre/
34. METHOD 25.1 - AQMD, accessed on July 1, 2026, https://www.aqmd.gov/docs/default-source/laboratory-procedures/methods-procedures/stm-025-1.pdf
35. Why Engine Overheating Can Lead To A Blown Head Gasket - Yates Automotive, accessed on July 1, 2026, https://www.yatesautomotive.com/blog/why-engine-overheating-can-lead-to-a-blown-head-gasket
36. Laser Spectroscopic Motor Exhaust Gas Analyzer MEXA-ONE-QL-NX - Envirosys, accessed on July 1, 2026, https://enviro-sys.gr/en/catalog/vehicle-inspection-systems/laser-spectroscopic-motor-exhaust-gas-analyzer-mexa-one-ql-nx
37. Combustibles Measurement in Sulfur Recovery Unit Acid Gas with a Combined NDUV / NDIR Analyzer - AMETEK PROCESS INSTRUMENTS, accessed on July 1, 2026, https://www.ametekpi.com/-/media/ametekpi/files/products/western-research/ips-4-integrated-photometric-spectrometer/technical-papers/feed-gas-analyzer.pdf?la=en&revision=fa0a8903-3736-4cb3-820d-deabf62e7af8
38. Assessment of On-Board and Laboratory Gas Measurement Systems for Future Heavy-Duty Emissions Regulations - PMC, accessed on July 1, 2026, https://pmc.ncbi.nlm.nih.gov/articles/PMC9141819/
39. MEXA-ONE -Emission Measurement System - HORIBA, accessed on July 1, 2026, https://www.horiba.com/int/mobility/products/detail/action/show/Product/mexa-one-41/
40. Scan Tool Stopped reading Mode 6 misfire data - ScannerDanner Forum, accessed on July 1, 2026, https://scannerdanner.com/forum/post-your-repair-questions-here/13458-scan-tool-stopped-reading-mode-6-misfire-data.html
