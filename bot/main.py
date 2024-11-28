import telebot
from handlers import register_handlers


bot = telebot.TeleBot('7474555252:AAGtHPd1XT6YhL9zyZegp4r_KDZmY-Zvsv0')


def main():
    register_handlers(bot)
    bot.polling()


if __name__ == '__main__':
    main()
