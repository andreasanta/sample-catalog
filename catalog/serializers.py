from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            'sku',
            'name',
            'qty',
            'price',
            'created_at',
            'updated_at'
        )