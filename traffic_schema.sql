-- 1. DATABASE SETUP
CREATE DATABASE IF NOT EXISTS SmartTrafficDB;
USE SmartTrafficDB;

-- 2. STRUCTURE (The Blueprint)
CREATE TABLE IF NOT EXISTS signals (
    signal_id INT PRIMARY KEY AUTO_INCREMENT,
    location_name VARCHAR(100) NOT NULL,
    current_state ENUM('RED', 'YELLOW', 'GREEN') DEFAULT 'RED',
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id INT PRIMARY KEY AUTO_INCREMENT,
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    vehicle_type ENUM('EMERGENCY', 'BUS', 'PRIVATE', 'COMMERCIAL') NOT NULL,
    entry_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS trafficlogs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    signal_id INT,
    vehicle_id INT,
    passing_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (signal_id) REFERENCES signals(signal_id),
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id)
);

-- 3. SAMPLE DATA (The Content)
INSERT IGNORE INTO signals (location_name, current_state) 
VALUES ('Silk Board Junction', 'RED'), ('Indiranagar 100ft Rd', 'GREEN');

-- 4. VERIFICATION
SELECT * FROM vehicles;