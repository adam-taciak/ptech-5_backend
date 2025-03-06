import mysql.connector
import os


DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'user')
DB_PASS = os.getenv('DB_PASS', 'password')
DB_NAME = os.getenv('DB_NAME', 'app')
DB_PORT = os.getenv('DB_PORT', 3306)


def connect():
    db = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        passwd=DB_PASS,
        database=DB_NAME,
        port=DB_PORT
    )

    return db


def disconnect(db):
    db.close()
