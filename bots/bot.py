from telebot.custom_filters import StateFilter

from .telebot_override import MyBot

bot = MyBot(parse_mode='HTML')
bot.add_custom_filter(StateFilter(bot))
