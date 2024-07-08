import mysql.connector
from mysql.connector import errorcode

config = {
    'user': 'root',
    'password': 'root',
    'host': 'localhost',
    'database': 'Food_orders',
}

# SQL statement to create a table
create_table_query = """
CREATE TABLE customer_order (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    order_date DATE
)
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
