from django.contrib.auth import authenticate, get_user_model
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.http import is_safe_url
from .forms import RegisterForm, RegisterForm2, RegisterForm3, LoginForm, LibroForm, AutorForm, GeneroForm, EditorialForm, CapituloForm, NovedadForm, SuscriptorForm, TarjetaForm, TipoTarjetaForm
from .models import Libro, Novedad, Trailer, Autor, Editorial, Genero, TarjetaManager, Tarjeta, TipoTarjeta
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as do_login, logout as do_logout
from django.contrib import messages

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
            return redirect('/listBooks')
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
            return redirect('/listBooks')
    # Si llegamos al final renderizamos el formulario
    return render(request, "admin/editBook.html", {'form': form})

def deleteBook(request, libro_id):
    # Recuperamos la instancia de la persona y la borramos
    instancia = Libro.objects.get(id=libro_id)
    instancia.delete()
    # Después redireccionamos de nuevo a la lista
    return redirect('/listBooks')

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
            return redirect('/listAutores')
    return render(request, "admin/createAutor.html", {'form': form})

def deleteAutor(request, autor_id):
    instancia = Autor.objects.get(id=autor_id)
    instancia.delete()
    return redirect('/listAutores')

def listAutores(request):
    autores = Autor.objects.all()
    return render(request, "admin/listOfAutores.html", {'autores': autores})

def createGenero(request):
    form = GeneroForm()
    if request.method == "POST":
        form = GeneroForm(request.POST)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('/listGeneros')
    return render(request, "admin/createGenero.html", {'form': form})

def deleteGenero(request, genero_id):
    instancia = Genero.objects.get(id=genero_id)
    instancia.delete()
    return redirect('/listGeneros')

def listGeneros(request):
    generos = Genero.objects.all()
    return render(request, "admin/listOfGeneros.html", {'generos': generos})

def createEditorial(request):
    form = EditorialForm()
    if request.method == "POST":
        form = EditorialForm(request.POST)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('/listEditoriales')
    return render(request, "admin/createEditorial.html", {'form': form})

def deleteEditorial(request, editorial_id):
    instancia = Editorial.objects.get(id=editorial_id)
    instancia.delete()
    return redirect('/listEditoriales')

def listEditoriales(request):
    editoriales = Editorial.objects.all()
    return render(request, "admin/listOfEditoriales.html", {'editoriales': editoriales})

def createNovedad(request):
    form = NovedadForm()
    if request.method == "POST":
        form = NovedadForm(request.POST,request.FILES)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('/listNovedades')
    return render(request, "admin/createNovedad.html", {'form': form})

def editNovedad(request, novedad_id):
    instancia = Novedad.objects.get(id=novedad_id)
    form = NovedadForm(instance=instancia)
    if request.method == "POST":
        form = NovedadForm(request.POST,request.FILES, instance=instancia)
        if form.is_valid():
            instancia = form.save(commit=False)
            instancia.save()
            return redirect('/listNovedades')
    return render(request, "admin/editNovedad.html", {'form': form})

def deleteNovedad(request, novedad_id):
    instancia = Novedad.objects.get(id=novedad_id)
    instancia.delete()
    return redirect('/listNovedades')

def listNovedades(request):
    novedades = Novedad.objects.all()
    return render(request, "shared/listOfNovedades.html", {'novedades': novedades})

def loadFile(request, libro_id):
    return render(request, "admin/loadFile.html", {'libro_id': libro_id})

def loadCapitulo(request, libro_id):
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
                    return render(request, "users/perfiles.html")
    return render(request, "users/login.html", {'form': form})

User = get_user_model()
def register(request):
    form = RegisterForm(request.POST or None)
    form2 = RegisterForm2(request.POST or None)
    form3 = RegisterForm3(request.POST or None)
    context = {
        "form": form, "form2": form2, "form3": form3
    }
    if form.is_valid() and form2.is_valid() and form3.is_valid():
        print(form.cleaned_data)
        nombre = form.cleaned_data.get("nombre")
        apellido  = form.cleaned_data.get("apellido")
        email  = form.cleaned_data.get("email")
        password  = form.cleaned_data.get("password")
        premium = form3.cleaned_data.get("premium")
        tipo = form2.cleaned_data.get("tipo")
        dni = form2.cleaned_data.get("dni")
        numero = form2.cleaned_data.get("numero")
        clave = form2.cleaned_data.get("clave")
        fechaVencimiento = form2.cleaned_data.get("fechaVencimiento")

        new_tarj = TarjetaManager.create_tarjeta(dni,numero,clave,fechaVencimiento,tipo)
        new_user  = User.objects.create_suscriptor(nombre, apellido, email, premium, password,new_tarj.id)
        print(new_user)#en la anterior linea el orden de los datos del usuario no son en ese orden
        if new_user is not None:#pero por un bug raro lo tube que cambiar para que registre bien
            do_login(request, new_user)#si se llega a arreglar el orden es nombre, apellido, email, pass, idtarjeta
            return redirect('/')

    return render(request, "users/register.html", context)

def editarSuscriptor(request, sus_id):
    instancia = User.objects.get(id=sus_id)
    instancia2 = Tarjeta.objects.get(id=instancia.idTarjeta)
    form = SuscriptorForm(instance=instancia)
    form2 = TarjetaForm(instance=instancia2)
    if request.method == "POST":
        form = SuscriptorForm(request.POST, instance=instancia)
        form2 = TarjetaForm(request.POST, instance=instancia2)
        if form.is_valid() and form2.is_valid():
            instancia = form.save(commit=False)
            instancia2 = form2.save(commit=False)
            instancia.save()
            instancia2.save()
            messages.success(request, 'se modificó sus datos')
    return render(request, "users/editar.html", {'form': form,'form2': form2})

def infoSuscriptor(request, num=0):
    try:
        datosSuscriptor = User.objects.get(pk=num)
        print(datosSuscriptor.email)
        datosTarjeta = Tarjeta.objects.get(id=datosSuscriptor.idTarjeta)
        print(datosTarjeta.dni)
        nombreTipoTarjeta = TipoTarjeta.objects.get(id=datosTarjeta.tipo)
        print(nombreTipoTarjeta.nombre)
    except Exception as e:
        return render(request, "shared/infoSuscriptor.html",{'mensaje':"no se encontro al suscriptor cod:1"})

    if request.user.id == num:
        if datosSuscriptor is not None:
            return render(request, "shared/infoSuscriptor.html",{'datos':datosSuscriptor,'tarjeta':datosTarjeta,'tipo':nombreTipoTarjeta, 'mensaje':""})
        else:
            return render(request, "shared/infoSuscriptor.html",{'mensaje':"no se encontro al suscriptor cod:2"})
    else:
        return render(request, "shared/infoSuscriptor.html",{'mensaje':"no se encontro al suscriptor cod:3"})


def inicio(request):
    if request.user.is_authenticated:
        if request.user.is_superuser == 1:
            return render(request, "users/welcome.html")
        else:
            return render(request, "users/home.html")
    return redirect('/login')

def logout(request):
    do_logout(request)
    return redirect('/')
