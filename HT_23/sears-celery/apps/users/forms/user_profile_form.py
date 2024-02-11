from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _


class ProfileUserForm(forms.ModelForm):
    email = forms.CharField(
        disabled=True,
        label=_('email'),
        widget=forms.EmailInput()
    )
    username = forms.CharField(
        label=_('username'),
        widget=forms.TextInput())
    first_name = forms.CharField(
        label=_('first name'),
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': _('Enter your first name')}
        )
    )
    last_name = forms.CharField(
        label=_('last name'),
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': _('Enter your last name')}
        )
    )

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'first_name', 'last_name')
