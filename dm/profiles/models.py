# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import CoreModel, CoreModelManager
from products.models import Shop


class ProfileQuerySet(models.QuerySet):
    pass


class ProfileManager(CoreModelManager):
    pass


class Profile(CoreModel):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True,
     related_name="profile")
    nickname = models.CharField(max_length=20)
    description = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    shop = models.ForeignKey(Shop, on_delete=models.SET_NULL, null=True, blank=True)

    viber_id = models.CharField(max_length=100, null=True, blank=True)
    viber_name = models.CharField(max_length=100, null=True, blank=True)
    viber_avatar = models.URLField(max_length=300, null=True, blank=True)
    last_seen_at = models.DateTimeField(auto_now_add=True)
    
    active = models.BooleanField(default=True)  

    objects = ProfileManager()

    class Meta:
        ordering = ['pk',]

    def __str__(self):
        return 'Profile {}'.format(self.nickname)