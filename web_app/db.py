import sqlite3 as sql

con = sql.connect("database.db", check_same_thread=False)
cur = con.cursor()
