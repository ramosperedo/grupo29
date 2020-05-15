from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.forms import ModelForm
from .models import Libro, Autor, Editorial, Genero, Capitulo, Novedad, Trailer, Tarjeta, TipoTarjeta

class NovedadForm(forms.ModelForm):
    archivo = forms.FileField(required=False)
    class Meta:
        model = Novedad
        fields = ['titulo','descripcion','archivo']
        labels = {'titulo':'Titulo','descripcion':'Descripcion','archivo':'Ingrese el archivo'}
        widgets = {
            'titulo' : forms.TextInput(attrs={'class':'form-control'}),
            'descripcion' : forms.Textarea(attrs={'class':'form-control'}),
            'archivo' : forms.FileInput(attrs={'class':'form-control'})
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
    class Meta:
        model = Capitulo
        fields = ['nombre','idLibro','archivo']
        labels = {'nombre':'Nombre','idLibro':'Libro','archivo':'Ingrese el capitulo'}
        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'idLibro' : forms.Select(attrs={'class':'form-control'}),
            'archivo' : forms.FileInput(attrs={'class':'form-control'})
        }

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
            'descripcion' : 'Descripcion',
            'foto' : 'Ingrese una foto'
        }
        widgets = {
            'nombre' : forms.TextInput(attrs={'class':'form-control'}),
            'isbn' : forms.NumberInput(attrs={'class':'form-control'}),
            'idAutor' : forms.Select(attrs={'class':'form-control'}),
            'idGenero' : forms.Select(attrs={'class':'form-control'}),
            'idEditorial' : forms.Select(attrs={'class':'form-control'}),
            'descripcion' : forms.Textarea(attrs={'class':'form-control'}),
            'foto' : forms.FileInput(attrs={'class':'form-control'})
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

class LoginForm(forms.Form):
    username = forms.EmailField(label='E-mail')
    password = forms.CharField(widget=forms.PasswordInput)

CHOICES = ((0, 'Elija uno'),(1, 'MasterCard'),(2, 'American Express'),(3, 'Visa'),)

class RegisterForm(forms.Form):
    nombre = forms.CharField()
    apellido = forms.CharField()
    email    = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar password', widget=forms.PasswordInput)

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
    dni = forms.IntegerField(max_value=99999999, min_value=1000000)
    numero = forms.IntegerField(max_value=9999999999999999, min_value=1000000000000000, label='Numero de Tarjeta')
    clave = forms.IntegerField(max_value=999, min_value=100)
    fechaVencimiento = forms.DateField(required=True,label='Fecha Vencimiento',widget=forms.SelectDateWidget)
    tipo = forms.ChoiceField(choices=CHOICES, label='Tipo de Trajeta')

class RegisterForm3(forms.Form):
    premium = forms.BooleanField(required=False) 

class SuscriptorForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('nombre', 'apellido', 'email')

class TarjetaForm(forms.ModelForm):
    class Meta:
        model = Tarjeta
        fields = ('dni', 'numero', 'clave', 'fechaVencimiento', 'tipo')
        labels = {
            'numero': 'Numero de Tarjeta',
            'fechaVencimiento': 'Fecha de Vencimiento'
        }
        widgets = {
            'fechaVencimiento': forms.SelectDateWidget(),
            'tipo': forms.Select(choices=CHOICES),
        }
class TipoTarjetaForm(forms.ModelForm):
    class Meta:
        model = TipoTarjeta
        fields = ('nombre',)
        