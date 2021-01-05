from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal

class Product(models.Model):

    # Define product properties

    sku = models.CharField(max_length=128, primary_key=True, null=False)
    name = models.CharField(max_length=255, null=False)
    qty = models.PositiveIntegerField(null=False, default=0)
    price = models.FloatField(null=False, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



    def __str__(self):
        return self.name

    
    class Meta:
        app_label = 'catalog'