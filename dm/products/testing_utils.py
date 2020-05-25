# # -*- coding: utf-8 -*-
import random

from products.models import Shop, Category, Product, ProductImage


def create_test_dm_categories():
    titles = ['polufabrikati', 'konservaciya', 'vipechka', 'torti', 'myaso', 'ovoshi', 'napitki']
    cats = list()

    for title in titles:
        cats.append(Category(name=title, description=f'description of {title}', category_type='dm'))

    Category.objects.bulk_create(cats)


def create_test_dm_shops():
    titles = ['Вкусняшки от Елены', 'Консервы от Дугара', 'Стелла', 'АМТА', 'ИГОРЬ',
     'Овощи от дяди Славы', 'Овощи от дяди Пети', 'Александр самогон', 'Ольга Буузы',
     'мясопродукты Закамны']
    shops = list()

    for title in titles:
        shops.append(Shop(name=title, description=f'description of {title}', delivery='delivery dm'))

    Shop.objects.bulk_create(shops)


def gen_test_dm_products(shop_name, cats_list):
    shop = Shop.objects.get(name=shop_name)

    products = list()
    for cat in Category.objects.filter(name__in=cats_list):
        for i in range(0, random.randint(1, 7)):
            products.append(Product(shop=shop, category=cat, title=f'{cat.name} product {i}',
                 price=str(random.randint(10, 500))))
    Product.objects.bulk_create(products)

    for product in Product.objects.filter(price__gt=250, shop__name=shop_name):
        with open(f'../data/{product.category.name}.jpg', 'rb') as file:
            ProductImage.objects.create_product_image(product=product, image_file=file)


def create_test_dm_products():
    create_test_dm_categories()
    create_test_dm_shops()

    cats = Category.objects.filter(category_type='dm').values_list('name', flat=True)

    gen_test_dm_products(shop_name='Вкусняшки от Елены',
        cats_list=['polufabrikati', 'konservaciya', 'vipechka',])

    gen_test_dm_products(shop_name='Консервы от Дугара', cats_list=['konservaciya', ])

    gen_test_dm_products(shop_name='Стелла',
        cats_list=['polufabrikati', 'konservaciya', 'vipechka', 'torti', 'myaso', 'ovoshi', 'napitki'])

    gen_test_dm_products(shop_name='АМТА', cats_list=['torti', 'vipechka'])

    gen_test_dm_products(shop_name='ИГОРЬ', cats_list=['polufabrikati', 'myaso', 'ovoshi', 'napitki'])

    gen_test_dm_products(shop_name='Овощи от дяди Славы', cats_list=['ovoshi'])

    gen_test_dm_products(shop_name='Овощи от дяди Пети', cats_list=['ovoshi', 'konservaciya'])

    gen_test_dm_products(shop_name='Александр самогон', cats_list=['napitki'])

    gen_test_dm_products(shop_name='Ольга Буузы', cats_list=['polufabrikati',])

    gen_test_dm_products(shop_name='мясопродукты Закамны', cats_list=['polufabrikati', 'myaso'])
