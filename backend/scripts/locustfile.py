from locust import HttpUser, task, between
import random

class TelehealthLoadTester(HttpUser):
    """
    Simulates high-concurrency patient monitoring devices pushing telemetry to the FastAPI backend.
    Specifically designed to measure the p95 latency overhead introduced by:
    1. OAuth2 JWT Validation (RBAC)
    2. PostgreSQL pgp_sym_encrypt (Data at Rest Encryption)
    This addresses Professor Pollyn's direct feedback regarding system performance bottlenecks.
    """
    
    # Wait between 1 and 3 seconds between simulated requests
    wait_time = between(1.0, 3.0)
    
    def on_start(self):
        """
        Executed when a simulated user starts. We authenticate once to get the JWT token.
        """
        response = self.client.post("/api/auth/login", data={
            "username": "clinician",
            "password": "clinician123"
        })
        if response.status_code == 200:
            self.token = response.json()["access_token"]
            self.headers = {"Authorization": f"Bearer {self.token}"}
        else:
            self.headers = {}
            print("Failed to authenticate simulated user.")

    @task(3)
    def test_explainability_latency(self):
        """
        Simulates a clinician requesting an AI explanation. 
        Tests the overhead of JWT decoding + XGBoost inference + SHAP computation.
        """
        payload = {
            "systolic": random.uniform(110.0, 160.0),
            "diastolic": random.uniform(70.0, 100.0),
            "map": random.uniform(70.0, 110.0),
            "pulse_pressure": random.uniform(30.0, 80.0),
            "is_night": random.choice([0, 1]),
            "is_dipper": random.choice([0, 1])
        }
        self.client.post("/api/modeling/explain", json=payload, headers=self.headers)
        
    @task(2)
    def test_database_encryption_latency(self):
        """
        Simulates registering a new patient into the system.
        Measures the p95 latency overhead of inserting row-level encrypted data (pgp_sym_encrypt).
        """
        # We append a random integer to the email to avoid the UNIQUE constraint failure on repeat tests
        rand_id = random.randint(1000, 9999999)
        payload = {
            "first_name": "Test",
            "last_name": f"User_{rand_id}",
            "ssn_last_four": str(random.randint(1000, 9999)),
            "contact_email": f"patient_{rand_id}@example.com",
            "date_of_birth": "1980-01-01"
        }
        self.client.post("/api/clinical/patients", json=payload, headers=self.headers)
        
    @task(1)
    def test_unauthorized_rejection(self):
        """
        Tests the API's ability to quickly reject unauthenticated requests 
        without crashing the server under load.
        """
        payload = {
            "systolic": 120.0,
            "diastolic": 80.0,
            "map": 93.3,
            "pulse_pressure": 40.0,
            "is_night": 0,
            "is_dipper": 1
        }
        # Intentionally omitting self.headers
        self.client.post("/api/modeling/explain", json=payload)
