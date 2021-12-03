from rest_framework import serializers
from .models import StockManageModel, PurchaseModel, PurchaseItemModel

class StockManageSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockManageModel
        fields = ['id', 'name', 'price', 'on_sale', 'count']

class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseModel
        fields = ['id', 'bought_at', 'staff_name']

class PurchaseItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseItemModel
        fields = ['id', 'purchase_id', 'stock_id', 'price', 'bought_count']
