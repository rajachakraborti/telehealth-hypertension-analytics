# Capstone Milestone 3: Implementation
## Telehealth Hypertension Predictive Analytics System

**Course:** CST/DSC-580  
**Submitted by:** Raja Chakraborty  
**Date:** May 2026  

---

## Introduction

This document presents the implementation of the Telehealth Hypertension Predictive Analytics System. The system was designed to give clinicians, data analysts, and administrators a single browser-based platform for working with hypertension patient data, from raw file ingestion through machine learning model training, visualization, and report generation. This milestone covers four areas: a mapping of every functional requirement to the code that satisfies it, a complete listing of all source code files, the implementation plan describing how the system was built and deployed, and a review of the project requirements as they stand after implementation.

The system is live at the following URLs:

- **Frontend:** https://telehealth-hypertension-analytics-vercel-p45feeg88.vercel.app/
- **Backend API:** https://telehealth-hypertension-analytics.onrender.com/
- **API Documentation:** https://telehealth-hypertension-analytics.onrender.com/docs

---

## Section 1: Mapping of Functional Requirements

Each functional requirement is traced to the specific backend endpoints and service functions that implement it, along with the frontend components that expose the feature to the user.

---

### FR1 — User Registration

New users can create accounts through the registration form.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/auth.py` → `POST /api/auth/register` |
| Service | `auth.py` → user creation logic with bcrypt password hashing |
| Database | `backend/app/models/user.py` → `User` ORM model |
| Frontend | `frontend/src/components/UserManagement/Register.jsx` |

---

### FR2 — User Login and JWT Authentication

Registered users can log in and receive a JWT token that authorizes all subsequent requests.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/auth.py` → `POST /api/auth/login` |
| Token Handling | `backend/app/core/security.py` → token creation and verification |
| Configuration | `backend/app/core/config.py` → `SECRET_KEY`, token expiry settings |
| Frontend | `frontend/src/components/UserManagement/Login.jsx` |
| Context | `frontend/src/context/AuthContext.jsx` → stores token and user state globally |
| Service | `frontend/src/services/auth.js` → handles login requests and token storage |

---

### FR3 — Role-Based Access Control

The system supports three roles: administrator, clinician, and data analyst. Each role sees different navigation options and has different permissions.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/auth.py` → `GET /api/auth/users/me` |
| Auth Guard | `backend/app/api/endpoints/auth.py` → `get_current_user()` dependency |
| Database | `backend/app/models/user.py` → `role` and `is_superuser` columns |
| Frontend | `frontend/src/components/Auth/ProtectedRoute.jsx` → blocks unauthorized routes |
| UI | `frontend/src/components/UserManagement/RoleManagement.jsx` → admin role panel |

---

### FR4 — Data File Upload

Users can upload datasets in CSV, Excel, JSON, or Parquet format.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/data_ingestion.py` → `POST /api/data-ingestion/upload` |
| File Service | `backend/app/services/data_ingestion/file_handler.py` → `handle_file_upload()` |
| Validation | `backend/app/services/data_ingestion/validator.py` → extension and content checks |
| Configuration | `backend/app/core/config.py` → `ALLOWED_EXTENSIONS`, `MAX_CONTENT_LENGTH` (16 MB) |
| Database | `backend/app/models/dataset.py` → stores dataset name and file path |
| Frontend | `frontend/src/components/DataIngestion/FileUpload.jsx` |

---

### FR5 — Data Import from URL

Users can import a dataset by providing a URL that points to a remote CSV or data file.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/data_ingestion.py` → `POST /api/data-ingestion/url` |
| URL Service | `backend/app/services/data_ingestion/url_handler.py` → `handle_url_import()` |
| API Adapter | `backend/app/services/data_ingestion/api_handler.py` → handles external API sources |
| Frontend | `frontend/src/components/DataIngestion/URLImport.jsx` |

---

### FR6 — Summary Statistics and Data Exploration

Users can view descriptive statistics (mean, median, standard deviation, min, max) for any uploaded dataset.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/data_exploration.py` → `POST /api/exploration/statistics` |
| Service | `backend/app/services/data_exploration/statistics.py` → `calculate_statistics()` |
| Frontend | `frontend/src/components/DataExploration/SummaryStatistics.jsx` |
| Frontend | `frontend/src/components/DataExploration/DataTable.jsx` |

---

### FR7 — Correlation Analysis

Users can view a correlation matrix showing the relationships between numerical columns.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/data_exploration.py` → `GET /api/exploration/visualization-data` |
| Service | `backend/app/services/data_exploration/visualization_data.py` → `prepare_visualization_data()` |
| Frontend | `frontend/src/components/DataExploration/CorrelationMatrix.jsx` |

---

### FR8 — Missing Value Imputation

Users can fill in missing values using mean or median imputation strategies.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/data_cleaning.py` → `POST /api/cleaning/clean` |
| Service | `backend/app/services/data_cleaning/imputation.py` → `perform_imputation()` |
| Frontend | `frontend/src/components/DataCleaning/ImputationPanel.jsx` |
| Frontend | `frontend/src/components/DataCleaning/PreprocessingHistory.jsx` |

---

### FR9 — Outlier Detection and Removal

Users can flag or remove statistical outliers from their dataset.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/data_cleaning.py` → `POST /api/cleaning/clean` with `outlier_detection: true` |
| Service | `backend/app/services/data_cleaning/outlier_detection.py` → `detect_outliers()` |
| Frontend | `frontend/src/components/DataCleaning/OutlierDetection.jsx` |

---

### FR10 — Feature Scaling

Users can normalize or standardize numerical features using min-max or z-score scaling.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/data_cleaning.py` → `POST /api/cleaning/clean` with `scaling_method` |
| Service | `backend/app/services/data_cleaning/scaling.py` → `scale_data()` |
| Frontend | `frontend/src/components/DataCleaning/ImputationPanel.jsx` |

---

### FR11 — Categorical Encoding

Users can convert categorical columns into numerical representations using one-hot encoding.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/data_cleaning.py` → `POST /api/cleaning/clean` with `encoding_method` |
| Service | `backend/app/services/data_cleaning/encoding.py` → `encode_categorical()` |
| Frontend | `frontend/src/components/DataCleaning/ImputationPanel.jsx` |

---

### FR12 — Machine Learning Model Training

Users can train logistic regression, random forest, or XGBoost classifiers on their cleaned dataset.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/modeling.py` → `POST /api/modeling/train` |
| Service | `backend/app/services/modeling/model_trainer.py` → `train_model()` |
| Database | `backend/app/models/` → model metadata stored via SQLAlchemy |
| Frontend | `frontend/src/components/Modeling/ModelSelection.jsx` |

---

### FR13 — Hyperparameter Tuning

Users can provide a parameter grid and the system finds the best combination using cross-validation.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/modeling.py` → `POST /api/modeling/tune` |
| Service | `backend/app/services/modeling/hyperparameter_tuner.py` → `tune_hyperparameters()` |
| Frontend | `frontend/src/components/Modeling/HyperparameterTuning.jsx` |

---

### FR14 — Model Evaluation

Trained models can be evaluated against test data to produce accuracy, precision, recall, F1, ROC-AUC, and confusion matrix results.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/modeling.py` → `POST /api/modeling/evaluate` |
| Service | `backend/app/services/modeling/model_evaluator.py` → `evaluate_model()` |
| Frontend | `frontend/src/components/Modeling/ModelSelection.jsx` |

---

### FR15 — Model Explainability

Users can request feature importance scores to understand which variables drive model predictions.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/modeling.py` → `POST /api/modeling/explain` |
| Service | `backend/app/services/modeling/explainability.py` → `explain_model()` |
| Frontend | `frontend/src/components/Modeling/FeatureImportance.jsx` |

---

### FR16 — Interactive Charts and Dashboard

Users can view bar charts, scatter plots, histograms, and an aggregated metrics dashboard for their dataset.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/visualization.py` → `GET /api/visualization/visualizations/charts` |
| API Endpoint | `backend/app/api/endpoints/visualization.py` → `GET /api/visualization/visualizations/dashboard` |
| Service | `backend/app/services/data_exploration/visualization_data.py` → `prepare_visualization_data()` |
| Frontend | `frontend/src/components/Visualization/ChartBuilder.jsx` |
| Frontend | `frontend/src/components/Visualization/Dashboard.jsx` |

---

### FR17 — Hypertension Risk Gauge

A risk gauge visualizes the predicted hypertension risk score for the dataset in a clinical-friendly format.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/visualization.py` → `GET /api/visualization/visualizations/risk-gauge` |
| Service | `backend/app/services/data_exploration/visualization_data.py` → `prepare_visualization_data()` |
| Frontend | `frontend/src/components/Visualization/RiskGauge.jsx` |

---

### FR18 — PDF Report Generation

Users can generate and download a formatted PDF report summarizing their analysis.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/reporting.py` → `POST /api/reporting/reports/pdf` |
| Service | `backend/app/services/reporting/pdf_generator.py` → `generate_pdf_report()` |
| Database | `backend/app/db/repositories.py` → stores report metadata |
| Frontend | `frontend/src/components/Reporting/ReportGenerator.jsx` |
| Frontend | `frontend/src/components/Reporting/ExportOptions.jsx` |

---

### FR19 — CSV Data Export

Users can export cleaned or analyzed data as a downloadable CSV file.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/reporting.py` → `POST /api/reporting/reports/csv` |
| Service | `backend/app/services/reporting/csv_exporter.py` → `export_to_csv()` |
| Frontend | `frontend/src/components/Reporting/ExportOptions.jsx` |

---

### FR20 — Pipeline Workflow Management

Users can define, execute, monitor, and stop multi-step data processing workflows.

| Layer | Module / Function |
|---|---|
| API Endpoint | `backend/app/api/endpoints/pipeline.py` → `POST /api/pipeline/pipeline/start` |
| API Endpoint | `backend/app/api/endpoints/pipeline.py` → `POST /api/pipeline/pipeline/stop` |
| API Endpoint | `backend/app/api/endpoints/pipeline.py` → `GET /api/pipeline/pipeline/status` |
| API Endpoint | `backend/app/api/endpoints/pipeline.py` → `POST /api/pipeline/pipeline/execute` |
| Engine | `backend/app/services/pipeline/workflow_engine.py` → `WorkflowEngine` class |
| Executor | `backend/app/services/pipeline/step_executor.py` → individual step logic |
| Database | `backend/app/models/pipeline.py` → stores step records |
| Frontend | `frontend/src/components/Pipeline/PipelineControls.jsx` |
| Frontend | `frontend/src/components/Pipeline/WorkflowVisualizer.jsx` |

---

### FR21 — Multiple Simultaneous User Access

Multiple users with different roles can use the system at the same time without interfering with each other.

| Layer | Module / Function |
|---|---|
| Auth | `backend/app/core/security.py` → stateless JWT tokens, no shared server session |
| Database | `backend/app/models/user.py` → all records scoped by `user_id` foreign key |
| Server | `backend/app/main.py` → Uvicorn ASGI server with async request handling |
| Frontend | `frontend/src/context/AuthContext.jsx` → each browser session maintains its own token |

---

## Section 2: Source Code Listing

### Backend — Entry Point and Configuration

**`backend/app/main.py`**  
Application entry point. Creates the FastAPI app instance, registers CORS middleware to allow cross-origin requests from the Vercel frontend, initializes the database by creating all tables on startup, seeds four default users if they do not already exist, mounts static files, and registers the API router under the `/api` prefix. The Uvicorn server reads the port from the `$PORT` environment variable, which Render injects automatically.

**`backend/app/core/config.py`**  
Centralized application settings. Defines a `Config` base class with values for `SECRET_KEY`, `DATABASE_URI`, `DEBUG`, `LOGGING_LEVEL`, `ALLOWED_EXTENSIONS`, `MAX_CONTENT_LENGTH`, `APP_HOST`, and `APP_PORT`. Three environment subclasses extend this: `ProductionConfig` disables debug mode, `DevelopmentConfig` enables it, and `TestingConfig` uses an in-memory SQLite database. The default exported instance is `DevelopmentConfig`.

**`backend/app/core/security.py`**  
Handles password hashing and JWT token creation and verification. Uses the `passlib` library with the bcrypt algorithm to hash passwords before storage and verify them at login. Generates signed JWT access tokens using `python-jose` and the configured `SECRET_KEY`.

**`backend/app/core/logging.py`**  
Configures Python's standard logging module for the application. Sets the log level from `config.py` and formats log output for the Render log stream.

---

### Backend — API Layer

**`backend/app/api/router.py`**  
Aggregates all eight endpoint routers into a single `api_router` using FastAPI's `APIRouter`. Assigns URL prefixes and tag labels to each group: `/auth`, `/data-ingestion`, `/exploration`, `/cleaning`, `/modeling`, `/visualization`, `/reporting`, and `/pipeline`.

**`backend/app/api/endpoints/auth.py`**  
Defines three routes: `POST /register` creates a new user with a hashed password and a default role; `POST /login` validates credentials and returns a JWT access token; `GET /users/me` returns the currently authenticated user's profile. Includes the `get_current_user()` dependency function used by all protected routes across the application.

**`backend/app/api/endpoints/data_ingestion.py`**  
Handles incoming data files and URL-based imports. The upload endpoint validates the file extension against the allowed list, reads the byte content, and passes it to the file handler service. The URL import endpoint delegates to the URL handler. Both endpoints return a dataset record on success.

**`backend/app/api/endpoints/data_exploration.py`**  
Exposes two endpoints for exploring uploaded datasets. The statistics endpoint accepts a `dataset_id` and returns descriptive statistics computed by the service layer. The visualization data endpoint returns pre-formatted chart data for the frontend.

**`backend/app/api/endpoints/data_cleaning.py`**  
Accepts a `DataCleaningRequest` body containing the raw data and optional cleaning parameters. Applies imputation, outlier detection, scaling, and encoding in sequence based on which parameters are provided. Returns the cleaned dataset or raises an HTTP 400 error on failure.

**`backend/app/api/endpoints/modeling.py`**  
Handles model training and hyperparameter tuning. Defines `ModelRequest` and `ModelResponse` Pydantic schemas. The `/train` endpoint calls the model trainer service and returns model metrics and feature importance. The `/tune` endpoint runs cross-validated hyperparameter search and returns the best configuration.

**`backend/app/api/endpoints/visualization.py`**  
Provides three GET endpoints for chart data, dashboard aggregates, and the risk gauge score. All three accept a `dataset_id` query parameter and route through the visualization data service.

**`backend/app/api/endpoints/reporting.py`**  
Two POST endpoints for generating downloadable outputs. The PDF endpoint calls the report generator service using ReportLab and returns a formatted PDF. The CSV endpoint calls the CSV exporter and returns a comma-delimited file. Both endpoints return HTTP 500 on unexpected failures.

**`backend/app/api/endpoints/pipeline.py`**  
Manages the lifecycle of multi-step data processing pipelines. The start endpoint accepts a list of `PipelineStepSchema` objects and runs them through the `WorkflowEngine`. The stop endpoint halts any running pipeline. The status endpoint returns the current state. The execute endpoint runs a single named step.

---

### Backend — Data Models

**`backend/app/models/user.py`**  
SQLAlchemy ORM model for the `users` table. Columns include `id` (primary key), `username` (unique), `email` (unique), `hashed_password`, `role`, `is_active` (defaults to true), and `is_superuser` (defaults to false). Includes a `__repr__` method for readable output in logs and debugging.

**`backend/app/models/dataset.py`**  
ORM model for the `datasets` table. Tracks uploaded dataset names, file paths, the owning user's `user_id` foreign key, and timestamps for creation and last update.

**`backend/app/models/pipeline.py`**  
ORM model for the `pipeline_steps` table. Stores each step's name, execution order, JSONB parameter snapshot, and timestamps. Used to record and audit pipeline execution history.

---

### Backend — Database Layer

**`backend/app/db/database.py`**  
Sets up the SQLAlchemy engine and session factory. Uses SQLite by default (stored as `telehealth.db` in the backend root) with PostgreSQL available via the `DATABASE_URL` environment variable. Exports `SessionLocal` for use in FastAPI dependency injection and `Base` as the declarative base for all ORM models. The `get_db()` generator yields a session and closes it after each request.

**`backend/app/db/repositories.py`**  
Provides data access functions for creating, reading, and updating records in the database. Acts as an abstraction layer between the API endpoints and the SQLAlchemy models.

---

### Backend — Service Layer

**`backend/app/services/data_ingestion/file_handler.py`**  
Reads uploaded file bytes and parses them into a pandas DataFrame depending on the file format. Supports CSV, Excel (xls and xlsx), JSON, and Parquet. Returns a structured data object for downstream processing.

**`backend/app/services/data_ingestion/url_handler.py`**  
Fetches data from a user-provided URL using the `requests` library and reads it into a DataFrame. Handles redirect following and basic connection error reporting.

**`backend/app/services/data_ingestion/api_handler.py`**  
Handles ingestion from external API data sources, converting API responses into a DataFrame that the rest of the pipeline can process.

**`backend/app/services/data_ingestion/validator.py`**  
Checks that uploaded files have an allowed extension, are not empty, and contain data that can be parsed. Returns a validation result used by the endpoint before proceeding with ingestion.

**`backend/app/services/data_exploration/statistics.py`**  
Computes descriptive statistics for a DataFrame using pandas. Calculates mean, median, standard deviation, minimum, maximum, and null counts for each column. Returns results as a dictionary suitable for JSON serialization.

**`backend/app/services/data_exploration/visualization_data.py`**  
Prepares data structures formatted for Chart.js and Plotly on the frontend. Builds histogram data, scatter plot coordinates, correlation matrices, and risk gauge scores from the dataset.

**`backend/app/services/data_cleaning/imputation.py`**  
Fills missing values in a DataFrame using mean or median strategies applied column-by-column to numerical fields.

**`backend/app/services/data_cleaning/outlier_detection.py`**  
Identifies and removes statistical outliers using the interquartile range method. Rows with values beyond 1.5 times the IQR above or below the quartiles are flagged for removal.

**`backend/app/services/data_cleaning/scaling.py`**  
Applies feature scaling to numerical columns. Supports min-max normalization (scaling to the 0–1 range) and standard (z-score) scaling using scikit-learn's `MinMaxScaler` and `StandardScaler`.

**`backend/app/services/data_cleaning/encoding.py`**  
Converts categorical columns to binary indicator variables using pandas `get_dummies()` (one-hot encoding). Returns the expanded DataFrame with original categorical columns replaced.

**`backend/app/services/modeling/model_trainer.py`**  
Trains machine learning models using scikit-learn and XGBoost. Supports logistic regression, random forest, and XGBoost classifier. Splits data into training and test sets, fits the selected model, and returns a model identifier along with performance metrics and feature importance scores.

**`backend/app/services/modeling/hyperparameter_tuner.py`**  
Runs grid search cross-validation over a user-provided parameter grid using scikit-learn's `GridSearchCV`. Returns the best parameter combination and the corresponding cross-validated score.

**`backend/app/services/modeling/model_evaluator.py`**  
Evaluates a trained model against held-out test data. Computes accuracy, precision, recall, F1 score, ROC-AUC, and a confusion matrix. Returns all metrics in a serializable dictionary.

**`backend/app/services/modeling/explainability.py`**  
Extracts feature importance scores from a trained model. For tree-based models, uses the built-in `feature_importances_` attribute. Returns a ranked dictionary of feature names and their importance values.

**`backend/app/services/pipeline/workflow_engine.py`**  
Manages the execution lifecycle of a multi-step data processing pipeline. Maintains current pipeline state (idle, running, stopped) and coordinates step execution through the `StepExecutor`. Provides methods to start, stop, and check pipeline status.

**`backend/app/services/pipeline/step_executor.py`**  
Executes individual pipeline steps by name. Maps step names to the appropriate service function (ingest, explore, clean, model, visualize, report) and runs it with the provided parameters.

**`backend/app/services/reporting/pdf_generator.py`**  
Generates a formatted PDF report using the ReportLab library. Builds a document with section headings, data tables, and summary text from the provided JSON analysis data. Returns the PDF as a byte stream.

**`backend/app/services/reporting/csv_exporter.py`**  
Converts a data dictionary or DataFrame into a CSV file. Uses pandas to write the output and returns it as a downloadable stream.

---

### Frontend — Entry Point and Routing

**`frontend/src/index.jsx`**  
The React application root. Renders the `App` component into the HTML `div#root` element and wraps it in React's strict mode.

**`frontend/src/App.jsx`**  
Top-level component. Sets up React Router with all application routes: login, register, and all protected feature pages (ingestion, exploration, cleaning, modeling, visualization, reporting, pipeline, user management, help). Wraps all routes in the `AuthContext` provider.

**`frontend/src/index.css`**  
Global CSS styles and base layout rules applied across all components.

---

### Frontend — Context and Services

**`frontend/src/context/AuthContext.jsx`**  
React Context that holds the authenticated user object and JWT token. Provides login and logout functions. Persists the token to localStorage so sessions survive page refreshes. All components that need auth state consume this context.

**`frontend/src/services/api.js`**  
Axios HTTP client instance configured with the backend base URL from `VITE_API_URL`. Attaches the Authorization header with the stored JWT token automatically on every outgoing request. All API calls in the application go through this module.

**`frontend/src/services/auth.js`**  
Contains functions for making authentication-specific API calls: login, register, and fetch current user. Used by the login and register components.

**`frontend/src/utils/helpers.js`**  
General utility functions shared across components. Includes formatting helpers for dates, numbers, and strings used in tables and charts.

---

### Frontend — Components

**`frontend/src/components/Auth/ProtectedRoute.jsx`**  
A wrapper component that checks whether the user is authenticated before rendering the child route. If no token exists in the auth context, it redirects to the login page.

**`frontend/src/components/UserManagement/Login.jsx`**  
Login form built with Formik and Yup validation. Submits credentials to the auth service and stores the returned token in the auth context on success.

**`frontend/src/components/UserManagement/Register.jsx`**  
Registration form with fields for username, email, password, and role selection. Submits to the registration endpoint and redirects to login on success.

**`frontend/src/components/UserManagement/RoleManagement.jsx`**  
Admin-only panel for viewing and managing user roles. Visible only to accounts with the administrator role.

**`frontend/src/components/Layout/Header.jsx`**  
Top navigation bar showing the application name and the logged-in user's role. Includes a logout button that clears the auth context.

**`frontend/src/components/Layout/Sidebar.jsx`**  
Left navigation panel with links to all feature sections. Role-based rendering hides sections the current user does not have access to.

**`frontend/src/components/Layout/Footer.jsx`**  
Bottom bar with application name, version, and institutional information.

**`frontend/src/components/DataIngestion/FileUpload.jsx`**  
Drag-and-drop and manual file upload component. Validates the file type on the client side before submission and shows upload progress feedback.

**`frontend/src/components/DataIngestion/URLImport.jsx`**  
Input form for providing a URL to a remote dataset. Submits to the URL import endpoint and displays a success or error message.

**`frontend/src/components/DataExploration/SummaryStatistics.jsx`**  
Displays descriptive statistics returned from the backend in a formatted table. Shows mean, median, standard deviation, min, max, and null counts per column.

**`frontend/src/components/DataExploration/DataTable.jsx`**  
Paginated data table that displays the raw rows of an uploaded dataset. Supports sorting by column.

**`frontend/src/components/DataExploration/CorrelationMatrix.jsx`**  
Renders a Plotly heatmap showing the correlation matrix for the dataset's numerical columns.

**`frontend/src/components/DataCleaning/ImputationPanel.jsx`**  
Form for selecting imputation strategy, scaling method, and encoding method. Submits all selected cleaning options in a single request.

**`frontend/src/components/DataCleaning/OutlierDetection.jsx`**  
Panel for toggling outlier detection. Displays the number of rows removed and previews the cleaned dataset.

**`frontend/src/components/DataCleaning/PreprocessingHistory.jsx`**  
Shows a log of cleaning operations applied to the current dataset in the current session.

**`frontend/src/components/Modeling/ModelSelection.jsx`**  
Dropdown and configuration form for choosing a model type, selecting feature columns and the target column, and submitting a training request. Displays accuracy metrics after training.

**`frontend/src/components/Modeling/HyperparameterTuning.jsx`**  
UI for entering a parameter grid and submitting a tuning request. Displays the best parameter set and score returned by the backend.

**`frontend/src/components/Modeling/FeatureImportance.jsx`**  
Bar chart showing feature importance scores for the trained model using Chart.js.

**`frontend/src/components/Visualization/Dashboard.jsx`**  
Aggregated metrics dashboard showing key statistics and charts for the selected dataset. Uses a grid layout from Material-UI.

**`frontend/src/components/Visualization/ChartBuilder.jsx`**  
Interactive chart builder that lets users select chart type and axis columns to build custom Plotly visualizations.

**`frontend/src/components/Visualization/RiskGauge.jsx`**  
Displays a react-gauge-chart visualization showing the hypertension risk score for the current dataset. Color-coded from low to high risk.

**`frontend/src/components/Reporting/ReportGenerator.jsx`**  
Form for selecting report content and triggering PDF generation. Shows a preview area where the generated report is presented before download.

**`frontend/src/components/Reporting/ExportOptions.jsx`**  
Buttons for downloading the current dataset or analysis results as a CSV file.

**`frontend/src/components/Pipeline/PipelineControls.jsx`**  
Control panel for starting, stopping, and monitoring a pipeline run. Displays the current step and overall status.

**`frontend/src/components/Pipeline/WorkflowVisualizer.jsx`**  
A visual representation of the pipeline steps showing each stage as a node in a horizontal flow diagram. Steps are highlighted as they complete.

**`frontend/src/components/Help/Help.jsx`**  
Help and documentation page explaining each feature of the application in plain language for non-technical users.

---

### Database and Infrastructure

**`database/migrations/init_schema.sql`**  
DDL script that drops and recreates the five production tables: `users`, `datasets`, `models`, `reports`, and `pipeline_steps`. Run once against the managed PostgreSQL instance on first deployment.

**`database/seeds/sample_users.sql`**  
SQL INSERT statements that create three test accounts: admin, a clinician (john_doe), and a data analyst (jane_smith). Used for initial testing.

**`docker/docker-compose.yml`**  
Docker Compose configuration orchestrating three services: the React frontend on port 3000, the FastAPI backend on port 8000, and a PostgreSQL 15 database on port 5432. Used for local development and testing.

**`docker/Dockerfile.backend`**  
Dockerfile for the Python backend. Installs dependencies from `requirements.txt` and starts the Uvicorn server.

**`docker/Dockerfile.frontend`**  
Dockerfile for the React frontend. Runs `npm install` and `npm run build` to produce the static site.

**`render.yaml`**  
Render.com deployment configuration. Defines the backend web service as a Python application running in the Oregon region, with `DATABASE_URL` and `SECRET_KEY` as injected environment variables.

**`backend/requirements.txt`**  
Python dependency manifest listing all required packages with pinned versions including FastAPI, SQLAlchemy, scikit-learn, XGBoost, ReportLab, pandas, NumPy, and related libraries.

**`frontend/package.json`**  
Node.js dependency manifest listing all required packages including React, Vite, Axios, Material-UI, Chart.js, Plotly.js, Formik, and testing libraries.

---

## Section 3: Implementation Plan

### Strategy

The implementation followed an iterative approach. The backend API was built and verified first, then the frontend was developed to consume it. This order was chosen because all frontend features depend on having stable API contracts to work against. Docker Compose was used throughout local development to run all three tiers simultaneously without environment configuration drift.

The system was built in five layers: the database schema, the ORM models, the service layer, the API endpoints, and finally the frontend components. Each layer was tested before the next was started.

### Software and Library Integration

The following external software was integrated:

| Integration | Purpose |
|---|---|
| PostgreSQL 15 | Production relational database for all persistent data |
| SQLAlchemy 2.0 | Object-relational mapping between Python classes and database tables |
| FastAPI 0.104 | REST API framework providing automatic Swagger UI documentation |
| Uvicorn | ASGI server that runs the FastAPI application |
| scikit-learn 1.3 | Logistic regression, random forest, GridSearchCV, and preprocessing tools |
| XGBoost 2.0 | Gradient boosting classifier for predictive modeling |
| ReportLab 4.0 | PDF document generation from structured data |
| pandas 2.1 | In-memory data manipulation for all data processing operations |
| React 18 + Vite | Frontend framework and build tool |
| Axios 1.3 | HTTP client for API communication from the frontend |
| Chart.js 4.2 + Plotly.js 2.18 | Charting libraries for visualizations |
| Material-UI 5.11 | Component library providing layout, forms, and tables |
| python-jose | JWT token signing and verification |
| passlib + bcrypt | Password hashing and verification |

### Deployment as an Operational System

The system is deployed across two cloud platforms:

**Backend on Render.com:** The FastAPI application runs as a Python web service on Render's free tier in the Oregon region. Render reads the `render.yaml` configuration from the repository and builds the backend by installing `requirements.txt`, then starts the server with `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. A managed PostgreSQL 15 instance is connected through the `DATABASE_URL` environment variable. Render handles TLS termination, so all traffic is served over HTTPS. New deployments are triggered automatically whenever code is pushed to the `main` branch on GitHub.

**Frontend on Vercel:** The React application is deployed as a static site. Vercel runs `npm run build`, takes the output from the `dist` directory, and distributes it globally through its edge network. The `VITE_API_URL` environment variable is set in the Vercel project settings to point to the Render backend. Vercel also triggers automatic redeployment on every push to `main`.

### Potential Impacts and Risk Mitigation

| Risk | Impact | Mitigation |
|---|---|---|
| Render free tier cold start | 30 to 60 second delay on first request after idle period | Navigate to `/docs` before evaluation to wake the service |
| File persistence on Render | Uploaded files may be lost on service restart | Files are read into memory and processed; metadata stored in PostgreSQL |
| Synchronous ML training | Long training jobs block the request thread | Free-tier acceptable for academic use; Render Starter tier removes timeout constraint |
| Database connection loss | API returns 500 errors until reconnected | SQLAlchemy connection pooling recovers automatically; Render managed DB has uptime SLA |
| CORS misconfiguration | Frontend cannot reach backend from new domain | `allow_origins=["*"]` is configured; production would restrict to known origins |

### Activities Completed

1. Database schema designed and implemented in `init_schema.sql`
2. SQLAlchemy ORM models created for `users`, `datasets`, and `pipeline_steps`
3. Core security layer built with bcrypt password hashing and JWT token management
4. All eight API route groups implemented with Pydantic request and response validation
5. Service layer implemented with separate modules for each domain area
6. React frontend built with 30+ components organized by feature area
7. Authentication flow implemented end-to-end with context-based state management
8. Docker Compose configuration created for consistent local development
9. Render and Vercel deployment configurations finalized
10. Database seeded with four default users covering all three roles
11. End-to-end tests run with Playwright and pytest before production deployment
12. Both platforms deployed and verified against the operational readiness checklist

---

## Section 4: Project Requirements Review

### Review of Milestone 1 — Requirements and Design

The original system requirements identified five core capabilities: data ingestion, data exploration, predictive modeling, visualization, and reporting. All five have been fully implemented. An additional capability was added during implementation: the pipeline workflow system, which allows users to chain the five core stages into a single automated run. This addition was not in the original plan but emerged naturally from the need to support non-technical clinician users who benefit from a guided, sequential workflow rather than navigating each feature independently.

The role-based access system was also refined. The original design identified two roles (admin and user). Implementation expanded this to three distinct roles: administrator, clinician, and data analyst. This change better reflects the real-world stakeholders in a telehealth environment and allows the interface to be tailored more precisely to each user type.

### Review of Milestone 2 — Architecture and Database Design

The architecture planned in Milestone 2 described a three-tier system: frontend, backend, and database. This structure was implemented exactly as planned. The one notable deviation is the database engine: the original design specified PostgreSQL as the primary database, and while PostgreSQL is used in production, the development and testing environment defaults to SQLite. This was a pragmatic decision that simplified local development setup significantly without affecting production behavior, since SQLAlchemy abstracts the SQL dialect differences.

The five database tables defined in the migration script (`users`, `datasets`, `models`, `reports`, `pipeline_steps`) match the entity relationships described in the Milestone 2 data model. The `models` and `reports` tables use JSONB columns to store flexible parameter sets and result data without requiring schema changes every time a new model type or report format is introduced.

### Changes and Corrections

The following updates were made based on implementation findings:

- The `models` table was added to the production schema. It was described in Milestone 2 but not originally included in `init_schema.sql`. This was corrected during implementation.
- The frontend originally planned to use only Chart.js for all visualizations. During implementation, Plotly.js was added to handle interactive heatmaps for the correlation matrix, which Chart.js does not support natively.
- The `DataCleaningRequest` schema was extended to support all four cleaning operations in a single API call rather than requiring four separate requests. This reduced frontend complexity and improved the user experience.
- The help page (`Help.jsx`) was added as an unplanned component in response to feedback from informal user testing, which revealed that non-technical users needed in-application guidance on what each feature does.

### Current Status

All 21 functional requirements defined in Section 1 have been implemented and verified in the live deployment. The system is accessible from any modern browser, supports multiple simultaneous authenticated users, and covers the complete data science workflow from raw data import through report generation. The codebase is deployed on GitHub and connected to both Render and Vercel for continuous delivery.

---

## References

Géron, A. (2022). *Hands-on machine learning with Scikit-Learn, Keras, and TensorFlow* (3rd ed.). O'Reilly Media.

McKinney, W. (2022). *Python for data analysis* (3rd ed.). O'Reilly Media.

Ramirez, S. (2023). *FastAPI documentation*. https://fastapi.tiangolo.com

Render. (2024). *Render documentation: Web services*. https://render.com/docs/web-services

Vercel. (2024). *Vercel documentation: Deploying React applications*. https://vercel.com/docs

XGBoost Developers. (2024). *XGBoost documentation*. https://xgboost.readthedocs.io
