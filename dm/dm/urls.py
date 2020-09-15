# -*- coding: utf-8 -*-
import os

from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers

from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

from products.views import ProductViewSet, CategoryViewSet, ShopViewSet, InitTestDataView, viber_view
from profiles.views import ContactViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'shops', ShopViewSet, basename='shops')
router.register(r'contacts', ContactViewSet, basename='contacts')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^api/init_data/$', InitTestDataView.as_view()),
    url(r'^api/jwt/api-token-auth/', obtain_jwt_token),
    url(r'^api/jwt/api-token-refresh/', refresh_jwt_token),
    url(r'^api/jwt/api-token-verify/', verify_jwt_token),
    path('viber/', viber_view, name='viber'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static('/media/', document_root=os.path.join(settings.BASE_DIR, '../media'))
