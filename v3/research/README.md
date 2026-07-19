# v3 Phase-4 Research Pack — blocking-measurement briefs

These files are **external-research prompts**. They identify the additional measurements that
would let the engine separate fault families a single warm-idle 5-gas snapshot cannot — the
discrimination-blocked cases (PRODUCER_GAP + DATA_GAP) that cap accuracy.

## How to use
For each research run, give the agent **two files**: the shared context + one cluster brief.

```
  00_4DLAB_CONTEXT.md   +   CLUSTER_<n>_*.md   ->   one research run
```

The context document is identical for every cluster; the cluster brief is the specific question.
Run clusters independently (they can be parallelized). Cluster 2 (rich vs catalyst) is the
largest blocked bucket — a good first run.

## Files
- `00_4DLAB_CONTEXT.md` — the system, its four input channels, the 12 fault families, the
  discrimination limits, and the two-point (RPM-step) discriminator hypothesis. Pair with each brief.
- `CLUSTER_1_mechanical_vs_misfire.md` — mechanical wear vs ignition misfire vs coolant intrusion.
- `CLUSTER_2_rich_vs_catalyst.md` — rich mixture vs catalyst failure (largest blocked bucket).
- `CLUSTER_3_ecu_control_fault.md` — ECU/control fault vs the chemistry faults it imitates.
- `CLUSTER_4_exhaust_leak_vs_lean_vs_sensor.md` — false-lean: exhaust leak vs lean vs biased O2.
- `CLUSTER_5_lean_root_cause.md` — lean sub-cause: vacuum leak vs fuel delivery vs MAF under-read.
- `CLUSTER_6_sensor_under_detection.md` — lazy/biased sensor read as healthy (under-detection).
- `CLUSTER_7_cam_timing_vvt.md` — cam timing / VVT.
- `CLUSTER_8_non_starter.md` — no-start root cause (gas + live-OBD suppressed).
- `CLUSTER_9_confirm_no_fault.md` — reliably confirming a healthy vehicle without false-healthy.

## What comes back feeds
Each brief asks for a ranked discriminator + acquisition protocol + expected signature +
feasibility tier + citations, ending with a "minimum added-signal set." Those answers become the
acquisition spec for the deferred Phase-4 signal tasks in the v3 plan.
