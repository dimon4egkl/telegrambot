import telebot
import sqlite3
import config
import datetime
import time

bot = telebot.TeleBot(config.TOKEN)

db = sqlite3.connect("server.sqlite3")
sql = db.cursor()
while True:
    date = datetime.datetime.now().time()
    hour = date.hour + 7
        # додати 7 годин коли закідати в git
    if hour == 10:
        sql.execute("SELECT * FROM users")
    users = sql.fetchall()


    date = str(datetime.datetime.now().day) +"."+ str(datetime.datetime.now().month) + "."+ str(datetime.datetime.now().year)
    report_text = "Добрий ранок, друзі! Це звіт за {0}.\nСьогодні вчасно прокинулось '|' людей. \n\nНадіслали вчасно відео звіт та завдання: \n&Є питання до: \n&&".format(date)
    def report(report_text):
        wokeup_in_time = 0
        for user in users:
            name = ""
            if user[1] == None or user[1] =="" or user[1]==" ":
                if user[10]==None:
                    name = user[9]
                else:
                    name = user[9]+ " " + user[10]
            else:
                name = "@"+ user[1]
            task_text = ""
            if user[6]==0:
                task_text= " Завдання не виконано ❌"
            if int(user[8]) == 0:
                insert_index = report_text.find("&&")
                insert_text = name + " -відео не було надіслане до 10:00 ❌".format(user)
                report_text = report_text[:insert_index] + insert_text +task_text+ "\n" + report_text[insert_index:]
            if int(user[8]) == 2:
                insert_index = report_text.find("&&")
                insert_text = name + " -відео надіслане пізніше {0[4]}:{0[5]}❌".format(user)
                report_text = report_text[:insert_index] + insert_text +task_text +"\n" + report_text[insert_index:]
            if int(user[8]) == 1 and user[6]==0:
                insert_index = report_text.find("&&")
                insert_text = name+task_text
                report_text = report_text[:insert_index] + insert_text +"\n" +report_text[insert_index:]
                wokeup_in_time+=1
            if int(user[8]) == 1 and user[6]!=0:
                insert_index = report_text.find("&")
                insert_text = name+" ✅"
                report_text = report_text[:insert_index] + insert_text +"\n" +report_text[insert_index:]
                wokeup_in_time+=1

        insert_index = report_text.find("&")
        report_text = report_text[:insert_index] +report_text[insert_index+1:]
        insert_index = report_text.find("&&")
        report_text = report_text[:insert_index]
        insert_index = report_text.find("|")
        report_text = report_text[:insert_index] +str(wokeup_in_time)+ report_text[insert_index + 1:]
        return report_text


    report_text = report(report_text)
    bot.send_message(config.GROUP_CHAT_ID, report_text, parse_mode="html")

    time.sleep(3600)








