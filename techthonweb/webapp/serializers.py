from rest_framework import serializers
from .models import StockManageModel

class StockManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockManageModel
        fields = ['id', 'name', 'price', 'on_sale', 'count']
