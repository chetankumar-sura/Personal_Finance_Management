# Initialize the finance management package
from .finance_app import register_user, login_user
from .transactions import add_transaction, delete_transaction, update_transaction
from .reports import generate_monthly_report, generate_yearly_report, calculate_savings
from .finance_app import set_monthly_budget, check_budget_exceedance, view_monthly_budgets
from .finance_app import initialize_db, backup_database, restore_database, view_data

# initialize the database when the package is imported
initialize_db()

