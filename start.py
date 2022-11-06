from server import Server

if __name__ == "__main__":
    server = Server()

    COMMAND_LIST = {
        "привет": server.command_hi,
        "пока": server.command_bye,
        "погода": server.command_weather,
        "помощь": server.command_help,
    }
    print("Сервер запущен!")
    server.start(COMMAND_LIST)
