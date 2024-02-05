from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label=_('old password'),
                                   widget=forms.PasswordInput(attrs={'placeholder': _('Enter your old password')}))
    new_password1 = forms.CharField(label=_('new password'),
                                    widget=forms.PasswordInput(attrs={'placeholder': _('Enter your new password')}))
    new_password2 = forms.CharField(label=_('repeat new password'),
                                    widget=forms.PasswordInput(attrs={'placeholder': _('Repeat your new password')}))

    class Meta:
        model = get_user_model()
