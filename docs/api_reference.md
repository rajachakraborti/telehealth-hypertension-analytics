# API Reference for Telehealth Hypertension Predictive Analytics System

## Overview

This document provides a comprehensive reference for the API endpoints available in the Telehealth Hypertension Predictive Analytics System. Each section outlines the purpose of the endpoint, the HTTP method used, the required parameters, and the expected responses.

---

## Authentication

### Login
- **Endpoint:** `/api/auth/login`
- **Method:** POST
- **Description:** Authenticates a user and returns a JWT token.
- **Request Body:**
  - `username`: string (required)
  - `password`: string (required)
- **Response:**
  - **200 OK**
    - `token`: string
  - **401 Unauthorized**
    - `message`: string

---

## Data Ingestion

### Upload Data File
- **Endpoint:** `/api/data_ingestion/upload`
- **Method:** POST
- **Description:** Uploads a data file for processing.
- **Request Body:**
  - `file`: file (required)
- **Response:**
  - **200 OK**
    - `message`: string
    - `data_id`: string
  - **400 Bad Request**
    - `message`: string

### Import Data from URL
- **Endpoint:** `/api/data_ingestion/url`
- **Method:** POST
- **Description:** Imports data from a specified URL.
- **Request Body:**
  - `url`: string (required)
- **Response:**
  - **200 OK**
    - `message`: string
    - `data_id`: string
  - **400 Bad Request**
    - `message`: string

---

## Data Exploration

### Get Summary Statistics
- **Endpoint:** `/api/data_exploration/statistics`
- **Method:** GET
- **Description:** Retrieves summary statistics for the ingested data.
- **Query Parameters:**
  - `data_id`: string (required)
- **Response:**
  - **200 OK**
    - `statistics`: object
  - **404 Not Found**
    - `message`: string

### Get Data Table
- **Endpoint:** `/api/data_exploration/data_table`
- **Method:** GET
- **Description:** Retrieves the data in a tabular format.
- **Query Parameters:**
  - `data_id`: string (required)
- **Response:**
  - **200 OK**
    - `data`: array
  - **404 Not Found**
    - `message`: string

---

## Data Cleaning

### Apply Data Cleaning Methods
- **Endpoint:** `/api/data_cleaning/apply`
- **Method:** POST
- **Description:** Applies specified data cleaning methods to the dataset.
- **Request Body:**
  - `data_id`: string (required)
  - `methods`: array of strings (required)
- **Response:**
  - **200 OK**
    - `message`: string
  - **400 Bad Request**
    - `message`: string

---

## Modeling

### Train Model
- **Endpoint:** `/api/modeling/train`
- **Method:** POST
- **Description:** Trains a model using the specified parameters.
- **Request Body:**
  - `data_id`: string (required)
  - `model_type`: string (required)
  - `parameters`: object (optional)
- **Response:**
  - **200 OK**
    - `model_id`: string
  - **400 Bad Request**
    - `message`: string

### Get Model Evaluation
- **Endpoint:** `/api/modeling/evaluate`
- **Method:** GET
- **Description:** Retrieves evaluation metrics for a trained model.
- **Query Parameters:**
  - `model_id`: string (required)
- **Response:**
  - **200 OK**
    - `metrics`: object
  - **404 Not Found**
    - `message`: string

---

## Visualization

### Get Visualization Data
- **Endpoint:** `/api/visualization/data`
- **Method:** GET
- **Description:** Retrieves data for visualization.
- **Query Parameters:**
  - `data_id`: string (required)
- **Response:**
  - **200 OK**
    - `visualization_data`: object
  - **404 Not Found**
    - `message`: string

---

## Reporting

### Generate Report
- **Endpoint:** `/api/reporting/generate`
- **Method:** POST
- **Description:** Generates a report based on the analysis performed.
- **Request Body:**
  - `data_id`: string (required)
  - `report_type`: string (required)
- **Response:**
  - **200 OK**
    - `report_url`: string
  - **400 Bad Request**
    - `message`: string

---

## Pipeline Management

### Execute Pipeline
- **Endpoint:** `/api/pipeline/execute`
- **Method:** POST
- **Description:** Executes the analytic pipeline.
- **Request Body:**
  - `pipeline_id`: string (required)
- **Response:**
  - **200 OK**
    - `status`: string
  - **400 Bad Request**
    - `message`: string

---

## Conclusion

This API reference provides a detailed overview of the endpoints available in the Telehealth Hypertension Predictive Analytics System. For further information, please refer to the technical documentation or contact the development team.