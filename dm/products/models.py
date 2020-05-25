# -*- coding: utf-8 -*-
import tempfile

from django.db import models
from django.db.models import Q, Subquery, OuterRef, Count
from django.db.models.functions import Coalesce
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import CoreModel, CoreModelManager
from products.utils import create_resized_image_from_file


class Category(CoreModel):
    CAT_TYPES =  [('dm', 'dm'), ('ds', 'ds')]
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    category_type = models.CharField(max_length=20, choices=CAT_TYPES)

    class Meta:
        ordering = ['pk',]

    def __str__(self):
        return self.name


class ShopQuerySet(models.QuerySet):
    def add_products_count_by_dm_cat(self):
        data = dict()

        for cat in Category.objects.filter(category_type='dm'):
            subquery = Product.objects.filter(shop__pk=OuterRef('pk'), category=cat) \
                        .values('category') \
                        .annotate(cnt=Count('*')) \
                        .values('cnt')
            data[f'{cat.name}_count'] = Coalesce(Subquery(subquery, 
                output_field=models.IntegerField()), 0)

        return self.annotate(**data)

    def filter_by_cat(self, cat_name):
        return self.filter(**{f"{cat_name}_count__gt": 0}).order_by(f'-{cat_name}_count')


class Shop(CoreModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(null=True)
    delivery = models.CharField(max_length=100, null=True, blank=True)

    objects = ShopQuerySet.as_manager()

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    pass


class Product(CoreModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)

    active = models.BooleanField(default=True)  

    objects = ProductQuerySet.as_manager()

    class Meta:
        ordering = ['pk',]

    def __str__(self):
        return f'{self.title} - {self.price}'


class ProductImageQuerySet(models.QuerySet):
    pass


class ProductImageManager(CoreModelManager):
    def get_queryset(self):
        return ProductImageQuerySet(self.model, using=self._db)

    def create_product_image(self, image_file, product=None):
        product_image = self.create(product=product)
        name = image_file.name.split('/')[-1]

        product_image.original.save('test.jpg', image_file)

        catalog_image_name = f'catalog_{product_image.original.name}'
        catalog_image = create_resized_image_from_file(image_file, 480)
        product_image.catalog_image.save(catalog_image_name, catalog_image)

        thumb_image_name = f'thumb_{product_image.original.name}'
        thumb_image = create_resized_image_from_file(image_file, 48)
        product_image.thumb_image.save(thumb_image_name, thumb_image)

        return product_image


class ProductImage(CoreModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images',
    	 null=True, blank=True)
    original = models.FileField(null=True, blank=True)
    catalog_image = models.FileField(null=True, blank=True)
    thumb_image = models.FileField(null=True, blank=True)

    objects = ProductImageManager()

    class Meta:
        ordering = ['pk',]