# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from circuit import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
