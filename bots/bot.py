from .telebot_override import MyBot, StateFilter

bot = MyBot(parse_mode='HTML')
bot.add_custom_filter(StateFilter(bot))
