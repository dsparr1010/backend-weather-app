from dotenv import load_dotenv
import click
import requests
import json
import os
from datetime import datetime

load_dotenv()
OW_TOKEN = os.environ.get('OW_TOKEN')
MQ_TOKEN = os.environ.get('MQ_TOKEN')

coordinates = []
formatted_coord_list = []

class Directions:
    
    def __init__(self, start_address, work_address):
        self.start_address = start_address
        self.work_address = work_address
        
    
    def get_directions(self):
        MQ_res = requests.get(
            f'http://www.mapquestapi.com/directions/v2/route?key={MQ_TOKEN}&from={self.start_address}&to={self.work_address}')
        MQ_res.raise_for_status()
        MQ_dictionary = MQ_res.json()
        MQ_miles = MQ_dictionary['route']['distance']
        toll_checker = MQ_dictionary['route']['hasTollRoad']
        formattedTime = MQ_dictionary['route']['formattedTime']
        real_time = MQ_dictionary['route']['realTime']
        # Destructuring coord info: (ul = upper left; lr = lower right)
        bounding_box_lng1, bounding_box_lat1, bounding_box_lng2, bounding_box_lat2 = MQ_dictionary['route']['boundingBox']['lr']['lng'], MQ_dictionary['route']['boundingBox']['lr']['lat'], MQ_dictionary['route']['boundingBox']['ul']['lng'], MQ_dictionary['route']['boundingBox']['ul']['lat']
        res_coordinate = bounding_box_lng1, bounding_box_lat1, bounding_box_lng2, bounding_box_lat2
        coordinates.append(res_coordinate)
        
        # format seconds to minutes
        real_time = int(round(real_time / 60))
        
        # format coordinates to be able to input into next API call to get traffic information (boudingBox)
        for x in coordinates[0]:
            # stringify rounded coords to prepare to join
            formatted_coord = str(round(x, 2))
            formatted_coord_list.append(formatted_coord)
        
        string_coordinates = ','
        string_coordinates = string_coordinates.join(formatted_coord_list)
          
        direction_data = {'total_miles' : MQ_miles, 'tolls' : toll_checker, 'formatted_time' : formattedTime, 
                          'unformatted_coordinates' : coordinates, 'real_time' : real_time, 
                          'formatted_coordinates' : string_coordinates }            

        # return just data
        return direction_data
    
    def get_traffic_info(self, format_coors):
        # USING FOR EXAMPLE TO HANDLE TRAFFIC DATA W INCIDENCE
        try:
            traffic_res = requests.get(
            f'http://www.mapquestapi.com/traffic/v2/incidents?key={MQ_TOKEN}&boundingBox={format_coors}')
            # traffic_res = requests.get(f'http://www.mapquestapi.com/traffic/v2/incidents?key={MQ_TOKEN}&boundingBox=39.95,-105.25,39.52,-104.71')
            traffic_res.raise_for_status()
            traffic_dictionary = traffic_res.json()
            if len(traffic_dictionary['incidents']) == 0 or traffic_dictionary['incidents'] == []:
                return False
            else:
                incident_data = traffic_dictionary['incidents']
                
                # filter to search for severity > 0, filter looks for true or false
                # lambda (anon function) will receive each instance to compare
                filtered_list = map(lambda x:x['shortDesc'], filter(lambda x: x['impacting'], incident_data))
                for incidents in filtered_list:
                    return incidents
                    
                
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            raise SystemExit(e)
    
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