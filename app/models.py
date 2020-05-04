from django.db import models

# Create your models here.

class Libro(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    autor = models.CharField(max_length=50)
    isbn = models.IntegerField(unique=True)
    genero = models.CharField(max_length=20)
    editorial = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=250)
    foto = models.CharField(max_length=100, null=True)

class TipoTarjeta(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)

class Tarjeta(models.Model):
    id = models.AutoField(primary_key=True)
    nombreTitular = models.CharField(max_length=50)
    numero = models.IntegerField()
    clave = models.IntegerField()
    fechaVencimiento = models.IntegerField()
    idTipoTarjeta = models.ForeignKey(TipoTarjeta,on_delete=models.CASCADE)

class Suscriptor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    clave = models.CharField(max_length=256)
    email = models.CharField(max_length=100, unique=True)
    idTarjeta = models.ForeignKey(Tarjeta,on_delete=models.CASCADE)
    premium = models.IntegerField()

class Perfil(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    foto = models.CharField(max_length=50)
    idSuscriptor = models.ForeignKey(Suscriptor,on_delete=models.CASCADE)

class Configuracion(models.Model):
    id = models.AutoField(primary_key=True)
    maximoPremium = models.IntegerField(default=4)
    maximoStandar = models.IntegerField(default=2)
    Premium = models.IntegerField(default=1)
    Standar = models.IntegerField(default=0)

class Favoritos(models.Model):
    id = models.AutoField(primary_key=True)
    idPerfil = models.ForeignKey(Perfil,on_delete=models.CASCADE)
    idLibro = models.ForeignKey(Libro,on_delete=models.CASCADE)

class Recomendaciones(models.Model):
    id = models.AutoField(primary_key=True)
    idPerfil = models.ForeignKey(Perfil,on_delete=models.CASCADE)
    idLibro = models.ForeignKey(Libro,on_delete=models.CASCADE)

class Capitulos(models.Model):
    id = models.AutoField(primary_key=True)
    idLibro = models.ForeignKey(Libro,on_delete=models.CASCADE)
    nombre = models.CharField(max_length=50)
    archivo = models.CharField(max_length=100)

class Historial(models.Model):
    id = models.AutoField(primary_key=True)
    idPerfil = models.ForeignKey(Perfil,on_delete=models.CASCADE)
    idLibro = models.ForeignKey(Libro,on_delete=models.CASCADE)

class Novedad(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)
    archivo = models.CharField(max_length=100)
    
class Trailer(models.Model):
    id = models.AutoField(primary_key=True)
    idLibro = models.ForeignKey(Libro,on_delete=models.CASCADE)
    titulo = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=150)
    archivo = models.CharField(max_length=100)