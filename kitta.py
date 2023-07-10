import requests
# import json



response = requests.get('https://api.kitta.dev/stocks/live', headers={
  'Authorization': 'f1aed281-9b22-47cd-9fca-ed9ae52a8479'
})

result = response.json()



def getTodayPrice(stocks):
    stock_prices =[]
    for item in result:
        for stock in stocks:
            if stock == item['stockSymbol']:
                stock_prices.append(item['closingPrice'])
                # print(stock_prices)
    return (stock_prices)

# stocks= ["NABIL", "PLI", "NICA"]
# getTodayPrice(stocks)


