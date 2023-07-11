import requests
# import json
from schema import cur, con



response = requests.get('https://api.kitta.dev/stocks/live', headers={
  'Authorization': 'f1aed281-9b22-47cd-9fca-ed9ae52a8479'
})

result = response.json()


for item in result:
    scrip = item['stockSymbol']
    closing_price = item['closingPrice']
    cur.execute("UPDATE stock SET closing_price = ? WHERE scrip = ?",(closing_price, scrip,))
    con.commit()


# stocks= ["NABIL", "PLI", "NICA"]
# getTodayPrice(stocks)


