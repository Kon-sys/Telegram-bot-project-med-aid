translations = {
    'en': {
    #handlers.py
    'hello_message': ". I'm your virtual medical assistant! 🌟"
    "\nI'm here to help you manage your health and remember to take your medications. Here's what I can do for you:"
    "\n1. Medication Reminders: I'll remind you when to take your medications so you can take care of your health without any worries."
    "\n2. Pharmacy Locator: If you need to find a pharmacy near you, just text me the address or name, and I'll help you find the most convenient options."
    "\n3. Medication Information: If you have questions about your medications, I'll help you with dosage information and possible side effects."
    "\n4. Medication History Record: You can keep track of all the medications you've taken, and I'll help you keep track of your records."
    "\n\nJust type /start_sign_in to get started or choose the desired action from the menu. Let's take care of your health together! 💊✨",
    'start_message': "👋 Hello!"
    "\nTo get started, please choose one of the following actions:"
    "\n🔐 Sign in to an existing account"
    "\nIf you already have an account, just enter your login details."
    "\n📝 Register"
    "\nIf you are a new user, register to get access to all the bot's features."
    "\n😶‍🌫️ Forgot your password?"
    "\nIf you have already created an account but can't remember your password, I will help you recover it."
    "\n\nAfter logging in or registering, I will be able to remind you to take your medications and help you find the nearest pharmacies.",
    'forgot_password' : "Forgot your password?",
    'start_registry' : "Register",
    'sign_in' : "Log in to an existing account",
    'input_email' : "📧 Enter your yandex email address",
    'text_for_recovery' : "📧 To recover your password, enter your email address",
    'wait_location' : "Waiting for your geolocation 📍",
    'wait_adress' : "Waiting for your address in the above format 🌏",
    'default' : "😭 I don't understand anything...",
    'remind_early' : "Enter how early I should send you a reminder ⏰ (for example: 15)",

    #functional.py
    'all_med' : "👀 View all medications",
    'add_med' : "💊 Add medicine",
    'user_med' : "👨‍🔬 Your medicines",
    'where_med' : "🔎 Where to buy medicine?",
    'history' : "🧠 History of administration",
    'your_functional' : "👋 Hello! I am your assistant for taking medications and finding pharmacies."
    "\nTo get started, choose one of the following options:"
    "\n🗓️ View all medications - see a list of all the medications I remember."
    "\n💊 Add a medication - you can add a medication and a note for it, and I will remind you not to forget to take these medications."
    "\n📋 View your medications - see your current list of medications and their schedule."
    "\n🔍 Find a pharmacy near you - I will help you find a pharmacy near you."
    "\n💬 Get your medication history - I remember every time you take your medication."
    "\n\nClick the button below to continue!",

    #create_user.py
    'password' : "Enter your password",
    'email_mistake' : "This login is not an email account. 😢 \nPlease enter your email again 🔄:",
    'success_registry' : "Registration was successful. Congratulations! 🎉🥳🎊",
    'user_almost_created' : "This user is already registered ❌, please try again 🔄.\nPlease enter your email",
    'format_mistake' : "Incorrect email 😢, please try again",
    'cong_sign' : "Congratulations on your successful login! 🎉🥳🎊",
    'sign_in_mistake' : "Incorrect email or incorrect password 😢. \nPlease try again or register 🔄.",

    #password_recovery.py
    'send_code' : "Password recovery code sent to",
    'insert_code' : "Enter the code sent to your email 🧑‍💻",
    'new_password' : "Enter your new password:",
    'incorrect_code' : "😱 The code you entered was incorrect ❌, try again 🔄: ",
    'password_updated' : "Your password has been updated successfully! 🎉🥳",
    'user_non_created' : "This user is not registered, try again. 😭\nEnter your email",

    #medicament.py
    'back' : "Back",
    'no_med' : "You have no added medications 😳",
    'message_for_back_or_add' : "😃 You can add a medication or go back to the top",
    'what_u_can' : "😃 You can add a medicine, delete it or return to the beginning",
    'delete_med' : "Delete a medicine from the list 🗑",
    'no_med_in_list' : "This medicine is not on the list 🫣, try again 🔄",
    'write_med_name' : "😄Enter the name of the medicine from the list",
    'helper' : "As a faithful assistant 🤖, I will always tell you when and in what dose to take the medicine 💊, but I still recommend seeking help from trained specialists 👩‍⚕️👨‍⚕️.",
    'note_add' : "Would you like to add a note? 🤔",
    'write_note' : "Write your note",
    'remind_text' : 'You will receive reminders to take your medication 💊 based on how many times you need to take your medication per day 📅. '
    '\n\nBut you can get notifications earlier ⏰ (for example, 10 minutes before your appointment time)!',
    'mark_taking' : "Mark taking your medication✅",
    'daily_remind' : "Daily reminder 📅: It's time to take your 💊",
    'no_history' : "You don't have any medication history available 📜.",
    'name_med_to_delete' : "Enter the name of the medication to delete it 🗑.",

    #pharmacie.py
    'send_location' : "Send geolocation 🌍",
    'write_adress' : "Write the address 📍",
    'adress_format' : "I'll help you find the pharmacy closest to you 🏪, but I need to know your address to do so 📍\n\n"
    "Enter your address in the format:\nMoscow, Pervomayskaya street, 75\n\n"
    "Or you can just send me your geolocation =)",
    'no_waiting_location' : "🤔 I'm not waiting for your geolocation...",
    'no_adress' : "This address does not exist ❌, try again 🔄",
    'input_adress' : "Enter your address 😃",
    },
    'ru': {
        #handlers.py
        'hello_message': ". Я ваш виртуальный помощник по медицинским вопросам! 🌟"
"\nЯ здесь, чтобы помочь вам следить за вашим здоровьем и не забывать о приеме лекарств. Вот что я могу сделать для вас:"
"\n1. Напоминания о приеме лекарств: Я буду напоминать вам о том, когда необходимо принять ваши лекарства, чтобы вы могли заботиться о своем здоровье без лишних забот."
"\n2. Поиск аптек: Если вам нужно найти ближайшую аптеку, просто напишите мне адрес или название, и я помогу вам найти самые удобные варианты."
"\n3. Информация о лекарствах: Если у вас есть вопросы о ваших лекарствах, я помогу вам с информацией о дозировке и возможных побочных эффектах."
"\n4. Запись истории приема: Вы можете вести учет всех принятых лекарств, и я помогу вам отслеживать ваши записи."
"\n\nПросто напишите /start_sign_in, чтобы начать, или выберите нужное действие из меню. Давайте заботиться о вашем здоровье вместе! 💊✨",
        'start_message': "👋 Здравствуйте!"
"\nЧтобы начать работу, пожалуйста, выберите одно из следующих действий:"
"\n🔐 Войти в существующий аккаунт"
"\nЕсли у вас уже есть учетная запись, просто введите свои данные для входа."
"\n📝 Пройти регистрацию"
"\nЕсли вы новый пользователь, зарегистрируйтесь, чтобы получить доступ ко всем функциям бота."
"\n😶‍🌫️ Забыли пароль?"
"\nЕсли вы уже создали аккаунт, но не можете вспомнить пароль, то я помогу вам его восстановить."
"\n\nПосле входа или регистрации я смогу напоминать вам о приеме лекарств и помочь найти ближайшие аптеки.",
        'forgot_password' : "Забыли пароль?",
        'start_registry' : "Пройти регистрацию",
        'sign_in' : "Войти в существующий аккаунт",
        'input_email' : "📧 Введите адрес вашей электронной почты yandex",
        'text_for_recovery' : "📧 Чтобы восстановить пароль, введите адрес вашей электронной почты",
        'wait_location' : "Жду вашу геолокацию 📍",
        'wait_adress' : "Жду ваш адрес в вышеуказанном формате 🌏",
        'default' : "😭 Ничего не понимаю...",
        'remind_early' : "Введите на сколько раньше я должен отправлять вам напоминание ⏰(например: 15)",

        #functional.py
        'all_med' : "👀 Просмотреть все лекарства",
        'add_med' : "💊 Добавить лекарство",
        'user_med' : "👨‍🔬 Ваши лекарства",
        'where_med' : "🔎 Где купить лекарство?",
        'history' : "🧠 История приема",
        'your_functional' : "👋 Привет! Я ваш помощник по приему лекарств и поиску аптек."
"\nЧтобы начать, выберите одну из следующих опций:"
"\n🗓️ Просмотр всех лекарств — просмотрите список всех лекарств, которые я помню."
"\n💊 Добавить лекарство - вы можете добавить лекарство и заметку к нему, а я буду напоминать вам не забывать принимать эти лекарства."
"\n📋 Посмотреть список ваших лекарств — просмотрите ваш текущий список лекарств и их график приема."
"\n🔍 Найти ближайшую аптеку — я помогу вам найти аптеку рядом с вами."
"\n💬 Получить историю вашего приема лекарств — я запоминаю каждый ваш прием лекарства."
"\n\nНажмите на кнопку ниже, чтобы продолжить!",

        #create_user.py
        'password' : "Введите ваш пароль",
        'email_mistake' : "Данный логин не является учетной записью почты. 😢 \nВведите адрес электронной почты еще раз 🔄:",
        'success_registry' : "Регистрация прошла успешно. Поздравляю вас! 🎉🥳🎊",
        'user_almost_created' : "Данный пользователь уже зарегистрирован ❌, попробуйте еще раз 🔄.\nВведите вашу электронную почту",
        'format_mistake' : "Некорректный адрес электронной почты 😢, попробуйте еще раз",
        'cong_sign' : "Поздравляю с успешным входом! 🎉🥳🎊",
        'sign_in_mistake' : "Неверная электронная почта или неверный пароль 😢. \nПопробуйте еще раз или пройдите регистрацию 🔄.",

        #password_recovery.py

        'send_code' : "Код для восстановления пароля отправлена на",
        'insert_code' : "Введите код, отправленный вам на электронную почту 🧑‍💻",
        'new_password' : "Введите новый пароль:",
        'incorrect_code' : "😱 Был введён неверный код ❌, попробуйте еще раз 🔄: ",
        'password_updated' : "Ваш пароль успешно обновлён! 🎉🥳",
        'user_non_created' : "Данный пользователь не зарегистрирован, попробуйте еще раз. 😭\nВведите вашу электронную почту",

        #medicament.py

        'back' : "Назад",
        'no_med' : "У вас нет добавленных лекарств 😳",
        'message_for_back_or_add' : "😃 Вы можете добавить лекарство или вернуться в начало",
        'what_u_can' : "😃 Вы можете добавить лекарство, удалить или вернуться в начало",
        'delete_med' : "Удалить лекарство из списка 🗑",
        'no_med_in_list' : "Данного лекарства нет в списке 🫣, попробуйте еще раз 🔄",
        'write_med_name' : "😄Введите название лекарства из списка",
        'helper' : "Как верный помощник 🤖, я вам всегда подскажу, когда и в какой дозе пить лекарство 💊, но я все же рекомендую обращаться за помощью к обученным специалистам 👩‍⚕️👨‍⚕️.",
        'note_add' : "Желаете ли вы добавить заметку? 🤔",
        'write_note' : "Напишите вашу заметку",
        'remind_text' : 'Вам будут поступать напоминания о приеме 💊 в зависимости от нужного количества приемов лекарства в день 📅. '
                        '\n\nНо вы можете получать уведомления раньше ⏰ (например, за 10 минут до времени приема)!',
        'mark_taking' : "Отметить приём лекарства✅",
        'daily_remind' : "Ежедневное напоминание 📅: Вам пора принять 💊",
        'no_history' : "У вас нет доступной истории приема лекарств 📜.",
        'name_med_to_delete' : "Введите название лекарства, чтобы его удалить 🗑.",

        #pharmacie.py

        'send_location' : "Отравить геолокацию 🌍",
        'write_adress' : "Написать адрес 📍",
        'adress_format' : "Я помогу вам найти ближайшую к вам аптеку 🏪, но для этого мне нужно узнать ваш адрес 📍\n\n"
                     "Введите ваш адрес в формате:\nМосква, улица Первомайская, 75\n\n"
                     "Или можете просто отправить мне вашу геолокацию =)",
        'no_waiting_location' : "🤔 Я не ожидаю вашу геолокацию...",
        'no_adress' : "Данного адреса не существует ❌, попробуйте еще раз 🔄",
        'input_adress' : "Введите ваш адрес 😃",
    }
}
