from django.conf.urls import include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from libros.views import LibroLatestView

urlpatterns = [
    # Examples:
    # url(r'^$', 'tiendalibros.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', LibroLatestView.as_view(), name="index"),
    url(r'^$', LibroLatestView.as_view(), name="index"),
    url(r'^admin/', view = include(admin.site.urls)),

    # App includes
    url(r'^libros/',    include('libros.urls')),
    url(r'^pagos/',     include('pagos.urls')),
]

# Servir imagenes y archivos durante desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

