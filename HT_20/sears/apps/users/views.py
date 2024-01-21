from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.generic import UpdateView

from apps.users.forms import LoginUserForm
from apps.users.forms import ProfileUserForm
from apps.users.forms import RegisterUserForm
from apps.users.forms import UserPasswordChangeForm


class RegistrationUserView(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/registration.html'
    extra_context = {'title': 'Registration', 'user_page': 'registration'}
    success_url = reverse_lazy('products:my_products')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(self.request, f'Registration successful! Welcome {self.request.user.username.title()}!')
        return response


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Login', 'user_page': 'login'}
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f'Welcome {self.request.user.username.title()}!')
        return response


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'users/profile.html'
    extra_context = {'title': 'User Profile', 'user_page': 'profile'}
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Profile updated successfully!')
        return response


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/change_password.html'
    extra_context = {'title': 'Change Password', 'user_page': 'change-password'}
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Password updated successfully!')
        return response


def logout_user(request):
    username = request.user.username.title()
    logout(request)
    messages.success(request, f'Goodbye, {username}! You have been successfully logged out.')
    return redirect('users:login')
