from django.urls import path

from apps.home.views import index, login

app_name = 'home'

urlpatterns = [
    path('', index),
    path('login/', login),
]
