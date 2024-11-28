import sqlite3
from telebot import types
from telebot.types import InlineKeyboardMarkup
from datetime import datetime, timedelta
import threading
import time
from src.text import translations
from src.dictionaries import user_languages

#The send_all_medicament function connects to the database and simply sends
#information to the user in a specific format
def send_all_medicament(bot, message, id):
    conn = sqlite3.connect('../src/base_tg.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM medicament')
    medicament = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    i = 1
    info = ""
    for el in medicament:
        if user_languages[message.chat.id] == 'ru':
            info += f'{i}) {el[1]}, доза - {el[2]}💊, частота приема - {el[3]} раза в день 📅.\n'
        else:
            info += f'{i}) {el[1]}, dose - {el[2]}💊, reception frequency - {el[3]} times a day 📅.\n'
        i += 1
    markup = types.InlineKeyboardMarkup()
    btn_for_back = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]["back"], callback_data=f'back:{id}')
    markup.row(btn_for_back)
    bot.send_message(message.chat.id, info, reply_markup=markup)


#The function accesses the database through the user id to the user_med table and gets the id of the
#medicaments. Next, using the medicament id, we get information from the medicament table
def users_medicament(bot, message, id):
    conn = sqlite3.connect('../src/base_tg.sql')
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM user_med WHERE id_user = ?', (id,))
    count = cur.fetchone()[0]
    if count < 1:
        bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]["no_med"])
        conn.commit()
        cur.close()
        conn.close()
        markup = types.InlineKeyboardMarkup()
        btn_for_back = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]["back"], callback_data=f'back:{id}')
        btn_for_add = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]["add_med"], callback_data=f'add_medicament:{id}')
        markup.row(btn_for_add, btn_for_back)
        bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]["message_for_back_or_add"],  reply_markup=markup)
    else:
        cur.execute('SELECT * FROM user_med WHERE id_user = ?', (id,))
        list_com = cur.fetchall()
        for el in list_com:
            cur.execute('SELECT * FROM medicament WHERE id = ?', (el[1],))
            med = cur.fetchone()
            if user_languages[message.chat.id] == 'ru':
                if el[2] is None:
                    bot.send_message(message.chat.id, f'Лекарство: {med[1]}, доза: {med[2]}')
                else:
                    bot.send_message(message.chat.id, f'Лекарство: {med[1]}, доза: {med[2]}\nЗаметка: 📝 {el[2]}')
            else:
                if el[2] is None:
                    bot.send_message(message.chat.id, f'Medicine: {med[1]}, dose: {med[2]}')
                else:
                    bot.send_message(message.chat.id, f'Medicine: {med[1]}, dose: {med[2]}\nNote: 📝 {el[2]}')
        conn.commit()
        cur.close()
        conn.close()
        markup = types.InlineKeyboardMarkup()
        btn_for_back = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]["back"], callback_data=f'back:{id}')
        btn_for_add = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]["add_med"], callback_data=f'add_medicament:{id}')
        btn_for_delete = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]["delete_med"], callback_data=f'delete:{id}')
        markup.row(btn_for_add, btn_for_delete)
        markup.row(btn_for_back)
        bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]["what_u_can"], reply_markup=markup)


#The function receives all objects from the drug table and displays them for the user and prompts
#them to select. The choice is made by message from the user. If the message format is
#incorrect, the function processes it and asks the user to try again.
def add_medicament(bot, message, id):
    if user_languages[message.chat.id] == 'ru':
        bot.send_message(message.chat.id, 'Для добавления лекарства напишите его название из списка 📝💊.')
    else:
        bot.send_message(message.chat.id, 'To add a medicine, write its name from the list 📝💊.')
    bot.register_next_step_handler(message, lambda msg: choice_of_med(bot, msg, id))


#The choice is made by message from the user. If the message format is
#incorrect, the function processes it and asks the user to try again.
def choice_of_med(bot, message, id):
    choice = message.text.capitalize()
    conn = sqlite3.connect('../src/base_tg.sql')
    cur = conn.cursor()
    cur.execute('SELECT COUNT(*) FROM medicament WHERE name = ?', (choice,))
    count = cur.fetchone()[0]
    if count < 1:
        bot.reply_to(message, translations[user_languages[message.chat.id]]["no_med_in_list"])
        bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]["write_med_name"])
        conn.commit()
        cur.close()
        conn.close()
        bot.register_next_step_handler(message, lambda msg: choice_of_med(bot, msg, id))
    else:
        cur.execute('SELECT * FROM medicament WHERE name = ?', (choice,))
        medicament = cur.fetchone()
        cur.execute('SELECT * FROM user_med WHERE id_user = ? AND id_med = ?', (id, medicament[0],))
        existence = cur.fetchone()
        conn.commit()
        cur.close()
        conn.close()
        if existence is not None:
            markup = types.InlineKeyboardMarkup()
            btn_for_back = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]["back"], callback_data=f'back:{id}')
            markup.row(btn_for_back)
            if user_languages[message.chat.id] == 'ru':
                bot.reply_to(message, 'Это лекарство уже есть в вашем списке 💊! '
                                    '\n\nПожалуйста, проверьте ваш список, прежде чем добавлять новое. Если вам нужно внести изменения, просто дайте знать!', reply_markup=markup)
            else:
                bot.reply_to(message, 'Это лекарство уже есть в вашем списке 💊! '
                                     '\n\nПожалуйста, проверьте ваш список, прежде чем добавлять новое. Если вам нужно внести изменения, просто дайте знать!', reply_markup=markup)
        else:
            markup = types.InlineKeyboardMarkup()
            if user_languages[message.chat.id] == 'ru':
                bot.reply_to(message, f'Вы выбрали: {medicament[1]} 💊.'
                                    f'\nПринимать его стоит по {medicament[2]} грамм за один прием 📏.'
                                    f'\nЧастота приема - {medicament[3]} раза в день 📅.')
                btn_for_agreement = types.InlineKeyboardButton('Да✅', callback_data=f'answer_yes:{id}:{medicament[0]}')
                btn_for_disagreement = types.InlineKeyboardButton('Нет🚫', callback_data=f'answer_no:{id}:{medicament[0]}')
            else:
                bot.reply_to(message, f'You selected: {medicament[1]} 💊.'
                                      f'\nIs worth taken {medicament[2]} grams at day 📏.'
                                      f'\nFrequency of medicine use - {medicament[3]} times a day 📅.')
                btn_for_agreement = types.InlineKeyboardButton('Yes✅', callback_data=f'answer_yes:{id}:{medicament[0]}')
                btn_for_disagreement = types.InlineKeyboardButton('No🚫', callback_data=f'answer_no:{id}:{medicament[0]}')
            markup.row(btn_for_agreement, btn_for_disagreement)
            bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]["helper"])
            bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]["note_add"], reply_markup=markup)

#The last step of executing the function is to add a new row to the user_med table
#(if the user wants to add a note: the function is called adding_note)
def last_step_adding(bot, message, user_id, med_id, answer):
    if answer:
        bot.reply_to(message, translations[user_languages[message.chat.id]]["write_note"])
        bot.register_next_step_handler(message, lambda msg: adding_note(bot, msg, user_id, med_id))
    else:
        conn = sqlite3.connect('../src/base_tg.sql')
        cur = conn.cursor()
        cur.execute("INSERT INTO user_med (id_user, id_med) VALUES ('%s', '%s')" % (user_id, med_id))
        cur.execute("SELECT * FROM medicament WHERE id = ?", (med_id,))
        value = int(cur.fetchone()[3])
        conn.commit()
        cur.close()
        conn.close()

        markup = types.InlineKeyboardMarkup()
        if user_languages[message.chat.id] == 'ru':
            btn_for_not_remind = types.InlineKeyboardButton('Ничего не изменять 🙅‍♂️',
                                                            callback_data=f'remind:{user_id}:{med_id}:{value}:0')
            btn_for_reminder = types.InlineKeyboardButton('Установить напоминание раньше ⏰',
                                                        callback_data=f'remind:{user_id}:{med_id}:{value}:1')
            bot.send_message(message.chat.id, 'Ваше лекарство успешно добавлено ✅💊!')
        else:
            btn_for_not_remind = types.InlineKeyboardButton("Don't change anything 🙅‍♂️",
                                                            callback_data=f'remind:{user_id}:{med_id}:{value}:0')
            btn_for_reminder = types.InlineKeyboardButton('Set a reminder earlier ⏰',
                                                          callback_data=f'remind:{user_id}:{med_id}:{value}:1')
            bot.send_message(message.chat.id, 'Your medicine has been added successfully ✅💊!')

        markup.row(btn_for_not_remind, btn_for_reminder)

        bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]["remind_text"], reply_markup=markup)
def adding_note(bot, message, user_id, med_id):
    note = message.text.capitalize()
    conn = sqlite3.connect('../src/base_tg.sql')
    cur = conn.cursor()
    cur.execute("INSERT INTO user_med (id_user, id_med, notes) VALUES ('%s', '%s', '%s')" % (user_id, med_id, note))
    cur.execute("SELECT * FROM medicament WHERE id = ?", (med_id,))
    value = int (cur.fetchone()[3])
    conn.commit()
    cur.close()
    conn.close()

    markup = types.InlineKeyboardMarkup()
    if user_languages[message.chat.id] == 'ru':
        btn_for_not_remind = types.InlineKeyboardButton('Ничего не изменять 🙅‍♂️',
                                                       callback_data=f'remind:{user_id}:{med_id}:{value}:0')
        btn_for_reminder = types.InlineKeyboardButton('Установить напоминание раньше ⏰',
                                                      callback_data=f'remind:{user_id}:{med_id}:{value}:1')
        bot.send_message(message.chat.id, 'Ваше лекарство успешно добавлено ✅💊!')
    else:
        btn_for_not_remind = types.InlineKeyboardButton("Don't change anything 🙅‍♂️",
                                                        callback_data=f'remind:{user_id}:{med_id}:{value}:0')
        btn_for_reminder = types.InlineKeyboardButton('Set a reminder earlier ⏰',
                                                      callback_data=f'remind:{user_id}:{med_id}:{value}:1')
        bot.send_message(message.chat.id, 'Your medicine has been added successfully ✅💊!')

    markup.row(btn_for_not_remind, btn_for_reminder)

    bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]["remind_text"], reply_markup=markup)


def remind(bot, message, user_id, med_id, value):
    time_remind_early = int(message.text)
    time_app(bot, message, user_id, med_id, value, time_remind_early)
def decrease_time(time_options, minutes):
    for key, times in time_options.items():
        new_times = []
        for time_str in times:
            # Преобразуем строку времени в объект datetime
            time_obj = datetime.strptime(time_str, '%H:%M')
            # Вычитаем 2 часа
            new_time_obj = time_obj - timedelta(minutes=minutes)
            # Преобразуем обратно в строку
            new_time_str = new_time_obj.strftime('%H:%M')
            new_times.append(new_time_str)
        # Обновляем словарь
        time_options[key] = new_times
def time_app(bot, message, user_id, med_id, value, time_remind_early):
    time_options = {
        1: ["15:00"],
        2: ["09:00", "21:00"],
        3: ["07:00", "15:00", "23:00"],
        4: ["07:00", "12:20", "17:40", "23:00"],
        5: ["07:00", "11:00", "15:00", "19:00" ,"23:00"]
    }

    if time_remind_early is not None:
        decrease_time(time_options, time_remind_early)


    selected_time = time_options[value]
    info = ""

    for el in selected_time:
        info += f'{el} '
        now = datetime.now()
        scheduled_time = datetime.strptime(el, '%H:%M').replace(year=now.year, month=now.month, day=now.day)
        if scheduled_time < now:
            scheduled_time += timedelta(days=1)
        running_thread = threading.Thread(target=send_daily_message, args=(bot, message, message.chat.id, med_id, user_id, scheduled_time))
        running_thread.start()
        print(f"поток включен на {el}")
    markup = types.InlineKeyboardMarkup()
    btn_for_back = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]["back"], callback_data=f'back:{user_id}')
    markup.row(btn_for_back)
    if user_languages[message.chat.id] == 'ru':
        bot.send_message(message.chat.id, f"Вы будете получать напоминания о приёме 💊 в {info} 📅.", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f"You will receive appointment reminders 💊 at {info} 📅.", reply_markup=markup)


def send_daily_message(bot, message, chat_id, med_id, user_id, scheduled_time):
    conn = sqlite3.connect('../src/base_tg.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_med WHERE id_user = ? AND id_med = ?", (user_id, med_id,))
    check = cur.fetchone()
    while check:
        now = datetime.now()
        if scheduled_time:
            # Вычисляем задержку до следующего отправления
            next_send_time = scheduled_time.replace(year=now.year, month=now.month, day=now.day)

            if next_send_time < now:
                next_send_time += timedelta(days=1)

            wait_time = (next_send_time - now).total_seconds()
            time.sleep(wait_time)  # Ждем до следующего отправления

            markup = types.InlineKeyboardMarkup()
            btn_for_applying = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]["mark_taking"],
                                                          callback_data=f'applying:{user_id}:{med_id}')
            markup.row(btn_for_applying)

            cur.execute("SELECT * FROM medicament WHERE id = ?", (med_id,))
            med = cur.fetchone()[1]
            cur.execute("SELECT * FROM user_med WHERE id_user = ? AND id_med = ?", (user_id, med_id,))
            check = cur.fetchone()
            if check:
                text = f"{translations[user_languages[message.chat.id]]['daily_remind']} {med}"
                bot.send_message(chat_id, text, reply_markup=markup)

    cur.close()
    conn.close()
    print("Поток остановлен")


def apply(user_id, med_id):
    conn = sqlite3.connect('../src/base_tg.sql')
    cur = conn.cursor()

    cur.execute("SELECT * FROM user_med WHERE id_user = ? AND id_med = ?", (user_id, med_id,))

    now = datetime.now()
    time_applying = now.strftime("%d.%m.%Y %H:%M")

    info = cur.fetchone()[3]
    if info is None:
        info = time_applying
    else:
        info += f";{time_applying}"

    cur.execute("UPDATE user_med SET time_app = ? WHERE id_user = ? AND id_med = ?", (info, user_id, med_id,))
    conn.commit()
    cur.close()
    conn.close()


def history(bot, message, user_id):
    conn = sqlite3.connect('../src/base_tg.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM user_med WHERE id_user = ?", (user_id,))
    queue = cur.fetchall()
    markup = types.InlineKeyboardMarkup()
    btn_for_back = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]['back'], callback_data=f'back:{user_id}')
    markup.row(btn_for_back)
    if not queue:
        bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]['no_history'], reply_markup=markup)
    else:
        i = 1
        info = ""
        if user_languages[message.chat.id] == 'ru':
            for el in queue:
                if el[3]:
                    cur.execute("SELECT * FROM medicament WHERE id = ?", (el[1],))
                    name = cur.fetchone()[1]
                    info += f"{i}) Лекарство - {name} 🌿. Вы принимали его:\n"
                    for qe in el[3].split(';'):
                        info += f'{qe}\n'
                    info += '\n\n'
                    i += 1
        else:
            for el in queue:
                if el[3]:
                    cur.execute("SELECT * FROM medicament WHERE id = ?", (el[1],))
                    name = cur.fetchone()[1]
                    info += f"{i}) Medicine - {name} 🌿. You took it:\n"
                    for qe in el[3].split(';'):
                        info += f'{qe}\n'
                    info += '\n\n'
        if info:
            bot.send_message(message.chat.id, info, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]['no_history'], reply_markup=markup)
    cur.close()
    conn.close()


#function for removing a medicine from the user's list by accessing the medicament table,
#taking its id and removing this medicine from the user_med table
def delete_medicament(bot, message, id):
    conn = sqlite3.connect('../src/base_tg.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM user_med WHERE id_user = ?', (id,))
    list_com = cur.fetchall()

    i = 1
    if user_languages[message.chat.id] == 'ru':
        for el in list_com:
            cur.execute('SELECT * FROM medicament WHERE id = ?', (el[1],))
            med = cur.fetchone()
            bot.send_message(message.chat.id, f'{i}) Лекарство 🌿: {med[1]}')
            i += 1
    else:
        for el in list_com:
            cur.execute('SELECT * FROM medicament WHERE id = ?', (el[1],))
            med = cur.fetchone()
            bot.send_message(message.chat.id, f'{i}) Medicine 🌿: {med[1]}')
            i += 1
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]['name_med_to_delete'])
    bot.register_next_step_handler(message, lambda msg: deleting(bot, msg, id))
def deleting(bot, message, id):
    med_name = message.text.capitalize()
    try:
        conn = sqlite3.connect('../src/base_tg.sql')
        cur = conn.cursor()
        cur.execute('SELECT * FROM medicament WHERE name = ?', (med_name,))
        id_med = cur.fetchone()[0]
        cur.execute('DELETE FROM user_med WHERE id_user = ? AND id_med = ?', (id, id_med))
        conn.commit()
        cur.close()
        conn.close()
        markup = InlineKeyboardMarkup()
        btn_for_back = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]['back'], callback_data=f'back:{id}')
        btn_for_users_med = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]['user_med'], callback_data=f'users_medicament:{id}')
        markup.row(btn_for_users_med, btn_for_back)
        if user_languages[message.chat.id] == 'ru':
            bot.reply_to(message, f'Лекарство - {med_name} успешно удалено ✅🗑️!', reply_markup=markup)
        else:
            bot.reply_to(message, f'Medicine - {med_name} successfully deleted ✅🗑️!', reply_markup=markup)
    except TypeError:
        if user_languages[message.chat.id] == 'ru':
            bot.reply_to(message, 'Данного лекарства и так нет в вашем списке. 🤷‍♂️')
            bot.send_message(message.chat.id, 'Введите название лекарства еще раз 🔁')
        else:
            bot.reply_to(message, 'This medicine is not on your list anyway. 🤷‍♂️')
            bot.send_message(message.chat.id, 'Enter the name of the medicine again 🔁')
        bot.register_next_step_handler(message, lambda msg: deleting(bot, msg, id))