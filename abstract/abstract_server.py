from abc import ABC, abstractmethod


class AbstractBaseServer(ABC):
    @abstractmethod
    def start(self, command) -> None:
        """
        Данный метод будет запускать команды из словаря.
        :param command: dict
        :return: None
        """
        pass

    @abstractmethod
    def _command_worker(self, event) -> None:
        """
        Данный метод будет выбирать команду, в зависимости от того, что напишет пользователь.
        :param event: Event
        :return: None
        """
        pass


class AbstractKeyboardMixin(ABC):
    @staticmethod
    @abstractmethod
    def get_start() -> None:
        """
        Клавитаура для начала общения с ботом.
        Данная клавиатура появляется при прощании с ботом.
        :return: None
        """
        pass

    @staticmethod
    @abstractmethod
    def get_standart_keyboard() -> None:
        """
        Клавиатура со всеми основными командами.
        :return: None
        """
        pass

    @staticmethod
    @abstractmethod
    def get_help() -> None:
        """
        Клавиатура помощи. Появляется в конце каждого действия.
        Показывает все основные команды.
        :return: None
        """
        pass