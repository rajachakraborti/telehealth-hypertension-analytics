# Telehealth Hypertension Predictive Analytics System

This repository contains the backend API and machine learning pipeline for a telehealth system designed to monitor and predict hypertensive crises using synthetic Ambulatory Blood Pressure Monitoring (ABPM) telemetry.

> **Reviewing this project?** Start with [PROGRESS.md](PROGRESS.md): it maps every milestone (Topics 1 to 8) to its deliverable and to the commits and code that support it. Final deliverables are in `submissions/`.

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

### 6. Reproduce the results
Requirements: Python 3.10 and Node 20 (for the dashboard). The report, deck and poster builders (`build_*.py`) also need Windows with Microsoft Office; everything else runs on any OS.
```bash
git clone https://github.com/rajachakraborti/telehealth-hypertension-analytics.git
cd telehealth-hypertension-analytics
python -m venv .venv && source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt

# 1. Tests (about 30 seconds). Expect: 48 passed
cd backend && pytest && cd ..

# 2. Rebuild the model, metrics and figures (about 10 minutes; executes the notebook in place)
python scripts/run_notebook.py Topic_6_Advanced_Analysis_and_Model_Refinement.ipynb
python scripts/make_topic7_figures.py

# 3. Run the app: backend in one terminal, dashboard in another
cd backend && python -m uvicorn app.main:app --port 8000
cd frontend && npm install && npm run dev               # http://localhost:3000
```
Sign in with `clinician` / `clinician123` (demo account), open **Clinical > ABPM Staging**, load a sample record and click **Classify record**.

After step 2, `artifacts/topic6/topic6_metrics.json` should show holdout accuracy 0.902, Stage 2 recall 0.970, macro ROC-AUC 0.984 and ECE 0.014, with hyperparameter search adopted and isotonic calibration rejected. Random seeds are fixed (42), so results repeat on the same library versions. Step 2 also rewrites `backend/models_saved/abpm_xgb_refined.json`; the parity test in step 1 checks that the API reproduces the notebook's features and probabilities.
