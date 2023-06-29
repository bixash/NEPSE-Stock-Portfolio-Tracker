from flask import Blueprint, render_template
import sqlite3 as sql

con = sql.connect("database.db", check_same_thread=False)
cur = con.cursor()

views = Blueprint('views', __name__)


@views.route('/')
def dashboard():
   cur.execute("SELECT DISTINCT scrip FROM `Transaction`")
   stock_symbols = cur.fetchall()

   result = []
   for stock in stock_symbols:
      cur.execute("SELECT * from `transaction` where scrip = ? ORDER BY sn ASC limit 1", stock)
      result.append(cur.fetchall())
      
   return render_template("dashboard.html", transaction=result)


