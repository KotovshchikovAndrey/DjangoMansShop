from django.urls import path
from .views import *

urlpatterns = [
    path('register/',RegisterView.as_view(),name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',logout_view,name='logout'),
    path('reset/',ResetPasswordView.as_view(),name='reset'),
    path('change/<str:uidb64>/<str:token>/',ChangePasswordView.as_view(),name='change'),
    path('profile/',ProfileView.as_view(),name='profile'),
]