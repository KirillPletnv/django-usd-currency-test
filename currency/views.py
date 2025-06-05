from django.utils import timezone
from django.http import JsonResponse
from .models import ExchangeRate
from .service import requests_api
from .time_check import current_rate_limit


@current_rate_limit
def get_current_usd(_):
    valute = 'USD'
    rate = requests_api(valute)
    last_10_rate = ExchangeRate.get_last_rates(count=10)
    response = JsonResponse({ 'current_rate': rate, 'history': last_10_rate, })
    return response
