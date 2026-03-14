USE SmartTrafficDB;

SELECT 
    signals.location_name, 
    vehicles.license_plate, 
    vehicles.vehicle_type, 
    trafficlogs.passing_time
FROM trafficlogs
JOIN signals ON trafficlogs.signal_id = signals.signal_id
JOIN vehicles ON trafficlogs.vehicle_id = vehicles.vehicle_id;