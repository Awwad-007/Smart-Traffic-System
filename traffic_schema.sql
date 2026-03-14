USE SmartTrafficDB;

-- Clear previous test commands
-- Add actual data
INSERT INTO signals (location_name, current_state) 
VALUES ('Silk Board Junction', 'RED'), ('Indiranagar 100ft Rd', 'GREEN');

-- See the data
SELECT * FROM signals;