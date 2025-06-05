import time
from django.test import TestCase, RequestFactory
from django.http import JsonResponse
from .time_check import current_rate_limit
import json



def request_api_generator():
    value = 78.5025
    while True:
        yield value
        value += 1


gen = request_api_generator()
fake_request_api = lambda: next(gen)


def fake_last_rate():
    return [
        {"rate": 78.5025, "timestamp": "2025-06-04T23:29:22.044Z"},
        {"rate": 78.5025, "timestamp": "2025-06-04T23:23:59.134Z"},
        {"rate": 78.5025, "timestamp": "2025-06-04T23:21:17.356Z"},
        {"rate": 78.5025, "timestamp": "2025-06-04T23:20:42.572Z"},
        {"rate": 78.5025, "timestamp": "2025-06-04T23:18:24.139Z"},
        {"rate": 78.5025, "timestamp": "2025-06-04T23:14:11.325Z"},
        {"rate": 78.5025, "timestamp": "2025-06-04T23:12:12.561Z"},
        {"rate": 78.5025, "timestamp": "2025-06-04T23:11:06.413Z"},
        {"rate": 78.5025, "timestamp": "2025-06-04T23:10:55.384Z"},
        {"rate": 78.5025, "timestamp": "2025-06-04T23:09:19.574Z"}]


def dummy_view(request):
    return JsonResponse({'current_rate': fake_request_api(), 'history': fake_last_rate(),})


class CurrentRateLimitDecoratorTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        #cache.clear()
        self.decorated_view = current_rate_limit(dummy_view)

    def test_response_caching(self):
        """Тест кеширования"""
        request = self.factory.get('/fake-url/')

        # Получаем первый ответ
        response1 = self.decorated_view(request)
        first_data = json.loads(response1.content)
        self.assertEqual(len(first_data['history']), 10)
        first_value = first_data['current_rate']  # Фиксируем первое значение

        # Точно меняем курс
        fake_request_api()

        # Получаем второй ответ (из кеша)
        response2 = self.decorated_view(request)
        second_data = json.loads(response2.content)

        # Проверяем, что значение не изменилось
        self.assertEqual(first_value, second_data['current_rate'])
        self.assertEqual(response1.content, response2.content)
        time.sleep(11)


        # Проверяем, что через 10 секунд значение изменилось
        response3 = self.decorated_view(request)
        third_data = json.loads(response3.content)
        self.assertNotEqual(first_value, third_data['current_rate'])






