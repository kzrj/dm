# # -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from django.views.decorators.csrf import csrf_exempt

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages import (
        TextMessage,
        ContactMessage,
        PictureMessage,
        VideoMessage
    )
from viberbot.api.messages.data_types.contact import Contact

from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest

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


viber = Api(BotConfiguration(
    name='dm-eda',
    avatar='http://site.com/avatar.jpg',
    auth_token='4ba8b47627e7dd45-896232bcd5f44988-d6eba79009c0e27'
))

@csrf_exempt
def viber_view(request):
    viber_request = viber.parse_request(request.body)

    if not viber.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    if isinstance(viber_request, ViberMessageRequest):
        text_message = TextMessage(text="Лариса :)")
        message = viber_request.message
        
        viber.send_messages(viber_request.sender.id, [
            text_message, 
        ])

    elif isinstance(viber_request, ViberSubscribedRequest):
        viber.send_messages(viber_request.get_user.id, [
            TextMessage(text="thanks for subscribing!")
        ])

    return Response(status=200)