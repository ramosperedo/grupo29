from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import ModelForm
<<<<<<< HEAD
from .models import Libro, Autor, Editorial, Genero, Capitulo, Novedad, Trailer, Tarjeta, TipoTarjeta
from datetime import date, datetime
=======
from .models import Libro, Autor, Editorial, Genero, Capitulo, Novedad, Trailer, Tarjeta, TipoTarjeta, Perfil
from datetime import date

>>>>>>> luisbranch6

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['idSuscriptor','nombre']
        labels = {'nombre':'Nombre'}
        widgets = {
            'idSuscriptor' : forms.HiddenInput(),
            'nombre' : forms.TextInput(attrs={'class':'form-control'})
        }
    def clean_idSuscriptor(self):
        idSuscriptor = self.cleaned_data['idSuscriptor']
        if idSuscriptor is None:
            return self.fields['idSuscriptor'].initial
        return idSuscriptor

class TrailerForm(forms.ModelForm):
    archivo = forms.FileField(required=False, label=('Ingrese un archivo'))
    archivoVideo = forms.FileField(required=False, label=('Ingrese un Video'))
    class Meta:
        model = Trailer
        fields = ['titulo','idLibro','descripcion','archivo','archivoVideo']
        labels = {'titulo':'Titulo','idLibro':'Libro','descripcion':'Descripcion'}
        widgets = {
            'titulo' : forms.TextInput(attrs={'class':'form-control'}),
            'idLibro' : forms.Select(attrs={'class':'form-control'}),
            'descripcion' : forms.Textarea(attrs={'class':'form-control'})
        }

class NovedadForm(forms.ModelForm):
    archivo = forms.FileField(required=False, label=('Ingrese una Imagen'))
    archivoVideo = forms.FileField(required=False, label=('Ingrese un Video'))
    class Meta:
        model = Novedad
        fields = ['titulo','descripcion','archivo','archivoVideo']
        labels = {'titulo':'Titulo','descripcion':'Descripcion'}
        widgets = {
            'titulo' : forms.TextInput(attrs={'class':'form-control'}),
            'descripcion' : forms.Textarea(attrs={'class':'form-control'})
        }

class AutorForm(forms.ModelForm):
    class Meta:
        model = Autor
        fields = ['nombre']
        labels = {'nombre' : 'Nombre'}
        widgets = {'nombre' : forms.TextInput(attrs={'class':'form-control'})}

class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ['nombre']
        labels = {'nombre' : 'Nombre'}
        widgets = {'nombre' : forms.TextInput(attrs={'class':'form-control'})}

class EditorialForm(forms.ModelForm):
    class Meta:
        model = Editorial
        fields = ['nombre']
        labels = {'nombre' : 'Nombre'}
        widgets = {'nombre' : forms.TextInput(attrs={'class':'form-control'})}

class CapituloForm(forms.ModelForm):
    archivo = forms.FileField(required=True, label=('Ingrese el Capitulo'))
    class Meta:
        model = Capitulo
        fields = ['idLibro','nombre','numero','archivo','fechaLanzamiento','fechaVencimiento']
        labels = {'nombre':'Nombre','numero':'Numero de capitulo','fechaLanzamiento':'Fecha de Lanzamiento','fechaVencimiento':'Fecha de Vencimiento'}
        widgets = {
            'idLibro' : forms.HiddenInput(),
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'numero' : forms.NumberInput(attrs={'class':'form-control'}),
            'fechaLanzamiento' : forms.SelectDateWidget(attrs={'class':'form-control'}),
            'fechaVencimiento' : forms.SelectDateWidget(attrs={'class':'form-control'})
        }
    def clean_idLibro(self):
        idLibro = self.cleaned_data['idLibro']
        if idLibro is None:
            return self.fields['idLibro'].initial
        return idLibro

class LibroForm(forms.ModelForm):
    foto = forms.FileField(required=False)
    class Meta:
        model = Libro
        fields = ['nombre','isbn','idAutor','idGenero','idEditorial','descripcion','foto']
        labels = {
            'nombre' : 'Nombre',
            'isbn' : 'isbn',
            'idAutor' : 'Autor',
            'idGenero' : 'Genero',
            'idEditorial' : 'Editorial',
            'descripcion' : 'Descripcion'
        }
        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'isbn' : forms.NumberInput(attrs={'class':'form-control'}),
            'idAutor' : forms.Select(attrs={'class':'form-control','required':'true'}),
            'idGenero' : forms.Select(attrs={'class':'form-control','required':'true'}),
            'idEditorial' : forms.Select(attrs={'class':'form-control','required':'true'}),
            'descripcion' : forms.Textarea(attrs={'class':'form-control'})
        }

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if len(str(isbn))!=10 and len(str(isbn))!=13:
            raise forms.ValidationError("El isbn debe ser de 10 o 13 digitos")
        return isbn


User = get_user_model()

class UserAdminCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email',) #'full_name',)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class UserAdminChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'password', 'active', 'admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

#class LoginForm(forms.Form):
#    username = forms.EmailField(label='E-mail')
#    password = forms.CharField(widget=forms.PasswordInput)

CHOICES = ((0, 'Elija uno'),(1, 'MasterCard'),(2, 'American Express'),(3, 'Visa'),)

class RegisterForm(forms.Form):
    nombre = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label=('Nombre'))
    apellido = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control'}), label=('Apellido'))
    email    = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}), label=('E-mail'))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label=('Contraseña'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control'}), label=('Confirmar contraseña'))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("Este email ya se encuentra registrado")
        return email

    def clean(self):
        data = self.cleaned_data
        password = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if password2 != password:
            raise forms.ValidationError("las contraseñas no coinciden.")
        return data

class RegisterForm2(forms.Form):
    dni = forms.IntegerField(max_value=99999999, min_value=1000000, widget=forms.NumberInput(attrs={'class':'form-control'}), label=('Dni Titular'))
    numero = forms.IntegerField(max_value=9999999999999999, min_value=1000000000000000, widget=forms.NumberInput(attrs={'class':'form-control'}), label=('Numero de Tarjeta'))
    clave = forms.IntegerField(max_value=999, min_value=100, widget=forms.NumberInput(attrs={'class':'form-control'}), label=('Clave'))
    fechaVencimiento = forms.DateField(required=True,label='Fecha Vencimiento',widget=forms.SelectDateWidget(attrs={'class':'form-control'}))
    tipo = forms.ChoiceField(choices=CHOICES, label='Tipo de Trajeta')

    def clean_dni(self):
        dniBuscar = self.cleaned_data.get('dni')
        obj = Tarjeta.objects.filter(dni=dniBuscar)
        if obj:
            raise forms.ValidationError("Este dni ya esta registrado")
        return dniBuscar
    def clean_fechaVencimiento(self):
        fecha = self.cleaned_data.get('fechaVencimiento')
        if fecha < date.today():
            raise forms.ValidationError("la fecha tiene que ser mayor a la actual")
        return fecha

class RegisterForm3(forms.Form):
    premium = forms.BooleanField(required=False) 

class SuscriptorForm(forms.ModelForm):
    premium = forms.BooleanField(required=False) 
    class Meta:
        model = User
        fields = ('nombre', 'apellido', 'email', 'premium')
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'email': 'E-mail'
        }
        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'apellido' : forms.TextInput(attrs={'class':'form-control'}),
            'email' : forms.EmailInput(attrs={'class':'form-control'})
        }

class TarjetaForm(forms.ModelForm):
    fechaVencimiento = forms.DateField(required=True,label='Fecha Vencimiento',widget=forms.SelectDateWidget(attrs={'class':'form-control'}))
    class Meta:
        model = Tarjeta
        fields = ('dni', 'numero', 'clave', 'fechaVencimiento', 'tipo')
        labels = {
            'dni' : 'Dni Titular',
            'numero': 'Numero de Tarjeta',
            'fechaVencimiento': 'Fecha de Vencimiento'
        }
        widgets = {
            'dni' : forms.NumberInput(attrs={'class':'form-control'}),
            'numero' : forms.NumberInput(attrs={'class':'form-control'}),
            'clave' : forms.NumberInput(attrs={'class':'form-control'}),
            'fechaVencimiento': forms.SelectDateWidget(attrs={'class':'form-control'}),
            'tipo': forms.Select(choices=CHOICES),
        }
    def clean_fechaVencimiento(self):
        fecha = self.cleaned_data.get('fechaVencimiento')
        if fecha < date.today():
            raise forms.ValidationError("la fecha tiene que ser mayor a la actual")
        return fecha
class TipoTarjetaForm(forms.ModelForm):
    class Meta:
        model = TipoTarjeta
        fields = ('nombre',)
        