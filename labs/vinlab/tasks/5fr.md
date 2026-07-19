Yes, the ECU absolutely has the capability to correct fuel trims using the downstream narrowband oxygen sensor on this engine. [1, 2] 
This vehicle uses a Bosch MED17.4 Engine Management System, which implements a secondary fuel control strategy known as Post-Cat Fuel Trim Control (often logged on diagnostic scan tools as LTFT-B1S2 or STFT-B1S2). [3, 4] 
While older OBD-II cars only used the rear sensor to track catalytic converter health, modern GDI engines use it for targeted fuel control through specific mechanisms: [1, 5] 
## 1. Pre-Cat Wideband Sensor Calibration [6] 
Wideband sensors (Sensor 1) can drift slightly in their accuracy over time due to exhaust heat, aging, or mild contamination. Because a narrowband sensor (Sensor 2) is extremely precise at exactly Lambda = 1.0 (0.45 Volts), the Bosch ECU uses the downstream sensor as a "sanity check". If the rear sensor reports a sustained variation from stoichiometric equilibrium, the ECU adjusts its long-term baseline fueling strategy to recalibrate the wideband sensor's reading. [6, 7] 
## 2. Catalyst Efficiency Window Tuning
The catalytic converter operates at maximum emission scrubbing efficiency within a very tight atmospheric window. The ECU will command minor, slow-moving fuel corrections based on the rear sensor's feedback to keep the catalytic converter loaded with the optimal amount of oxygen. [2, 8, 9] 
## Authority and Correction Limits

* Limited Influence: Under standard operating conditions, the downstream sensor holds minimal trimming authority—typically contributing only ±1% to ±2% of the total fuel trim correction. The upstream wideband sensor remains the dominant driver for fuel management. [1, 3, 10, 11] 
* Abnormal Conditions: If you have an exhaust leak between the upstream and downstream sensors, or if the rear sensor fails and drifts in voltage, it can fool the ECU. In skewed scenarios, the downstream bias can command much larger, erroneous fuel trim corrections, sometimes throwing off your total trim calculations or triggering rich/lean trouble codes. [1, 3, 12, 13, 14] 

When an engine burns oil, the oil bypasses the combustion chamber or turbo seal and enters the exhaust stream. When this oil hits the hot catalytic converter, it burns off, creating ash, phosphorus, and zinc coatings that poison the catalyst and alter the exhaust chemistry.
Because the downstream narrowband sensor monitors this exact environment, it reacts to the altered exhaust gas and commands incorrect fuel trims. On a Bosch MED17.4 ECU, this creates distinct post-cat fuel trim signatures depending on where and how the oil is entering.
------------------------------
## The Baseline Mechanics: Why Oil Fools the Post-Cat Trim
Burning oil consumes oxygen in the exhaust, creating a local low-oxygen environment. The downstream sensor reads this low oxygen level as a false rich condition (high voltage output, e.g., 0.75V - 0.9V).
In response, the ECU's post-cat fuel trim capability tries to correct this by pulling fuel back. Therefore, the overarching signature of oil-burning in a Bosch system is a negative Post-Cat Fuel Trim (STFT/LTFT B1S2), while the primary upstream wideband sensor might show near-normal readings.
------------------------------
## Specific Signatures by Failure Mode## 1. Worn Valve Stem Seals
Oil leaks past the seals down the valve guides into the combustion chamber, accumulating heavily when the engine is idling or under high intake vacuum. [1, 2] 

* The Dynamic Behavior: Highly volatile and highly dependent on engine load.
* The Post-Cat Signature: At hot idle, STFT B1S2 will drop sharply negative (e.g., -8% to -15%). Upon sudden acceleration after a long idle, the sensor voltage spikes massively high (0.9V+ due to the plume of burnt oil), forcing a severe temporary negative trim correction. Once cruising under load, the trim baseline stabilizes back toward 0%.
* Other Clues: A distinct puff of blue-gray smoke from the tailpipe only upon accelerating away from a stoplight.

## 2. Worn Piston Rings or Cylinder Wall Oil Leaks [3] 
Blow-by allows oil to continuously sweep past the piston rings into the combustion chamber, worsening under high engine load and high RPMs. [4, 5] 

* The Dynamic Behavior: Constant, steady, and worsens with engine speed.
* The Post-Cat Signature: LTFT B1S2 becomes steadily and permanently negative (e.g., -5% to -12%) across all driving conditions. Unlike valve seals, it does not clean up at high speeds; the negative trim persists on the highway.
* Other Clues: High crankcase pressure (blow-by blowing the oil oil-filler cap off when unscrewed at idle). Consistent oil consumption per 1,000 km. [6, 7] 

## 3. Leaking Turbocharger Seals (Exhaust/Turbine Side) [8] 
Oil leaks directly into the hot exhaust housing after the combustion chamber but before the catalytic converter.

* The Dynamic Behavior: Completely decoupled from engine combustion vacuum.
* The Post-Cat Signature: STFT B1S2 will drop deeply negative during decel fuel cut-off (DFCO) or prolonged idling. When you lift your foot off the accelerator while driving down a hill, the fuel injectors turn off entirely. The upstream sensor should see pure air (0%). However, the leaking turbo seal keeps dripping oil onto the hot turbine, burning oxygen. The downstream sensor stays pinned rich (0.8V), forcing a highly anomalous negative trim correction when no fuel is even being injected. [9] 
* Other Clues: The intercooler piping may be completely dry, but the exhaust downpipe directly behind the turbo exhaust wheel will be wet with liquid oil.

## 4. Crankcase Valve (PCV) Stuck Open / Torn Valve Cover Membrane
On the 1.6 THP engine, the PCV system is integrated into the plastic valve cover. A torn membrane or stuck valve forces the intake manifold to pull a massive vacuum directly on the oil-laden crankcase, drinking oil vapor straight into the intake. [10] 

* The Dynamic Behavior: Maximum oil ingestion occurs at high vacuum (idle and deceleration). [11] 
* The Post-Cat Signature: STFT B1S2 drops deeply negative at idle (-12% to -20%). However, because this acts like a massive unmetered vacuum leak combined with oil vapor, the upstream primary trims (STFT B1B1) will often fight it by swinging wildly positive (+15%) trying to correct for the unmetered air, while the downstream trim swings wildly negative trying to correct for the unburnt oil vapors hitting the cat. This divergent split trim signature (Upstream Positive, Downstream Negative) is a classic PCV failure telltale.
* Other Clues: Severe whistling or hissing sound from the valve cover at idle, and immense suction when trying to remove the oil oil-filler cap with the engine running. [12] 

------------------------------
## Diagnostic Summary Table

| Failure Mode [13, 14, 15, 16, 17] | Post-Cat Trim Behavior (B1S2) | Primary Trigger Condition | Associated System Clue |
|---|---|---|---|
| Valve Stem Seals | Highly Negative STFT | Hot idling / Tip-in after idle | Blue smoke puff on takeoff |
| Worn Piston Rings | Fixed Negative LTFT | Consistent across all RPM/Loads | Heavy oil cap blow-by pressure |
| Leaking Turbo Seal | Deeply Negative STFT | Engine deceleration (DFCO) | Wet oil inside the exhaust downpipe |
| Stuck Open PCV Valve | Deeply Negative STFT | Idle only (Divergent from upstream) | Intense vacuum at the oil fill cap |


