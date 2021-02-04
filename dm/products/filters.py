# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django_filters import rest_framework as filters

from products.models import Shop


class ShopFilter(filters.FilterSet):
    category = filters.CharFilter(method='filter_by_category')

    def filter_by_category(self, queryset, name, value):
        return queryset.filter_by_cat(value)

    def filter_by_activity_in_category(self, queryset, name, value):
    	return queryset.add_last_modified_date_product(category_name=value)\
    		.order_by('-last_modified_date_product')

    def filter_random(self, queryset, name, value):
    	return queryset.order_by('?')

    class Meta:
        model = Shop
        fields = '__all__'