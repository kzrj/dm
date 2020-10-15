# -*- coding: utf-8 -*-

from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from products.models import Shop, Category, Product, ProductImage
from feedbacks.models import Feedback, Like
import products.testing_utils as product_testing
from products.serializers import ShopDetailSerializer


class ShopViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        product_testing.create_test_dm_products(images_onOff=False)
        self.profile = Profile.objects.get(user__username='kzr')
        self.shop = Shop.objects.all().first()
        
    def test_shop_list_with_category_products(self):
        response = self.client.get('/api/shops/?category=polufabrikati')
        self.assertNotEqual(response.data['results'][0].get('category_products', False), False)

        response = self.client.get('/api/shops/')
        self.assertEqual(response.data['results'][0].get('category_products', False), False)