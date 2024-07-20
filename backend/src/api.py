from flask import Flask, request, jsonify, session
import mysql.connector
from mysql.connector import errorcode
from flask_cors import CORS
from db_config import db_config
from flask_bcrypt import Bcrypt
from flask_session import Session
from app_config import AppConfig
from uuid import uuid4

app = Flask(__name__)
app.config.from_object(AppConfig)
CORS(app)
bcrypt = Bcrypt(app)
server_session = Session(app)

# Gets DB auth creds
config = db_config().get_config()

def create_db_connection():
    try:
        cnx = mysql.connector.connect(**config)
        return cnx
    except mysql.connector.Error as err:
        print(err)
        return None
    
def get_uuid():
    return uuid4().hex

@app.route('/register', methods=['POST'])
def register_user():
    cnx = create_db_connection()
    if cnx is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    
    cursor = cnx.cursor(dictionary=True)
    
    email = request.json["email"]
    password = request.json["password"]
    first_name = request.json["first_name"]
    last_name = request.json["last_name"]
    customer_id = get_uuid()

    # Check if the user already exists
    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user_exists = cursor.fetchone()

    if user_exists:
        cursor.close()
        cnx.close()
        return jsonify({"error": "Email already exists"}), 409
    
    # If user doesn't exist, create a new user
    try:
        hashed_pwd = bcrypt.generate_password_hash(password)
        insert_query = "INSERT INTO users (customer_id, email, first_name, last_name, pwd) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (customer_id, email, first_name, last_name, hashed_pwd))
        cnx.commit()
        cursor.close()
        cnx.close()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        cnx.rollback()
        cursor.close()
        cnx.close()
        return jsonify({"error": str(e)}), 500


@app.route('/login', methods=['POST'])
def login_user():
    cnx = create_db_connection()
    if cnx is None:
        return jsonify({"error": "Failed to connect to the database"}), 500
    
    cursor = cnx.cursor(dictionary=True)
    
    email = request.json["email"]
    password = request.json["password"]

    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    if user is None or not bcrypt.check_password_hash(user['pwd'], password):
        cursor.close()
        cnx.close()
        return jsonify({"error": "Invalid email or password"}), 401
    
    Session["user_id"] = user['customer_id']
    
    cursor.close()
    cnx.close()
    return jsonify({
        "message": "Login successful",
        "email": email
        }), 200

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
