from portfoliotracker.repo.db import DBConnection
from portfoliotracker.entities.stock import Stock
from portfoliotracker.repo.db import get_db_connection

db = get_db_connection()
import threading 
lock = threading.Lock()
class StockRepo:
    def __init__(self, db: DBConnection):
        self.db = db

    def update_stock_prices(self, stock: Stock) -> bool:
        try: 

            cur = self.db.get_cursor()
            cur.execute("UPDATE stock SET previous_closing = ?, trade_date = ?, closing_price = ?, difference_rs =?, percent_change = ? WHERE scrip = ?",(stock.previous_closing, stock.trade_date, stock.closing_price, stock.difference_rs, stock.percent_change, stock.scrip, ))
            self.db.commit()
            return True
        finally:
            self.db.commit()
            # self.db.close()
    
    def insert_stock_prices(self, stock: Stock) -> bool:
        try:
            cur = self.db.get_cursor()
            cur.execute("INSERT INTO stock (scrip, previous_closing, trade_date, closing_price, difference_rs, percent_change) values(?, ?, ?, ?, ?, ?)",(stock.scrip, stock.previous_closing, stock.trade_date, stock.closing_price, stock.difference_rs, stock.percent_change, ))
            self.db.commit()
            return True
        finally:
            self.db.commit()
            # self.db.close()
        
    
    def fetch_allstock_prices(self) ->list:
        try:     
            cur = self.db.get_cursor()
            # con = self.db.get_connection()
            cur.execute("SELECT previous_closing, trade_date, closing_price FROM stock")
            return cur.fetchall()
        finally:
            self.db.commit()
            # self.db.close()
    
    def fetch_stock_price(self, stockSymbol:str):
        try:
            cur = self.db.get_cursor()
            # con = self.db.get_connection()
            cur.execute("SELECT scrip, previous_closing, trade_date, closing_price, difference_rs, percent_change FROM stock WHERE scrip = ?", (stockSymbol,))
            return cur.fetchone()
        finally:
            self.db.commit()
            # self.db.close()
    
    def select_all_stock_prices(self) ->list:

        cur = self.db.get_cursor()
        cur.execute("SELECT * FROM stock")
        return cur.fetchall()
       
    
    def select_stock_by_scrip(self, stockSymbol:str):
        
        con = self.db.get_connection()
        cur = con.cursor()
        cur.execute("SELECT scrip, previous_closing, trade_date, closing_price, difference_rs, percent_change FROM stock WHERE scrip = ?", (stockSymbol, ))
        return cur.fetchone()
       
    
    
    def get_stock_tradeDate(self):

        cur = self.db.get_cursor()
        lock.acquire(True)
        cur.execute("SELECT trade_date FROM stock limit 1")
        return cur.fetchone()
        
            # self.db.close()