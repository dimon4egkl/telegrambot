import sqlite3
import datetime
import time
db = sqlite3.connect("server.sqlite3")
sql = db.cursor()


while True:
    sql.execute("SELECT id, present_day_task_completeness, wakeup_completeness FROM users")
    tasks = sql.fetchall()
    date = datetime.datetime.now().time()
    hour = date.hour + 7
    if hour > 24:
        hour -= 24
    if hour == 2:
        for task in tasks:
            sql.execute("UPDATE users SET prev_day_task_completeness =?, present_day_task_completeness=?,wakeup_completeness=?  WHERE id =? ",(task[1],0,0,task[0],))
            db.commit()
    time.sleep(3600)


