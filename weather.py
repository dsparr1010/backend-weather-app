from dotenv import load_dotenv
import click
import requests
import json
import os
from datetime import datetime

load_dotenv()
OW_TOKEN = os.environ.get('OW_TOKEN')

class Weather:
    def __init__(self, city):
        self.city = city
        
    def get_weather(self):
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={self.city}&appid={OW_TOKEN}&units=imperial')
        response.raise_for_status()
        response_dictionary = response.json()
        main, description = response_dictionary['weather'][0]['main'], response_dictionary['weather'][0]['description']
        current_temp, low_temp, high_temp = int(round(response_dictionary['main']['temp'])), int(round(response_dictionary['main']['temp_min'])), int(round(response_dictionary['main']['temp_max']))
        # click.echo(f'The weather in {city} is currently described as : {main.lower()} with {description}\n'+
        #            f"The current temperature is {current_temp}\N{DEGREE SIGN} with a low of {low_temp}\N{DEGREE SIGN} and a high of {high_temp}\N{DEGREE SIGN}."
        #            )
        weather_data = {'main' : main, 'description' : description, 'current_temp' : current_temp, 'low_temp' : low_temp, 'high_temp' : high_temp}
        return weather_data

    def format_main_str(self, weather_data):
        main, description, current_temp, low_temp, high_temp = weather_data['main'], weather_data['description'], weather_data['current_temp'], weather_data['low_temp'], weather_data['high_temp']
        return (f'The weather in {self.city} is currently described as : {main} with {description}\n'+
            f"The current temperature is {current_temp}\N{DEGREE SIGN} with a low of {low_temp}\N{DEGREE SIGN} and a high of {high_temp}\N{DEGREE SIGN}.")
            
        
        