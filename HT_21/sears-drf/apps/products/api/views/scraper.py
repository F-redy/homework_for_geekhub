import sys
from subprocess import Popen

from apps.products.api.serializers.scraper import ProductScraperSerializer
from apps.products.views.product_add import PROCESSING_MESSAGE
from apps.products.views.product_add import SCRAPE_ERROR_MESSAGE
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema
from drf_spectacular.utils import OpenApiExample
from drf_spectacular.utils import OpenApiParameter
from drf_spectacular.utils import OpenApiResponse
from rest_framework import generics
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response


@extend_schema(
    parameters=[
        OpenApiParameter(
            name='ids',
            description='product id from <a href="https://www.sears.com/" target="_blank">site</a>',
            required=True,
            type=str,
            examples=[
                OpenApiExample(
                    'Example 1',
                    description='one product ID',
                    value='A082465319'
                ),
                OpenApiExample(
                    'Example 2',
                    description='multiple product IDs',
                    value='A013234131,SPM8463462127,SPM8796106614'
                ),
            ],
        ),
    ],
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            description=_(PROCESSING_MESSAGE),
            response=None,
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description=_(SCRAPE_ERROR_MESSAGE),
            response=None,
        ),
    },
)
class ScrapeProduct(generics.CreateAPIView):
    serializer_class = ProductScraperSerializer
    permission_classes = [IsAdminUser, ]

    def create(self, request, *args, **kwargs):
        ids = request.data.get('ids')
        try:
            Popen([sys.executable, 'services/products/subscraper.py', ids])

            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)
