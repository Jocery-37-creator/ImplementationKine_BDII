import psycopg2
from pymongo import MongoClient
from datetime import datetime

# PostgreSQL connection
pg_conn = psycopg2.connect(
    host="localhost",
    database="Kine",
    user="postgres",
    password="1234"
)
pg_cursor = pg_conn.cursor()

# MongoDB Atlas connection
uri = "mongodb+srv://solozanom:Kine123@cluster0.01b75sj.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

mongo_client = MongoClient(uri)
mongo_db = mongo_client["kine"]
mongo_movements = mongo_db["movement_archive"]

# Define date range
start_date = "2022-01-01"
end_date = "2022-12-31"

# Query movements in the date range
query = """
SELECT 
    movement_id,
    source_account_id,
    amount,
    date_time,
    status,
    type_movement,
    reference
FROM "movement"
WHERE date_time BETWEEN %s AND %s;
"""

pg_cursor.execute(query, (start_date, end_date))
movements = pg_cursor.fetchall()

print(f"✅ Retrieved {len(movements)} movements from PostgreSQL.")

# Prepare documents for MongoDB
documents = []

for row in movements:
    movement_doc = {
        "movement_id": row[0],
        "source_account_id": str(row[1]),
        "amount": float(row[2]),
        "date_time": row[3],
        "status": row[4],
        "type_movement": row[5],
        "reference": row[6]
    }
    documents.append(movement_doc)

# Insert into MongoDB Atlas
if documents:
    mongo_movements.insert_many(documents)
    print(f"✅ Inserted {len(documents)} documents into MongoDB Atlas.")

    delete=input("Delete date: y/n")
    if delete=="y":
        delete_query = """
        DELETE FROM "movement"
        WHERE date_time BETWEEN %s AND %s;
        """

        pg_cursor.execute(delete_query, (start_date, end_date))
        pg_conn.commit()

        print(f"✅ Deleted {pg_cursor.rowcount} movements from PostgreSQL.")

else:
    print("⚠️ No movements found for the specified range.")
