#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings

from django.core.urlresolvers import reverse

from django_countries.fields import CountryField
from django_languages import LanguageField
from isbn_field.fields import ISBNField
from uuid import uuid4
from datetime import date
from easy_thumbnails.fields import ThumbnailerImageField
from django.utils.translation import ugettext_lazy as _
import os

# easy_thumbnails generate thumbnails at creation
from easy_thumbnails.signals import saved_file
from easy_thumbnails.signal_handlers import generate_aliases_global
saved_file.connect(generate_aliases_global)



# Create your models here.

class ImagenMixin(models.Model):
    """Añade una imagen con miniaturas al modelo"""   
 
    def _generar_ruta_imagen(instance, filename):
        """Generar la ruta donde almacenar la imagen, el nombre de la imagén
        es modificado para que no existan colisiones."""
        # Extraer la extensión original de la imagen
        ext = os.path.splitext(filename)[1][1:]

        # Generar el directorio concatenando el nombre del modelo y la fecha 
        # para no almacenar muchas imagenes por directorio.
        nombre_modelo = instance.__class__.__name__
        ruta = os.path.join('imagenes', nombre_modelo, date.today().strftime("%Y/%m"))

        # Generar nombre archivo uniendo una cadena aleatoria con la extension
        # original.
        nombre_archivo = '{}.{}'.format(uuid4().hex, ext)

        # Se devuelve la ruta completa
        return os.path.join(ruta, nombre_archivo)
 
    imagen = ThumbnailerImageField(upload_to=_generar_ruta_imagen, 
        blank=True)

    class Meta:
        abstract = True
    

class PublicadoMixin(models.Model):
    """Añade campos comunes a todo el contenido publicado"""
    ESTADO_ACTIVO    = 'A' # El contenido se puede mostrar
    ESTADO_BORRADOR  = 'B' # Solo el creador puede ver la entrada
    ESTADO_BLOQUEADO = 'Q' # No se puede mostrar
    ESTADO_OPCIONES = (
        (ESTADO_ACTIVO,     _(u'Activo')),
        (ESTADO_BORRADOR,   _(u'Borrador')),
        (ESTADO_BLOQUEADO,  _(u'Bloqueado')))

    estado = models.CharField(max_length=1, choices=ESTADO_OPCIONES, 
        default=ESTADO_ACTIVO)
    
    # Usuario que creo este contenido
    creador = models.ForeignKey(settings.AUTH_USER_MODEL)
    
    # Fechas de creacion y ultima modificacion
    creado = models.DateTimeField(auto_now_add=True, editable=False)
    modificado = models.DateTimeField(auto_now=True)

    # Contenido promocionado, que es mostrado de forma preferente.
    promo = models.BooleanField(default=False) 

    class Meta:
        abstract = True



class Editorial(models.Model):
    """Editorial del libro"""
    nombre = models.CharField(max_length=40, unique=True, db_index=True)
    nombre_completo = models.CharField(blank=True, max_length=150) 
    pais = CountryField();

    # Pagina del editor
    web = models.URLField(max_length=300, blank=True)
    
    # Informacion de contacto de la editoral
    email = models.EmailField(blank=True)
    notas = models.TextField(blank=True, max_length=2000)
    
    def __str__(self):
        if self.nombre_completo:
            return self.nombre_completo
        else:
            return self.nombre

    def get_absolute_url(self):
        return reverse('editorial-libros', args=[str(self.id)])


class Genero(models.Model):
    """Posibles generos de los libros"""
    nombre = models.CharField(max_length=50, unique=True)
    descripcion = models.TextField(max_length=500, blank=True)

    # Generos relacionados con este, mas sencillo que un arbol jerarquizado
    generos_relacionados = models.ManyToManyField('self', blank=True)

    def __str__(self):
        return self.nombre
    
    def get_absolute_url(self):
        return reverse('genero-libros', args=[str(self.id)])



class Autor(PublicadoMixin, ImagenMixin):
    """ """ 
    GENERO_HOMBRE   = 'H'
    GENERO_MUJER    = 'M'
    GENERO_OPCIONES = (
        (GENERO_HOMBRE, u'Hombre'),
        (GENERO_MUJER,  u'Mujer'),
    )

    # Basic information
    nombre_completo = models.CharField(max_length=100, 
        verbose_name='Nombre y Apellidos', db_index=True)
    biografia = models.TextField(blank=True, max_length=2000)

    # Extra author info
    genero      = models.CharField(choices=GENERO_OPCIONES, 
                        max_length=1, default=GENERO_HOMBRE)
    nacionalidad = CountryField(blank=True, default='US')
    fecha_nacimiento  = models.DateField(blank=True, null=True)
    fecha_muerte  = models.DateField(blank=True, null=True)
    
    lugar_nacimiento = models.CharField(max_length=100, blank=True)

    # Authors net info
    web       = models.URLField(blank=True)
    wikipedia = models.URLField(blank=True)
    twitter_username = models.CharField(max_length=50, blank=True)

    def get_absolute_url(self):
        return reverse('autor-detail', args=[str(self.id)])

    def __str__(self):
        return self.nombre_completo



class Libro(PublicadoMixin, ImagenMixin):
    """Novels are never displayed, and are used to link together
    all the editions, with the common information among them
    authors, genre..."""

    # Informacion basica del libro
    titulo = models.CharField(max_length=200, db_index=True)
    titulo_completo = models.CharField(max_length=300, blank=True)
    numero_paginas = models.PositiveIntegerField(default=0)
    resumen = models.TextField(max_length=2000, blank=True)
    fecha_publicacion = models.DateField(blank=True, null=True)    
    idioma = LanguageField(default='es')

    # Informacion sobre edicion y editorial
    numero_edicion = models.PositiveSmallIntegerField(default=1)
    editorial = models.ForeignKey(Editorial, blank=True, null=True)
  
    # Algunos libros pueden tener multiples autores
    autores = models.ManyToManyField('Autor') 
    
    # Generos del libro
    generos = models.ManyToManyField('Genero')

    # Ruta del ebook en los distintos formatos
    epub = models.FileField(upload_to='ebooks/epub/', blank=True)
    mobi = models.FileField(upload_to='ebooks/mobi/', blank=True)
 
    # ISBN del libro.
    isbn = ISBNField(blank=True)
    
    # Precio del libro
    precio = models.DecimalField(max_digits=6, decimal_places=2)

    class META:
        ordering = ['-fecha_publicacion']

    def get_absolute_url(self):
        return reverse('libro-detail', args=[str(self.id),])

    def __str__(self):
        return self.titulo




