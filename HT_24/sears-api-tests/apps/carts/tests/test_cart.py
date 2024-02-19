from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from apps.carts.tests.factories import CartFactory
from apps.products.tests.factories import ProductFactory
from apps.users.tests.factories import UserFactory

QUANTITY = 3


class CartTestCase(APITestCase):
    client: APIClient()
    maxDiff = None

    def test_access_not_authenticated_user_prohibited(self):
        response = self.client.get(
            path=reverse('api_carts:cart-list'),
        )
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code, msg=response.content)
        self.assertDictEqual(
            response.json(),
            {'detail': 'Authentication credentials were not provided.'},
            msg=response.content
        )

    def test_add_product_to_cart_success(self):
        self.client.force_authenticate(user=UserFactory())
        product = ProductFactory()

        response = self.client.post(
            path=reverse('api_carts:cart-list'),
            data={
                'quantity': QUANTITY,
                'product': product.pk
            }
        )

        self.assertEqual(status.HTTP_201_CREATED, response.status_code, msg=response.content)
        self.assertDictEqual(
            {
                'pk': 1,
                'user': 1,
                'price': product.final_price,
                'quantity': QUANTITY,
                'product': product.pk,
                'products_price': product.final_price * QUANTITY
            },
            response.json(),
            msg=response.content
        )

    def test_view_cart_list(self):
        self.client.force_authenticate(user=UserFactory())
        products = ProductFactory.create_batch(5)

        for product in products:
            response = self.client.post(
                path=reverse('api_carts:cart-list'),
                data={
                    'quantity': QUANTITY,
                    'product': product.pk
                }
            )
            self.assertEqual(status.HTTP_201_CREATED, response.status_code, msg=response.content)

        response = self.client.get(reverse('api_carts:cart-list'))
        response_data = response.json()

        self.assertEqual(len(products), response_data['count'], msg=response.content)

        for indx, product in enumerate(products, 1):
            self.assertIn(
                {
                    'pk': indx,
                    'user': 1,
                    'price': product.final_price,
                    'quantity': QUANTITY,
                    'product': product.pk,
                    'products_price': product.final_price * QUANTITY
                },
                response_data['results']
            )

    def test_add_existing_product_to_cart(self):
        self.client.force_authenticate(user=UserFactory())

        cart = CartFactory()

        response = self.client.post(
            path=reverse('api_carts:cart-list'),
            data={
                'quantity': cart.quantity,
                'product': cart.product.pk
            }
        )

        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code, msg=response.context)
        self.assertDictEqual(
            response.json(),
            {'product': ['cart with this product already exists.']},
            msg=response.content
        )
