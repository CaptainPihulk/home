from django.contrib import admin
from .models import Product, Stock, StockProduct


@admin.register (Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register (Stock)
class StockAdmin(admin.ModelAdmin):
    pass

@admin.register (StockProduct)
class StockProductAdmin(admin.ModelAdmin):
    pass