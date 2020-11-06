# -*- coding: utf-8 -*-
from django.views import generic

from products.models import Shop, Category


class IndexView(generic.TemplateView):
    template_name = 'index.html'


class MainPageCategoryView(generic.TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['og_title'] = 'Домашняя продукция'
        context['og_description'] = 'Описание дм'
        context['og_image'] = None

        shop_pk = kwargs.get('shop_pk')
        if shop_pk:
            shop = Shop.objects.get(pk=shop_pk)
            # add category
            context['og_title'] = shop.name
            context['og_description'] = shop.description
            image = shop.products.all().first().images.all().first()
            if image:
                context['og_image'] = image.catalog_image.url

        cat_name = kwargs.get('cat_name')
        if cat_name:
            cat = Category.objects.filter(name=cat_name).first()
            context['og_title'] = cat.ru_name
            context['og_description'] = cat.description
            image = cat.images.all().first()
            if image:
                context['og_image'] = image.catalog_image.url

        return context