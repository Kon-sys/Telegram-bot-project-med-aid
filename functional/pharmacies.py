from geopy.geocoders import Nominatim
from src.dictionaries import user_states_location
import requests
import json
from telebot import types
from src.text import translations
from src.dictionaries import user_languages

def search_medicament(bot, message, id):
    markup = types.InlineKeyboardMarkup()
    btn_for_location = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]['send_location'], callback_data=f'choose_location:{id}')
    btn_for_adress = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]['write_adress'], callback_data=f'choose_adress:{id}')
    markup.row(btn_for_location, btn_for_adress)
    bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]['adress_format'], reply_markup=markup)
    user_states_location[id] = f'awaiting_location'


def getting_location(bot, message, id):
    if (user_states_location.get(id)) == 'awaiting_location':
        latitude = message.location.latitude
        longitude = message.location.longitude

        adress = get_address_from_coordinates(latitude,longitude)

        # Сброс состояния после получения геолокации
        del user_states_location[id]

        view_nearest_pharmacies(bot, message, id, adress)

    else:
        bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]['no_waiting_location'])

def get_adress(bot, message, id):
    adress = message.text.strip()
    if check_adress_exists(adress):
        view_nearest_pharmacies(bot, message, id, adress)
    else:
        bot.reply_to(message, translations[user_languages[message.chat.id]]['no_adress'])
        bot.send_message(message.chat.id, translations[user_languages[message.chat.id]]['input_adress'])
        bot.register_next_step_handler(message, lambda msg: get_adress(bot, msg, id))



def get_address_from_coordinates(latitude, longitude):
    # Формируем URL для запроса к Nominatim с указанием языка
    url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json&accept-language=ru"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Проверяем статус ответа
        data = response.json()

        # Извлекаем компоненты адреса
        address_components = data.get("address", {})
        city = address_components.get("city", "")
        town = address_components.get("town", "")
        village = address_components.get("village", "")
        street = address_components.get("road", "")
        house_number = address_components.get("house_number", "")
        # Форматируем адрес
        city_name = city or town or village
        formatted_address = f"{city_name}, {street}, {house_number}".strip(", ")

        return formatted_address if formatted_address else "Адрес не найден"
    except Exception as e:
        return f"Ошибка: {e}"


def view_nearest_pharmacies(bot, message, id, adress):
    url = "https://google.serper.dev/maps"
    payload = json.dumps({
        "q": f"pharmacie near {adress}",
        "hl": user_languages[message.chat.id]
    })
    headers = {
        'X-API-KEY': '9df2847704d354800bc377faaf66c276f8cd1475',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    data = json.loads(response.text)
    places = data.get('places', [])

    markup = types.InlineKeyboardMarkup()
    btn_for_back = types.InlineKeyboardButton(translations[user_languages[message.chat.id]]['back'], callback_data=f'back:{id}')
    markup.row(btn_for_back)

    i = 0
    if user_languages[message.chat.id] == 'ru':
        for place in places:
            i += 1
            title = place.get('title', 'Неизвестно')
            add = place.get('address', 'Адрес не указан')
            phone = place.get('phoneNumber', 'Телефон не указан')  # Получаем номер телефона
            opening_hours = place.get('openingHours', {})  # Получаем график работы

            # Форматируем график работы
            formatted_hours = format_opening_hours(opening_hours, message)
            if i != 3:
                # Вывод информации
                bot.send_message(message.chat.id, f"Название: {title}, \nАдрес: {transform_address(add, message)}, \nТелефон: {phone}, \nГрафик работы: {formatted_hours if formatted_hours else 'Не указан'}")
            else:
                bot.send_message(message.chat.id, f"Название: {title}, \nАдрес: {transform_address(add, message)}, \nТелефон: {phone}, \nГрафик работы: {formatted_hours if formatted_hours else 'Не указан'}", reply_markup=markup)
                break
    else:
        for place in places:
            i += 1
            title = place.get('title', 'Unknown')
            add = place.get('address', 'Address not specified')
            phone = place.get('phoneNumber', 'Phone number not specified')  # Получаем номер телефона
            opening_hours = place.get('openingHours', {})  # Получаем график работы

            # Форматируем график работы
            formatted_hours = format_opening_hours(opening_hours, message)
            if i != 3:
                # Вывод информации
                bot.send_message(message.chat.id, f"Pharmacy name: {title}, \nAdress: {transform_address(add, message)}, \nPhone number: {phone}, \nWork time: {formatted_hours if formatted_hours else 'Not specified'}")
            else:
                bot.send_message(message.chat.id, f"Pharmacy name: {title}, \nAdress: {transform_address(add, message)}, \nPhone number: {phone}, \nWork time: {formatted_hours if formatted_hours else 'Not specified'}", reply_markup=markup)
                break

def format_opening_hours(opening_hours, message):
    if user_languages[message.chat.id] == 'ru':
        days = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
        hours_dict = {day: opening_hours.get(day, 'Не указано') for day in days}

        # Проверяем, повторяется ли график для всех дней
        all_same = len(set(hours_dict.values())) == 1
        common_hours = hours_dict[days[0]]  # Часы для всех дней, если одинаковые

        if all_same:
            return f"Понедельник-Воскресенье: {common_hours}"
    else:
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        hours_dict = {day: opening_hours.get(day, 'Не указано') for day in days}

        # Проверяем, повторяется ли график для всех дней
        all_same = len(set(hours_dict.values())) == 1
        common_hours = hours_dict[days[0]]  # Часы для всех дней, если одинаковые

        if all_same:
            return f"Monday-Sunday: {common_hours}"
    # Проверяем, повторяется ли график с понедельника по пятницу
    weekday_hours = set(hours_dict[day] for day in days[:5])
    weekend_hours = set(hours_dict[day] for day in days[5:])

    formatted_hours = []

    if len(weekday_hours) == 1:  # Если с понедельника по пятницу график один
        formatted_hours.append(f"{days[0]}-{days[4]}: {hours_dict[days[0]]}")
    else:  # Разные графики
        for day in days[:5]:
            formatted_hours.append(f"{day}: {hours_dict[day]}")

    # Добавляем график для выходных
    if len(weekend_hours) == 1:  # Если в выходные график один
        formatted_hours.append(f"{days[5]}-{days[6]}: {hours_dict[days[5]]}")
    else:  # Разные графики
        for day in days[5:]:
            formatted_hours.append(f"{day}: {hours_dict[day]}")

    return ', '.join(formatted_hours)



def transform_address(address, message):
    # Убираем префикс "Адрес:" если он есть
    if address.startswith("Адрес: "):
        address = address[len("Адрес: "):].strip()

    # Разделяем адрес на части
    parts = address.split(", ")

    # Предполагаем, что первый элемент - это полный адрес
    main_part = parts[0]

    # Проверяем, если последний элемент является почтовым индексом
    if len(parts) > 1:
        postal_info = parts[1]  # Например, "Минск 220013"
        # Извлекаем город
        city_info = postal_info.split()[0]  # Город - это первое слово в postal_info
    else:
        if user_languages[message.chat.id] == 'ru':
            return "Город не найден"
        else:
            return "City not found"

    # Формируем финальный адрес
    if user_languages[message.chat.id] == 'ru':
        transformed_address = f"г.{city_info}, {main_part.replace(city_info, '').strip()}"
    else:
        transformed_address = f"{city_info} city, {main_part.replace(city_info, '').strip()}"

    return transformed_address.strip(", ")


def check_adress_exists(adress):
    geolocator = Nominatim(user_agent="my_unique_app_name_biffs8y28b28side294nd")
    location = geolocator.geocode(adress)
    if location:
        return True
    else:
        return False
