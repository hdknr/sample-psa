# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import views

urlpatterns = [
    url('^social/', include('social.apps.django_app.urls', namespace='social')),
] + views.AuthView.urls() + views.ProfileView.urls()
