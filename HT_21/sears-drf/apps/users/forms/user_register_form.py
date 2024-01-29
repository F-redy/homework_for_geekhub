from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

VALIDATION_ERROR_MESSAGES = _('That e-mail already exists!')


class RegisterUserForm(UserCreationForm):
    email = forms.CharField(
        label=_('e-mail'),
        widget=forms.EmailInput(
            attrs={
                'placeholder': _('Enter your e-mail'),
            }
        )
    )
    username = forms.CharField(
        label=_('username'),
        required=False,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Enter your username'),
            }
        )
    )
    password1 = forms.CharField(
        label='password',
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Enter your password'),
            }
        )
    )
    password2 = forms.CharField(
        label=_('repeat password'),
        widget=forms.PasswordInput(
            attrs={
                'placeholder': _('Repeat your password'),
            }
        )
    )

    class Meta:
        model = get_user_model()
        fields = ['email', 'username', 'password1', 'password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError(VALIDATION_ERROR_MESSAGES)
        return email
