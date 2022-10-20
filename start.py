from server import Server

if __name__ == "__main__":
    server = Server()

    COMMAND_LIST = {
        "привет": server.command_hi,
        "пока": server.command_bye,
        "сейчас": server.command_weather_now,
        "завтра": server.command_weather_tomorrow
    }
    print("Сервер запущен!")
    server.start(COMMAND_LIST)
