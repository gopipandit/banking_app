# app.py

import streamlit as st
import pandas as pd
from st_aggrid import AgGrid,GridOptionsBuilder,grid_options_builder
from models.person import Person
from models.account import SavingsAccount
from models.exceptions import InvalidAccountInformationException, InsufficientFundsException, NonExistingBankAccountException
from database.db import initialize_db, add_customer, get_customer, get_all_transactions

def main():
    st.title("Banking Transaction Application")

    menu = ["Create Account", "Deposit", "Withdraw", "Account Details", "Transactions"]
    choice = st.sidebar.selectbox("Menu", menu)

    initialize_db()

    if choice == "Create Account":
        st.subheader("Create a New Account")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        age = st.number_input("Age", min_value=18, max_value=100, step=1)
        balance = st.number_input("Initial Balance", min_value=0.0, step=10.0)
        interest_rate = st.number_input("Interest Rate", min_value=0.0, step=0.1)
        interest_type = st.selectbox("Interest Type", ["simple", "compound"])
        
        if st.button("Create Account"):
            try:
                person = Person(first_name, last_name, age)
                account = SavingsAccount(person, balance, interest_rate, interest_type)
                add_customer(account.account_number, person.first_name, person.last_name, person.age, balance, interest_rate, interest_type)
                st.success(f"Account created successfully! Your account number is {account.account_number}")
            except InvalidAccountInformationException as e:
                st.error(e)

    elif choice == "Deposit":
        st.subheader("Deposit Amount")
        account_number = st.number_input("Account Number", min_value=1000, step=1)
        amount = st.number_input("Amount to Deposit", min_value=0.0, step=10.0)

        if st.button("Deposit"):
            customer = get_customer(account_number)
            if customer:
                person = Person(customer[1], customer[2], customer[3])
                account = SavingsAccount(person, customer[4], customer[5], customer[6])
                account.deposit(amount)
                st.success(f"Deposited {amount}. New balance is {account.balance}.")
            else:
                st.error("Account not found.")

    elif choice == "Withdraw":
        st.subheader("Withdraw Amount")
        account_number = st.number_input("Account Number", min_value=1000, step=1)
        amount = st.number_input("Amount to Withdraw", min_value=0.0, step=10.0)

        if st.button("Withdraw"):
            customer = get_customer(account_number)
            if customer:
                person = Person(customer[1], customer[2], customer[3])
                account = SavingsAccount(person, customer[4], customer[5], customer[6])
                try:
                    account.withdraw(amount)
                    st.success(f"Withdrew {amount}. New balance is {account.balance}.")
                except InsufficientFundsException as e:
                    st.error(e)
            else:
                st.error("Account not found.")

    elif choice == "Account Details":
        st.subheader("Account Details")
        account_number = st.number_input("Account Number", min_value=1000, step=1)

        if st.button("Show Details"):
            customer = get_customer(account_number)
            if customer is not None:
                AgGrid(customer)
                # st.dataframe(customer)
            else:
                st.error("Account not found.")

    elif choice == "Transactions":
        st.subheader("Transactions")
        account_number = st.number_input("Account Number", min_value=1000, step=1)

        if st.button("Show Transactions"):
            transactions = get_all_transactions(account_number)
            if transactions:
                for txn in transactions:
                    st.write(txn)
            else:
                st.error("No transactions found or account not found.")

if __name__ == "__main__":
    main()
