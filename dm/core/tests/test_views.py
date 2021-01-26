# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from products.models import Shop, Category, Product, ProductImage
from feedbacks.models import Feedback, Like, Suggestion
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


class PermissionsViewSetTest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        product_testing.create_test_dm_products(images_onOff=False)
        product_testing.create_test_shop_test_user1()

        self.profile = Profile.objects.get(user__username='kzr')
        self.admin = User.objects.get(username='kaizerj')
        self.shop = Shop.objects.filter(name='test_shop').first()
        self.owner = self.shop.profiles.all().first().user
        self.category = Category.objects.all().first()

    def test_suggestions_permission(self):
        response = self.client.post(f'/api/suggestions/', {'text': 'test text'})
        self.assertEqual(response.data, 'Created')
        self.assertEqual(response.status_code, 200)

        response = self.client.get(f'/api/suggestions/')
        self.assertEqual(response.status_code, 401)

        self.client.force_authenticate(self.profile.user)
        response = self.client.get(f'/api/suggestions/')
        self.assertEqual(response.status_code, 403)
        self.client.logout()

        self.client.force_authenticate(self.admin)
        response = self.client.get(f'/api/suggestions/')
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        s = Suggestion.objects.all().first()
        self.client.force_authenticate(self.profile.user)
        response = self.client.get(f'/api/suggestions/{s.pk}/')
        self.assertEqual(response.status_code, 403)

        response = self.client.patch(f'/api/suggestions/{s.pk}/')
        self.assertEqual(response.status_code, 403)

        self.client.logout()

    def test_ownerCUD_permission(self):
        # response = self.client.post(f'/api/feedbacks/', {'text': 'test text'})
        # self.assertEqual(response.status_code, 401)

        response = self.client.get(f'/api/feedbacks/')
        self.assertEqual(response.status_code, 200)

        self.client.force_authenticate(self.owner)
        response = self.client.get(f'/api/feedbacks/')
        self.assertEqual(response.status_code, 200)

        response = self.client.post(f'/api/feedbacks/', {'text': 'test text', 
            'shop': self.shop.pk})
        self.assertEqual(response.status_code, 200)

        response = self.client.patch(f'/api/feedbacks/', data={'text': 'test text', 
            'shop': self.shop.pk})
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.client.logout()

        # self.client.force_authenticate(self.profile.user)
        # response = self.client.get(f'/api/feedbacks/')
        # self.assertEqual(response.status_code, 200)

        # response = self.client.post(f'/api/feedbacks/', {'text': 'test text', 
        #     'shop': self.shop.pk})
        # self.assertEqual(response.status_code, 200)

        # response = self.client.patch(f'/api/feedbacks/', {'text': 'test text', 
        #     'shop': self.shop.pk})
        # self.assertNotEqual(response.status_code, 200)
        # self.client.logout()


