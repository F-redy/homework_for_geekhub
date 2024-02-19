from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from apps.users.tests.factories import UserFactory


class UsersListTestCase(APITestCase):
    client: APIClient
    maxDiff = None

    def test_unauthenticated_user_accessing_user_list_returns_401(self):
        UserFactory.create_batch(5)
        response = self.client.get(path=reverse('api_users:user_list'))

        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code, msg=response.content)
