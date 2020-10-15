# -*- coding: utf-8 -*-
from rest_framework import serializers

from products.models import Product, ProductImage, Category, Shop
from profiles.models import Profile


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
        fields = ['catalog_image', 'thumb_image', 'id']


class ProductImageThumbSerializer(serializers.ModelSerializer):
    thumb_image = serializers.ReadOnlyField(source='thumb_image.url')

    class Meta:
        model = ProductImage
        fields = ['thumb_image']


class ProductImageCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['original']


class ProductImageIdSerializer(serializers.Serializer):
    image = serializers.PrimaryKeyRelatedField(queryset=ProductImage.objects.all())


class ProductSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.name')
    images = ProductImageSerializer(many=True)

    class Meta:
        model = Product
        exclude = ['created_at', 'modified_at', 'shop', ]


class ProductMiniSerializer(serializers.ModelSerializer):
    images = ProductImageThumbSerializer(many=True)

    class Meta:
        model = Product
        fields = ['images', 'title', 'price', 'active']


class CreateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description', 'category', 'id', 'active']


class UpdateProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['title', 'price', 'description', 'category', 'id', 'active']


class ActivateDeactivateProductSerializer(serializers.Serializer):
    active = serializers.BooleanField()


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ShopSerializer(serializers.ModelSerializer):
    likes_list = serializers.ReadOnlyField()

    class Meta:
        model = Shop
        fields = '__all__'


class ShopWithProductsSerializer(AnnotateFieldsModelSerializer, serializers.ModelSerializer):
    category_products = ProductMiniSerializer(many=True)
    category_images = serializers.ReadOnlyField()
    likes_list = serializers.ReadOnlyField()

    class Meta:
        model = Shop
        exclude = ['created_at', 'modified_at', 'description', 'delivery']


class ShopDetailSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True)
    categories = serializers.ReadOnlyField()
    likes_list = serializers.ReadOnlyField()

    class Meta:
        model = Shop
        fields = '__all__'


class CreateShopSerializer(serializers.Serializer):
    name = serializers.CharField()
    phone = serializers.CharField()
    delivery = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
    profile = serializers.PrimaryKeyRelatedField(queryset=Profile.objects.all())


class UpdateShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'delivery', 'description', 'phone']