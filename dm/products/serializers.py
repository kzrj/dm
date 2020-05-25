# -*- coding: utf-8 -*-
from rest_framework import serializers

from products.models import Product, ProductImage, Category, Shop



class AnnotateFieldsModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer that takes an additional `fields` argument that
    controls which fields should be displayed.
    """

    def __init__(self, *args, **kwargs):
        # Instantiate the superclass normally
        super(AnnotateFieldsModelSerializer, self).__init__(*args, **kwargs)

        if len(args) > 0 and len(args[0]) > 0:
            for field_name in args[0][0].__dict__.keys():
                if field_name[0] == '_' or field_name in self.fields.keys():
                    continue
                self.fields[field_name] = serializers.ReadOnlyField()



class ProductImageSerializer(serializers.ModelSerializer):
    catalog_image = serializers.ReadOnlyField(source='catalog_image.url')
    thumb_image = serializers.ReadOnlyField(source='thumb_image.url')

    class Meta:
        model = ProductImage
        fields = ['catalog_image', 'thumb_image']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ShopSerializer(AnnotateFieldsModelSerializer, serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = '__all__'