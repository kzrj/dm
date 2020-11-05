# -*- coding: utf-8 -*-
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from products.models import Shop, Category, Product, ProductImage
from feedbacks.models import Feedback, Like
from profiles.models import Profile
import products.testing_utils as product_testing
from products.serializers import ShopDetailSerializer


class CoreViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        product_testing.create_test_dm_products(images_onOff=False)
        self.profile = Profile.objects.get(user__username='kzr')
        self.shop = Shop.objects.all().first()
        self.category = Category.objects.all().first()
        
    def test_index_category(self):
        # response = self.client.get(f'/shops/{self.shop.pk}/products/polufabrikati/')
        response = self.client.get(f'/category/{self.category.name}/')
        self.assertEqual(response.context['og_title'], self.category.ru_name)
        self.assertEqual(response.context['og_description'], self.category.description)

    def test_index_shop(self):
        response = self.client.get(f'/shops/{self.shop.pk}/products/{self.category.name}/')
        self.assertEqual(response.context['og_title'], self.shop.name)
        self.assertEqual(response.context['og_description'], self.shop.description)