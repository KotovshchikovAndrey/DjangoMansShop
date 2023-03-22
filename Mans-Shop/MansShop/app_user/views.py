from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse, redirect, render
from django.urls import reverse
from django.views import View

from .forms import *
from .services import (
    change_user_password,
    get_form_errors,
    registration,
    send_mail_for_reset_password,
)


class RegisterView(View):
    def get(self, request):
        form = RegisterForm()

        context = {
            "title": "Регистрация",
            "form": form,
            "action": "Зарегистрироваться",
            "url": reverse("register"),
        }

        return render(request, "app_user/auth.html", context)

    def post(self, request):
        form = RegisterForm(request.POST)

        if form.is_valid():
            registration(request, form)
            return redirect("/")

        context = {
            "title": "Регистрация",
            "form": form,
            "action": "Зарегистрироваться",
            "errors": get_form_errors(form),
            "url": reverse("register"),
        }

        return render(request, "app_user/auth.html", context)


class LoginView(View):
    def get(self, request):
        form = LoginForm()

        context = {
            "title": "Авторизация",
            "form": form,
            "action": "Авторизироваться",
            "url": reverse("login"),
        }

        return render(request, "app_user/auth.html", context)

    def post(self, request):
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return redirect("/")
            form.add_error("__all__", "Неверный Логин или Пароль!")

        context = {
            "title": "Авторизация",
            "form": form,
            "action": "Авторизироваться",
            "errors": get_form_errors(form),
            "url": reverse("login"),
        }

        return render(request, "app_user/auth.html", context)


def logout_view(request):
    logout(request)
    return redirect("/")


class ResetPasswordView(View):
    def get(self, request):
        form = ResetForm()

        context = {
            "title": "Сброс Пароля",
            "form": form,
            "action": "Отправить",
            "url": reverse("reset"),
        }

        return render(request, "app_user/auth.html", context)

    def post(self, request):
        form = ResetForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data.get("email")
            try:
                user = User.objects.get(email=email)
            except:
                user = None

            if user:
                mail = send_mail_for_reset_password(user, email)
                if mail:
                    return HttpResponse(
                        "Письмо Успешно Оправленно, проверьте свою почту"
                    )

                return HttpResponse(
                    "Ошибка отправки письма, посвторите поппытку позже,возможно такого Email не существует, проверьте правильно ли вы написали адресс почты"
                )
            form.add_error("email", "Пользователь с таким Email не найден!")

        context = {
            "title": "Сброс Пароля",
            "form": form,
            "action": "Отправить",
            "errors": get_form_errors(form),
            "url": reverse("reset"),
        }

        return render(request, "app_user/auth.html", context)


class ChangePasswordView(View):
    def get(self, request, **kwargs):
        form = ChangePasswordForm()

        context = {
            "title": "Изменение Пароля",
            "form": form,
            "action": "Сменить",
            "url": reverse("change", kwargs=kwargs),
        }

        return render(request, "app_user/auth.html", context)

    def post(self, request, **kwargs):
        form = ChangePasswordForm(request.POST)

        if form.is_valid():
            change_user_password(request, form, kwargs)
            return HttpResponse("Пароль успешно изменен!")

        context = {
            "title": "Изменение Пароля",
            "form": form,
            "action": "Сменить",
            "errors": get_form_errors(form),
            "url": reverse("change", kwargs=kwargs),
        }

        return render(request, "app_user/auth.html", context)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        form = ProfileForm(instance=request.user)

        context = {
            "title": "Профиль",
            "form": form,
            "action": "Изменить Данные",
            "url": reverse("profile"),
        }

        return render(request, "app_user/profile.html", context)

    def post(self, request):
        form = ProfileForm(
            instance=request.user, data=request.POST, files=request.FILES
        )

        if form.is_valid():
            form.save()
            return redirect("profile")

        context = {
            "title": "Профиль",
            "form": form,
            "action": "Изменить Данные",
            "errors": get_form_errors(form),
            "url": reverse("profile"),
        }

        return render(request, "app_user/profile.html", context)
