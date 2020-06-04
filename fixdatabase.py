import sqlite3

db = sqlite3.connect("server.sqlite3")
sql = db.cursor()
sql.execute("CREATE TABLE IF NOT EXISTS tasks (id integer PRIMARY KEY,text text NOT NULL)");

print("done")
