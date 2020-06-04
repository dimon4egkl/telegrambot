#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This is a simple echo bot using decorators and webhook with flask
# It echoes any incoming text messages and does not use the polling method.
import config
import logging
import time
import sqlite3
import flask
import datetime
from telebot import types
import telebot


API_TOKEN = config.TOKEN

WEBHOOK_HOST = '185.253.218.184'
WEBHOOK_PORT = 88  # 443, 80, 88 or 8443 (port need to be 'open')
WEBHOOK_LISTEN = '185.253.218.184'  # In some VPS you may need to put here the IP addr

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Path to the ssl certificate
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Path to the ssl private key

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % (API_TOKEN)

logger = telebot.logger
telebot.logger.setLevel(logging.INFO)

bot = telebot.TeleBot(API_TOKEN)

app = flask.Flask(__name__)


# Empty webserver index, return nothing, just http 200
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return ''


# Process webhook calls
@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)


# Handle '/start' and '/help'
@bot.message_handler(commands=['start'])
def welcome(message):
    if message.chat.type =="private":
        db = sqlite3.connect("server.sqlite3")

        sql = db.cursor()
        sql.execute("SELECT id FROM users WHERE id =?", (message.from_user.id,))
        if sql.fetchone() is None:
            sql.execute(f"INSERT INTO users VALUES (?,?,?,?,?,?,?,?,?,?,?)",(message.from_user.id, message.from_user.username, 0, 0, 0, 0,0,0,0,message.from_user.first_name,message.from_user.last_name))
            db.commit()
            bot.send_message(message.chat.id, "Вас зареєстровано в базі",reply_to_message_id=message.message_id)
        else:
            bot.send_message(message.chat.id, "Ви уже зареєстровані в базі")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("⏰ Встановити новий час підйому")
        item2 = types.KeyboardButton("📌 Завдання на сьогодні")
        item3 = types.KeyboardButton("🧍‍♀️🧍 Мій друзяка на сьогодні")
        markup.add(item1,item2,item3)
        sti = open('sticker.webp', 'rb')
        bot.send_sticker(message.chat.id, sti)
        bot.send_message(message.chat.id,
                         "Привіт, {0.first_name}! \n Я - {1.first_name}".format(message.from_user, bot.get_me()),
                         parse_mode='html', reply_markup=markup)
    else:
        bot.send_message(message.chat.id,
                        "Привіт, Я - {1.first_name}".format(message.from_user, bot.get_me()),)


# Handle all other messages
@bot.message_handler(content_types=['text'])
def reply(message):
    if message.chat.type=='private':
        db = sqlite3.connect("server.sqlite3")
        sql = db.cursor()
        if message.text == "⏰ Встановити новий час підйому":
            sql.execute("UPDATE users SET hour_set_bool = 1 WHERE id =?", (message.from_user.id,))
            db.commit()
            bot.send_message(message.chat.id,"Введіть будь ласка коли ви хочете встати у форматі год:хв")
            return
        if message.text == "📌 Завдання на сьогодні":
            sql.execute("SELECT text FROM tasks")
            task = sql.fetchone()
            bot.send_message(message.from_user.id,"Ваше завдання на сьогодні : " + task)
            return
        if message.text == "🧍‍♀️🧍 Мій друзяка на сьогодні":
            sql.execute("SELECT friend_id FROM friends WHERE id =?", (message.from_user.id,))
            friend_id = sql.fetchone()
            friend= sql.execute("SELECT username,first_name,last_name FROM users WHERE id=?",(friend_id,))
            name = " "
            if friend[0] == None or friend[0] == "" or friend[0] == " ":
                if friend[2] == None:
                    name = friend[1]
                else:
                    name = friend[1] + " " + friend[2]
            else:
                name = "@" + friend[0]
            bot.send_message(message.chat.id, "Ваш друзяка на сьогодні: "+ name)
            return
        sql.execute("SELECT hour_set_bool FROM users WHERE id =?", (message.from_user.id,))
        hour_bool=sql.fetchone()
        hour_bool=hour_bool[0]
        if hour_bool == 1:
            colon_index = message.text.find(":")

            if colon_index == -1:
                bot.send_message(message.chat.id, "Введіть будь ласка коли ви хочете встати у форматі год:хв")
            else:
                message_length= len(message.text)
                try:
                    hour =int(message.text[0:colon_index])
                    minute = int(message.text[colon_index + 1:message_length])
                    if hour <10 and hour >=5 or(hour==10 and minute==0) :

                        sql.execute("UPDATE users SET hour_of_wakeup =?, minute_of_wakeup=?, hour_set_bool=0  WHERE id =?",
                                    (hour, minute, message.from_user.id,))
                        db.commit()
                        bot.send_message(message.chat.id,
                                         "Час назначено на " + "{:02d}".format(hour) + ":" + "{:02d}".format(minute))
                    else:
                        bot.send_message(message.chat.id, "Вибач, друже, але в такі години не можна прокидатися. Запропоновані години : з 5:00 по 10:00")
                        bot.send_message(message.chat.id, "Введіть будь ласка коли ви хочете встати у форматі год:хв")
                except:
                    bot.send_message(message.chat.id, "Ви ввели дату у неправильному форматі. Портрібно у форматі год:хв. Введіть ще раз")
                return
    else:
        if message.from_user.id == 404063513 or message.from_user.id == 298563297:
            if message.text.find("#newtask")!=-1:
                db = sqlite3.connect("server.sqlite3")
                sql = db.cursor()
                index = message.text.find("#newtask")
                string = message.text[:index] + message.text[index+9:]
                sql.execute("UPDATE tasks SET text=?",(string,))
                db.commit()
                sql.execute("SELECT id FROM users")
                users = sql.fetchmany(2)
                for user in users:
                    bot.send_message(user[0],string)
                try:
                    bot.unpin_chat_message(message.chat.id)
                except:
                    pass
                bot.pin_chat_message(message.chat.id,message.message_id)
                return
        if message.text.find("#task")!=-1:
            db = sqlite3.connect("server.sqlite3")
            sql = db.cursor()
            bot.send_message(message.from_user.id,"Завдання виконано")
            sql.execute("UPDATE users SET present_day_task_completeness = 1 WHERE id =? ",(message.from_user.id,))
            db.commit()
@bot.message_handler(content_types=['photo'])
def photo_task(message):
    if message.caption.find("#task")!=-1:
        print(message.caption)
        db = sqlite3.connect("server.sqlite3")
        sql = db.cursor()
        bot.send_message(message.from_user.id, "Завдання виконано")
        sql.execute("UPDATE users SET present_day_task_completeness = 1 WHERE id =? ", (message.from_user.id,))
        db.commit()
@bot.message_handler(content_types=['video_note','video'])
def vid(message):
    db = sqlite3.connect("server.sqlite3")
    sql = db.cursor()
    sql.execute("SELECT hour_of_wakeup, minute_of_wakeup, wakeup_completeness FROM users WHERE id =?",
                (message.from_user.id,))
    check= sql.fetchone()
    check_hour = check[0]
    if check_hour==0:
        bot.send_message(message.from_user.id, "Вам потрібно спочатку задати час пробудження. Настисніть кнопки під клавіатурою \n'⏰ Встановити новий час підйому' ",parse_mode='html')
    elif check[2]==1:
        pass
    else:
        check_minute = check[1]
        date = datetime.datetime.fromtimestamp(message.date)
        date_hour = int(date.strftime('%H'))+ 7
        if date_hour>24:
             date_hour-=24
        date_minute = int(date.strftime('%M'))
        if check_hour >= date_hour or (check_hour==date_hour and check_minute >= date_minute):
            bot.send_message(message.from_user.id, "Відео прийняте. Ти молодець. Гарного ранку )")
            sql.execute("UPDATE users SET wakeup_completeness=1  WHERE id =?",
                        (message.from_user.id,))
            db.commit()
            #wakeup_completeness  1 - скинув вчасно 2 - запізно скинув
        else:
            sql.execute("UPDATE users SET wakeup_completeness=2  WHERE id =?",
                        (message.from_user.id,))
            db.commit()
            bot.send_message(message.from_user.id, "Ти трішки запінився. Але не переживай. Завтра обов'язково вийде")
# Remove webhook, it fails sometimes the set if there is a previous webhook
bot.remove_webhook()

time.sleep(5)

# Set webhook
bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                certificate=open(WEBHOOK_SSL_CERT, 'r'))

# Start flask server
app.run(host=WEBHOOK_LISTEN,
        port=WEBHOOK_PORT,
        ssl_context=(WEBHOOK_SSL_CERT, WEBHOOK_SSL_PRIV),
        debug=True)
