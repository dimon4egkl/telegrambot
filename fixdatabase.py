import sqlite3
import random
db = sqlite3.connect("db.sqlite3")
sql = db.cursor()

#sql.execute("UPDATE users SET prev_day_task_completeness=1")
# sql.execute("ALTER TABLE users ADD COLUMN prev_day_list_completeness INTEGER")
# sql.execute("ALTER TABLE users ADD COLUMN present_day_list_completeness INTEGER")

# sql.execute("ALTER TABLE users DROP COLUMN prev_day_list_completeness")
# sql.execute("ALTER TABLE users DROP COLUMN present_day_list_completeness")
sql.execute("UPDATE users SET present_day_list_completeness=0")
sql.execute("UPDATE users SET prev_day_list_completeness=0")
db.commit()
