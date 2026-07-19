# EP-DTC-02 — SAE J2012 / ISO 15031-6 Eight-Family Fault Taxonomy Backbone

This reference document establishes the L2 routing backbone for the 4DLab diagnostic engine. Every present and future fault node in the global registry attaches under one of these standard powertrain P-code families.

| Family ID | Name / Scope | Standards Citation (ISO-primary) | What Attaches Here |
|---|---|---|---|
| **P00XX** | Fuel and Air Metering (VVT, CKP/CMP correlation, sensor reference) | ISO 15031-6 §5.6.1 / SAE J2012 Table D1 | VVT phaser faults, CKP/CMP correlation, and intake valve carbon buildup. |
| **P01XX** | Fuel and Air Metering (MAF, MAP, IAT, ECT, O2 circuits, trims) | ISO 15031-6 §5.6.1 / SAE J2012 Table D2 | Vacuum leaks, fuel trim deviations, ECT thermostat faults, and O2 sensor bias/heater faults. |
| **P02XX** | Fuel and Air Metering (Injector circuits, fuel pump, turbo boost) | ISO 15031-6 §5.6.1 / SAE J2012 Table D3 | Injector electrical circuit errors, fuel pump failures, and turbo/boost performance faults. |
| **P03XX** | Ignition System or Misfire (Misfire, knock sensor, ignition coils) | ISO 15031-6 §5.6.1 / SAE J2012 Table D4 | Ignition misfires, coil failures, and knock sensor circuit malfunctions. |
| **P04XX** | Auxiliary Emission Controls (Catalyst efficiency, EGR, EVAP) | ISO 15031-6 §5.6.1 / SAE J2012 Table D5 | Catalyst degradation, EGR flow errors, and EVAP system leaks/purging faults. |
| **P05XX** | Vehicle Speed, Idle Control, and Auxiliary Inputs (Idle air control) | ISO 15031-6 §5.6.1 / SAE J2012 Table D6 | Idle speed control errors (IAC) and auxiliary input sensor faults. |
| **P06XX** | Computer and Auxiliary Outputs (PCM memory, 5V reference) | ISO 15031-6 §5.6.1 / SAE J2012 Table D7 | ECU internal checksums, PCM driver circuits, and 5V sensor reference voltage faults. |
| **P07XX_P08XX_P09XX** | Transmission (Transmission control, sensors, clutches) | ISO 15031-6 §5.6.1 / SAE J2012 Table D8/D9/D10 | TCM communication errors, solenoid failures, and transmission gear ratio faults. |
