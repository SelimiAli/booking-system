-- Create the database
CREATE DATABASE IF NOT EXISTS booking_db;
USE booking_db;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    name VARCHAR(100) NOT NULL,
    date DATE NOT NULL,
    time TIME NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Insert some sample data
INSERT INTO users (username, password) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFrBtdZn3t3YiKe'); -- Password: admin123

INSERT INTO bookings (user_id, name, date, time) VALUES
(1, 'John Doe', '2025-11-08', '14:30:00'),
(1, 'Jane Smith', '2025-11-09', '10:00:00'),
(1, 'Bob Wilson', '2025-11-10', '16:45:00');