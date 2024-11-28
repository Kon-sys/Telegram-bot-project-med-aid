from telebot import types
from src.text import translations
from src.dictionaries import user_languages


def functional(bot, message, id):
    markup = types.InlineKeyboardMarkup()
    btn_for_visual = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]['all_med'], callback_data=f'all_medicament:{id}')
    btn_for_add = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]['add_med'], callback_data=f'add_medicament:{id}')
    btn_for_users_med = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]['user_med'], callback_data=f'users_medicament:{id}')
    btn_for_search_pharmacies = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]['where_med'], callback_data=f'search_medicament:{id}')
    btn_for_history = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]['history'], callback_data=f'history:{id}')
    markup.row(btn_for_users_med, btn_for_visual)
    markup.row(btn_for_add, btn_for_search_pharmacies)
    markup.row(btn_for_history)
    bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]['your_functional'], reply_markup=markup)

