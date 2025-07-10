INSERT INTO "authentication" (auth_id, user_id, PIN) VALUES
(gen_random_uuid(), '', 4832),
(gen_random_uuid(), '', 1203);

INSERT INTO "device" (device_id, user_id, registration_date, last_used, status) VALUES
(gen_random_uuid(), '', CURRENT_TIMESTAMP - interval '90 days', CURRENT_TIMESTAMP - interval '2 days', 'active'),
(gen_random_uuid(), '', CURRENT_TIMESTAMP - interval '85 days', CURRENT_TIMESTAMP - interval '1 days', 'active');

INSERT INTO "cushion" (cushion_id, account_id, balance, is_locked, creation_date) VALUES 
(DEFAULT, '', 25000.00, FALSE, CURRENT_TIMESTAMP);

INSERT INTO "Pocket" (pocket_id, account_id, name_pocket, balance, creation_date, is_goal, goal, regularity, quota)
VALUES (DEFAULT, '', 'Vacaciones', 50000.00, CURRENT_TIMESTAMP, TRUE, 1000000.00, 'monthly', 200000.00);

INSERT INTO "Card" (card_id, account_id, card_number, expiry_date, status, issued_date)
VALUES (DEFAULT, '', '1234567890123456', '2027-06-30', 'active', CURRENT_TIMESTAMP);
