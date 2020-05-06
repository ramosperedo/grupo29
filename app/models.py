from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False, is_superuser=False, is_premium=False):
        if not email:
            raise ValueError("campo email obligatorio")
        if not password:
            raise ValueError("campo contraseña obligatorio")

        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.set_password(password) # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.superuser = is_superuser
        user_obj.premium = is_premium
        user_obj.save(using=self._db)
        return user_obj
    
    def create_staffuser(self, email, password=None):
        user = self.create_user(
                email,
                password=password,
                is_staff=True
        )
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
                email,
                password=password,
                is_staff=True,
                is_admin=True,
                is_superuser=True,
                is_premium=True
        )
        return user
    def create_suscriptor(self, email, password=None):
        user = self.create_user(
                email,
                password=password
        )
        return user

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

class User(AbstractBaseUser):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(max_length=255,unique=True)
    active = models.BooleanField(default=True) #can login
    staff = models.BooleanField(default=False) #staff user non superuser
    admin = models.BooleanField(default=False) #superuser
    superuser = models.BooleanField(default=False)
    idTarjeta = models.ForeignKey(Tarjeta,on_delete=models.CASCADE, null=True)
    premium = models.BooleanField(default=False)

    USERNAME_FIELD = 'email' #username
    #USERNAME_FIELD and password are required by default
    REQUIRED_FIELDS = [] #'full_name' python manage.py createsuperuser

    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.nombre + self.apellido

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.admin

    def has_module_perms(self, app_Label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin
    
    @property
    def is_active(self):
        return self.active

    @property
    def is_superuser(self):
        return self.superuser    
    
    @property
    def is_premium(self):
        return self.premium

class Libro(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    autor = models.CharField(max_length=50)
    isbn = models.IntegerField(unique=True)
    genero = models.CharField(max_length=20)
    editorial = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=250)
    foto = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.nombre

class Perfil(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    foto = models.CharField(max_length=50)
    idSuscriptor = models.ForeignKey(User,on_delete=models.CASCADE)

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