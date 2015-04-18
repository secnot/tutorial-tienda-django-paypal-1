from django.contrib import admin
from libros.models import (Libro, Autor, Editorial, Genero)
# Register your models here.



class EditorialAdmin(admin.ModelAdmin):
    pass

class AutorAdmin(admin.ModelAdmin):
    pass

class LibroAdmin(admin.ModelAdmin):
    pass

class GeneroAdmin(admin.ModelAdmin):
    pass


admin.site.register(Genero, GeneroAdmin)
admin.site.register(Autor, AutorAdmin)
admin.site.register(Libro, LibroAdmin)
admin.site.register(Editorial, EditorialAdmin)

