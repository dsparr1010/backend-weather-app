import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

load_dotenv()

MYSQL_HOST = os.environ.get('MYSQL_HOST')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE')
MYSQL_USER = os.environ.get('MYSQL_USER')
MYSQL_PASS = os.environ.get('MYSQL_PASS')

def connect():
    """ Connect to MySQL database """
    conn = None
    try:
        conn = mysql.connector.connect(host=MYSQL_HOST,
                                       database=MYSQL_DATABASE,
                                       user=MYSQL_USER,
                                       password=MYSQL_PASS,
                                       get_warnings=True)
        #tinyint synonym for boolean in mysql,
        #accepts 0 (false) or 1 (true)
        mysql_create_table_query = """CREATE TABLE IF NOT EXISTS Profile (
            id int(12) NOT NULL AUTO_INCREMENT PRIMARY KEY,
            first_name varchar(20) NOT NULL,
            last_name varchar(30) NOT NULL,
            username varchar(50) NOT NULL,
            password varchar(50) NOT NULL,
            email varchar(255),
            add_addresses tinyint(1),
            created_stamp timestamp default '0000-00-00 00:00:00',
            updated_stamp timestamp default now() on update now()
        )
        """
        cursor = conn.cursor()
        result = cursor.execute(mysql_create_table_query)
        print("Profile Table created successfully")
        if conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("select database();")
            record = cursor.fetchone()
            print("You're connected to database: ", record)

    except Error as e:
        print(e)

    finally:
        if conn is not None and conn.is_connected():
            cursor.close()
            conn.close()
            print("MySQL connection is closed")


if __name__ == '__main__':
    connect()