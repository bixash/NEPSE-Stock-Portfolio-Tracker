import requests
from bs4 import BeautifulSoup
url = 'https://www.nepalstock.com/api/nots/nepse-data/today-price'
headers = requests.utils.default_headers()

headers.update(
    {
        'Authority': 'www.nepalstock.com',
        'Method': 'POST',
        'Path':'/api/nots/nepse-data/today-price?',
        'Scheme': 'https',
        'Accept':'application/json, text/plain, */*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US,en;q=0.9',

        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',

        'Authorization': 'Salter eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..pIzXG-vlLHGd97Wh3dy_hw4wHtlQWv14rpVDdSkKG3esO1JmFax6fJtCpifDuYAXvimddCg6JDA5qcDcghpjqiSQhRPCRB6nGJCkOj9KZ2qhGzYlg8D397vNNQF2K9CxloPW2A8g5eaIJVlLml4ilk3DBk701ZDYkEKPOaiyWjQ.3RqbpMjjcj9HcMHIM8qsjA',

        'Content-Length': '13',

        'Content-Type':'application/json',

        'Origin':'https://www.nepalstock.com',

        'Referer':'https://www.nepalstock.com/today-price'
    }
)

json = {'id':'352987'}
# response = requests.get(url, headers=headers)
response = requests.post(url, headers=headers, json= json)
print(response.text)

# soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.title)