from portfoliotracker.entities import BaseResponse
from portfoliotracker.repo.db import DBConnection
from portfoliotracker.entities.stock import Stock

class APIRepo:
    def __init__(self, db: DBConnection):
        self.db = db

    def update_stock_prices(self, stock: Stock) -> bool:
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("UPDATE stock SET previous_closing = ?, trade_date = ?, closing_price = ? WHERE scrip = ?",(stock.previous_closing, stock.trade_date, stock.closing_price, stock.scrip, ))
        con.commit()
        return True
    
    def insert_stock_prices(self, stock: Stock) -> bool:
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("INSERT INTO stock (scrip, company_name, previous_closing, trade_date, closing_price) values(?,?,?,?,?)",(stock.scrip, stock.company_name, stock.previous_closing, stock.trade_date, stock.closing_price, ))
        con.commit()
        return True