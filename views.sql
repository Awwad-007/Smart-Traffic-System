CREATE DATABASE IF NOT EXISTS SmartTrafficDB;
USE SmartTrafficDB;

-- 1. Create Tables
CREATE TABLE IF NOT EXISTS signals (
    signal_id INT PRIMARY KEY AUTO_INCREMENT,
    location_name VARCHAR(100),
    current_state VARCHAR(10) DEFAULT 'RED'
);

CREATE TABLE IF NOT EXISTS trafficlogs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    signal_id INT,
    vehicle_id INT,
    passing_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (signal_id) REFERENCES signals(signal_id)
);

-- 2. Create the View for the Web Dashboard
CREATE OR REPLACE VIEW traffic_dashboard AS
SELECT 
    s.signal_id AS ID,
    s.location_name AS Junction,
    s.current_state AS Signal_Status,
    COUNT(l.log_id) AS Vehicles_Passed
FROM signals s
LEFT JOIN trafficlogs l ON s.signal_id = l.signal_id
GROUP BY s.signal_id;

-- 3. The PRO Feature: Stored Procedure
DELIMITER //
CREATE PROCEDURE IF NOT EXISTS ForceEmergencyGreen(IN target_id INT)
BEGIN
    UPDATE signals SET current_state = 'GREEN' WHERE signal_id = target_id;
    UPDATE signals SET current_state = 'RED' WHERE signal_id != target_id;
    INSERT INTO trafficlogs (signal_id, vehicle_id) VALUES (target_id, 911);
END //
DELIMITER ;

-- 4. Initial Data
INSERT IGNORE INTO signals (signal_id, location_name, current_state) 
VALUES (1, 'Silk Board Junction', 'RED'), (2, 'Indiranagar 100ft Rd', 'GREEN');