from django.contrib import admin

from products.models import ProductAd, Category, ProductAdImage, Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Product._meta.fields]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Category._meta.fields]


@admin.register(ProductAdImage)
class ProductAdImageAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ProductAdImage._meta.fields]


@admin.register(ProductAd)
class ProductAdAdmin(admin.ModelAdmin):
    list_display = [f.name for f in ProductAd._meta.fields]
