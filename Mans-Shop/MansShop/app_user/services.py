from django.contrib.auth import login
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from .models import User

def change_user_password(request,form,kwargs):
    password = form.cleaned_data.get('password')
    user_id = force_text(urlsafe_base64_decode(kwargs['uidb64']))
    user = User.objects.get(pk=user_id)
    user.set_password(password)
    user.save()
    login(request,user,backend='django.contrib.auth.backends.ModelBackend')


def send_mail_for_reset_password(user,email):
    token = default_token_generator.make_token(user)
    uidb = urlsafe_base64_encode(force_bytes(user.pk))

    context = {
        'protocol': 'http',
        'domain': 'http://127.0.0.1:8000',
        'token': token,
        'uidb': uidb,
        'username': user.username
    }

    message = render_to_string('app_user/email_message.html', context)
    mail = send_mail('Ссылка на сброс пароля', 'ссылка', settings.EMAIL_HOST_USER, [email], fail_silently=True,html_message=message)

    return mail

def registration(request,form):
    password = form.cleaned_data['password']
    user = form.save(commit=False)
    user.set_password(password)
    user.save()
    login(request,user,backend='django.contrib.auth.backends.ModelBackend')


def get_form_errors(form):
    error_list = []

    for error_field in form.errors:
        for error in form.errors[error_field]:
            error_list.append(error)

    return error_list
