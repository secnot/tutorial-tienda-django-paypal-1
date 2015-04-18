#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import (LibroDetailView, AutorDetailView, 
    EditorialListaLibrosView, GeneroListaLibrosView)


urlpatterns = patterns('',
    url(
        regex = r'^libro/(?P<pk>\d+)/$',
        view  = LibroDetailView.as_view(),
        name  = "libro-detail"),
    url(
        regex = r'^autor/(?P<pk>\d+)/$',
        view  = AutorDetailView.as_view(),
        name  = "autor-detail"),
    url(
        regex = r'^editorial/(?P<pk>\d+)/$',
        view  = EditorialListaLibrosView.as_view(),
        name  = "editorial-libros"),
    url(
        regex = r'^genero/(?P<pk>\d+)/$',
        view  = GeneroListaLibrosView.as_view(),
        name  = "genero-libros"),
)

