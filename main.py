# main.py

from models.person import Person
from models.account import SavingsAccount
from models.exceptions import InvalidAccountInformationException, InsufficientFundsException, NonExistingBankAccountException
from database.db import initialize_db, add_customer, get_customer, get_all_transactions


def main():
    initialize_db()

    try:
        first_name = input("Enter first name: ")
        last_name = input("Enter last name: ")
        age = int(input("Enter age: "))
        person = Person(first_name, last_name, age)
        
        balance = float(input("Enter initial balance: "))
        interest_rate = float(input("Enter interest rate: "))
        interest_type = input("Enter interest type (simple/compound): ").lower()
        
        account = SavingsAccount(person, balance, interest_rate, interest_type)
        
        add_customer(account.account_number, person.first_name, person.last_name, person.age, balance, interest_rate, interest_type)
        
        print("\nAccount created successfully!\n")
        account.display_account_details()

        while True:
            print("\n1. Deposit")
            print("2. Withdraw")
            print("3. Display Account Details")
            print("4. Display Transactions")
            print("5. Exit")
            choice = int(input("Enter your choice: "))

            if choice == 1:
                amount = float(input("Enter amount to deposit: "))
                account.deposit(amount)
            elif choice == 2:
                amount = float(input("Enter amount to withdraw: "))
                try:
                    account.withdraw(amount)
                except InsufficientFundsException as e:
                    print(e)
            elif choice == 3:
                account.display_account_details()
            elif choice == 4:
                transactions = get_all_transactions(account.account_number)
                for txn in transactions:
                    print(txn)
            elif choice == 5:
                break
            else:
                print("Invalid choice. Please try again.")

    except InvalidAccountInformationException as e:
        print(e)

if __name__ == "__main__":
    main()
