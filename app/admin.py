from django.contrib import admin
from app.models import Libro, Novedad, Trailer, Suscriptor

# Register your models here.

admin.site.register(Libro)
admin.site.register(Novedad)
admin.site.register(Trailer)
admin.site.register(Suscriptor)