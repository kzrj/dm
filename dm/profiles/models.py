# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models import Q
from django.core.exceptions import ValidationError as DjangoValidationError

from core.models import CoreModel, CoreModelManager


class ProfileQuerySet(models.QuerySet):
    pass


class ProfileManager(CoreModelManager):
    @staticmethod
    def gen_username():
        last_user = User.objects.all().order_by('-pk').first()
        unique = False
        username = ''

        if last_user:
            _id = 1
            while not unique:
                username = f'user_{(last_user.pk + _id)}'
                user = User.objects.filter(username=username).first()
                if user:
                    _id += 1
                else:
                    unique = True
        else:
            username = 'user_1'

        return username

    def get_or_create_profile_viber(self, viber_id, viber_name, viber_avatar=None):
        profile = self.filter(viber_id=viber_id).first()
        if profile:
            return profile

        user = User.objects.create_user(username=self.gen_username())
        return self.create(user=user, nickname=viber_name, viber_id=viber_id, viber_name=viber_name,
            viber_avatar=viber_avatar)


class Profile(CoreModel):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True,
     related_name="profile")
    nickname = models.CharField(max_length=20, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    shop = models.ForeignKey('products.Shop', on_delete=models.SET_NULL, null=True,
         blank=True, related_name='profiles')

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
