# db_postgres.py

import psycopg2

def get_pg_connection():
    conn = psycopg2.connect(
        host="localhost",
        database="Kine",
        user="postgres",
        password="1234"
    )
    return conn

def get_user_id_by_phone(phone):
    conn = get_pg_connection()
    cursor = conn.cursor()
    query = """
    SELECT user_id FROM "User"
    WHERE phone = %s;
    """
    cursor.execute(query, (phone,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    else:
        return None
