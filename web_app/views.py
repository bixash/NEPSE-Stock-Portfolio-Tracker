from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from werkzeug.utils import secure_filename
from .methods import date_format, stringToInt, shorten_history, tupleToStr, ZeroBalancetoEmpty, allowed_file
from .kittapi import getStockPrices
import csv, sqlite3, os
from .db import cur, con





views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
def home():
   return render_template("base.html")


@views.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
   if 'user_id' and 'username'  in session:
      user_id = session['user_id']
      user_name = session['username']
      
      try:
         getStockPrices() 
      except Exception as err:
         print(err)
      finally:
      
         cur.execute("SELECT DISTINCT scrip FROM transactions where uid = ?", (user_id,))
         stock_symbols = cur.fetchall()

         transactions = []

         for stock in stock_symbols:
            stock = tupleToStr(stock)

            # cur.execute("SELECT  stock.scrip, balance_after_transaction, closing_price from stock where stock.scrip in( SELECT s FROM) FROM stock INNER JOIN transactions ON transactions.scrip = stock.scrip")

            # cur.execute("SELECT stock.scrip, balance_after_transaction from transactions where scrip = ? and uid = ? order by transaction_date desc limit 1", (stock, user_id, ))

            cur.execute("SELECT stock.scrip, balance_after_transaction, closing_price FROM stock INNER JOIN transactions ON transactions.scrip = stock.scrip where transactions.scrip = ? and uid = ? order by transaction_date desc limit 1", (stock, user_id, ))

            transactions.append(cur.fetchall())

         '''
         changing zero balance scrip to empty list and removing empty list 
         '''   
         result = list(filter(None, ZeroBalancetoEmpty(transactions)))
      
         return render_template("dashboard.html", transaction = result, username=user_name)
   else:
      err_msg = "Please login to goto dashboard!"
      return render_template("base.html", msg= err_msg)
   

@views.route('/upload', methods=['GET','POST'])
def upload():
   if 'user_id' and 'username' in session:
      user_id = session['user_id']
      username = session['username']
   
   if request.method == 'POST':

      if 'file' not in request.files:
         flash('No file part')
         return redirect(request.url)
      
      file = request.files['file']

      if file.filename == '':
         flash('No selected file')
         return redirect(request.url)
      
      if file and allowed_file(file.filename):

         filename = secure_filename(file.filename)
         if filename.endswith('.csv'):

            path = os.path.join('web_app', 'static', 'uploads')
            save_filename =  f"{user_id}_{username}_transactions.csv"
            
            file.save(os.path.join(path, save_filename))

         with open(os.path.join(path, save_filename), newline='') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
               scrip= row['Scrip']
               transaction_date = date_format(row['Transaction Date'])
               credit_quantity = stringToInt(row['Credit Quantity'])
               debit_quantity = stringToInt(row['Debit Quantity'])
               balance_after_transaction = stringToInt(row['Balance After Transaction'])
               history_description = shorten_history(row['History Description'])
               
               try:
                  cur.execute("INSERT INTO transactions (scrip, transaction_date, credit_quantity, debit_quantity, balance_after_transaction, history_description, uid)values(?,?,?,?,?,?,?)", (scrip,transaction_date, credit_quantity, debit_quantity, balance_after_transaction, history_description, user_id))

                  con.commit()
               
               except sqlite3.IntegrityError as e:
                  return render_template("upload.html", msg=e) 
               
            return redirect(url_for("views.dashboard"))
      else:
         return 'No file selected!'
      
   return render_template("upload.html")             