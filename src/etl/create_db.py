import sqlite3

conn = sqlite3.connect("db/nifty100.db")

conn.execute("PRAGMA foreign_keys = ON")

with open("db/schema.sql", "r") as file:
    conn.executescript(file.read())

print("Schema Created Successfully")

conn.close()

import sqlite3

conn = sqlite3.connect("db/nifty100.db")

cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

print(cursor.fetchall())

conn.close()
