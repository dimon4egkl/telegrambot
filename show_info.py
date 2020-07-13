import sqlite3
import datetime

db = sqlite3.connect("db.sqlite3")
sql = db.cursor()

sql.execute("SELECT * FROM users")
users = sql.fetchall()
print("users")
for user in users:
    print(user)
print("task")
sql.execute("SELECT text FROM tasks")
task = sql.fetchone()
print(task)
sql.execute("SELECT * FROM friends")
friends = sql.fetchall()
print("Friends")
for friend in friends:
    print(friend)
print("done")