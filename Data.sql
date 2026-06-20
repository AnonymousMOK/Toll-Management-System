BEGIN;

-- ==========================================
-- 1. EXCISE REGISTRY: Pakistani Citizens
-- ==========================================
INSERT INTO excise.owners (owner_id, full_name, national_id, phone_number) VALUES
('a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d', 'Ali Raza',       '42101-1111111-1', '+923001234567'),
('b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e', 'Fatima Ahmed',   '42201-2222222-2', '+923339876543'),
('c3d4e5f6-a7b8-9c0d-1e2f-3a4b5c6d7e8f', 'Kamran Khan',    '35202-3333333-3', '+923451122334'),
('d4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9a', 'Usman Tariq',    '42301-4444444-4', '+923129988776'),
('10000000-0000-0000-0000-000000000001', 'Kamran Akmal',  '42101-0000001-1', '+923001111111'),
('10000000-0000-0000-0000-000000000002', 'Shaheen Afridi','42101-0000002-2', '+923002222222'),
('10000000-0000-0000-0000-000000000003', 'Babar Azam',    '42101-0000003-3', '+923003333333'),
('10000000-0000-0000-0000-000000000004', 'Rizwan Ahmed',  '42101-0000004-4', '+923004444444'),
('10000000-0000-0000-0000-000000000005', 'Shadab Khan',   '42101-0000005-5', '+923005555555'),
('10000000-0000-0000-0000-000000000006', 'Fakhar Zaman',  '42101-0000006-6', '+923006666666'),
('10000000-0000-0000-0000-000000000007', 'Haris Rauf',    '42101-0000007-7', '+923007777777'),
('10000000-0000-0000-0000-000000000008', 'Imam Ul Haq',   '42101-0000008-8', '+923008888888'),
('10000000-0000-0000-0000-000000000009', 'Naseem Shah',   '42101-0000009-9', '+923009999999'),
('10000000-0000-0000-0000-000000000010', 'Abrar Ahmed',   '42101-0000010-0', '+923000000000');

-- ==========================================
-- 2. EXCISE REGISTRY: Local Vehicles
-- ==========================================
INSERT INTO excise.vehicles (plate_number, owner_id, make, model, registered_class, status) VALUES
('KHI-123', 'a1b2c3d4-e5f6-7a8b-9c0d-1e2f3a4b5c6d', 'Toyota', 'Corolla GLI', 'Car',        'Active'),
('LHR-456', 'b2c3d4e5-f6a7-8b9c-0d1e-2f3a4b5c6d7e', 'Suzuki', 'Alto VXR',    'Car',        'Active'),
('TKG-999', 'c3d4e5f6-a7b8-9c0d-1e2f-3a4b5c6d7e8f', 'Hino',   'Dutro Truck', 'Heavy_Axle', 'Active'),
('ISB-789', 'd4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f9a', 'Honda',  'Civic Oriel', 'Car',        'Stolen'),
('KHI-881', '10000000-0000-0000-0000-000000000001', 'Honda',   'Civic',   'Car',        'Active'),
('LHR-332', '10000000-0000-0000-0000-000000000002', 'Toyota',  'Hilux',   'Heavy_Axle', 'Active'),
('ISB-505', '10000000-0000-0000-0000-000000000003', 'Suzuki',  'Cultus',  'Car',        'Active'),
('RAW-911', '10000000-0000-0000-0000-000000000004', 'Kia',     'Sportage','Car',        'Active'),
('MUL-404', '10000000-0000-0000-0000-000000000005', 'Toyota',  'Corolla', 'Car',        'Active'),
('QTA-777', '10000000-0000-0000-0000-000000000006', 'Hyundai', 'Tucson',  'Car',        'Active'),
('PES-212', '10000000-0000-0000-0000-000000000007', 'Changan', 'Alsvin',  'Car',        'Active'),
('HYD-606', '10000000-0000-0000-0000-000000000008', 'Suzuki',  'WagonR',  'Car',        'Active'),
('SUK-111', '10000000-0000-0000-0000-000000000009', 'Honda',   'City',    'Car',        'Stolen'),
('FSD-808', '10000000-0000-0000-0000-000000000010', 'Toyota',  'Fortuner','Car',        'Stolen');

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
('TAG-PK-001', 'KHI-123', 5000.00, 'Active'),      
('TAG-PK-002', 'LHR-456',   20.00, 'Low_Balance'), 
('TAG-PK-003', 'TKG-999', 15000.00, 'Active'),     
('TAG-PK-101',     'KHI-881',  4500.00, 'Active'),     
('TAG-PK-102',     'LHR-332', 18000.00, 'Active'),     
('TAG-PK-103',     'ISB-505',    15.00, 'Low_Balance'),
('TAG-PK-104',     'RAW-911',     0.00, 'Low_Balance'),
('TAG-PIRATED-99', 'GHOST-00',  500.00, 'Active'),
('TAG-PK-110',     'FSD-808',  1200.00, 'Active');
COMMIT;