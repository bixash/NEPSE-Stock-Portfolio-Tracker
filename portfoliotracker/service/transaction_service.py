from portfoliotracker.repo.transaction_repo import TransactionRepo
from portfoliotracker.utils.methods import *
from portfoliotracker.entities import User, Transaction, BaseResponse


import csv


class TransactionService:
    def __init__(self, trans_repo: TransactionRepo):
        self.trans_repo = trans_repo

    def upload_transactions(self, user: User, file_location :str)  -> BaseResponse:
        with open(file_location, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    transaction = Transaction(scrip= row['Scrip'], transaction_date = date_format(row['Transaction Date']),credit_quantity = stringToInt(row['Credit Quantity']), debit_quantity = stringToInt(row['Debit Quantity']), balance_after_transaction = stringToInt(row['Balance After Transaction']),history_description = shorten_history(row['History Description']))
                except Exception:
                    return BaseResponse(error=True, success=False, msg="CSV file is not valid in format!")
                if not self.trans_repo.insert_transaction(user, transaction):
                    return BaseResponse(error=True, success=False, msg="Could not insert a transaction into db!")
            return BaseResponse(error=False, success=True, msg="success")
 
    def check_transaction(self, user: User) -> bool:
        result = self.trans_repo.retrieve_all_transaction(user)
        if result is None:
            return False
        return True

    def distinct_stockSymbols(self, user:User) -> list:
        stockSymbols = []
        for item in self.trans_repo.retrieve_distinct_scrip(user):
            stockSymbols.append(item[0])
        return stockSymbols
    
    def balanced_transactions_with_prices(self, user:User, stockSymbol: str):
        result = self.trans_repo.transaction_join_stock(user, stockSymbol)
        """[(39, 'MKHC', '2023-03-17', 10, 0, 10, 'IPO-MKHCL-079/80', 8, 215.8, '2023-08-14', 215.9, 0.1, 0.05)]"""
        for item in result:
            if item[5] <= 0:
                return None
            return dict(stockSymbol = item[1], transaction_date = item[2], balance = item[5], previous_price=item[8], trade_date=item[9], closing_price=item[10], difference_rs = item[11], percent_change = item[12])   
            
    
    def transactions_balance_price_info(self, user:User):
        transactionDict =[]
        for stockSymbol in self.distinct_stockSymbols(user):
            result = self.balanced_transactions_with_prices(user, stockSymbol)
            if result:
                transactionDict.append(result)
        return transactionDict

    