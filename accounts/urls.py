# -*- coding: utf-8 -*-
from . import views

urlpatterns = [
] + views.AuthView.urls() + views.ProfileView.urls()
