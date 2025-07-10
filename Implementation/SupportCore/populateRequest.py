from faker import Faker
import numpy as np
import psycopg2
from pymongo import MongoClient
from datetime import datetime
import random

# Initialize Faker
generation = Faker()

# PostgreSQL connection
pg_conn = psycopg2.connect(
    host="localhost",
    database="Kine",
    user="postgres",
    password="1234"
)
pg_cursor = pg_conn.cursor()

# MongoDB connection
mongo_client = MongoClient("mongodb://localhost:27017/")
mongo_db = mongo_client["kine"]
mongo_request = mongo_db["request"]
mongo_agent = mongo_db["agent"]

# Get all agents from Mongo
agents_cursor = mongo_agent.find({})
agent_ids = [agent["agent_id"] for agent in agents_cursor]

if not agent_ids:
    print("No agents found in MongoDB. Please insert some agents first.")
    exit()

# Fetch all users from PostgreSQL
pg_cursor.execute('SELECT user_id FROM "User";')
users = pg_cursor.fetchall()

if not users:
    print("No users found in PostgreSQL.")
    exit()

print(f"Found {len(users)} users in PostgreSQL.")

for user in users:
    user_id = str(user[0])

    # Generate fake request
    request_doc = {
        "user_id": user_id,
        "type": np.random.choice(["query", "complaint", "report"]),
        "status": "open",
        "create_date": datetime.now(),
        "description": str(np.random.randint(1000, 9999)),
        "user_attach": [],
        "responses": []
    }

    # Insert request
    result = mongo_request.insert_one(request_doc)
    request_id = result.inserted_id
    print(f"Created request {request_id} for user {user_id}")

    # Generate 1 or 2 responses
    num_responses = np.random.choice([1, 2])

    for _ in range(num_responses):
        random_agent_id = random.choice(agent_ids)

        response_doc = {
            "agent_id": random_agent_id,
            "date": datetime.now(),
            "message": f"Auto-generated response {np.random.randint(100, 999)}",
            "response_attach": []
        }

        mongo_request.update_one(
            {"_id": request_id},
            {"$push": {"responses": response_doc}}
        )

        print(f"Added response from agent {random_agent_id} to request {request_id}")

print("All fake data has been inserted.")
