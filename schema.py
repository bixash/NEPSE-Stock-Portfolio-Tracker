import sqlite3 as sql

con = sql.connect("database.db", check_same_thread=False)
cur = con.cursor()

# Schema for User table
def create_user_table():
    cur.execute("CREATE TABLE user ( id INTEGER NOT NULL, email VARCHAR(150), password VARCHAR(150), PRIMARY KEY (id), UNIQUE (email))")

# Schema for transaction table
def create_transaction_table():
    cur.execute("CREATE TABLE transactions (id INTEGER NOT NULL, scrip VARCHAR(225),transaction_date DATE NOT NULL, credit_quantity INTEGER NOT NULL, debit_quantity INTEGER NOT NULL,balance_after_transaction INTEGER NOT NULL,history_description VARCHAR(225), uid INTEGER NOT NULL, FOREIGN KEY(uid) REFERENCES user(id),FOREIGN KEY(scrip) REFERENCES stock(scrip), PRIMARY KEY (id))")

def create_stock_table():
    cur.execute("CREATE TABLE stock(scrip VARCHAR(255), closing_price INTEGER, PRIMARY KEY (scrip))")

# create_stock_table()
