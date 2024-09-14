import sqlite3
from datetime import datetime

# Function to add a transaction (income or expense)
def add_transaction(user_id, transaction_type, category, amount, date=None):
    """
    Adds a new transaction (income/expense) for the user.

    Args:
        user_id (int): The ID of the user.
        transaction_type (str): The type of transaction ('income' or 'expense').
        category (str): The category of the transaction (e.g., 'Food', 'Salary').
        amount (float): The amount of the transaction.
        date (str, optional): The date of the transaction (YYYY-MM-DD). If None, defaults to today.

    Returns:
        None
    """
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    # Set date to today if not provided
    if date is None:
        date = datetime.today().strftime('%Y-%m-%d')

    # Insert the transaction into the transactions table
    cursor.execute(
        "INSERT INTO transactions (user_id, type, category, amount, date) VALUES (?, ?, ?, ?, ?)",
        (user_id, transaction_type, category, amount, date)
    )
    
    conn.commit()
    conn.close()
    print(f"Transaction of {amount} added under {category} as {transaction_type} on {date}.")

# Function to delete a transaction by ID
def delete_transaction(transaction_id):
    """
    Deletes a transaction by its ID.

    Args:
        transaction_id (int): The ID of the transaction to be deleted.

    Returns:
        None
    """
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    # Delete the transaction from the transactions table
    cursor.execute("DELETE FROM transactions WHERE id = ?", (transaction_id,))
    
    if cursor.rowcount == 0:
        print(f"No transaction found with ID {transaction_id}.")
    else:
        print(f"Transaction {transaction_id} deleted successfully.")

    conn.commit()
    conn.close()

# Function to update an existing transaction by ID
def update_transaction(transaction_id, transaction_type=None, category=None, amount=None, date=None):
    """
    Updates an existing transaction by its ID. Any field can be updated.

    Args:
        transaction_id (int): The ID of the transaction to be updated.
        transaction_type (str, optional): The new type of the transaction ('income' or 'expense').
        category (str, optional): The new category of the transaction.
        amount (float, optional): The new amount of the transaction.
        date (str, optional): The new date of the transaction (YYYY-MM-DD).

    Returns:
        None
    """
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    # Build the update query dynamically based on which fields are provided
    update_fields = []
    values = []

    if transaction_type:
        update_fields.append("type = ?")
        values.append(transaction_type)
    if category:
        update_fields.append("category = ?")
        values.append(category)
    if amount is not None:
        update_fields.append("amount = ?")
        values.append(amount)
    if date:
        update_fields.append("date = ?")
        values.append(date)

    # If no fields are provided, return without updating
    if not update_fields:
        print("No fields to update.")
        return

    # Add transaction_id to the values and execute the update query
    values.append(transaction_id)
    query = f"UPDATE transactions SET {', '.join(update_fields)} WHERE id = ?"
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        print(f"No transaction found with ID {transaction_id}.")
    else:
        print(f"Transaction {transaction_id} updated successfully.")

    conn.commit()
    conn.close()
