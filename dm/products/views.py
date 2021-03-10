# # -*- coding: utf-8 -*-
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import action

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.shortcuts import render

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
    ShopSerializer, ShopWithProductsSerializer, ShopDetailSerializer,  \
    CreateShopSerializer, UpdateShopSerializer, CreateProductSerializer, \
    UpdateProductSerializer, ActivateDeactivateProductSerializer, \
    ProductImageCreateSerializer, ProductImageIdSerializer, ShopDetailAllProductSerializer
from products.models import Product, Category, Shop
from products.testing_utils import create_test_dm_products
from products.filters import ShopFilter
from profiles.models import Profile, SocialLink
from profiles.serializers import ProfileSerializer

from core.utils import create_token


class CoreViewSet(viewsets.ViewSet):
    def destroy(self, request, pk=None):
        pass


class CategoryViewSet(CoreViewSet, viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.get_all()
    serializer_class = ProductSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return CreateProductSerializer
        if self.action == 'partial_update':
            return UpdateProductSerializer
        return self.serializer_class

    def create(self, request):
        serializer = UpdateProductSerializer(data=request.data)
        if serializer.is_valid():
            product = Product.objects.create_product(
                title=serializer.validated_data['title'],
                price=serializer.validated_data['price'],
                description=serializer.validated_data.get('description'),
                category=serializer.validated_data['category'],
                shop=request.user.profile.shop
            )
            return Response(ProductSerializer(product).data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, serializer_class=ProductImageCreateSerializer)
    def add_image(self, request, pk=None):
        serializer = ProductImageCreateSerializer(data=request.data)
        if serializer.is_valid():
            product = self.get_object()
            product.images.create_product_image(
                image_file=serializer.validated_data['original'],
                product=product
            )
            product.refresh_from_db()
            
            return Response(
                {
                    "product": ProductSerializer(product).data,
                    "message": "Изображение добавлено."
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['post'], detail=True, serializer_class=ProductImageIdSerializer)
    def delete_image(self, request, pk=None):
        serializer = ProductImageIdSerializer(data=request.data)
        if serializer.is_valid():
            product = self.get_object()
            image = serializer.validated_data['image']
            image.delete()
            product.refresh_from_db()
            
            return Response(
                {
                    "product": ProductSerializer(product).data,
                    "message": "Изображение удалено."
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ShopViewSet(viewsets.ModelViewSet):
    queryset = Shop.objects.all().prefetch_related('likes', 'feedbacks') 
    serializer_class = ShopSerializer
    filter_class = ShopFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ShopDetailSerializer
        if self.action == 'create':
            return CreateShopSerializer
        if self.action == 'partial_update':
            return UpdateShopSerializer
        return self.serializer_class

    def list(self, request):
        category_name = request.GET.get('category', None)

        if category_name:
            queryset = self.filter_queryset(
                self.queryset \
                    .add_products_count_by_dm_cat() \
                    .add_category_products(category_name=category_name)) \
                    .add_category_products_images_quantity(category_name=category_name)
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

    def create(self, request):
        serializer = CreateShopSerializer(data=request.data)
        if serializer.is_valid():
            shop = Shop.objects.create_shop(**serializer.validated_data)
            profile = serializer.validated_data['profile']
            profile.refresh_from_db()
            return Response(
                {
                    "message": "Created",
                    "shop": ShopDetailAllProductSerializer(shop).data,
                    "profile": ProfileSerializer(profile).data
                },
                status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None, *args, **kwargs):
        socials = request.data.get('socials')
        if socials:
            shop = self.get_object()
            shop.socials.create_update_delete_for_shop(shop=shop, socials=socials)

        return super(ShopViewSet, self).partial_update(request, *args, **kwargs)

    def destroy(self, request, pk=None):
        pass

    @action(methods=['post'], detail=True)
    def like(self, request, pk=None):
        shop = self.get_object()
        shop.likes.set_like_unlike(profile=request.user.profile, shop=shop)
        return Response(
            {
                "message": "Liked or Unliked",
                "likes_list": shop.likes_list
            },
            status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True)
    def viber_link(self, request, pk=None):
        shop = self.get_object()
        product = shop.products.all().first()

        context = {'shop': shop, 'image': product.images.all().first().catalog_image.url}
        return render(request, 'shop_detail.html', context)


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
    token = 'token'
    return {
            "Type": "keyboard",
            "Buttons": [
               {
                    "Columns": 6,
                    "Rows": 2,
                    "Text": "<br><font color=#494E67><b>Смотреть объявления</b></font>",
                    "TextSize": "regular",
                    "TextHAlign": "center",
                    "TextVAlign": "middle",
                    "ActionType": "open-url",
                    "ActionBody": f"https://svoyaeda.su/dm/login/v/{viber_id}",
                    "OpenURLType": "external",
                    "BgColor": "#20c997",
                    "Image": "https://s18.postimg.org/9tncn0r85/sushi.png"
                },
            ],
            "InputFieldState": 'regular'
        }


@csrf_exempt
def viber_view(request):
    viber_request = viber.parse_request(request.body)

    if isinstance(viber_request, ViberUnsubscribedRequest):
        return HttpResponse('ok', status=200)

    if isinstance(viber_request, ViberConversationStartedRequest):
        viber_user = viber_request.user

        text_message = TextMessage(text="Привет! Отправьте сообщение и сможете войти.")
        viber.send_messages(viber_request.user.id, [ text_message ])
    else:
        viber_user = viber_request.sender

        customer = Profile.objects.get_or_create_profile_viber(
                viber_id=viber_user.id,
                viber_name=viber_user.name,
                viber_avatar=viber_user.avatar,
                )

        if hasattr(viber_request, 'message'):
            if viber_request.message.tracking_data == 'TRACKING_SHOW_WEBSITE':
                return HttpResponse('ok', status=200)

        text_message = TextMessage(text="Нажмите кнопку 'Смотреть объявления'!")
        token = create_token(customer.user)
        viber.send_messages(viber_request.sender.id, [
            text_message, 
            KeyboardMessage(keyboard=login_keyboard(token),
                            tracking_data='TRACKING_SHOW_WEBSITE', 
                            min_api_version=6)
        ])

    return HttpResponse('ok', status=200)