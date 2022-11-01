import weather
import random
import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType
from config import TOKEN


class BaseServer:
    _vk = vk_api.VkApi(token=TOKEN)
    _longpoll = VkLongPoll(_vk)

    def start(self, COMMAND_LIST):
        self.__commands = COMMAND_LIST

        for event in self._longpoll.listen():
            self._command_worker(event)

    def _command_worker(self, event):
        if event.type == VkEventType.MESSAGE_NEW:
            if event.to_me: # привет
                print('Получено новое сообщение.')
                if self.__commands.get(event.text.lower()):
                    self.__commands[event.text.lower()](event)
                else:
                    self.command_weather_city(event)

    def command_weather_city(self, event):
        pass


class UtilsServer(BaseServer):

    def _send_msg(self, user_id, message):
        params = {
            "user_id": user_id,
            "message": message,
            "random_id": random.randint(1, 10000),
        }
        self._vk.method("messages.send", params)


class Server(UtilsServer):

    def command_hi(self, event):
        self._send_msg(
            event.user_id,
            'Привет, я бот, показывающий информацию о погодных условиях!'
        )

    def command_bye(self, event):
        self._send_msg(
            event.user_id,
            f'Пока, {event.user_id}, приходи завтра!'
        )

    def command_weather(self, event):
        self._send_msg(
            event.user_id,
            "Введите город: "
        )

    def command_weather_city(self, event):
        self._send_msg(
            event.user_id,
            weather.get_weather(event.text)
        )

    def command_help(self, event):
        self._send_msg(
            event.user_id,
            'Введите сообщение из списка: "привет", "погода", "пока", "help"'
        )
