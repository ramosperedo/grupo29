from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from .forms import RegisterForm, LoginForm, LibroForm, AutorForm, GeneroForm, EditorialForm, CapituloForm, NovedadForm
from .models import Libro, Novedad
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login, logout as do_logout
from app.models import TarjetaManager

def createBook(request):
    # Creamos un formulario vacío
    form = LibroForm()
    # Comprobamos si se ha enviado el formulario
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = LibroForm(request.POST,request.FILES)
        # Si el formulario es válido...
        if form.is_valid():
            # Guardamos el formulario pero sin confirmarlo,
            # así conseguiremos una instancia para manejarla
            instancia = form.save(commit=False)
            # Podemos guardarla cuando queramos
            instancia.save()
            # Después de guardar redireccionamos a la lista
            return redirect('/')
    # Si llegamos al final renderizamos el formulario
    return render(request, "admin/createBook.html", {'form': form})

def editBook(request, libro_id):
    # Recuperamos la instancia de la persona
    instancia = Libro.objects.get(id=libro_id)
    # Creamos el formulario con los datos de la instancia
    form = LibroForm(instance=instancia)
    # Comprobamos si se ha enviado el formulario
    if request.method == "POST":
        # Actualizamos el formulario con los datos recibidos
        form = LibroForm(request.POST,request.FILES, instance=instancia)
        # Si el formulario es válido...
        if form.is_valid():
            # Guardamos el formulario pero sin confirmarlo,
            # así conseguiremos una instancia para manejarla
            instancia = form.save(commit=False)
            # Podemos guardarla cuando queramos
            instancia.save()
            # Después de guardar redireccionamos a la lista
            return redirect('shared/listOfBooks.html')
    # Si llegamos al final renderizamos el formulario
    return render(request, "admin/editBook.html", {'form': form})

def deleteBook(request, libro_id):
    # Recuperamos la instancia de la persona y la borramos
    instancia = Libro.objects.get(id=libro_id)
    instancia.delete()
    # Después redireccionamos de nuevo a la lista
    return redirect('shared/listOfBooks.html')

def listBooks(request):
    libros = Libro.objects.all()
    return render(request, "shared/listOfBooks.html", {'libros': libros})

def createAutor(request):
    form = AutorForm()
    if request.method == "POST":
        form = AutorForm(request.POST)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('/')
    return render(request, "admin/createAutor.html", {'form': form})

def createGenero(request):
    form = GeneroForm()
    if request.method == "POST":
        form = GeneroForm(request.POST)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('/')
    return render(request, "admin/createGenero.html", {'form': form})

def createEditorial(request):
    form = EditorialForm()
    if request.method == "POST":
        form = EditorialForm(request.POST)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('/')
    return render(request, "admin/createEditorial.html", {'form': form})

def createNovedad(request):
    form = NovedadForm()
    if request.method == "POST":
        form = NovedadForm(request.POST,request.FILES)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('/')
    return render(request, "admin/createNovedad.html", {'form': form})

def createCapitulo(request):
    form = CapituloForm()
    if request.method == "POST":
        form = CapituloForm(request.POST)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('/')
    return render(request, "admin/createCapitulo.html", {'form': form})

def login(request):
    form = AuthenticationForm()
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                do_login(request, user)
                if request.user.is_superuser == 1:
                    return render(request, "users/welcome.html")
                else:
                    return render(request, "users/home.html")
    return render(request, "users/login.html", {'form': form})

User = get_user_model()
def register(request):
    form = RegisterForm(request.POST or None)
    context = {
        "form": form
    }
    if form.is_valid():
        print(form.cleaned_data)
        nombre = form.cleaned_data.get("nombre")
        apellido  = form.cleaned_data.get("apellido")
        email  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")

        tipo = form.cleaned_data.get("tipo")

        dni = form.cleaned_data.get("dni")
        numero = form.cleaned_data.get("numero")
        clave = form.cleaned_data.get("clave")
        fechaVencimiento = form.cleaned_data.get("fechaVencimiento")
        """form.revisandoDatosTarjeta(dni,numero,clave,fechaVencimiento)"""

        new_tarj = TarjetaManager.create_tarjeta(dni,numero,clave,fechaVencimiento,tipo)
        new_user  = User.objects.create_suscriptor(nombre, apellido, email, password,new_tarj.id)
        print(new_user)
        if new_user is not None:
            do_login(request, new_user)
            return redirect('/')

    return render(request, "users/register.html", context)


def welcome(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
            return render(request, "users/welcome.html")
        else:
            return render(request, "users/home.html")
    return redirect('/login')


def logout(request):
    do_logout(request)
    return redirect('/')
