from portfoliotracker.repo.db import DBConnection
from portfoliotracker.entities import Transaction,  User
from portfoliotracker.repo.stock_repo import StockRepo
from portfoliotracker.repo.company_repo import CompanyRepo

import threading 
lock = threading.Lock()

class TransactionRepo:
    def __init__(self, db: DBConnection):
        self.db = db

    def delete_transaction(self, user_id:int) -> bool:
        cur = self.db.get_cursor()
        con = self.db.get_connection()
        cur.execute("DELETE FROM transactions where uid = ?", (user_id,))
        con.commit()
        return True
        

    def insert_transaction(self, user: User, transaction: Transaction) -> bool:
        cur = self.db.get_cursor()
        con = self.db.get_connection()
        cur.execute("INSERT INTO transactions( scrip, transaction_date, credit_quantity, debit_quantity,balance_after_transaction, history_description, unit_price, uid) values(?,?,?,?,?,?,?,?)", (transaction.scrip, transaction.transaction_date, transaction.credit_quantity, transaction.debit_quantity, transaction.balance_after_transaction, transaction.history_description, transaction.unit_price, user.user_id,))
        con.commit()
        return True
               
    def retrieve_all_transaction(self, user: User):
        
        cur = self.db.get_cursor()
        
        cur.execute("SELECT scrip, transaction_date, credit_quantity, debit_quantity, balance_after_transaction,  history_description, unit_price, id from transactions where uid = ? ",(user.user_id,))
        return cur.fetchall()
       
    def retrieve_transaction_by_scrip(self, user: User, stock: str):
        con = self.db.get_connection()
        cur = con.cursor()
        cur.execute("SELECT scrip, transaction_date, credit_quantity, debit_quantity, balance_after_transaction,  history_description, unit_price, id FROM transactions WHERE scrip = ? and uid = ? ORDER BY transaction_date desc",(stock, user.user_id,))
        return cur.fetchall()
    
    def retrieve_limit_transaction(self, user: User):
        cur = self.db.get_cursor()
        cur.execute("SELECT scrip, transaction_date, credit_quantity, debit_quantity, balance_after_transaction, history_description, unit_price, id  from transactions where uid = ? ORDER BY transaction_date desc limit 7",(user.user_id,))
        return cur.fetchall()
    
    def transaction_join_all_stock(self, user: User):
        cur = self.db.get_cursor()
        cur.execute("SELECT * FROM transactions NATURAL JOIN stock WHERE uid = ? ORDER BY transaction_date desc",(user.user_id,))
        return cur.fetchall()
    
    def last_transaction_join_stock(self, user: User, stockSymbol:str):
        cur = self.db.get_cursor()
        cur.execute("SELECT * FROM transactions NATURAL JOIN stock WHERE uid = ? AND scrip = ? ORDER BY transaction_date desc limit 1",(user.user_id, stockSymbol,))
        return cur.fetchall()
    
    def select_distinct_scrip(self, user: User):
        con = self.db.get_connection()
        cur = con.cursor()
        cur.execute("SELECT DISTINCT scrip FROM transactions where uid = ?", (user.user_id,))
        return cur.fetchall()
        
            
    def join_one_transaction_stock_company(self, user: User, stockSymbol: str):
        cur = self.db.get_cursor()
        cur.execute("SELECT * FROM transactions NATURAL JOIN stock  NATURAL JOIN company  WHERE uid = ? AND transactions.scrip = ? ORDER BY transaction_date desc limit 1",(user.user_id, stockSymbol,))
        return cur.fetchall()

    def transaction_join_stock(self, user: User, stockSymbol: str):
        cur = self.db.get_cursor()
        cur.execute("SELECT * FROM transactions NATURAL JOIN stock WHERE uid = ? AND transactions.scrip = ? ORDER BY transaction_date desc limit 1",(user.user_id, stockSymbol,))
        return cur.fetchall()
    