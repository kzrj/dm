# # -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from products.serializers import ProductSerializer, CategorySerializer, \
    ShopSerializer, ShopWithProductsSerializer, ShopDetailSerializer
from products.models import Product, Category, Shop

from products.testing_utils import create_test_dm_products

from products.filters import ShopFilter


class CoreViewSet(viewsets.ModelViewSet):
    def create(self, request):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass


class CategoryViewSet(CoreViewSet, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ShopViewSet(CoreViewSet, viewsets.ModelViewSet):
    queryset = Shop.objects.all() \
        .add_products_count_by_dm_cat()
    serializer_class = ShopSerializer
    filter_class = ShopFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ShopDetailSerializer
        return ShopSerializer

    def list(self, request):
        category_name = request.GET.get('category', None)

        if category_name:
            queryset = self.filter_queryset(
                self.queryset.add_category_products(category_name=category_name))
            serializer = ShopWithProductsSerializer(queryset, many=True)

            page = self.paginate_queryset(queryset)
            if page is not None:
                serializer = ShopWithProductsSerializer(queryset, many=True)
                return self.get_paginated_response(serializer.data)

        return super().list(request)


class InitTestDataView(APIView):
    def get(self, request, format=None):
        create_test_dm_products()
        return Response({'msg': 'Done.'})


    