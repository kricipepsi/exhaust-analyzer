### DNALab / VINLab — vehicle identity + operator symptom (the independent prior)

State: the richest *untapped* channel, but the prior is weak in practice — low
symptom density, PARTIAL VIN confidence, ~62–65% CoC fill, empty `model`.

1. **How predictive is a user-reported primary symptom of the true fault
   family?** Need the empirical confusion matrix between reported symptom and
   confirmed fault to set the prior's strength honestly. *(never-surfaced, core)*
2. **What is realistic VIN-decode resolution for 1990–2010 vehicles** — can VIN
   reliably yield engine code, induction, fuel delivery, O₂ config, EGR/cat
   equipment, or is decode too partial? (Traces show `confidence=PARTIAL`
   uniformly.) *(data quality)*
3. **Do accessible per-engine-code CoC / type-approval idle datasets exist for
   this fleet, and how complete?** Currently ~62–65% filled from CSV medians — is
   there a real source? *(data availability)*
4. **Which vehicle-identity attributes actually interact with the diagnosis**
   (change the correct answer given the same gas/OBD signature) versus being
   collected but diagnostically inert? *(signal/noise)*
5. **What structured-symptom vocabulary do professional techs actually use**, and
   is the current 18-pair tier_1/tier_2 catalog complete and correctly mapped to
   families? *(coverage)*
6. **How should environmental context (cold/hot, occurs-during, engine-state)
   modify the family prior** — is there documented symptom-context→fault
   evidence? *(ranking)*
7. **How prevalent are non-VIN-decodable aftermarket mods (de-cat, aftermarket WB
   O₂) in the target fleet, and how much do they corrupt diagnosis if unknown?**
   *(data quality)*
8. **Does finer identity (`model`, engine variant) actually matter for
   diagnosis**, or is engine_code + displacement + induction sufficient? `model`
   is always empty today — confirm it can stay that way. *(scope)*
9. **What is the real-world rate of false/misleading operator symptom reports**
   that should bound how far the symptom prior is trusted? *(prior bounding)*
10. **Does labeled symptom→confirmed-fault data exist (e.g. repair-order
    datasets) to validate or train the prior**, rather than synthetically
    enriching the corpus? *(data availability)*
5. **Operator-symptom predictiveness (DNALab Q1).** The cheapest independent
   channel; quantifying its real strength tells you how hard to lean on it.