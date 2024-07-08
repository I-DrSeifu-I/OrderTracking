from flask import Flask, request, jsonify
import mysql.connector
from mysql.connector import errorcode
from flask_cors import CORS
from db_config import db_config

app = Flask(__name__)
CORS(app)  # Enable CORS if needed

# Gets DB auth creds
config = db_config().get_config()

def create_db_connection():
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        print(err)
        return None

# API endpoint to retrieve all customer orders
@app.route('/customer_orders', methods=['GET'])
def get_customer_orders():
    cnx = create_db_connection()
    if not cnx:
        return jsonify({"error": "Unable to connect to the database"}), 500
    cursor = cnx.cursor(dictionary=True)
    query = "SELECT * FROM customer_order"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    cnx.close()
    return jsonify(results)

# API endpoint to add a new customer order
@app.route('/customer_orders', methods=['POST'])
def add_customer_order():
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    order_date = data.get('order_date')
    
    if not all([first_name, last_name, order_date]):
        return jsonify({"error": "Missing required fields"}), 400
    
    cnx = create_db_connection()
    if not cnx:
        return jsonify({"error": "Unable to connect to the database"}), 500
    cursor = cnx.cursor()
    query = "INSERT INTO customer_order (first_name, last_name, order_date) VALUES (%s, %s, %s)"
    cursor.execute(query, (first_name, last_name, order_date))
    cnx.commit()
    cursor.close()
    cnx.close()
    return jsonify({"message": "Customer order added successfully"}), 201

if __name__ == '__main__':
    app.run(debug=True)
