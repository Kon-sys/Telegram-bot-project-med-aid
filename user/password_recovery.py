import asyncio
import sys
import os
import random
import re
import sqlite3
from src.text import translations
from src.dictionaries import user_languages
from user.create_user import encrypt_password

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from my_smtp import send_mail

from functional.functional import functional


def process_email(bot, message):
    user_email = message.text.strip()

    if re.match(r"[^@]+@[^@]+\.[^@]+", user_email):
        if check_for_login_exist(bot, message, user_email):
            bot.register_next_step_handler(message, lambda msg: process_email(bot, msg))
        else:
            bot.reply_to(message, f'{translations[user_languages[message.chat.id]]["send_code"]} {user_email}.')
            bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]["insert_code"])
            code_on_mail = random.randint(100000, 999999)
            asyncio.run(send_mail('Recovering password', user_email, f'<h1>Hello, your verification code: {code_on_mail}</h1>'))
            print(code_on_mail)
            bot.register_next_step_handler(message, lambda msg: check_code(bot, msg, code_on_mail, user_email))
    else:
        bot.reply_to(message, translations[user_languages[message.chat.id]]["format_mistake"])
        bot.register_next_step_handler(message, lambda msg: process_email(bot, msg))


def check_code(bot, message, code_on_mail, user_email):
    code = int(message.text.strip())
    if code == code_on_mail:
        bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]["new_password"])
        bot.register_next_step_handler(message, lambda msg: process_new_password(msg, bot, user_email))
    else:
        bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]["incorrect_code"])
        bot.register_next_step_handler(message, lambda msg: check_code(bot, msg, code_on_mail, user_email))


def process_new_password(message, bot, user_email):
    encrypted = message.text.strip()
    new_password = encrypt_password(encrypted)
    conn = sqlite3.connect('../src/base_tg.sql')
    cur = conn.cursor()
    cur.execute("UPDATE users SET password = ? WHERE login = ?", (new_password, user_email))
    cur.execute("SELECT * FROM users WHERE login = ?", (user_email,))
    id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    bot.reply_to(message, translations[user_languages[message.chat.id]]["password_updated"])
    functional(bot, message, id)


def check_for_login_exist(bot, message, user_email):
    conn = sqlite3.connect('../src/base_tg.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    existence = True
    cur.close()
    conn.close()
    for el in users:
        if user_email == el[1]:
            existence = False
    if existence:
        bot.reply_to(message, translations[user_languages[message.chat.id]]["user_non_created"])
    return existence