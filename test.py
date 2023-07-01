'''
first test convert into dict, to executemany queries
'''
dict = {}
data = {1,2,3,34,5,5,654,646,546,5}
for row in data:
    dict.update({"1": row})
    # print("1")
print(dict)

'''
connecting to database
'''
import sqlite3 as sql

con = sql.connect("database.db", check_same_thread=False)
cur = con.cursor()

email = 'bikash@gmail.com'
password = 'password'

cur.execute("SELECT * FROM `User` where email= ? and password = ?", (email, password))
result = cur.fetchone()
print(result[1])

'''
Changing MM/DD/YYYY into YYYY-MM-DD
'''

def toDoubleDigit(date):
    if int(date) < 10:
        date = '0'+ date
    return date

def date_format(date):
    newDate = date.split("/")
   
    month = toDoubleDigit(newDate[0])
    day = toDoubleDigit(newDate[1])
    year = newDate[2]

    newDate[0] = year
    newDate[1] = month
    newDate[2] = day

    newDate = "-".join(newDate)

    return newDate

date = "2/11/2023"
print(date)
date_format(date)