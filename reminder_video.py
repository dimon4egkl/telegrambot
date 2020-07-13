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
    hour = date.hour + 7
    if hour > 24:
        hour -= 24
    minute = date.minute
    # додати 7 годин коли закідати в git
    sql.execute("SELECT id, wakeup_completeness, hour_of_wakeup, minute_of_wakeup  FROM users")
    users = sql.fetchall()


    for user in users:
            differense_in_time = (user[2] - hour)*60 + user[3] - minute

            if differense_in_time <= 15 and differense_in_time > 0 and user[1]==0:
                bot.send_message(user[0], "До скидання відео звіту залишилось всього {0} хв. Поспіши :)".format(differense_in_time))
    time.sleep(900)


