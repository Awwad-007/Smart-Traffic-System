USE SmartTrafficDB;

-- 1. This adds vehicles ONLY if they aren't already there
INSERT IGNORE INTO vehicles (license_plate, vehicle_type) 
VALUES 
('KA-01-HH-1234', 'PRIVATE'),
('KA-03-EM-911', 'EMERGENCY'),
('KA-05-B-5555', 'BUS');

-- 2. This links a vehicle to a signal (Creating a "Log")
-- We are saying: Vehicle 2 (Emergency) just passed Signal 1 (Silk Board)
INSERT INTO trafficlogs (signal_id, vehicle_id) 
VALUES (1, 2);

-- 3. Now, let's see EVERYTHING combined
SELECT 
    v.license_plate, 
    v.vehicle_type, 
    s.location_name, 
    l.passing_time
FROM trafficlogs l
JOIN vehicles v ON l.vehicle_id = v.vehicle_id
JOIN signals s ON l.signal_id = s.signal_id;

USE SmartTrafficDB;

SELECT location_name, current_state FROM signals WHERE signal_id = 1;
INSERT INTO trafficlogs (signal_id, vehicle_id) VALUES (1, 2);
SELECT location_name, current_state FROM signals WHERE signal_id = 1;