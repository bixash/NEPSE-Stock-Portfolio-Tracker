from flask import Blueprint, render_template, request, url_for, session, redirect
from werkzeug.utils import secure_filename
from methods import date_format, stringToInt, shorten_history, tupleToStr
import csv
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

      cur.execute("SELECT id, email, password FROM `User` where email= ? and password = ?", (email, password))
      result = cur.fetchone()
      user_id = result[0]
      if email == result[1] and password == result[2]:
         session['user_id'] = user_id
         return redirect(url_for('views.dashboard'))
      
   return render_template("login.html")


@views.route('/signup', methods=['GET', 'POST'])
def signup():
   return render_template("signup.html")


@views.route('/dashboard')
def dashboard():
   if 'user_id' in session:
      user_id = session['user_id']
      

   cur.execute("SELECT DISTINCT scrip FROM transactions where uid = ?", (user_id,))
   stock_symbols = cur.fetchall()

   result = []

   for stock in stock_symbols:
      stock = tupleToStr(stock)
      cur.execute("SELECT * from transactions where scrip = ? and uid = ? order by transaction_date desc limit 1", (stock, user_id, ))
      result.append(cur.fetchall())
   # print(result)  
   return render_template("dashboard.html", transaction = result)


@views.route('/upload', methods=['GET','POST'])
def upload():
   if 'user_id' in session:
      user_id = session['user_id']
   
   if request.method == 'POST':
      f = request.files['file']
      f.save(secure_filename(f.filename))

      # print(secure_filename(f.filename))

      # reading uploaded file
      with open('Transaction_History.csv', newline='') as csvfile:
         reader = csv.DictReader(csvfile)

         for row in reader:
            sn = row['S.N']
            scrip= row['Scrip']
            transaction_date = date_format(row['Transaction Date'])
            credit_quantity = stringToInt(row['Credit Quantity'])
            debit_quantity = stringToInt(row['Debit Quantity'])
            balance_after_transaction = stringToInt(row['Balance After Transaction'])
            history_description = shorten_history(row['History Description'])

            print(sn,scrip,transaction_date,credit_quantity,debit_quantity,balance_after_transaction,history_description, user_id)
            
            cur.execute("INSERT INTO transactions (id, scrip, transaction_date, credit_quantity, debit_quantity, balance_after_transaction, history_description, uid)values(?,?,?,?,?,?,?,?)", (sn, scrip,transaction_date, credit_quantity, debit_quantity, balance_after_transaction, history_description, user_id))

            con.commit()
            return render_template("upload.html", msg = "Sucessfully uploaded!")
   return render_template("upload.html")             