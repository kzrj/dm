# -*- coding: utf-8 -*-
import tempfile

from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import CoreModel, CoreModelManager
from profiles.models import Profile
from products.utils import create_resized_image_from_file


class CategoryQuerySet(models.QuerySet):
    pass


class CategoryManager(CoreModelManager):
    pass


class Category(CoreModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)

    objects = CategoryManager()

    class Meta:
        ordering = ['pk',]

    def __str__(self):
        return self.title


class ProductQuerySet(models.QuerySet):
    pass


class ProductManager(CoreModelManager):
    pass


class Product(CoreModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)

    active = models.BooleanField(default=True)  

    objects = ProductManager()

    class Meta:
        ordering = ['pk',]

    def __str__(self):
        return 'Product {}'.format(self.title)


class ProductImageQuerySet(models.QuerySet):
    pass


class ProductImageManager(CoreModelManager):
    def get_queryset(self):
        return ProductImageQuerySet(self.model, using=self._db)

    def create_product_image(self, image_file):
        catalog_image = create_resized_image_from_file(image_file, 480)
        return self.create(original=image_file, catalog_image=catalog_image)

    # def create(self, *args, **kwargs):
    #     catalog_image = create_resized_image_from_file(image_file, 480)
    #     kwargs['catalog_image'] = catalog_image
    #     return super(ProductImageManager, self).create(*args, **kwargs)


class ProductImage(CoreModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    original = models.FileField()
    catalog_image = models.FileField(null=True, blank=True)

    objects = ProductImageManager()

    class Meta:
        ordering = ['pk',]

    # def __str__(self):
    #     return 'Product {}'.format(self.title)