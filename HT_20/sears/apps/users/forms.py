from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='username', widget=forms.TextInput(
        attrs={'placeholder': 'Enter your username or e-mail'}))
    password = forms.CharField(label='password',
                               widget=forms.PasswordInput(
                                   attrs={'placeholder': 'Enter your password'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='username',
                               widget=forms.TextInput(attrs={'placeholder': 'Enter your username'}))
    password1 = forms.CharField(label='password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password'}))
    password2 = forms.CharField(label='repeat password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your password'}))
    email = forms.CharField(label='e-mail',
                            widget=forms.EmailInput(attrs={'placeholder': 'Enter your e-mail(not necessary)'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password1', 'password2', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('That e-mail already exists!')
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='username', widget=forms.TextInput())
    email = forms.CharField(disabled=True, label='e-mail', required=False,
                            widget=forms.EmailInput(attrs={'placeholder': 'Enter your e-mail'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name']
        labels = {'first_name': 'first name', 'last_name': 'last name'}
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'})
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label='old password',
                                   widget=forms.PasswordInput(attrs={'placeholder': 'Enter your old password'}))
    new_password1 = forms.CharField(label='new password',
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Enter your new password'}))
    new_password2 = forms.CharField(label='repeat new password',
                                    widget=forms.PasswordInput(attrs={'placeholder': 'Repeat your new password'}))

    class Meta:
        model = get_user_model()
