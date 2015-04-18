#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import patterns, url
from .views import PaypalView, PaypalExecuteView


urlpatterns = patterns('',
    url(
        regex = r'^pago/(?P<libro_pk>\d+)/$',
        view  = PaypalView.as_view(),
        name  = "pago-paypal"),
    url(
        regex = r'^aceptar-pago/$',
        view  = PaypalExecuteView.as_view(),
        name  = "aceptar-pago-paypal"),
)

