from typing import Optional

from telebot import TeleBot, types


class NotValidToken:
    pass


class InvalidTokenException(Exception):
    pass


class ProcessUpdates:
    def __init__(self):
        self._bot: Optional[TeleBot] = TeleBot(NotValidToken(), parse_mode='HTML')
        self.register_handlers()

    @property
    def bot(self):
        return self._bot

    @bot.setter
    def bot(self, token: str):
        self._bot.token = token

    def start_handler(self, message: types.Message):
        self.bot.send_message(message.chat.id, "hello")

    def register_handlers(self):
        self.bot.register_message_handler(self.start_handler, commands=['start'])

    def run(self, data):
        update = types.Update.de_json(data)
        if isinstance(self.bot.token, NotValidToken):
            raise InvalidTokenException('Token is invalid. You need to set a valid token before process updates')
        self.bot.process_new_updates([update])


process_updates = ProcessUpdates()
