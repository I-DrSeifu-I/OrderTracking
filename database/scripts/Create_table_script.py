import mysql.connector
from mysql.connector import errorcode
from uuid import uuid4
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

# SQL statement to create a table
create_table_query = """
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT,
    menu_id INT,
    quantity INT,
    price DECIMAL(10, 2),
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (menu_id) REFERENCES menu(id)
);

"""

try:
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    cursor.execute(create_table_query)
    print("Table created successfully.")

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
        print("Table already exists.")
    else:
        print(err.msg)
else:
    cursor.close()
    cnx.close()
