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
    url(r'^find_adj_gates/$', views.find_adj_gates, name='find_adj_gates'),
    url(r'^insert_gate/$', views.insert_gate, name='insert_gate'),
    url(r'^insert_rotation/$', views.insert_rotation, name='insert_rotation'),
    url(r'^insert_swap/$', views.insert_swap, name='insert_swap'),
    url(r'^export_dump/$', views.export_dump, name='export_dump'),
]
