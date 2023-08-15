from portfoliotracker.repo.transaction_repo import TransactionRepo
from portfoliotracker.utils.methods import *
from portfoliotracker.entities import User, Transaction, BaseResponse


import csv


class TransactionService:
    def __init__(self, trans_repo: TransactionRepo):
        self.trans_repo = trans_repo

    def upload_transactions(self, user: User, file_location)  -> BaseResponse:
        
        try:
            transaction_data = []
            with open(file_location, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    
                    transaction = Transaction(scrip= row['Scrip'], transaction_date = date_format(row['Transaction Date']),credit_quantity = stringToInt(row['Credit Quantity']), debit_quantity = stringToInt(row['Debit Quantity']), balance_after_transaction = stringToInt(row['Balance After Transaction']),history_description = shorten_history(row['History Description']))
                    
                    transaction_data.append(row)
                    success = self.trans_repo.insert_transaction(user, transaction)
                    if not success:
                        raise Exception ("Could not insert a transaction!")
                return BaseResponse(error=False, success=True, result=transaction_data)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg = str(e))
        
    def check_transaction(self, user: User) -> bool:
        result = self.trans_repo.retrieve_all_transaction(user)
        if result is None:
            return False
        return True

    def distinct_stockSymbols(self, user:User) -> list:
        stockSymbols = []
        for item in self.trans_repo.retrieve_distinct_scrip(user):
            stockSymbols.append(item[0])
        print(stockSymbols)
        return stockSymbols
    
    def balanced_transactions_with_prices(self, user:User, stockSymbol: str):
        result = self.trans_repo.transaction_join_stock(user, stockSymbol)
        print(result)
        for item in result:
            if item[5] <= 0:
                return None
            return dict(stockSymbol = item[1], transaction_date = item[2], balance = item[5], previous_price=item[9], trade_date=item[10], closing_price=item[11])   
            
    
    def transactions_balance_price_info(self, user:User):
        transactionDict =[]
        for stockSymbol in self.distinct_stockSymbols(user):
            result = self.balanced_transactions_with_prices(user, stockSymbol)
            if result:
                transactionDict.append(result)
        return transactionDict

    