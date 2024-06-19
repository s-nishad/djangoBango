from django.urls import path

from home.views import console_view, redirect_view

app_name = 'home'
urlpatterns = [
    path('', redirect_view, name='redirect'),
    path('home/', console_view, name='home')
]