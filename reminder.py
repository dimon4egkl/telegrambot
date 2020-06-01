import time
import sqlite3
import telebot


db = sqlite3.connect("server.sqlite3")
sql = db.cursor()

sql.execute("SELECT id, present_day_task_completeness FROM users")
users = sql.fetchall()
for user in users:
    print(user)


