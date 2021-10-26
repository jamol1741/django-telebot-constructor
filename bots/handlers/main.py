from telebot import types

from bots.bot import bot


@bot.message_handler(commands='start')
def start_handler(message: types.Message):
    cid = message.chat.id
    bot.send_message(cid, "hi, what's your name?")
    bot.current_states.set(cid, 'name')


@bot.message_handler(state='name')
def name_handler(message: types.Message):
    cid = message.chat.id
    bot.send_message(cid, f'welcome, {message.text}')
    bot.current_states.finish(cid)
