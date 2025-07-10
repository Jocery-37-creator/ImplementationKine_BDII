import psycopg2
from faker import Faker
import random
import time
from datetime import datetime, timedelta

# Database connection settings
conn = psycopg2.connect(
    dbname='KineDataBase',
    user='postgres',
    password='1234567',
    host='localhost',
    port='5432'
)

cursor = conn.cursor()
faker = Faker('es_CO')

# Get all available account_id's
cursor.execute('SELECT account_id FROM account')
accounts = [row[0] for row in cursor.fetchall()]

# Simulation parameters
TOTAL = 463 #Transactions per minute in Nequi's app
types = ['transfer', 'withdrawal', 'bill_payment', 'credit']
statuses = ['completed', 'pending', 'failed']
channels = ['ATM', 'branch', 'corresponsal', 'online']
credit_statuses = ['approved', 'pending', 'rejected']
service_companies = ['ElectricCo', 'WaterCorp', 'InternetSA', 'GasLtd']

# Function to generate and execute a complete transaction
def insert_movement_with_detail():
    source_acc = random.choice(accounts)
    # Generate common data
    amount = round(random.uniform(1000, 5000000), 2)
    status = random.choices(statuses, weights=[0.85, 0.10, 0.05])[0]
    type_movement = random.choice(types)
    reference = faker.bothify(text='Trans###???')
    random_datetime = faker.date_time_between(start_date='-6M', end_date='now')

    # Insertion into Movement with RETURNING
    cursor.execute("""
        INSERT INTO movement (source_account_id, amount, date_time, status, type_movement, reference)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING movement_id
    """, (source_acc, amount, random_datetime, status, type_movement, reference))
    mov_id = cursor.fetchone()[0]

    # Insertion into the corresponding child table
    if type_movement == 'transfer':
        dest_acc = random.choice([acc for acc in accounts if acc != source_acc])
        type_transfer = random.choice(['internal', 'external'])
        cursor.execute("""
            INSERT INTO transfer (movement_id, associated_account_id, type_transfer)
            VALUES (%s, %s, %s)
        """, (mov_id, dest_acc, type_transfer))

    elif type_movement == 'withdrawal':
        channel = random.choice(channels)
        cursor.execute("""
            INSERT INTO "withdrawal" (movement_id, channel)
            VALUES (%s, %s)
        """, (mov_id, channel))

    elif type_movement == 'bill_payment':
        company = random.choice(service_companies)
        ref_num = faker.bothify(text='??-####-??')
        cursor.execute("""
            INSERT INTO "billPayment" (movement_id, service_company, reference_number)
            VALUES (%s, %s, %s)
        """, (mov_id, company, ref_num))

    elif type_movement == 'credit':
        interest = round(random.uniform(0.01, 0.2), 2)  # 1% to 20%
        due_date = (datetime.now() + timedelta(days=random.randint(30, 365))).date()
        credit_status = random.choice(credit_statuses)
        cursor.execute("""
            INSERT INTO "credit" (movement_id, credit_type, interest, due_date, credit_status)
            VALUES (%s, %s, %s, %s, %s)
        """, (mov_id, random.choice(['lifeline', 'booster']), interest, due_date, credit_status))

# Measure the insertion time for 463 complete transactions
start_time = time.time()

for _ in range(TOTAL):
    insert_movement_with_detail()

conn.commit()
elapsed = time.time() - start_time

print(f"Total time for {TOTAL} complete transactions: {elapsed:.4f} seconds")
if elapsed <= 1.0:
    print("PostgreSQL processed all complete transactions in ≤1 second")
else:
    print("It took more than 1 second")

cursor.close()
conn.close()