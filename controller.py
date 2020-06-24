import mysql.connector
from mysql.connector import Error
import os
from database_config.db_connection import create_connection
import bcrypt



def insert_into_profile(first_name, last_name, username, password, email, add_addresses):
    try:
        connection = create_connection()
        mysql_create_table_query = """CREATE TABLE IF NOT EXISTS Profile (
            user_id int(12) AUTO_INCREMENT PRIMARY KEY,
            first_name varchar(20) NOT NULL,
            last_name varchar(30) NOT NULL,
            username varchar(50) NOT NULL,
            password varchar(250) NOT NULL,
            email varchar(255),
            add_addresses tinyint(1),
            created_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_stamp DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        cursor = connection.cursor()
        cursor.execute(mysql_create_table_query)
        
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        print(hashed)
        
        mysql_insert_query = """INSERT INTO Profile (first_name, last_name, username, password, email, add_addresses) VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (first_name, last_name, username, hashed, email, add_addresses)
        cursor.execute(mysql_insert_query, values)
        connection.commit()
        print('inserted into DB')
    
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
            
def insert_address(name, street, city, state, zip, user_id):
    try:
        connection = create_connection()
        mysql_create_table_query = """CREATE TABLE IF NOT EXISTS Address (
            address_id int(12) AUTO_INCREMENT PRIMARY KEY,
            name varchar(20) NOT NULL,
            street varchar(30) NOT NULL,
            city varchar(50),
            state varchar(50),
            zip int(15),
            user_id int not null,
            FOREIGN KEY(user_id) REFERENCES Profile(user_id) ON UPDATE CASCADE ON DELETE CASCADE,
            created_stamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_stamp DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        cursor = connection.cursor()
        cursor.execute(mysql_create_table_query)
        mysql_insert_query = """INSERT INTO Address (name, street, city, state, zip, user_id) VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (name, street, city, state, zip, user_id)
        cursor.execute(mysql_insert_query, values)
        connection.commit()
        print('address inserted into DB')

    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))
            
def get_user_data(username, password):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        user_id, first_name, last_name, username, pass_in_db, email, add_addresses = get_pass_by_username(username)
        correct_password = check_password(password, pass_in_db)
        
        if correct_password:
            user_data = {
                'user_id' : user_id,
                'first_name' : first_name,
                'last_name' : last_name,
                'username' : username,
                'email' : email,
                'add_addresses' : add_addresses
            }
            print('correct password')
            return user_data
        else:
            return False
        
    except mysql.connector.Error as error:
        print("Failed to insert into MySQL table {}".format(error))

    
def get_hashed_password(plain_text_password):
    return bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))

def get_pass_by_username(username):
    try:
        connection = create_connection()
        cursor = connection.cursor()
        query = "SELECT user_id, first_name, last_name, username, password, email, add_addresses FROM Profile WHERE username = %s"
        this_username = (username ,)
        cursor.execute(query, this_username)
        result = cursor.fetchone()
        return result
        
    except mysql.connector.Error as error:
        print("Failed to find username {}".format(error))

