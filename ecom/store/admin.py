from django.contrib import admin
from .models import Catalog, Product, CatalogCategory, ProductDetail, ProductAttribute, Cart, Order, OrderItem, Customer

# Register your models here.
admin.site.register(Catalog)
admin.site.register(Product)
admin.site.register(CatalogCategory)
admin.site.register(ProductDetail)
admin.site.register(ProductAttribute)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Customer)