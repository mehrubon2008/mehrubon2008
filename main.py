import telebot
from telebot import types
from config import TOKEN
import random

bot = telebot.TeleBot(TOKEN)

user_states = {}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Угадай число")
    item2 = types.KeyboardButton("Камень, Ножницы, Бумага")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Выберите игру:", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Угадай число")
def start_guess_number_game(message):
    user_states[message.chat.id] = {"game": "guess_number", "number_to_guess": random.randint(1, 100)}
    bot.send_message(message.chat.id, "Я загадал число от 1 до 100. Попробуйте угадать!")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) and user_states[message.chat.id]["game"] == "guess_number")
def guess_number(message):
    try:
        guessed_number = int(message.text)
        correct_number = user_states[message.chat.id]["number_to_guess"]

        if guessed_number == correct_number:
            bot.send_message(message.chat.id, "Поздравляю! Вы угадали число!")
            del user_states[message.chat.id]
        elif guessed_number < correct_number:
            bot.send_message(message.chat.id, "Число больше. Попробуйте еще раз.")
        else:
            bot.send_message(message.chat.id, "Число меньше. Попробуйте еще раз.")
    except ValueError:
        bot.send_message(message.chat.id, "Введите целое число.")

@bot.message_handler(func=lambda message: message.text == "Камень, Ножницы, Бумага")
def start_rps_game(message):
    user_states[message.chat.id] = {"game": "rps"}
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Камень")
    item2 = types.KeyboardButton("Ножницы")
    item3 = types.KeyboardButton("Бумага")
    markup.add(item1, item2, item3)
    bot.send_message(message.chat.id, "Выберите свой вариант:", reply_markup=markup)

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) and user_states[message.chat.id]["game"] == "rps")
def play_rps(message):
    user_choice = message.text.lower()
    choices = ["камень", "ножницы", "бумага"]
    bot_choice = random.choice(choices)

    bot.send_message(message.chat.id, f"Ваш выбор: {user_choice}\nМой выбор: {bot_choice}")

    if user_choice in choices:
        if user_choice == bot_choice:
            bot.send_message(message.chat.id, "Ничья!")
        elif (
            (user_choice == "камень" and bot_choice == "ножницы") or
            (user_choice == "ножницы" and bot_choice == "бумага") or
            (user_choice == "бумага" and bot_choice == "камень")
        ):
            bot.send_message(message.chat.id, "Вы выиграли!")
        else:
            bot.send_message(message.chat.id, "Вы проиграли!")
        del user_states[message.chat.id]
    else:
        bot.send_message(message.chat.id, "Выберите камень, ножницы или бумагу.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text not in ["Угадай число", "Камень, Ножницы, Бумага"]:
        bot.send_message(message.chat.id, "Извините, я не понимаю. Пожалуйста, выберите игру.")

print('start')
bot.polling(none_stop=True)
