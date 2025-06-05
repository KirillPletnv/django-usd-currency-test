import requests
from currency.models import ExchangeRate


def requests_api(valute='USD'):
    response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
    data = response.json()
    rate = data['Valute'][valute]['Value']
    ExchangeRate.objects.create(rate=rate)
    return rate




