import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASS = os.environ.get('MYSQL_PASS')

def create_connection():
    try:
        connection = mysql.connector.connect(host=MYSQL_HOST,
                            database=MYSQL_DATABASE,
                            user=MYSQL_USER,
                            password=MYSQL_PASS,
                            get_warnings=True)
        if connection.is_connected():
            print('create connection successful')
            return connection
    except mysql.connector.Error as error:
        print("Failed to create MySQL connection: {}".format(error))
    
    