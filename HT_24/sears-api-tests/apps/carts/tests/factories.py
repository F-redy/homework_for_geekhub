import factory

from apps.carts.models import Cart
from apps.products.tests.factories import ProductFactory
from apps.users.tests.factories import UserFactory


class CartFactory(factory.django.DjangoModelFactory):
    user = factory.SubFactory(UserFactory)
    quantity = factory.Faker('random_int')
    product = factory.SubFactory(ProductFactory)

    class Meta:
        model = Cart
