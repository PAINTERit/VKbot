import random

import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import Event, VkEventType, VkLongPoll

import weather
from abstract.abstract_server import AbstractBaseServer, AbstractKeyboardMixin
from config import VK_GROUP_ID, VK_TOKEN


class BaseServer(AbstractBaseServer):
    """
    Используется для создания сессии в ВК и запуска команд.
    """

    _vk = vk_api.VkApi(token=VK_TOKEN)
    _longpoll = VkLongPoll(_vk)

    def start(self, COMMAND_LIST: dict) -> None:
        """
        Запуск команд из словаря.
        :param COMMAND_LIST: dict (словарь с командами)
        :return: None
        """
        self.__commands = COMMAND_LIST

        for event in self._longpoll.listen():
            self._command_worker(event)

    def _command_worker(self, event: Event) -> None:
        """
        Выбираются команды для запуска.
        :param event: Event
        :return: None
        """
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if self.__commands.get(event.text.lower()):
                self.__commands[event.text.lower()](event)
            else:
                self.command_weather_city(event)

    def command_weather_city(self, event: Event) -> None:
        """
        Заглушка для дальнейшего использования.
        :param event: Event
        :return: None
        """
        pass


class UtilsServer(BaseServer):
    """
    Используется для добавления метода отправки сообщения.
    """

    def _send_msg(self, user_id: int, message: str, keyboard: VkKeyboard = None) -> None:
        """
        Метод для отправки сообщения пользователю.
        :param user_id: int (id пользователя)
        :param message: str (сообщение для пользователя)
        :param keyboard: VkKeyboard
        :return: None
        """
        if keyboard:
            params = {
                "user_id": user_id,
                "message": message,
                "random_id": random.randint(1, 10000),
                "keyboard": keyboard.get_keyboard(),
            }
        else:
            params = {
                "user_id": user_id,
                "message": message,
                "random_id": random.randint(1, 10000),
            }
        self._vk.method("messages.send", params)


class Server(UtilsServer):
    """
    Испотзуется для создания методов для бота.
    """

    def __init__(self):
        self.keyboard = KeyboardMixin()

    def command_hi(self, event: Event) -> None:
        """
        Команда приветсвия.
        :param event: Event
        :return: None
        """
        self._send_msg(
            event.user_id,
            "Привет, я бот, показывающий информацию о погодных условиях!",
            keyboard=self.keyboard.get_standart_keyboard(),
        )

    def command_bye(self, event: Event) -> None:
        """
        Команда прощания.
        :param event: Event
        :return: None
        """
        self._send_msg(
            event.user_id, "Пока, приходи завтра!", keyboard=self.keyboard.get_start()
        )

    def command_weather(self, event: Event) -> None:
        """
        Команда для получения погоды.
        :param event: Event
        :return: None
        """
        self._send_msg(
            event.user_id,
            "Введите страну, город или улицу для получения погоды:",
            keyboard=self.keyboard.get_weather(),
        )

    def command_weather_coords(self, event: Event) -> None:
        """
        Команда для получения погоды через геолокацию.
        :param event: Event
        :return: None
        """
        result = self._vk.method(
            "messages.getById",
            {"message_ids": [event.message_id], "group_id": VK_GROUP_ID},
        )
        geo = result["items"][0]["geo"]["coordinates"]
        latitude, longitude = geo["latitude"], geo["longitude"]
        self._send_msg(
            event.user_id,
            weather.get_weather_from_coords(latitude, longitude),
            keyboard=self.keyboard.get_help(),
        )

    def command_weather_city(self, event: Event) -> None:
        """
        Команда для получения погоды через прописанное сообщение от пользователя.
        :param event: Event
        :return: None
        """
        if event.text:
            self._send_msg(
                event.user_id,
                weather.get_weather_from_city(event.text),
                keyboard=self.keyboard.get_help(),
            )
        else:
            self.command_weather_coords(event)

    def command_help(self, event: Event) -> None:
        """
        Команда для вызова помощи.
        :param event: Event
        :return: None
        """
        self._send_msg(
            event.user_id,
            "Вот какие команды я могу исполнить:",
            keyboard=self.keyboard.get_standart_keyboard(),
        )


class KeyboardMixin(VkKeyboard, AbstractKeyboardMixin):
    """
    Используется для создания кнопок в боте.
    """

    @staticmethod
    def get_start() -> VkKeyboard:
        """
        Клавитаутра приветствия.
        :return: VkKeyboard
        """
        keyboard = VkKeyboard()
        keyboard.add_button(label="Привет", color=VkKeyboardColor.POSITIVE)
        return keyboard

    @staticmethod
    def get_standart_keyboard() -> VkKeyboard:
        """
        Стандартная клавитаутра.
        :return: VkKeyboard
        """
        keyboard = VkKeyboard()
        keyboard.add_button(label="Погода", color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button(label="Пока", color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label="Помощь", color=VkKeyboardColor.PRIMARY)
        return keyboard

    @staticmethod
    def get_weather() -> VkKeyboard:
        """
        Клавитаутра геолокации.
        :return: VkKeyboard
        """
        keyboard = VkKeyboard()
        keyboard.add_location_button()
        keyboard.add_line()
        keyboard.add_button(label="Помощь", color=VkKeyboardColor.PRIMARY)
        return keyboard

    @staticmethod
    def get_help() -> VkKeyboard:
        """
        Клавитаутра помощи.
        :return: VkKeyboard
        """
        keyboard = VkKeyboard()
        keyboard.add_button(label="Помощь", color=VkKeyboardColor.PRIMARY)
        return keyboard
