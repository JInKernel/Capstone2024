import os
import time
import mysql.connector
from mysql.connector import Error

def wait_for_db():
    while True:
        try:
            connection = mysql.connector.connect(
                host=os.getenv('DB_HOST'),
                user=os.getenv('DB_USER'),
                password=os.getenv('DB_PASSWORD'),
                database=os.getenv('DB_NAME')
            )
            if connection.is_connected():
                print("Successfully connected to the database.")
                connection.close()
                break
        except Error as e:
            print("Error while connecting to MySQL", e)
            print("Retrying in 5 seconds...")
            time.sleep(5)

if __name__ == "__main__":
    wait_for_db()