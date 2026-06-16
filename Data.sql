BEGIN;

-- ==========================================
-- 1. EXCISE REGISTRY: Pakistani Citizens
-- ==========================================
INSERT INTO excise.owners (owner_id, full_name, national_id, phone_number) VALUES
('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d', 'Ali Raza',       '42101-1111111-1', '+923001234567'),
('b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e', 'Fatima Ahmed',   '42201-2222222-2', '+923339876543'),
('c3d4e5f6-a7b8-9c0d-1e2f-3a4b5c6d7e8f', 'Kamran Khan',    '35202-3333333-3', '+923451122334'),
('d4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9a', 'Usman Tariq',    '42301-4444444-4', '+923129988776');

-- ==========================================
-- 2. EXCISE REGISTRY: Local Vehicles
-- ==========================================
INSERT INTO excise.vehicles (plate_number, owner_id, make, model, registered_class, status) VALUES
('KHI-123', 'a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d', 'Toyota', 'Corolla GLI', 'Car',        'Active'),
('LHR-456', 'b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e', 'Suzuki', 'Alto VXR',    'Car',        'Active'),
('TKG-999', 'c3d4e5f6-a7b8-9c0d-1e2f-3a4b5c6d7e8f', 'Hino',   'Dutro Truck', 'Heavy_Axle', 'Active'),
('ISB-789', 'd4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9a', 'Honda',  'Civic Oriel', 'Car',        'Stolen'); -- TEST CASE: Stolen Vehicle

-- ==========================================
-- 3. TOLL INFRASTRUCTURE: Shahrah-e-Bhutto
-- ==========================================
INSERT INTO toll.plazas (plaza_id, plaza_name, location_gps) VALUES
(1, 'Shahrah-e-Bhutto North Toll Plaza', '24.8607, 67.0011'),
(2, 'Shahrah-e-Bhutto South Toll Plaza', '24.7954, 67.0423');

INSERT INTO toll.lanes (lane_id, plaza_id, lane_type, direction) VALUES
(101, 1, 'Automated_E_Tag_QR', 'Northbound'),
(102, 1, 'Manual_Cash',        'Northbound'),
(201, 2, 'Automated_E_Tag_QR', 'Southbound'),
(202, 2, 'Manual_Cash',        'Southbound');

-- ==========================================
-- 4. PAYMENT: E-Tags (M-Tag equivalents)
-- ==========================================
INSERT INTO payment.e_tags (e_tag_id, registered_plate, balance, status) VALUES
('TAG-PK-001', 'KHI-123', 5000.00, 'Active'),      -- Healthy balance
('TAG-PK-002', 'LHR-456',   20.00, 'Low_Balance'), -- Low balance (requires QR fallback)
('TAG-PK-003', 'TKG-999', 15000.00, 'Active');     -- Heavy commercial balance

COMMIT;