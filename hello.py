from dotenv import load_dotenv
from operator import itemgetter
from Classes.directions import Directions
from Classes.weather import Weather
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
@click.option('--string', help='This is the string that is greeted')
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
        g = geocoder.ip('me')
        if g.city == "Chicago" or g.city == "Arlington Heights":
            weather = Weather('chicago')
            weather_response = weather.get_weather()
            weather_main = weather.format_main_str(weather_response)
            click.echo(weather_main)
        else:
            city = input('What city would you like the current weather data for?')
            weather = Weather(city)
            weather_response = weather.get_weather()
            weather_main = weather.format_main_str(weather_response)
            click.echo(weather_main)
        
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
    
