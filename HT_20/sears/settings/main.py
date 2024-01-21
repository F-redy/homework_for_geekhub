from settings.base import *

INSTALLED_APPS += [
    'apps.main.apps.MainConfig',  # main
    'apps.products.apps.ProductsConfig',  # products
    'apps.baskets.apps.BasketConfig',  # basket
    'apps.users.apps.UsersConfig',  # users
]

if DEBUG:
    INSTALLED_APPS += [
        'django_extensions',
        'debug_toolbar',
    ]

    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    INTERNAL_IPS = [
        "127.0.0.1",
    ]

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'products:my_products'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'apps.users.authentication.EmailAuthentication',
]
