# -*- coding: utf-8 -*-
from django.test import TransactionTestCase, tag

from products.models import Shop, Category, Product, ProductImage

import products.testing_utils as product_testing
from products.utils import create_resized_image_from_file
from products.serializers import ShopDetailSerializer


class ShopTest(TransactionTestCase):
    def setUp(self):
        product_testing.create_test_dm_products(images_onOff=False)

    def test_create_test_dm_products(self):
        self.assertEqual(Product.objects.all().count() > 0, True)


    def test_add_products_count_by_dm_cat(self):
        shop = Shop.objects.all().add_products_count_by_dm_cat().first()

        shop_polufabrikati_count = Product.objects.filter(shop=shop,
         category__name='polufabrikati').count()

        shop_myaso_count = Product.objects.filter(shop=shop,
         category__name='myaso').count()

        self.assertEqual(shop.polufabrikati_count, shop_polufabrikati_count)
        self.assertEqual(shop.myaso_count, shop_myaso_count)

    def test_shop_filter_by_cat(self):
        shops = Product.objects.filter(category__name='polufabrikati') \
            .values_list('shop', flat=True)
        shops = Shop.objects.filter(pk__in=list(set(shops)))

        polufabrikati_shops = Shop.objects.all().add_products_count_by_dm_cat() \
            .filter_by_cat('polufabrikati')

        self.assertEqual(set(shops.values_list('pk', flat=True)), 
            set(polufabrikati_shops.values_list('pk', flat=True)))

        self.assertEqual(polufabrikati_shops[0].polufabrikati_count >= \
            polufabrikati_shops[1].polufabrikati_count, True)

    def test_add_category_products(self):
        with self.assertNumQueries(3):
            shops = Shop.objects.filter().add_category_products(category_name='polufabrikati')
            bool(shops)
            self.assertEqual(hasattr(shops[0], 'category_products'), True)

    @tag('with_file')
    def test_create_shop_with_product(self):
        category = Category.objects.all().first()
        image = open('../data/polufabrikati.jpg', 'rb')

        data = {
            'shop_name': 'Test shop',
            'shop_phone': '79148569874',
            'shop_add_info': None,
            'shop_delivery': None,

            'product_name': 'test product',
            'product_category': category,
            'product_price': '100 za shtuku',
            'product_add_info': None,
            'product_image': image
        }

        shop = Shop.objects.create_shop_with_product(**data)
        self.assertEqual(shop.name, data['shop_name'])
        self.assertEqual(shop.phones.all().first().phone, data['shop_phone'])

        product = shop.products.all().first()
        self.assertEqual(product.title, data['product_name'])
        self.assertEqual(product.category, data['product_category'])
        self.assertEqual(product.price, data['product_price'])

        image = product.images.all().first()
        self.assertEqual(image.catalog_image.name, f'catalog_{product.pk}.jpg')


class ImageCreationTest(TransactionTestCase):
    @tag('with_file')
    def test_create_resized_image_from_file(self):
        with open('../data/polufabrikati.jpg', 'rb') as file:
            pimage = ProductImage.objects.create_product_image(image_file=file)


class SerializersTest(TransactionTestCase):
    def setUp(self):
        product_testing.create_test_dm_products(images_onOff=False)

    def test_shop_detail_serializer(self):
        # print()
        with self.assertNumQueries(4):
            shop = Shop.objects.all().first()
            bool(ShopDetailSerializer(shop).data)