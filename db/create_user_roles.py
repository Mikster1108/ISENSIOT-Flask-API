import os

import mysql.connector
from dotenv import load_dotenv

load_dotenv()


def create_roles():
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'),
        user=os.getenv('DB_USERNAME'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME'),
        port=os.getenv('DB_PORT')
    )

    cursor = conn.cursor()
    cursor.execute("SELECT id FROM role WHERE name='user' OR name='admin';")
    existing_roles = cursor.fetchall()

    if not existing_roles:
        cursor.execute(
            "INSERT INTO role (name) VALUES ('user'), ('admin');"
        )

    conn.commit()
    cursor.close()
    conn.close()
