# -*- coding: utf-8 -*-
from rest_framework import serializers

from products.models import ProductAd, ProductAdImage, Category, Product


class ProductAdImageSerializer(serializers.ModelSerializer):
    original = serializers.SerializerMethodField()

    def get_original(self, image):
        return f'{image.original.url}'

    class Meta:
        model = ProductAdImage
        fields = ['original', 'catalog_image']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['name', 'price']


class ProductAdSerializer(serializers.ModelSerializer):
    images = ProductAdImageSerializer(many=True)
    products = ProductSerializer(many=True)

    class Meta:
        model = ProductAd
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'