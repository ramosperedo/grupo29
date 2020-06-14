"""Bookflix URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from app import views

urlpatterns = [

    path('', views.inicio),
    path('createBook/', views.createBook),
    path('editBook/<int:libro_id>', views.editBook),
    path('deleteBook/<int:libro_id>', views.deleteBook),
    path('listBooks/', views.listBooks),
    path('loadLibroEnCapitulos/<int:libro_id>', views.loadLibroEnCapitulos),
    path('loadLibroCompleto/<int:libro_id>', views.loadLibroCompleto),
    path('createAutor/', views.createAutor),
    path('deleteAutor/<int:autor_id>', views.deleteAutor),
    path('listAutores/', views.listAutores),
    path('createGenero/', views.createGenero),
    path('deleteGenero/<int:genero_id>', views.deleteGenero),
    path('listGeneros/', views.listGeneros),
    path('createEditorial/', views.createEditorial),
    path('deleteEditorial/<int:editorial_id>', views.deleteEditorial),
    path('listEditoriales/', views.listEditoriales),
    path('createNovedad/', views.createNovedad),
    path('editNovedad/<int:novedad_id>', views.editNovedad),
    path('deleteNovedad/<int:novedad_id>', views.deleteNovedad),
    path('viewNovedad/<int:novedad_id>', views.viewNovedad),
    path('listNovedades/', views.listNovedades),
    path('createTrailer/', views.createTrailer),
    path('editTrailer/<int:trailer_id>', views.editTrailer),
    path('deleteTrailer/<int:trailer_id>', views.deleteTrailer),
    path('viewTrailer/<int:trailer_id>', views.viewTrailer),
    path('listTrailers/', views.listTrailers),
    path('register/', views.register),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('infoSuscriptor/', views.infoSuscriptor, name='infoSus'),
    path('perfiles/', views.administrarPerfiles),
    path('createPerfil/', views.createPerfil),
    path('inicio', views.inicio, name='inicio'),
    path('editarSuscriptor/<int:sus_id>', views.editarSuscriptor, name='editarsus'),
    path('historial/', views.historial, name='historial'),

    path('admin/', admin.site.urls)
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)