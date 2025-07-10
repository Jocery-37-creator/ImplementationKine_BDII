import psycopg2
from pymongo import MongoClient
import pandas as pd
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

# Input
phone = input("Enter user's phone number: ").strip()
start_date = input("Enter start date (YYYY-MM-DD): ").strip()
end_date = input("Enter end date (YYYY-MM-DD): ").strip()

# Get user data
query_user = """
SELECT user_id, full_name, phone
FROM "User"
WHERE phone = %s;
"""

pg_cursor.execute(query_user, (phone,))
result = pg_cursor.fetchone()

if not result:
    print("❌ User not found in PostgreSQL.")
    exit()

user_id, full_name, phone_number = result
print(f"✅ User found: {full_name} - {phone_number}")

# Get account_id
query_account = """
SELECT account_id
FROM "account"
WHERE user_id = %s;
"""

pg_cursor.execute(query_account, (user_id,))
account_result = pg_cursor.fetchone()

if not account_result:
    print("❌ No account found for this user.")
    exit()

account_id = str(account_result[0])
print(f"✅ Found account_id: {account_id}")

# Query movements from MongoDB Atlas
start_dt = datetime.strptime(start_date, "%Y-%m-%d")
end_dt = datetime.strptime(end_date, "%Y-%m-%d")

movements_cursor = mongo_movements.find({
    "source_account_id": account_id,
    "date_time": {
        "$gte": start_dt,
        "$lte": end_dt
    }
})

movements_list = list(movements_cursor)

if not movements_list:
    print("⚠️ No movements found in the selected period.")
    exit()

print(f"✅ Found {len(movements_list)} movements in MongoDB Atlas.")

# Build DataFrame
data = []

for mov in movements_list:
    data.append({
        "date_time": mov["date_time"].strftime("%Y-%m-%d %H:%M:%S"),
        "type_movement": mov["type_movement"],
        "status": mov["status"],
        "reference": mov["reference"],
        "amount": float(mov["amount"])
    })

df = pd.DataFrame(data)

# Calculate income and expense
income_types = ["credit"]
expense_types = ["transfer", "withdrawal", "bill_payment"]

df["income"] = df.apply(
    lambda row: row["amount"] if row["type_movement"] in income_types else 0,
    axis=1
)

df["expense"] = df.apply(
    lambda row: row["amount"] if row["type_movement"] in expense_types else 0,
    axis=1
)

total_income = df["income"].sum()
total_expense = df["expense"].sum()

# Save CSV
filename = f"statement_{full_name.replace(' ', '_')}_{start_date}_to_{end_date}.csv"

df[["date_time", "type_movement", "status", "reference", "amount"]].to_csv(
    filename, index=False
)

with open(filename, "a") as f:
    f.write("\n")
    f.write(f"Total Income,{total_income}\n")
    f.write(f"Total Expense,{total_expense}\n")

print(f"✅ Statement saved as: {filename}")
