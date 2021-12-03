from django.db import models

# Create your models here.

class StockManageModel(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(null=False, max_length=20)
    price = models.IntegerField(null=False, default=0)
    on_sale = models.BooleanField(null=False, default=False)
    count = models.IntegerField(null=False, default=0)

    def __str__(self) -> str:
        return self.id
    
    def init_data(self):
        self.objects.all().delete()
        self.id = 0
        self.name = 'pen'
        self.price = 100
        self.on_sale = True
        self.count = 100
