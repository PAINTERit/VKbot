import weather
import random
import vk_api

from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
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
            if event.to_me:
                print('Получено новое сообщение.')
                if self.__commands.get(event.text.lower()):
                    self.__commands[event.text.lower()](event)
                else:
                    self.command_weather_city(event)

    def command_weather_city(self, event):
        pass


class UtilsServer(BaseServer):

    def _send_msg(self, user_id, message, keyboard=None):
        if keyboard:
            params = {
                "user_id": user_id,
                "message": message,
                "random_id": random.randint(1, 10000),
                "keyboard": keyboard.get_keyboard()
            }
        else:
            params = {
                "user_id": user_id,
                "message": message,
                "random_id": random.randint(1, 10000),
            }
        self._vk.method("messages.send", params)


class Server(UtilsServer):

    def __init__(self):
        self.keyboard = KeyboardMixin()

    def command_hi(self, event):
        self._send_msg(
            event.user_id,
            'Привет, я бот, показывающий информацию о погодных условиях!',
            keyboard=self.keyboard.get_standart_keyboard()
        )

    def command_bye(self, event):
        self._send_msg(
            event.user_id,
            f'Пока, {event.user_id}, приходи завтра!',
            keyboard=self.keyboard.get_start()
        )

    def command_weather(self, event):
        self._send_msg(
            event.user_id,
            "Введите город или отправьте геопозицию:",
            keyboard=self.keyboard.get_weather()
        )

    def command_weather_city(self, event):
        self._send_msg(
            event.user_id,
            weather.get_weather(event.text)
        )

    def command_help(self, event):
        self._send_msg(
            event.user_id,
            "Вот какие команды я могу исполнить:",
            keyboard=self.keyboard.get_standart_keyboard()
        )


class KeyboardMixin(VkKeyboard):

    @staticmethod
    def get_start():
        keyboard = VkKeyboard()
        keyboard.add_button(label='Привет', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()

    @staticmethod
    def get_standart_keyboard():
        keyboard = VkKeyboard()
        keyboard.add_button(label='Погода', color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button(label='Пока', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='Помощь', color=VkKeyboardColor.PRIMARY)
        return keyboard

    @staticmethod
    def get_weather():
        keyboard = VkKeyboard()
        keyboard.add_button(label='Помощь', color=VkKeyboardColor.PRIMARY)
        return keyboard
