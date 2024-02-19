from django.urls import path

from apps.users.api.views import UserListView

app_name = 'api_users'

urlpatterns = [
    path('', UserListView.as_view(), name='user_list'),
]
