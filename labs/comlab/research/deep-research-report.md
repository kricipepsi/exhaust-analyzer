# Evidence Review for Calibrated Confidence, Ranked Differentials, and Bounded Symptom Priors in Petrol OBD Fault Diagnosis

## Executive summary

This engine should stop treating “confidence” as evidence completeness and instead publish a **calibrated probability of correctness** for the leading fault family, learned on a held-out labeled set and externally checked with **reliability diagrams, ECE, and Brier score**. For multiclass outputs like ~12 near-exclusive fault families, the evidence supports classic post-hoc calibration of class scores, especially **Platt scaling** when calibration data are limited, **isotonic/PAV** when calibration data are larger, and **temperature scaling** when the model behaves like a logit-based classifier; **conformal prediction** is valuable when the product should output a **set of plausible families with guaranteed coverage**, but it does **not** by itself make a top-1 probability calibrated. citeturn5view4turn5view6turn5view0turn7search1turn36view0

For presentation and evaluation, the evidence favors a **ranked differential** over a single forced answer when signatures overlap. Across clinical analogs, the jump from top-1 to top-3 is often material: about **+17 to +33 percentage points** in several studies, which is exactly what you expect when near-confusable classes share signatures. citeturn11search13turn10view1turn13view0

A self-reported symptom matters, but published evidence suggests most single symptoms are **weak-to-moderate evidence**, not strong evidence: many individual symptom likelihood ratios cluster around **1 to 3**, with some better features reaching roughly **4**, while strong diagnostic evidence is usually reserved for objective tests or composite rules. The architect should therefore **bound symptom influence so it breaks ties and lifts close contenders, but does not overturn strong sensor/code/gas evidence**. citeturn23view4turn24search2turn38view0turn23view0

## Confidence calibration to real likelihood

**Finding.**  
The right target is a **calibrated posterior probability** for each fault family, estimated **after** the engine produces its raw class scores, and validated on held-out cases with final confirmed labels. The strongest transferable evidence supports this sequence:

First, use a **post-hoc calibrator** rather than the current evidence-completeness label. In clinical prediction, calibration is explicitly the agreement between predicted and true risk, and it is essential whenever individualized predictions are used for decision-making. Reliability diagrams show where the model over- or underestimates; ECE summarizes the average bin-wise gap; and the Brier score summarizes overall probabilistic error, though it mixes calibration and discrimination and should not be interpreted as calibration alone. citeturn36view0turn37view2turn37view4turn37view3

Second, choose the calibrator by score type and sample size. In the classic multiclass calibration paper, **Zadrozny and Elkan** recommend calibrating binary decompositions and recombining them for multiclass probability estimates; on **Pendigits**, calibrating naive Bayes with **PAV** improved test MSE from **0.0326 to 0.0241** and lowered error rate from **0.1672 to 0.1498**; on **20 Newsgroups**, PAV calibration improved MSE from **0.01625 to 0.01220** with a small error-rate gain from **0.15836 to 0.15305**. citeturn6view4

Third, when calibration data are modest, **Platt scaling** is usually the safer first choice. In **Niculescu-Mizil and Caruana** across **eight problems**, Platt scaling beat isotonic regression for **small-to-medium calibration sets under about 1,000 cases** for margin-based models such as SVMs and boosted trees; with **1,000 or more calibration cases**, isotonic regression was as good as or better than Platt, and for already well-calibrated models calibration could help little or even hurt when calibration sets were small. citeturn5view4turn5view5

Fourth, if the engine’s internal scores are logit-like, **temperature scaling** is the most practical low-variance correction. In **Guo et al.** on modern neural networks, temperature scaling improved reliability diagrams, **binning methods did not outperform temperature scaling**, and temperature scaling altered probabilities with **one parameter** while leaving class ranking intact; it was also much faster than isotonic or Bayesian binning methods. citeturn5view0turn5view1

Fifth, if the product requirement is “report a set of plausible causes with user-facing coverage,” then **conformal prediction** is the cleanest method. Conformal prediction converts model scores into **prediction sets** with a user-specified finite-sample marginal coverage level, such as a guarantee that the true label is included with probability **at least 1−α** under exchangeability. That property is very useful for an automotive “differential” output, but it is different from saying the top-1 probability is calibrated. citeturn7search1turn7search2

For discrete confidence tiers, the published literature supports two defensible approaches. One is **LR-based bands**, where likelihood ratios further from 1 provide stronger evidence; **Deeks and Altman** note that **LRs above 10** and **below 0.1** are generally strong rule-in and rule-out evidence. The other is **probability-banded reporting**, as in radiology systems such as **BI-RADS** and **O-RADS**, which tie categories to explicit malignancy-risk bands instead of arbitrary adjectives. That is the most transferable pattern for a human-facing diagnostic UX: define tiers by calibrated probability or LR, not by evidence completeness. citeturn38view0turn34search3turn33search1

**Evidence and sources.**  
Platt scaling maps raw scores through a sigmoid; isotonic regression uses a monotone step function; classic multiclass calibration can be built by calibrating binary decompositions and recombining; temperature scaling is a one-parameter post-hoc correction that usually preserves ranking; reliability diagrams, ECE, and Brier are standard verification tools in clinical and ML calibration literature. citeturn37view0turn37view1turn5view6turn5view0turn37view2turn37view4turn37view3

**Confidence.**  
**High** for the general recommendation to replace completeness labels with calibrated posteriors, to validate with reliability diagrams plus ECE/Brier, and to consider conformal prediction for set-valued outputs. **Medium** for the exact choice among Platt, isotonic, and temperature scaling in this automotive problem, because no petrol-OBD-specific calibration benchmark with your four-channel fusion structure was found. citeturn36view0turn5view4turn5view0turn7search1

**Data gaps and domain-transfer caveats.**  
I did **not** find a peer-reviewed benchmark specific to **1990–2010 petrol passenger cars in EU/NA** that compared Platt, isotonic, temperature scaling, and conformal prediction on a multiclass OBD fault-family task. The calibration advice here is therefore a transfer from general ML and clinical prediction-model literature, where the statistical problem is the same but the data-generating process differs. citeturn36view0turn5view4turn5view0turn7search2

## Single verdict versus ranked differential

**Finding.**  
When some fault-family pairs genuinely share a signature, a forced top-1 verdict is a product choice, not a reflection of certainty. In that setting, the evidence strongly favors **outputting a ranked differential** and measuring both **top-1** and **top-k** performance. The standard definition is simple: **top-k** or **any-correct-in-k** means the true class appears anywhere in the first *k* ranked candidates. In a medical analogue from **100 confirmed myocardial infarction cases**, symptom checkers reported **D1** when MI was first, **D3** when it appeared in the first three, and **D5** within the first five; mean sensitivity rose from **48% ± 31% at D1** to **73% ± 20% at D3** and **79% ± 14% at D5**. citeturn13view0

Across comparable clinical decision-support tasks, the top-1 to top-3 gap is often large. In the **Semigran 2015** audit of **23 symptom checkers on 45 standardized vignettes**, the correct diagnosis was listed **first in 34%** of cases and **within the first three in 51%**, a **17-point** gain. citeturn11search13turn20view4

In a **30-case emergency-department dataset using real patient self-reported symptom inputs**, **Ada** went from **30% top-1 to 63% top-3**; **ChatGPT-3.5** from **40% to 63%**; **ChatGPT-4.0** from **33% to 50%**; **WebMD** from **40% to 57%**; and the mean physician result was **47% top-1 versus 69% top-3**. Those are gains of **17 to 33 percentage points** from preserving the differential instead of forcing a single answer. citeturn10view1

A newer real-world symptom-checker study using **381 outpatient cases with confirmed diagnoses** defined success as the final diagnosis appearing **within a top-10 differential**, and found overall list accuracy of **45.1%**; accuracy fell to **24.2%** in uncommon disease and **14.5%** in atypical presentations. That study is not a top-3 result, but it reinforces the point that on ambiguous cases, list coverage contains useful information that top-1 alone throws away. citeturn4view8

User value is more nuanced than “top-k always helps.” In a randomized physician-vignette study, overall physician accuracy was **57.4% with** versus **56.3% without** an AI-generated differential list, so the list did not improve aggregate top-1 accuracy by itself. But when the AI list **contained the correct diagnosis**, the odds of physician correctness increased sharply (**adjusted OR 7.68, 95% CI 4.68–12.58**). The same study also found **15.9% omission errors** and **14.8% commission errors**, showing that ranked differentials are useful but can also induce automation bias if not paired with calibrated confidence and good UX. citeturn15search2

A related exploratory analysis found that at least **15%** of physicians’ differential diagnoses were affected by the AI-generated list. And in a separate trust-calibration study, physicians’ diagnostic accuracy was **54.5%** when their trust calibration was correct versus **20.8%** when it was incorrect, with trust calibration associated with better accuracy (**adjusted OR 5.90, 95% CI 2.93–12.46**). The design lesson is that **a ranked differential is valuable when it is paired with calibrated uncertainty**, not when it is presented as an unqualified oracle. citeturn12search5turn8view1

For this engine, the product implication is straightforward: if some families are structurally confusable, the UI should present a **lead candidate plus the next two or three plausible alternatives**, because that is more truthful to the evidence and more actionable for follow-up testing. Scoring should continue to report **top-1** for external comparability, but internal evaluation should add **top-2/top-3**, and ideally a set-based coverage metric if conformal prediction is adopted. This is an inference from the studies above, not a direct automotive benchmark result. citeturn13view0turn10view1turn15search2

**Evidence and sources.**  
The clinical literature repeatedly measures diagnostic success both as first-position correctness and as inclusion in a short list, and the gap is material. Differential lists can improve human performance when the correct answer is present, but can also create omission and commission errors when the human over-trusts the tool. citeturn11search13turn10view1turn15search2turn8view1

**Confidence.**  
**Medium.** The empirical case for ranked differentials is strong in clinical analogues and general multiclass classification, but I did **not** find a peer-reviewed benchmark on a directly comparable **petrol OBD four-channel, ~12-family** automotive task that reported both top-1 and top-3. citeturn13view0turn10view1turn11search0

**Data gaps and domain-transfer caveats.**  
I found no strong automotive UX study asking technicians whether a calibrated top-3 list improves trust, speed, or repair yield on **1990–2010 petrol** vehicles. The ranked-differential recommendation is therefore grounded mainly in clinical decision-support and general multiclass-evaluation evidence. citeturn15search2turn8view1turn13view0

## Magnitude of a self-reported symptom prior

**Finding.**  
The best published evidence says **history matters**, but **individual subjective symptoms are usually not strong evidence by themselves**. In the classic internal-medicine study summarized in later literature, the **history alone led to the final diagnosis in 76%** of patients, versus **12%** for the physical examination and **11%** for laboratory tests. That means the operator’s complaint should not be ignored. But it does **not** mean that a single self-reported symptom deserves a large prior boost in a multiclass engine. citeturn17search1

When quantified as likelihood ratios, most individual symptoms are modest. In a systematic review of chest-pain history, positive LRs ranged from roughly **1.3 to 4.1** for the more useful historical features, and several “negative” descriptors had LRs around **0.2 to 0.3**. Specific examples included **radiation to both arms or shoulders LR+ 4.1**, **exertional pain LR+ 2.4**, **diaphoresis LR+ 2.0**, **pressure LR+ 1.3**, and “pleuritic” or “reproducible with palpation” at about **0.2 to 0.3**. The authors concluded that chest-pain history is **helpful but imperfect**, and noted that some published symptom LRs likely **overestimate** their strength because symptoms were treated as independent when they were not. citeturn23view4turn23view3

A second systematic review of **signs and symptoms for acute myocardial infarction** reached a similar conclusion: **sweating** had the highest pooled **LR+ of 2.92 (95% CI 1.97–4.23)**, while specificity for many symptoms had little effect on likelihood. In other words, even in a domain where symptoms are central, single self-reported symptoms often land in the **weak-to-moderate** evidence range rather than the **strong evidence** range. citeturn24search2

By contrast, objective evidence often sits in a stronger LR regime. In diagnostic theory, **LRs above 10** are generally considered strong rule-in evidence. In the chest-pain/ACS literature, the review’s bottom line is that **troponin and ECG in the context of symptoms should be the focus**, rather than individual symptoms or risk factors in isolation, and that composite tools combining history with objective data perform best. citeturn38view0turn23view0

The reliability of self-report is also variable enough that its weight should be discounted when the complaint is vague, second-hand, or inconsistent. In one primary-care comparison of symptom self-report with the medical record, total agreement ranged from **61%** for sore throat to **88%** for muscle aches and earache; positive agreement was often much lower, from **13%** for chills to **58%** for earache, with cough being an exception. A broader meta-analysis of self-report versus register data in another health context found average **sensitivity 0.82** and **specificity 0.91**, again showing that self-report can be informative but is not noiseless. citeturn32search0turn32search3turn31search1

The most defensible bound, therefore, is to treat a self-reported primary symptom as **weak-to-moderate prior evidence unless and until your own calibration data prove otherwise**. A practical evidence-based transfer would be:

- default symptom boost in the range of **LR about 1 to 3** for routine complaints;
- only allow stronger influence if your own labeled fleet data show a stable higher LR for that complaint-family pairing;
- never let the symptom prior exceed the level of “strong” evidence, because published symptom LRs rarely approach the **>10** rule-in band that objective tests can achieve. citeturn23view4turn24search2turn38view0

For “break ties, not override strong evidence,” the evidence-supported product rule is: **cap the symptom contribution below the strength of strong objective evidence**, and explicitly discount it when the complaint is nonspecific, internally contradictory, or supplied through an intermediary rather than direct observation. That cap is an inference from the LR literature and the scarcity of direct automotive estimates; I did not find a published automotive standard that gives an exact numeric cap for driver complaints in a multiclass OBD engine. citeturn23view4turn38view0turn32search3

**Evidence and sources.**  
Clinical diagnosis depends heavily on history, but individual symptoms usually have modest LRs and imperfect reporting reliability. Objective tests and composite scores dominate when available. Evidence on direct self-diagnosis is mixed: the BMJ Open review found the evidence **does not support routine self-diagnosis** for several common conditions, although some **home-test-based** pathways, such as HIV self-testing against laboratory reference, achieved **pooled sensitivity 92.8%** and **specificity 99.8%** precisely because they added an objective test rather than relying on symptom report alone. citeturn17search1turn23view4turn29view0turn30view0

**Confidence.**  
**Medium.** Confidence is high that single self-reported symptoms should usually be bounded below strong objective evidence. Confidence is lower on the exact numeric cap for an automotive engine because I found **very little direct automotive literature** estimating likelihood ratios for owner-reported complaints such as rough idle, hard start, or poor fuel economy against confirmed fault families in the defined petrol fleet. citeturn23view4turn24search2turn38view0

**Data gaps and domain-transfer caveats.**  
No peer-reviewed source was found that estimates complaint-to-fault-family likelihood ratios for **EU/NA petrol passenger cars from ~1990–2010** in a way that would justify a precise symptom-prior coefficient. The weighting advice here is a domain transfer from clinical evidence-based diagnosis and diagnostic-test theory. citeturn17search1turn23view4turn38view0

## Tier-definition table

The table below is a **recommended transfer**, not an automotive standard. It combines the diagnostic-test LR interpretation literature with medical reporting systems that map categories to explicit probability bands.

| Confidence tier | LR or posterior band it maps to | Calibration method that can produce it | Source |
|---|---|---|---|
| Definitive | **Posterior ≥95%** or evidence equivalent to **LR+ >10** versus the leading alternative / prior odds | Calibrated posterior from Platt, isotonic, or temperature scaling; alternatively a risk-banded reporting scheme after external calibration | Deeks & Altman on strong LR bands; BI-RADS category 5 >95%; O-RADS high-risk categories use explicit PPV bands. citeturn38view0turn34search3turn33search1 |
| Probable | **Posterior ~50–95%** or moderate rule-in evidence, roughly **LR+ 5–10** | Calibrated posterior from post-hoc calibration; optionally class-conditional conformal set if top-1 remains below “definitive” | BI-RADS 4C 50–95%; Deeks & Altman on LR strength increasing with distance from 1. citeturn34search3turn38view0 |
| Possible | **Posterior ~10–50%** or weak-to-moderate evidence, roughly **LR+ 2–5** | Calibrated posterior; ranked differential recommended; conformal set useful here | BI-RADS 4A/4B spans 2–10% and 10–50%; McGee and LR-band teaching literature treat LR 2–5 as a small-to-moderate shift. citeturn34search3turn21search2turn38view0 |
| Uncertain differential only | **Posterior below ~10% for any single class**, or top class not separated enough from runners-up | Ranked top-2/top-3 or conformal prediction set rather than a single verdict | O-RADS/BI-RADS show that low-risk bands are still reportable; conformal prediction supports set output with coverage control. citeturn33search1turn34search7turn7search1 |

A practical UX implication follows: if the model cannot honestly reach a “probable” or “definitive” band after calibration, it should **show the ranked differential and the missing evidence needed to separate the top families**, rather than convert uncertainty into a misleading certainty label. citeturn36view0turn7search1turn15search2

## Consolidated source table

| Source | Type | Year | Domain | Claim supported | Access | Link |
|---|---|---:|---|---|---|---|
| Platt, *Probabilistic Outputs for Support Vector Machines* citeturn4view0 | Peer-reviewed conference chapter | 1999 | General ML | Basis of sigmoid post-hoc calibration for scores | Free | Linked citation |
| Zadrozny & Elkan, *Transforming Classifier Scores into Accurate Multiclass Probability Estimates* citeturn4view1turn6view4 | Peer-reviewed conference paper | 2002 | General ML | Multiclass calibration by calibrating binary problems; Pendigits and 20 Newsgroups MSE improvements | Free | Linked citation |
| Niculescu-Mizil & Caruana, *Predicting Good Probabilities With Supervised Learning* citeturn4view3turn5view4 | Peer-reviewed conference paper | 2005 | General ML | Platt better with smaller calibration sets; isotonic better with larger sets | Free | Linked citation |
| Guo et al., *On Calibration of Modern Neural Networks* citeturn4view2turn5view0 | Peer-reviewed conference paper | 2017 | General ML | Temperature scaling is strong, simple post-hoc calibration; reliability diagram and ECE usage | Free | Linked citation |
| Angelopoulos & Bates, *A Gentle Introduction to Conformal Prediction* citeturn7search1 | Tutorial / methods paper | 2021 | General ML | Conformal prediction provides prediction sets with user-chosen finite-sample marginal coverage | Free | Linked citation |
| Huang et al., *A Tutorial on Calibration Measurements and Calibration Models for Clinical Prediction Models* citeturn36view0turn37view4 | Peer-reviewed tutorial review | 2020 | Medical / general | Calibration definitions; reliability diagrams, ECE, Brier, Platt, isotonic in clinical prediction | Free | Linked citation |
| Deeks & Altman, *Diagnostic Tests 4: Likelihood Ratios* citeturn38view0 | Peer-reviewed methods note | 2004 | Medical / general | LR interpretation; LR >10 and <0.1 as strong evidence bands | Free | Linked citation |
| Semigran et al., *Evaluation of Symptom Checkers for Self Diagnosis and Triage* citeturn11search13turn20view4 | Peer-reviewed audit study | 2015 | Medical DDSS | Top-1 34%, top-3 51% on 45 standardized vignettes across 23 symptom checkers | Free | Linked citation |
| Wallace et al., *The Diagnostic and Triage Accuracy of Digital and Online Symptom Checker Tools* citeturn11search0 | Peer-reviewed systematic review | 2022 | Medical DDSS | Across studies, primary diagnostic accuracy 19–36% and top-3 33–58% | Free | Linked citation |
| Fraser et al., *Comparison of Diagnostic and Triage Accuracy…* citeturn10view1 | Peer-reviewed study | 2023 | Medical DDSS | Real-patient ED symptom data: large gains from top-1 to top-3 | Free | Linked citation |
| Wallace et al., *Evaluating the Diagnostic and Triage Performance… for Myocardial Infarction* citeturn13view0 | Peer-reviewed study | 2024 | Medical DDSS | Direct D1/D3/D5 definition of top-k style diagnostic sensitivity | Free | Linked citation |
| Harada et al., *Efficacy of AI-Driven Differential-Diagnosis List on Physicians’ Diagnostic Accuracy* citeturn15search2 | Peer-reviewed randomized study | 2021 | Medical DDSS / human factors | Correct-in-list helps; omission and commission errors exist | Free | Linked citation |
| Harada et al., *Effects of a Differential Diagnosis List of Artificial Intelligence on Differential Diagnoses by Physicians* citeturn12search5 | Peer-reviewed exploratory analysis | 2021 | Medical DDSS / human factors | About 15% of physicians’ differentials were affected by the AI list | Free | Linked citation |
| Niki et al., *Facilitating Trust Calibration in AI-Driven Diagnostic Decision Support Systems* citeturn8view1 | Peer-reviewed quasi-experimental study | 2024 | Medical DDSS / human factors | Trust calibration accuracy associated with markedly better physician diagnosis | Free | Linked citation |
| Peterson et al., *Contributions of the History, Physical Examination, and Laboratory Investigation* citeturn17search1 | Peer-reviewed observational study | 1992 | Medical diagnosis | History contributed to diagnosis in 76% of cases | Free snippet / abstract | Linked citation |
| Swap & Nagurney, *Value and Limitations of Chest Pain History* citeturn23view4turn23view3 | Peer-reviewed review | 2005 | Medical diagnosis | Individual symptom LRs are usually modest; history is helpful but imperfect | Free PDF | Linked citation |
| Bruyninckx et al., *Signs and Symptoms in Diagnosing Acute Myocardial Infarction* citeturn24search2 | Peer-reviewed systematic review | 2008 | Medical diagnosis | Highest pooled symptom LR+ only about 2.92 for sweating | Free | Linked citation |
| McLellan et al., *Accuracy of Self-Diagnosis in Conditions Commonly Managed in Primary Care* citeturn29view0turn30view0 | Peer-reviewed systematic review / meta-analysis | 2023 | Medical self-diagnosis | Evidence does not support routine self-diagnosis for several conditions; HIV self-testing works better because it adds objective testing | Free | Linked citation |
| Barbara et al., *Agreement Between Self-Report and Medical Records on Signs and Symptoms of Respiratory Illness* citeturn32search0turn32search3 | Peer-reviewed observational study | 2012 | Medical measurement | Self-report agreement on symptoms varies widely; positive agreement can be poor | Free snippet | Linked citation |
| BI-RADS summary sources for explicit risk bands citeturn34search3turn34search7 | Clinical reporting framework / summary | 2023–2026 summaries of ACR framework | Medical reporting | Example of non-arbitrary probability-banded categories | Free | Linked citation |
| O-RADS US risk stratification system citeturn33search1 | Peer-reviewed reporting framework | 2020 | Medical reporting | Example of standardized probability-banded categorical reporting | Paid/abstract accessible | Linked citation |

## Could not be found and final verdict

**Could not be found.**  
No peer-reviewed source was found that directly estimates **likelihood ratios or calibrated prior strengths for owner-reported complaints** against confirmed **petrol OBD fault families** in **1990–2010 EU/NA passenger cars**. citeturn11search0turn14search4

No strong published benchmark was found comparing **top-1 versus top-3** specifically for a **four-channel automotive fault-diagnosis engine** of the type described here. citeturn14search4turn14search23

No automotive standard was found that defines technician-facing confidence tiers like **definitive / probable / possible** in explicit **posterior-probability or LR bands** analogous to BI-RADS or O-RADS. citeturn33search19turn34search3

No petrol-vehicle benchmark was found that directly compares **Platt scaling, isotonic regression, temperature scaling, and conformal prediction** on multiclass OBD fault-family outputs. citeturn14search4turn36view0

**One-line verdict.**  
The highest-leverage change is **to calibrate the existing ranked differential into real probabilities and present that differential explicitly**; rebounding the symptom prior matters, but it is secondary. citeturn36view0turn10view1turn15search2turn23view4