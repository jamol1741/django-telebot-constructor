from typing import Callable, Union

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

    def process_new_updates(self, updates):
        if isinstance(self.token, InvalidToken):
            raise ValueError("Token is not valid. You need to change Bot instance token to valid one")
        super(MyBot, self).process_new_updates(updates)


class InvalidToken:
    pass


bot = MyBot(InvalidToken(), parse_mode='HTML')
