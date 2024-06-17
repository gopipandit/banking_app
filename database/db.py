# db.py

import sqlite3
import pandas as pd

def initialize_db():
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS customers (
                        account_number INTEGER PRIMARY KEY,
                        first_name TEXT NOT NULL,
                        last_name TEXT NOT NULL,
                        age INTEGER NOT NULL,
                        balance REAL NOT NULL,
                        interest_rate REAL NOT NULL,
                        interest_type TEXT NOT NULL
                    )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        txn_id INTEGER PRIMARY KEY,
                        account_number INTEGER,
                        transaction_type TEXT NOT NULL,
                        amount REAL NOT NULL,
                        transaction_date TEXT NOT NULL,
                        FOREIGN KEY (account_number) REFERENCES customers (account_number)
                    )''')
    conn.commit()
    conn.close()

def add_customer(account_number, first_name, last_name, age, balance, interest_rate, interest_type):
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO customers (account_number, first_name, last_name, age, balance, interest_rate, interest_type)
                      VALUES (?, ?, ?, ?, ?, ?, ?)''',
                   (account_number, first_name, last_name, age, balance, interest_rate, interest_type))
    conn.commit()
    conn.close()

def get_customer(account_number):
    conn = sqlite3.connect('bank.db')
    query = f"""SELECT * FROM customers WHERE account_number = {account_number};"""
    account_details = pd.read_sql_query(query, conn)
    conn.close()
    return account_details

def get_all_transactions(account_number):
    conn = sqlite3.connect('bank.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM transactions WHERE account_number = ?', (account_number,))
    transactions = cursor.fetchall()
    conn.close()
    return transactions
