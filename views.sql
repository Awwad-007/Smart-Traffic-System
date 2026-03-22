USE SmartTrafficDB;

-- This creates a live dashboard view
CREATE OR REPLACE VIEW traffic_dashboard AS
SELECT 
    s.location_name AS Junction,
    s.current_state AS Signal_Status,
    COUNT(l.log_id) AS Vehicles_Passed,
    MAX(l.passing_time) AS Last_Activity
FROM signals s
LEFT JOIN trafficlogs l ON s.signal_id = l.signal_id
GROUP BY s.signal_id;

-- To see your new dashboard, just run:
SELECT * FROM traffic_dashboard;