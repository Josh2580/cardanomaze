from coin.models import Mining
from rest_framework import serializers


class MiningSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mining
        fields = "__all__"