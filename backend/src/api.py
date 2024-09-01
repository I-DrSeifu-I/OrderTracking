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
CORS(app, supports_credentials=True)
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
        insert_query = "INSERT INTO users (email, first_name, last_name, password) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_query, (email, first_name, last_name, hashed_pwd))
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
    
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Invalid input"}), 400
    
    email = data["email"]
    password = data["password"]

    query = "SELECT * FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user = cursor.fetchone()

    if user is None or not bcrypt.check_password_hash(user['password'], password):
        cursor.close()
        cnx.close()
        return jsonify({"error": "Invalid email or password"}), 401
    
    # Store the user ID in the session
    session["user_id"] = user['id']
    
    cursor.close()
    cnx.close()
    return jsonify({
        "message": "Login successful",
        "email": email
    }), 200


@app.route('/logout', methods=['POST'])
def logout_user():
    session.pop("user_id", None)
    return jsonify({"message": "Logout successful"}), 200


@app.route('/get_orders', methods=['GET'])
def get_orders():

    #gets the user ID from the current session
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({"error":"User is not logged in" }), 401
    
    cnx = create_db_connection()
    if cnx is None:
        return jsonify({"error": "Unable to connect to database"}), 500
    
    cursor = cnx.cursor(dictionary=True)

    query = """
    SELECT o.id AS order_id, o.order_date, o.total_amount, u.email
    FROM orders o
    JOIN users u ON o.user_id = u.id
    WHERE o.user_id = %s
    ORDER BY o.order_date DESC
    """
    cursor.execute(query, (user_id,))

    orders = cursor.fetchall()

    cursor.close()
    cnx.close()

    return jsonify({"orders":orders}), 200

@app.route('/get_menu', methods=['GET'])
def get_menu():
    user_id = session.get('user_id')
    print(f"Retrieved session user_id: {user_id}")

    if not user_id:
        return jsonify({"error": "User is not logged in"}), 401
    
    cnx = create_db_connection()
    if cnx is None:
        return jsonify({"error": "Unable to connect to database"}), 500
    
    cursor = cnx.cursor(dictionary=True)
    try:
        query = "SELECT * FROM menu"
        cursor.execute(query)

        menu = cursor.fetchall()

        cursor.close()
        cnx.close()

        return jsonify(menu), 200
    except Exception as e:
        return jsonify({"error": f"Unable to return menu items, {e}"}), 500



@app.route('/order_food', methods=['POST'])
def order_food():
    data = request.json
    order_item_number = data.get('order_item_number')
    quantity_of_food = data.get('quantity')
    user_id = session.get("user_id")
    status = "Pending"

    if quantity_of_food is None or not isinstance(quantity_of_food, int):
        return jsonify({"error": "Invalid quantity provided"}), 400

    cnx = create_db_connection()
    if not cnx:
        return jsonify({"error": "Unable to connect to the database"}), 500

    try:
        cursor = cnx.cursor(dictionary=True)
        
        # Get the price of the menu item
        query = "SELECT price FROM menu WHERE id = %s"
        cursor.execute(query, (order_item_number,))
        menu_item = cursor.fetchone()

        if not menu_item:
            return jsonify({"error": "Menu item not found"}), 404

        try:
            menu_item_price = float(menu_item["price"])  # Convert to float if necessary
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid price data in menu"}), 500

        try:
            quantity_of_food = int(quantity_of_food)  # Convert to integer if necessary
        except (TypeError, ValueError):
            return jsonify({"error": "Invalid quantity data"}), 400

        total_price = menu_item_price * quantity_of_food

        query = "INSERT INTO orders (user_id, total_amount, status) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, total_price, status))
        cnx.commit()

        return jsonify({
            "message": "Customer order added successfully",
            "food_item": order_item_number,
            "total_price": total_price
        }), 201

    except Exception as e:
        return jsonify({"error": f"Unable to process the order: {str(e)}"}), 500

    finally:
        cursor.close()
        cnx.close()


@app.route('/update_food_status', methods=['POST'])
def update_food_order():
    data = request.json
    order_id = data.get('order_id')
    order_status = data.get('status')
    user_id = session.get('user_id')

    if not order_id:
        return jsonify({"error": "Please enter a valid order ID"}), 400

    if not order_status:
        return jsonify({"error": "Please provide a status"}), 400
    
    try:
        cnx = create_db_connection()  # Call the function to get a connection
    except Exception as e:
        return jsonify({"error": f"Unable to connect to DB: {e}"}), 500

    try:
        cursor = cnx.cursor()
        query = """
        UPDATE orders SET status = %s WHERE id = %s AND user_id = %s
        """
        cursor.execute(query, (order_status, order_id, user_id))
        cursor.callproc('move_completed_orders')
        cnx.commit()  # Commit changes on the connection
        return jsonify({"message": "Order status updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": f"Unable to update order: {e}"}), 500

    finally:
        cursor.close()
        cnx.close()  



if __name__ == '__main__':
    app.run(debug=True)
