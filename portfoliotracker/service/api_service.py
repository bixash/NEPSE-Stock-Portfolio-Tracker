import requests
from portfoliotracker.entities import BaseResponse
from portfoliotracker.entities.stock import Stock
from portfoliotracker.repo.db import DBConnection

# {'stockSymbol': 'NIBLPF', 'companyName': 'NIBL Pragati Fund', 'noOfTransactions': 25, 'maxPrice': 10.13, 'minPrice': 9.1, 'openingPrice': 0.0, 'closingPrice': 9.74, 'amount': 442697.5, 'previousClosing': 9.26, 'differenceRs': 0.48, 'percentChange': 5.18, 'volume': 46597, 'ltv': 0, 'asOfDate': '2023-07-13T15:00:00', 'asOfDateString': 'As of Thu, 13 Jul 2023 | 03:00:00 PM', 'tradeDate': '2023-07-13', 'dataType': None}


db = DBConnection()
cur = db.get_connection()
con = db._commit()

def getStockPrices(stock: Stock) -> BaseResponse:
  
  url = 'https://www.nepalipaisa.com/api/GetTodaySharePrice'
  
  response = requests.get(url)
  result = response.json()

  for item in result['result']['stocks']:
    stock.scrip = item['stockSymbol']
    stock.closing_price = item['closingPrice']
    stock.company_name = item['companyName']
    stock.previous_closing =item['previousClosing']
    stock.trade_date = item['tradeDate']
    
    

def getKittaDevPrices():
  url ='https://api.kitta.dev/stocks/live'

  response = requests.get(url, headers={
  'Authorization': 'f1aed281-9b22-47cd-9fca-ed9ae52a8479'
  })

  result = response.json()
  for item in result:
    scrip = item['stockSymbol']
    closing_price = item['closingPrice']
    cur.execute("UPDATE stock SET closing_price = ? WHERE scrip = ?",(closing_price, scrip,))
    con.commit()




