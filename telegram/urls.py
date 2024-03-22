from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TelegramUserViewSet, telegram_update, OrderViewSet
from rest_framework_nested import routers


# router = DefaultRouter()
# router.register(r'', TelegramUserViewSet)

# Create a router and register our viewsets with it.
router = routers.DefaultRouter()
router.register(r'all', TelegramUserViewSet,
                basename='telegram_users')

user_router = routers.NestedDefaultRouter(router, "all", lookup='users')
user_router.register('order', OrderViewSet,
                      basename="order_items")


urlpatterns = [
    path('', include(router.urls)),
    path('', include(user_router.urls)),
    path('webhook/', telegram_update, name='telegram_webhook'),
]