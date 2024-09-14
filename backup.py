import sqlite3
import shutil
import os

# Function to connect to the database
def connect_db(db_name='finance.db'):
    """
    Establishes a connection to the SQLite database.

    Args:
        db_name (str): The name of the database file.

    Returns:
        sqlite3.Connection: The connection object.
    """
    return sqlite3.connect(db_name)

# Function to initialize the database (create tables if they don't exist)
def initialize_db():
    """
    Initializes the SQLite database by creating necessary tables for the application.
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Create users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT
                    )''')

    # Create transactions table
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        type TEXT,            -- 'income' or 'expense'
                        category TEXT,        -- e.g., 'Food', 'Rent', 'Salary'
                        amount REAL,
                        date TEXT,            -- Date of the transaction (YYYY-MM-DD)
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )''')

    # Create budgets table
    cursor.execute('''CREATE TABLE IF NOT EXISTS budgets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        category TEXT,
                        amount REAL,
                        month INTEGER,
                        year INTEGER,
                        FOREIGN KEY (user_id) REFERENCES users(id)
                    )''')

    conn.commit()
    conn.close()

    print("Database initialized successfully!")

# Function to back up the database
def backup_database(backup_dir='backups', db_name='finance.db'):
    """
    Backs up the SQLite database by copying it to a backup directory.

    Args:
        backup_dir (str): The directory where the backup should be saved.
        db_name (str): The name of the database file to be backed up.

    Returns:
        str: The path to the backup file.
    """
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)

    backup_file = os.path.join(backup_dir, f'backup_{db_name}')
    try:
        shutil.copyfile(db_name, backup_file)
        print(f"Database backed up successfully at {backup_file}")
        return backup_file
    except Exception as e:
        print(f"Error during backup: {e}")
        return None

# Function to restore the database from a backup
def restore_database(backup_file, db_name='finance.db'):
    """
    Restores the SQLite database from a backup file.

    Args:
        backup_file (str): The path to the backup file.
        db_name (str): The name of the database file to restore.

    Returns:
        bool: True if the restore was successful, False otherwise.
    """
    if not os.path.exists(backup_file):
        print(f"Backup file {backup_file} does not exist.")
        return False

    try:
        shutil.copyfile(backup_file, db_name)
        print(f"Database restored successfully from {backup_file}")
        return True
    except Exception as e:
        print(f"Error during restore: {e}")
        return False

# Function to view the contents of the database for debugging 
def view_data(user_id=None):
    """
    Displays the data stored in the database for debugging purposes.

    Args:
        user_id (int, optional): If provided, displays data for a specific user.
    """
    conn = connect_db()
    cursor = conn.cursor()

    # Display all users
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print("Users:")
    for user in users:
        print(user)

    # Display all transactions (optionally filter by user_id)
    if user_id:
        cursor.execute("SELECT * FROM transactions WHERE user_id = ?", (user_id,))
    else:
        cursor.execute("SELECT * FROM transactions")
    transactions = cursor.fetchall()
    print("\nTransactions:")
    for transaction in transactions:
        print(transaction)

    # Display all budgets 
    if user_id:
        cursor.execute("SELECT * FROM budgets WHERE user_id = ?", (user_id,))
    else:
        cursor.execute("SELECT * FROM budgets")
    budgets = cursor.fetchall()
    print("\nBudgets:")
    for budget in budgets:
        print(budget)

    conn.close()

