from django.contrib import admin
from .models import TelegramUser, Order, MyInfo

# Register your models here.
admin.site.register(TelegramUser)
admin.site.register(Order)
admin.site.register(MyInfo)