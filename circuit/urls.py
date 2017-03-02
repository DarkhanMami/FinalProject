# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from circuit import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^calculate/$', views.calculate, name='calculate'),
    url(r'^new_circuit/$', views.new_circuit, name='new_circuit'),
    url(r'^new_rotation/$', views.new_rotation, name='new_rotation'),
    url(r'^remove_gate/$', views.remove_gate, name='remove_gate'),
    url(r'^new_swap/$', views.new_swap, name='new_swap'),
]
