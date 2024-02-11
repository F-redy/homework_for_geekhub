from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.utils.translation import gettext_lazy as _

from apps.users.forms import LoginUserForm

SUCCESS_MESSAGE = 'Welcome {}!'


class LoginUserView(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': _('Login'), 'user_page': 'login'}
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super().form_valid(form)
        name = self.request.user.username.title() or self.request.user.email
        messages.success(self.request, _(SUCCESS_MESSAGE.format(name)))
        return response
