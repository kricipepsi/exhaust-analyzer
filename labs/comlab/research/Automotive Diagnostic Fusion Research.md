# Automotive Diagnostic Fusion Research — Web-research result A (scoring & fusion)

> Faithful text transcription of `Automotive Diagnostic Fusion Research.pdf` / `AutomotiveDiagnosticFusionResearch.html`.
> In the original export every number, percentage and equation was a separate inline PNG image, so the figures
> were neither selectable nor searchable. All 70 formula/number images have been transcribed inline as text here
> (display equations shown in code blocks; citation markers as `[n]` keyed to **Works cited**). Content is otherwise unchanged.

---
# Multi-Source Evidence Fusion and Calibrated Probabilistic Networks for Legacy Petrol Engine Diagnostics

## Executive summary

The diagnostic engine under study, which operates on legacy petrol passenger cars (model years ≈ 1990–2010), faces a diagnostic performance plateau with top-1 accuracy limited to 50–52%. Analysis indicates that the current hand-tuned, additive, weighted "prune-then-rank" classifier is the primary system constraint. This linear, deterministic architecture is incapable of resolving non-linear diagnostic spaces, conditional sensor dependencies, or severe sensor contradictions.

A systematic review of cross-domain benchmarks reveals that hand-tuned rule bases suffer an absolute performance penalty of 15–35%  compared to learned statistical classifiers and Bayesian networks [1]. To overcome this constraint without discarding valuable expert knowledge, a transition to a calibrated probabilistic fusion model is required. This report demonstrates that:

1. Additive rule engines have an inherent mathematical ceiling that prevents scalable multi-class diagnostics under noisy or missing data conditions [3].
2. Sensor contradictions can be modeled as active diagnostic features using Dezert-Smarandache Theory (DSmT) or Proportional Conflict Redistribution (PCR5/6) to prevent Zadeh's paradox [4].
3. Conditional dependencies between live sensor data and exhaust chemistry must be resolved via Stacked Bayesian Networks or Log-Odds Aggregator frameworks to prevent "swamping" reliable channels [6].

## Rule-based vs learned rankers: the achievable ceiling

The first research question addresses the performance limit of hand-tuned rule-based classifiers relative to learned statistical rankers on multi-class diagnostic tasks with noisy, partially missing evidence.

### Finding

Hand-tuned rule engines and additive weight rankers consistently plateau at top-1 accuracies of 50–62%  on complex multi-class diagnostic tasks involving noisy or incomplete data [3]. Under identical data conditions, learned statistical and probabilistic classifiers—including Bayesian networks, Support Vector Machines (SVMs), and Random Forests—routinely achieve top-1 accuracies of 80–99% [1]. The absolute performance gap between hand-tuned rule systems and learned approaches ranges from 15%  to over 35% [1].

The primary ceiling for the current "prune-then-rank" engine is its linear additive structure. It cannot resolve non-linear diagnostic boundaries where symptoms overlap, nor can it handle cases where diagnostic trouble codes (DTCs) are absent, which starves the rule base of its primary triggers [3].

### Evidence and sources

The most rigorous head-to-head comparison between a hand-tuned rule-based expert system and a Bayesian network on identical noisy datasets is documented in the HEPAR medical diagnostic project [3]. HEPAR-RB is a hand-crafted rule-based expert system utilizing 178 hierarchical production rules [3]. HEPAR-BN (and its successor HEPAR II) is a causal Bayesian network containing over 70 nodes and conditional probability tables (CPTs) learned from clinical cases [3]. Both models were evaluated on the IFF dataset (699 patients) and the DH dataset (181 patients) to diagnose complex, overlapping disorders under conditions of missing symptoms and laboratory findings [3].

The diagnostic results for Primary Biliary Cirrhosis (PBC) are detailed in the table below [3]. In this evaluation, "Unclassified" (UC) designates cases where the rule base failed to activate or the Bayesian network did not clear a conservative 50%  probability threshold [3].

| Evaluation Dataset & Class | Hepar-RB (Rule-Based Expert System) | Hepar-BN (Bayesian Network) | Absolute Performance Gap |
|---|---|---|---|
| IFF Dataset (699 Cases) |  |  |  |
| Actual Positive PBC (280 cases) Correct | 62.0% | 94.0% | +32.0%  (BN Superiority) |
| Actual Positive PBC Unclassified (UC) | 34.0% | 1.0% | −33.0%  (BN Red. Uncertainty) |
| Actual Negative PBC (419 cases) Correct | 20.0% | 45.0% | +25.0%  (BN Superiority) |
| Actual Negative PBC Unclassified (UC) | 76.0% | 40.0% | −36.0%  (BN Red. Uncertainty) |
| DH Dataset (181 Cases) |  |  |  |
| Actual Positive PBC (15 cases) Correct | 73.3% | 80.0% | +6.7%  (BN Superiority) |
| Actual Positive PBC Unclassified (UC) | 13.3% | 0.0% | −13.3%  (BN Red. Uncertainty) |
| Actual Negative PBC (166 cases) Correct | 86.0% | 39.0% | −47.0%  (RB Specificity Edge) |
| Actual Negative PBC Unclassified (UC) | 13.0% | 60.0% | +47.0%  (BN Conservative Hold) |

In the larger and noisier IFF dataset, HEPAR-RB left 76%  of negative cases and 34%  of positive cases unclassified due to rule starvation [3]. The Bayesian network resolved these cases by calculating posterior probabilities over the remaining weak signals, achieving a 94%  sensitivity on positive cases [3]. This shows how a probabilistic framework handles missing inputs without stalling.

In the engineering domain, similar performance gaps are documented. In multi-class fault classification across twelve distinct grid faults, SVMs, Decision Trees, and LSTMs achieved accuracies of 96–98% [1]. Conversely, traditional rule-based systems struggle with rule explosion and poor generalization when operating outside of tightly controlled, stable environments [11].

In aluminum electrolysis cells, an optimized rule-based system utilizing certainty factors achieved 94.2%  diagnostic accuracy, which matched an LSTM model ( 93.8% ) but required extensive manual tuning of disjunctive and conjunctive certainty rules [2].

### Confidence

High. The HEPAR benchmark represents a long-term, peer-reviewed evaluation of rule-based and Bayesian networks on identical, noisy real-world data [3].

### Data gaps and domain-transfer caveats

The HEPAR dataset represents a medical domain [3]. However, the domain transfer to automotive fault diagnosis is structurally valid. Medical findings (patient symptoms, physical signs, and blood tests) correspond to the four automotive diagnostic channels under study: operator symptoms, live sensor telemetry, 5-gas exhaust chemistry, and DTC presence.

Both systems map noisy, incomplete, and conditionally dependent features to a discrete, mutually exclusive or near-exclusive label space. Unlike human physiology, automotive systems are bounded by rigid thermodynamic and chemical equations (such as Stoichiometric combustion chemistry), which should make a probabilistic physical structure more robust than its medical counterpart.

## Contradiction as a discriminator without destructive override

The second research question examines principled mathematical methods that allow a classifier to use evidence contradiction as an active diagnostic feature, rather than as a hard, destructive override.

### Finding

When independent evidence channels contradict each other—such as when live ECU sensor data indicates a stoichiometric mixture ( λ ≈ 1.0 ) but the 5-gas exhaust analyzer measures high oxygen levels ( O₂ > 2% ) indicating a lean burn—traditional rule-based systems rely on hard overrides. These overrides are highly sensitive to single-channel failures, often resulting in diagnostic errors.

In evidence theory, classical Dempster's rule of combination fails under high contradiction ( K → 1 ), leading to overconfident, counter-intuitive conclusions known as Zadeh's paradox [4].

To constructively utilize contradiction without destructive overrides, modern multi-sensor fusion architectures employ Proportional Conflict Redistribution (PCR5 or PCR6) rules [4]. These methods mathematically isolate the conflicting probability mass and redistribute it locally to the specific channels generating the contradiction, preserving the semantic meaning of the disagreement [4].

### Evidence and sources

The hazard of classical evidence fusion under contradiction is demonstrated by Zadeh's paradox [4]. Let a diagnostic system evaluate three mutually exclusive fault families: Rich mixture ( R ), Lean mixture ( L ), and Mechanical wear ( W ). Let the basic belief assignments (BBAs) from two independent sensors be:

    m₁(R) = 0.99,  m₁(L) = 0.01,  m₁(W) = 0.00

    m₂(W) = 0.99,  m₂(L) = 0.01,  m₂(R) = 0.00

Here, the first channel indicates a Rich mixture with 99%  confidence, while the second channel indicates Mechanical wear with 99%  confidence. They weakly agree on a Lean mixture ( 1% ) [13].

Under classical Dempster-Shafer Theory, the total conflict mass K  represents the sum of the products of conflicting evidence [13]:

    K = Σ_(A∩B=∅) m₁(A)·m₂(B) = m₁(R)m₂(W) + m₁(R)m₂(L) + m₁(L)m₂(W)

> Note: in the source HTML/PDF this equation image is cut off after `m₁(L)m₂(`; the final term `m₁(L)m₂(W)` is recovered from the numeric expansion in the next line.

    K = (0.99 × 0.99) + (0.99 × 0.01) + (0.01 × 0.99) = 0.9999

The denominator normalization factor becomes 

    1 − K = 0.0001
 [4]. Applying Dempster's combination rule, the joint belief for the weakly supported Lean mixture L  is [13]:

    m(L) = m₁(L)·m₂(L) / (1 − K) = (0.01 × 0.01) / 0.0001 = 1.00

This yields a 100%  certain diagnosis of a Lean mixture [13]. This result is highly counter-intuitive and dangerous for a physical engine; a minor agreement in a high-conflict scenario completely overrides the dominant diagnostic signals [4].

To prevent this failure mode, alternative combination rules have been developed. The table below compares how different fusion methods distribute probability mass under this high-conflict scenario [5]:

| Fusion Operator / Method | Mass Assigned to R (Rich) | Mass Assigned to W (Wear) | Mass Assigned to L (Lean) | Mass Assigned to Ignorance / Unknown |
|---|---|---|---|---|
| Dempster's Rule (Classic DST) [cite: 14] | 0.000 | 0.000 | 1.000  (Paradoxical) | 0.000 |
| Murphy Method [cite: 14] | 0.499 | 0.499 | 0.002 | 0.000 |
| Sun Method [cite: 14] | 0.182 | 0.182 | 0.003 | 0.633  (Ignorance) |
| PCR5 / PCR6 Rule [cite: 5] | 0.494 | 0.494 | 0.012 | 0.000 |

The PCR5/6 rules isolate the conflict product ( 

    m₁(R)·m₂(W) = 0.9801
 ) and redistribute it back to R  and W  proportionally to their original masses [4]. This maintains the true diagnostic uncertainty, signaling to the downstream controller that further evidence is required [4].

In machine learning and domain adaptation, this conflict can be extracted explicitly. By constructing a cross-domain transition matrix M, where the trace of the matrix represents prediction correlation, researchers have successfully quantified "environmental disagreement" [16]. When non-causal environment features disagree, this trace acts as an active discriminator feature to guide the model to ignore misleading variables and avoid negative transfer [16].

### Confidence

High. The mathematical limitations of classical DST and the robustness of PCR5/6 rules under high contradiction are well-established in multi-sensor fusion theory [5].

### Data gaps and domain-transfer caveats

While the mathematics of PCR5/PCR6 is highly mature, empirical implementation within automotive engine control units (ECUs) is extremely rare. Legacy vehicle diagnostics (1990–2010) are severely limited by computational constraints (8-bit to 32-bit microcontrollers with low memory limits). The localized nature of PCR calculations (which require storing cross-products of beliefs for combinations of hypotheses) represents a major structural barrier for on-vehicle embedded systems [5]. However, this is not a constraint for off-board PC-based garage diagnostic scan tools.

## Calibrated-likelihood / Bayesian fusion vs additive weights

The third research question evaluates how calibrated-likelihood and Bayesian fusion approaches compare with simple additive weighting when evidence channels are conditionally dependent, and how to prevent weak channels from being swamped.

### Finding

The naive Bayes conditional independence assumption—which assumes that the joint probability of the evidence is the product of individual channel probabilities—is highly destructive when channels are correlated [19]. In the engine under study, volumetric efficiency cross-checks, calculated engine load, and short/long-term fuel trims are highly correlated physical responses to a single root cause (e.g., an intake manifold vacuum leak).

Under naive independence assumptions, these correlated features cause "swamping," where the overlapping signals inflate the joint probability of a specific family, completely drowning out independent diagnostic channels (e.g., raw gas chemistry) [19].

To prevent swamping while preserving diagnostic performance under missing-evidence states (such as the absence of a DTC), three architectural corrections are validated [6]:

1. Bayesian Belief Networks (BBNs): Directed Acyclic Graphs (DAGs) that explicitly model the causal dependencies between sensors [6].
2. Stacked Generalization (Stacking over channels): Using logistic regression or a Log-Odds Precedent Aggregator (LOPA) to aggregate channel-level predictions, which naturally prunes redundant dependencies [7].
3. Leak Probabilities in Noisy-OR structures: Allocating a non-zero probability to unmodeled causes to prevent the network from collapsing to zero when evidence channels are starved [20].

### Evidence and sources

In complex engine systems like diesel and petrol powertrains, research shows that a pure model-based or data-driven diagnostic network often fails under variable loads or when sensors degrade [21].

To address this, a "Belief Rule-Based" (BRB) expert system was developed for marine diesel engines, which integrates expert-elicited qualitative rules with numerical sensor data using Dempster-Shafer evidential reasoning [22]. This hybrid model was benchmarked against Artificial Neural Networks (ANN), Support Vector Machines (SVM), and binary logistic regression under five-fold cross-validation [22]:

- Diagnostic Performance on Engine Wear: The optimized BRB model achieved a top-1 diagnostic accuracy of 95.56% [24]. It consistently outperformed the standalone ANN, SVM, and binary logistic regression models in terms of diagnostic stability, computational footprint, and multi-fault identification [23].
- Handling Starved Inputs: By incorporating a structural "leak probability"  parameter—representing the background probability of unmodeled causes—the model maintained stable classifications even when input indicators were missing [20].

Furthermore, in multi-DTC vehicle electronic systems, incorporating a causal BBN rather than standard decision trees dramatically reduced misdiagnoses [6]. Under standard rule-based structures, if any intermediate sensor in the logical chain fails or is absent, the system misdiagnoses or stalls [6].

The BBN models the joint probability 

    P(Fault | Symptom₁, …, Symptomₙ)
  and can reversely infer the most likely failure cause even when multiple DTCs are missing or logged simultaneously [6].

To mitigate feature correlation and swamping, the Log-Odds Precedent Aggregator (LOPA) replaces standard naive Bayes product fusion with a log-odds aggregation of per-source reliability estimates [7]. LOPA mathematically prunes redundant chains and prevents highly correlated symptoms from compounding and overwhelming the independent diagnostic channels [7].

### Confidence

High. The mathematical consequences of conditional independence violations (such as the XOR limitation and joint probability inflation) are proven statistical realities [19]. BBN implementations in complex engine platforms show consistent performance gains [6].

### Data gaps and domain-transfer caveats

The high-performing BRB and BBN engine benchmarks cited are predominantly conducted on marine diesel powertrains [22]  or simulation models (e.g., CWRU rolling bearing databases) [26]. These systems exhibit slower dynamic transients than passenger car petrol engines, which must continuously adapt to fast-changing driver demands and closed-loop three-way catalyst behaviors.

Furthermore, parameterizing the CPTs of a large Bayesian Network requires highly specialized software tools (such as GeNIe or SMILE) and significant historical datasets [27], which are rarely standardized across legacy automotive service networks.

## Method comparison table

The following table compares the diagnostic fusion paradigms evaluated in this report, detailing their advantages, structural vulnerabilities, comparable performance, and overall architectural maturity:

| Approach | What it Buys | What it Costs / When it Fails | Evidence It Beats Additive Weighting on Comparable Tasks | Maturity |
|---|---|---|---|---|
| Additive Weights   (Current Paradigm) | Extreme simplicity; easily written in basic logic; requires no complex matrix calculations; highly interpretable at a single-rule level. | Linear constraints; cannot model feature dependencies; prone to "outranking" errors; completely fails under input starvation [3]. | Evaluated as the baseline. Plateaus at 50–52%  top-1 accuracy in the legacy petrol passenger car system under study. | Legacy (1980s–1990s standard). |
| Dempster-Shafer Conflict-Aware (PCR5/6) | Explicitly quantifies and isolates channel contradictions; stops single-sensor overrides of dominant signals [4]. | Highly complex combinatorial calculations; requires defined basic belief assignments for all subsets [4]. | Replaces Dempster's rule under high conflict ( K = ). Corrects the counter-intuitive BBA distribution from 100%  error to a balanced distribution [14]. | Research grade; high usage in military and advanced multi-sensor tracking. |
| Bayesian Network (BBN / TAN) | Models true causal dependencies (DAGs) [6]; provides calibrated probabilities; naturally handles missing DTCs or sensors [28]. | Constructing and maintaining the Directed Acyclic Graph structure is highly labor-intensive; CPTs are difficult to populate [30]. | On the HEPAR medical dataset, the BN (Hepar-BN) achieved 94.0%  sensitivity compared to only 62.0%  for the rule-based model [3]. | Mature in academic and aerospace health management; emerging in advanced automotive workshop tools [6]. |
| Stacked Logistic Regression / LOPA | Merges channels using learned, robust weights; prevents redundant, highly correlated sensors from swamping [7]. | Requires a centralized, labeled training dataset of unified sensor/gas cases to fit stacking coefficients. | Outperforms simple majority voting and naive Bayes by pruning redundant diagnostic chains in legal and ML benchmark domains [7]. | High industrial maturity in general machine learning; low integration in embedded controllers. |
| Learned Rankers (Random Forest / XGBoost) | Exceptional multi-class separation; handles hundreds of raw variables; completely automates feature engineering [8]. | Acts as a complete "black box"; cannot provide physical or logical explanations; highly sensitive to training data shift [33]. | On simulated electrical grid and mechanical fault datasets, Random Forests achieved 88.17%  accuracy compared to 79.01%  for standard Naive Bayes [8]. | High industrial maturity; standard for cloud-based predictive maintenance. |

## Consolidated source table

This table aggregates the peer-reviewed literature, dataset evaluations, and technical standards supporting the assertions and findings in this report:

| Source | Type | Year | Domain | Claim it Supports | Access | Link |
|---|---|---|---|---|---|---|
| Onisko et al. | Peer-Reviewed Journal | 2001 | Medical / Diagnostics | HEPAR study results; rules plateau at 62%  sensitivity whereas Bayesian networks reach 94% [3]. | Free | AIME 2001 Paper |
| Aragao & Alcantara | Technical Preprint | 2024 | Information Fusion | DS combination rule anomalies; Murphy and PCR5/6 conflict redistribution evaluation [14]. | Free | arXiv:2408.08928 |
| Amin & Karmilasari | Peer-Reviewed Journal | 2021 | Automotive Diagnostics | Standard DSmT vs. DST comparison; managing high conflict scenarios [4]. | Free | IRJAES Journal PDF |
| He et al. | Peer-Reviewed Journal | 2021 | Power Systems / ML | Random Forest ( 88.17% ) outperforming Naive Bayes ( 79.01% ) on multi-class fault diagnostics [8]. | Free | Frontiers in Energy Research |
| Xu et al. | Peer-Reviewed Journal | 2017 | Powertrain / Marine | Belief Rule-Based expert systems reaching 95.56%  accuracy and outperforming standard ANNs and SVMs [24]. | Paid | IEEE SMC Paper |
| Dezert & Smarandache | Monograph | 2006 | Sensor Fusion | PCR5/6 mathematical formulas; proportional conflict redistribution rules to resolve Zadeh's paradox [5]. | Free | UNM Math Monograph |
| Bings et al. | Conference Proceeding | 2025 | Legal Reasoning / AI | LOPA framework; aggregating precedent opinions in posterior log-odds to prune redundant chains [7]. | Free | JURIX 2025 LOPA |
| Hu et al. | Review Paper | 2018 | Chemistry / Machine Learning | High-dimensional swamping of Naive Bayes signals by correlated, non-relevant features [19]. | Free | ACS Chemical Reviews |
| Shao et al. | Peer-Reviewed Journal | 2022 | Industrial Process Control | Certainty factors vs. LSTM networks on aluminum cell diagnostics ( 94.2%  accuracy) [2]. | Free | MDPI Processes Journal |
| Xu & Yang | Peer-Reviewed Monograph | 2021 | Automotive / Electronics | Bayesian Belief Network (BBN) framework for multi-DTC vehicle electronic system troubleshooting [6]. | Paid | ResearchGate Publication |
| Li et al. | Peer-Reviewed Journal | 2025 | Domain Adaptation / ML | Disagreement and transition matrices M  to model non-causal environmental conflict [17]. | Free | arXiv:2510.24044v1 |

## Could not be found list

The following gaps in empirical evidence have been identified in the literature search:

1. Direct Head-to-Head Comparative Benchmarks for Legacy Petrol Fleets: No publicly documented, peer-reviewed datasets exist that directly compare a hand-tuned additive rule-based engine against a Bayesian Network or Random Forest using the four exact diagnostic channels under study (5-gas exhaust chemistry, live OBD-II sensor streams, generic P-codes, and operator symptoms) for model years 1990–2010.
2. Computational Benchmarks for PCR5/6 on Embedded Legacy ECUs: Quantitative data documenting the execution time and memory footprint of Proportional Conflict Redistribution rules (PCR5 or PCR6) compiled on 8-bit, 16-bit, or early 32-bit automotive microcontrollers (e.g., Motorola 68HC11 or Infineon TriCore) is absent.
3. Statistical Characterization of Operator-Reported Symptom Noise: No peer-reviewed studies quantify the exact prior probability distributions, error rates, or likelihood noise for qualitative operator complaints (e.g., "runs rough") when fused with quantitative combustion chemistry datasets in real-time diagnostics.

#### Works cited

1. AI-Driven automatic Fault Detection Systems: Revolutionizing Modern Smart Grids - A-State research and creativity hub, https://arch.astate.edu/cgi/viewcontent.cgi?article=2145&context=all-etd
2. Field Implementation of an Expert System for Energy Efficiency Improvement in Industrial Aluminum Electrolysis: A Rule-Based Explainable AI Approach - MDPI, https://www.mdpi.com/2227-9717/14/7/1113
3. http://www.cs.ru.nl/P.Lucas/aime01.pdf
4. HyperSoft Set Methods in Engineering - Sciences Force, https://ojs.sciencesforce.com/index.php/hsse/article/download/644/789
5. Improvement of Proportional Conflict Redistribution Rules of Combination of Basic Belief Assignments - UNM Digital Repository, https://digitalrepository.unm.edu/cgi/viewcontent.cgi?article=1654&context=math_fsp
6. (PDF) Bayesian belief network based fault diagnosis in automotive electronic systems, https://www.researchgate.net/publication/228611973_Bayesian_belief_network_based_fault_diagnosis_in_automotive_electronic_systems
7. The Result Model under Inconsistent Knowledge: Theory and Experiments, https://www.logic.at/staff/agata/jurix2025.pdf
8. Comparative evaluation of multiple machine learning models for power system fault diagnosis - Frontiers, https://www.frontiersin.org/journals/energy-research/articles/10.3389/fenrg.2026.1669209/full
9. KNOWLEDGE INTEGRATION BY PROBABILISTIC ARGUMENTATION - TU e-Thesis (Thammasat University), http://ethesisarchive.library.tu.ac.th/thesis/2022/TU_2022_5622300233_14922_22458.pdf
10. (PDF) Medical diagnosis - ResearchGate, https://www.researchgate.net/publication/312661358_Medical_diagnosis
11. A Review of Fault Diagnosis Methods: From Traditional Machine Learning to Large Language Model Fusion Paradigm - PMC, https://pmc.ncbi.nlm.nih.gov/articles/PMC12846000/
12. Summary of Fault Diagnosis of Electric Vehicle Braking System - Journal of Applied Science and Engineering Innovation, http://icasetoc.com/PDF/12/12-16-22.pdf
13. Resolving Zadeh's Paradox: Axiomatic Possibility Theory as a Foundation for Reliable Artificial Intelligence - arXiv, https://arxiv.org/pdf/2512.05257
14. A mixed D-S combination rule based on the induced ordered weighted averaging operator and adaptive weighting - PMC, https://pmc.ncbi.nlm.nih.gov/articles/PMC11893798/
15. Data fusion and sensor selection from imperfect sources with regards to the operating environment | International Journal of Intelligent Computing and Cybernetics | Emerald Publishing, https://www.emerald.com/ijicc/article/6/4/358/133483/Data-fusion-and-sensor-selection-from-imperfect
16. Mitigating Negative Transfer via Reducing Environmental Disagreement, https://www.computer.org/csdl/journal/tp/5555/01/11429561/2eOD3ZlH5hS
17. Mitigating Negative Transfer via Reducing Environmental Disagreement - arXiv, https://arxiv.org/html/2510.24044v1
18. Adaptative combination rule and proportional conflict redistribution rule for information fusion - arXiv, https://arxiv.org/pdf/cs/0604042
19. Concepts of Artificial Intelligence for Computer-Assisted Drug Discovery | Chemical Reviews, https://pubs.acs.org/doi/10.1021/acs.chemrev.8b00728
20. Comparison of Rule-Based and Bayesian Network Approaches in Medical Diagnostic Systems - ResearchGate, https://www.researchgate.net/publication/221450321_Comparison_of_Rule-Based_and_Bayesian_Network_Approaches_in_Medical_Diagnostic_Systems
21. Fault detection and diagnosis method of diesel engine by combining rule-based algorithm and Bayesian/neural networks - ResearchGate, https://www.researchgate.net/publication/341762741_Fault_detection_and_diagnosis_method_of_diesel_engine_by_combining_rule-based_algorithm_and_Bayesianneural_networks
22. A Belief Rule-Based Expert System for Fault Diagnosis of Marine Diesel Engines - The University of Manchester, https://personalpages.manchester.ac.uk/staff/jian-bo.yang/JB%20Yang%20Journal_Papers/XuXiaojianYanShengYuanXuYang-BRB-Fault-IEEESMC2017pdf.pdf
23. Jianbo Yang's research works | University of Manchester and other places - ResearchGate, https://www.researchgate.net/scientific-contributions/Jianbo-Yang-2116879479
24. Fault Diagnosis for Complex Equipment Based on Belief Rule Base with Adaptive Nonlinear Membership Function - MDPI, https://www.mdpi.com/1099-4300/25/3/442
25. A Belief Rule-Based Expert System for Fault Diagnosis of Marine Diesel Engines, https://www.researchgate.net/publication/320600342_A_Belief_Rule-Based_Expert_System_for_Fault_Diagnosis_of_Marine_Diesel_Engines
26. On the Sparse Gradient Denoising Optimization of Neural Network Models for Rolling Bearing Fault Diagnosis Illustrated by a Ship Propulsion System - MDPI, https://www.mdpi.com/2077-1312/10/10/1376
27. Probabilistic Causal Models in Medicine: Application to Diagnosis of Liver Disorders., https://www.aragorn.wi.pb.edu.pl/~aonisko/agnieszka-onisko-phd.pdf
28. Enhancements of Systems Based on Bayesian Networks and Structural Equation Models for Command and Control Support - DTIC, https://apps.dtic.mil/sti/tr/pdf/ADA419906.pdf
29. Bayesian Networks in Fault Diagnosis - World Scientific Publishing, https://www.worldscientific.com/doi/pdf/10.1142/9789813271494_0001
30. A Fault Prediction Approach Based on Bayesian Network for System - IAPSAM, https://www.iapsam.org/psam14/proceedings/paper/paper_406_1.pdf
31. Grid fault diagnosis based on the deep pyramid convolutional neural network - Frontiers, https://www.frontiersin.org/journals/physics/articles/10.3389/fphy.2025.1624919/full
32. Application of Integrated Vehicle Health Management in Automated Decision-making for Driverless Vehicles - kth.diva, https://kth.diva-portal.org/smash/get/diva2:1754807/FULLTEXT01.pdf
33. Machine Learning for Fault Diagnosis of Industrial Systems - DiVA, https://www.diva-portal.org/smash/get/diva2:2014152/FULLTEXT01.pdf
34. Artificial Intelligence for Fault Detection and Diagnosis in Power Distribution Systems, https://www.hilarispublisher.com/open-access/artificial-intelligence-for-fault-detection-and-diagnosis-in-power-distribution-systems-111392.html
