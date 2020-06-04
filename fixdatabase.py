import sqlite3
import random
db = sqlite3.connect("server.sqlite3")
sql = db.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS friends (id integer,username text,first_name text ,last_name text, friend_id integer)")
sql.execute("SELECT id,username,first_name,last_name FROM users")
users = sql.fetchall()
for user in users:
    sql.execute("INSERT INTO friends VALUES(?,?,?,?,?)",(user[0],user[1],user[2],user[3],0,))
    db.commit()

sql.execute("SELECT id, present_day_task_completeness, wakeup_completeness FROM users")
tasks = sql.fetchall()
friends = set()
for task in tasks:
    friends.add(task[0])
    #sql.execute("UPDATE users SET prev_day_task_completeness =?, present_day_task_completeness=?,wakeup_completeness=?  WHERE id =? ",(task[1], 0, 0, task[0],))
    #db.commit()
    print("changed!")
new_friends = random.sample(friends, len(friends))
for i in range(0, len(new_friends) - 1, 2):
    sql.execute("UPDATE friends SET friend_id=?  WHERE id =? ", (new_friends[i + 1], new_friends[i]))
    db.commit()
    sql.execute("UPDATE friends SET friend_id=?  WHERE id =? ", (new_friends[i], new_friends[i + 1]))
    db.commit()
print("inserted")
