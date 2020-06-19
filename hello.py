from dotenv import load_dotenv
from operator import itemgetter
from directions import Directions, Route_Information
from datetime import datetime
import json
import os
import click
import requests
import geocoder

load_dotenv()
OW_TOKEN = os.environ.get('OW_TOKEN')
MQ_TOKEN = os.environ.get('MQ_TOKEN')


@click.command()
@click.option('--string', default = 'World', help='This is the string that is greeted')
@click.argument('name', default='guest')
def cli(string, name):
    '''Welcome to My Day Planner'''
    start_address = '3716 W Eddy St,Chicago,IL'
    work_address = '1500+West+Shure+Drive,+Arlington+Heights,+IL'
    city = 'chicago'
    # name = input('What\'s your name?\n')
    # city = input(f'Hello! What city would you like the weather for?').lower()
    try:
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OW_TOKEN}&units=imperial')
        response.raise_for_status()
        response_dictionary = response.json()
        main, description = response_dictionary['weather'][0]['main'], response_dictionary['weather'][0]['description']
        current_temp, low_temp, high_temp = int(round(response_dictionary['main']['temp'])), int(round(response_dictionary['main']['temp_min'])), int(round(response_dictionary['main']['temp_max']))
        click.echo(f'The weather in {city} is currently described as : {main.lower()} with {description}\n'+
                   f"The current temperature is {current_temp}\N{DEGREE SIGN} with a low of {low_temp}\N{DEGREE SIGN} and a high of {high_temp}\N{DEGREE SIGN}"
                   )
        
        
        weekday = Directions.is_workday(datetime.date(datetime.now()))
        if weekday:
            drive_to_work = input('It\'s a weekday - Do you want to see the current traffic conditions to work?')
            if drive_to_work == 'yes':
                newDir = Directions(start_address, work_address)
                getDir = newDir.get_directions(start_address, work_address)
                print(getDir)
                newRouteInfo = Route_Information(newDir.start_address, newDir.work_address)
                print(newRouteInfo.to_address) # access to parent attr - print formatted address
            else:
                click.echo('add some other func that asks another question')
                

    
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    
