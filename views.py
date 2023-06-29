from flask import Blueprint, render_template, request
import sqlite3 as sql

con = sql.connect("database.db", check_same_thread=False)
cur = con.cursor()

views = Blueprint('views', __name__)


@views.route('/')
def base():
   return render_template("base.html")


@views.route('/login', methods=['GET', 'POST'])
def login():
   if request.method == 'POST':
      email = request.form['email']
      password = request.form['password']

      cur.execute("SELECT * FROM `User` where email= ? and password = ?", (email, password))
      result = cur.fetchone()

      if email == result[1] and password == result[2]:
         return render_template("dashboard.html", user_id = result[0])
      
   return render_template("login.html")


@views.route('/signup', methods=['GET', 'POST'])
def signup():
   return render_template("signup.html")


@views.route('/dashboard')
def dashboard():

   cur.execute("SELECT DISTINCT scrip FROM `Transaction`")
   stock_symbols = cur.fetchall()

   result = []
   for stock in stock_symbols:
      cur.execute("SELECT * from `transaction` where scrip = ? ORDER BY sn ASC limit 1", stock)
      result.append(cur.fetchall())
      
   return render_template("dashboard.html", transaction=result)


