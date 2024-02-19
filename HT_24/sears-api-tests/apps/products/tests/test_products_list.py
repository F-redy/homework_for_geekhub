from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from apps.products.tests.factories import ProductFactory


class ProductsListTasCase(APITestCase):
    client: APIClient
    maxDiff: None

    def test_products_list_returns_success(self):
        products = ProductFactory.create_batch(10)
        response = self.client.get(
            path=reverse('api_products:products_list')
        )

        response_data = response.json()

        self.assertEqual(status.HTTP_200_OK, response.status_code, msg=response.content)
        self.assertEqual(len(products), response_data['count'], msg=response.content)

        for product in products:
            self.assertIn(
                {
                    "pk": product.pk,
                    'product_id': product.product_id,
                    'category': product.category.pk,
                    'name': product.name,
                    'brand': product.brand,
                    'image_url': product.image_url,
                    'base_price': product.base_price,
                    'final_price': product.final_price,
                    'savings_price': product.savings_price,
                    'url': product.url,
                    'short_description': product.short_description
                },
                response_data['results']
            )
