from dotenv import load_dotenv
from operator import itemgetter
from directions import Directions
import json
import os
import click
import requests

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
        # make responses in json format to easily access data
        response_dictionary = response.json()
        main, description = response_dictionary['weather'][0]['main'], response_dictionary['weather'][0]['description']
        current_temp, low_temp, high_temp = int(round(response_dictionary['main']['temp'])), int(round(response_dictionary['main']['temp_min'])), int(round(response_dictionary['main']['temp_max']))
        click.echo(f'The weather in {city} is currently described as : {main.lower()} with {description}\n'+
                   f"The current temperature is {current_temp}\N{DEGREE SIGN} with a low of {low_temp}\N{DEGREE SIGN} and a high of {high_temp}\N{DEGREE SIGN}"
                   )
        drive_day = input('Are you driving to work today?')
        if city == 'chicago' and drive_day == 'yes':
            newDir = Directions(start_address, work_address)
            getDir = newDir.get_directions(start_address, work_address)
            print(getDir)
            print(newDir.to_address)
            print(newDir.from_address)
            
            
            
            # MQ_res = requests.get(
            #     f'http://www.mapquestapi.com/directions/v2/route?key={MQ_TOKEN}&from={start_address}&to={work_address}')
            
            # MQ_res.raise_for_status()
            # MQ_dictionary = MQ_res.json()
            # MQ_miles = MQ_dictionary['route']['distance']
            # click.echo(f'It will take approximately xminutes to travel the {MQ_miles} to work.')
            
        # print(MQ_dictionary)
    
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    
