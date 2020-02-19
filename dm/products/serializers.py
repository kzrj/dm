# -*- coding: utf-8 -*-
from rest_framework import serializers

from products.models import Product, ProductImage, Category


class ProductImageSerializer(serializers.ModelSerializer):
    original = serializers.SerializerMethodField()

    def get_original(self, image):
        return f'http://192.168.1.4{image.original.url}'

    class Meta:
        model = ProductImage
        fields = ['original', 'catalog_image']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'