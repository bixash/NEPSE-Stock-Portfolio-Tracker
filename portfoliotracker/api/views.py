from flask import Blueprint, render_template, request, url_for, session, redirect, flash
from werkzeug.utils import secure_filename
from portfoliotracker.utils.methods import date_format, stringToInt, shorten_history, tupleToStr, ZeroBalancetoEmpty, allowed_file
from portfoliotracker.service.kittapi import getStockPrices
import csv, sqlite3, os
from portfoliotracker.repo.db import cur, con
from portfoliotracker.repo.models import fetch_scrip_balance_price, insert_history, fetch_history



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
            cur.execute(fetch_scrip_balance_price, (stock, user_id, ))
            transactions.append(cur.fetchall())
        
         '''
         changing zero balance scrip to empty list and removing empty list 
         '''   
         result = list(filter(None, ZeroBalancetoEmpty(transactions)))

         total = 0
         
         for item in transactions:
            for scrip, balance, price in item:
               value =  price * balance 
               total = total + value
         
         return render_template("dashboard.html", transaction = result, username=user_name, total = total)
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

            path = os.path.join('web_app', '../../resources/static', 'uploads')
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
                  cur.execute(insert_history, (scrip, transaction_date, credit_quantity, debit_quantity, balance_after_transaction, history_description, user_id))

                  con.commit()
               
               except sqlite3.IntegrityError as e:
                  return render_template("upload.html", msg=e) 
               
            return redirect(url_for("views.dashboard"))
      else:
         return 'No file selected!'
      
   return render_template("upload.html")             


@views.route('/show_csv')
def show_data():

   user_id = session.get('user_id')
   username = session.get('username')

   path = os.path.join('web_app', '../../resources/static', 'uploads')
   save_filename =  f"{user_id}_{username}_transactions.csv"

   with open(os.path.join(path, save_filename), newline='') as csvfile:
      reader = csv.DictReader(csvfile)

      result = []
      for row in reader:
         result.append(row)

   return render_template('show_csv.html', data=result)


@views.route('/show_history')
def show_history():
   user_id = session.get('user_id')

   cur.execute(fetch_history ,(user_id,))

   result = cur.fetchall()
   return render_template('show_history.html', data=result)