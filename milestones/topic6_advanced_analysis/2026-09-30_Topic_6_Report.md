^^ 

^^ 

^^**Advanced Analysis and Model Refinement Report: Telehealth Hypertension Analytics**

^^ 

^^Raja Chakraborty

^^College of Science, Engineering, and Technology, Grand Canyon University

^^DSC-590: Data Science Capstone

^^Instructor: Jonathan Pollyn

^^September 30, 2026

<pagebreak>

# Advanced Analysis and Model Refinement Report: Telehealth Hypertension Analytics

## 1. Introduction and Project Background

Cardiovascular disease remains a leading cause of death worldwide, and high blood pressure is its most common modifiable risk factor. Routine care still depends heavily on occasional office readings, which miss two clinically important patterns. In white-coat hypertension, clinic anxiety raises a reading that is normal at home. In masked hypertension, blood pressure is high outside the clinic, often at night, but normal during the daytime visit. Ambulatory blood pressure monitoring (ABPM) addresses both by recording readings around the clock (Whelton et al., 2018). However, a 24-hour record contains roughly 48 readings per patient, and reviewing them adds charting work for busy clinicians.

This capstone built a telehealth analytics platform that ingests 24-hour ABPM records, classifies each patient into one of the four 2017 American College of Cardiology/American Heart Association (ACC/AHA) stages (Normal, Elevated, Stage 1, Stage 2), and explains each prediction with TreeSHAP attributions (Lundberg et al., 2020). This report documents the advanced analysis and refinement phase. All results come from the companion Jupyter notebook (*Topic_6_Advanced_Analysis_and_Model_Refinement.ipynb*). It runs end to end with a fixed random seed, so every number and figure below can be reproduced.

**Changes since the previous phase.** For this phase the pipeline was rebuilt with a stricter evaluation protocol, and the results replace those reported earlier. Three changes matter:

1. Each synthetic patient now has 48 half-hourly readings with measurement noise, 3% cuff and motion artifacts, 8% missing readings, and day-to-day variability, instead of one clean summary row. This makes the task harder and more realistic, and it makes circadian analysis possible.
2. The previous notebook fitted its probability calibrator on the test set and then scored the calibrated model on that same set. This leaks information and inflates results. Every tuning and calibration step now uses cross-validation on the training data only, and the 30% holdout is used once, for final scoring.
3. Latency is now measured on this machine rather than estimated.

As a result, overall accuracy is lower than the 94.2% reported in the previous phase, but it is reproducible and free of leakage.

## 2. Detailed Model Evaluation

### 2.1 Evaluation design and metrics

The cohort has 1,800 synthetic patients, 450 per stage. A stratified 30% holdout of 540 patients (135 per stage) was set aside before any modeling. Five kinds of metrics are reported, because accuracy alone hides the errors that matter clinically:

* **Class-level metrics:** precision, recall (sensitivity), F1-score, and specificity, plus a confusion matrix.
* **Ranking metrics:** one-vs-rest ROC-AUC and precision-recall AUC (PR-AUC).
* **Probability quality:** the multi-class Brier score and the top-label expected calibration error (ECE). Calibration matters because clinicians act on the stated confidence, not only on the predicted label (Van Calster et al., 2019).
* **Uncertainty:** 95% bootstrap confidence intervals from 1,000 resamples of the holdout.
* **Efficiency:** median single-patient inference latency.

**Table 1**

*Holdout Performance of the Refined Model (Feature-Engineered, Tuned XGBoost), n = 540*

| Stage (2017 ACC/AHA) | Precision | Recall | F1-Score | Specificity | PR-AUC | ROC-AUC |
|---|---|---|---|---|---|---|
| Normal | 0.896 | 0.896 | 0.896 | 0.965 | 0.960 | 0.986 |
| Elevated | 0.819 | 0.837 | 0.828 | 0.938 | 0.884 | 0.963 |
| Stage 1 | 0.910 | 0.904 | 0.907 | 0.970 | 0.960 | 0.988 |
| Stage 2 | 0.985 | 0.970 | 0.978 | 0.995 | 0.995 | 0.998 |
| Macro average | 0.903 | 0.902 | 0.902 | 0.967 | 0.950 | 0.984 |

*Note.* Overall accuracy = 90.2% (95% bootstrap CI [87.4%, 92.6%]); Brier score = 0.148; ECE = 0.014. PR-AUC = precision-recall area under the curve; ROC-AUC = one-vs-rest area under the receiver operating characteristic curve.

**Figure 1**

*Holdout Confusion Matrices Before (Default XGBoost) and After Refinement*

![Confusion matrices](topic6_fig1_confusion.png)

*Note.* Counts with row percentages. Darker cells hold a larger share of each true stage.

### 2.2 Strengths

* **Stage 2 is the strongest class.** Recall is 0.970: 131 of 135 Stage 2 patients were identified (95% CI [0.938, 0.993]). Precision is 0.985, specificity is 0.995, and PR-AUC is 0.995. Only 2 of 405 patients outside Stage 2 were labeled Stage 2. This is the class where a miss is most dangerous, and also where false alarms most quickly cause alert fatigue.
* **Errors stay one stage away.** Figure 1 shows that every error is between adjacent stages, and no patient is off by two or more stages. The four missed Stage 2 patients were all labeled Stage 1, so they were still flagged as hypertensive and routed for follow-up.
* **Discrimination is high across all stages.** ROC-AUC is above 0.96 for every stage (macro 0.984). The ROC curves in Figure 3 are computed directly from holdout predictions and sit well above the chance diagonal.
* **Probabilities are well calibrated.** ECE is 0.014, so the stated confidence differs from observed accuracy by about 1.4 percentage points on average.

### 2.3 Weaknesses

* **Elevated is the weakest stage** (F1 = 0.828, PR-AUC = 0.884). It is bounded on both sides, so it can be confused with Normal (14 Elevated patients were predicted Normal and 14 Normal patients predicted Elevated) or with Stage 1 (8 and 11). Of the 53 holdout errors, 28 are Normal/Elevated confusions and 19 are Elevated/Stage 1 confusions.
* **Errors are concentrated near the cutoffs.** Section 4.4 shows that patients whose daytime systolic mean lies within 5 mmHg of the 120 or 130 mmHg cutoffs are misclassified 16.2% of the time, against 5.1% elsewhere. With readings that vary by several mmHg from day to day, a single monitoring day cannot reliably place these patients. This mirrors genuine clinical uncertainty at the cutoffs rather than a defect specific to this model.
* **Small gains over simple models.** The refined model's accuracy advantage over logistic regression (+1.9 points, 95% CI [−0.2, +3.7]) and over default XGBoost (+1.3 points, CI [−0.6, +3.1]) is not statistically distinguishable from zero. The refinement mainly improved probability quality, not accuracy (Section 3).

### 2.4 Comparison with benchmarks and industry standards

The refined model was compared against two rule-based clinical benchmarks and two machine learning baselines, all scored on the same holdout (Table 2).

**Table 2**

*Benchmark Comparison on the Holdout Set (n = 540)*

| Approach | Accuracy | Macro F1 | Stage 2 Recall | Stage 2 Precision | Macro ROC-AUC | Brier | ECE | Latency (ms) |
|---|---|---|---|---|---|---|---|---|
| Office AHA rule (one clinic reading) | 54.3% | 0.521 | 0.956 | 0.573 | — | — | — | < 1 |
| ABPM guideline rule (daytime mean) | 61.5% | 0.588 | 0.993 | 0.554 | — | — | — | < 1 |
| Logistic regression | 88.3% | 0.884 | 0.948 | 0.970 | 0.980 | 0.182 | 0.056 | 2.3 |
| Default XGBoost | 88.9% | 0.889 | 0.970 | 0.970 | 0.980 | 0.181 | 0.076 | 2.9 |
| **Refined XGBoost** | **90.2%** | **0.902** | **0.970** | **0.985** | **0.984** | **0.148** | **0.014** | **3.5 (+15.7 SHAP)** |

*Note.* The rules assign stages from fixed thresholds, so they produce no probabilities and have no ROC-AUC, Brier, or ECE. Latency is the median time to score one patient on a laptop CPU. The SHAP figure is the extra time to compute one patient's TreeSHAP explanation. Latencies vary by about ±0.5 ms between runs.

**Clinical rule benchmarks.** The office rule applies the 2017 ACC/AHA office thresholds to a single simulated clinic reading. The ABPM rule applies the guideline's matching daytime ABPM thresholds (120/80, 130/80, and 135/85 mmHg; Whelton et al., 2018, Table 11). Both rules catch Stage 2 patients (recall 0.956 and 0.993) but heavily over-call Stage 2: only 57% and 55% of their Stage 2 labels are correct. The ABPM rule also places 98 of 135 Stage 1 patients in Stage 2, because its 135 mmHg daytime cutoff falls inside the Stage 1 distribution. Compared with these rules, the refined model gains 24–33 accuracy points (bootstrap CI for the difference versus the ABPM rule [+24.3, +32.8]) and nearly doubles Stage 2 precision. In practice, that means far fewer unnecessary escalations. Part of the rules' poor showing comes from how the synthetic labels were defined (Section 5.1), so the size of this gap would need to be confirmed on real data.

**Machine learning baselines.** Logistic regression is the strongest baseline: its accuracy and ROC-AUC are within noise of the refined model. However, it misses more Stage 2 patients (recall 0.948 vs 0.970) and its probabilities are much less reliable (ECE 0.056 vs 0.014). Since the platform shows confidence scores to clinicians, the refined model's main benefit is its probability quality.

**Industry standards.** Against conventional thresholds, macro ROC-AUC of 0.984 exceeds the 0.90 level usually described as outstanding discrimination (Hosmer et al., 2013). Single-patient scoring plus explanation takes about 20 ms, far inside the project's 200 ms response target. On the other hand, the model **does not yet meet** the standards that govern clinical deployment:

* The FDA's good machine learning practice principles call for testing on independent data that represents the intended patient population (U.S. Food and Drug Administration et al., 2021). This model has only been validated internally on synthetic data.
* The TRIPOD reporting guideline expects external validation before a prediction model is used clinically (Collins et al., 2015).

These are the main deployment gaps (Section 5).

## 3. Iterative Refinement Process

Starting from default XGBoost (Chen & Guestrin, 2016) on seven raw summary features, three refinements were tried one at a time. Each was kept only if it improved held-out performance. Table 3 and Figures 2 through 5 document each step.

**Table 3**

*Holdout Metrics After Each Refinement Step*

| Step | Accuracy | Macro F1 | Stage 2 Recall | Macro ROC-AUC | Brier | ECE | Latency (ms) | Decision |
|---|---|---|---|---|---|---|---|---|
| Default XGBoost (raw features) | 88.9% | 0.889 | 0.970 | 0.980 | 0.181 | 0.076 | 2.9 | Baseline |
| + Feature engineering | 88.9% | 0.889 | 0.970 | 0.979 | 0.176 | 0.065 | 3.9 | Kept |
| + Hyperparameter search | 90.2% | 0.902 | 0.970 | 0.984 | 0.148 | 0.014 | 3.5 | Kept |
| + Isotonic calibration | 90.0% | 0.900 | 0.970 | 0.982 | 0.152 | 0.024 | 22.7 | Rejected |

**Figure 2**

*Holdout Metric Progression Across Refinement Steps*

![Refinement progression](topic6_fig2_progression.png)

### 3.1 Refinement 1: Domain-specific feature engineering

Four physiologically grounded features were added to the seven raw features, keeping default hyperparameters so that the change was isolated:

* **Mean arterial pressure (MAP), day and night:** DBP + (SBP − DBP)/3, the average perfusion pressure over a cardiac cycle.
* **Pulse pressure:** SBP − DBP, a marker of arterial stiffness.
* **Nocturnal dipping ratio:** (mean daytime SBP − mean nighttime SBP) / mean daytime SBP.

*Impact:* Accuracy did not change (88.9%), but probability quality improved (Brier 0.181 to 0.176, ECE 0.076 to 0.065). Section 4.3 shows that the model relies heavily on the new features: nighttime MAP has the largest SHAP attribution. They did not raise accuracy because tree ensembles can already approximate these combinations from the raw inputs. What the features do is make the model's reasoning easier to explain, since clinicians already think in terms of MAP and dipping. The step was kept for that reason and for the small calibration gain.

### 3.2 Refinement 2: Cross-validated hyperparameter search

A randomized search over 40 configurations (Bergstra & Bengio, 2012) was run with 5-fold stratified cross-validation on the training set. It covered tree depth, learning rate, number of trees, row and column subsampling, minimum child weight, and L2 regularization. Configurations were scored on multi-class log loss, a proper scoring rule, so the search rewarded honest probabilities as well as correct labels. The best configuration used shallow trees (max_depth = 3), a slow learning rate (0.025), and 319 trees, with row subsampling of 0.71, min_child_weight = 2, and reg_lambda = 0.13.

*Impact:* This was the most effective refinement:

* Holdout accuracy rose to 90.2% and macro F1 to 0.902.
* Brier score fell 16%, from 0.176 to 0.148.
* ECE fell almost fivefold, from 0.065 to 0.014.
* Cross-validated log loss on the training data fell 32%, from 0.445 to 0.302, and its fold-to-fold standard deviation narrowed from 0.057 to 0.038 (Figure 5). So the improvement holds across data splits, not just on one holdout.

The default configuration's deeper trees (depth 6) had overfit the noisy readings, which gave overconfident probabilities. Figure 4 shows this clearly: the default model's predictions made with 80–90% confidence were correct only about 65% of the time.

**Figure 3**

*One-vs-Rest ROC Curves Before and After Refinement (Holdout Set)*

![ROC curves](topic6_fig3_roc.png)

*Note.* Inset panels zoom to false-positive rates of 0–0.20, where the clinically relevant differences lie. The largest gain is for the Elevated stage (AUC 0.956 to 0.963).

**Figure 4**

*Reliability Diagram of Top-Label Confidence Across Refinement Steps*

![Reliability diagram](topic6_fig4_calibration.png)

*Note.* Bins with fewer than five patients are omitted. The lower panel shows how many patients fall at each confidence level.

**Figure 5**

*Cross-Validated Log Loss Before and After Hyperparameter Search (5 Folds × 3 Repeats, Training Set)*

![CV stability](topic6_fig5_cv_stability.png)

### 3.3 Refinement 3: Isotonic probability calibration (tested and rejected)

Gradient-boosted trees often produce distorted probabilities that post-hoc calibration can correct (Niculescu-Mizil & Caruana, 2005). Isotonic calibration was applied with `CalibratedClassifierCV` using 5-fold internal cross-validation on the training set, so each calibrator was fitted on data its model had not seen.

*Impact:* Calibration made the probabilities slightly *worse* (Brier 0.148 to 0.152, ECE 0.014 to 0.024) and lowered accuracy by 0.2 points. Because it requires five model copies, it also multiplied inference time by about six (3.5 to 22.7 ms). The tuned model was already well calibrated because its search optimized log loss, so isotonic regression mainly added variance from fitting a step function to about 250 patients per fold. **The step was therefore rejected.** Testing the refinement and rejecting it is a useful result in itself: calibration should be applied when the data shows it is needed, not by default.

### 3.4 Summary of key findings

1. The refined model is the feature-engineered, tuned XGBoost: 90.2% accuracy, Stage 2 recall 0.970 with 0.985 precision, macro ROC-AUC 0.984, ECE 0.014, and about 20 ms for prediction plus explanation.
2. The largest gain was in **probability quality**. Brier score fell 18% and ECE fell 81% from the default model. The gain in accuracy was small and within sampling error.
3. Optimizing a proper scoring rule during tuning made a separate calibration step unnecessary. This kept the system simpler and about six times faster.

## 4. Exploratory Data and Trend Analysis

Earlier phases looked only at per-patient summary statistics. The half-hourly records allowed four further analyses.

### 4.1 Circadian profiles and the morning surge

**Figure 6**

*Mean Half-Hourly Systolic Blood Pressure by Stage, With 95% Confidence Bands (n = 1,800)*

![Circadian profiles](topic6_fig6_circadian.png)

Figure 6 shows a clear rise in systolic pressure between 06:00 and 10:00 in every stage, followed by a daytime plateau and a fall after bedtime. How deep the night dip is varies sharply by stage. The median dipping ratio falls from 15.0% in Normal patients to 3.2% in Stage 2, and the share of non-dippers (dip below 10%) rises from 5% to 33%, 83%, and 99% across the four stages (Figure 7, right).

**Figure 7**

*Morning Surge and Nocturnal Dipping by Stage*

![Surge and dipping](topic6_fig7_surge_dip.png)

The analysis also exposed a measurement problem that the earlier phase missed. The conventional pre-waking surge (mean SBP in the 2 hours after waking minus the 2 hours before; Kario et al., 2003) *decreases* with stage, from a median of 18.5 mmHg in Normal patients to 14.6 mmHg in Stage 2 (Figure 7, left). The reason is that it measures the whole rise from the night trough, and patients who dip deeply at night have more to rise. Measured this way, the surge is largely a restatement of dipping. A dip-adjusted measure, **surge excess** (the rise above the patient's own daytime mean), shows the opposite pattern: medians rise from 4.0 mmHg in Normal patients to 5.5, 7.9, and 11.4 mmHg across the higher stages (Figure 7, center). The surge excess captures the extra morning rise above the day's level, which is the part of the surge Kario et al. (2003) linked to stroke risk and which coincides with the morning peak in heart attacks (Muller et al., 1985).

An important caveat: because the data are synthetic, the stage-dependent surge and dipping were *built into the generator*, based on the published literature. Recovering them shows that the feature pipeline measures these patterns correctly. It does not amount to a clinical discovery. The methodological point, that a surge definition must be adjusted for dipping, does carry over to real data.

### 4.2 Office spot-checks versus 24-hour monitoring

**Figure 8**

*Single Office Systolic Reading Versus Daytime ABPM Mean, by Hypertension Pattern*

![Office versus ABPM](topic6_fig8_office_vs_abpm.png)

Using the guideline correspondence of office 130/80 to daytime ABPM 130/80, the simulated cohort contains 265 white-coat patients (14.7%) and 84 masked patients (4.7%) (Figure 8). A single office reading disagrees with the patient's true hypertensive status for 25.5% of the cohort. As a result, the office rule misclassified 247 of 540 holdout patients (Table 2). This bears directly on the project's central goal: roughly one patient in four would be misjudged by a spot-check alone, and 24-hour monitoring with automated interpretation corrects most of these errors.

### 4.3 What drives the model

**Figure 9**

*Global Feature Attribution: Mean Absolute SHAP Value per Feature, Refined Model, Holdout Set*

![SHAP importance](topic6_fig9_shap.png)

Nighttime features dominate (Figure 9). Nighttime MAP (mean |SHAP| = 1.18), nighttime SBP (0.77), and nighttime DBP (0.62) together far outweigh the daytime systolic mean (0.08). This agrees with outcome studies in which nighttime pressure predicts cardiovascular events better than daytime pressure (Hansen et al., 2011). Part of the effect again comes from the generator, where dipping shrinks with stage and so pulls the nighttime values further apart. Two design implications follow:

* The dashboard should show nighttime values and dipping status prominently, not just the daytime average.
* A patient whose nighttime readings are missing or full of artifacts should get a lower-confidence result, not a normal-looking one.

### 4.4 Where errors occur, and a follow-up feature experiment

**Figure 10**

*Holdout Error Rate by Daytime Systolic Level (Refined Model)*

![Error rate by systolic level](topic6_fig10_errors.png)

Figure 10 shows that 70% of the refined model's errors occur within 5 mmHg of the 120 or 130 mmHg cutoffs. In that zone the error rate is 16.2%, against 5.1% elsewhere. Above 150 mmHg there are almost no errors. A second ABPM day or home readings would therefore improve accuracy most for patients close to a cutoff, and the platform should label these cases "near threshold: confirm" rather than present a confident label.

Following the surge finding, the three surge features were added to the refined model with its hyperparameters unchanged. The holdout gain was minimal (accuracy 90.2% to 90.6%, Brier 0.148 to 0.148), and cross-validated log loss was within noise (0.302 to 0.299, SD 0.038). The surge features are not yet adopted. Most of the signal they carry is already captured by the dipping and nighttime features. The surge features are more likely to matter for **outcome prediction** (stroke or cardiac events), which is the project's next objective, than for staging.

### 4.5 Relevance to project objectives

The project aims to move hypertension care from reacting to emergencies toward catching problems early. The analyses above support that aim in four ways:

* They quantify how much spot-check care misses (25.5% disagreement).
* They show that nighttime readings carry the most diagnostic weight, which is information an office visit cannot provide.
* They identify the patients near a cutoff for whom one monitoring day is not enough.
* They establish a dip-adjusted surge measure ready for the outcome-prediction phase.

The surge findings also suggest a role in decisions about medication timing. However, the large TIME randomized trial found no difference in cardiovascular outcomes between evening and morning dosing of antihypertensives (Mackenzie et al., 2022). Any timing suggestion should therefore be framed as information for the clinician, not as a recommendation to change dosing time.

## 5. Critical Assessment of Model Limitations

### 5.1 Current limitations

* **Synthetic data and how labels are defined.** All results come from simulated patients, and the stage labels are the categories the data was generated from. This has three consequences. First, realistic sensor problems such as loose cuffs, arrhythmias, and motion during exercise are only roughly approximated. Second, any pattern the generator encodes, such as surge rising with stage, can be "discovered" but not validated. Third, the rule benchmarks are partly disadvantaged because the stage distributions were drawn on an office-reading scale while the ABPM rule uses ABPM thresholds. Real performance could be higher or lower than reported.
* **Biases cannot be assessed.** Accuracy is similar for women and men (90.7% ± 3.4 vs 89.7% ± 3.7). It is lower for patients under 45 (86.0% ± 7.0, n = 93) than for those 65 and over (94.4% ± 4.1, n = 124), but the generator has no age effect on blood pressure, so this gap reflects sampling variation in small groups. More fundamentally, synthetic data contains only the biases put into it. Real-world bias, for example from cuff-size mismatch in patients with obesity, measurement differences across racial groups, or under-represented populations, can only be measured on real data. Obermeyer et al. (2019) showed how a clinical algorithm can carry racial bias that is invisible until it is audited against real outcomes.
* **Narrow patient coverage.** The cohort reflects adult essential hypertension. Chronic kidney disease, secondary hypertension, pregnancy-related hypertension, and pediatric patients behave differently and are not represented.
* **A single monitoring day.** Each patient contributes one 24-hour record, yet patients near a cutoff need repeat measurement (Section 4.4).
* **Explanation cost.** Scoring takes 3.5 ms, but computing TreeSHAP explanations adds 15.7 ms per patient. That is acceptable for one patient but grows linearly when large batches are scored at once.

### 5.2 Potential enhancements

1. **Validate on real data.** Retrospective validation on de-identified ABPM data (for example, through a data-use agreement with a hospital) would allow a check on whether calibration holds in a new population (Van Calster et al., 2019), audited subgroup performance, and reporting under TRIPOD (Collins et al., 2015).
2. **Treat near-threshold cases differently.** Report predictions within about 5 mmHg of a cutoff as "confirm with repeat monitoring," and combine several days of home readings when they are available.
3. **Check signal quality before scoring.** Detect artifacts and require minimum nighttime coverage before classifying. When nighttime data is poor, widen the stated uncertainty.
4. **Edge and batch efficiency.** Compile the tree ensemble (for example with Treelite or ONNX Runtime) for on-device scoring, and compute SHAP explanations only on request or in batches.
5. **Clinician feedback loop.** Send cases where the clinician overrides the model to review, and use them as new labels for scheduled retraining. Retraining should be gated on calibration checks, consistent with the iterative, process-driven approach used throughout the project (Saltz & Krasteva, 2022).

### 5.3 Applicability across scenarios and industries

* **Remote chronic-disease monitoring (primary setting).**
  - *Benefits:* Rural networks without cardiologists gain triage with high Stage 2 precision (few false escalations) and plain-language SHAP explanations that nurses can relay to patients.
  - *Drawbacks:* Intermittent connectivity calls for an offline mode, and regulators will require real-world validation before clinical use.
* **Consumer wearables.**
  - *Benefits:* Cuffless wrist estimates could screen for non-dipping and nighttime hypertension at population scale.
  - *Drawbacks:* Cuffless readings are noisier than the cuff data simulated here. Without recalibration, the model's well-calibrated probabilities would not carry over, and false alarms could drive unnecessary clinic visits.
* **Occupational health in safety-critical jobs (pilots, rail operators, commercial drivers).**
  - *Benefits:* Periodic 24-hour monitoring could catch the masked hypertension that fitness-for-duty office checks miss (Section 4.2).
  - *Drawbacks:* Using the model to make employment decisions raises fairness, privacy, and due-process concerns. Its role should be limited to referral, not disqualification.
* **Clinical trials and pharmaceutical research.**
  - *Benefits:* Automated ABPM interpretation could standardize endpoint assessment and flag non-dippers for enrichment.
  - *Drawbacks:* Trial use requires strict documentation of algorithm versions and locked models.

## 6. Conclusion

This phase rebuilt the evaluation on a more realistic, leakage-free protocol and refined the model through documented steps. Feature engineering and hyperparameter search, tuned on a proper scoring rule, produced a model with 90.2% accuracy, Stage 2 recall of 0.970 at 0.985 precision, macro ROC-AUC of 0.984, and well-calibrated probabilities (ECE 0.014), returned with explanations in about 20 ms. Isotonic calibration was tested and rejected because it added cost without benefit. The exploratory work showed four things:

* A single office reading misjudges about one patient in four.
* Nighttime pressure carries most of the diagnostic signal.
* Errors concentrate near the cutoffs.
* Morning-surge measures must be adjusted for dipping.

The model is ready for **prospective validation on real ABPM data**, not yet for clinical use. Real-data validation, a subgroup bias audit, and repeat monitoring for near-threshold patients are the necessary next steps.

<pagebreak>

## References

Bergstra, J., & Bengio, Y. (2012). Random search for hyper-parameter optimization. *Journal of Machine Learning Research, 13*, 281–305. https://www.jmlr.org/papers/v13/bergstra12a.html

Chen, T., & Guestrin, C. (2016). XGBoost: A scalable tree boosting system. In *Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining* (pp. 785–794). Association for Computing Machinery. https://doi.org/10.1145/2939672.2939785

Collins, G. S., Reitsma, J. B., Altman, D. G., & Moons, K. G. M. (2015). Transparent reporting of a multivariable prediction model for individual prognosis or diagnosis (TRIPOD): The TRIPOD statement. *Annals of Internal Medicine, 162*(1), 55–63. https://doi.org/10.7326/M14-0697

Hansen, T. W., Li, Y., Boggia, J., Thijs, L., Richart, T., & Staessen, J. A. (2011). Predictive role of the nighttime blood pressure. *Hypertension, 57*(1), 3–10. https://doi.org/10.1161/HYPERTENSIONAHA.109.133900

Hosmer, D. W., Jr., Lemeshow, S., & Sturdivant, R. X. (2013). *Applied logistic regression* (3rd ed.). Wiley. https://doi.org/10.1002/9781118548387

Kario, K., Pickering, T. G., Umeda, Y., Hoshide, S., Hoshide, Y., Morinari, M., Murata, M., Kuroda, T., Schwartz, J. E., & Shimada, K. (2003). Morning surge in blood pressure as a predictor of silent and clinical cerebrovascular disease in elderly hypertensives. *Circulation, 107*(10), 1401–1406. https://doi.org/10.1161/01.CIR.0000056521.67546.AA

Lundberg, S. M., Erion, G., Chen, H., DeGrave, A., Prutkin, J. M., Nair, B., Katz, R., Himmelfarb, J., Bansal, N., & Lee, S.-I. (2020). From local explanations to global understanding with explainable AI for trees. *Nature Machine Intelligence, 2*(1), 56–67. https://doi.org/10.1038/s42256-019-0138-9

Mackenzie, I. S., Rogers, A., Poulter, N. R., Williams, B., Brown, M. J., Webb, D. J., Ford, I., Rorie, D. A., Guthrie, G., Grieve, J. W. K., Pigazzani, F., Rothwell, P. M., Young, R., McConnachie, A., Struthers, A. D., Lang, C. C., & MacDonald, T. M. (2022). Cardiovascular outcomes in adults with hypertension with evening versus morning dosing of usual antihypertensives in the UK (TIME study): A prospective, randomised, open-label, blinded-endpoint clinical trial. *The Lancet, 400*(10361), 1417–1425. https://doi.org/10.1016/S0140-6736(22)01786-X

Muller, J. E., Stone, P. H., Turi, Z. G., Rutherford, J. D., Czeisler, C. A., Parker, C., Poole, W. K., Passamani, E., Roberts, R., Robertson, T., Sobel, B. E., Willerson, J. T., Braunwald, E., & the MILIS Study Group. (1985). Circadian variation in the frequency of onset of acute myocardial infarction. *New England Journal of Medicine, 313*(21), 1315–1322. https://doi.org/10.1056/NEJM198511213132103

Niculescu-Mizil, A., & Caruana, R. (2005). Predicting good probabilities with supervised learning. In *Proceedings of the 22nd International Conference on Machine Learning* (pp. 625–632). Association for Computing Machinery. https://doi.org/10.1145/1102351.1102430

Obermeyer, Z., Powers, B., Vogeli, C., & Mullainathan, S. (2019). Dissecting racial bias in an algorithm used to manage the health of populations. *Science, 366*(6464), 447–453. https://doi.org/10.1126/science.aax2342

Saltz, J. S., & Krasteva, I. (2022). Current approaches for executing big data science projects: A systematic literature review. *PeerJ Computer Science, 8*, Article e862. https://doi.org/10.7717/peerj-cs.862

U.S. Food and Drug Administration, Health Canada, & Medicines and Healthcare products Regulatory Agency. (2021). *Good machine learning practice for medical device development: Guiding principles*. https://www.fda.gov/medical-devices/software-medical-device-samd/good-machine-learning-practice-medical-device-development-guiding-principles

Van Calster, B., McLernon, D. J., van Smeden, M., Wynants, L., & Steyerberg, E. W. (2019). Calibration: The Achilles heel of predictive analytics. *BMC Medicine, 17*, Article 230. https://doi.org/10.1186/s12916-019-1466-7

Whelton, P. K., Carey, R. M., Aronow, W. S., Casey, D. E., Jr., Collins, K. J., Dennison Himmelfarb, C., DePalma, S. M., Gidding, S., Jamerson, K. A., Jones, D. W., MacLaughlin, E. J., Muntner, P., Ovbiagele, B., Smith, S. C., Jr., Spencer, C. C., Stafford, R. S., Taler, S. J., Thomas, R. J., Williams, K. A., Sr., . . . Wright, J. T., Jr. (2018). 2017 ACC/AHA/AAPA/ABC/ACPM/AGS/APhA/ASH/ASPC/NMA/PCNA guideline for the prevention, detection, evaluation, and management of high blood pressure in adults. *Journal of the American College of Cardiology, 71*(19), e127–e248. https://doi.org/10.1016/j.jacc.2017.11.006
