from django.contrib import messages
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _

SUCCESS_MESSAGE = 'Goodbye, {}! You have been successfully logged out.'


def logout_user(request):
    name = request.user.username.title() or request.user.email
    logout(request)
    messages.success(request, _(SUCCESS_MESSAGE.format(name)))
    return redirect('users:login')
