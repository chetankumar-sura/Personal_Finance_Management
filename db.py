import sqlite3
def create_tables():
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    # Create the users table
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        username TEXT UNIQUE,
                        password TEXT
                    )''')
    conn.commit()
    conn.close()
