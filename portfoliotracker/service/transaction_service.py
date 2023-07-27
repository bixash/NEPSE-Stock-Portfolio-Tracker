from portfoliotracker.repo.transaction_repo import TransactionRepo
from portfoliotracker.utils.methods import *
from portfoliotracker.entities import User, Transaction, BaseResponse


import csv


class TransactionService:
    def __init__(self, trans_repo: TransactionRepo):
        self.trans_repo = trans_repo

    def upload_transactions(self, user: User, file_location)  -> BaseResponse:
        
        try:
            with open(file_location, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:

                    transaction = Transaction(scrip= row['Scrip'], transaction_date = date_format(row['Transaction Date']),credit_quantity = stringToInt(row['Credit Quantity']), debit_quantity = stringToInt(row['Debit Quantity']), balance_after_transaction = stringToInt(row['Balance After Transaction']),history_description = shorten_history(row['History Description']))

                    success = self.trans_repo.insert_transaction(user, transaction)
                    if not success:
                        raise Exception ("Could not insert a transaction!")
            return BaseResponse(error=False, success=True)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg = str(e))