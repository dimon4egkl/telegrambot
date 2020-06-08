import sqlite3
import random
db = sqlite3.connect("server.sqlite3")
sql = db.cursor()

sql.execute("UPDATE users SET prev_day_task_completeness=1")
db.commit()
