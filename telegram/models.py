from django.db import models

# Create your models here.

class MyInfo(models.Model):
    name = models.CharField(max_length=255, default="Shady", unique=True)
    api_key = models.CharField(max_length=1055, default="api-key-123", unique=True)
  
    def __str__(self):
        return self.name


class TelegramUser(models.Model):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    telegram_id = models.CharField(unique=True, max_length=200)
    currency = models.CharField(max_length=50, default="ADA")
    


    def __str__(self):
        return self.username


class Order(models.Model):
    user = models.ForeignKey(TelegramUser, related_name='user_order', on_delete=models.SET_NULL, null=True, blank=True)
    fiat_amount = models.DecimalField(max_digits=15, default="3.00", decimal_places=2)
    fiat_currency = models.CharField(max_length=50, default="usd")
    crypto_currency = models.CharField(max_length=50, default="ADA")
    isPaid = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user} - {self.isPaid}"