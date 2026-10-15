# Project Proposal and Methodology Refinement: Telehealth Hypertension Analytics

## Introduction
This capstone project builds an end-to-end predictive analytics platform for remote hypertension monitoring. Using a FastAPI backend, PostgreSQL database, and React user interface, the system collects patient blood pressure readings, trains machine learning models, and generates explainable risk assessments. Based on initial planning reviews and direct faculty feedback, this report refines project scope, evaluates clinical needs and limitations, outlines methodology, and details data security frameworks.

---

## Part 1: Project Proposal Refinement

### Revised Project Scope and Objectives
Initial scoping established a baseline application for batch upload, statistical summaries, and classification. Following faculty feedback and current medical software trends (such as FDA guidance on Software as a Medical Device), I revised the scope to include three technical additions:

1. **Dual-Layer Explainable AI (XAI)**: Professor Pollyn noted that technical SHAP plots can be difficult for clinicians to interpret during busy clinic schedules. To address this, I redesigned the explainability component to generate both a SHAP waterfall plot and an automated plain-English summary (Lundberg & Lee, 2017). Rather than only displaying mathematical scores, the interface outputs clinical narratives (e.g., *"Elevated risk is driven 23% by sodium intake and 18% by BMI"*), giving doctors actionable context for 15-minute consultations.
2. **Quantitative Validation for Synthetic Telemetry**: Following faculty feedback on simulated data risks, I added an empirical validation gate. Because privacy rules prevent using raw clinical records, synthetic blood pressure telemetry will be tested against national baseline distributions from CDC NHANES using Kolmogorov-Smirnov (K-S) tests and Jensen-Shannon Divergence (JSD < 0.05) before model training (Tsao et al., 2023). I also added boundary checks to verify that derived indicators—Mean Arterial Pressure (MAP) and Pulse Pressure (PP)—remain within plausible clinical ranges.
3. **HIPAA Technical Security Alignment**: Following faculty guidance on compliance scope, I reframed our deliverables into an explicit "HIPAA Technical Security Alignment Matrix." Rather than claiming full organizational compliance, this document maps engineering controls—role-based route guards, database encryption, and audit logs—directly to HIPAA Security Rule technical standards (§ 164.308, § 164.310, § 164.312) (Saltz & Krasteva, 2022).

These adjustments improve practical feasibility, clinical trust, and alignment with regulatory standards.

### Needs Analysis, Limitations, and Feasibility
Nearly half of US adults (47%) have hypertension, but fewer than one in four have it under control (Tsao et al., 2023). Standard care relies on infrequent 15-minute visits, creating fragmented records and delayed treatment adjustments (Whelton et al., 2018). While home monitors are common, doctors lack automated tools to interpret months of raw readings. This platform automates ingestion, anomaly detection, and risk scoring to bridge that gap. Feasibility analysis identified practical limitations alongside operational risks:

* **Project Limitations**: Synthetic telemetry cannot capture every individual medication nuance, and home cuffs introduce user measurement errors that the pipeline must treat as observational noise.
* **Data Privacy vs. Realism**: **Risk**: Using actual patient data creates privacy liabilities, while poorly generated synthetic data distorts models. **Strategy**: Use a parameterized generator preserving diurnal rhythms, validated against NHANES benchmarks before training.
* **Clinician Adoption**: **Risk**: Providers reject black-box models lacking transparency. **Strategy**: Display plain-language clinical explanations directly on the React dashboard.
* **Memory Limits**: **Risk**: High-frequency telemetry files can trigger Out-Of-Memory crashes. **Strategy**: Ingest CSV files in streaming chunks (chunksize = 5000) using Pandas.

---

## Part 2: Methodology Outline

### High-Level Methodological Approach
The machine learning pipeline combines supervised classification algorithms with unsupervised anomaly detection to give clinicians a clear picture of patient health.

**Workflow Pipeline:**  
Step 1: Ingestion (FastAPI) ➔ Step 2: Batch Preprocessing & Scaling ➔ Step 3: Classification & Anomaly Detection ➔ Step 4: Dual-Layer SHAP Explanations ➔ Step 5: React Dashboard

1. **Supervised Classification & Validation**: XGBoost and Random Forest classifiers predict patient hypertension stages based on American Heart Association categories (Normal, Elevated, Stage 1, Stage 2, Crisis). The dataset uses an 80/20 train-test split evaluated with 5-fold cross-validation. Model tuning prioritizes recall and sensitivity (targeting at least 0.90 for high-risk stages) to avoid dangerous false negatives.
2. **Unsupervised Anomaly Detection**: An Isolation Forest algorithm processes longitudinal readings to flag sudden blood pressure spikes or deviations from a patient's personal circadian baseline.
3. **Data Sources & Preparation**: The project combines CDC NHANES demographic baselines with simulated continuous telemetry. Missing values are handled via median imputation, and derived clinical features are calculated directly from raw readings: Mean Arterial Pressure (MAP = DBP + 1/3[SBP - DBP]) and Pulse Pressure (PP = SBP - DBP).

### Data Preprocessing & System Scaling
To ensure the platform runs reliably across varying data volumes and hardware limits, I built in specific scaling mechanisms:

* **Feature Scaling**: Numerical features undergo MinMax normalization ([0, 1] range) and Z-score standardization so high blood pressure values do not overwhelm lower-magnitude variables.
* **Streaming Ingestion**: Telemetry files are read in chunks of 5,000 rows, maintaining a minimal RAM footprint.
* **Infrastructure Scaling**: Asynchronous FastAPI endpoints running on Uvicorn provide stateless routing that scales horizontally on Render as user traffic grows.

### Project Credibility, Ethics, and Intellectual Property
To maintain credibility and ethical standards, the project follows strict licensing, transparency, and data protection practices:

* **Intellectual Property**: Third-party libraries (FastAPI, Scikit-Learn, React, XGBoost) use permissive MIT or Apache 2.0 licenses, and CDC public domain data is cited accordingly.
* **Fairness Checks**: To prevent algorithmic bias, model performance is audited across demographic sub-groups (age, sex, ethnicity) using demographic parity and equalized odds metrics.
* **HIPAA Technical Safeguards**:
  * *Access Control (§ 164.312(a))*: Enforced through OAuth2 JWT authentication and role-based route dependencies (get_current_user).
  * *Encryption (§ 164.312(c/e))*: TLS 1.3 protects data in transit, while PostgreSQL column-level symmetric encryption (pgp_sym_encrypt) secures patient identifiers at rest.
  * *Audit Logs (§ 164.312(b))*: Structured logs record the user ID, timestamp, and action for every API transaction.
* **Cloud Security**: Render and Vercel hostings leverage infrastructure with documented SOC 2 Type II and HIPAA physical security attestations.

---

## References

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. Advances in Neural Information Processing Systems, 30, 4765–4774.

Saltz, J., & Krasteva, I. (2022). Current approaches for executing big data science projects: A systematic literature review. PeerJ Computer Science, 8, e942. https://doi.org/10.7717/peerj-cs.942

Tsao, C. W., Aday, A. W., Almarzooq, Z. I., Anderson, C. A., Arora, P., Avery, C. L., ... & Martin, S. S. (2023). Heart disease and stroke statistics—2023 update: A report from the American Heart Association. Circulation, 147(8), e93–e621. https://doi.org/10.1161/CIR.0000000000001123

Whelton, P. K., Carey, R. M., Aronow, W. S., Casey, D. E., Collins, K. J., Himmelfarb, C. D., ... & Wright, J. T. (2018). 2017 ACC/AHA/AAPA/ABC/ACPM/AGS/APhA/ASH/ASPC/NMA/PCNA guideline for the prevention, detection, evaluation, and management of high blood pressure in adults. Journal of the American College of Cardiology, 71(19), e127–e248. https://doi.org/10.1016/j.jacc.2017.11.006