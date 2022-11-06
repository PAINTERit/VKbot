import json

import requests
from geopy import Nominatim

import weather_dict
from config import GEOCODER_TOKEN, headers


def get_weather_from_coords(latitude: float, longitude: float) -> str:
    """
    API запрос для получения погоды по координатам.
    :param latitude: float (широта)
    :param longitude: float (долгота)
    :return: str (погода)
    """
    data = requests.get(
        f"https://api.weather.yandex.ru/v2/forecast?lat={latitude}&lon={longitude}&limit=1&hours=false&extra=true",
        headers=headers
    )
    return get_weather_data(data)


def get_weather_from_city(city: str) -> str:
    """
    API запрос для получения погоды по адресу, который преобразуется в координаты.
    :param city: str (адрес от пользователя)
    :return: str (погода)
    """
    geolocator = Nominatim(user_agent="Tester")
    location = geolocator.geocode(city)
    data = requests.get(
        f"https://api.weather.yandex.ru/v2/forecast?lat={location.latitude}&lon={location.longitude}&limit=1&hours=false&extra=true",
        headers=headers
    )
    return get_weather_data(data)


def get_city_from_coords(latitude: float, longitude: float) -> str:
    """
    Запрос для преобразования координат в адрес.
    :param latitude: float (широта)
    :param longitude: float (долгота)
    :return: str (адрес)
    """
    city_data = requests.get(
        f"https://geocode-maps.yandex.ru/1.x/?format=json&apikey={GEOCODER_TOKEN}&geocode={longitude},{latitude}"
    ).json()
    return city_data["response"]["GeoObjectCollection"]["featureMember"][0][
        "GeoObject"]["metaDataProperty"]["GeocoderMetaData"][
        "Address"]["Components"][2]["name"]


def get_weather_data(request: json) -> str:
    """
    Вытягивание данных из json и вывод погодных данных.
    :param request: json (файл с погодой)
    :return: str
    """
    data = request.json()
    lat = data["info"]["lat"]
    lon = data["info"]["lon"]
    city = get_city_from_coords(lat, lon)
    temp = data["fact"]["temp"]
    feels_temp = data["fact"]["feels_like"]
    condition = weather_dict.weather_condition[data["fact"]["condition"]]
    wind_speed = data["fact"]["wind_speed"]
    pressure = data["fact"]["pressure_mm"]
    humidity = data["fact"]["humidity"]
    prec_t = weather_dict.prec_type[data["fact"]["prec_type"]]
    if prec_t == "дождь":
        prec_s = weather_dict.prec_rain_strength[data["fact"]["prec_strength"]]
    elif prec_t == "снег":
        prec_s = weather_dict.prec_snow_strength[data["fact"]["prec_strength"]]
    else:
        prec_s = "без осадков"
    cloud = weather_dict.cloudness[data["fact"]["cloudness"]]

    return (
        f"Погода в городе: {city}\nТемпература: {temp}°C\n"
        f"Температура по ощущениям: {feels_temp}°C\nПогодные условия: {condition}\n"
        f"Облачность: {cloud}\nТип осадков: {prec_t}\n"
        f"Сила осадков: {prec_s}\nВлажность воздуха: {humidity}%\n"
        f"Скорость ветра: {wind_speed} м/с\nДавление: {pressure} мм рт. ст.\n"
    )
