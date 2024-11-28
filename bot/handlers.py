import sqlite3
from telebot import types
from user.password_recovery import process_email
from user.create_user import registration, sign_in
from functional import medicament
from functional.functional import functional
from functional.pharmacies import search_medicament, getting_location, get_adress
import src.text
from src.dictionaries import callback_handlers, user_states_location, user_languages



#A function for processing handlers received from the user
#by commands or using buttons
def register_handlers(bot):


# The main callback processing function.
# Receives a function from the dictionary by key (dictionary - .src/dictionaries) and
# if the callback of the dictionary and the user's callback match, calls the corresponding handler
    @bot.callback_query_handler(func=lambda call: True)
    def handle_callback_query(call):
        # Получаем функцию из словаря по ключу
        handler = callback_handlers.get(call.data.split(':')[0])

        # Если обработчик существует, вызываем его
        if handler:
            handler(call)
        else:
            bot.send_message(call.message.chat.id, "Неизвестный callback!")



# '/start' command handler
# Displays messages to the user as described in the .src/text.py file
    @bot.message_handler(commands=['start'])
    def main(message):
        user_languages[message.chat.id] = message.from_user.language_code
        if user_languages[message.chat.id] == 'ru':
            if message.from_user.last_name is None:
                bot.send_message(message.chat.id, f'👋Привет, {message.from_user.first_name}{src.text.translations[user_languages[message.from_user.id]]["hello_message"]}')
            else:
                bot.send_message(message.chat.id,
                                f'👋Привет, {message.from_user.first_name} {message.from_user.last_name}{src.text.translations[user_languages[message.from_user.id]]["hello_message"]}')
        else:
            if message.from_user.last_name is None:
                bot.send_message(message.chat.id,
                                 f'👋Hello, {message.from_user.first_name}{src.text.translations[user_languages[message.from_user.id]]["hello_message"]}')
            else:
                bot.send_message(message.chat.id,
                                 f'👋Hello, {message.from_user.first_name} {message.from_user.last_name}{src.text.translations[user_languages[message.from_user.id]]["hello_message"]}')


    @bot.message_handler(commands=['language'])
    def main(message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(types.KeyboardButton('🇷🇺Русский'), types.KeyboardButton('🏴󠁧󠁢󠁥󠁮󠁧󠁿English'))
        bot.send_message(message.chat.id, "Выберите язык:", reply_markup=keyboard)


    @bot.message_handler(func=lambda message: message.text in ['🇷🇺Русский', '🏴󠁧󠁢󠁥󠁮󠁧󠁿English'])
    def language_selection(message):
        if message.text == '🇷🇺Русский':
            bot.send_message(message.chat.id, "Вы выбрали русский язык.")
            user_languages[message.chat.id] = 'ru'
        elif message.text == '🏴󠁧󠁢󠁥󠁮󠁧󠁿English':
            bot.send_message(message.chat.id, "You selected English language.")
            user_languages[message.chat.id] = 'en'


# '/help' command handler
# Displays messages to the user as described in the .src/text.py file
    @bot.message_handler(commands=['start_sign_in'])
    def main(message):
        markup = types.InlineKeyboardMarkup()
        btn_for_recovery = types.InlineKeyboardButton(src.text.translations[user_languages[message.chat.id]]['forgot_password'], callback_data='password_recovery')
        btn_for_registry = types.InlineKeyboardButton(src.text.translations[user_languages[message.chat.id]]['start_registry'], callback_data='registry')
        btn_for_sign_in = types.InlineKeyboardButton(src.text.translations[user_languages[message.chat.id]]['sign_in'], callback_data='sign_in')
        markup.row(btn_for_registry, btn_for_sign_in)
        markup.row(btn_for_recovery)
        bot.send_message(message.chat.id, src.text.translations[user_languages[message.chat.id]]['start_message'], reply_markup=markup)


# '/registry' button handler
# Allows the user to register by entering his email address and password.
# After user registration, the fields go to the database .src/base_tg.sql
# '/registry' button handler. The command is added to dictionary
    def handle_callback_registry(call):
        registration(bot, call.message)
    callback_handlers['registry'] = handle_callback_registry


# Function for processing the command and the 'sign_in' button. Allows the user
# to log into an existing account using a login and password.
# Receiving this data, a match search is carried out and if found, the user logs into his account
# '/sign_in' button handler. The command is added to dictionary
    def handle_callback_sign_in(call):
        bot.send_message(call.message.chat.id, src.text.translations[user_languages[call.message.chat.id]]['input_email'])
        bot.register_next_step_handler(call.message, lambda msg: sign_in(bot, msg))
    callback_handlers['sign_in'] = handle_callback_sign_in


# Function for recovering users password using his email and protocol smtp.
# User get message on his email with code which he should write to bot
# '/password_recovery' button handler. The command is added to dictionary
    def handle_callback_password_recovery(call):
        bot.send_message(call.message.chat.id, src.text.translations[user_languages[call.message.chat.id]]["text_for_recovery"])
        bot.register_next_step_handler(call.message, lambda msg: process_email(bot, msg))
    callback_handlers['password_recovery'] = handle_callback_password_recovery


# '/all_medicament' button handler for viewing all records with medicament from '.src/base_tg.sql'.
# The command is added to dictionary
    def handle_callback_all_medicament(call):
        id = call.data.split(':')[1]
        medicament.send_all_medicament(bot, call.message, id)
    callback_handlers['all_medicament'] = handle_callback_all_medicament


# '/users_medicament' button handler for viewing all users record about his medicament.
# The command is added to dictionary
    def handle_callback_users_medicament(call):
        id = call.data.split(':')[1]
        medicament.users_medicament(bot, call.message, id)
    callback_handlers['users_medicament'] = handle_callback_users_medicament


# '/add_medicament' button handler for adding record abot users medicament.
# The command is added to dictionary
    def handle_callback_add_medicament(call):
        id = call.data.split(':')[1]
        medicament.add_medicament(bot, call.message, id)
    callback_handlers['add_medicament'] = handle_callback_add_medicament

# Button handlers for adding (not adding) notes in the users medicament. 
# The command is added to dictionary
    def handle_callback_answer_yes(call):
        user_id = call.data.split(':')[1]
        med_id = call.data.split(':')[2]
        medicament.last_step_adding(bot, call.message, user_id, med_id, True)
    callback_handlers['answer_yes'] = handle_callback_answer_yes

    def handle_callback_answer_no(call):
        user_id = call.data.split(':')[1]
        med_id = call.data.split(':')[2]
        medicament.last_step_adding(bot, call.message, user_id, med_id, False)
    callback_handlers['answer_no'] = handle_callback_answer_no


# '/delete' button handler for deleting users record. The command is added to dictionary
    def handle_callback_delete(call):
        id = call.data.split(':')[1]
        medicament.delete_medicament(bot, call.message, id)
    callback_handlers['delete'] = handle_callback_delete


# '/search_medicament' button handler for searching medicament in the range closest to the user.
# Function uses users location and search nearest pharmacies from database '.src.base_tg.sql'.
# The command is added to dictionary
    def handle_callback_search_medicament(call):
        id = call.data.split(':')[1]
        search_medicament(bot, call.message, id)
    callback_handlers['search_medicament'] = handle_callback_search_medicament


    def handle_callback_choose_location(call):
        id = call.data.split(':')[1]
        bot.send_message(call.message.chat.id, src.text.translations[user_languages[call.message.chat.id]]["wait_location"])
        bot.register_next_step_handler(call.message, lambda msg: getting_location(bot, msg, id))
    callback_handlers['choose_location'] = handle_callback_choose_location


    def handle_callback_choose_adress(call):
        id = call.data.split(':')[1]
        bot.send_message(call.message.chat.id, src.text.translations[user_languages[call.message.chat.id]]["wait_adress"])
        bot.register_next_step_handler(call.message, lambda msg: get_adress(bot, msg, id))
    callback_handlers['choose_adress'] = handle_callback_choose_adress


    def handle_callback_applying(call):
        user_id = call.data.split(':')[1]
        med_id = call.data.split(':')[2]
        bot.delete_message(call.message.chat.id, call.message.message_id)
        medicament.apply(user_id, med_id)
    callback_handlers['applying'] = handle_callback_applying


    def handle_callback_history(call):
        user_id = call.data.split(':')[1]
        medicament.history(bot, call.message, user_id)
    callback_handlers['history'] = handle_callback_history


    def handle_callback_remind(call):
        user_id = call.data.split(':')[1]
        med_id = call.data.split(':')[2]
        value = int(call.data.split(':')[3])
        if call.data.split(':')[4] == '0':
            medicament.time_app(bot, call.message, user_id, med_id, value, None)
        else:
            bot.send_message(call.message.chat.id, src.text.translations[user_languages[call.message.chat.id]]["remind_early"])
            bot.register_next_step_handler(call.message, lambda msg: medicament.remind(bot, msg, user_id, med_id, value))
    callback_handlers['remind'] = handle_callback_remind


# '/back' button handler for viewing bots functional. The command is added to dictionary
    def handle_callback_back(call):
        id = call.data.split(':')[1]
        functional(bot, call.message, id)
    callback_handlers['back'] = handle_callback_back


    @bot.message_handler(func=lambda message: True)
    def handle_text_message(message):
        try:
            bot.send_message(message.chat.id, src.text.translations[user_languages[message.chat.id]]["default"])
        except Exception:
            bot.send_message(message.chat.id, src.text.translations[message.from_user.language_code]["default"])