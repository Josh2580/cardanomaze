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




class TelegramUserViewSet(viewsets.ModelViewSet):
    queryset = TelegramUser.objects.all()
    serializer_class = TelegramUserSerializer
    # lookup_field = 'telegram_id'


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



    
    # return initiate_payment(amount, email, order_id)
    # return Response(initiate_payment(amount, email, order_id))


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
    
    