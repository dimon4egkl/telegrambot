import time
import sqlite3
import telebot
import config
import datetime

bot = telebot.TeleBot(config.TOKEN)
db = sqlite3.connect("server.sqlite3")
sql = db.cursor()
#while True:
date = datetime.datetime.now().time()
hour = date.hour + 7
    # додати 7 годин коли закідати в git
if hour == 18 or hour ==21:
    sql.execute("SELECT id, present_day_task_completeness FROM users")
    users = sql.fetchall()
    for user in users:
        if user[1] == 0 :
            print("delivered")
            bot.send_message(user[0], "Пссс Пссс. Тут тебе цей... завдання чекає. Рекомендую приділити пару хвилин, щоб його виконати. А тоді повертайся до своїх корисних і приємних справ")
   # time.sleep(3600)

