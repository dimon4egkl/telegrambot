import sqlite3

db = sqlite3.connect("server.sqlite3")
sql = db.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS tasks (id integer PRIMARY KEY,text text NOT NULL)")
sql.execute("INSERT INTO tasks VALUES (1,'-')")
db.commit()
print("inserted")
