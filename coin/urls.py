from django.urls import include, path
from rest_framework import routers
from coin import views


router = routers.DefaultRouter()
router.register(r'', views.MiningViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # path('api-auth/', include('rest_framework.urls', namespace='cardanomaze_auth_url'))
]
