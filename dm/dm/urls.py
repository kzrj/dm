# -*- coding: utf-8 -*-
import os

from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings

from rest_framework import routers

from products.views import ProductAdViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r'product_ads', ProductAdViewSet, basename='product_ads')
router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
+ static('/media/', document_root=os.path.join(settings.BASE_DIR, '../media'))
