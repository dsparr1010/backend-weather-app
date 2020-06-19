from dotenv import load_dotenv
from operator import itemgetter 
import json
import os
import click
import requests

load_dotenv()
TOKEN = os.environ.get('TOKEN')



@click.command()
@click.option('--string', default = 'World', help='This is the string that is greeted')
@click.argument('name', default='guest')
def cli(string, name):
    '''This script greets'''
    name = input('What\'s your name?\n')
    city = input(f'Hello {name}! What city would you like the weather for?').lower()
    try:
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={TOKEN}')
        response.raise_for_status()
        current_weather = response.json()['weather']
        main = list(map(itemgetter('main'), current_weather))
        #for main, description in current_weather:
            #print(main, description) 
        click.echo(f'The weather in {city} is currently {main[0]}')

    
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)