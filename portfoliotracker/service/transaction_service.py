from portfoliotracker.repo.transaction_repo import TransactionRepo
from portfoliotracker.utils import utils
from portfoliotracker.utils.methods import stringToInt, date_format, convert_date_format, shorten_history
from portfoliotracker.entities import User, Transaction, BaseResponse, Stock

from portfoliotracker.repo.db import get_db_connection
from portfoliotracker.repo.stock_repo import StockRepo
from portfoliotracker.repo.company_repo import CompanyRepo



import csv
import threading 

lock = threading.Lock()

stock_repo = StockRepo(get_db_connection())
company_repo = CompanyRepo(get_db_connection())

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
                    return BaseResponse(error=True, success=False, msg="File is not in valid format!")
                if not self.trans_repo.insert_transaction(user, transaction):
                    return BaseResponse(error=True, success=False, msg="Could not insert a transaction into db!")
            return BaseResponse(error=False, success=True, msg="success")
 
    def check_user_transactions(self, user:User)->bool:
        if self.trans_repo.retrieve_all_transaction(user):
            return True
        return False
    
    def distinct_stockSymbols(self, user:User) -> list:
        stockSymbols = []
        distinct = self.trans_repo.select_distinct_scrip(user)
        for item in distinct:
            stockSymbols.append(item[0])
        return stockSymbols

    def sector_summary(self, trans_company:dict )-> list:
        
        sectorList = company_repo.select_all_distinct_sector()
        sectorInfo = []
        for sector in sectorList:
            count = 0
            value = 0
            for item in trans_company:
                if item['sector'] == sector[0]:
                    count = count + 1
                    value = value + item['current_value']
            sectorInfo.append(dict(sector= sector[0], no_of_scrip = count, total_value=  round(value, 2)))
        return sectorInfo     

    def XYarray(self, stats:list):
        xarray = []
        yarray = []
        # if stats
        for item in stats:

            if item['total_value'] > 0:
                xarray.append(item['sector'])
                yarray.append(item['total_value'])
        return {'xValues': xarray, 'yValues': yarray}

    def instrument_summary(self, trans_company:dict):
        instruments = company_repo.select_all_distinct_instrument()
        instrumentInfo = []
        for ins in instruments:
            count = 0
            value = 0
            for item in trans_company:
                if item['instrument'] == ins[0]:
                    count = count + 1
                    value = value + item['current_value']
            instrumentInfo.append(dict(instrument= ins[0], no_of_scrip = count, total_value= round(value, 2)))
        return instrumentInfo
    
    def holdings_summary(self, holdings: list):
        total_invest_value = 0
        total_current_value = 0
        total_previous_value = 0
        total_sold_value = 0
        total_profit_loss = 0
        total_credit_quantity = 0
        total_debit_quantity = 0
        total_balance_quantity = 0 
        total_balance_percent = 0
        total_profit_loss = 0
        total_profit_loss_percent = 0
        today_profit_loss = 0
        today_profit_loss_percent = 0
        avg_invest_value=0
        for stock in holdings:
            total_credit_quantity = total_credit_quantity + stock['credit_quantity']
            total_debit_quantity = total_debit_quantity + stock['debit_quantity']
            total_invest_value=  total_invest_value + stock['invest_value']
            avg_invest_value = avg_invest_value+ stock['avg_invest_value']
            total_sold_value = total_sold_value + stock['sold_value']
            total_current_value= total_current_value + stock['current_value']
            total_previous_value = total_previous_value + stock['previous_value']

        if total_credit_quantity > 0:
            total_balance_quantity = total_credit_quantity-total_debit_quantity
            total_balance_percent = round((total_balance_quantity / total_credit_quantity)*100, 2)
            # total_profit_loss = round((total_sold_value + total_current_value) - total_invest_value, 2)
            # total_profit_loss = round(total_current_value - total_invest_value, 2)
            total_profit_loss = round(total_current_value - avg_invest_value, 2)
            # total_profit_loss_percent = round((total_profit_loss * 100)/total_invest_value, 2)
            total_profit_loss_percent = round((total_profit_loss * 100)/avg_invest_value, 2)
            today_profit_loss = round(total_current_value - total_previous_value, 2)
            today_profit_loss_percent = round((today_profit_loss * 100)/ total_previous_value, 2)
        return {"invest_value": round(total_invest_value, 2), "current_value": round(total_current_value, 2), "total_profit_loss": total_profit_loss, "today_profit_loss": today_profit_loss,  "today_profit_loss_percent": today_profit_loss_percent, "total_profit_loss_percent":  total_profit_loss_percent, "total_credit_quantity" : total_credit_quantity, 'total_debit_quantity':total_debit_quantity, 'total_balance_quantity': total_balance_quantity, "total_balance_percent":  total_balance_percent,  "total_sold_value": total_sold_value, "avg_invest_value": avg_invest_value }
    
    def portfolio_summary(self, holdings: list):
        total_invest_value = 0
        total_current_value= 0
        total_sold_value = 0
        total_profit_loss = 0
        total_credit_quantity = 0
        total_debit_quantity = 0
        total_balance_quantity = 0 
        total_balance_percent = 0
        total_profit_loss_percent = 0
        for stock in holdings:
            total_credit_quantity = total_credit_quantity + stock['credit_quantity']
            total_debit_quantity = total_debit_quantity + stock['debit_quantity']

            total_invest_value=  total_invest_value + stock['invest_value']
            total_sold_value = total_sold_value + stock['sold_value']
            total_current_value= total_current_value + stock['current_value']

        if total_credit_quantity > 0:
            total_balance_quantity = total_credit_quantity-total_debit_quantity
            total_balance_percent = round((total_balance_quantity / total_credit_quantity)*100, 2)
            total_profit_loss = round((total_sold_value + total_current_value) - total_invest_value, 2)
            total_profit_loss_percent = round((total_profit_loss * 100)/total_invest_value, 2)
        
        return {"total_invest_value": round(total_invest_value, 2), "total_profit_loss": total_profit_loss, "total_profit_loss_percent":  total_profit_loss_percent, "total_credit_quantity" : total_credit_quantity, 'total_debit_quantity':total_debit_quantity, 'total_balance_quantity': total_balance_quantity, "total_balance_percent":  total_balance_percent,  "total_sold_value": total_sold_value,}

    def holdings_stats(self, user:User, trans_stock:list):
        holdings = []
        for stockSymbol in trans_stock:
            if self.transactions_stock_price(stockSymbol):
                prices = self.transactions_stock_price(stockSymbol)
                stats = self.stock_transaction_stats(user, stockSymbol)

                current_value = stats['balance_quantity'] * prices.closing_price
                previous_value = stats['balance_quantity'] * prices.previous_closing
                

                holdings.append(dict(scrip=stockSymbol, credit_quantity= stats['credit'], debit_quantity= stats['debit'], balance_quantity=stats['balance_quantity'], closing_price = prices.closing_price, previous_closing = prices.previous_closing, difference_rs = prices.difference_rs, percent_change=prices.percent_change, invest_value = stats["invest_value"], sold_value=stats["sold_value"], current_value=round(current_value, 2), previous_value = previous_value, avg_invest_value=stats['avg_invest_value'], average_cost = stats['average_cost'], profit_loss = stats['profit_loss'], net_change = stats['net_change'] ))
        return holdings    

    def holdings_only(self, holdingsList:list) -> list:
        holdingsOnly =[]
        for stock in holdingsList:
            if stock['balance_quantity'] > 0:
                holdingsOnly.append(stock)
        return holdingsOnly

    def holdings_sector_instrument(self, company_stats: list, sector:str, instrument:str):
        resultList = []
        if sector == 'Sectors' and instrument == 'Stocks':
                resultList = company_stats
        elif (sector == 'Sectors' and instrument != 'Stocks'):
            for stock in company_stats:
                if instrument == stock['instrument']:
                    resultList.append(stock)
        elif (sector != 'Sectors' and instrument == 'Stocks'):
            for stock in company_stats:
                if sector == stock['sector']:
                    resultList.append(stock)
        else:
            for stock in company_stats:
                if sector == stock['sector'] and instrument == stock['instrument']:
                    resultList.append(stock)
        return resultList

    def holdings_sector_instrument_list(self,  holdings:list) -> dict:
        sectors =[]
        instruments = []
        # print(holdings)
        for item in holdings:
            # sector = item['sector']
            # instrument = item['instrument']
            if item['sector'] not in sectors:
                sectors.append(item['sector'])
            if item['instrument'] not in instruments:
                instruments.append(item['instrument'])
        return dict(sectors=sectors, instruments = instruments)
    
    def transactions_stock_price(self, scrip:str):
        
        if stock_repo.select_stock_by_scrip(scrip):
            stock_res = stock_repo.select_stock_by_scrip(scrip)

            stock = Stock(scrip=stock_res[0], previous_closing=stock_res[1], trade_date=stock_res[2], closing_price=stock_res[3], difference_rs=stock_res[4], percent_change=stock_res[5])

            return stock

    def company_stats(self, holdings: list) -> list:
        company_stats_list = []
        for stock in holdings:
            scrip = stock['scrip']
            company_res = self.company_info(scrip)
            
            company_stats_list.append(dict(scrip = scrip, sector = company_res['sector'], instrument= company_res['instrument'], status = company_res['status'], closing_price = stock['closing_price'], previous_closing = stock['previous_closing'], difference_rs = stock['difference_rs'], percent_change = stock['percent_change'], credit_quantity=stock['credit_quantity'], balance_quantity = stock['balance_quantity'], debit_quantity = stock['debit_quantity'], current_value = stock['current_value'], invest_value = stock['invest_value'], sold_value = stock["sold_value"], previous_value = stock['previous_value'], avg_invest_value=stock['avg_invest_value'], average_cost = stock['average_cost'], profit_loss = stock['profit_loss'], net_change = stock['net_change'] ))
        return company_stats_list
    
    def company_info(self, scrip:str) -> list:
        
        if company_repo.select_company_by_scrip(scrip):
            company_res = company_repo.select_company_by_scrip(scrip)
            company = dict(scrip = scrip, sector = company_res[0][1], instrument= company_res[0][2], status = company_res[0][3])
        return company

    def stock_transaction_stats(self, user:User, scrip:str):
        total_invest_value = 0
        total_sold_value = 0
        total_credit_quantity = 0
        total_debit_quantity = 0
        total_profit_loss_percent = 0
        total_profit_loss = 0
        overall_percent = 0
        overall_profit_loss = 0
        total_credit_transactions_no = 0
        net_change = 0
        total_unit_price = 0
        avg_invest_value = 0
        average_cost = 0

        prices = self.transactions_stock_price(scrip)
        transactions = utils.dictifiy_transactions(self.trans_repo.retrieve_transaction_by_scrip(user, scrip))
        
        for item in transactions:
            if item['credit_quantity'] > 0:
                total_credit_transactions_no = total_credit_transactions_no + 1
                total_unit_price =  total_unit_price +  item['unit_price']
            total_credit_quantity = total_credit_quantity + item['credit_quantity']
            total_debit_quantity = total_debit_quantity + item['debit_quantity']
            
            total_invest_value = total_invest_value + (item['credit_quantity'] * item['unit_price'])
            total_sold_value = total_sold_value + (item['debit_quantity'] * item['unit_price'])

        # print(item['scrip'], total_credit_transactions_no)
        if total_credit_transactions_no >0:
            average_cost = total_unit_price / total_credit_transactions_no

        
        total_balance_quantity = total_credit_quantity - total_debit_quantity
        current_value = prices.closing_price * total_balance_quantity
        avg_invest_value = average_cost * total_credit_quantity
        profit_loss = current_value - avg_invest_value

        if avg_invest_value > 0:
            net_change = round((profit_loss/avg_invest_value)*100, 2)
        overall_profit_loss = (total_sold_value + current_value) - total_invest_value
        if total_sold_value != 0:
            total_profit_loss = total_sold_value - total_invest_value
            
        if total_invest_value > 0:
            total_profit_loss_percent = round((total_profit_loss / total_invest_value)*100, 2)
            overall_percent =  round((overall_profit_loss / total_invest_value)*100, 2)

        return {"stockSymbol": scrip, "invest_value": total_invest_value, "sold_value": total_sold_value, "total_profit_loss": round(total_profit_loss, 2), "credit": total_credit_quantity, "debit": total_debit_quantity, "balance_quantity": total_balance_quantity, "total_profit_loss_percent": total_profit_loss_percent, "current_value": current_value, "overall_profit_loss": round(overall_profit_loss, 2), "overall_percent": round(overall_percent,2), "average_cost": round(average_cost, 2), "net_change":  net_change, "profit_loss": round(profit_loss, 2), "avg_invest_value": avg_invest_value}

    # def get_joined_result(self, user:User)->BaseResponse:
    #     try:
    #         lock.acquire(True)
    #         transactionDict =[]
    #         for stockSymbol in self.distinct_stockSymbols(user):
    #             result = self.trans_repo.join_one_transaction_stock_company(user, stockSymbol)
    #             for item in result:
    #                 """id|scrip|transaction_date|credit_quantity|debit_quantity|balance_after_transaction|history_description|unit_price|uid|previous_closing|trade_date|closing_price|difference_rs|percent_change|company_name|status|sector|instrument|email|url"""

    #                 stock = dict(stockSymbol = item[1], transaction_date = item[2], credit = item[3], debit =item[4], balance = item[5], unit_price=item[7], previous_price=item[9], trade_date=item[10], closing_price=item[11], difference_rs = item[12], percent_change = item[13], company_name = item[14], status= item[15], sector = item[16], instrument = item[17] )
    #                 transactionDict.append(stock)
    #         return BaseResponse(error=False, success=True, msg="success", result=transactionDict)    
    #     except Exception as e:
    #         return BaseResponse(error=True, success=False, msg=str(e))
    #     finally:
    #         lock.release()

    def recent_transactions(self, user:User):
        try:
            # res = self.trans_repo.retrieve_limit_transaction(user)
            result = utils.dictifiy_transactions(self.trans_repo.retrieve_limit_transaction(user))
            # print (result)
            return BaseResponse(error=False, success=True, msg="success", result=result)    
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))
        
    def all_transactions(self, user:User):
        try:
            # res = self.trans_repo.retrieve_limit_transaction(user)
            result = utils.dictifiy_transactions(self.trans_repo.retrieve_all_transaction(user))
            # print (result)
            return BaseResponse(error=False, success=True, msg="success", result=result)    
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))
                
    def get_all_transactions_by_scrip(self, user:User, scrip: str):
        try:
            result= utils.dictifiy_transactions(self.trans_repo.retrieve_transaction_by_scrip(user, scrip))
            return BaseResponse(error=False, success=True, msg="success", result=result)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg = str(e))
       
    def delete_transactions(self, user_id:int):
        try:
            result = self.trans_repo.delete_transaction(user_id)
            return BaseResponse(error=False, success=True, msg="success", result=result)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg = str(e))
        
        