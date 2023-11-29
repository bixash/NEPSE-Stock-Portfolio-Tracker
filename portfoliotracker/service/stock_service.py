import requests
from portfoliotracker.entities import BaseResponse
from portfoliotracker.entities.stock import Stock
from portfoliotracker.repo.stock_repo import StockRepo
from portfoliotracker.entities.user import User
from portfoliotracker.utils.methods import *

from portfoliotracker.repo import TransactionRepo
from portfoliotracker.repo.db import get_db_connection
trans_repo = TransactionRepo(get_db_connection())

class StockService:

    def __init__(self, stock_repo: StockRepo):
        self.api_url = "https://www.nepalipaisa.com/api/GetTodaySharePrice"
        self.stock_repo = stock_repo

    def get_stock_prices_from_api(self)-> BaseResponse:
        try:
            response = requests.get(self.api_url)
            result = response.json()
            return BaseResponse(error=False, success=True, msg='Got prices from api!', result=result)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))
        
    def update_prices_todb(self) -> BaseResponse:

        try:
            api_response = self.get_stock_prices_from_api()
           
            if not api_response.success:
                raise Exception("Could not update a stock_prices!")
            result = api_response.result
            for item in result['result']['stocks']:
                stock = Stock(scrip=item['stockSymbol'], closing_price=item['closingPrice'], previous_closing=item['previousClosing'], trade_date=item['tradeDate'], difference_rs=item['differenceRs'], percent_change=item['percentChange'])
                self.stock_repo.update_stock_prices(stock)
            return BaseResponse(error=False, success=True, msg='Stock_prices updated into db!')
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))

    def get_all_stock_prices(self)-> BaseResponse:
        try:
            res= self.stock_repo.select_all_stock_prices()
            resultList = []
            for item in res:
                stock_info = dict(scrip = item[0], previous_closing = item[1], trade_date= convert_date_format(item[2]),closing_price= item[3],difference_rs = item[4],percent_change=item[5] )
                resultList.append(stock_info)
            return BaseResponse(error=False, success=True, msg='success', result= resultList)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))
                
    def getKittaDevPrices():
        url = 'https://api.kitta.dev/stocks/live'

        response = requests.get(url, headers={
            'Authorization': 'f1aed281-9b22-47cd-9fca-ed9ae52a8479'
        })

        result = response.json()
        for item in result:
            scrip = item['stockSymbol']
            closing_price = item['closingPrice']
            # cur.execute("UPDATE stock SET closing_price = ? WHERE scrip = ?",(closing_price, scrip,))
            # con.commit()
        return result

    def is_tradeDate_same_db(self, api_date: str):
        db_date = trans_repo.get_stock_tradeDate()
        if api_date == db_date[0]:
            return True
        else:
            return False
       
    def get_stock_by_scrip(self, scrip: str):

        try:
            stock= self.stock_repo.fetch_stock_price(scrip)
        
            stock_info = dict(scrip = stock[0], previous_closing = stock[1], trade_date= convert_date_format(stock[2]),closing_price= stock[3],difference_rs = stock[4],percent_change=stock[5] )
            return BaseResponse(error=False, success=True, msg='success', result= stock_info)
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))
