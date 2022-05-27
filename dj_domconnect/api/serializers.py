from rest_framework import serializers
from .models import PVResult


class PVResultSerializer(serializers.ModelSerializer):

    class Meta:
        model = PVResult
        fields = '__all__'
