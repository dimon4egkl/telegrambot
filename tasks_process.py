import sqlite3
import datetime
import time
import random
db = sqlite3.connect("db.sqlite3")
sql = db.cursor()


while True:

    sql.execute("SELECT id, present_day_task_completeness, wakeup_completeness, present_day_list_completeness  FROM users")
    tasks = sql.fetchall()
    date = datetime.datetime.now().time()
    hour = date.hour  + 7
    if hour > 24:
        hour -= 24
    print(hour)
    if hour == 2:
        friends = set()
        for task in tasks:
            friends.add(task[0])
            sql.execute("UPDATE users SET prev_day_task_completeness =?, present_day_task_completeness=?,wakeup_completeness=?,prev_day_list_completeness=?,present_day_list_completeness=?  WHERE id =? ",(task[1],0,0,task[0],task[3],0))
            db.commit()
            print("changed!")
        new_friends = random.sample(friends,len(friends))
        for i in range(0,len(new_friends)-1,2):
            sql.execute("UPDATE friends SET friend_id=?  WHERE id =? ",(new_friends[i+1],new_friends[i]))
            db.commit()
            sql.execute("UPDATE friends SET friend_id=?  WHERE id =? ", (new_friends[i], new_friends[i+1]))
            db.commit()
    print("done")
    time.sleep(3600)


