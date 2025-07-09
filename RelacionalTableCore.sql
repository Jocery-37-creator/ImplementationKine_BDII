CREATE EXTENSION IF NOT EXISTS pgcrypto;
-- ============================================
-- Tabla: User
-- ============================================
CREATE TABLE "user" (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    full_name VARCHAR(100) NOT NULL,
    ID_document VARCHAR(15) NOT NULL UNIQUE,
    phone VARCHAR(10) NOT NULL UNIQUE,
    email TEXT NOT NULL UNIQUE,
    country_of_residence VARCHAR(50),
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(15) NOT NULL CHECK (status IN ('active', 'inactive'))
);

-- ============================================
-- Tabla: Authentication
-- ============================================
CREATE TABLE "authentication" (
    auth_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL,
    PIN INT NOT NULL CHECK (PIN BETWEEN 0 AND 9999),
    FOREIGN KEY (user_id) REFERENCES "user"(user_id) ON DELETE CASCADE
);

-- ============================================
-- Tabla: Device
-- ============================================
CREATE TABLE "device" (
    device_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_used TIMESTAMP,
    status VARCHAR(15) NOT NULL CHECK (status IN ('active', 'inactive', 'blocked')),
    FOREIGN KEY (user_id) REFERENCES "user"(user_id) ON DELETE CASCADE
);

-- ============================================
-- Tabla: Account
-- ============================================
CREATE TABLE "account" (
    account_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL UNIQUE,
    type_account VARCHAR(20) NOT NULL CHECK (type_account IN ('low_amount', 'savings')),
    balance NUMERIC(15, 2) DEFAULT 0 CHECK (balance >= 0),
    monthly_limit NUMERIC(15,2) CHECK (monthly_limit >= 0),
    status VARCHAR(15) NOT NULL CHECK (status IN ('active', 'inactive', 'blocked')),
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    exempt_4x1000 BOOLEAN DEFAULT FALSE,
    FOREIGN KEY (user_id) REFERENCES "user"(user_id) ON DELETE CASCADE
);

-- ============================================
-- Tabla: Movement
-- ============================================
CREATE TABLE "movement" (
    movement_id serial PRIMARY KEY,
    source_account_id UUID NOT NULL,
    amount NUMERIC(15,2) NOT NULL CHECK (amount >= 0),
    date_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(15) NOT NULL CHECK (status IN ('pending', 'completed', 'failed')),
    type_movement VARCHAR(20) NOT NULL CHECK (type_movement IN ('transfer', 'withdrawal', 'bill_payment', 'credit')),
    reference VARCHAR(50),
    FOREIGN KEY (source_account_id) REFERENCES "account"(account_id) ON DELETE CASCADE
);

-- ============================================
-- Tabla: Transfer
-- ============================================
CREATE TABLE "transfer" (
    movement_id integer PRIMARY KEY,
    associated_account_id UUID NOT NULL,
    type_transfer VARCHAR(15) NOT NULL CHECK (type_transfer IN ('internal', 'external')),
    FOREIGN KEY (movement_id) REFERENCES "movement"(movement_id) ON DELETE CASCADE,
    FOREIGN KEY (associated_account_id) REFERENCES "account"(account_id) ON DELETE CASCADE
);

-- ============================================
-- Tabla: Withdrawal
-- ============================================
CREATE TABLE "withdrawal" (
    movement_id integer PRIMARY KEY,
    channel VARCHAR(30) NOT NULL CHECK (channel IN ('ATM', 'branch', 'corresponsal', 'online')),
    FOREIGN KEY (movement_id) REFERENCES "movement"(movement_id) ON DELETE CASCADE
);

-- ============================================
-- Tabla: BillPayment
-- ============================================
CREATE TABLE "billPayment" (
    movement_id integer PRIMARY KEY,
    service_company VARCHAR(100) NOT NULL,
    reference_number VARCHAR(50) NOT NULL,
    FOREIGN KEY (movement_id) REFERENCES "movement"(movement_id) ON DELETE CASCADE
);

-- ============================================
-- Tabla: Credit
-- ============================================
CREATE TABLE "credit" (
    movement_id integer PRIMARY KEY,
    credit_type VARCHAR(20) NOT NULL CHECK (credit_type IN ('lifeline', 'booster')),
    interest NUMERIC(5,2) NOT NULL CHECK (interest >= 0),
    due_date DATE NOT NULL,
    credit_status VARCHAR(20) NOT NULL CHECK (credit_status IN ('approved', 'pending', 'rejected')),
    FOREIGN KEY (movement_id) REFERENCES "movement"(movement_id) ON DELETE CASCADE
);

-- ============================================
-- Tabla: Pocket
-- ============================================
CREATE TABLE "pocket" (
    pocket_id serial PRIMARY KEY,
    account_id UUID NOT NULL,
    name_pocket VARCHAR(50) NOT NULL,
    balance NUMERIC(15,2) DEFAULT 0 CHECK (balance >= 0),
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_goal BOOLEAN NOT NULL DEFAULT FALSE,
    goal NUMERIC(15,2) CHECK (goal >= 0),
    regularity VARCHAR(20) CHECK (regularity IN ('daily', 'weekly', 'biweekly', 'monthly')),
    quota NUMERIC(15,2) CHECK (quota >= 0),
    FOREIGN KEY (account_id) REFERENCES "account"(account_id) ON DELETE CASCADE
);

-- ============================================
-- Tabla: Cushion
-- ============================================
CREATE TABLE "cushion" (
    cushion_id serial PRIMARY KEY,
    account_id UUID NOT NULL UNIQUE,
    balance NUMERIC(15,2) DEFAULT 0 CHECK (balance >= 0),
    is_locked BOOLEAN DEFAULT FALSE,
    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (account_id) REFERENCES "account"(account_id) ON DELETE CASCADE
);

-- ============================================
-- Tabla: Card
-- ============================================
CREATE TABLE "card" (
    card_id serial PRIMARY KEY,
    account_id UUID NOT NULL UNIQUE,
    card_number VARCHAR(20) NOT NULL UNIQUE,
    expiry_date DATE NOT NULL,
    status VARCHAR(15) NOT NULL CHECK (status IN ('active', 'inactive', 'cancelled')),
	FOREIGN KEY (account_id) REFERENCES "account"(account_id) ON DELETE CASCADE
);
