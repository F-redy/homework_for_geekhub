import factory

from apps.products.models import Category
from apps.products.models import Product


class CategoryFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda i: f'Category-{i}')

    class Meta:
        model = Category


class ProductFactory(factory.django.DjangoModelFactory):
    product_id = factory.Sequence(lambda i: f'A099702448{i}')
    category = factory.SubFactory(CategoryFactory)
    name = factory.Faker('word')
    brand = factory.Faker('word')
    image_url = factory.Faker('url')
    base_price = 500.0
    final_price = 450.0
    savings_price = 50.0
    url = factory.Faker('url')
    short_description = factory.Faker('paragraph')

    class Meta:
        model = Product
