import click
import choice
from controller import insert_into_profile, insert_address, get_pass_by_username, get_user_data
from database_config.db_connection import create_connection
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
import sys
import bcrypt

load_dotenv()

@click.command()
def greeting():
    user_greeting_response = choice.Menu(['Login', 'Create new profile']).ask()
    if user_greeting_response == 'Login':
        print('add some functionality to log in')
        username = choice.Input('Enter your username', str).ask()
        password = choice.Input('Enter your password', str).ask()
        user_id = get_user_data(username, password)['user_id']
        if user_id:
            click.echo('You are logged in! What would you like to do?')
            user_want_response = choice.Menu(['Manage my addresses', 'See the weather', 'Check traffic conditions']).ask()
            return user_want_response
        else:
            click.echo('Incorrect password or username')
            greeting()
        
    else:
        click.echo('creating a new user')
        first_name = choice.Input('What is your first name?', str).ask()
        last_name = choice.Input('What is your last name?', str).ask()
        username = choice.Input('Pick a username?', str).ask()
        password = choice.Input('Enter a password', str).ask()
        email = choice.Input('Enter your email address', str).ask() # can be null
        add_addresses = choice.Binary('Would you like to add addresses to your profile?', True).ask()
        insert_into_profile(first_name, last_name, username, password, email, add_addresses)
        
        if add_addresses:
            user_id = get_user_data(username, password)['user_id']
            add_addresses_prompt(user_id)
            
    
def add_addresses_prompt(user_id):
    name = choice.Input('What is the name of the address you want to save? i.e. Home, Work, or Grandpa\'s', str).ask()
    street = choice.Input('What is the street? i.e. 4311 Saint Lawrnce', str).ask()
    city = choice.Input('City?', str).ask()
    state = choice.Input('What state?', str).ask()
    zip = choice.Input('What is the zip?', int).ask()
    insert_address(name, street, city, state, zip, user_id)


def test_connection():
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        for table in tables:
                print(table)
    except mysql.connector.Error as error:
        print("Failed to SHOW TABLES in MySQL: {}".format(error))
    finally:
        cursor.close()
        connection.close()
        print("MySQL connection is closed")

greeting()
