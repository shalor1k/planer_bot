import telebot
from telebot import types
import quickstart

TOKEN = 'token'

bot = telebot.TeleBot(TOKEN, parse_mode=None)

chooses = []
category = ["Логотип", "Фирменный стиль", "Брендинг", "Носитель стиля", "Нейминг", "Проверка названия", "Слоган"]


@bot.message_handler(commands=['help', 'start'])
def start(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton(text="Логотип"))
    markup.add(types.KeyboardButton(text="Фирменный стиль"))
    markup.add(types.KeyboardButton(text="Брендинг"))
    markup.add(types.KeyboardButton(text="Носитель стиля"))
    markup.add(types.KeyboardButton(text="Нейминг"))
    markup.add(types.KeyboardButton(text="Проверка названия"))
    markup.add(types.KeyboardButton(text="Слоган"))

    bot.send_message(message.chat.id, "Здравствуйте, выберите категорию", reply_markup=markup)


@bot.message_handler(content_types=['text'])
def query_handler(message):
    if message.text == "Заново" or message.text in category:
        global chooses
        chooses = []
        chooses.append(message.text)
        msg = bot.send_message(message.chat.id, "Введите название: ")
        bot.register_next_step_handler(msg, name_apply)


def name_apply(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton(text="Да"))
    markup.add(types.KeyboardButton(text="Нет"))
    name_string = message.text
    chooses.append(name_string)
    msg = bot.send_message(message.chat.id, "Вы уверены, что хотите ввести '{}'?".format(chooses[1]),
                           reply_markup=markup)
    bot.register_next_step_handler(msg, name_to_comment)


def name_to_comment(message):
    if message.text == "Да":
        msg = bot.send_message(message.chat.id, "Введите комментарий: ")
        bot.register_next_step_handler(msg, comment)
    elif message.text == "Нет":
        chooses.pop()
        msg = bot.send_message(message.chat.id, "Введите название: ")
        bot.register_next_step_handler(msg, name_apply)


def comment(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton(text="Да"))
    markup.add(types.KeyboardButton(text="Нет"))
    comment_string = message.text
    chooses.append(comment_string)
    msg = bot.send_message(message.chat.id, "Вы уверены, что хотите ввести '{}'?".format(chooses[2]),
                           reply_markup=markup)
    bot.register_next_step_handler(msg, comment_to_data)


def comment_to_data(message):
    if message.text == "Да":
        msg = bot.send_message(message.chat.id, "Введите дату (в формате yyyy-mm-dd): ")
        bot.register_next_step_handler(msg, data)
    elif message.text == "Нет":
        chooses.pop()
        msg = bot.send_message(message.chat.id, "Введите комментарий: ")
        bot.register_next_step_handler(msg, comment)


def data(message):
    data = message.text
    chooses.append(data)
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton(text="Да"))
    markup.add(types.KeyboardButton(text="Нет"))
    msg = bot.send_message(message.chat.id, text="Вы уверены, что хотите ввести '{}'?".format(chooses[3]),
                           reply_markup=markup)
    bot.register_next_step_handler(msg, data_to_restart)


def data_to_restart(message):
    if message.text == "Да":
        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton(text="Да"))
        markup.add(types.KeyboardButton(text="Нет"))
        msg = bot.send_message(message.chat.id, "Вы уверены, что хотите внести этот проект в расписание?",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, apply)
    elif message.text == "Нет":
        chooses.pop()
        msg = bot.send_message(message.chat.id, "Введите дату: ")
        bot.register_next_step_handler(msg, comment)


def apply(message):
    if message.text == "Да":
        type()
        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton(text="Да"))
        msg = bot.send_message(message.chat.id, "Проект внесён в расписание\nХотите внести ещё проект?",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, start)
    elif message.text == "Нет":
        markup = types.ReplyKeyboardMarkup()
        markup.add(types.KeyboardButton(text="Да"))
        msg = bot.send_message(message.chat.id, "Очень жаль, хорошая была задумка\nХотите внести ещё проект?",
                               reply_markup=markup)
        bot.register_next_step_handler(msg, start)


def restart(message):
    markup = types.ReplyKeyboardMarkup()
    markup.add(types.KeyboardButton(text="Заново"))
    msg = bot.send_message(message.chat.id, text="Начать заново?", reply_markup=markup)
    bot.register_next_step_handler(msg, start)


def type():
    time_delta = 0
    if category.index(str(chooses[0])) == 0:
        time_delta = 7
    elif category.index(str(chooses[0])) == 1:
        time_delta = 15
    elif category.index(str(chooses[0])) == 2:
        time_delta = 20
    elif 3 <= category.index(str(chooses[0])) <= 6:
        time_delta = 5
    name_project = chooses[1]
    commentary = chooses[2]
    date = chooses[3]

    quickstart.main(time_delta, name_project, commentary, date)


bot.infinity_polling()

