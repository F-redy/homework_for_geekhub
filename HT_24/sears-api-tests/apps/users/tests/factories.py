import factory

from apps.users.models import User

TEST_PASSWORD = 'testuserpasssword111'


class UserFactory(factory.django.DjangoModelFactory):
    email = factory.Sequence(lambda i: f'test_email_{i}@example.com')
    password = factory.PostGenerationMethodCall('set_password', TEST_PASSWORD)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.Faker('user_name')

    class Meta:
        model = User
