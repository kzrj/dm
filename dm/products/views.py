# # -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages import (
        TextMessage,
        ContactMessage,
        PictureMessage,
        VideoMessage,
        URLMessage,
        KeyboardMessage
    )
from viberbot.api.messages.data_types.contact import Contact

from viberbot.api.viber_requests import (
    ViberConversationStartedRequest,
    ViberFailedRequest,
    ViberMessageRequest,
    ViberSubscribedRequest,
    ViberUnsubscribedRequest,
    ViberDeliveredRequest,
    ViberSeenRequest
    )

from products.serializers import ProductSerializer, CategorySerializer, \
    ShopSerializer, ShopWithProductsSerializer, ShopDetailSerializer, CreateShopAndProductSerializer
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

    @action(methods=['post'], detail=False)
    def create_shop_and_product(self, request):
        serializer = CreateShopAndProductSerializer(data=request.data)
        if serializer.is_valid():
            shop = Shop.objects.create_shop_with_product(**serializer.validated_data)
            return Response(
                {
                    "message": "Created"
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InitTestDataView(APIView):
    def get(self, request, format=None):
        create_test_dm_products()
        return Response({'msg': 'Done.'})


viber = Api(BotConfiguration(
    name='dm-eda',
    avatar='http://site.com/avatar.jpg',
    auth_token='4ba8b47627e7dd45-896232bcd5f44988-d6eba79009c0e27'
))


def login_keyboard(viber_id=None):
    # get or create user with profile.viber_id = viber_id
    # gen token
    token = 'token'
    return {
            "Type": "keyboard",
            "Buttons": [
               {
                    "Columns": 1,
                    "Rows": 2,
                    "Text": "<br><font color=#494E67><b>Открыть сайт</b></font>",
                    "TextSize": "regular",
                    "TextHAlign": "center",
                    "TextVAlign": "middle",
                    "ActionType": "open-url",
                    "ActionBody": f"https://svoyaeda.su/dm/login/v/{token}",
                    "OpenURLType": "internal",
                    "BgColor": "#f7bb3f",
                    "Image": "https://s18.postimg.org/9tncn0r85/sushi.png"
                },
                {
                    "Columns": 1,
                    "Rows": 2,
                    "BgColor": "#e6f5ff",
                    "BgMedia": "http://link.to.button.image",
                    "BgMediaType": "picture",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "MASS_MESSAGES",
                    "ReplyType": "message",
                    "Text": "Много месаг"
                },
                {
                    "Columns": 1,
                    "Rows": 2,
                    "BgColor": "#e6f5ff",
                    "BgMedia": "http://link.to.button.image",
                    "BgMediaType": "picture",
                    "BgLoop": True,
                    "ActionType": "reply",
                    "ActionBody": "MASS_MESSAGES2",
                    "ReplyType": "message",
                    "Text": "XZ"
                },
            ],
            "InputFieldState": 'regular'
        }

@csrf_exempt
def viber_view(request):
    try:
        viber_request = viber.parse_request(request.body)
    except:
        return HttpResponse('ok', status=200)

    text_message = TextMessage(text="Оппа!")
    msgs = [text_message for i in range(0, 10)]

    if isinstance(viber_request, ViberConversationStartedRequest):
        text_message = TextMessage(text="Конверсэйшн! Приветствие! Логин!", trackingData='FIRST_LOGIN')
        viber.send_messages(viber_request.user.id, [
            text_message, 
            # KeyboardMessage(tracking_data='TRACKING_CREATE_AD_PHONE', 
            #                 keyboard=login_keyboard(viber_request.user.id),
            #                 min_api_version=6)
        ])
    elif isinstance(viber_request, ViberDeliveredRequest):
        return HttpResponse('ok', status=200)

    elif isinstance(viber_request, ViberSeenRequest):
        return HttpResponse('ok', status=200)
    elif isinstance(viber_request, ViberUnsubscribedRequest):
        return HttpResponse('ok', status=200)
    elif viber_request.message.text == 'MASS_MESSAGES':
        for i in range(0, 10):
            viber.send_messages(viber_request.sender.id, [
                text_message
            ])
    elif viber_request.message.text == 'MASS_MESSAGES2':
        viber.send_messages(viber_request.sender.id, msgs)
    else:
        # text_message = TextMessage(text="Оппа!")
        viber.send_messages(viber_request.sender.id, msgs)
        url_message = URLMessage(media="https://svoyaeda.su/api/");
        viber.send_messages(viber_request.sender.id, [
            text_message, url_message,
            KeyboardMessage(tracking_data='TRACKING_CREATE_AD_PHONE', 
                            keyboard=login_keyboard(viber_request.sender.id),
                            min_api_version=6)
        ])

    return HttpResponse('ok', status=200)