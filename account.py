import random
import sys
from datetime import datetime
import re

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

# Function to check if the user is authorized
def is_authorized(user_id, password):
    return user_id in data_store and data_store[user_id]['password'] == password

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

# Signup function
def sign_up():
    print("\n=== Sign Up ===")
    user_id = input("Enter a unique User ID: ")

    if user_id in data_store:
        print("User ID already exists. Please try again.")
        return

    full_name = input("Enter your full name: ")
    dob = input("Enter your date of birth (YYYY-MM-DD): ")
    address = input("Enter your address: ")
    email = input("Enter your email address: ")
    phone = input("Enter your phone number: ")

    try:
        year = int(dob.split('-')[0])
        age = datetime.now().year - year
    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")
        return

    if age < 18:
        print("You are not eligible to create an account.")
        return

    while True:
        password = input("Set a password: ")
        validation_error = validate_password(password)
        if validation_error:
            print(validation_error)
        else:
            break

    account_number = generate_account_number()
    data_store[user_id] = {
        'full_name': full_name,
        'dob': dob,
        'address': address,
        'email': email,
        'phone': phone,
        'password': password, # the password should contian atleast 8 chracters int he one special chracter and remaing should be alphanumeric
        'account_number': account_number,
        'transaction_history': [],
        'balance': 0.0
    }
    print(f"Account created successfully! Your account number is {account_number}.")
    account_details(user_id)

# Login function
def login():
    print("\n=== Login ===")
    user_id = input("Enter User ID: ")
    password = input("Enter Password: ")

    if is_authorized(user_id, password):
        print(f"Welcome {data_store[user_id]['full_name']}!")
        account_details(user_id)
    else:
        print("Invalid User ID or Password.")
        if input("Forgot password? (yes/no): ").strip().lower() == "yes":
            forgot_password(user_id)

# Forgot password function
def forgot_password(user_id):
    if user_id in data_store:
        print(f"Your password is: {data_store[user_id]['password']}")
    else:
        print("User ID not found. Please sign up first.")

# Account Details Section
def account_details(user_id):
    while True:
        print("\n=== Account Details ===")
        print("1. Profile")
        print("2. Loans")
        print("3. Deposit")
        print("4. Transaction History")
        print("5. Cards")
        print("6. Check Balance")
        print("7. Net Banking")
        print("8. Help")
        print("9. Bank Offers")
        print("10. Logout")
        choice = input("Enter your choice: ")

        if choice == '1':
            show_profile(user_id)
        elif choice == '2':
            show_loans()
        elif choice == '3':
            deposit_amount(user_id)
        elif choice == '4':
            show_transaction_history(user_id)
        elif choice == '5':
            show_cards()
        elif choice == '6':
            if password_verification(user_id):
                check_balance(user_id)
        elif choice == '7':
            if password_verification(user_id):
                net_banking(user_id)
        elif choice == '8':
            show_help()
        elif choice == '9':
            show_offers()
        elif choice == '10':
            print("Logged out successfully.")
            break
        else:
            print("Invalid choice. Please try again.")

# Password verification function
def password_verification(user_id):
    password = input("Please re-enter your password for verification: ")
    if is_authorized(user_id, password):
        return True
    else:
        print("Incorrect password. Access denied.")
        return False

# Display Profile
def show_profile(user_id):
    print("\n=== Profile ===")
    user = data_store[user_id]
    print(f"Full Name: {user['full_name']}")
    print(f"Date of Birth: {user['dob']}")
    print(f"Address: {user['address']}")
    print(f"Email: {user['email']}")
    print(f"Phone: {user['phone']}")
    print(f"Account Number: {user['account_number']}")
    print("\n=== Transaction History ===")
    for transaction in user['transaction_history']:
        print(transaction)

# Deposit Function
def deposit_amount(user_id):
    try:
        amount = float(input("Enter the amount to deposit: $"))
        if amount <= 0:
            print("Invalid deposit amount. Please try again.")
        else:
            user = data_store[user_id]
            user['balance'] += amount
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user['transaction_history'].append(f"Deposited: ${amount:.2f} on {timestamp}")
            print(f"Deposit successful! Your new balance is: ${user['balance']:.2f}")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Display Loans
def show_loans():
    print("\n=== Loans ===")
    print("1. Educational Loan: Low interest rate, 5 years repayment.")
    print("2. Home Loan: High loan amount, 15 years repayment.")
    print("3. Personal Loan: Quick processing, medium interest rate.")

# Display Transaction History
def show_transaction_history(user_id):
    print("\n=== Transaction History ===")
    user = data_store[user_id]
    for transaction in user['transaction_history']:
        print(transaction)

# Display Cards
def show_cards():
    print("\n=== Cards ===")
    card_type = input("Choose Card Type (1. Debit Card, 2. Credit Card): ")
    if card_type in ('1', '2'):
        card_number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
        expiry_date = f"{random.randint(1, 12)}/{random.randint(2025, 2035)}"
        cvv = ''.join([str(random.randint(0, 9)) for _ in range(3)])
        print(f"Card Number: {card_number}")
        print(f"Expiry Date: {expiry_date}")
        print(f"CVV: {cvv}")
    else:
        print("Invalid card choice.")

# Check Balance
def check_balance(user_id):
    print(f"Your current balance is: ${data_store[user_id]['balance']:.2f}")

# Net Banking
def net_banking(user_id):
    try:
        receiver_account = input("Enter the receiver's account number: ")
        ifsc_code = input("Enter the receiver's IFSC code: ")
        nickname = input("Enter a nickname for the transaction (optional): ")
        amount = float(input("Enter the amount to transfer: $"))

        user = data_store[user_id]
        if amount > user['balance']:
            print("Insufficient balance. Transaction failed.")
        else:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            user['balance'] -= amount
            user['transaction_history'].append(
                f"Sent: ${amount:.2f} to {receiver_account} ({nickname}) on {timestamp}, IFSC: {ifsc_code}"
            )
            print("Transaction successful!")
    except ValueError:
        print("Invalid input. Please enter a valid number.")

# Help
def show_help():
    print("\n=== Help ===")
    print("Customer Helpline: 1800-123-4567")
    print("Email: support@kulabanking.com")

# Bank Offers
def show_offers():
    print("\n=== Bank Offers ===")
    print("Credit Card Offers: 5% cashback on all online purchases.")
    print("Loan Offers: Special 7% interest rate on home loans.")

# Main Menu
def main_menu():
    while True:
        print("\nWELCOME TO KULA BANKING")
        print("1. Login")
        print("2. Sign Up")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            login()
        elif choice == "2":
            sign_up()
        elif choice == "3":
            print("Thank you for using the Kula Banking System. Goodbye!")
            sys.exit()
        else:
            print("Invalid choice. Please try again.")

# Run the program
if __name__ == "__main__":
    main_menu()
