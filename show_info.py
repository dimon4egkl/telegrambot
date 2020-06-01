import sqlite3
import datetime

db = sqlite3.connect("server.sqlite3")
sql = db.cursor()

sql.execute("SELECT * FROM users")
tasks = sql.fetchall()
for task in tasks:
    print(task)
print("done")