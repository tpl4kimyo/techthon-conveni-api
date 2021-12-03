from django.db import models
from django.db.models.fields import TimeField

# Create your models here.

class StockManageModel(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(null=False, max_length=20)
    price = models.IntegerField(null=False, default=0)
    on_sale = models.BooleanField(null=False, default=False)
    count = models.IntegerField(null=False, default=0)

    def __str__(self) -> str:
        return self.id

class PurchaseModel(models.Model):
    id = models.IntegerField(primary_key=True)
    bought_at = models.DateTimeField(null=False)
    staff_name = models.CharField(null=False, max_length=63)

    def __str__(self) -> str:
        return self.id

class PurchaseItemModel(models.Model):
    purchase_id = models.ForeignKey(PurchaseModel,on_delete=models.CASCADE)
    stock_id = models.ForeignKey(StockManageModel,on_delete=models.CASCADE)
    price = models.IntegerField(null=False, default=0)
    bought_count = models.IntegerField(null=False, default=0)

    def __str__(self) -> str:
        return self.id