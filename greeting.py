import click
import choice
from db import insert_into_profile
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASS = os.environ.get('MYSQL_PASS')
MYSQL_TABLE = os.environ.get('MYSQL_TABLE')


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

        insert_into_tbl(first_name, last_name, username, password, email, add_addresses)
    
    
greeting()