from settings.base import *

INSTALLED_APPS += [
    'apps.products.apps.ProductsConfig',
    'apps.baskets.apps.BasketConfig',
]

if DEBUG:
    INSTALLED_APPS += [
        'django_extensions',
    ]
