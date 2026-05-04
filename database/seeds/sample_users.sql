INSERT INTO users (username, email, hashed_password, role, is_active, is_superuser) VALUES
('admin', 'admin@example.com', 'hashed_password_1', 'administrator', TRUE, TRUE),
('john_doe', 'john.doe@example.com', 'hashed_password_2', 'clinician', TRUE, FALSE),
('jane_smith', 'jane.smith@example.com', 'hashed_password_3', 'data_analyst', TRUE, FALSE);