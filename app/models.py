from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, nombre=None, apellido=None, password=None, is_active=True, is_staff=False, is_admin=False, is_superuser=False, is_premium=False, idTarjeta=None):
        if not email:
            raise ValueError("campo email obligatorio")
        if not password:
            raise ValueError("campo contraseña obligatorio")

        user_obj = self.model(
            email = self.normalize_email(email)
        )
        user_obj.nombre = nombre
        user_obj.apellido = apellido
        user_obj.set_password(password) # change user password
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.superuser = is_superuser
        user_obj.premium = is_premium
        user_obj.idTarjeta = idTarjeta
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
                nombre="",
                apellido="",
                password=password,
                is_staff=True,
                is_admin=True,
                is_superuser=True,
                is_premium=True,
                idTarjeta=0
        )
        return user
    def create_suscriptor(self,nombre, apellido, email, premium, password=None,idTarjeta=None):
        user = self.create_user(
                email,
                nombre,
                apellido,
                password=password,
                is_premium=premium,
                idTarjeta=idTarjeta
        )
        return user

class TipoTarjetaManager(models.Manager):
    def create_tipo_tarjeta(self,nombre):
        tipo_tarjeta_obj = TipoTarjeta()
        tipo_tarjeta_obj.nombre = nombre
        tipo_tarjeta_obj.save()
        return tipo_tarjeta_obj

class TipoTarjeta(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=20)

    objects = TipoTarjetaManager()

class TarjetaManager(models.Manager):
    def create_tarjeta(dni,numero,clave,fechaVencimiento,tipo):
        tarjeta_obj = Tarjeta()
        tarjeta_obj.dni = dni
        tarjeta_obj.numero = numero
        tarjeta_obj.clave =clave
        tarjeta_obj.fechaVencimiento = fechaVencimiento
        tarjeta_obj.tipo = tipo
        tarjeta_obj.save()
        return tarjeta_obj

class Tarjeta(models.Model):
    id = models.AutoField(primary_key=True)
    dni = models.IntegerField(default=0,unique=True)
    numero = models.IntegerField(default=0)
    clave = models.IntegerField(default=0)
    fechaVencimiento = models.DateField()
    tipo = models.IntegerField(default=0)

    objects = TarjetaManager()

class User(AbstractBaseUser):
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField(max_length=255,unique=True)
    active = models.BooleanField(default=True) #can login
    staff = models.BooleanField(default=False) #staff user non superuser
    admin = models.BooleanField(default=False) #superuser
    superuser = models.BooleanField(default=False)
    idTarjeta = models.IntegerField(default=0)
    premium = models.BooleanField(default=False)
    dateCreate = models.DateField(auto_now=True)

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

class Autor(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.nombre

class Genero(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.nombre

class Editorial(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.nombre

class Libro(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,unique=True)
    isbn = models.IntegerField(unique=True)
    idAutor = models.ForeignKey(Autor,on_delete=models.CASCADE,null=True,blank=True)
    idGenero = models.ForeignKey(Genero,on_delete=models.CASCADE,null=True,blank=True)
    idEditorial = models.ForeignKey(Editorial,on_delete=models.CASCADE,null=True,blank=True)
    descripcion = models.CharField(max_length=1000)
    foto = models.ImageField(upload_to='static/images/',null=True,blank=True)
    vistos = models.IntegerField(null=True, default=0)
    ultimoCapitulo = models.BooleanField(default=False)
    LibroEnCapitulos = models.BooleanField(default=False)
    fechaVencimientoFinal = models.DateField(null=True)
    lecturaEnCurso = models.IntegerField(default=0)
    lecturaTerminada = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

class Capitulo(models.Model):
    id = models.AutoField(primary_key=True)
    idLibro = models.ForeignKey(Libro,on_delete=models.CASCADE,blank=False)
    nombre = models.CharField(max_length=50,unique=True,null=True)
    numero = models.IntegerField(null=True,default=0)
    archivo = models.FileField(upload_to='static/file/')
    fechaLanzamiento = models.DateField()
    fechaVencimiento = models.DateField()

    def __str__(self):
        return self.nombre

class PerfilManager(models.Manager):
    def create_perfil(nombre,idSuscriptor):
        perfil_obj = Perfil()
        perfil_obj.nombre = nombre
        perfil_obj.idSuscriptor = idSuscriptor
        perfil_obj.save()
        return perfil_obj

class Perfil(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50,unique=True)
    foto = models.CharField(max_length=50,null=True,blank=True)
    idSuscriptor = models.ForeignKey(User,on_delete=models.CASCADE)

    objects = PerfilManager()
    
    def __str__(self):
        return self.nombre

class Configuracion(models.Model):
    id = models.AutoField(primary_key=True)
    maximoPremium = models.IntegerField(default=4)
    maximoStandar = models.IntegerField(default=2)

class Favoritos(models.Model):
    id = models.AutoField(primary_key=True)
    idPerfil = models.ForeignKey(Perfil,on_delete=models.CASCADE)
    idLibro = models.ForeignKey(Libro,on_delete=models.CASCADE)

class Recomendaciones(models.Model):
    id = models.AutoField(primary_key=True)
    idPerfil = models.ForeignKey(Perfil,on_delete=models.CASCADE)
    idLibro = models.ForeignKey(Libro,on_delete=models.CASCADE)

class Historial(models.Model):
    id = models.AutoField(primary_key=True)
    idPerfil = models.ForeignKey(Perfil,on_delete=models.CASCADE)
    idCapitulo = models.ForeignKey(Capitulo,on_delete=models.CASCADE)
    terminado = models.BooleanField(default=False)

class Novedad(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=50,unique=True)
    descripcion = models.CharField(max_length=1000)
    archivo = models.ImageField(upload_to='static/images/',null=True,blank=True)
    archivoVideo = models.FileField(upload_to='static/videos/',null=True,blank=True)

    def __str__(self):
        return self.titulo

class PerfilActual(models.Model):
    id = models.AutoField(primary_key=True)
    idPerfil = models.ForeignKey(Perfil,on_delete=models.CASCADE)
    idSuscriptor = models.ForeignKey(User,on_delete=models.CASCADE)
    
class Trailer(models.Model):
    id = models.AutoField(primary_key=True)
    idLibro = models.ForeignKey(Libro,on_delete=models.CASCADE,null=True,blank=True)
    titulo = models.CharField(max_length=50,unique=True)
    descripcion = models.CharField(max_length=1000)
    archivo = models.FileField(upload_to='static/file/',null=True,blank=True)
    archivoVideo = models.FileField(upload_to='static/videos/',null=True,blank=True)

    def __str__(self):
        return self.titulo

class Review(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length = 50)
    idPerfil = models.ForeignKey(Perfil, null = True, on_delete = models.SET_NULL)
    idLibro = models.ForeignKey(Libro, null = True, on_delete = models.CASCADE)
    texto = models.CharField(max_length = 256)
    puntaje = models.IntegerField(null = False, blank = False)
    spoiler = models.BooleanField(default = False)
    spoilerAdmin = models.BooleanField(default = False)

class Favorito(models.Model):
    id = models.AutoField(primary_key=True)
    idPerfil = models.ForeignKey(Perfil,on_delete=models.CASCADE)
    idLibro = models.ForeignKey(Libro,on_delete=models.CASCADE)