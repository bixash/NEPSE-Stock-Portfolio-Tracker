import requests
from bs4 import BeautifulSoup
# url = 'https://www.nepalstock.com/api/nots/nepse-data/today-price'
url = "https://www.nepalipaisa.com/api/GetCompanies"
headers = requests.utils.default_headers()

# headers.update(
#     {
#         'Authority': 'www.nepalstock.com',
#         'Method': 'POST',
#         'Path':'/api/nots/nepse-data/today-price?',
#         'Scheme': 'https',
#         'Accept':'application/json, text/plain, */*',
#         'Accept-Encoding':'gzip, deflate, br',
#         'Accept-Language':'en-US,en;q=0.9',

#         'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36',

#         'Authorization': 'Salter eyJlbmMiOiJBMTI4Q0JDLUhTMjU2IiwiYWxnIjoiZGlyIn0..pIzXG-vlLHGd97Wh3dy_hw4wHtlQWv14rpVDdSkKG3esO1JmFax6fJtCpifDuYAXvimddCg6JDA5qcDcghpjqiSQhRPCRB6nGJCkOj9KZ2qhGzYlg8D397vNNQF2K9CxloPW2A8g5eaIJVlLml4ilk3DBk701ZDYkEKPOaiyWjQ.3RqbpMjjcj9HcMHIM8qsjA',

#         'Content-Length': '13',

#         'Content-Type':'application/json',

#         'Origin':'https://www.nepalstock.com',

#         'Referer':'https://www.nepalstock.com/today-price'
#     }
# )

headers.update(
    {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection':'keep-alive',
        'Content-Length': '2',
        'Content-Type':'application/json; charset=UTF-8',
        'Cookie':'_ga=GA1.1.147338546.1689132925;fpestid=7wjek7hWWIcbEQWLgdUQKEWSIM5TqrqizjNnMc0j7pDA7OImb-_WrBgDgLk3ev1WbKrbcw;_cc_id=959ef3cd1e06f867fa8956d2c475870e; panoramaId_expiry=1689591808359;panoramaId=36835cca2cdee06b3b98bdc8a440a9fb927ae83b7ec6e7d40e476046522c1e76; panoramaIdType=panoDevice;_ga_MSBMR2LE7J=GS1.1.1689505405.3.1.1689506448.0.0.0',

        'Host':'www.nepalipaisa.com',

        'Origin':'https://www.nepalipaisa.com',

        'Referer':'https://www.nepalipaisa.com/today-share-price',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Mobile Safari/537.36'
    }
)

# json = {'id':'352987'}
response = requests.post(url, headers=headers)
# response = requests.post(url, headers=headers, json= json)
print(response)

