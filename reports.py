import sqlite3
from datetime import datetime

# Function to generate financial report for a specific month and year
def generate_monthly_report(user_id, month, year):
    """
    Generates a monthly financial report showing total income, expenses, and savings.

    Args:
        user_id (int): The ID of the user.
        month (int): The month for the report (1-12).
        year (int): The year for the report (e.g., 2023).

    Returns:
        dict: A dictionary containing total income, total expenses, and savings.
    """
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    # Fetch total income for the given month and year
    cursor.execute("""
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ? AND type = 'income' AND strftime('%m', date) = ? AND strftime('%Y', date) = ?
    """, (user_id, f'{month:02}', str(year)))
    total_income = cursor.fetchone()[0] or 0.0

    # Fetch total expenses for the given month and year
    cursor.execute("""
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ? AND type = 'expense' AND strftime('%m', date) = ? AND strftime('%Y', date) = ?
    """, (user_id, f'{month:02}', str(year)))
    total_expenses = cursor.fetchone()[0] or 0.0

    # Calculate savings as the difference between income and expenses
    savings = total_income - total_expenses

    conn.close()

    report = {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "savings": savings
    }

    print(f"Monthly Report for {month}/{year}")
    print(f"Total Income: {total_income}")
    print(f"Total Expenses: {total_expenses}")
    print(f"Savings: {savings}")

    return report

# Function to generate a yearly financial report
def generate_yearly_report(user_id, year):
    """
    Generates a yearly financial report showing total income, expenses, and savings.

    Args:
        user_id (int): The ID of the user.
        year (int): The year for the report (e.g., 2023).

    Returns:
        dict: A dictionary containing total income, total expenses, and savings for the year.
    """
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    # Fetch total income for the given year
    cursor.execute("""
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ? AND type = 'income' AND strftime('%Y', date) = ?
    """, (user_id, str(year)))
    total_income = cursor.fetchone()[0] or 0.0

    # Fetch total expenses for the given year
    cursor.execute("""
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ? AND type = 'expense' AND strftime('%Y', date) = ?
    """, (user_id, str(year)))
    total_expenses = cursor.fetchone()[0] or 0.0

    # Calculate yearly savings
    savings = total_income - total_expenses

    conn.close()

    report = {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "savings": savings
    }

    print(f"Yearly Report for {year}")
    print(f"Total Income: {total_income}")
    print(f"Total Expenses: {total_expenses}")
    print(f"Savings: {savings}")

    return report

# Helper function to calculate total income, expenses, and savings for a custom period
def calculate_totals(user_id, start_date, end_date):
    """
    Calculates total income, expenses, and savings for a custom period.

    Args:
        user_id (int): The ID of the user.
        start_date (str): Start date in YYYY-MM-DD format.
        end_date (str): End date in YYYY-MM-DD format.

    Returns:
        dict: A dictionary containing total income, total expenses, and savings.
    """
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    # Fetch total income for the given period
    cursor.execute("""
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ? AND type = 'income' AND date BETWEEN ? AND ?
    """, (user_id, start_date, end_date))
    total_income = cursor.fetchone()[0] or 0.0

    # Fetch total expenses for the given period
    cursor.execute("""
        SELECT SUM(amount) FROM transactions
        WHERE user_id = ? AND type = 'expense' AND date BETWEEN ? AND ?
    """, (user_id, start_date, end_date))
    total_expenses = cursor.fetchone()[0] or 0.0

    # Calculate savings
    savings = total_income - total_expenses

    conn.close()

    totals = {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "savings": savings
    }

    print(f"Total Income: {total_income}")
    print(f"Total Expenses: {total_expenses}")
    print(f"Savings: {savings}")

    return totals
