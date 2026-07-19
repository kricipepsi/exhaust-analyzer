



## 1. Q5 — Define & hone the symptom questionnaire (CENTRE OF THIS BRIEF)

**Question.** What structured symptom vocabulary do professional diagnostic systems and
techs actually use, and is the current 6-category / 18-pair catalog complete, non-overlapping,
and correctly mapped to petrol fault families?

**Find:**
- The top-level **driveability complaint categories** used by professional sources, and how
  they compare to the current 6. Are any common petrol complaints missing (e.g. **hard
  starting (but starts)**, **surging/hunting idle**, **knock/pinging under load**, **stalls
  on cold start**, **backfire**, **misfire/stumble felt as vibration**)?
- For each tier_1, whether the **3 sub-filters are the right 3** — gaps, overlaps, or
  sub-filters that don't discriminate between fault families.
- The **fault family each symptom/sub-filter should route to** in a petrol engine.

**Where to look:** professional diagnostic taxonomies and symptom menus — Identifix,
Mitchell1 ProDemand, ALLDATA, Bosch ESI[tronic], Autodata symptom search, Haynes/driveability
diagnostic flowcharts; SAE driveability terminology; manufacturer "customer concern code" /
"condition" lists; OBD-II driveability symptom-to-cause guides; trade forums only as
corroboration, never as a primary source.

**Deliverable (return this):**
- A **revised catalog table**: tier_1 (plain label + internal id) → tier_2 sub-filters
  (plain label + internal id) → mapped fault family → 1-line rationale → source link.
- A short **changelog vs the current 18 pairs**: ADD / KEEP / REWORD / MERGE / DROP, each
  with a one-line reason and a source.
- A note on whether **occurs_during** and **engine_state** are the right two environmental
  axes, or whether a third (e.g. load state: idle / cruise / acceleration) is needed —
  with sources (feeds Q6).

---

## 2. Q1 — How predictive is a reported symptom of the true fault family?

**Question.** When an owner reports symptom X, how often is the confirmed fault actually in
the family X points to? This sets how *strong* the prior is allowed to be.

**Find:** published diagnostic-accuracy figures — symptom-to-confirmed-fault correlation,
"first-guess" hit rates, the prevalence of common causes behind each complaint (e.g. of all
"rough idle" petrol cases, what share are vacuum leak vs misfire vs CTS vs idle-control).
Also "no-fault-found" / "could-not-duplicate" rates (overlaps Q9).

**Where to look:** automotive diagnostics journals and SAE papers, warranty/repair-rate
studies, fleet-maintenance analyses, manufacturer technical-bulletin frequency data,
reliability-survey breakdowns by complaint.

**Deliverable:** a per-tier_1 table of **prior strength**: symptom → most-likely fault
families with rough probability bands (e.g. 50–70% / 20–30% / <10%) → source. End with an
explicit **honesty note**: a true confusion matrix needs labeled paired data (see Q10); state
which numbers are real measurements vs informed estimates.

---

## 3. Q6 — How should environmental context shift the prior?

**Question.** Given the same primary complaint, how much does cold-vs-hot / when-it-occurs /
engine-state change the most-likely fault family?

**Find:** documented context→fault associations for petrol engines, e.g. *cold-only rough
idle* → coolant-temp-sensor / cold-enrichment; *hot-only stall* → crank sensor / fuel
delivery / vapour lock; *hesitation only at high rpm* → fuel pressure / ignition under load;
*won't start when hot* vs *when cold* split.

**Where to look:** driveability diagnostic guides organised by "condition occurs when…",
cold-start vs hot-restart troubleshooting trees, temperature-dependent fault literature.

**Deliverable:** a **context-modifier table**: (tier_1 + occurs_during/engine_state) → how the
fault-family ranking shifts (which family is promoted/demoted) → source. Flag any context
combination with no documented signal (so it stays neutral, not invented).

---

## 4. Q9 — Real-world rate of false / misleading symptom reports

**Question.** How often is the owner's reported symptom wrong, vague, or misleading — the
bound on how far the prior can ever be trusted?

**Find:** "could-not-duplicate" / "no-trouble-found" rates, customer-complaint-accuracy
studies, share of repair visits where the reported concern didn't match the diagnosed fault,
mismatch between customer description and tech-verified condition.

**Where to look:** warranty-claim analyses, service-department CND/NTF statistics, dealer
diagnostic studies, fleet/service quality literature.

**Deliverable:** a **trust-ceiling figure or range** (e.g. "owner symptom is misleading/
unverifiable in ~X–Y% of cases") with sources, plus any breakdown by complaint type (some
symptoms are reported more reliably than others). This caps the prior's maximum weight.

---

## 5. Q10 — Does labeled symptom→confirmed-fault data exist to validate/train the prior?

**Question.** Is there a public or licensable dataset that pairs a **reported symptom** with a
**confirmed fault/repair** for petrol cars — so the prior (Q1) can be validated empirically
rather than estimated?

**Find & catalogue candidate datasets:** NHTSA complaints + vPIC, CarMD / repair databases,
Kaggle / academic automotive fault datasets, OBD-II fault datasets, repair-order /
service-record corpora, insurance/warranty claim datasets, vehicle-health telematics sets.

**Where to look:** open-data portals, academic dataset repositories, Kaggle, government
vehicle-safety data, commercial diagnostic-data vendors.

**Deliverable:** a **dataset catalogue table**: name → what it contains → does it pair
reported-symptom ↔ confirmed-fault (Y/N/partial) → petrol 1990–2010 coverage → access terms
(free / licence / scrape-restricted) → link. Conclude with a one-line verdict: is empirical
validation of the prior feasible from any of these, or must we estimate?

---

## Source-quality bar (applies to every section)

Prefer professional diagnostic systems, SAE/standards bodies, manufacturer technical data,
and peer-reviewed/industry studies. Forums and blogs may **corroborate** but never stand as
the sole source for a recommendation. Every row in every deliverable table carries a link.
Mark each finding as **measured** (real data) or **estimated** (expert inference) — do not
blur the two.

---

## DB note — what stays in the database, not the web

DNA10 Q2 (VIN-decode resolution), Q3 (per-engine-code CoC idle datasets), Q4 (which identity
attributes are populated), and Q8 (does `model`/variant add anything over engine_code) are
answered from the local `DBS` data, **not** by web research. If honing the
questionnaire reveals we need an engine-attribute field that isn't yet extracted, the TecDoc
table schema is documented in `DBS/tecdoc/td2018_tables_description.pdf` (describes the
`articles`, `article_attributes`, `article_li` applicability, engine-linkage tables, etc.) —
that is the reference for writing a parts/engine-attribute extraction query. Keep such
extraction as a separate DB task; it is not part of this web-research brief.


## 0. Context the researcher needs

4DLab diagnoses **petrol passenger cars, model years 1990–2010 (Euro 1 – Euro 5)**, warm
engine, using exhaust-gas chemistry as ground truth and the ECU as perception. Before any
measurement, the vehicle owner/operator answers a short **symptom questionnaire** in plain
language. That report becomes the cheapest independent diagnostic channel.

The questionnaire today produces four pieces of data per session:

- `tier_1_primary_symptom` — the main complaint (6 categories today).
- `tier_2_subfield_filter` — a sub-filter that refines it (3 per category today = 18 pairs).
- `environmental_conditions` — two fixed fields: **occurs_during** (`always` / `cold_only` /
  `hot_only` / `intermittent`) and **engine_state** (`running` / `cranking` / `will_not_start`).
- `free_text_notes` — optional free text.

**Current 18-pair catalog (this is what you are honing, not replacing):**

| tier_1 primary symptom | tier_2 sub-filters |
|---|---|
| `vehicle_wont_start` | fast_crank_whining · no_crank_silent · normal_crank_zero_rpm |
| `rough_idle_shudder` | cold_engine_only · hot_engine_only · constant_shudder |
| `lack_of_power_hesitation` | flat_sluggish_always · only_high_rpm_highway · sudden_jerk_stumble |
| `poor_economy_fuel_odor` | just_poor_mpg · strong_fuel_smell · right_after_fillup |
| `engine_dies_or_stalls` | when_coasting_to_stop · intermittent_random · only_when_hot |
| `visible_exhaust_smoke` | black_smoke · blue_oily_smell · white_sweet_smell |

**Hard constraints on any recommendation you return:**

1. **Operator-facing wording.** The owner answers, not a technician. Each option must be
   phrased in language a non-expert driver understands — but it must map cleanly onto the
   fault families professional techs use. Return both the plain-language label *and* the
   technical fault family it points to.
2. **Every symptom must earn its place by pointing to a fault family.** If a proposed new
   symptom/sub-filter cannot be tied to a specific petrol fault family (e.g. lean-misfire,
   vacuum leak, coolant-temp-sensor, ignition-coil, fuel-delivery, valve-timing, catalyst,
   EGR), it does not belong in the questionnaire. No "nice to have" options.
3. **Stay in the operating envelope.** Petrol, 1990–2010, Euro 1–5, warm-engine driveability.
   Ignore diesel, EV/hybrid, modern Euro 6/7-only faults, and ADAS/body/electrical complaints.