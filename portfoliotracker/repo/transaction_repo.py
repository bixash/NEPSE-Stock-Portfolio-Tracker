from portfoliotracker.repo.db import DBConnection
from portfoliotracker.entities import Transaction,  User

class TransactionRepo:
    def __init__(self, db: DBConnection):
        self.db = db

    def delete_transaction(self, user: User):
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("DELETE FROM transactions where uid = ?", (user.user_id,))
        con.commit()
        

    def insert_transaction(self, user: User, transaction: Transaction) -> bool:
        cur = self.db.get_connection()
        con = self.db._commit()
        cur.execute("INSERT INTO transactions( scrip, transaction_date, credit_quantity, debit_quantity,balance_after_transaction, history_description, uid) values(?,?,?,?,?,?,?)", (transaction.scrip, transaction.transaction_date, transaction.credit_quantity, transaction.debit_quantity, transaction.balance_after_transaction, transaction.history_description, user.user_id,))
        con.commit()
        return True
               
    def retrieve_all_transaction(self, user: User):
        cur = self.db.get_connection()
        cur.execute("SELECT scrip, transaction_date, credit_quantity, debit_quantity, balance_after_transaction, history_description from transactions where uid = ? ",(user.user_id,))
        return cur.fetchall()
    
    def retrieve_limit_transaction(self, user: User):
        cur = self.db.get_connection()
        cur.execute("SELECT scrip, transaction_date, credit_quantity, debit_quantity, balance_after_transaction, history_description from transactions where uid = ? ORDER BY transaction_date desc limit 10",(user.user_id,))
        return cur.fetchall()