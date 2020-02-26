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


class ProductAdQuerySet(models.QuerySet):
    pass


class ProductAdManager(CoreModelManager):
    pass


class ProductAd(CoreModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True)
    price = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)

    active = models.BooleanField(default=True)  

    objects = ProductAdManager()

    class Meta:
        ordering = ['pk',]

    def __str__(self):
        return 'ProductAd {}'.format(self.title)


class Product(CoreModel):
    product_ad = models.ForeignKey(ProductAd, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=20)
    price = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name} - {self.price}'


class ProductAdImageQuerySet(models.QuerySet):
    pass


class ProductAdImageManager(CoreModelManager):
    def get_queryset(self):
        return ProductAdImageQuerySet(self.model, using=self._db)

    def create_product_image(self, image_file):
        catalog_image = create_resized_image_from_file(image_file, 480)
        return self.create(original=image_file, catalog_image=catalog_image)

    # def create(self, *args, **kwargs):
    #     catalog_image = create_resized_image_from_file(image_file, 480)
    #     kwargs['catalog_image'] = catalog_image
    #     return super(ProductImageManager, self).create(*args, **kwargs)


class ProductAdImage(CoreModel):
    product = models.ForeignKey(ProductAd, on_delete=models.CASCADE, related_name='images')
    original = models.FileField()
    catalog_image = models.FileField(null=True, blank=True)

    objects = ProductAdImageManager()

    class Meta:
        ordering = ['pk',]