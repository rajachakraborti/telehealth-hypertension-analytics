DROP TABLE IF EXISTS pipeline_steps CASCADE;
DROP TABLE IF EXISTS reports CASCADE;
DROP TABLE IF EXISTS models CASCADE;
DROP TABLE IF EXISTS datasets CASCADE;
DROP TABLE IF EXISTS users CASCADE;



CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    role VARCHAR(20) NOT NULL, -- <-- Add this line
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE
);

CREATE TABLE datasets (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    dataset_name VARCHAR(100) NOT NULL,
    file_path VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE models (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    model_name VARCHAR(100) NOT NULL,
    model_type VARCHAR(50) NOT NULL,
    parameters JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE reports (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id),
    report_name VARCHAR(100) NOT NULL,
    report_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE pipeline_steps (
    id SERIAL PRIMARY KEY,
    pipeline_id INT,
    step_name VARCHAR(100) NOT NULL,
    step_order INT NOT NULL,
    parameters JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);