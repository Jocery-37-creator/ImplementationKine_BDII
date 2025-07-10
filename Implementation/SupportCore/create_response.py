# create_response.py

from db_mongo import get_mongo_db, agent_exists
from datetime import datetime
from bson import ObjectId


def create_response():
    request_id_str = input("Enter the _id of the request you want to respond to: ").strip()

    try:
        request_id = ObjectId(request_id_str)
    except:
        print("The _id entered is not valid.")
        return

    agent_id = input("Enter the agent_id that responds:: ").strip()

    if not agent_exists(agent_id):
        print("The agente is not valid.")
        return

    mensaje = input("Enter the response message: ").strip()

    response_attach = input("Attachments (comma separated, or empty: ").strip()
    if response_attach:
        attach_list = [a.strip() for a in response_attach.split(",")]
    else:
        attach_list = []

    db = get_mongo_db()
    collection = db["request"]

    result = collection.update_one(
        {"_id": request_id},
        {"$push": {
            "responses": {
                "agent_id": agent_id,
                "date": datetime.now(),
                "message": mensaje,
                "response_attach": attach_list
            }
        }}
    )

    if result.modified_count:
        print("Answer added successfully.")
    else:
        print("The request was not found.")
