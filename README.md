# Telehealth Hypertension Predictive Analytics System

## Overview

The Telehealth Hypertension Predictive Analytics System is a web-based application designed to assist healthcare professionals in managing chronic hypertension among adults through predictive analytics. This system enables users to ingest, explore, clean, analyze, and visualize healthcare data effectively.

## Project Structure

The project is organized into two main components: the frontend and the backend.

### Frontend

The frontend is built using React and provides a user-friendly interface for interacting with the system. Key components include:

- **Data Ingestion**: Components for uploading files and importing data from URLs.
- **Data Exploration**: Tools for displaying summary statistics, data tables, and correlation matrices.
- **Data Cleaning**: Options for handling missing data and outliers.
- **Modeling**: Interfaces for selecting models and tuning hyperparameters.
- **Visualization**: Components for creating charts and dashboards.
- **Reporting**: Tools for generating and exporting reports.
- **Pipeline Management**: Visualizers and controls for managing the analytic workflow.
- **User Management**: Interfaces for user login and role management.

### Backend

The backend is built using Python and FastAPI, providing API endpoints for all functionalities. Key components include:

- **API Endpoints**: For data ingestion, exploration, cleaning, modeling, visualization, reporting, and user authentication.
- **Services**: Functions for handling data processing, model training, and report generation.
- **Database**: A PostgreSQL database for storing user data and processed datasets.

## Installation

To set up the project locally, follow these steps:

1. Clone the repository:
   ```
   git clone <repository-url>
   cd telehealth-hypertension-analytics
   ```

2. Set up the backend:
   - Navigate to the `backend` directory.
   - Install dependencies:
     ```
     pip install -r requirements.txt
     ```
   - Run the backend server:
     ```
     uvicorn app.main:app --reload
     ```

3. Set up the frontend:
   - Navigate to the `frontend` directory.
   - Install dependencies:
     ```
     npm install
     ```
   - Run the frontend application:
     ```
     npm run dev
     ```

## Usage

Once both the frontend and backend are running, access the application through your web browser at `http://localhost:3000`. Users can upload data files, explore datasets, apply data cleaning methods, build models, visualize results, and generate reports.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgments

- Special thanks to the contributors and the community for their support in developing this project.

# Sample login
 Run the Python seed script
  cd backend
  source venv/bin/activate
  python scripts/seed_users.py

 Login Credentials

  | Username  | Password   |
  |-----------|------------|
  | admin     | admin123   |
  | testuser  | test123    |
  | clinician | clinic123  |
  | analyst   | analyst123 |