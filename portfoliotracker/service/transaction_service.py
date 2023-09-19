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
                    transaction = Transaction(scrip= row['Scrip'], transaction_date = date_format(row['Transaction Date']),credit_quantity = stringToInt(row['Credit Quantity']), debit_quantity = stringToInt(row['Debit Quantity']), balance_after_transaction = stringToInt(row['Balance After Transaction']),history_description = shorten_history(row['History Description']), unit_price = row['Unit Price'])
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
    

    def get_distinct_stockSymbols(self, user:User) -> list:
        stockSymbols = []
        for item in self.trans_repo.retrieve_distinct_scrip(user):
            stockSymbols.append(item[0])
        return stockSymbols
    
    def get_balanced_transactions_with_prices(self, user:User)->BaseResponse:
        try:
            transactionDict =[]
            for stockSymbol in self.get_distinct_stockSymbols(user):
                result = self.trans_repo.last_transaction_join_stock(user, stockSymbol)
                
                for item in result:
                    if item[5] > 0:
                        stock = dict(stockSymbol = item[1], transaction_date = item[2], balance = item[5], previous_price=item[8], trade_date=item[9], closing_price=item[10], difference_rs = item[11], percent_change = item[12])
                        transactionDict.append(stock)
            return BaseResponse(error=False, success=True, msg="success", result=transactionDict)    
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))
    
    def recent_transactions(self, user:User):
        try:
            res = self.trans_repo.retrieve_limit_transaction(user)
            return BaseResponse(error=False, success=True, msg="success", result=res)    
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))
    
    