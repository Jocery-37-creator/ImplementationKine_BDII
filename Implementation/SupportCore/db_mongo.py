# db_mongo.py

from pymongo import MongoClient

def get_mongo_db():
    client = MongoClient("mongodb://localhost:27017/")
    db = client["kine"]
    return db

def agent_exists(agent_id):
    db = get_mongo_db()
    agent = db.agent.find_one({"agent_id": int(agent_id)})
    return agent is not None

def get_agent():
    db = get_mongo_db()
    agents = db.agent.find({})
    agent_ids = [agent["agent_id"] for agent in agents]
    return agent_ids is not None
