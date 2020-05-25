# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_filters import rest_framework as filters

from products.models import Shop


class ShopFilter(filters.FilterSet):
    category = filters.CharFilter(method='filter_by_category')

    def filter_by_category(self, queryset, name, value):
        return queryset.filter_by_cat(value)

    class Meta:
        model = Shop
        fields = '__all__'