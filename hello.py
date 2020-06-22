from dotenv import load_dotenv
from operator import itemgetter
from directions import Directions
from datetime import datetime
import json
import os
import click
import requests
import geocoder
from win10toast import ToastNotifier
toaster = ToastNotifier()

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
    testing_address = 'Denver,CO'
    # name = input('What\'s your name?\n')
    # city = input(f'Hello! What city would you like the weather for?').lower()
    try:
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OW_TOKEN}&units=imperial')
        response.raise_for_status()
        response_dictionary = response.json()
        main, description = response_dictionary['weather'][0]['main'], response_dictionary['weather'][0]['description']
        current_temp, low_temp, high_temp = int(round(response_dictionary['main']['temp'])), int(round(response_dictionary['main']['temp_min'])), int(round(response_dictionary['main']['temp_max']))
        click.echo(f'The weather in {city} is currently described as : {main.lower()} with {description}\n'+
                   f"The current temperature is {current_temp}\N{DEGREE SIGN} with a low of {low_temp}\N{DEGREE SIGN} and a high of {high_temp}\N{DEGREE SIGN}."
                   )
        
        # toaster.show_toast(f"Current temp for {city.capitalize()}", "{current_temp}\N{DEGREE SIGN} with a low of {low_temp}\N{DEGREE SIGN} and a high of {high_temp}\N{DEGREE SIGN}.""}",duration = 10)
        weekday = Directions.is_workday(datetime.date(datetime.now()))
        if weekday:
            drive_to_work = input('It\'s a weekday - Do you want to see the current traffic conditions to work?')
            if drive_to_work == 'yes':
                #direction1 = one variable to hold instance, returns 'dir_data'
                direction1 = Directions(start_address, work_address)
                dir_data = direction1.get_directions()
                formatted_time, total_miles, tolls, real_time = dir_data['formatted_time'], dir_data['total_miles'], dir_data['tolls'], dir_data['real_time']
                has_tolls = click.echo(f'It will take approximately {real_time} minutes to drive the {total_miles} miles to get to {direction1.to_address}.'+
                                  '\nBring change because this route requires tolls.') if tolls else print(f'It will take approximately {real_time} minutes to drive the {total_miles} miles to get to {direction1.to_address}')
                
                click.echo(has_tolls)

                formatted_coordinates = dir_data['formatted_coordinates']
                traffic_data = direction1.get_traffic_info(formatted_coordinates)
                # print(traffic_data)
                if traffic_data:
                    req_traffic_info = input(f'There are incidences on your route to {direction1.to_address}. Would you like details?')
                    if req_traffic_info:
                        click.echo(traffic_data)
                else:
                    click.echo('Your route does not have any traffic outside of the norm - Enjoy')

            else:
                click.echo('add some other func that asks another question')
                
        else:
            click.echo('It\'s the weekend')
                

    
    except requests.exceptions.HTTPError as err:
        raise SystemExit(err)
    
