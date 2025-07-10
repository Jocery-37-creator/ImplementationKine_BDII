# create_request.py

from db_postgres import get_user_id_by_phone
from db_mongo import get_mongo_db
from datetime import datetime


def create_request():
    phone = input("User phone: ").strip()

    user_id = get_user_id_by_phone(phone)
    if not user_id:
        print("User not valid.")
        return

    tipo = input("Type of request (query, report, complaint, etc.): ").strip()
    descripcion = input("Description of the problem: ").strip()

    user_attach = input("Attachments (comma separated, or empty): ").strip()
    if user_attach:
        attach_list = [a.strip() for a in user_attach.split(",")]
    else:
        attach_list = []

    db = get_mongo_db()
    collection = db["request"]

    result = collection.insert_one({
        "user_id": str(user_id),
        "type": tipo,
        "status": "open",
        "create_date": datetime.now(),
        "description": descripcion,
        "user_attach": attach_list,
        "responses": []
    })

    print(f"✅ Request create, id: {result.inserted_id}")
