# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_filters import rest_framework as filters

from feedbacks.models import Feedback


class FeedbackFilter(filters.FilterSet):
    class Meta:
        model = Feedback
        fields = '__all__'