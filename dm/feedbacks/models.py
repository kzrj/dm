# -*- coding: utf-8 -*-
from django.db import models

from core.models import CoreModel, CoreModelManager
from profiles.models import Profile
from products.models import Shop, Product


class FeedbackManager(CoreModelManager):
    def create_feedback(self, profile, text, shop=None, rel_feedback=None):
        return self.create(profile=profile, text=text, shop=shop, rel_feedback=rel_feedback)

    def profile_ids(self):
        return self.filter(like=True).values_list('profile__pk', flat=True)


class Feedback(CoreModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="feedbacks")
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="feedbacks",
        null=True, blank=True)
    text = models.TextField()

    rel_feedback = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
        related_name='related_feedback')

    active = models.BooleanField(default=True)

    objects = FeedbackManager()

    class Meta:
        ordering = ['pk',]
        constraints = [
            models.UniqueConstraint(fields=['profile', 'shop'],
                name='unique_feedback_to_shop'),
        ]

    def __str__(self):
        return 'Feedback {}'.format(self.pk)


class LikeManager(CoreModelManager):
    def create_like(self, profile, like=True, shop=None, feedback=None):
        return self.create(profile=profile, like=like, shop=shop, feedback=feedback)

    def set_like_unlike(self, profile, shop=None, feedback=None):
        like = self.filter(profile=profile, shop=shop, feedback=feedback).first()
        if like:
            like.like = not like.like
            like.save()
            return like
        else:
            return self.create_like(profile=profile, shop=shop, feedback=feedback, like=True)

    def profile_ids(self):
        return self.filter(like=True).values_list('profile__pk', flat=True)


class Like(CoreModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="likes")
    feedback = models.ForeignKey(Feedback, on_delete=models.CASCADE, related_name="likes",
        null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name="likes",
        null=True, blank=True)

    like = models.BooleanField(null=True)

    objects = LikeManager()

    class Meta:
        ordering = ['pk',]
        constraints = [
            models.UniqueConstraint(fields=['profile', 'shop'],
                name='unique_like_to_shop'),
            models.UniqueConstraint(fields=['profile', 'feedback'],
                name='unique_like_to_feedback'),
        ]

    def __str__(self):
        return 'Like {}'.format(self.pk)