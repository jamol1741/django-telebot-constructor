from telebot import types

from bots.bot import bot


@bot.message_handler(commands='start')
def start_handler(message: types.Message):
    bot.send_message(message.chat.id, "hi, what's your name?")
    bot.register_next_step_handler(message, process_name_step)


def process_name_step(message: types.Message):
    bot.send_message(message.chat.id, f"welcome, {message.text}")
