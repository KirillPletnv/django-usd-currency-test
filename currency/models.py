from django.db import models


class ExchangeRate(models.Model):
    rate = models.FloatField(verbose_name="Курс USD/RUB")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время обновления")

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Курс валюты"
        verbose_name_plural = "Курсы валют"

    @classmethod
    def get_last_rates(cls, count=10):
        return list(cls.objects.values('rate', 'timestamp')[:count])

    def __str__(self):
        return f"1 USD = {self.rate} RUB ({self.timestamp})"