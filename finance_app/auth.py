import sqlite3
import hashlib

# Function to register a new user
def register_user(username, password):
    """
    Registers a new user with a username and password.

    Args:
        username (str): The username for the new user.
        password (str): The password for the new user.

    Returns:
        bool: True if registration is successful, False if the username already exists.
    """
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    # Hash the password before storing it
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    try:
        # Insert the new user into the users table
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
        conn.commit()
        print("User registered successfully!")
        return True
    except sqlite3.IntegrityError:
        print("Error: Username already exists. Please choose a different username.")
        return False
    finally:
        conn.close()

# Function to authenticate (login) an existing user
def login_user(username, password):
    """
    Logs in an existing user by verifying the username and password.

    Args:
        username (str): The username of the user.
        password (str): The password of the user.

    Returns:
        bool: True if login is successful, False otherwise.
    """
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    # Hash the password to compare with stored hash
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Check if the user exists with the given username and hashed password
    cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, hashed_password))
    user = cursor.fetchone()

    conn.close()

    if user:
        print(f"Welcome, {username}! Login successful.")
        return True
    else:
        print("Error: Invalid username or password. Please try again.")
        return False




