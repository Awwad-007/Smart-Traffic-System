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

-- Table for Vehicles
CREATE TABLE Vehicles (
    vehicle_id INT PRIMARY KEY AUTO_INCREMENT,
    license_plate VARCHAR(20) UNIQUE NOT NULL,
    vehicle_type ENUM('EMERGENCY', 'BUS', 'PRIVATE', 'COMMERCIAL') NOT NULL,
    entry_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table to log which vehicle passed which signal
CREATE TABLE TrafficLogs (
    log_id INT PRIMARY KEY AUTO_INCREMENT,
    signal_id INT,
    vehicle_id INT,
    passing_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (signal_id) REFERENCES Signals(signal_id),
    FOREIGN KEY (vehicle_id) REFERENCES Vehicles(vehicle_id)
);
