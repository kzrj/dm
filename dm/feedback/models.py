# -*- coding: utf-8 -*-
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import CoreModel, CoreModelManager
from profiles.models import Profile
from products.models import Product


class FeedbackManager(CoreModelManager):
    pass


class Feedback(CoreModel):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="feedbacks")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="feedbacks")
    text = models.TextField()

    active = models.BooleanField(default=True)  

    objects = FeedbackManager()

    class Meta:
        ordering = ['pk',]

    def __str__(self):
        return 'Feedback {}'.format(self.pk)