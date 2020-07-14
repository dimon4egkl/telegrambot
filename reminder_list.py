import time
import sqlite3
import telebot
import config
import datetime

bot = telebot.TeleBot(config.TOKEN)
db = sqlite3.connect("db.sqlite3")
sql = db.cursor()
while True:
    date = datetime.datetime.now().time()
    day = datetime.datetime.now().weekday()
    hour = date.hour + 7
        # додати 7 годин коли закідати в git
    if day!=6 and (hour == 18 or hour ==21) :
        sql.execute("SELECT id, present_day_list_completeness FROM users")
        users = sql.fetchall()
        for user in users:
            if user[1] == 0 :
                bot.send_message(user[0], "Твій трекер звичок хоче, щоб ним поділились в чаті \"КращіМИ\"")
    time.sleep(3600)

