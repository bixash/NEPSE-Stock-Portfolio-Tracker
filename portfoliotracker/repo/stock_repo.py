from portfoliotracker.repo.db import DBConnection
from portfoliotracker.entities.stock import Stock

class StockRepo:
    def __init__(self, db: DBConnection):
        self.db = db

    def update_stock_prices(self, stock: Stock) -> bool:
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("UPDATE stock SET previous_closing = ?, trade_date = ?, closing_price = ?, difference_rs =?, percent_change = ? WHERE scrip = ?",(stock.previous_closing, stock.trade_date, stock.closing_price, stock.difference_rs, stock.percent_change, stock.scrip, ))
        con.commit()
        return True
    
    def insert_stock_prices(self, stock: Stock) -> bool:
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("INSERT INTO stock (scrip, previous_closing, trade_date, closing_price, difference_rs, percent_change) values(?, ?, ?, ?, ?, ?)",(stock.scrip, stock.previous_closing, stock.trade_date, stock.closing_price, stock.difference_rs, stock.percent_change, ))
        con.commit()
        return True
    
    def fetch_allstock_prices(self) ->list:
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("SELECT previous_closing, trade_date, closing_price FROM stock")
        con.commit()
        return cur.fetchall()
    
    def fetch_stock_price(self, stockSymbol:str):
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("SELECT scrip, previous_closing, trade_date, closing_price, difference_rs, percent_change FROM stock WHERE scrip = ?", (stockSymbol,))
        con.commit()
        return cur.fetchone()
    
    def select_all_stock_prices(self) ->list:
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("SELECT * FROM stock")
        con.commit()
        return cur.fetchall()
    
    def select_stock_by_scrip(self, stockSymbol:str):
        cur = self.db.get_connection()
        cur.execute("SELECT scrip, previous_closing, trade_date, closing_price, difference_rs, percent_change FROM stock WHERE scrip = ?", (stockSymbol,))
        return cur.fetchone()