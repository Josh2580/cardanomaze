from django.db import models
from django.utils import timezone
from telegram.models import TelegramUser


class Mining(models.Model):
    user = models.OneToOneField(TelegramUser, related_name='user_coin', on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(default="CARDANO MAZE", max_length=20)
    quantity_mined = models.DecimalField(max_digits=10, default="100.00", decimal_places=2)
    time_clicked = models.DateTimeField()
    first_click = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    mineral_extracted = models.CharField(max_length=50, default="")
    extraction_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name}"


    