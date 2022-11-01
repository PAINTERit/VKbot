import requests
from weather_dict import weather_dict, prec_type, prec_strength, cloudness
from geopy import Nominatim
from config import headers


def get_cords(city):
    geolocator = Nominatim(user_agent="Tester")  # без юзер-фгента не определяет координаты
    location = geolocator.geocode(city)
    return location.latitude, location.longitude


def get_weather(city):
    r = requests.get(
        f"https://api.weather.yandex.ru/v2/forecast?lat={get_cords(city)[0]}&lon={get_cords(city)[1]}&limit=1&hours=false&extra=true",
        headers=headers
    )

    data = r.json()
    temp = data["fact"]["temp"]
    feels_temp = data["fact"]["feels_like"]
    condition = weather_dict[data["fact"]["condition"]]
    wind_speed = data["fact"]["wind_speed"]
    pressure = data["fact"]["pressure_mm"]
    humidity = data["fact"]["humidity"]
    prec_t = prec_type[data["fact"]["prec_type"]]
    prec_s = prec_strength[data["fact"]["prec_strength"]]
    cloud = cloudness[data["fact"]["cloudness"]]

    return (f"Погода в городе: {city}\nТемпература: {temp}°C\n"
          f"Температура по ощущениям: {feels_temp}°C\nПогодные условия: {condition}\n"
          f"Облачность: {cloud}\nТип осадков: {prec_t}\n"
          f"Сила осадков: {prec_s}\nВлажность воздуха: {humidity}%\n"
          f"Скорость ветра: {wind_speed} м/с\nДавление: {pressure} мм рт. ст.\n")
