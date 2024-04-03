from rest_framework import viewsets, permissions
from .models import TelegramUser, Order
from .serializers import TelegramUserSerializer, OrderSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from rest_framework.decorators import action
from coin.models import Mining
from rest_framework.response import Response
from .payment import create_invoice_func
import requests
from rest_framework import status
from rest_framework.decorators import api_view
##






class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    # lookup_field = 'telegram_id'


@api_view(['GET'])
def set_telegram_webhook(request):
    # print("request")
    TELEGRAM_BOT_TOKEN = '6637720245:AAGLltaPLybSJxuXWkZDthbN92TSOLwQUvA'
    # WEBHOOK_URL = 'https://cardanomaze.onrender.com/telegram_webhook/'
    # url = f'https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/setWebhook'
    updates_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    # updates_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe"

    response = requests.get(updates_url)  # Making a GET request to get updates.
    if response.status_code == 200:
        updates = response.json().get("result", [])
        for update in updates:
            message = update.get("message", {})
            user = message.get("from", {})
            if user:  # Check if user info is present
                # Assuming `TelegramUserSerializer` expects all these fields.
                serializer = TelegramUserSerializer(data={
                    "username": user.get("username", ""),
                    "first_name": user.get("first_name"),
                    "last_name": user.get("last_name", ""),
                    "telegram_id": user.get("id"),
                })
                if serializer.is_valid():
                    serializer.save()  # This saves the model instance.
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'status': 'ok'}, status=status.HTTP_201_CREATED)
    else:
        return Response({'error': 'Failed to fetch updates'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


   


    # updates = response.json().get("result", [])
    # for update in updates:
    #     message = update.get("message", {})
    #     user = message.get("from", {})
    #     user_info = {
    #         "user_id": user.get("id"),
    #         "is_bot": user.get("is_bot"),
    #         "first_name": user.get("first_name"),
    #         "last_name": user.get("last_name", ""),
    #         "username": user.get("username", ""),
    #         "language_code": user.get("language_code", "")
    #     }
    #     telegram_user = TelegramUser.objects.create(
    #         username=user.get("username", ""),
    #         first_name=user.get("first_name"),
    #         last_name=user.get("last_name", ""),
    #         telegram_id=user.get("id"),
    #     )
    #     serializer = TelegramUserSerializer(data=telegram_user)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, {'status': 'ok'}, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # print(user_info)
    # if request.method == 'POST':
    #     message = request.data.get('message', {})
    #     user_info = message.get('from', {})
    #     telegram_id = user_info.get('id')
    #     username = user_info.get('username')
    #     first_name = user_info.get('first_name')
    #     last_name = user_info.get('last_name')
    #     telegram_user = TelegramUser.objects.create(
    #         username=username,
    #         first_name=first_name,
    #         last_name=last_name,
    #         telegram_id=telegram_id
    #     )
    #     serializer = TelegramUserSerializer(data=telegram_user)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, {'status': 'ok'}, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        # return Response({'status': 'ok', 'data': request.data}, status=status.HTTP_200_OK)
    # response = requests.post(url, data={'url': WEBHOOK_URL})
    # response_data = response.json()
    # response.raise_for_status()
    # return Response(response_data)




@csrf_exempt
def telegram_update(request):
    if request.method == "POST":
        update = json.loads(request.body)
        user_data = update.get('message', {}).get('from')
        if user_data:
            TelegramUser.objects.update_or_create(
                telegram_id=user_data['id'],
                defaults={
                    'first_name': user_data.get('first_name'),
                    'last_name': user_data.get('last_name'),
                    'username': user_data.get('username'),
                }
            )
        return JsonResponse({"ok": True})
    return JsonResponse({"error": "Method not allowed"}, status=405)



class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Order.objects.filter(user_id=self.kwargs["users_pk"])
    
    def perform_create(self, serializer):
        user_url_id = self.kwargs["users_pk"]
        active_user = TelegramUser.objects.get(id=user_url_id)
        print(active_user.telegram_id)
        serializer.save(user=active_user)
 
    
    @action(detail=True, methods=['post', 'get'], url_path='invoice')
    def invoice(self, request, pk=None, users_pk=None):
    # def invoice(self, request):
        user_url_id = self.kwargs["users_pk"]
        active_user = TelegramUser.objects.get(id=user_url_id)
        order = self.get_object()
        fiat_amount = order.fiat_amount
        fiat_currency = order.fiat_currency
        crypto_currency = order.crypto_currency
        order_id = str(active_user.telegram_id)
        # print(user_url_id)
        return create_invoice_func(active_user, fiat_amount, fiat_currency, crypto_currency, order_id)

        # return Response({"status": "Success", "value":f"teleID {order_id} {fiat_amount} {fiat_currency} {crypto_currency}"})
    
    