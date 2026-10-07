# Telehealth Hypertension Predictive Analytics System

This repository contains the backend API and machine learning pipeline for a telehealth system designed to monitor and predict hypertensive crises using synthetic Ambulatory Blood Pressure Monitoring (ABPM) telemetry.

## Architecture & Features
* **ABPM staging model (current)**: XGBoost classifier that stages a patient's full 24-hour ambulatory record (Normal, Elevated, Stage 1, Stage 2). Served at `POST /api/abpm/classify`; trained and evaluated in `Topic_6_Advanced_Analysis_and_Model_Refinement.ipynb`.
* **Legacy per-reading models**: the original XGBoost/Isolation Forest pair under `/api/modeling`. Superseded by the ABPM staging model; its split is by reading, not by patient (see the audit report).
* **Explainable AI (XAI)**: TreeSHAP attributions for the predicted stage, returned with a plain-English summary and a manual-review flag when confidence is below 65% (`ABPM_REVIEW_THRESHOLD`).
* **HIPAA Compliance**: 
  * Role-Based Access Control (RBAC) via OAuth2 JWT.
  * Column-level encryption (`pgp_sym_encrypt`) on PostgreSQL for Protected Health Information (PHI).
* **Data Synthesis**: Automated data generator producing time-series telemetry strictly adhering to clinical bounds (MAP 70-110, Dipping 10-20%).

## Getting Started

### 1. Installation
Install the project dependencies inside a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
pip install shap locust pytest
```

### 2. Running the Server
Launch the FastAPI server:
```bash
cd backend
python -m uvicorn app.main:app --port 8000
```
Navigate to `http://localhost:8000/docs` to view the interactive Swagger API documentation.

### 3. ABPM staging model: reproduce and call
Re-run the notebook (about 20 minutes, mostly the nested cross-validation). It writes metrics and figures to `artifacts/topic6/`, the model to `backend/models_saved/abpm_xgb_refined.json`, a model card, and the parity fixture used by the tests:
```bash
python -m nbconvert --to notebook --execute --inplace Topic_6_Advanced_Analysis_and_Model_Refinement.ipynb
python scripts/make_topic7_figures.py
```
Classify one 24-hour record (clinician or administrator token required; sample records are in `frontend/public/sample_abpm_patients.json`):
```bash
curl -X POST http://localhost:8000/api/abpm/classify -H "Authorization: Bearer $TOKEN"      -H "Content-Type: application/json" -d @record.json
```
The model was trained on **simulated** data and is **not clinically validated**; see `abpm_model_card.json`. Optional environment variables: `ABPM_REVIEW_THRESHOLD`, `CORS_ORIGINS`, `SEED_<USERNAME>_PASSWORD`, `SECRET_KEY`, `PGP_SYMMETRIC_KEY`.

### 4. Load Testing (Locust)
To evaluate the p95 latency overhead of the database encryption and JWT security layers:
```bash
cd backend
locust -f scripts/locustfile.py
```
Navigate to `http://localhost:8089` to start the simulated concurrent users.

### 5. Unit Testing
Run the test suite using pytest to verify statistical boundaries and API security:
```bash
cd backend
pytest tests/
```