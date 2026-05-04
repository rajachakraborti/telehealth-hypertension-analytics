-- SQL Script to seed users with bcrypt hashed passwords
-- Generated for Telehealth Hypertension Analytics System
--
-- Login credentials after running this script:
--   Username: admin       Password: admin123
--   Username: testuser    Password: test123
--   Username: clinician   Password: clinic123
--   Username: analyst     Password: analyst123

-- Create users table if it doesn't exist
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE,
    hashed_password VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    is_superuser BOOLEAN DEFAULT false
);

-- Clear existing users (uncomment if you want to reset)
-- DELETE FROM users;

-- Insert sample users with bcrypt hashed passwords
INSERT INTO users (username, email, hashed_password, is_active, is_superuser) VALUES
  ('admin', 'admin@example.com', '$2b$12$qSfEXQBUn8XleQmgQ1CihOv.fwckXFrpiFVJsJ/ztXG5mYiCXI7se', true, true)
ON CONFLICT (username) DO NOTHING;

INSERT INTO users (username, email, hashed_password, is_active, is_superuser) VALUES
  ('testuser', 'testuser@example.com', '$2b$12$i7ass4.4VB9F8bjQMyB/3uMrQwlSadn.kdZgPEhsIafgp5b6d2Xby', true, false)
ON CONFLICT (username) DO NOTHING;

INSERT INTO users (username, email, hashed_password, is_active, is_superuser) VALUES
  ('clinician', 'clinician@example.com', '$2b$12$iv2Mw5pjBzc1ZOmUT7U34.sTkWjR59MPDRE8osOR4cILhnCykkgCm', true, false)
ON CONFLICT (username) DO NOTHING;

INSERT INTO users (username, email, hashed_password, is_active, is_superuser) VALUES
  ('analyst', 'analyst@example.com', '$2b$12$yXSRcob6CJ29Z92EqT3xlOpiegTZ.CvIbBli1W.FwdA6xEzvH9Ppy', true, false)
ON CONFLICT (username) DO NOTHING;

-- Verify users were created
SELECT id, username, email, is_active, is_superuser FROM users;
