"""
URL configuration for djangoBango project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView, \
    PasswordResetView
from django.urls import path, include

from djangoBango import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls', namespace='home')),
    path('auth/', include('user.urls', namespace='user')),
    path('user/', include([
        # password reset functionality
        path('password-reset/', PasswordResetView.as_view(template_name='user/password_reset.html'),
             name='password-reset'),
        path('password-reset/done/', PasswordResetDoneView.as_view(template_name='user/password_reset_done.html'),
             name='password_reset_done'),
        path('password-reset-confirm/<uidb64>/<token>/',
             PasswordResetConfirmView.as_view(template_name='user/password_reset_confirm.html'),
             name='password_reset_confirm'),
        path('password-reset-complete/',
             PasswordResetCompleteView.as_view(template_name='user/password_reset_complete.html'),
             name='password_reset_complete'),
    ])),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
