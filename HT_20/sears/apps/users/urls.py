from apps.users import views
from django.urls import path

app_name = 'users'

urlpatterns = [
    path('registration/', views.RegistrationUserView.as_view(), name='registration'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path("change-password/", views.UserPasswordChangeView.as_view(), name='change_password'),
    path('logout/', views.logout_user, name='logout'),
]
