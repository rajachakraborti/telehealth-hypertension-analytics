# Planning Phase: Telehealth Hypertension Predictive Analytics System

## Introduction

This document establishes the planning phase for the Telehealth Hypertension Predictive Analytics System, an end-to-end web application that leverages machine learning to forecast chronic hypertension risk and detect anomalous blood pressure trends. Built on a FastAPI backend, React frontend, and PostgreSQL database, the system shifts clinical workflows from reactive monitoring to proactive, data-driven decision support. The following sections outline the innovative features, project objectives grounded in a Christian worldview, a needs analysis of the clinical landscape, a detailed project timeline, the resources required, and strategies for overcoming anticipated challenges.

---

## Articulate Innovative Ideas

Three innovative features distinguish this project and align it with current data science trends:

**Explainable AI (XAI) for Clinical Triage.** Machine learning models in healthcare are frequently dismissed as opaque "black boxes," eroding clinician trust and slowing adoption (Lundberg & Lee, 2017). This system integrates SHAP (SHapley Additive exPlanations) to produce patient-specific feature attribution visualizations directly on the clinician dashboard. This aligns with the FDA's emerging framework for Software as a Medical Device (SaMD), which requires algorithmic transparency and clinical validation before deployment in care settings (Saltz & Krasteva, 2022).

**Longitudinal Anomaly Detection on Home Telemetry.** Rather than relying on isolated, episodic clinic readings, the system implements unsupervised anomaly detection algorithms (Isolation Forests) to monitor continuous patient-submitted blood pressure data over time. This directly leverages the Internet of Medical Things (IoMT) trend, where wearable devices and home monitors generate high-frequency physiological data streams that require automated intelligent analysis (Tsao et al., 2023).

**Algorithmic Fairness Auditing.** Aligning with the EU AI Act's requirements for high-risk AI systems, the platform incorporates a fairness auditing engine that monitors demographic parity metrics across age, sex, and ethnicity, alerting analysts to model bias and ensuring equitable risk assessments for all patient populations (Saltz & Krasteva, 2022).

---

## Establish Objectives and Goals

The primary objective is to build an equitable, transparent, and secure predictive analytics tool that enhances clinical decision-making. The goals reflect the Christian worldview principles of stewardship, justice, and service:

**Stewardship of Healthcare Resources.** Scripture teaches that "each of you should use whatever gift you have received to serve others, as faithful stewards of God's grace" (1 Peter 4:10, NIV). By identifying high-risk patients before adverse events occur, the system enables clinics to allocate limited resources wisely, reducing preventable hospital readmissions and exercising responsible stewardship of medical personnel and community healthcare budgets.

**Justice Through Algorithmic Equity.** The fairness auditing framework ensures that predictive risk metrics do not systematically disadvantage underserved demographics. This reflects the biblical call to "learn to do right; seek justice. Defend the oppressed" (Isaiah 1:17, NIV), guaranteeing that every patient receives an equitable risk assessment regardless of socioeconomic background.

**Service to the Vulnerable.** The application serves chronically ill patients by translating complex model outputs into transparent, easy-to-understand health summaries, while reducing clinicians' administrative burdens through automated reporting.

### Structured Use Case Analysis (Competency 2.2)

A structured five-step use case analysis framework ensures the system solves the actual clinical problem rather than a theoretical one:

1. **Stakeholder and Context Mapping**: Three personas are defined. Clinicians require rapid, explainable risk flags during patient encounters. Data analysts need pipeline performance metrics and model accuracy dashboards. Administrators require secure role-based user management and audit logs.
2. **Data Requirement Specification**: Systolic and diastolic blood pressure readings, patient demographics, BMI, sodium intake, and medication history serve as model inputs, mapped to a hypertension risk classification output.
3. **Analytical Engine Design**: XGBoost and Random Forest classifiers are selected, with performance metrics prioritizing recall and sensitivity to minimize missed high-risk diagnoses.
4. **Integration and Interface Mapping**: Backend predictions flow into the React dashboard via RESTful API endpoints, with automated PDF report generation for clinical documentation.
5. **Security and Compliance Auditing**: Role-Based Access Control (RBAC) and database encryption safeguard Protected Health Information (PHI), simulating HIPAA-compliant development practices.

---

## Conduct a Needs Analysis

Hypertension affects approximately 47% of the adult population in the United States, yet only about 24% of those diagnosed have their condition under control (Tsao et al., 2023). Traditional clinical management suffers from data fragmentation: patients log blood pressure sporadically using paper logs or disconnected mobile apps, and clinicians lack the time to analyze longitudinal trends during brief 15-minute consultations (Whelton et al., 2018). Existing electronic health record (EHR) systems provide storage but not predictive intelligence.

This system addresses these gaps by providing an automated data ingestion and preprocessing pipeline that transforms periodic patient uploads into structured longitudinal profiles. The anomaly detection engine catches clinically significant spikes before they escalate into hypertensive crises, while the SHAP-powered explanation layer bridges the trust gap between algorithmic output and clinical decision-making.

---

## Create a Project Timeline

The capstone is organized into four phases across eight weeks, as illustrated in the Gantt chart below:

![DSC-590 Capstone Project Gantt Chart](C:\Users\rajac\.gemini\antigravity\brain\f2981cce-e7a9-436b-85ac-b8847e580e9f\gantt_chart_1787787939901.jpg)

| Phase | Weeks | Dates | Key Deliverables |
| :--- | :--- | :--- | :--- |
| **Planning & Scope** | 1–2 | Aug 20 – Sep 2 | Needs analysis report, project scope document, database schema, preprocessing pipeline design |
| **ML Modeling** | 3–4 | Sep 3 – Sep 16 | Baseline classifiers (XGBoost, Random Forest), anomaly detection engine, RBAC middleware |
| **Dashboard & XAI** | 5–6 | Sep 17 – Sep 30 | SHAP visualization integration, fairness audit dashboard, clinical report generator |
| **Validation & Close** | 7–8 | Oct 1 – Oct 14 | Security audit, scientific capstone paper, final showcase poster presentation |

---

## Identify Resources

| Resource Category | Specific Resources | Acquisition Plan |
| :--- | :--- | :--- |
| **Data Sources** | CDC NHANES public health dataset; simulated longitudinal BP records | NHANES data downloaded at no cost from the CDC public data portal. Synthetic patient data generated via Python scripts to avoid privacy violations. |
| **Software & Frameworks** | Python 3.9+, FastAPI, PostgreSQL, React, Scikit-learn, XGBoost, SHAP | All open-source; installed via pip and npm package managers. |
| **Hosting Platforms** | GitHub, Vercel (frontend), Render (backend + PostgreSQL) | Free-tier cloud hosting plans; GitHub Education license for private repositories. |
| **Collaboration** | Instructor office hours, peer code reviews, GCU library databases | Scheduled through LoudCloud course portal and GCU library access. |

---

## Anticipate Challenges and Devise Strategies

**Challenge 1: Privacy and Security of Patient Data.**
Even with simulated data, the system must demonstrate production-grade security. The mitigation strategy employs database column-level encryption, strict RBAC route protection, and comprehensive audit logging on the FastAPI server. This approach embodies the Christian principle of transparency, ensuring that data handling practices are open and accountable (Saltz & Krasteva, 2022).

**Challenge 2: Algorithmic Bias and Inequitable Predictions.**
Predictive models trained on imbalanced datasets risk systematically disadvantaging minority populations. Drawing on the Christian teaching of fairness, model accuracy will be audited across demographic sub-groups using equalized odds metrics. If bias is detected, resampling techniques (SMOTE) or threshold calibration will be applied to guarantee equitable classification, reflecting the commitment to community engagement and equal treatment.

**Challenge 3: Clinician Resistance to Black-Box Models.**
Healthcare professionals resist acting on predictions they cannot interpret. By integrating interactive SHAP waterfall plots that show exactly why a specific patient was flagged, the system practices radical transparency. This approach fosters community trust between the technical team and clinical stakeholders, ensuring the tool is collaborative rather than prescriptive.

---

## References

Lundberg, S. M., & Lee, S.-I. (2017). A unified approach to interpreting model predictions. *Advances in Neural Information Processing Systems*, 30, 4765–4774.

Saltz, J., & Krasteva, I. (2022). Current approaches for executing big data science projects: A systematic literature review. *PeerJ Computer Science*, 8, e942. https://doi.org/10.7717/peerj-cs.942

Tsao, C. W., Aday, A. W., Almarzooq, Z. I., Anderson, C. A., Arora, P., Avery, C. L., ... & Martin, S. S. (2023). Heart disease and stroke statistics—2023 update: A report from the American Heart Association. *Circulation*, 147(8), e93–e621. https://doi.org/10.1161/CIR.0000000000001123

Whelton, P. K., Carey, R. M., Aronow, W. S., Casey, D. E., Collins, K. J., Himmelfarb, C. D., ... & Wright, J. T. (2018). 2017 ACC/AHA/AAPA/ABC/ACPM/AGS/APhA/ASH/ASPC/NMA/PCNA guideline for the prevention, detection, evaluation, and management of high blood pressure in adults. *Journal of the American College of Cardiology*, 71(19), e127–e248. https://doi.org/10.1016/j.jacc.2017.11.006
