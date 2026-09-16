# Telehealth Hypertension Predictive Analytics System

This repository contains the backend API and machine learning pipeline for a telehealth system designed to monitor and predict hypertensive crises using synthetic Ambulatory Blood Pressure Monitoring (ABPM) telemetry.

## Architecture & Features
* **Machine Learning Pipeline**: Custom XGBoost Classifier (AHA Hypertension Staging) and Isolation Forest (Anomaly Detection).
* **Explainable AI (XAI)**: Dual-layer SHAP TreeExplainer generating both mathematical feature attributions and plain-English clinical summaries.
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

### 3. Load Testing (Locust)
To evaluate the p95 latency overhead of the database encryption and JWT security layers:
```bash
cd backend
locust -f scripts/locustfile.py
```
Navigate to `http://localhost:8089` to start the simulated concurrent users.

### 4. Unit Testing
Run the test suite using pytest to verify statistical boundaries and API security:
```bash
cd backend
pytest tests/
```