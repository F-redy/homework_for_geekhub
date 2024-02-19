from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from apps.products.tests.factories import CategoryFactory


class CategoryListTasCase(APITestCase):
    client: APIClient
    maxDiff: None

    def test_categories_list_returns_success(self):
        categories = CategoryFactory.create_batch(10)
        response = self.client.get(
            path=reverse('api_products:categories_list')
        )
        response_data = response.json()

        self.assertEqual(status.HTTP_200_OK, response.status_code, msg=response.content)
        self.assertEqual(len(categories), response_data['count'], msg=response.content)

        for category in categories:
            self.assertIn(
                {
                    'pk': category.pk,
                    'name': category.name,
                    'quantity_products': 0
                },
                response_data['results']
            )
