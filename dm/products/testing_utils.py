# # -*- coding: utf-8 -*-
import random

from django.contrib.auth.models import User

from products.models import Shop, Category, Product, ProductImage
from profiles.models import Profile


def create_test_dm_categories():
    titles = [('polufabrikati', 'полуфабрикаты'), ('konservaciya', 'консервация'),
     ('vipechka', 'выпечка'), ('torti', 'торты'), ('myaso', 'мясо'), ('ovoshi', 'овощи'),
     ('napitki', 'напитки')]
    cats = list()

    for title in titles:
        cats.append(Category(name=title[0], ru_name=title[1], description=f'description of {title}',
         category_type='dm'))

    Category.objects.bulk_create(cats)


def create_test_dm_shops():
    titles = ['Вкусняшки от Елены', 'Консервы от Дугара', 'Стелла', 'АМТА', 'ИГОРЬ',
     'Овощи от дяди Славы', 'Овощи от дяди Пети', 'Александр самогон', 'Ольга Буузы',
     'мясопродукты Закамны']
    shops = list()

    for title in titles:
        shops.append(Shop(name=title, description=f'description of {title}', delivery='delivery dm'))

    Shop.objects.bulk_create(shops)


def gen_test_dm_products(shop_name, cats_list, images=True):
    shop = Shop.objects.get(name=shop_name)

    products = list()
    for cat in Category.objects.filter(name__in=cats_list):
        for i in range(0, random.randint(1, 7)):
            products.append(Product(shop=shop, category=cat, title=f'{cat.name} product {i}',
                 price=str(random.randint(10, 500))))
    Product.objects.bulk_create(products)

    if images:
        for product in Product.objects.filter(price__gt=250, shop__name=shop_name):
            with open(f'../data/{product.category.name}.jpg', 'rb') as file:
                ProductImage.objects.create_product_image(product=product, image_file=file)


def create_test_dm_products(images_onOff=True):
    User.objects.create_superuser(username='kaizerj', email='kzrster@gmail.com', password='jikozfree')
    user = User.objects.create_user(username='kzr', password='qwerty123')
    Profile.objects.create(user=user)

    create_test_dm_categories()
    create_test_dm_shops()

    cats = Category.objects.filter(category_type='dm').values_list('name', flat=True)

    gen_test_dm_products(shop_name='Вкусняшки от Елены',
        cats_list=['polufabrikati', 'konservaciya', 'vipechka',], images=images_onOff)

    gen_test_dm_products(shop_name='Консервы от Дугара', cats_list=['konservaciya'], images=images_onOff)

    gen_test_dm_products(shop_name='Стелла',
        cats_list=['polufabrikati', 'konservaciya', 'vipechka', 'torti', 'myaso', 'ovoshi', 'napitki'],
        images=images_onOff)

    gen_test_dm_products(shop_name='АМТА', cats_list=['torti', 'vipechka'], images=images_onOff)

    gen_test_dm_products(shop_name='ИГОРЬ', cats_list=['polufabrikati', 'myaso', 'ovoshi', 'napitki'],
        images=images_onOff)

    gen_test_dm_products(shop_name='Овощи от дяди Славы', cats_list=['ovoshi'], images=images_onOff)

    gen_test_dm_products(shop_name='Овощи от дяди Пети', cats_list=['ovoshi', 'konservaciya'],
        images=images_onOff)

    gen_test_dm_products(shop_name='Александр самогон', cats_list=['napitki'], images=images_onOff)

    gen_test_dm_products(shop_name='Ольга Буузы', cats_list=['polufabrikati',], images=images_onOff)

    gen_test_dm_products(shop_name='мясопродукты Закамны', cats_list=['polufabrikati', 'myaso'],
     images=images_onOff)
