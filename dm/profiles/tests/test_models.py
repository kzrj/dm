# -*- coding: utf-8 -*-
from django.test import TransactionTestCase
from django.contrib.auth.models import User

from profiles.models import Profile


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
