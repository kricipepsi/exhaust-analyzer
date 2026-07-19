Based on the categories established in the architecture payload, the presence of MAP and MAF sensors belongs inside the Aspiration and Induction Systems subsystem.
They sit within this category because they do not define the core physical dimensions of the metal engine block (Engine Architecture), but rather monitor the air intake induction pathways and manifold pressure dynamics required to feed the cylinders.
## Updated Subsystem Mapping for Your Developer
To keep your app database clean and structured, group the parameters under these explicit structural headers:

* Subsystem 1: Engine and Displacement Architecture
* engine_displacement_liters
   * cylinder_count
   * engine_configuration (e.g., V6, I4)
   * number_of_banks
* Subsystem 2: Aspiration and Induction Systems 🔴 (MAP/MAF belongs here)
* induction_type (Naturally Aspirated / Turbocharged / Supercharged)
   * fuel_delivery_type (GDI / PFI)
   * has_maf_sensor (Boolean)
   * has_map_sensor (Boolean)
   * primary_load_calculation
* Subsystem 3: Powertrain and Valvetrain Management
* valvetrain_type (VVT / VVL)
   * fuel_type (Gasoline / Diesel / Flex-Fuel)
* Subsystem 4: Emissions Control Specifications
* upstream_o2_type (Wideband AFR / Narrowband)
   * egr_equipped (Boolean)
   * secondary_air_equipped (Boolean)



