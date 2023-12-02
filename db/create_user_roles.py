import os
import sqlite3

import mysql.connector
from dotenv import load_dotenv

from tests import in_testing_mode

load_dotenv()


def create_roles():
    testing = in_testing_mode()
    if testing:
        conn = sqlite3.connect(':memory:')
    else:
        conn = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USERNAME'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=os.getenv('DB_PORT')
        )

    cursor = conn.cursor()

    if testing:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='role';")
        table_exists = cursor.fetchone()

        if not table_exists:
            cursor.execute(
                "CREATE TABLE role (id INTEGER PRIMARY KEY, name VARCHAR(80) UNIQUE);"
            )

    cursor.execute("SELECT id FROM role WHERE name='user' OR name='admin';")
    existing_roles = cursor.fetchall()

    if not existing_roles:
        cursor.execute(
            "INSERT INTO role (name) VALUES ('user'), ('admin');"
        )

    conn.commit()
    cursor.close()
    conn.close()
