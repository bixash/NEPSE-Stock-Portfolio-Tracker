from portfoliotracker.repo.transaction_repo import TransactionRepo
from portfoliotracker.utils.methods import *
from portfoliotracker.entities import User, Transaction, BaseResponse



import csv
import threading 

lock = threading.Lock()


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
        for item in self.trans_repo.select_distinct_scrip(user):
            stockSymbols.append(item[0])
        return stockSymbols
    

    def get_sector_summary(self, trans:dict, sectorList: list )-> list:
        
        sectorInfo = []
        for sector in sectorList:
            count = 0
            value = 0
            for item in trans:
                if item['sector'] == sector[0]:
                    count = count + 1
                    value = value + item['closing_price'] * item['balance']
            sectorInfo.append(dict(sector= sector[0], no_of_scrip = count, total_value=  round(value, 2)))
        return sectorInfo     


    def XYarray(self, sectorInfo:list):
        xarray = []
        yarray = []
        for item in sectorInfo:
            if item['total_value'] > 0:
                xarray.append(item['sector'])
                yarray.append(item['total_value'])
        return {'xValues': xarray, 'yValues': yarray}

    def sectorDicttoArray(self, arr:list)-> list:
        resultArray = [['Sector', 'Total Value'],]
        for item in arr:
            resultArray.append([item['sector'], item['total_value']])
        return resultArray

    def get_instrument_summary(self, trans:dict, instrument: list):
        instrumentInfo = []
        for ins in instrument:
            count = 0
            value = 0
            for item in trans:
                if item['instrument'] == ins[0]:
                    count = count + 1
                    value = value + item['closing_price'] * item['balance']
            instrumentInfo.append(dict(instrument= ins[0], no_of_scrip = count, total_value= round(value, 2)))
        return instrumentInfo
    
    def instrumentDicttoArray(self, arr:list)-> list:
        resultArray = [['Instrument', 'Total Value'],]
        for item in arr:
            resultArray.append([item['instrument'], item['total_value']])
        return resultArray

    def get_statusActive_scrip(self, trans:dict):
        temp = []
        for item in trans:
            if item['status'] == 'Active':
                temp.append(item)
        return temp

    def get_holdings(self, trans: dict):
        holds=[]
        for item in trans:
            if item['balance'] > 0 and item['balance'] != None:
                holds.append(item)
        return holds
    
    def get_holdings_summary(self, holdings: list):
        invest_value = 0
        current_value = 0
        previous_value = 0
        profit_loss = 0
        for item in holdings:
            invest_value= invest_value + (item['unit_price']* item['balance'])
            current_value= current_value + (item['closing_price'] * item['balance'])
            previous_value = previous_value + (item['previous_price']* item['balance'])
        profit_loss = round(current_value - invest_value, 2)
        profit_loss_percent = round((profit_loss * 100)/invest_value, 2)
        today_profit_loss = round(current_value - previous_value, 2)
        today_PL_percent = round((today_profit_loss * 100)/ previous_value, 2)
        
        return {"invest_value": invest_value, "current_value": current_value, "profit_loss": profit_loss, "today_profit_loss": today_profit_loss,  "today_PL_percent": today_PL_percent, "profit_loss_percent":  profit_loss_percent}

            
    
    def get_joined_result(self, user:User)->BaseResponse:
        try:
            lock.acquire(True)
            transactionDict =[]
            for stockSymbol in self.get_distinct_stockSymbols(user):
                result = self.trans_repo.join_one_transaction_stock_company(user, stockSymbol)
                for item in result:
                    """id|scrip|transaction_date|credit_quantity|debit_quantity|balance_after_transaction|history_description|unit_price|uid|previous_closing|trade_date|closing_price|difference_rs|percent_change|company_name|status|sector|instrument|email|url"""

                    stock = dict(stockSymbol = item[1], transaction_date = item[2], balance = item[5], unit_price=item[7], previous_price=item[9], trade_date=item[10], closing_price=item[11], difference_rs = item[12], percent_change = item[13], company_name = item[14], status= item[15], sector = item[16], instrument = item[17] )
                    transactionDict.append(stock)
            return BaseResponse(error=False, success=True, msg="success", result=transactionDict)    
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))
        finally:
            lock.release()

    
    def recent_transactions(self, user:User):
        try:
            # res = self.trans_repo.retrieve_limit_transaction(user)
            result = self.dictifiy_transactions(self.trans_repo.retrieve_limit_transaction(user))
            # print (result)
            return BaseResponse(error=False, success=True, msg="success", result=result)    
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))
        
    def all_transactions(self, user:User):
        try:
            # res = self.trans_repo.retrieve_limit_transaction(user)
            result = self.dictifiy_transactions(self.trans_repo.retrieve_all_transaction(user))
            # print (result)
            return BaseResponse(error=False, success=True, msg="success", result=result)    
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))
    
    def dictifiy_transactions(self, transactions:tuple):
        # MKHC|2023-03-17|10|0|10|IPO-MKHCL-079/80|100.0|1
        resultList = []
        for item in transactions:
            transaction = dict(scrip = item[0], transaction_date= convert_date_format(item[1]), credit_quantity = item[2], debit_quantity = item[3], after_balance = item[4], history_description =item[5], unit_price =item[6])
            resultList.append(transaction)
        return resultList

                
    def check_user_transactions(self, user:User)->bool:
        if self.trans_repo.retrieve_all_transaction(user):
            return True
        return False
    
    def get_transactions_by_scrip(self, user:User, scrip: str):
        try:
            result= self.dictifiy_transactions(self.trans_repo.retrieve_transaction_by_scrip(user, scrip))
            return BaseResponse(error=False, success=True, msg="success", result=result)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg = str(e))
       
           

    def delete_transactions(self, user_id:int):
        try:
            result = self.trans_repo.delete_transaction(user_id)
            return BaseResponse(error=False, success=True, msg="success", result=result)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg = str(e))