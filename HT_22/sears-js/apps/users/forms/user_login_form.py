from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import gettext_lazy as _


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(
        label=_('email'),
        widget=forms.TextInput(
            attrs={'placeholder': _('Enter your e-mail')}
        )
    )
    password = forms.CharField(
        label=_('Password'),
        widget=forms.PasswordInput(
            attrs={'placeholder': _('Enter your password')}
        )
    )

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']
