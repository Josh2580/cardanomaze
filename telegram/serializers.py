from rest_framework import serializers
from .models import TelegramUser, Order
from coin.models import Mining

class TelegramUserSerializer(serializers.ModelSerializer):
    user_coin = serializers.PrimaryKeyRelatedField(many=False, read_only=True)

    class Meta:
        model = TelegramUser
        fields = ['id', 'username', 'first_name', 'last_name', 'telegram_id', 'user_coin']


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.id")

    class Meta:
        model = Order
        fields = "__all__"