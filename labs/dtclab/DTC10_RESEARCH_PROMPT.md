# DTC10 — web-research prompt doc

**Date:** 2026-06-11
**Purpose:** drive a web-research pass on the DTC10 questions the new wiki does
**not** fully answer. Each block below is a ready-to-use prompt: the question,
what the wiki already has, what's missing, search terms, and the bar a
*complete* answer must clear.

## Fixed context to paste into any search session

> Scope: **petrol, 1990–2010 (Euro 1–Euro 5)**, SAE J1979 OBD-II, manually
> entered scan data (no live CAN streaming), **idle-centric** diagnosis (curb
> idle + stress idle ~3500–4500 RPM, read at ECT ≥ 75 °C). No diesel, LPG, CNG,
> E85, hybrid. Post-2010 / Euro 6+ tech (GPF, LSPI, secondary-air-injection) is
> out of scope. The goal is to *measure or pin* numbers that let DTCLab rank
> faults — not general "how OBD works" prose.

## Status of the 10 questions

Resolved without research: **Q4, Q5, Q6, Q8** (answered in the wiki) and **Q7**
(closed by the 1990–2010 scope decision — GPF/P244A are out). The five below
still need work. Two of them (**Q1, Q2, Q9**) are partly *corpus-measurement*
questions — the web gives the convention and published rates, but the real
numbers for our engine come from counting our own `DTCLab/cases/` corpus. Each
block flags which part is web-findable and which needs an internal count.

---

## Q1 — What fraction of real fault cases present a stored DTC at diagnosis? *(core)*

**Why it matters:** DTC10's premise is that the DTC discriminator is *starved* —
"64/90 outranked cases have no DTC." If no-DTC is the norm, DTC-based ranking is
structurally weak and the engine must lean on gas + freeze-frame + Mode `$06`
instead. We need the actual fraction.

**Wiki today:** argues *why* no-DTC cases matter (Mode `$06` as pre-DTC evidence;
"none stored" non-start cases) but never gives a fraction.

**Resolve it by answering:**

- What share of driveability/emissions faults on 1990–2010 petrol cars set a
  *confirmed* (MIL-on) DTC at the point a tech diagnoses them — versus pending-
  only, versus no code at all? Split by fault family if possible (mixture,
  misfire, catalyst, EGR/EVAP, sensor).
- How often is the *stored* code a downstream artefact rather than the root
  cause (e.g. P0171 set by a misfire)?

**Web search terms:** "percentage of driveability faults with no DTC",
"intermittent fault no stored code OBD statistics", "MIL-off emissions failure
rate", "pending vs confirmed DTC frequency study", Tom Denton *Advanced
Automotive Fault Diagnosis* fault-frequency tables, SAE papers on OBD detection
coverage / "monitor detection efficiency".

**Also needs (internal):** a straight count over `DTCLab/cases/` — cases with ≥1
confirmed DTC ÷ total — to get *our* corpus's real fraction, not just published.

**Complete answer =** a numeric fraction (ideally web figure + our-corpus count
side by side), broken down by family, with sources cited.

---

## Q2 — Empirical P-code→family mapping strength *(OUTRANKED)*

**Why it matters:** ranking trusts a code only as much as it points to one
family. If P0171 fires across vacuum leak / MAF / fuel-pressure / exhaust-leak
with similar frequency, the code alone is a weak discriminator and the freeze-
frame/RPM tie-breakers carry the load.

**Wiki today:** shows the *multiplicity* qualitatively (P0171 → vacuum leak, fuel
delivery, MAF skew, exhaust leak, misfire-mask) and gives discriminators — but
**no co-occurrence frequencies**.

**Resolve it by answering:**

- For the highest-volume generic codes (P0171/P0174, P0300/P030x, P0420,
  P0401/P0402, P0101), what is the empirical distribution of *actual* root
  causes behind each? e.g. "of confirmed P0171, X% vacuum leak, Y% MAF, Z% fuel
  pressure, …".
- Which codes are effectively 1:1 with a family, and which are "fan-out" codes?

**Web search terms:** "P0171 most common causes statistics / percentage",
"P0420 root cause distribution", "most common causes ranked OBD code", "fuel
trim DTC false lean misfire frequency", repair-database aggregates (e.g.
published shop-data summaries), SAE/IM240 program fault-distribution reports.

**Also needs (internal):** tabulate code↔confirmed-root-cause co-occurrence over
`DTCLab/cases/` to get our own mapping-strength matrix.

**Complete answer =** a per-code root-cause frequency table (the "fan-out
matrix"), web + corpus, flagging which codes are reliable vs fan-out.

---

## Q3 — Which P1xxx (manufacturer) codes add discriminating power, usable without per-OEM DBs? *(coverage)*

**Why it matters:** generic P0xxx codes fan out; some manufacturer P1xxx codes
are far more specific. But using them normally needs per-OEM lookup tables we
don't have. The question is whether a *small, cross-OEM-stable* subset is worth
hard-coding.

**Wiki today:** P1xxx appear only as non-start/immobiliser examples (P1260,
P1404, P1233, P1602, P1626). No systematic "which P1xxx beat the generic set"
and no answer on OEM-DB dependence.

**Resolve it by answering:**

- Which P1xxx codes carry diagnostic meaning that is **consistent across most
  OEMs** for 1990–2010 petrol (so they can be used without a per-make database)?
- Which are hopelessly OEM-specific (same number, different meaning per make)
  and therefore unusable without a lookup table?
- For the stable subset, what family does each point to?

**Web search terms:** "P1xxx manufacturer specific codes common across makes",
"are P1 codes standardized", "Ford/GM/Toyota P1xxx meaning differs", "PATS
immobiliser P1260 generic", "manufacturer-specific DTC overlap petrol", Bosch
KTS / generic-vs-enhanced code coverage notes.

**Complete answer =** a shortlist of cross-OEM-stable P1xxx → family entries,
explicitly separated from the OEM-specific ones to avoid, with a one-line
feasibility verdict on "without per-OEM DBs".

---

## Q9 — One-trip vs two-trip maturation & clearing bias — does it skew the corpus? *(corpus realism)*

**Why it matters:** if some monitors set a code in one trip and others need two,
and clearing/healing/erasing behave differently per family, the *presence* of a
code in the corpus is biased by monitor mechanics, not just by how often the
fault occurs. That bias would distort any family prior built from code counts.

**Wiki today:** has the maturation/clearing mechanics (pending→confirmed on 3rd
cycle, ≥40-warm-up erase, clearing resets LTFT + readiness, "all-clear scan is
untested"). But the explicit **one-trip vs two-trip** monitor split is not named,
and the **corpus-skew** implication is not drawn.

**Resolve it by answering:**

- Which monitors/codes are **one-trip** (MIL on first failure — typically
  safety/misfire-catalyst-damage and fuel-system) vs **two-trip** (need two
  consecutive failed cycles)? Pin the standard list for 1990–2010.
- How do erase-after-40-warm-ups and clear-on-disconnect behaviours differ by
  monitor type, and would that make any family **over- or under-represented** in
  a manually-collected case corpus?

**Web search terms:** "one trip vs two trip monitor DTC list", "type A type B
misfire one trip MIL", "two-trip detection logic OBD II", "trip definition
warm-up cycle erase 40", SAE J1979 / J1699-3 trip logic, Denton §5.4 trip/cycle
counts.

**Also needs (internal):** check whether our corpus over-weights one-trip
families (misfire, fuel-system) relative to two-trip ones (catalyst, EVAP).

**Complete answer =** the one-trip/two-trip code list for the era, plus an
explicit statement of the direction and rough size of any corpus skew.

---

## Q10 — What heuristic do techs use to pick the "primary" code among several? *(ranking)*

**Why it matters:** when several codes are stored at once, the rank step needs a
defensible rule for which one leads. The wiki has the *pieces*
(misfire-before-lean, Type A before Type B, permanent>confirmed>pending,
immobiliser-first in non-start) but no single consolidated ordering.

**Wiki today:** fragments scattered across chunks `01/02/06/10`; no standard
severity/priority convention stated as one rule the rank step can adopt.

**Resolve it by answering:**

- Is there a recognised professional/standards convention for **primary-code
  selection** (severity ordering, "fix this first" hierarchy)?
- How do techs order: safety/catalyst-damage (flashing-MIL misfire) → root-cause
  codes → downstream/secondary codes → soft/rationality codes? Where do sensor-
  circuit and "system too lean/rich" codes sit?
- Does the order differ when a known cause→effect chain exists (e.g. fix the
  misfire and the secondary lean code clears)?

**Web search terms:** "diagnostic priority which DTC to fix first", "primary vs
secondary DTC technician order", "DTC severity ranking standard", "code priority
hierarchy driveability", "flashing MIL first then", ASE/AVI diagnostic-strategy
guides, manufacturer "diagnostic trouble code priority" service-manual language.

**Complete answer =** a single ordered priority list (with the tie-break rules)
that the rank step could adopt as a convention, sourced to professional practice
rather than invented.

---

## After research — what to do with the answers

Each resolved question becomes either a wiki update (a pinned number with its
source citation) or, where it adds a contract field, a **proposal** with a named
COMLab/fault-atlas consumer — authored as its own task spec, one per session.
Q1/Q2/Q9's corpus counts are measurement tasks over `DTCLab/cases/`; Q3/Q10 are
wiki pins (convention + shortlist). None of this flips a ledger row here.
