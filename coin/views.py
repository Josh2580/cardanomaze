from django.shortcuts import render
from rest_framework import permissions, viewsets
from coin.models import Mining
from coin.serializers import MiningSerializer
# Create your views here.


class MiningViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Mining.objects.all()
    serializer_class = MiningSerializer
    # permission_classes = [permissions.AllowAny]