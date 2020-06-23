import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASS = os.environ.get('MYSQL_PASS')

def insert_into_profile(first_name, last_name, username, password, email, add_addresses):
    try:
        connection = mysql.connector.connect(host=MYSQL_HOST,
                                database=MYSQL_DATABASE,
                                user=MYSQL_USER,
                                password=MYSQL_PASS,
                                get_warnings=True)
        print('db connected')
        mysql_create_table_query = """CREATE TABLE IF NOT EXISTS Profile (
            id int(12) AUTO_INCREMENT PRIMARY KEY,
            first_name varchar(20) NOT NULL,
            last_name varchar(30) NOT NULL,
            username varchar(50) NOT NULL,
            password varchar(50) NOT NULL,
            email varchar(255),
            add_addresses tinyint(1),
            created_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_stamp DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        cursor = connection.cursor()
        cursor.execute(mysql_create_table_query)
        mysql_insert_query = """INSERT INTO Profile (first_name, last_name, username, password, email, add_addresses) VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (first_name, last_name, username, password, email, add_addresses)
        cursor.execute(mysql_insert_query, values)
        connection.commit()
        print('inserted into DB')
    
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        if (connection.is_connected()):
            cursor.close()
            connection.close()
            print("MySQL connection is closed")