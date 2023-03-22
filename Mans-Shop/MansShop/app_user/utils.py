from django import forms
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError

from app_user.models import User


class EmailAuthBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        user = User.objects.filter(email=username).first()
        if user is not None:
            is_correct_password = user.check_password(password)
            if is_correct_password:
                return user

        return None


class PasswordMixin(forms.ModelForm):
    password = forms.CharField(
        required=True,
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "auth-form-input"}),
        error_messages={"required": "Поле Пароль Обязательно для заполнения!"},
    )

    confirm_password = forms.CharField(
        required=True,
        label="Пароль",
        widget=forms.PasswordInput(attrs={"class": "auth-form-input"}),
        error_messages={"required": "Обязательно повторите свой Пароль!"},
    )

    def clean_password(self):
        password = self.cleaned_data.get("password")

        if len(password) < 8:
            raise ValidationError("Длинна пароля должна быть не меньше 8 символов")
        return password

    def clean(self):
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password is not None and password != confirm_password:
            raise ValidationError("Пароли не совпадают!")
        return self.cleaned_data
