import requests
from config import weather_url, headers
from bs4 import BeautifulSoup

r = requests.get(weather_url, headers=headers)
bs = BeautifulSoup(r.text, 'lxml')


def weather_now():
    weather_now = bs.find('span', class_='unit unit_temperature_c')
    weather_conditions = bs.find('a', class_='weathertab weathertab-link tooltip').get('data-text').lower()
    return f'Погода сейчас: {weather_now.text}, {weather_conditions}.'


def weather_tomorrow():
    weather_tomorrow_min = bs.find('div', style='top: 9px;width: 50%;').find('span', class_='unit unit_temperature_c')
    weather_tomorrow_max = bs.find('div', style='top: 0px;width: 50%;').find('span', class_='unit unit_temperature_c')
    weather_tomorrow_conditions = bs.find('a', class_='weathertab weathertab-link tooltip', href='/weather-moscow-4368/tomorrow/').get('data-text').lower()
    return f'Погода завтра от {weather_tomorrow_min.text} до {weather_tomorrow_max.text}, {weather_tomorrow_conditions}'
