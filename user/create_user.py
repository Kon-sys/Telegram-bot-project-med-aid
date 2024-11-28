import re
import sqlite3
from telebot import types
from functional.functional import functional
from src.text import translations
from src.dictionaries import user_languages
from cryptography.fernet import Fernet


def registration(bot, message):
    bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]['input_email'])
    bot.register_next_step_handler(message, lambda msg: create_username(bot, msg))

def create_username(bot, message):
    login = message.text.strip()
    if re.search(r"[^@]+@[^@]+\.[^@]+", login):
        if check_for_login_exist(login): #implement a match check for the 'login' field
            bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]['password'])
            bot.register_next_step_handler(message, lambda msg: create_userpassword(bot, msg, login))
        else:
            bot.reply_to(message, translations[user_languages[message.chat.id]]['user_almost_created'])
            bot.register_next_step_handler(message, lambda msg: create_username(bot, msg))
    else:
        bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]['email_mistake'])
        bot.register_next_step_handler(message, lambda msg: create_username(bot, msg))


def create_userpassword(bot, message, login):
    password = message.text.strip()
    encrypted = encrypt_password(password)
    conn = sqlite3.connect('../src/base_tg.sql')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (login, password) VALUES (?, ?)", (login, encrypted))
    cur.execute('SELECT * FROM users WHERE login = ? AND password = ?', (login, encrypted))
    id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)
    markup = types.InlineKeyboardMarkup()
    bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]['success_registry'], reply_markup=markup)
    functional(bot, message, id)

def check_for_login_exist(login):
    conn = sqlite3.connect('../src/base_tg.sql')
    cur = conn.cursor()

    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    cur.close()
    conn.close()
    for el in users:
        if login == el[1]:
            return False
    return True


def sign_in(bot, message):
    email = message.text.strip()
    if re.search(r"[^@]+@[^@]+\.[^@]+", email):
        bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]['password'])
        bot.register_next_step_handler(message, lambda msg: sign_in_password(bot, msg, email))
    else:
        bot.reply_to(message, translations[user_languages[message.chat.id]]['format_mistake'])
        bot.register_next_step_handler(message, lambda msg: sign_in(bot, msg))

def sign_in_password(bot, message, email):
    password = message.text
    conn = sqlite3.connect('../src/base_tg.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE login = ?', (email,))
    correct = cur.fetchone()

    if correct is None:
        markup = types.InlineKeyboardMarkup()
        btn_for_recovery = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]['forgot_password'], callback_data='password_recovery')
        btn_for_registry = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]['start_registry'], callback_data='registry')
        btn_for_sign_in = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]['sign_in'], callback_data='sign_in')
        markup.row(btn_for_registry, btn_for_recovery)
        markup.row(btn_for_sign_in)
        bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]['sign_in_mistake'], reply_markup=markup)
        conn.commit()
        cur.close()
        conn.close()
        return

    correct_password = decrypt_password(correct[2])
    #Если есть пользователи, войти - если нет, рекурсивно вызвать sign_in или предложить выйти
    if password == correct_password:
        bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]['cong_sign'])
        cur.execute('SELECT * FROM users WHERE login = ?', (email,))
        id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()
        functional(bot, message, id)
    else:
        conn.commit()
        cur.close()
        conn.close()
        markup = types.InlineKeyboardMarkup()
        btn_for_recovery = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]['forgot_password'], callback_data='password_recovery')
        btn_for_registry = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]['start_registry'], callback_data='registry')
        btn_for_sign_in = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]['sign_in'], callback_data='sign_in')
        markup.row(btn_for_registry, btn_for_sign_in)
        markup.row(btn_for_recovery)
        bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]['sign_in_mistake'], reply_markup=markup)


def load_key():
    return open("/Users/adriel-ai/Desktop/Telegram-bot project/src/secret.key", "rb").read()

# Шифровка пароля
def encrypt_password(password):
    key = load_key()
    f = Fernet(key)
    encrypted_password = f.encrypt(password.encode())
    return encrypted_password

# Дешифровка пароля
def decrypt_password(encrypted_password):
    key = load_key()
    f = Fernet(key)
    decrypted_password = f.decrypt(encrypted_password).decode()
    return decrypted_password