import requests

try:
    courses = requests.get('https://api.binance.com/api/v3/ticker/price').json()
    print(courses)
except:
    print('huy')