USE SmartTrafficDB;

-- Change the delimiter so MySQL doesn't get confused by the semicolons inside the trigger
DELIMITER //

CREATE TRIGGER priority_clearance
AFTER INSERT ON trafficlogs
FOR EACH ROW
BEGIN
    -- If the vehicle that just passed is an ambulance/fire truck
    IF (SELECT vehicle_type FROM vehicles WHERE vehicle_id = NEW.vehicle_id) = 'EMERGENCY' THEN
        -- Force the signal to GREEN immediately
        UPDATE signals 
        SET current_state = 'GREEN' 
        WHERE signal_id = NEW.signal_id;
    END IF;
END;
//

DELIMITER ;
