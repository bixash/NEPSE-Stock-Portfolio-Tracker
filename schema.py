import sqlite3 as sql

con = sql.connect("database.db", check_same_thread=False)
cur = con.cursor()

# Schema for User table
# cur.execute("CREATE TABLE user ( id INTEGER NOT NULL, email VARCHAR(150), password VARCHAR(150), PRIMARY KEY (id), UNIQUE (email))")

# Schema for transaction table
cur.execute("CREATE TABLE IF NOT EXISTS `transaction` (id INTEGER NOT NULL, sn INTEGER NOT NULL, scrip VARCHAR(225),transaction_date VARCHAR(225),credit_quantity VARCHAR(225),debit_quantity VARCHAR(225),balance_after_transaction VARCHAR(225),history_description VARCHAR(225), uid INTEGER NOT NULL, FOREIGN KEY(uid) REFERENCES user(id), PRIMARY KEY (id))")

