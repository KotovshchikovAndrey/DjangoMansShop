from django import forms
from .models import User
from django.core.exceptions import ValidationError
from .utils import PasswordMixin

class RegisterForm(PasswordMixin,forms.ModelForm):
    username = forms.CharField(required=True,label='Логин',widget=forms.TextInput(attrs={'class':'auth-form-input'}),
    error_messages={'required': 'Поле Логин Обязательно для заполнения!'})

    email = forms.CharField(required=True,label='Email',widget=forms.EmailInput(attrs={'class':'auth-form-input'}),
    error_messages={'required': 'Поле Email Обязательно для заполнения!'})

    class Meta:
        model = User
        fields = ('username','email','password','confirm_password')

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if User.objects.filter(username=username).exists():
            raise ValidationError('Пользователь с таким именем уже существует!')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError('Пользователь с таким email уже существует!')
        return email


class LoginForm(forms.Form):
    username = forms.CharField(required=True, label='Логин', widget=forms.TextInput(attrs={'class': 'auth-form-input'}),
    error_messages={'required': 'Поле Логин Обязательно для заполнения!'})

    password = forms.CharField(required=True, label='Пароль',widget=forms.PasswordInput(attrs={'class': 'auth-form-input'}),
    error_messages={'required': 'Поле Пароль Обязательно для заполнения!'})

class ResetForm(forms.Form):
    email = forms.CharField(required=True, label='Email', widget=forms.EmailInput(attrs={'class': 'auth-form-input'}),
    error_messages={'required': 'Поле Email Обязательно для заполнения!'})

class ChangePasswordForm(PasswordMixin,forms.ModelForm):

    class Meta:
        model = User
        fields = ('password','confirm_password')

class ProfileForm(forms.ModelForm):
    username = forms.CharField(required=True, label='Логин', widget=forms.TextInput(attrs={'class': 'auth-form-input'}))
    photo = forms.ImageField(required=False,label='Фото',widget=forms.FileInput(attrs={'class': 'auth-form-photo'}))
    email = forms.CharField(required=True, label='Email',widget=forms.EmailInput(attrs={'class': 'auth-form-input'}))
    balans = forms.CharField(required=False, label='Баланс',widget=forms.NumberInput(attrs={'class': 'auth-form-input','readonly': True}))

    class Meta:
        model = User
        fields = ('username','photo','email')

    def clean_username(self):
        username = self.cleaned_data.get('username')

        if username != self.instance.username and User.objects.filter(username=username).exists():
            raise ValidationError('Нельзя установить такое имя, так как оно уже занято!')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if email != self.instance.email and User.objects.filter(email=email).exists():
            raise ValidationError('Данная почта уже занята!')
        return email


