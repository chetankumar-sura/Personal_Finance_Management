from finance_app import auth, transactions, reports, budget

def main():
    print("Welcome to the Personal Finance Management App")
    choice = input("Do you have an account? (yes/no): ")
    
    if choice.lower() == 'no':
        username = input("Enter a username: ")
        password = input("Enter a password: ")
        auth.register_user(username, password)
    else:
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = auth.login_user(username, password)
        if user:
            print("Login successful!")
            # Further actions such as adding transactions, viewing reports, etc.
        else:
            print("Invalid credentials")

if __name__ == "__main__":
    main()
