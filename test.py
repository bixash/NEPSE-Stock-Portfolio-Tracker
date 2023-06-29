# dict = {}
# data = {1,2,3,34,5,5,654,646,546,5}
# for row in data:
#     dict.update({"1": row})
#     # print("1")
# print(dict)

import sqlite3 as sql

con = sql.connect("database.db", check_same_thread=False)
cur = con.cursor()

email = 'bikash@gmail.com'
password = 'password'

cur.execute("SELECT * FROM `User` where email= ? and password = ?", (email, password))
result = cur.fetchone()
print(result[1])