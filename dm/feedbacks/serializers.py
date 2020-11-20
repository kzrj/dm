# -*- coding: utf-8 -*-
from rest_framework import serializers

from feedbacks.models import Feedback


class FeedbackSerializer(serializers.ModelSerializer):
    nickname = serializers.StringRelatedField(source='profile')

    class Meta:
        model = Feedback
        fields = '__all__'


class FeedbackEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['shop', 'rel_feedback', 'text']