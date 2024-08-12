import sqlite3
from config import DATABASE


def connect_db():
    return sqlite3.connect(DATABASE)
