# -*- coding: utf-8 -*-
import tempfile

from django.db import models
from django.db.models import Q, Subquery, OuterRef, Count, Prefetch, F
from django.db.models.functions import Coalesce
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import CoreModel, CoreModelManager
from products.utils import create_resized_image_from_file


class Category(CoreModel):
    CAT_TYPES =  [('dm', 'dm'), ('ds', 'ds')]
    name = models.CharField(max_length=100)
    ru_name = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    category_type = models.CharField(max_length=20, choices=CAT_TYPES)

    class Meta:
        ordering = ['name',]

    def __str__(self):
        return self.ru_name


class ShopQuerySet(models.QuerySet):
    def create_shop(self, name, phone, profile, delivery=None, description=None):
        shop = self.create(name=name, phone=phone, description=description, delivery=delivery)
        profile.shop = shop
        profile.save()

        return shop

    def add_products_count_by_dm_cat(self):
        data = dict()

        for cat in Category.objects.filter(category_type='dm'):
            subquery = Product.objects.filter(shop__pk=OuterRef('pk'), category=cat, active=True) \
                        .values('category') \
                        .annotate(cnt=Count('*')) \
                        .values('cnt')
            data[f'{cat.name}_count'] = Coalesce(Subquery(subquery, 
                output_field=models.IntegerField()), 0)

        return self.annotate(**data)

    def filter_by_cat(self, cat_name):
        return self.filter(**{f"{cat_name}_count__gt": 0}).order_by(f'-{cat_name}_count')

    def add_category_products(self, category_name):
        return self.prefetch_related(
                        Prefetch(
                            'products',
                            queryset=Product.objects.filter(category__name=category_name,
                                                             active=True) \
                                                    .prefetch_related('images'),
                            to_attr='category_products'
                        )
                    )

    def add_last_modified_date_product(self, category_name):
        product_last_activity_subquery = Subquery(
            Product.objects.filter(shop__pk=OuterRef('pk'), active=True, category__name=category_name) \
                .order_by('-modified_at') \
                .values('modified_at')[:1], output_field=models.DateTimeField())
        return self.annotate(last_modified_date_product=product_last_activity_subquery)


class Shop(CoreModel):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    delivery = models.TextField(null=True, blank=True)

    objects = ShopQuerySet.as_manager()

    def __str__(self):
        return self.name

    @property
    def category_images(self):
        images = []
        if not hasattr(self, 'category_products'):
            return images
        
        for product in self.category_products:
            if product.images.all().first():
                images.append(product.images.all().first().catalog_image.url)

        return images[:2]

    @property
    def all_products(self):
        return self.products.get_all().filter(shop=self)

    @property
    def categories(self):
        return self.products.categories_distinct()

    @property
    def likes_list(self):
        return list(self.likes.profile_ids())

    @property
    def feedbacks_list(self):
        return list(self.feedbacks.profile_ids())
            

class ProductQuerySet(models.QuerySet):
    pass


class ProductManager(CoreModelManager):
    def get_queryset(self):
        return ProductQuerySet(self.model, using=self._db) \
            .select_related('category').prefetch_related('images').filter(active=True)

    def get_all(self):
        return ProductQuerySet(self.model, using=self._db) \
            .select_related('category').prefetch_related('images')

    def create_product(self, title, category, shop, price, description=None, image=None):
        product = self.create(title=title, category=category, shop=shop, description=description,
         price=price)

        if image:
            product.images.create_product_image(image_file=image, product=product)

        return product

    def categories_distinct(self):
        cat_ids = self.select_related('category').filter(active=True).values_list('category__pk', flat=True) 
        return Category.objects.filter(pk__in=cat_ids)


class Product(CoreModel):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    price = models.CharField(max_length=100, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='products')
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')

    active = models.BooleanField(default=True)  

    objects = ProductManager()

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
        catalog_image, cat_width, cat_height = create_resized_image_from_file(image_file)

        thumb_image, thumb_width, thumb_height = \
            create_resized_image_from_file(image_file, width=80, height=60)

        product_image = self.create(product=product)
        product_pk = product.pk if product else 0

        product_image.original.save(f'{product.pk}.jpg', image_file)

        catalog_image_name = f'catalog_{product_image.original.name}.jpg'
        product_image.catalog_image.save(catalog_image_name, catalog_image)
        product_image.cat_width = cat_width
        product_image.cat_height = cat_height
        product_image.save()

        thumb_image_name = f'thumb_{product_image.original.name}.jpg'
        product_image.thumb_image.save(thumb_image_name, thumb_image)

        return product_image


class ProductImage(CoreModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images',
         null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='images',
         null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='images',
         null=True, blank=True)
    original = models.FileField(null=True, blank=True)
    catalog_image = models.FileField(null=True, blank=True)
    cat_width = models.IntegerField(null=True, blank=True)
    cat_height = models.IntegerField(null=True, blank=True)

    thumb_image = models.FileField(null=True, blank=True)

    objects = ProductImageManager()

    class Meta:
        ordering = ['pk',]