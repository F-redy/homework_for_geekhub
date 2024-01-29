from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from apps.users.forms import UserPasswordChangeForm

SUCCESS_MESSAGE = _('Password updated successfully!')


class UserPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = UserPasswordChangeForm
    template_name = 'users/change_password.html'
    extra_context = {'title': _('Change Password'), 'user_page': 'change-password'}
    success_url = reverse_lazy('users:profile')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, SUCCESS_MESSAGE)
        return response
