# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url('^social/', include('social_django.urls', namespace='social')),
] + views.AuthView.urls() + views.ProfileView.urls()
