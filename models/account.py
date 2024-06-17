# account.py

from models.person import Person
from models.exceptions import InsufficientFundsException, InvalidAccountInformationException
import sqlite3
import datetime

class BankAccount:
    account_counter = 1000

    def __init__(self, account_holder, balance=0, interest_rate=0, interest_type="simple"):
        self.account_number = BankAccount.account_counter
        BankAccount.account_counter += 1
        self.account_holder = account_holder
        self._balance = balance
        self.interest_rate = interest_rate
        self.interest_type = interest_type

    @property
    def account_number(self):
        return self._account_number

    @account_number.setter
    def account_number(self, value):
        self._account_number = value

    @property
    def account_holder(self):
        return self._account_holder

    @account_holder.setter
    def account_holder(self, value):
        if isinstance(value, Person):
            self._account_holder = value
        else:
            raise InvalidAccountInformationException("Account holder must be a Person instance")

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if isinstance(value, (int, float)) and value >= 0:
            self._balance = value
        else:
            raise InvalidAccountInformationException("Balance must be a non-negative number")

    @property
    def interest_rate(self):
        return self._interest_rate

    @interest_rate.setter
    def interest_rate(self, value):
        if isinstance(value, (int, float)) and value >= 0:
            self._interest_rate = value
        else:
            raise InvalidAccountInformationException("Interest rate must be a non-negative number")

    @property
    def interest_type(self):
        return self._interest_type

    @interest_type.setter
    def interest_type(self, value):
        if value in ["simple", "compound"]:
            self._interest_type = value
        else:
            raise InvalidAccountInformationException("Interest type must be 'simple' or 'compound'")

    def deposit(self, amount):
        if amount > 0:
            self._balance += amount
            self.record_transaction('deposit', amount)
            print(f"Deposited {amount}. New balance is {self._balance}.")
        else:
            raise ValueError("Deposit amount must be positive")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self._balance - amount < 0:
            raise InsufficientFundsException("Insufficient funds for this withdrawal")
        self._balance -= amount
        self.record_transaction('withdraw', amount)
        print(f"Withdrew {amount}. New balance is {self._balance}.")

    def display_account_details(self):
        print(f"Account Number: {self.account_number}")
        print(f"Account Holder: {self.account_holder.first_name} {self.account_holder.last_name}")
        print(f"Age: {self.account_holder.age}")
        print(f"Balance: {self._balance}")
        print(f"Interest Rate: {self.interest_rate}%")
        print(f"Interest Type: {self.interest_type}")

    def record_transaction(self, transaction_type, amount):
        conn = sqlite3.connect('bank.db')
        cursor = conn.cursor()
        txn_id = int(datetime.datetime.now().timestamp() * 1000)
        transaction_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO transactions (txn_id, account_number, transaction_type, amount, transaction_date) VALUES (?, ?, ?, ?, ?)",
                       (txn_id, self.account_number, transaction_type, amount, transaction_date))
        conn.commit()
        conn.close()

class SavingsAccount(BankAccount):
    def __init__(self, account_holder, balance=0, interest_rate=0, interest_type="simple"):
        super().__init__(account_holder, balance, interest_rate, interest_type)

    def calculate_interest(self, years):
        if self.interest_type == "simple":
            return self._balance * (1 + self.interest_rate / 100 * years)
        elif self.interest_type == "compound":
            return self._balance * ((1 + self.interest_rate / 100) ** years)
        else:
            raise ValueError("Invalid interest type")
