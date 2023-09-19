import requests
from portfoliotracker.entities import BaseResponse
from portfoliotracker.entities.stock import Stock
from portfoliotracker.repo.api_repo import APIRepo
from portfoliotracker.entities.user import User


class APIService:

    def __init__(self, api_repo: APIRepo):
        self.api_url = "https://www.nepalipaisa.com/api/GetTodaySharePrice"
        self.api_repo = api_repo

    def get_stock_prices_from_api(self):
        response = requests.get(self.api_url)
        result = response.json()
        return result

    def update_prices_todb(self) -> BaseResponse:

        try:
            result = self.get_stock_prices_from_api()
            # print(result)
            for item in result['result']['stocks']:
              stock = Stock(scrip=item['stockSymbol'], closing_price=item['closingPrice'], previous_closing=item['previousClosing'], trade_date=item['tradeDate'], difference_rs=item['differenceRs'], percent_change=item['percentChange'])

              response = self.api_repo.update_stock_prices(stock)
            if not response:
              raise Exception("Could not update a stock_prices!")
            return BaseResponse(error=False, success=True, msg='success')
        except Exception as e:
            return BaseResponse(error=True, success=False, msg=str(e))

    def get_stock_price_db(self, stockSymbol: str):
        result = self.api_repo.fetch_stock_price(stockSymbol)
        if result:
            return dict(stockSymbol=result[0], previous_closing=result[1], trade_date=result[2], closing_price=result[3])

    def transactions_stock_price(self, user: User) -> list:
        pricesDict = []
        for stockSymbol in self.distinct_stockSymbols(user):
            result = self.get_stock_price_db(user, stockSymbol)
            if result:
                pricesDict.append(result)
        return pricesDict

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

    def is_tradeDate_same(self):
      from portfoliotracker.repo import TransactionRepo
      from portfoliotracker.repo.db import get_db_connection
      db = get_db_connection()

      trans_repo = TransactionRepo(db)
      
      result = self.get_stock_prices_from_api()
      api_date = result['result']['stocks'][1]['tradeDate']

      db_date = trans_repo.get_stock_tradeDate()
      if api_date == db_date:
          return True
      return False
