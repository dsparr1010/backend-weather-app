from dotenv import load_dotenv
import click
import requests
import json
import os
from datetime import datetime

load_dotenv()
OW_TOKEN = os.environ.get('OW_TOKEN')
MQ_TOKEN = os.environ.get('MQ_TOKEN')

# to work URL
# http://www.mapquestapi.com/traffic/v2/incidents?key=FjAT0vnJcQYYG8oJ9se6Mbayp8mASMC3&boundingBox=-87.71,41.94,-88.02,42.13

# def format_bounding_box(coordinates):
#     for i in coordinates:
#         print(i)
#         return float(round(coordinates[i]))

coordinates = []
formatted_coord_list = []

class Directions:
    def __init__(self, start_address, work_address):
        self.start_address = start_address
        self.work_address = work_address
        
    
    def get_directions(self, start_address, work_address):
        MQ_res = requests.get(
            f'http://www.mapquestapi.com/directions/v2/route?key={MQ_TOKEN}&from={self.start_address}&to={self.work_address}')
        MQ_res.raise_for_status()
        MQ_dictionary = MQ_res.json()
        MQ_miles = MQ_dictionary['route']['distance']
        toll_checker = MQ_dictionary['route']['hasTollRoad']
        formattedTime = MQ_dictionary['route']['formattedTime']
        bounding_box_lng1 = MQ_dictionary['route']['boundingBox']['lr']['lng']
        bounding_box_lat1 = MQ_dictionary['route']['boundingBox']['lr']['lat']
        bounding_box_lng2 = MQ_dictionary['route']['boundingBox']['ul']['lng']
        bounding_box_lat2 = MQ_dictionary['route']['boundingBox']['ul']['lat']
        res_coordinate = bounding_box_lng1, bounding_box_lat1, bounding_box_lng2, bounding_box_lat2
        coordinates.append(res_coordinate)
        
        for x in coordinates[0]:
            formatted_coord = str(round(x, 2))
            formatted_coord_list.append(formatted_coord)
            
            #str(formatted_coord_list

        print(formatted_coord_list)
            
        return f'It will take approximately {formattedTime} to travel the {MQ_miles} miles to {self.to_address}.'
            
    
    @staticmethod
    def is_workday(day):
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True
    
    @property
    def to_address(self):
        formatted_str = self.work_address.replace('+', ' ')
        return formatted_str
    
    @property
    def from_address(self):
        formatted_str = self.start_address.replace(',', ', ')
        return formatted_str

# incident/traffic API is specfic - must have boundingBox rounded to nearest hundredths place and all spaces removed
# Example:boundingBox=39.95,-105.25,39.52,-104.71

class Route_Information(Directions):
    def __init__(self, start_address, work_address):
        super().__init__(start_address, work_address)
        print('In Route info class')
    
    
    