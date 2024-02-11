from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import CreateView

from apps.users.forms import RegisterUserForm

SUCCESS_MESSAGE = 'Registration successful! Welcome {}!'


class RegistrationUserView(CreateView):
    form_class = RegisterUserForm
    template_name = 'users/registration.html'
    extra_context = {'title': _('Registration'), 'user_page': 'registration'}
    success_url = reverse_lazy('products:my_products')

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object, backend='django.contrib.auth.backends.ModelBackend')
        name = self.request.user.username.title() or self.request.user.email
        messages.success(self.request, _(SUCCESS_MESSAGE.format(name)))
        return response
