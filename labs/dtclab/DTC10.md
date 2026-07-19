## DTCLab — DTC sanitization → routing tags (the main rank discriminator)

State: clean code; the discriminator it produces is **starved** — most outranked
cases have no DTC, and the generic-code→family mapping strength is unmeasured.

1. **Across the 1990–2010 petrol fleet, what fraction of real fault cases present
   a stored DTC at diagnosis time?** 64/90 outranked cases have none — if no-DTC
   is the norm, DTC discriminators are structurally weak. *(OUTRANKED, core)*
2. **What is the empirical P-code→family mapping strength?** Does P0171 reliably
   mean lean_condition, or fire across vacuum leak / MAF / fuel-pressure /
   exhaust-leak with similar frequency? Need real co-occurrence statistics.
   *(OUTRANKED)*
3. **Which manufacturer-specific (P1xxx) codes carry discriminating power the
   generic set lacks**, and can they be used without per-OEM databases? *(coverage)*
4. **Which freeze-frame parameters most improve family discrimination** (load,
   RPM, ECT, fuel-trim-at-freeze) and how consistent are they across OEMs?
   *(OUTRANKED)*
5. **How should DTC state (pending $07 / confirmed $03 / permanent $0A) weight
   the family prior differently** — what's the professional convention? *(ranking)*
6. **How should multi-DTC patterns be read as a combined signature** (e.g.
   P0300+P030x, or P0171+P0174) rather than independent tags? *(OUTRANKED)*
7. **Are GPF / Euro-6d hex-tailed codes (P244A) even in scope for 1990–2010**, or
   are they dead weight inherited from a wider-scope era? (Ties to the `T-FX-13`
   regex contract gap.) *(scope)*
8. **Can cylinder-specific misfire codes (P0301–P0308) plus their pattern/count
   discriminate mechanical vs ignition vs lean vs fuel misfire** from the DTC set
   alone? *(OUTRANKED)*
9. **How do one-trip vs two-trip monitor maturation and clearing behaviors bias
   which codes are present**, and could that skew the corpus toward/away from
   families? *(corpus realism)*
10. **What domain heuristic do professional techs use to pick the "primary" code**
    among several stored simultaneously? There may be a standard severity/priority
    ordering the rank step could adopt. *(ranking)*