#!/usr/bin/env python
# -*- coding: utf-8 -*-

from .validators import ISBNValidator
from django.db.models import CharField, SubfieldBase


class ISBNField(CharField):

    __metaclass__ = SubfieldBase

    def __init__(self, *args, **kwargs):
        # Establecer la longitud máxima para ISBN13, y añadir validacion.
        kwargs['max_length'] = 13
        kwargs['validators'] = [ISBNValidator]
        super(ISBNField, self).__init__(*args, **kwargs)

    def formfield(self, **kwargs):
        defaults = {
            'max_length': 13,
            'min_length': 10,
            'validators': [ISBNValidator],
        }
        defaults.update(kwargs)
        return super(ISBNField, self).formfield(**defaults)

    def __unicode__(self):
        return self.value
