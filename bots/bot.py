from typing import Optional, Callable, Union

from telebot import TeleBot, types, Handler


class MyBot(TeleBot):
    def register_next_step_handler(
            self, message: types.Message, callback: Callable, *args, **kwargs) -> None:
        handler_group_id = ":".join([self.token.split(":")[0], str(message.chat.id)])
        self.register_next_step_handler_by_chat_id(handler_group_id, callback, *args, **kwargs)

    def register_next_step_handler_by_bot_chat_id(
            self, handler_group_id: Union[int, str], callback: Callable, *args, **kwargs) -> None:
        self.next_step_backend.register_handler(handler_group_id, Handler(callback, *args, **kwargs))

    def _notify_next_handlers(self, new_messages):
        for i, message in enumerate(new_messages):
            need_pop = False
            handler_group_id = ":".join([self.token.split(":")[0], str(message.chat.id)])
            handlers = self.next_step_backend.get_handlers(handler_group_id)
            if handlers:
                for handler in handlers:
                    need_pop = True
                    self._exec_task(handler["callback"], message, *handler["args"], **handler["kwargs"])
            if need_pop:
                new_messages.pop(i)  # removing message that was detected with next_step_handler


class NotValidToken:
    pass


class InvalidTokenException(Exception):
    pass


class ProcessUpdates:
    def __init__(self):
        self._bot: Optional[TeleBot] = MyBot(NotValidToken(), parse_mode='HTML')
        self.register_handlers()

    @property
    def bot(self):
        return self._bot

    @bot.setter
    def bot(self, token: str):
        self._bot.token = token

    def start_handler(self, message: types.Message):
        self.bot.send_message(message.chat.id, "salom, ismingiz nima?")
        self.bot.register_next_step_handler(message, self.edited_message_handler)

    def edited_message_handler(self, message):
        self.bot.send_message(message.chat.id, f'yaxshi, {message.text}')

    def register_handlers(self):
        self.bot.register_message_handler(self.start_handler, commands=['start'])

    def run(self, data):
        update = types.Update.de_json(data)
        if isinstance(self.bot.token, NotValidToken):
            raise InvalidTokenException('Token is invalid. You need to set a valid token before process updates')
        self.bot.process_new_updates([update])


process_updates = ProcessUpdates()
