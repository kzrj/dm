# -*- coding: utf-8 -*-
from django.test import TransactionTestCase, tag

from products.models import Shop, Category, Product, ProductImage
from profiles.models import Profile
from feedbacks.models import Feedback, Like

import products.testing_utils as product_testing
from products.utils import create_resized_image_from_file
from products.serializers import ShopDetailSerializer, ShopWithProductsSerializer


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

    # @tag('with_file')
    # def test_create_shop_with_product(self):
    #     category = Category.objects.all().first()
    #     image = open('../data/polufabrikati.jpg', 'rb')

    #     data = {
    #         'shop_name': 'Test shop',
    #         'shop_phone': '79148569874',
    #         'shop_add_info': None,
    #         'shop_delivery': None,

    #         'product_name': 'test product',
    #         'product_category': category,
    #         'product_price': '100 za shtuku',
    #         'product_add_info': None,
    #         'product_image': image
    #     }

    #     shop = Shop.objects.create_shop_with_product(**data)
    #     self.assertEqual(shop.name, data['shop_name'])
    #     self.assertEqual(shop.phones.all().first().phone, data['shop_phone'])

    #     product = shop.products.all().first()
    #     self.assertEqual(product.title, data['product_name'])
    #     self.assertEqual(product.category, data['product_category'])
    #     self.assertEqual(product.price, data['product_price'])

    #     image = product.images.all().first()
    #     self.assertEqual(image.catalog_image.name, f'catalog_{product.pk}.jpg')

    def test_create_shop(self):
        profile = Profile.objects.get(user__username='kzr')
        shop = Shop.objects.create_shop(name='test shop', phone='123', profile=profile,
            delivery='delivery', description='description')
        self.assertEqual(shop.name, 'test shop')
        self.assertEqual(shop.description, 'description')
        self.assertEqual(shop.phone, '123')

        profile.refresh_from_db()
        self.assertEqual(profile.shop, shop)

    def test_add_last_modified_date_product(self):
        category1 = Category.objects.get(name='myaso')
        category2 = Category.objects.get(name='napitki')

        profile1 = Profile.objects.get(user__username='kzr')
        shop1 = Shop.objects.create_shop(name='test shop', phone='123', profile=profile1,
            delivery='delivery', description='description')

        profile2 = Profile.objects.get(user__username='test_user1')
        shop2 = Shop.objects.create_shop(name='test shop 2', phone='123', profile=profile2,
            delivery='delivery', description='description')

        product11 = Product.objects.create_product(title='test product1 shop1', category=category1,
             price='1', shop=shop1)
        product12 = Product.objects.create_product(title='test product2 shop1', category=category2,
             price='1', shop=shop1)
        product21 = Product.objects.create_product(title='test product1 shop2', category=category1,
             price='1', shop=shop2)
        product22 = Product.objects.create_product(title='test product2 shop2', category=category2,
             price='1', shop=shop2)

        self.assertEqual(Shop.objects.all().add_last_modified_date_product() \
                .order_by('-last_modified_date_product').first(), shop2)

        # for shop in Shop.objects.all().add_last_modified_date_product().order_by('-last_modified_date_product'):
        #     print(shop, shop.modified_at, shop.last_modified_date_product)


class ImageCreationTest(TransactionTestCase):
    @tag('with_file')
    def test_create_resized_image_from_file(self):
        with open('../data/polufabrikati.jpg', 'rb') as file:
            pimage = ProductImage.objects.create_product_image(image_file=file)


class SerializersTest(TransactionTestCase):
    def setUp(self):
        product_testing.create_test_dm_products(images_onOff=False)
        self.profile = Profile.objects.get(user__username='kzr')
        self.shop = Shop.objects.all().first()

    def test_shop_detail_serializer(self):
        like = Like.objects.set_like_unlike(profile=self.profile, shop=self.shop)

        with self.assertNumQueries(4):
            bool(ShopDetailSerializer(self.shop).data)

    # def test_shop_with_product_serializer(self):
    #     like = Like.objects.set_like_unlike(profile=self.profile, shop=self.shop)

    #     with self.assertNumQueries(4):
    #         bool(ShopWithProductsSerializer(self.shop).data)
