import pytest

@pytest.fixture
def client():
    from fastapi.testclient import TestClient
    from app.main import app
    return TestClient(app)

def test_upload_valid_file(client):
    response = client.post("/api/data-ingestion/upload", files={"file": ("test.csv", b"col1,col2\n1,2\n3,4")})
    assert response.status_code == 200
    assert response.json() == {"message": "File uploaded successfully", "filename": "test.csv"}

def test_upload_invalid_file_type(client):
    response = client.post("/api/data-ingestion/upload", files={"file": ("test.txt", b"invalid content")})
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid file type"}

def test_upload_empty_file(client):
    response = client.post("/api/data-ingestion/upload", files={"file": ("empty.csv", b"")})
    assert response.status_code == 400
    assert response.json() == {"detail": "File is empty"}

def test_import_data_from_url(client):
    response = client.post("/api/data-ingestion/url", json={"url": "http://example.com/data.csv"})
    assert response.status_code == 200
    assert response.json() == {"message": "Data imported successfully from URL"}

def test_import_data_from_invalid_url(client):
    response = client.post("/api/data-ingestion/url", json={"url": "http://invalid-url"})
    assert response.status_code == 400
    assert response.json() == {"detail": "Failed to fetch data from URL"}