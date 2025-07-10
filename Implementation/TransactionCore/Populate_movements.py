import psycopg2
from faker import Faker
import random
import time
from datetime import datetime, timedelta

# Configuración de conexión a la base de datos
conn = psycopg2.connect(
    dbname='KineDataBase',
    user='postgres',
    password='1234567',
    host='localhost',
    port='5432'
)

cursor = conn.cursor()
faker = Faker('es_CO')

# Obtener todos los account_id disponibles
cursor.execute('SELECT account_id FROM account')
accounts = [row[0] for row in cursor.fetchall()]

# Parámetros de simulación
TOTAL = 463
types = ['transfer', 'withdrawal', 'bill_payment', 'credit']
statuses = ['completed', 'pending', 'failed']
channels = ['ATM', 'branch', 'corresponsal', 'online']
credit_statuses = ['approved', 'pending', 'rejected']
service_companies = ['ElectricCo', 'WaterCorp', 'InternetSA', 'GasLtd']

# Función para generar y ejecutar una transacción completa
def insertar_movimiento_con_detalle():
    source_acc = random.choice(accounts)
    # Generar datos comunes
    amount = round(random.uniform(1000, 5000000), 2)
    status = random.choices(statuses, weights=[0.85, 0.10, 0.05])[0]
    type_movement = random.choice(types)
    reference = faker.bothify(text='Trans###???')
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Inserción en Movement con RETURNING
    cursor.execute("""
        INSERT INTO movement (source_account_id, amount, date_time, status, type_movement, reference)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING movement_id
    """, (source_acc, amount, now, status, type_movement, reference))
    mov_id = cursor.fetchone()[0]

    # Inserción en la tabla hija correspondiente
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
        interest = round(random.uniform(0.01, 0.2), 2)  # 1% a 20%
        due_date = (datetime.now() + timedelta(days=random.randint(30, 365))).date()
        credit_status = random.choice(credit_statuses)
        cursor.execute("""
            INSERT INTO "credit" (movement_id, credit_type, interest, due_date, credit_status)
            VALUES (%s, %s, %s, %s, %s)
        """, (mov_id, random.choice(['lifeline', 'booster']), interest, due_date, credit_status))

# Medir el tiempo de inserción de 463 transacciones completas
start_time = time.time()

for _ in range(TOTAL):
    insertar_movimiento_con_detalle()

conn.commit()
elapsed = time.time() - start_time

print(f"Tiempo total para {TOTAL} transacciones completas: {elapsed:.4f} segundos")
if elapsed <= 1.0:
    print("PostgreSQL procesó todas las transacciones completas en ≤1 segundo")
else:
    print("Tardó más de 1 segundo")

cursor.close()
conn.close()

