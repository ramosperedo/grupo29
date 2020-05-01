from django.db import models

# Create your models here.

class Libro(models.Model):
    nombre = models.CharField(max_length=50)
    autor = models.CharField(max_length=50)
    isbn = models.IntegerField(max_length=13)
    genero = models.CharField(max_length=20)
    editorial = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=250)

class TipoTarjeta(models.Model):
    nombre = models.CharField(max_length=20)

class Tarjeta(models.Model):
    nombreTitular = models.CharField(max_length=50)
    numero = models.IntegerField(max_length=16)
    clave = models.IntegerField(max_length=3)
    fechaVencimiento = models.IntegerField(max_length=4)
    idTipoTarjeta = models.ForeignKey(TipoTarjeta)

class Suscriptor(models.Model):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    clave = models.CharField(max_length=256)
    email = models.CharField(max_length=100)
    idTarjeta = models.ForeignKey(Tarjeta)
    premium = models.IntegerField(max_length=1)

class Perfil(models.Model):
    nombre = models.CharField(max_length=50)
    foto = models.CharField(max_length=50)
    idSuscriptor = models.ForeignKey(Suscriptor)

class Configuracion(models.Model):
    maximoPremium= models.IntegerField(max_length=1)
    maximoStandar= models.IntegerField(max_length=1)

class Favoritos(models.Model):
    idPerfil = models.ForeignKey(Perfil)
    idLibro = models.ForeignKey(Libro)

class Recomendaciones(models.Model):
    idPerfil = models.ForeignKey(Perfil)
    idLibro = models.ForeignKey(Libro)

class Capitulos(models.Model):
    idLibro = models.ForeignKey(Libro)
    nombre = models.CharField(max_length=100) 

class Historial(models.Model):
    idPerfil = models.ForeignKey(Perfil)
    idLibro = models.ForeignKey(Libro)