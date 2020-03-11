# A python program that consumes API to check weather data for cities.

import requests

import json

class WeatherService(object):

    API_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&APPID={}&units=metric";

    API_KEY = "3b31a7e394e41c3a30759dfde1a3383e";

    def __init__(self):
        pass


    def get_weather_data(self, city_name):
        
        r = requests.get(WeatherService.API_URL.format(city_name, WeatherService.API_KEY))

        weather_data = (r.json())

        temp = self._extract_temp(weather_data)

        description = self._extract_desc(weather_data)

        return "Currently, in {}, its {} degrees with {}".format(city_name, temp, description)


    def _extract_temp(self, weatherdata):

        temp = weatherdata['main']['temp']

        return temp


    def _extract_desc(self, weahterdata):

        return weahterdata['weather'][0]['description']


    
