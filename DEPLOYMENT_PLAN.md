# Deployment Plan: Telehealth Hypertension Predictive Analytics System

---

## Overview

The Telehealth Hypertension Predictive Analytics System is a cloud deployed, full stack data product designed for three types of users: administrators, clinicians, and data analysts. The system gives these users a secure, browser based way to work with hypertension patient data, from uploading raw files all the way through building predictive models and generating reports. The goal is to support telehealth care teams that are spread across different locations and need access to the same analytical tools without installing anything locally.

The product is now live across two cloud platforms:

- **Frontend (Vercel):** https://telehealth-hypertension-analytics-vercel-p45feeg88.vercel.app/
- **Backend API (Render):** https://telehealth-hypertension-analytics.onrender.com/
- **Interactive API Docs:** https://telehealth-hypertension-analytics.onrender.com/docs

### Cloud Platforms Selected

**Render.com** hosts the Python FastAPI backend. Render was the right choice here because the repository already had a `render.yaml` configuration file pointing to the Oregon region on a free tier Python web service. It handles ASGI applications through Uvicorn, manages PostgreSQL databases, provisions TLS certificates automatically, and rolls out new versions whenever code is pushed to GitHub. None of the underlying server infrastructure needs to be managed manually. The backend runs via `uvicorn app.main:app --host 0.0.0.0 --port $PORT`, with `DATABASE_URL` and an automatically generated `SECRET_KEY` provided as environment variables at startup.

**Vercel** hosts the React/Vite frontend as a static site distributed globally through its edge network. Pages load in under 100ms for most users regardless of location. The build process runs automatically using `npm run build` and serves the output from the `dist` directory. Each GitHub branch also gets its own preview URL, which made testing easy before the final version went live. The frontend talks to the Render backend through `VITE_API_URL`, and CORS is configured on the API side to accept requests from the Vercel domain.

### Deployment Activities Completed

- Provisioned managed PostgreSQL on Render
- Injected environment variables (`DATABASE_URL`, `SECRET_KEY`)
- Executed `init_schema.sql` to create the five production tables
- Seeded four default accounts via `sample_users.sql`
- Built and deployed the Docker based backend service
- Connected the Vercel frontend to the live API base URL

---

## Assumptions, Dependencies, and Constraints

### Assumptions

- The instructor has a modern browser (Chrome, Firefox, Edge) and internet access.
- The Render free tier web service is active. If it has been idle for a while, the first request may take 30 to 60 seconds while the service wakes up. After that, responses return to normal speed.
- The PostgreSQL instance on Render keeps its data between deploys unless it is manually reset.
- Opening up CORS to all origins is acceptable in this academic context.

### Dependencies

| Layer | Technology | Version |
|---|---|---|
| Backend runtime | Python / FastAPI / Uvicorn | 3.11 / 0.104.1 |
| ORM | SQLAlchemy | 2.0.23 |
| Database driver | psycopg2-binary | latest |
| ML | scikit-learn / XGBoost | 1.3.2 / 2.0.3 |
| PDF generation | ReportLab | 4.0.7 |
| Frontend | React / Vite | 18.2.0 / 4.1.0 |
| HTTP client | Axios | 1.3.0 |
| Charting | Chart.js / Plotly.js | 4.2.0 / 2.18.0 |
| UI | Material-UI | 5.11.0 |
| Database | PostgreSQL (Render managed) | 15 |
| CI/CD | GitHub to Render and Vercel | automatic deploy on push to `main` |

### Constraints

- Render's free tier shuts down services that have been inactive for 15 minutes. This is fine for academic evaluation but would not meet the uptime requirements of a real production system.
- Uploaded files are stored in temporary memory on Render. A production version of this system would need a dedicated file storage service like S3 to persist uploads reliably.
- Model training runs synchronously, so multiple users submitting large training jobs at the same time could cause timeouts on the free tier.
- Sensitive values like `SECRET_KEY` and `DATABASE_URL` are stored in Render's environment variable panel and are never written into the codebase.

---

## Operational Readiness

Before sharing the URLs, the following checks were completed to confirm the system was ready:

| Check | Method | Status |
|---|---|---|
| Backend root endpoint responds | `GET /` returns welcome message JSON | Verified |
| API documentation accessible | `GET /docs` renders Swagger UI with all 8 route groups | Verified |
| Database schema initialized | All 5 tables present: `users`, `datasets`, `models`, `reports`, `pipeline_steps` | Verified |
| Seed users created | 4 accounts seeded on first startup by `main.py` | Verified |
| Authentication flow functional | `POST /api/auth/login` returns JWT bearer token | Verified |
| Frontend loads | Vercel URL renders React application with navigation | Verified |
| Frontend to backend connectivity | Login API call succeeds from the Vercel domain | Verified |
| Role based access | Admin, clinician, and analyst each see the correct navigation options | Verified |
| Full pipeline end to end | Upload, explore, clean, train, and report all complete without errors | Verified |
| Multiple user access | Three simultaneous browser sessions confirmed working at the same time | Verified |

End to end tests from the `/frontend/tests/` folder and the pytest suite in `/backend/tests/` were both run before deployment using `pytest --cov`. All tests passed before the code was pushed to production.

---

## Data Conversion

The database schema was set up by running `init_schema.sql` against the Render managed PostgreSQL instance. The script drops and recreates five tables:

| Table | Purpose |
|---|---|
| `users` | Stores login credentials, user roles, active status, and superuser flags |
| `datasets` | Tracks uploaded dataset names and file paths, linked to the user who uploaded them |
| `models` | Stores trained model metadata and parameters for each user |
| `reports` | Holds generated report data linked to the user who requested it |
| `pipeline_steps` | Records each step in a workflow run, including its order and parameters |

### Seeded Default Users

| Username | Email | Role | Superuser |
|---|---|---|---|
| admin | admin@telehealth.com | administrator | Yes |
| clinician | clinician@telehealth.com | clinician | No |
| analyst | analyst@telehealth.com | data_analyst | No |
| testuser | test@example.com | clinician | No |

No data from a previous system needed to be migrated. The hypertension CSV datasets that were used during local development were uploaded again through the live Data Ingestion interface after deployment. This confirmed that the upload endpoint stores file metadata correctly and that the dataset becomes available for the rest of the pipeline. Row counts, column types, and stored parameter values were all checked and matched what was expected.

---

## Phased Rollout

### Phase 1 — Infrastructure Provisioning (Day 1)

- Render managed PostgreSQL instance created and connection string saved to `DATABASE_URL`.
- `render.yaml` applied: Python web service deployed in Oregon region on the free plan.
- `SECRET_KEY` automatically generated and injected by Render.
- Backend started up and created all tables, then seeded the default users on first boot.
- Confirmed that `GET https://telehealth-hypertension-analytics.onrender.com/` returns HTTP 200.

### Phase 2 — Backend API Verification (Day 1 and 2)

The Swagger UI at `/docs` was used to confirm that all 8 API route groups were available and responding correctly:

| Route Group | Prefix |
|---|---|
| Authentication | `/api/auth` |
| Data Ingestion | `/api/data-ingestion` |
| Data Exploration | `/api/exploration` |
| Data Cleaning | `/api/cleaning` |
| ML Modeling | `/api/modeling` |
| Visualization | `/api/visualization` |
| Reporting | `/api/reporting` |
| Pipeline | `/api/pipeline` |

A JWT token was obtained through `POST /api/auth/login` and used to test protected endpoints directly in the Swagger UI.

### Phase 3 — Frontend Deployment (Day 2)

- Repository connected to Vercel with build command `npm run build` and publish directory set to `dist`.
- `VITE_API_URL` set to `https://telehealth-hypertension-analytics.onrender.com` in the Vercel environment settings.
- Vercel deployed successfully and the frontend URL went live.
- Login was tested from the Vercel domain to confirm that API requests were reaching the Render backend without any CORS issues.

### Phase 4 — Feature Verification (Day 3)

Every feature in the application was tested in the live environment. Full details are in the Test Plan section below.

### Phase 5 — Multiple User and Report Demonstration (Day 3 and 4)

- Three browser sessions were opened at the same time: laptop Chrome, mobile Safari, and a laptop incognito window.
- Each session logged in under a different role: admin, clinician, and analyst.
- All three sessions ran simultaneously without affecting each other, confirming that the stateless JWT based authentication keeps sessions fully isolated.

### Phase 6 — Stakeholder Release (Day 4)

- Final URLs submitted for evaluation.
- Render service health and Vercel deployment logs both checked and confirmed clean.

---

## Test Plan

### Authentication Tests

| Test ID | Test Case | Steps | Expected Result |
|---|---|---|---|
| AUTH-01 | Valid admin login | `POST /api/auth/login` with `admin` and correct password | Returns `access_token` (JWT) and `token_type: bearer` |
| AUTH-02 | Valid clinician login | `POST /api/auth/login` with `clinician` credentials | Returns JWT token |
| AUTH-03 | Invalid credentials | `POST /api/auth/login` with wrong password | Returns HTTP 401 Unauthorized |
| AUTH-04 | No token on protected endpoint | `GET /api/auth/users/me` with no Authorization header | Returns HTTP 401 |
| AUTH-05 | Valid token on protected endpoint | `GET /api/auth/users/me` with `Bearer <token>` | Returns user profile JSON |
| AUTH-06 | Role enforcement | Log in as analyst and attempt an admin only action | Returns HTTP 403 Forbidden |

---

### Data Ingestion Tests

| Test ID | Test Case | Steps | Expected Result |
|---|---|---|---|
| ING-01 | Upload CSV file | `POST /api/data-ingestion/upload` with valid `.csv` | Returns `dataset_id` and success message |
| ING-02 | Upload Excel file | POST with `.xlsx` file | Dataset created and metadata stored |
| ING-03 | Upload JSON file | POST with `.json` file | Dataset created successfully |
| ING-04 | Upload unsupported format | POST with `.txt` file | Returns HTTP 400 with error message |
| ING-05 | Import from URL | `POST /api/data-ingestion/url` with valid CSV URL | Dataset fetched and created |
| ING-06 | Verify dataset persisted | After upload, check `datasets` table | Record present with correct `user_id` and `file_path` |

---

### Data Exploration Tests

| Test ID | Test Case | Steps | Expected Result |
|---|---|---|---|
| EXP-01 | Summary statistics | `POST /api/exploration/statistics` with `dataset_id` | Returns mean, median, std dev, min, and max per column |
| EXP-02 | Visualization data | `GET /api/exploration/visualization-data?dataset_id=X` | Returns chart ready JSON |
| EXP-03 | Correlation matrix | Request correlation from the exploration endpoint | Returns correlation coefficients between numerical columns |
| EXP-04 | Invalid dataset ID | Request stats with a non-existent `dataset_id` | Returns HTTP 404 |

---

### Data Cleaning Tests

| Test ID | Test Case | Steps | Expected Result |
|---|---|---|---|
| CLN-01 | Mean imputation | `POST /api/cleaning/clean` with `imputation_method: "mean"` | Missing values replaced with column mean |
| CLN-02 | Median imputation | `imputation_method: "median"` | Missing values replaced with median |
| CLN-03 | Outlier detection | `outlier_detection: true` | Outlier rows flagged or removed |
| CLN-04 | Min max scaling | `scaling_method: "minmax"` | Values normalized to [0, 1] range |
| CLN-05 | Standard scaling | `scaling_method: "standard"` | Values z-score normalized |
| CLN-06 | One hot encoding | `encoding_method: "onehot"` | Categorical columns expanded to binary columns |
| CLN-07 | Combined operations | All four options enabled at once | All transformations applied in the correct order |

---

### Modeling Tests

| Test ID | Test Case | Steps | Expected Result |
|---|---|---|---|
| MDL-01 | Train logistic regression | `POST /api/modeling/train` with `model_type: "logistic_regression"` | Returns `model_id`, accuracy, precision, recall, and F1 score |
| MDL-02 | Train random forest | `model_type: "random_forest"` | Returns metrics and a feature importance dictionary |
| MDL-03 | Train XGBoost | `model_type: "xgboost"` | Model trained and feature importance returned |
| MDL-04 | Hyperparameter tuning | `POST /api/modeling/tune` with a parameter grid | Returns the best parameters and cross validated score |
| MDL-05 | Model evaluation | `POST /api/modeling/evaluate` with `model_id` and test data | Returns confusion matrix and ROC-AUC score |
| MDL-06 | Model explainability | `POST /api/modeling/explain` | Returns feature importance scores |
| MDL-07 | Missing target column | Train with an invalid `target` field name | Returns HTTP 400 with a descriptive error |

---

### Visualization Tests

| Test ID | Test Case | Steps | Expected Result |
|---|---|---|---|
| VIZ-01 | Chart data | `GET /api/visualization/visualizations/charts?dataset_id=X` | Returns Plotly and Chart.js compatible JSON |
| VIZ-02 | Dashboard data | `GET /api/visualization/visualizations/dashboard?dataset_id=X` | Returns aggregated metrics for the dashboard |
| VIZ-03 | Risk gauge | `GET /api/visualization/visualizations/risk-gauge?dataset_id=X` | Returns a risk score for the gauge chart |
| VIZ-04 | Frontend chart rendering | Open the Visualization tab in a browser | Charts render without any console errors |
| VIZ-05 | Dashboard interactivity | Change the selected dataset in the dashboard UI | Charts update to reflect the new selection |

---

### Reporting Tests

| Test ID | Test Case | Steps | Expected Result |
|---|---|---|---|
| RPT-01 | Generate PDF report | `POST /api/reporting/reports/pdf` with JSON data | Returns a downloadable PDF file |
| RPT-02 | Export CSV | `POST /api/reporting/reports/csv` | Returns a downloadable `.csv` file |
| RPT-03 | Report placeholder visible | Navigate to the Reporting section in the UI | Report generation form visible on the page |
| RPT-04 | Report stored in DB | After generation, check the `reports` table | Record present with `user_id` and `report_data` |
| RPT-05 | Empty data submission | Submit an empty JSON body | Returns HTTP 422 Unprocessable Entity |

---

### Pipeline Tests

| Test ID | Test Case | Steps | Expected Result |
|---|---|---|---|
| PIP-01 | Start pipeline | `POST /api/pipeline/pipeline/start` with step definitions | Returns a pipeline started confirmation |
| PIP-02 | Check status | `GET /api/pipeline/pipeline/status` | Returns the current step name and progress |
| PIP-03 | Execute single step | `POST /api/pipeline/pipeline/execute` with one step | Step runs and returns a result |
| PIP-04 | Stop pipeline | `POST /api/pipeline/pipeline/stop` | Pipeline stops and status reflects the change |
| PIP-05 | Full end to end pipeline | Ingest, explore, clean, model, visualize, and report in sequence | All steps finish and the `pipeline_steps` table records each one |

---

### Multiple User Concurrent Access Tests

| Test ID | Test Case | Steps | Expected Result |
|---|---|---|---|
| MU-01 | Simultaneous login | Open desktop Chrome, a mobile browser, and an incognito tab; log in with admin, clinician, and analyst | All three sessions authenticate at the same time |
| MU-02 | Concurrent data upload | Two users upload different CSV files at the same time | Both uploads succeed and each dataset is tied to the correct user |
| MU-03 | Concurrent model training | Two analyst sessions submit training jobs at the same time | Both return correct results with no overlap between models |
| MU-04 | Session isolation | Admin makes a change; check that the clinician session is unaffected | Each session remains fully independent |
| MU-05 | Concurrent report generation | Two users generate PDF reports at the same time | Both receive the correct report for their own data |

---

### Security Tests

| Test ID | Test Case | Steps | Expected Result |
|---|---|---|---|
| SEC-01 | Expired token rejection | Use a JWT token after its expiration window | Returns HTTP 401 |
| SEC-02 | Tampered token | Modify the JWT payload and resubmit | Returns HTTP 401 because the signature no longer matches |
| SEC-03 | SQL injection in login | Submit `' OR 1=1; --` as the username | SQLAlchemy parameterized queries block the injection and return 401 |
| SEC-04 | Password storage | Check the `hashed_password` column in the `users` table | Passwords are stored as bcrypt hashes, never in plain text |
| SEC-05 | HTTPS enforced | Try accessing both URLs over plain HTTP | Render and Vercel redirect all traffic to HTTPS automatically |

---

## Support

### User Credentials for Testing

| Role | Username | Email |
|---|---|---|
| Administrator | admin | admin@telehealth.com |
| Clinician | clinician | clinician@telehealth.com |
| Data Analyst | analyst | analyst@telehealth.com |
| Test User | testuser | test@example.com |

### Self-Service Documentation

The Swagger UI at https://telehealth-hypertension-analytics.onrender.com/docs covers every API endpoint with request and response examples that can be tested directly in the browser. No additional setup is needed to use it.

### User Training Workflow Guide

1. Navigate to https://telehealth-hypertension-analytics-vercel-p45feeg88.vercel.app/
2. Log in with your assigned credentials.
3. Upload a hypertension CSV dataset using the **Data Ingestion** tab.
4. Review summary statistics and correlations in the **Data Exploration** tab.
5. Handle missing values, outliers, and scaling in the **Data Cleaning** tab.
6. Choose a model type, train it, and review the accuracy metrics in the **Modeling** tab.
7. Explore the risk gauge, charts, and dashboard in the **Visualization** tab.
8. Generate and download a PDF or CSV report from the **Reporting** tab.

### Administrator Tasks

Users with administrator access and the `is_superuser` flag set to true can create new accounts, disable existing ones, and review pipeline logs through the **User Management** section. This area is only visible to administrator accounts.

---

## Release Planning

### Production Release Artifacts

| Artifact | URL |
|---|---|
| Live Frontend | https://telehealth-hypertension-analytics-vercel-p45feeg88.vercel.app/ |
| Live Backend API | https://telehealth-hypertension-analytics.onrender.com/ |
| Interactive API Docs | https://telehealth-hypertension-analytics.onrender.com/docs |

Both platforms are connected to the GitHub repository and will redeploy automatically whenever new code is pushed to `main`.

### Evidence of Deployment

- The Vercel deployment dashboard shows a successful build with full `vite build` output and a deployment timestamp.
- The Render dashboard shows the web service as **Live** and the PostgreSQL instance as **Available**, with logs confirming that the application started up cleanly.
- Screenshots document three simultaneous browser sessions running under different roles.
- Screenshots show a PDF report being requested, produced, and downloaded from the live site.

### Contingency Plans

| Scenario | Contingency |
|---|---|
| Render free tier cold start delays evaluation | Open the `/docs` page about 60 seconds before testing to wake the service up first |
| Render service crashes during evaluation | Use the one click redeploy option in the Render dashboard to restore the last working build |
| Vercel frontend build fails on a new push | Roll back to the previous deployment using Vercel's instant rollback feature |
| Database data is lost | Rerun `init_schema.sql` and `sample_users.sql`; the application will reseed users on the next startup |
| CORS errors appear from a new domain | Add the domain to the allowed origins list in the FastAPI middleware and redeploy |
| ML training times out on the free tier | Use a smaller dataset or a narrower parameter grid; upgrading to Render Starter at $7 per month removes this limitation |

### Post-Release Monitoring

- Render streams request and error logs in real time from the service dashboard.
- Vercel provides deployment logs and edge network traffic data.
- Any unhandled errors in the backend are captured by the logging setup in `backend/app/core/logging.py` and appear immediately in the Render log stream.
