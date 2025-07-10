import psycopg2
from faker import Faker
import random
import time
from datetime import datetime

faker = Faker()

# Conexión a la base de datos
conn = psycopg2.connect(
    dbname='KineDataBase',
    user='postgres',
    password='1234567',
    host='localhost',
    port='5432'
)

cursor = conn.cursor()

# Lista de UUIDs de cuenta (puedes acortar o ampliar)
account_ids = [
    "cb5de771-f1be-4ee2-8b22-e7ea6593af64", "89e04548-4df5-431d-bfea-2a7e034afd9c",
    "645c7d86-7668-404c-a0bb-c87617e82daf", "846a54cd-7cd0-438f-903b-1366616c4c7f",
    "e2eb1bf7-c5b3-436e-91df-a305e81c0765", "2ee8d25a-11f7-4c96-b4df-46f1b53d8d64",
    "5cc6a354-af52-4c3c-a18a-6d3beb3ca7dc", "0bab8f6c-e11f-4057-92e0-1056a6789d8e",
    "d8e03b99-d00a-4fbd-9164-080af27ed0dc", "4f4431f1-c002-4e98-bae5-d60570bda27b",
    "38fcbbf3-ed32-4659-afd2-6d5d90d764f9", "3fb75d03-fb64-407d-b8d6-204dfff1fb63",
    "97ee2107-e47f-4ac6-8acf-903f5ad9f1fe", "c080955a-e7b8-4910-8e14-7498cf50f8f0"
]

types = ['transfer', 'withdrawal', 'bill_payment', 'credit']
statuses = ['completed', 'pending', 'failed']

def generar_movimiento():
    acc = random.choice(account_ids)
    amount = round(random.uniform(1000, 5000000), 2)
    dt = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    status = random.choices(statuses, weights=[0.85, 0.10, 0.05])[0]
    type_movement = random.choice(types)
    reference = faker.bothify(text='Trans###???')
    return (acc, amount, dt, status, type_movement, reference)

# Generar los 463 movimientos
movimientos = [generar_movimiento() for _ in range(463)]

# Medir el tiempo de inserción
start = time.time()

cursor.executemany("""
    INSERT INTO "movement" (source_account_id, amount, date_time, status, type_movement, reference)
    VALUES (%s, %s, %s, %s, %s, %s)
""", movimientos)

conn.commit()
end = time.time()

# Resultado
elapsed = end - start
print(f"Tiempo de inserción de 463 movimientos: {elapsed:.4f} segundos")
if elapsed <= 1.0:
    print("PostgreSQL procesó las transacciones en ≤1 segundo")
else:
    print("Tardó más de 1 segundo")

# Cierre
cursor.close()
conn.close()
