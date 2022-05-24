from pprint import pprint

import requests

data1 = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
pprint(data1['Valute']['USD']['Value'])
data2 = data1['Valute']['USD']['Value']

