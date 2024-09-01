import mysql.connector
from mysql.connector import errorcode
from datetime import datetime
from dotenv import load_dotenv
import os

#loads env variables
load_dotenv()


config = {
    'user': os.getenv('user'),
    'password': os.getenv('password'),
    'host': os.getenv('host'),
    'database': os.getenv('DB'),
}

# Function to get user input
def get_user_input():
    first_name = input("Enter first name: ")
    last_name = input("Enter last name: ")
    order_date = input("Enter order date (YYYY-MM-DD): ")
    return first_name, last_name, order_date


insert_data_query = """
INSERT INTO customer_order (first_name, last_name, order_date)
VALUES (%s, %s, %s)
"""

try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    first_name, last_name, order_date = get_user_input()

    cursor.execute(insert_data_query, (first_name, last_name, order_date))
    cnx.commit()

    print("Data inserted successfully.")

except mysql.connector.Error as err:
    print(err.msg)
except ValueError as err:
    print("Invalid input:", err)
else:
    cursor.close()
    cnx.close()
