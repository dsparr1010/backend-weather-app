import click
import choice
from db import insert_into_profile, insert_address, get_user_id
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()


@click.command()
def greeting():
    user_greeting_response = choice.Menu(['Login', 'Create new profile']).ask()
    if user_greeting_response == 'Login':
        print('add some functionality to log in')
    else:
        print('creating a new user')
        first_name = choice.Input('What is your first name?', str).ask()
        last_name = choice.Input('What is your last name?', str).ask()
        username = choice.Input('Pick a username?', str).ask()
        password = choice.Input('Enter a password', str).ask()
        email = choice.Input('Enter your email address', str).ask() # can be null
        add_addresses = choice.Binary('Would you like to add addresses to your profile?', True).ask()
        insert_into_profile(first_name, last_name, username, password, email, add_addresses)
        
        if add_addresses:
            user_id = get_user_id(username)
            add_addresses_prompt(user_id)
            
    
def add_addresses_prompt(user_id):
    name = choice.Input('What is the name of the address you want to save? i.e. Home, Work, or Grandpa\'s', str).ask()
    street = choice.Input('What is the street? i.e. 4311 Saint Lawrnce', str).ask()
    city = choice.Input('City?', str).ask()
    state = choice.Input('What state?', str).ask()
    zip = choice.Input('What is the zip?', int).ask()
    insert_address(name, street, city, state, zip, user_id)



greeting()