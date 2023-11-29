from rest_framework import serializers
from .models import Product, StockProduct, Stock


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description']


class ProductPositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockProduct
        fields = ['product', 'price', 'quantity']


class StockSerializer(serializers.ModelSerializer):
    positions = ProductPositionSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['id', 'address', 'products', 'positions']

    def create(self, validated_data):
        positions = validated_data.pop('positions')
        new_stock = super().create(validated_data)

        for product in positions:
            stock_product = StockProduct(
                stock = new_stock,
                product = product.get('product'),
                quantity = product.get('quantity'),
                price = product.get('price')
            )
            stock_product.save()

        return new_stock


    def update(self, instance, validated_data):
        positions = validated_data.pop('positions')
        stock = super().update(instance, validated_data)

        for product in positions:
            obj, created = StockProduct.objects.update_or_create(
                stock = stock,
                product = product.get('product'),
                defaults = {'price': product.get('price'), 
                'quantity': product.get('quantity')}
            )


        return stock
