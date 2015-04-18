#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404

from django.views.generic import DetailView, ListView

from libros.models import Libro, Autor, Genero, Editorial
from django.db.models import Q

# Create your views here.


def get_libros_autor(autor):
    """Devuelve los demas libros del autor del libro"""
    return Libro.objects.filter(autores=autor)


def get_libros_recomendados(libro):
    """Devuelve libros recomendados similares a este"""
    # TODO: Implementar sistema de recomendaciones, por ahora 
    # solo devuelve los ultimos 20 libros añadidos
    return Libro.objects.filter()[:20] 


class LibroDetailView(DetailView):

    model = Libro
    template_name = 'libros/libro_detail.html'
    context_object_name = 'libro'
   
    def get_context_data(self, **kwargs):
        """Obtener mas libros del mismo autor"""
        context = super(LibroDetailView, self).get_context_data(**kwargs)
        libro = self.object 
        autor = libro.autores.first()
        context['libros_autor'] = get_libros_autor(autor)[:16]
        context['libros_recomendados'] = get_libros_recomendados(libro)
        return context


class AutorDetailView(DetailView):
    
    model = Autor
    template_name = 'libros/autor_detail.html'
    context_object_name = 'autor'

    def get_context_date(self, **kwargs):
        """Obtener todos los libros del autor"""
        context = super(AutorDetail, self). get
        context['libros_autor'] = get_libros_autor(self.object)
        return context


class EditorialListaLibrosView(ListView):
    """Listado de todos los libros de la editorial"""
    template_name = 'libros/editorial_libros_list.html'
    context_object_name = 'libro_list'
    pagination = 20

    def get_queryset(self):
        self.editorial = get_object_or_404(Editorial, pk=int(self.args[0])) 
        return Libro.objects.filter(editorial=self.editorial)

    def get_context_data(self):
        """Añadir al context la editorial para que aparezca en el template"""
        context = super(EditorialListaLibrosView, self).get_context_data(**kwargs)
        context['editorial'] = self.editorial
        return context
        

class GeneroListaLibrosView(ListView):
    """Lista de todos los libros del genero"""
    template_name = 'libros/genero_libros_list.html'
    context_object_name = 'libro_list'
    pagination = 20

    def get_queryset(self):
        self.genero = get_object_or_404(Editorial, pk=int(self.args[0]))
        return Libro.objects.filter(genero=self.genero)
   
    def get_context_data(self, **kwargs):
        """Añadir al contexto el genero para que aparezca en el template"""
        context = super(GeneroListaLibrosView, self).get_context_data(**kwargs)
        context['genero'] = self.genero
        return context


class LibroLatestView(ListView):
    """Lista de los ultimos libros añadidos que se usar como index de la
    aplicación"""

    template_name = 'libros/libros_latest.html'
    context_object_name = 'libro_list'
    pagination = 40

    def get_queryset(self):
        return Libro.objects.all()



