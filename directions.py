from dotenv import load_dotenv
import click
import requests
import json
import os

load_dotenv()
OW_TOKEN = os.environ.get('OW_TOKEN')
MQ_TOKEN = os.environ.get('MQ_TOKEN')

class Directions:
    def __init__(self, start_address, work_address):
        self.start_address = start_address
        self.work_address = work_address
        print('connected')
        click.echo(self.start_address) # prints address
        
    
    def get_directions(self, start_address, work_address):
        click.echo('in get_direct func')
        MQ_res = requests.get(
            f'http://www.mapquestapi.com/directions/v2/route?key={MQ_TOKEN}&from={self.start_address}&to={self.work_address}')
        MQ_res.raise_for_status()
        MQ_dictionary = MQ_res.json()
        MQ_miles = MQ_dictionary['route']['distance']
        toll_checker = MQ_dictionary['route']['hasTollRoad']
        return f'It will take approximately xminutes to travel the {MQ_miles} to work.'
        
    def __str__(self):
        return f'Stringified info on {self}'
    
    
    @property
    def to_address(self):
        formatted_str = self.work_address.replace('+', ' ')
        return f'To address: {formatted_str}'
    
    @property
    def from_address(self):
        formatted_str = self.start_address.replace(',', ', ')
        return f'From address: {formatted_str}'
    