# -*- coding: utf-8 -*-
from django.test import TransactionTestCase
from django.contrib.auth.models import User

from profiles.models import Profile, SocialLink
import products.testing_utils as product_testing


class ProfileTest(TransactionTestCase):
    def test_gen_username(self):
        username = Profile.objects.gen_username()
        self.assertEqual(username, 'user_1')
        User.objects.create_user(username=username)

        # username = Profile.objects.gen_username()
        # self.assertEqual(username, 'user_2')
        # User.objects.create_user(username=username)

    def test_gen_username2(self):
        username = Profile.objects.gen_username()
        self.assertEqual(username, 'user_1')
        User.objects.create_user(username=username)

    def test_create_profile(self):
        profile = Profile.objects.create_profile(
            viber_id=123,
            viber_name='Test_user',
            )

        self.assertEqual(profile.user.username, 'user_1')


class SocialLinkCUDTest(TransactionTestCase):
    def setUp(self):
        self.shop = product_testing.create_test_shop_test_user1()
        socials_list = [
            {'link_type': 'vk', 'link': 'http://vk.com/papdsp'},
            {'link_type': 'instagram', 'link': 'http://instagram.com/papdsp'},
        ]
        self.shop.socials.create_or_update_for_shop(socials=socials_list, shop=self.shop)

    def test_create(self):
        self.assertEqual(SocialLink.objects.all().count(), 2)
        self.assertEqual(SocialLink.objects.all().first().link_type, 'vk')

    def test_update(self):
        socials_list = [
            {'link_type': 'vk', 'link': 'http://vk.com/papdsp2'},
            {'link_type': 'instagram', 'link': 'http://instagram.com/papdsp'},
        ]
        self.shop.socials.create_or_update_for_shop(socials=socials_list, shop=self.shop)

        self.assertEqual(SocialLink.objects.all().count(), 2)
        self.assertEqual(SocialLink.objects.all().first().link, 'http://vk.com/papdsp2')

    def test_add_new(self):
        socials_list = [
            {'link_type': 'vk', 'link': 'http://vk.com/papdsp2'},
            {'link_type': 'instagram', 'link': 'http://instagram.com/papdsp'},
            {'link_type': 'web', 'link': 'http://example.com/papdsp'},
        ]
        self.shop.socials.create_or_update_for_shop(socials=socials_list, shop=self.shop)

        self.assertEqual(SocialLink.objects.all().count(), 3)
        self.assertEqual(SocialLink.objects.all().filter(link_type='web').first().link,
             'http://example.com/papdsp')

    def test_delete_for_shop(self):
        self.assertEqual(SocialLink.objects.all().count(), 2)
        socials_list = [
            {'link_type': 'vk', 'link': 'http://vk.com/papdsp2'},
        ]

        self.shop.socials.delete_for_shop(socials=socials_list, shop=self.shop)
        self.assertEqual(self.shop.socials.all().count(), 1)
        self.assertEqual(self.shop.socials.all().first().link_type, 'vk')

    def test_create_update_delete_for_shop(self):
        # delete
        self.assertEqual(SocialLink.objects.all().count(), 2)
        socials_list = [
            {'link_type': 'vk', 'link': 'http://vk.com/papdsp'},
        ]
        self.shop.socials.create_update_delete_for_shop(socials=socials_list, shop=self.shop)
        self.assertEqual(self.shop.socials.all().count(), 1)
        self.assertEqual(self.shop.socials.all().first().link_type, 'vk')

        # add
        socials_list = [
            {'link_type': 'vk', 'link': 'http://vk.com/papdsp'},
            {'link_type': 'web', 'link': 'http://example.com/papdsp'},
        ]
        self.shop.socials.create_update_delete_for_shop(socials=socials_list, shop=self.shop)
        self.assertEqual(self.shop.socials.all().count(), 2)
        self.assertEqual(self.shop.socials.all().filter(link_type='vk').first().link,
             'http://vk.com/papdsp')
        self.assertEqual(self.shop.socials.all().filter(link_type='web').first().link, 
            'http://example.com/papdsp')

        # update
        socials_list = [
            {'link_type': 'vk', 'link': 'http://vk.com/papdsp2'},
            {'link_type': 'web', 'link': 'http://example.com/papdsp'},
        ]
        self.shop.socials.create_update_delete_for_shop(socials=socials_list, shop=self.shop)
        self.assertEqual(self.shop.socials.all().count(), 2)
        self.assertEqual(self.shop.socials.all().filter(link_type='vk').first().link_type, 'vk')
        self.assertEqual(self.shop.socials.all().filter(link_type='vk').first().link,
             'http://vk.com/papdsp2')
        

