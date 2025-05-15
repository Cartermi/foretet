from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,  SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model
from .models import *
from django.forms import ModelForm


from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm,  SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model
from .models import *
from django.forms import ModelForm

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(help_text='A valid email address, please.', required=True)

    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()

        return user

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username or Email'}),
        label="Username or Email*")

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))


class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

class PasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super(PasswordResetForm, self).__init__(*args, **kwargs)


class CustomerForm (ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        exclude = ['user', 'name']


class ProfileForm (ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user', 'name']

class AccountForm (ModelForm):
    class Meta:
        model = Account
        fields = '__all__'
        exclude = ['user', 'name']


class DepositForm (ModelForm):
    class Meta:
        model = Deposit
        fields = '__all__'
        exclude = ['user']


class AlertForm (ModelForm):
    class Meta:
        model = Alert
        fields = '__all__'
        exclude = ['user']

class WalletForm (ModelForm):
    class Meta:
        model = Wallet
        fields = '__all__'
        exclude = ['user']

class KycForm (ModelForm):
    class Meta:
        model = Kyc
        fields = '__all__'
        exclude = ['user', 'name']


class PinForm (ModelForm):
    class Meta:
        model = Pin
        fields = '__all__'
        exclude = ['user', 'name']

class ReportForm (ModelForm):
    class Meta:
        model = Report
        fields = '__all__'
        exclude = ['user']

class Alert1Form (ModelForm):
    class Meta:
        model = Alert
        fields = '__all__'
        exclude = ['user', 'name']

class Alert2Form (ModelForm):
    class Meta:
        model = Alert
        fields = '__all__'
        exclude = ['user', 'name']