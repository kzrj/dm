# -*- coding: utf-8 -*-
from rest_framework import serializers

from profiles.models import Profile, Contact


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'nickname', 'viber_name', 'viber_avatar', 'shop']


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ['id', 'phone', 'shop']