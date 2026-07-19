# Per-cluster value-confirmation prompts (2026-07-01)

Nine focused research prompts, one per confusable cluster, to **confirm the numeric value bands and
tolerances** used to seed provisional synthetic sensor data (policy: `4DLab_CLAUDE.md` §Provisional
synthetic signals). Each was authored by studying its `research_answers/clusterN.md` so it asks ONLY
for values — ranges, fleet spread, distribution, and a CONFIRM/WIDEN/TIGHTEN/SHIFT/REJECT verdict —
and does **not** re-ask facts the cluster already established.

Hand each prompt to the deep-research tool **separately** (they are self-contained). Answers should
land in `v3/research/research_answers/` as `clusterN_values.md`, then each C-SYNTH task reconciles its
bands against the verdicts.

| Prompt | Cluster | State of numbers in the source answer |
|---|---|---|
| CLUSTER1 | mech vs misfire vs coolant | full band table — CONFIRM + get spread |
| CLUSTER2 | rich vs catalyst | bands drafted (repair-blog) — needs authoritative CONFIRM |
| CLUSTER3 | ECU/control | strong, many OEM-specific — separate generic vs OEM + spread |
| CLUSTER4 | exhaust leak vs lean vs biased O2 | ΔTrim/CO2 anecdotal — CONFIRM + leak-size dependence |
| CLUSTER5 | lean root cause | full decision matrix — CONFIRM + spread + altitude gap |
| CLUSTER6 | sensor under-detection | **sparse numbers** — mostly ESTABLISH (O2 ms, MAF %dev) |
| CLUSTER7 | cam/VVT | strong physics, **thin thresholds** — ESTABLISH deg/VE bands |
| CLUSTER8 | non-starter | full signature table — CONFIRM + spread + pulse-width gap |
| CLUSTER9 | confirm no-fault | full healthy-band table — CONFIRM the negative-class spread |
