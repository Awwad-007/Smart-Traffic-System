-- Create the Database
CREATE DATABASE IF NOT EXISTS SmartTrafficDB;
USE SmartTrafficDB;

-- Table for Traffic Signals
CREATE TABLE Signals (
    signal_id INT PRIMARY KEY AUTO_INCREMENT,
    location_name VARCHAR(100) NOT NULL,
    current_state ENUM('RED', 'YELLOW', 'GREEN') DEFAULT 'RED',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);