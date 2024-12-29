from flask import Flask, request, jsonify
from datetime import datetime
import random
import re

app = Flask(__name__)

# Dictionary to store user data
data_store = {
    "harsha": {
        "full_name": "Eswar Harsha Vardhan",
        "dob": "2004-03-25",
        "address": "Siddantham",
        "email": "harsha72@gmail.com",
        "phone": "9876546733",
        "password": "harsha123@",
        "account_number": "9701711230",
        "transaction_history": [],
        "balance": 5000.0
    }
}

# Function to generate a 10-digit random account number
def generate_account_number():
    return ''.join(random.choices("0123456789", k=10))

# Function to validate the password
def validate_password(password):
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"[a-zA-Z]", password):
        return "Password must contain at least one alphabet."
    if not re.search(r"\d", password):
        return "Password must contain at least one digit."
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return "Password must contain at least one special character."
    return None

# Signup endpoint
@app.route('/signup', methods=['POST'])
def sign_up():
    data = request.json
    user_id = data.get('user_id')

    if user_id in data_store:
        return jsonify({"error": "User ID already exists."}), 400

    full_name = data.get('full_name')
    dob = data.get('dob')
    address = data.get('address')
    email = data.get('email')
    phone = data.get('phone')
    password = data.get('password')

    try:
        year = int(dob.split('-')[0])
        age = datetime.now().year - year
    except ValueError:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    if age < 18:
        return jsonify({"error": "You must be at least 18 years old to create an account."}), 400

    validation_error = validate_password(password)
    if validation_error:
        return jsonify({"error": validation_error}), 400

    account_number = generate_account_number()
    data_store[user_id] = {
        'full_name': full_name,
        'dob': dob,
        'address': address,
        'email': email,
        'phone': phone,
        'password': password,
        'account_number': account_number,
        'transaction_history': [],
        'balance': 0.0
    }
    return jsonify({"message": "Account created successfully!", "account_number": account_number}), 201

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user_id = data.get('user_id')
    password = data.get('password')

    if user_id in data_store and data_store[user_id]['password'] == password:
        return jsonify({"message": f"Welcome {data_store[user_id]['full_name']}!"}), 200
    else:
        return jsonify({"error": "Invalid User ID or Password."}), 401

# Account details endpoint
@app.route('/account/<user_id>', methods=['GET'])
def account_details(user_id):
    user = data_store.get(user_id)
    if not user:
        return jsonify({"error": "User not found."}), 404

    return jsonify({
        "full_name": user['full_name'],
        "dob": user['dob'],
        "address": user['address'],
        "email": user['email'],
        "phone": user['phone'],
        "account_number": user['account_number'],
        "balance": user['balance'],
        "transaction_history": user['transaction_history']
    }), 200

# Deposit endpoint
@app.route('/deposit/<user_id>', methods=['POST'])
def deposit_amount(user_id):
    data = request.json
    amount = data.get('amount')

    if user_id not in data_store:
        return jsonify({"error": "User not found."}), 404

    if amount <= 0:
        return jsonify({"error": "Invalid deposit amount."}), 400

    user = data_store[user_id]
    user['balance'] += amount
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    user['transaction_history'].append(f"Deposited: ${amount:.2f} on {timestamp}")
    return jsonify({"message": "Deposit successful!", "new_balance": user['balance']}), 200

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
