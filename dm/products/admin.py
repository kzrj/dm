from django.contrib import admin

from products.models import Product, Category, ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Product._meta.fields]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Category._meta.fields]


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ProductImage._meta.fields]
