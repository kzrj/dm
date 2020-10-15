# -*- coding: utf-8 -*-
from django.test import TransactionTestCase, tag
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from products.models import Shop, Category, Product, ProductImage
from profiles.models import Profile
from feedbacks.models import Feedback, Like

import products.testing_utils as product_testing
from products.utils import create_resized_image_from_file


class FeedbackAndLikesTest(TransactionTestCase):
    def setUp(self):
        product_testing.create_test_dm_products(images_onOff=False)
        self.profile = Profile.objects.get(user__username='kzr')
        self.shop = Shop.objects.all().first()

    def test_create_feedback_constraints(self):
        feedback = Feedback.objects.create_feedback(
            profile=self.profile, shop=self.shop, text='Test feedback')
        
        with self.assertRaises(Exception):
            feedback2 = Feedback.objects.create_feedback(
                profile=self.profile, shop=self.shop, text='Test2 feedback')

        feedback3 = Feedback.objects.create_feedback(
            profile=self.profile, rel_feedback=feedback, text='Test3 feedback')
        feedback4 = Feedback.objects.create_feedback(
            profile=self.profile, rel_feedback=feedback, text='Test3 feedback')

    def test_create_likes_constraints(self):
        feedback = Feedback.objects.create_feedback(
            profile=self.profile, shop=self.shop, text='Test feedback')

        like1 = Like.objects.create_like(profile=self.profile, shop=self.shop)
        
        with self.assertRaises(Exception):
            like2 = Like.objects.create_like(profile=self.profile, shop=shop)

        like3 = Like.objects.create_like(profile=self.profile, feedback=feedback)

        with self.assertRaises(Exception):
            like4 = Like.objects.create_like(profile=self.profile, feedback=feedback)

    def test_set_like_unlike(self):
        like = Like.objects.set_like_unlike(profile=self.profile, shop=self.shop)
        self.assertEqual(like.like, True)

        like = Like.objects.set_like_unlike(profile=self.profile, shop=self.shop)
        self.assertEqual(like.like, False)
        self.assertEqual(Like.objects.all().count(), 1)

        like = Like.objects.set_like_unlike(profile=self.profile, shop=self.shop)
        self.assertEqual(like.like, True)
        self.assertEqual(Like.objects.all().count(), 1)

    def test_profile_ids(self):
        like = Like.objects.set_like_unlike(profile=self.profile, shop=self.shop)
        profile_ids = Like.objects.profile_ids()
        self.assertEqual(profile_ids[0], self.profile.pk)