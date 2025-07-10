-- ============================================
-- QUERY PROPOSALS
-- ============================================


-- User Registration and Authentication

--Query to verify if the user is already registered by document or phone number.
SELECT user_id, ID_document, phone
FROM "user"
WHERE id_document = '[DOCUMENT]' OR phone = '[PHONE_NUMBER]';

--Query to retrieve the user's credentials (PIN and biometrics) from the Authentication entity.
SELECT PIN 
FROM authentication
WHERE user_id = '[USER_ID]';

--Query to retrieve all devices associated with the user, including their status and usage dates.
SELECT device_id, registration_date, last_used, status
FROM device
WHERE user_id = '[USER_ID]';


-- Balance Inquiry and Account Movements

--Query to retrieve the current balance and status (active or blocked) of the account.
SELECT balance, status
FROM account
WHERE account_id = '[ACCOUNT_ID]';

--Query to retrieve the account's transaction history over a specific period.
SELECT movement_id, amount, date_time, type_movement, status, reference
FROM movement
WHERE source_account_id = '[ACCOUNT_ID]'
AND date_time BETWEEN '[2025-05-01]' AND '[2025-06-30]'
ORDER BY date_time DESC;


-- Money Transfers

--Query to verify the available balance before making a transfer.
SELECT balance
FROM account
WHERE account_id = '[ACCOUNT_ID]';

--Query to retrieve the recipient's name and account status in a Nequi-to-Nequi transfer.
SELECT u.full_name, a.status
FROM "user"
JOIN account a ON u.user_id = a.user_id
WHERE a.account_id = '[DESTINATION_ACCOUNT_ID]';

--Query to display transfers made or received, useful for the user interface.
SELECT movement_id, amount, date_time, reference
FROM movement
WHERE source_account_id = '[ACCOUNT_ID]'
AND type_movement = 'transfer'
ORDER BY date_time DESC;


-- Payments to Merchants and Services

--Query to retrieve payments made to public services, along with their reference.
SELECT m.movement_id, m.amount, m.date_time, m.reference, bp.service_company
FROM movement m
JOIN billPayment bp ON m.movement_id = bp.movement_id
WHERE m.source_account_id = '[ACCOUNT_ID]'
ORDER BY m.date_time DESC;


-- Expense Management with Pockets and Cushion

--Query to check the amount stored in the cushion and whether it is locked.
SELECT balance, is_locked
FROM cushion
WHERE account_id = '[ACCOUNT_ID]';



