import sqlite3
import datetime

db = sqlite3.connect("server.sqlite3")
sql = db.cursor()

# sql.execute("SELECT id, present_day_task_completeness, wakeup_completeness FROM users")
# #
# # tasks = sql.fetchall()
# # for task in tasks:
# #     print(task)
# #     sql.execute("UPDATE users SET prev_day_task_completeness =?, present_day_task_completeness=?  WHERE id =? ",(task[1],0,task[0],))
# #     db.commit()
# # print("done")

#sql.execute("SELECT id, present_day_task_completeness, wakeup_completeness FROM users")
sql.execute("SELECT * FROM users")
tasks = sql.fetchall()
for task in tasks:
    print(task)
     if task[1] == 'Vitalii' or task[9] =="Діма" or task[9] =="Dasha" or task[9]=="Volodymyr":
         sql.execute("UPDATE users SET prev_day_task_completeness =?  WHERE id =? ",(1,task[0],))
     else:
         sql.execute("UPDATE users SET prev_day_task_completeness =?,wakeup_completeness =?  WHERE id =? ",(1,0,task[0],))
    db.commit()
print("done")