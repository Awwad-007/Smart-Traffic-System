USE SmartTrafficDB;

-- 1. Create the View (The Report)
CREATE OR REPLACE VIEW traffic_dashboard AS
SELECT 
    s.location_name AS Junction,
    s.current_state AS Signal_Status,
    COUNT(l.log_id) AS Vehicles_Passed
FROM signals s
LEFT JOIN trafficlogs l ON s.signal_id = l.signal_id
GROUP BY s.signal_id;

-- 2. Add Sample Data (So the table isn't empty)
INSERT IGNORE INTO signals (signal_id, location_name, current_state) 
VALUES (1, 'Silk Board Junction', 'RED'), (2, 'Indiranagar Junction', 'GREEN');

-- 3. Simulate one vehicle
INSERT INTO trafficlogs (signal_id, vehicle_id) VALUES (1, 101);