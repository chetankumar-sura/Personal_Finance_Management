import sqlite3

# Function to set a monthly budget for a specific category
def set_monthly_budget(user_id, category, amount, month, year):
    """
    Sets a monthly budget for a specific category.

    Args:
        user_id (int): The ID of the user.
        category (str): The category for which the budget is set (e.g., 'Food', 'Rent').
        amount (float): The budget amount.
        month (int): The month for which the budget is set (1-12).
        year (int): The year for which the budget is set (e.g., 2024).

    Returns:
        None
    """
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    # Check if a budget for this category and month already exists
    cursor.execute("""
        SELECT * FROM budgets WHERE user_id = ? AND category = ? AND month = ? AND year = ?
    """, (user_id, category, month, year))
    existing_budget = cursor.fetchone()

    if existing_budget:
        # Update the budget if it exists
        cursor.execute("""
            UPDATE budgets SET amount = ? WHERE user_id = ? AND category = ? AND month = ? AND year = ?
        """, (amount, user_id, category, month, year))
        print(f"Updated budget for {category} in {month}/{year} to {amount}.")
    else:
        # Insert a new budget if it doesn't exist
        cursor.execute("""
            INSERT INTO budgets (user_id, category, amount, month, year) 
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, category, amount, month, year))
        print(f"Set budget for {category} in {month}/{year} to {amount}.")

    conn.commit()
    conn.close()

# Function to check if the user has exceeded their budget in any category for the current month
def check_budget_exceedance(user_id, month, year):
    """
    Checks if the user has exceeded their budget for any category in a given month and year.

    Args:
        user_id (int): The ID of the user.
        month (int): The month to check (1-12).
        year (int): The year to check (e.g., 2024).

    Returns:
        list: A list of categories where the budget has been exceeded.
    """
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    # Get all the budgets set for the user for the given month and year
    cursor.execute("""
        SELECT category, amount FROM budgets WHERE user_id = ? AND month = ? AND year = ?
    """, (user_id, month, year))
    budgets = cursor.fetchall()

    exceeded_categories = []

    # For each budgeted category, check if the user has exceeded the budget
    for category, budget_amount in budgets:
        cursor.execute("""
            SELECT SUM(amount) FROM transactions
            WHERE user_id = ? AND type = 'expense' AND category = ? 
            AND strftime('%m', date) = ? AND strftime('%Y', date) = ?
        """, (user_id, category, f'{month:02}', str(year)))
        total_spent = cursor.fetchone()[0] or 0.0

        if total_spent > budget_amount:
            exceeded_categories.append({
                "category": category,
                "budget_amount": budget_amount,
                "total_spent": total_spent,
                "over_budget": total_spent - budget_amount
            })

    conn.close()

    if exceeded_categories:
        for exceeded in exceeded_categories:
            print(f"Warning: You have exceeded your budget for {exceeded['category']}!")
            print(f"Budget: {exceeded['budget_amount']}, Spent: {exceeded['total_spent']}, Over Budget: {exceeded['over_budget']}")
    else:
        print("You are within your budget for all categories.")

    return exceeded_categories

# Function to display all budgets for a user for a given month and year
def view_monthly_budgets(user_id, month, year):
    """
    Displays all the set budgets for a user in a given month and year.

    Args:
        user_id (int): The ID of the user.
        month (int): The month (1-12).
        year (int): The year (e.g., 2024).

    Returns:
        list: A list of budgets with category and amount for the given month and year.
    """
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()

    # Fetch all budgets for the user for the given month and year
    cursor.execute("""
        SELECT category, amount FROM budgets WHERE user_id = ? AND month = ? AND year = ?
    """, (user_id, month, year))
    budgets = cursor.fetchall()

    if budgets:
        print(f"Budgets for {month}/{year}:")
        for category, amount in budgets:
            print(f"{category}: {amount}")
    else:
        print(f"No budgets set for {month}/{year}.")

    conn.close()
    return budgets
