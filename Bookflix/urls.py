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

    path('', views.welcome),
    path('createBook/', views.createBook),
    path('editBook/<int:libro_id>', views.editBook),
    path('deleteBook/<int:libro_id>', views.deleteBook),
    path('listBooks/', views.listBooks),
    path('createAutor/', views.createAutor),
    path('createGenero/', views.createGenero),
    path('createCapitulo/', views.createCapitulo),
    path('createEditorial/', views.createEditorial),
    path('createNovedad/', views.createNovedad),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),

    path('admin/', admin.site.urls)
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS)