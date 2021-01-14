# -*- coding: utf-8 -*-
from rest_framework import serializers

from profiles.models import Profile, SocialLink


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'nickname', 'viber_name', 'viber_avatar', 'shop']


class SocialLinkReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['link_type', 'link']