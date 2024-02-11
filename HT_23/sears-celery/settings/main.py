from settings.base import *

INSTALLED_APPS += [
    # extra apps
    'django_extensions',  # shell_plus
    'rest_framework',  # drf
    'drf_spectacular',  # spectacular

    # custom apps
    'apps.main.apps.MainConfig',  # main
    'apps.products.apps.ProductsConfig',  # products
    'apps.carts.apps.CartConfig',  # cart
    'apps.users.apps.UsersConfig',  # users
]

LOGIN_URL = 'users:login'
LOGIN_REDIRECT_URL = 'products:my_products'

CART_SESSION_KEY = 'cart'

# DRF
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'PAGE_SIZE': 10,
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
}

# SPECTACULAR
SPECTACULAR_SETTINGS = {
    'TITLE': 'Sears Scraper API',
    'DESCRIPTION': 'DRF tutorial project',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,

    'SWAGGER_UI_DIST': 'SIDECAR',  # shorthand to use the sidecar instead
    'SWAGGER_UI_FAVICON_HREF': 'SIDECAR',
    'REDOC_DIST': 'SIDECAR',
}

# Redis
REDIS_URL = env('REDIS_URL')

# Celery
CELERY_TIMEZONE = 'Europe/Kiev'
CELERY_TASK_TRACK_STARTED = True
CELERY_BROKER_URL = f'{REDIS_URL}'
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT = ['json']

if DEBUG:
    INSTALLED_APPS += [
        'debug_toolbar',
        'drf_spectacular_sidecar',
    ]

    MIDDLEWARE += [
        "debug_toolbar.middleware.DebugToolbarMiddleware",
    ]

    INTERNAL_IPS = [
        "127.0.0.1",
    ]
